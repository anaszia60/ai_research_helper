# 🚀 Research Co-Pilot

A sophisticated, modular AI-powered research assistant built with LangChain that helps users brainstorm and draft research papers step-by-step.

## ✨ Features

### 🤖 **Multi-Agent System**
- **Topic Agent**: Refines broad topics into specific research questions
- **Literature Agent**: Suggests relevant papers and provides summaries
- **Methodology Agent**: Recommends datasets, metrics, and experimental design
- **Drafting Agent**: Generates LaTeX draft skeleton with placeholders
- **Polish Agent**: Ensures formal academic tone and proper formatting

### 🔄 **Intelligent Workflow**
1. **Topic Refinement** → Generate 3-5 focused research questions
2. **Literature Review** → Suggest and summarize relevant papers
3. **Methodology Design** → Propose experimental approaches
4. **Draft Generation** → Create LaTeX skeleton with placeholders
5. **Polish & Finalize** → Ensure academic quality and formatting

### 💬 **Interactive User Experience**
- Each agent asks clarifying questions
- User makes decisions at each stage
- System assists humans, doesn't replace them
- Guided brainstorming process

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- GEMINI_API_KEY (Google AI API key)

### Setup
```bash
# Clone or navigate to project directory
cd "ai agent"

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

## 🚀 Usage

### Quick Start
```bash
# Run the Research Co-Pilot
python3 run_co_pilot.py

# Or run directly
python3 research_co_pilot.py
```

### Interactive Workflow Example
```
🎓 Welcome to Research Co-Pilot!
I'll help you brainstorm and draft a research paper step by step.

🔍 Enter your broad research topic: machine learning in healthcare

🔍 Topic Agent: Analyzing topic 'machine learning in healthcare'...
✅ Generated 5 research questions
   1. How can deep learning models improve early disease detection accuracy?
   2. What are the privacy implications of using patient data in ML systems?
   3. How do different ML algorithms compare in medical image classification?
   4. What validation strategies ensure ML models generalize to diverse populations?
   5. How can interpretable ML methods enhance clinical decision-making?

📝 Topic Agent: Please answer these clarifying questions:
1. What specific medical domain interests you most?
Your answer: radiology

2. What is your target audience (clinicians, researchers, policymakers)?
Your answer: clinicians

3. What is your timeline for this research?
Your answer: 6 months

📚 Literature Agent: Researching relevant papers...
[Paper suggestions displayed]

📋 Please select 3-5 papers you want to focus on:
Your selection (e.g., 1,3,5): 1,2,4

🔬 Methodology Agent: Designing methodology...
[Methodology suggestions displayed]

⚙️ Please answer these methodology preference questions:
1. What is your preferred experiment scale? (small/medium/large)
Your answer: medium

[Continue through all steps...]
```

## 📁 Output Files

### Generated Files
- **LaTeX File**: `research_paper_YYYYMMDD_HHMMSS.tex`
- **PDF File**: `research_paper_YYYYMMDD_HHMMSS.pdf` (if LaTeX compilation succeeds)

### File Structure
The generated LaTeX file includes:
- Proper LaTeX structure and packages
- Abstract with placeholders
- Introduction with placeholders
- Related Work section
- Methodology with placeholders
- Results section with placeholders
- Conclusion with placeholders
- References section

## 🔧 Customization

### Adding New Agents
```python
class CustomAgent:
    def __init__(self, llm):
        self.llm = llm
        # Custom implementation
    
    def process(self, context):
        # Custom processing logic
        pass
```

### Modifying Prompts
Edit the prompt templates in each agent class to customize:
- Question types
- Output formats
- Analysis depth
- Academic style preferences

## 🎯 Use Cases

### Academic Research
- PhD dissertation planning
- Conference paper preparation
- Journal article drafting
- Research proposal development

### Industry Research
- Technical white papers
- Patent applications
- Research reports
- Innovation proposals

### Student Projects
- Master's thesis planning
- Undergraduate research
- Capstone projects
- Research methodology learning

## 💡 Best Practices

### For Users
1. **Be Specific**: Provide detailed broad topics for better refinement
2. **Engage Actively**: Answer clarifying questions thoughtfully
3. **Review Outputs**: Always review and validate AI-generated content
4. **Iterate**: Use the system multiple times to refine your research

### For Developers
1. **Modular Design**: Keep agents independent and focused
2. **Error Handling**: Implement robust error handling for each agent
3. **User Feedback**: Collect and incorporate user feedback
4. **Continuous Improvement**: Regularly update prompts and logic

## 🚨 Limitations & Considerations

### Current Limitations
- Uses mock data for paper suggestions (can be enhanced with real APIs)
- LaTeX compilation requires local LaTeX installation
- Limited to English language output
- Requires internet connection for API calls

### Ethical Considerations
- AI assists but doesn't replace human judgment
- Generated content should be reviewed and validated
- Placeholders ensure human researchers add real results
- System designed for brainstorming, not final publication

## 🔮 Future Enhancements

### Planned Features
- Integration with real academic databases (arXiv, PubMed, etc.)
- Multi-language support
- Enhanced LaTeX templates
- Citation management integration
- Collaborative research features

### API Integrations
- Google Scholar API
- arXiv API
- PubMed API
- Citation databases
- Research collaboration platforms

## 📞 Support & Contributing

### Getting Help
- Check the error messages for common issues
- Verify your GEMINI_API_KEY is set correctly
- Ensure all dependencies are installed
- Check Python version compatibility

### Contributing
- Fork the repository
- Create feature branches
- Submit pull requests
- Report issues and bugs
- Suggest improvements

## 📄 License

This project is open source and available under the MIT License.

---

**🎓 Happy Researching!** The Research Co-Pilot is here to help you turn your research ideas into well-structured academic papers.
