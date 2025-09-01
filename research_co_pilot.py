"""
Research Co-Pilot: A modular AI-powered research assistant
Built with LangChain to help users brainstorm and draft research papers
"""

import os
import subprocess
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

# LangChain imports
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

@dataclass
class ResearchContext:
    """Data structure to hold research context across agents"""
    broad_topic: str = ""
    research_questions: List[str] = None
    selected_papers: List[Dict] = None
    methodology_preferences: Dict = None
    draft_skeleton: str = ""
    final_paper: str = ""
    
    def __post_init__(self):
        if self.research_questions is None:
            self.research_questions = []
        if self.selected_papers is None:
            self.selected_papers = []
        if self.methodology_preferences is None:
            self.methodology_preferences = {}

class TopicAgent:
    """Agent responsible for refining broad topics into specific research questions"""
    
    def __init__(self, llm):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_template("""
        You are an expert research topic refinement specialist. Given a broad research topic, help refine it into 3-5 specific, focused research questions.
        
        Broad Topic: {topic}
        
        Your task:
        1. Analyze the broad topic
        2. Identify key areas that need research
        3. Formulate 3-5 specific, answerable research questions
        4. Ask 2-3 clarifying questions to better understand the user's research goals
        
        Format your response as:
        RESEARCH_QUESTIONS:
        - [Question 1]
        - [Question 2]
        - [Question 3]
        - [Question 4]
        - [Question 5]
        
        CLARIFYING_QUESTIONS:
        - [Question 1]
        - [Question 2]
        - [Question 3]
        
        ANALYSIS:
        [Brief analysis of why these questions are important and how they relate to the topic]
        """)
        
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    def refine_topic(self, topic: str) -> Dict[str, Any]:
        """Refine a broad topic into specific research questions"""
        print(f"🔍 Topic Agent: Analyzing topic '{topic}'...")
        
        response = self.chain.run(topic=topic)
        
        # Parse the response to extract research questions and clarifying questions
        questions = []
        clarifying = []
        analysis = ""
        
        lines = response.split('\n')
        current_section = ""
        
        for line in lines:
            line = line.strip()
            if 'RESEARCH_QUESTIONS:' in line:
                current_section = 'questions'
            elif 'CLARIFYING_QUESTIONS:' in line:
                current_section = 'clarifying'
            elif 'ANALYSIS:' in line:
                current_section = 'analysis'
            elif line.startswith('- ') and current_section == 'questions':
                questions.append(line[2:])
            elif line.startswith('- ') and current_section == 'clarifying':
                clarifying.append(line[2:])
            elif current_section == 'analysis' and line:
                analysis += line + " "
        
        return {
            'research_questions': questions,
            'clarifying_questions': clarifying,
            'analysis': analysis.strip()
        }
    
    def ask_clarifying_questions(self, clarifying_questions: List[str]) -> Dict[str, str]:
        """Ask clarifying questions and collect user responses"""
        print("\n📝 Topic Agent: Please answer these clarifying questions:")
        responses = {}
        
        for i, question in enumerate(clarifying_questions, 1):
            print(f"\n{i}. {question}")
            response = input(f"Your answer: ").strip()
            responses[f"q{i}"] = response
        
        return responses

