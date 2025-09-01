"""
Research Co-Pilot Web Frontend
A beautiful, minimalistic web interface for the Research Co-Pilot system
"""

import os
import json
import tempfile
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
from dotenv import load_dotenv

# Import the Research Co-Pilot
from research_co_pilot import ResearchCoPilot

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Global variable to store the copilot instance
copilot = None

def initialize_copilot():
    """Initialize the Research Co-Pilot"""
    global copilot
    try:
        copilot = ResearchCoPilot()
        return True
    except Exception as e:
        print(f"Error initializing copilot: {e}")
        return False

@app.route('/')
def index():
    """Main page"""
    return render_template('co_pilot.html')

@app.route('/api/initialize', methods=['POST'])
def initialize():
    """Initialize the Research Co-Pilot"""
    try:
        if initialize_copilot():
            return jsonify({'success': True, 'message': 'Research Co-Pilot initialized successfully!'})
        else:
            return jsonify({'success': False, 'error': 'Failed to initialize Research Co-Pilot'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/start_workflow', methods=['POST'])
def start_workflow():
    """Start the research workflow"""
    global copilot
    
    if not copilot:
        return jsonify({'success': False, 'error': 'Research Co-Pilot not initialized'}), 500
    
    try:
        data = request.get_json()
        broad_topic = data.get('topic', '').strip()
        
        if not broad_topic:
            return jsonify({'success': False, 'error': 'No topic provided'}), 400
        
        # Start the workflow (this will be handled step by step)
        return jsonify({
            'success': True, 
            'message': f'Workflow started for topic: {broad_topic}',
            'topic': broad_topic
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/step1_topic', methods=['POST'])
def step1_topic():
    """Step 1: Topic Refinement"""
    global copilot
    
    if not copilot:
        return jsonify({'success': False, 'error': 'Research Co-Pilot not initialized'}), 500
    
    try:
        data = request.get_json()
        broad_topic = data.get('topic', '').strip()
        
        if not broad_topic:
            return jsonify({'success': False, 'error': 'No topic provided'}), 400
        
        # Run topic refinement
        topic_results = copilot.topic_agent.refine_topic(broad_topic)
        copilot.context.broad_topic = broad_topic
        copilot.context.research_questions = topic_results['research_questions']
        
        return jsonify({
            'success': True,
            'research_questions': topic_results['research_questions'],
            'clarifying_questions': topic_results['clarifying_questions'],
            'analysis': topic_results['analysis']
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/step2_literature', methods=['POST'])
def step2_literature():
    """Step 2: Literature Review"""
    global copilot
    
    if not copilot:
        return jsonify({'success': False, 'error': 'Research Co-Pilot not initialized'}), 500
    
    try:
        data = request.get_json()
        clarifying_responses = data.get('clarifying_responses', {})
        topic = copilot.context.broad_topic
        research_questions = copilot.context.research_questions
        
        # Generate paper suggestions
        user_preferences = " ".join([f"{k}: {v}" for k, v in clarifying_responses.items()])
        paper_suggestions = copilot.literature_agent.suggest_papers(
            topic, research_questions, user_preferences
        )
        
        return jsonify({
            'success': True,
            'paper_suggestions': paper_suggestions
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/step3_methodology', methods=['POST'])
def step3_methodology():
    """Step 3: Methodology Design"""
    global copilot
    
    if not copilot:
        return jsonify({'success': False, 'error': 'Research Co-Pilot not initialized'}), 500
    
    try:
        data = request.get_json()
        selected_papers = data.get('selected_papers', [])
        
        # Mock paper data based on selection
        mock_papers = [
            {"title": f"Relevant Paper {i+1}", "authors": f"Author {i+1}", "summary": f"Summary {i+1}"}
            for i in range(8)
        ]
        copilot.context.selected_papers = [mock_papers[i] for i in selected_papers]
        
        # Generate methodology suggestions
        methodology_suggestions = copilot.methodology_agent.suggest_methodology(
            copilot.context.broad_topic,
            copilot.context.research_questions,
            copilot.context.selected_papers
        )
        
        return jsonify({
            'success': True,
            'methodology_suggestions': methodology_suggestions
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/step4_draft', methods=['POST'])
def step4_draft():
    """Step 4: Draft Generation"""
    global copilot
    
    if not copilot:
        return jsonify({'success': False, 'error': 'Research Co-Pilot not initialized'}), 500
    
    try:
        data = request.get_json()
        methodology_preferences = data.get('methodology_preferences', {})
        
        copilot.context.methodology_preferences = methodology_preferences
        
        # Generate draft
        methodology_summary = " ".join([f"{k}: {v}" for k, v in methodology_preferences.items()])
        draft_skeleton = copilot.drafting_agent.create_draft(
            copilot.context.broad_topic,
            copilot.context.research_questions,
            copilot.context.selected_papers,
            methodology_summary
        )
        copilot.context.draft_skeleton = draft_skeleton
        
        return jsonify({
            'success': True,
            'draft_skeleton': draft_skeleton
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/step5_polish', methods=['POST'])
def step5_polish():
    """Step 5: Polish and Finalize"""
    global copilot
    
    if not copilot:
        return jsonify({'success': False, 'error': 'Research Co-Pilot not initialized'}), 500
    
    try:
        # Polish the draft
        final_paper = copilot.polish_agent.polish_paper(copilot.context.draft_skeleton)
        copilot.context.final_paper = final_paper
        
        return jsonify({
            'success': True,
            'final_paper': final_paper
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/download_paper', methods=['POST'])
def download_paper():
    """Download the final paper"""
    global copilot
    
    if not copilot:
        return jsonify({'success': False, 'error': 'Research Co-Pilot not initialized'}), 500
    
    try:
        data = request.get_json()
        paper_type = data.get('type', 'tex')  # 'tex' or 'pdf'
        
        if not copilot.context.final_paper:
            return jsonify({'success': False, 'error': 'No paper generated yet'}), 400
        
        # Save the paper
        filename = copilot.save_paper()
        
        # Always return LaTeX file since PDF generation is not working
        print(f"📄 Returning LaTeX file: {filename}")
        return send_file(filename, as_attachment=True, download_name=filename)
        
    except Exception as e:
        print(f"❌ Download error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Research Agent Web Frontend...")
    print("📱 Open your browser and go to: http://localhost:5003")
    app.run(debug=True, host='0.0.0.0', port=5003)