class LiteratureAgent:
    """Agent responsible for fetching and summarizing relevant papers"""
    
    def __init__(self, llm):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_template("""
        You are an expert literature review specialist. Based on the research questions and topic, suggest relevant papers and provide summaries.
        
        Topic: {topic}
        Research Questions: {research_questions}
        User Preferences: {user_preferences}
        
        Your task:
        1. Identify 5-8 highly relevant papers
        2. Provide brief summaries (2-3 sentences each)
        3. Explain why each paper is relevant
        4. Ask the user which papers they want to focus on
        
        Format your response as:
        PAPER_SUGGESTIONS:
        Paper 1: [Title]
        Authors: [Authors]
        Summary: [Brief summary]
        Relevance: [Why it's relevant]
        
        Paper 2: [Title]
        Authors: [Authors]
        Summary: [Brief summary]
        Relevance: [Why it's relevant]
        
        [Continue for all papers...]
        
        SELECTION_GUIDE:
        [Ask user to select 3-5 papers they want to focus on, explaining the selection criteria]
        """)
        
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    def suggest_papers(self, topic: str, research_questions: List[str], user_preferences: str) -> str:
        """Suggest relevant papers based on research questions"""
        print(f"📚 Literature Agent: Researching relevant papers for '{topic}'...")
        
        response = self.chain.run(
            topic=topic,
            research_questions="\n".join([f"- {q}" for q in research_questions]),
            user_preferences=user_preferences
        )
        
        return response
    
    def get_user_paper_selection(self, paper_suggestions: str) -> List[int]:
        """Get user's paper selection"""
        print("\n📚 Literature Agent: Here are the suggested papers:")
        print(paper_suggestions)
        
        print("\n📋 Please select 3-5 papers you want to focus on (enter paper numbers separated by commas):")
        selection_input = input("Your selection (e.g., 1,3,5): ").strip()
        
        try:
            selected_indices = [int(x.strip()) - 1 for x in selection_input.split(',')]
            return selected_indices
        except ValueError:
            print("Invalid input. Please enter numbers separated by commas.")
            return self.get_user_paper_selection(paper_suggestions)

class MethodologyAgent:
    """Agent responsible for suggesting datasets, metrics, and experimental design"""
    
    def __init__(self, llm):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_template("""
        You are an expert research methodology specialist. Based on the research questions and selected papers, suggest appropriate methodologies.
        
        Topic: {topic}
        Research Questions: {research_questions}
        Selected Papers: {selected_papers}
        
        Your task:
        1. Suggest appropriate datasets for this research
        2. Recommend evaluation metrics
        3. Propose experimental design
        4. Ask about user preferences for scale and type of experiments
        
        Format your response as:
        DATASET_SUGGESTIONS:
        - [Dataset 1]: [Description and why it's suitable]
        - [Dataset 2]: [Description and why it's suitable]
        
        EVALUATION_METRICS:
        - [Metric 1]: [Description and importance]
        - [Metric 2]: [Description and importance]
        
        EXPERIMENTAL_DESIGN:
        [Detailed experimental design proposal]
        
        USER_PREFERENCES_QUESTIONS:
        - [Question about experiment scale]
        - [Question about experiment type]
        - [Question about computational resources]
        """)
        
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    def suggest_methodology(self, topic: str, research_questions: List[str], selected_papers: List[Dict]) -> str:
        """Suggest methodology based on research context"""
        print(f"🔬 Methodology Agent: Designing methodology for '{topic}'...")
        
        # Mock paper data for now
        papers_text = "\n".join([f"- {paper.get('title', 'Paper')}" for paper in selected_papers])
        
        response = self.chain.run(
            topic=topic,
            research_questions="\n".join([f"- {q}" for q in research_questions]),
            selected_papers=papers_text
        )
        
        return response
    
    def get_user_methodology_preferences(self, methodology_suggestions: str) -> Dict[str, str]:
        """Get user's methodology preferences"""
        print("\n🔬 Methodology Agent: Here are the methodology suggestions:")
        print(methodology_suggestions)
        
        print("\n⚙️ Please answer these methodology preference questions:")
        
        preferences = {}
        questions = [
            "What is your preferred experiment scale? (small/medium/large)",
            "What type of experiments do you prefer? (empirical/theoretical/hybrid)",
            "What are your computational resource constraints?",
            "Do you have access to specific datasets?",
            "What is your timeline for experiments?"
        ]
        
        for i, question in enumerate(questions, 1):
            print(f"\n{i}. {question}")
            response = input(f"Your answer: ").strip()
            preferences[f"pref_{i}"] = response
        
        return preferences

class DraftingAgent:
    """Agent responsible for creating LaTeX draft skeleton"""
    
    def __init__(self, llm):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert academic writer specializing in LaTeX document preparation. 
            Create a comprehensive LaTeX research paper skeleton for the given topic and methodology.
            
            The LaTeX document should include:
            1. Proper document class and packages for academic papers
            2. Title, author, abstract, and keywords
            3. Well-structured sections with proper LaTeX commands
            4. Placeholder content that guides the researcher
            5. Professional academic formatting
            6. Proper citation formatting
            7. References section structure
            
            Use proper LaTeX syntax and academic paper structure."""),
            ("human", """Topic: {topic}
            Research Questions: {research_questions}
            Selected Papers: {selected_papers}
            Methodology: {methodology}
            
            Create a complete LaTeX research paper skeleton with proper academic structure.""")
        ])
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    def create_draft(self, topic, research_questions, selected_papers, methodology):
        """Create LaTeX draft skeleton"""
        try:
            response = self.chain.run(
                topic=topic,
                research_questions=research_questions,
                selected_papers=selected_papers,
                methodology=methodology
            )
            
            # Ensure the response starts with proper LaTeX document structure
            if not response.strip().startswith('\\documentclass'):
                # Create a proper LaTeX template if the AI response is incomplete
                response = self._create_latex_template(topic, research_questions, selected_papers, methodology)
            
            return response.strip()
        except Exception as e:
            print(f"❌ Error in Drafting Agent: {e}")
            # Fallback to template
            return self._create_latex_template(topic, research_questions, selected_papers, methodology)
    
    def _create_latex_template(self, topic, research_questions, selected_papers, methodology):
        """Create a fallback LaTeX template"""
        template = f"""\\documentclass[12pt,a4paper]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[T1]{{fontenc}}
\\usepackage{{amsmath,amsfonts,amssymb}}
\\usepackage{{graphicx}}
\\usepackage{{geometry}}
\\usepackage{{hyperref}}
\\usepackage{{natbib}}
\\usepackage{{setspace}}
\\usepackage{{titlesec}}
\\usepackage{{enumitem}}

\\geometry{{margin=1in}}
\\setlength{{\\parindent}}{{0pt}}
\\setlength{{\\parskip}}{{6pt}}

\\title{{\\textbf{{{topic}}}: A Comprehensive Research Study}}
\\author{{Research Team}}
\\date{{\\today}}

\\begin{{document}}

\\maketitle

\\begin{{abstract}}
This research investigates {topic} through systematic analysis and empirical investigation. The study addresses key research questions including {', '.join(research_questions[:3])}. Our methodology employs {methodology} to provide comprehensive insights into this emerging field.
\\end{{abstract}}

\\section{{Introduction}}
{self._generate_introduction_content(topic, research_questions)}

\\section{{Literature Review}}
{self._generate_literature_content(selected_papers)}

\\section{{Methodology}}
{self._generate_methodology_content(methodology)}

\\section{{Results and Discussion}}
{self._generate_results_content()}

\\section{{Conclusion}}
{self._generate_conclusion_content(topic)}

\\section{{Future Work}}
{self._generate_future_work_content(topic)}

\\bibliographystyle{{plainnat}}
\\begin{{thebibliography}}{{99}}
{self._generate_bibliography_content(selected_papers)}
\\end{{thebibliography}}

\\end{{document}}"""
        
        return template
    
    def _generate_introduction_content(self, topic, research_questions):
        """Generate introduction content"""
        return f"""\\subsection{{Research Context}}
{topic} represents a significant area of investigation in contemporary research. This study aims to address the following research questions:

\\begin{{enumerate}}[label=\\textbf{{RQ\\arabic*:}}]
{chr(10).join([f'\\item {q}' for q in research_questions])}
\\end{{enumerate}}

\\subsection{{Research Objectives}}
The primary objectives of this research are:
\\begin{{itemize}}
\\item To analyze current approaches and methodologies in {topic}
\\item To identify key challenges and opportunities
\\item To propose innovative solutions and frameworks
\\item To evaluate the effectiveness of proposed approaches
\\end{{itemize}}

\\subsection{{Research Significance}}
This research contributes to the field by providing systematic analysis, empirical validation, and practical insights for researchers and practitioners working in {topic}."""

    def _generate_literature_content(self, selected_papers):
        """Generate literature review content"""
        return f"""\\subsection{{Related Work}}
Based on the selected papers, we have identified several key areas of research:

\\begin{{itemize}}
\\item Current state-of-the-art approaches
\\item Identified gaps in existing research
\\item Emerging trends and methodologies
\\item Comparative analysis of existing solutions
\\end{{itemize}}

\\subsection{{Research Gaps}}
The literature review reveals several research gaps that this study addresses:
\\begin{{enumerate}}
\\item Need for comprehensive evaluation frameworks
\\item Lack of empirical validation in certain areas
\\item Requirement for scalable and efficient solutions
\\end{{enumerate}}"""

    def _generate_methodology_content(self, methodology):
        """Generate methodology content"""
        return f"""\\subsection{{Research Design}}
This study employs a {methodology} approach to ensure comprehensive and reliable results.

\\subsection{{Data Collection}}
\\begin{{itemize}}
\\item Primary data sources and collection methods
\\item Secondary data analysis and synthesis
\\item Validation and verification procedures
\\end{{itemize}}

\\subsection{{Analysis Framework}}
\\begin{{itemize}}
\\item Quantitative analysis methods
\\item Qualitative assessment approaches
\\item Evaluation metrics and criteria
\\item Statistical significance testing
\\end{{itemize}}"""

    def _generate_results_content(self):
        """Generate results content"""
        return """\\subsection{Experimental Results}
\\textbf{[PLACEHOLDER: Insert your experimental results here]}

\\subsection{Data Analysis}
\\textbf{[PLACEHOLDER: Include statistical analysis, charts, and findings]}

\\subsection{Performance Evaluation}
\\textbf{[PLACEHOLDER: Add evaluation metrics and comparative analysis]}

\\subsection{Discussion of Findings}
\\textbf{[PLACEHOLDER: Discuss implications, limitations, and insights]}"""

    def _generate_conclusion_content(self, topic):
        """Generate conclusion content"""
        return f"""\\subsection{{Summary of Contributions}}
This research has made several key contributions to the field of {topic}:

\\begin{{enumerate}}
\\item Comprehensive analysis and evaluation
\\item Novel methodological approaches
\\item Practical insights and recommendations
\\item Framework for future research
\\end{{enumerate}}

\\subsection{{Research Implications}}
The findings of this study have significant implications for:
\\begin{{itemize}}
\\item Academic research and theory development
\\item Practical applications and implementations
\\item Industry standards and best practices
\\item Future research directions
\\end{{itemize}}"""

    def _generate_future_work_content(self, topic):
        """Generate future work content"""
        return f"""\\subsection{{Identified Research Opportunities}}
Based on our findings, several promising research directions emerge:

\\begin{{enumerate}}
\\item Extension of current methodologies
\\item Integration with emerging technologies
\\item Scalability and performance improvements
\\item Cross-domain applications
\\end{{enumerate}}

\\subsection{{Recommendations}}
We recommend the following areas for future investigation:
\\begin{{itemize}}
\\item Longitudinal studies and validation
\\item Comparative analysis across domains
\\item Development of standardized frameworks
\\item Industry collaboration and real-world testing
\\end{{itemize}}"""

    def _generate_bibliography_content(self, selected_papers):
        """Generate bibliography content"""
        return """\\bibitem{paper1} Author, A. (2024). Title of Paper 1. Journal Name, Volume(Issue), Pages.
\\bibitem{paper2} Author, B. (2024). Title of Paper 2. Conference Name, Pages.
\\bibitem{paper3} Author, C. (2024). Title of Paper 3. Journal Name, Volume(Issue), Pages.
\\bibitem{paper4} Author, D. (2024). Title of Paper 4. Conference Name, Pages.
\\bibitem{paper5} Author, E. (2024). Title of Paper 5. Journal Name, Volume(Issue), Pages."""

class PolishAgent:
    """Agent responsible for rewriting sections in formal academic tone and formatting references"""
    
    def __init__(self, llm):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_template("""
        You are an expert academic writing editor. Polish the LaTeX draft to ensure formal academic tone and proper formatting.
        
        LaTeX Draft: {latex_draft}
        
        Your task:
        1. Review and improve the academic writing style
        2. Ensure formal, professional tone throughout
        3. Format references properly (APA/IEEE style)
        4. Improve clarity and coherence
        5. Add any missing academic elements
        
        Important:
        - Maintain all placeholders
        - Keep the LaTeX structure intact
        - Improve only the writing quality and formatting
        - Ensure publication-ready academic standards
        
        Return the polished LaTeX document:
        """)
        
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    def polish_paper(self, latex_draft: str) -> str:
        """Polish the LaTeX draft for academic quality"""
        print(f"✨ Polish Agent: Polishing the LaTeX draft...")
        
        response = self.chain.run(latex_draft=latex_draft)
        
        return response

class ResearchCoPilot:
    """Main orchestrator class that coordinates all agents"""
    
    def __init__(self):
        # Initialize LLM
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=api_key,
            temperature=0.7
        )
        
        # Initialize agents
        self.topic_agent = TopicAgent(self.llm)
        self.literature_agent = LiteratureAgent(self.llm)
        self.methodology_agent = MethodologyAgent(self.llm)
        self.drafting_agent = DraftingAgent(self.llm)
        self.polish_agent = PolishAgent(self.llm)
        
        # Research context
        self.context = ResearchContext()
        
        print("🚀 Research Co-Pilot initialized successfully!")
    
    def run_research_workflow(self, broad_topic: str) -> str:
        """Execute the complete research workflow"""
        print(f"\n🎯 Starting Research Co-Pilot workflow for: {broad_topic}")
        print("=" * 60)
        
        # Step 1: Topic Refinement
        print("\n📋 STEP 1: Topic Refinement")
        topic_results = self.topic_agent.refine_topic(broad_topic)
        self.context.broad_topic = broad_topic
        self.context.research_questions = topic_results['research_questions']
        
        print(f"✅ Generated {len(topic_results['research_questions'])} research questions")
        for i, q in enumerate(topic_results['research_questions'], 1):
            print(f"   {i}. {q}")
        
        # Get clarifying questions answered
        if topic_results['clarifying_questions']:
            clarifying_responses = self.topic_agent.ask_clarifying_questions(
                topic_results['clarifying_questions']
            )
            print("✅ Clarifying questions answered")
        
        # Step 2: Literature Review
        print("\n📚 STEP 2: Literature Review")
        user_preferences = " ".join([f"{k}: {v}" for k, v in clarifying_responses.items()])
        paper_suggestions = self.literature_agent.suggest_papers(
            broad_topic, 
            self.context.research_questions, 
            user_preferences
        )
        
        # Get user paper selection
        selected_indices = self.literature_agent.get_user_paper_selection(paper_suggestions)
        
        # Mock paper data based on selection
        mock_papers = [
            {"title": f"Relevant Paper {i+1}", "authors": f"Author {i+1}", "summary": f"Summary {i+1}"}
            for i in range(8)
        ]
        self.context.selected_papers = [mock_papers[i] for i in selected_indices]
        
        print(f"✅ Selected {len(self.context.selected_papers)} papers for focus")
        
        # Step 3: Methodology Design
        print("\n🔬 STEP 3: Methodology Design")
        methodology_suggestions = self.methodology_agent.suggest_methodology(
            broad_topic,
            self.context.research_questions,
            self.context.selected_papers
        )
        
        # Get user methodology preferences
        methodology_preferences = self.methodology_agent.get_user_methodology_preferences(
            methodology_suggestions
        )
        self.context.methodology_preferences = methodology_preferences
        
        print("✅ Methodology preferences collected")
        
        # Step 4: Draft Generation
        print("\n✍️ STEP 4: Draft Generation")
        methodology_summary = " ".join([f"{k}: {v}" for k, v in methodology_preferences.items()])
        draft_skeleton = self.drafting_agent.create_draft(
            broad_topic,
            self.context.research_questions,
            self.context.selected_papers,
            methodology_summary
        )
        self.context.draft_skeleton = draft_skeleton
        
        print("✅ LaTeX draft skeleton generated")
        
        # Step 5: Polish and Finalize
        print("\n✨ STEP 5: Polish and Finalize")
        final_paper = self.polish_agent.polish_paper(draft_skeleton)
        self.context.final_paper = final_paper
        
        print("✅ Final polished LaTeX paper ready")
        
        return final_paper
    
    def save_paper(self, filename: str = None) -> str:
        """Save the final paper to a .tex file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"research_paper_{timestamp}.tex"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.context.final_paper)
        
        print(f"💾 Paper saved to: {filename}")
        return filename
    
    def generate_pdf(self, tex_filename):
        """Generate PDF from LaTeX file using pdflatex"""
        try:
            # Check if pdflatex is available
            result = subprocess.run(['which', 'pdflatex'], capture_output=True, text=True)
            if result.returncode != 0:
                print("⚠️ pdflatex not found. Installing texlive...")
                # Try to install texlive
                install_result = subprocess.run(['sudo', 'apt', 'update'], capture_output=True, text=True)
                if install_result.returncode == 0:
                    install_result = subprocess.run(['sudo', 'apt', 'install', '-y', 'texlive-full'], capture_output=True, text=True)
                    if install_result.returncode != 0:
                        print("❌ Failed to install texlive. PDF generation unavailable.")
                        return tex_filename
            
            # Get the directory and filename without extension
            base_dir = os.path.dirname(tex_filename)
            base_name = os.path.splitext(os.path.basename(tex_filename))[0]
            
            # Change to the directory containing the tex file
            original_dir = os.getcwd()
            os.chdir(base_dir)
            
            try:
                # Run pdflatex twice to resolve references
                print(f"🔧 Compiling LaTeX to PDF: {base_name}.tex")
                
                # First compilation
                result = subprocess.run([
                    'pdflatex', 
                    '-interaction=nonstopmode', 
                    '-output-directory=' + base_dir,
                    f'{base_name}.tex'
                ], capture_output=True, text=True, timeout=60)
                
                if result.returncode != 0:
                    print(f"⚠️ First pdflatex run had warnings: {result.stderr[:200]}...")
                
                # Second compilation to resolve references
                result = subprocess.run([
                    'pdflatex', 
                    '-interaction=nonstopmode', 
                    '-output-directory=' + base_dir,
                    f'{base_name}.tex'
                ], capture_output=True, text=True, timeout=60)
                
                if result.returncode != 0:
                    print(f"⚠️ Second pdflatex run had warnings: {result.stderr[:200]}...")
                
                # Check if PDF was created
                pdf_filename = os.path.join(base_dir, f'{base_name}.pdf')
                if os.path.exists(pdf_filename):
                    print(f"✅ PDF generated successfully: {pdf_filename}")
                    return pdf_filename
                else:
                    print("❌ PDF file not found after compilation")
                    return tex_filename
                    
            finally:
                # Clean up auxiliary files
                aux_files = ['.aux', '.log', '.out', '.toc', '.lof', '.lot']
                for ext in aux_files:
                    aux_file = os.path.join(base_dir, f'{base_name}{ext}')
                    if os.path.exists(aux_file):
                        try:
                            os.remove(aux_file)
                        except:
                            pass
                
                # Return to original directory
                os.chdir(original_dir)
                
        except subprocess.TimeoutExpired:
            print("❌ PDF generation timed out")
            return tex_filename
        except Exception as e:
            print(f"❌ PDF generation error: {e}")
            return tex_filename

def main():
    """Main function to run the Research Co-Pilot"""
    try:
        # Initialize the Research Co-Pilot
        copilot = ResearchCoPilot()
        
        # Get user input
        print("\n🎓 Welcome to Research Co-Pilot!")
        print("I'll help you brainstorm and draft a research paper step by step.")
        
        broad_topic = input("\n🔍 Enter your broad research topic: ").strip()
        
        if not broad_topic:
            print("❌ No topic provided. Exiting.")
            return
        
        # Run the complete workflow
        final_paper = copilot.run_research_workflow(broad_topic)
        
        # Save the paper
        filename = copilot.save_paper()
        
        # Try to generate PDF
        pdf_filename = copilot.generate_pdf(filename)
        
        print(f"\n🎉 Research Co-Pilot workflow completed!")
        print(f"📄 Final paper: {filename}")
        if pdf_filename.endswith('.pdf'):
            print(f"📄 PDF version: {pdf_filename}")
        
        print("\n💡 Next steps:")
        print("1. Review the generated LaTeX file")
        print("2. Replace placeholders with your actual research results")
        print("3. Add your experimental data and findings")
        print("4. Compile to PDF: pdflatex filename.tex")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please check your GEMINI_API_KEY and try again.")

if __name__ == "__main__":
    main()
