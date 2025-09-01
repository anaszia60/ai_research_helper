from flask import Flask, request, jsonify, render_template_string
import os
import json
from datetime import datetime

# Create a minimal Flask app for Vercel
app = Flask(__name__)

# Simple HTML template for the interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Research Co-Pilot 🚀</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            margin: 0;
            padding: 20px;
            color: white;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            text-align: center;
        }
        .header h1 {
            font-size: 3rem;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .info-box {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 30px;
            margin: 30px 0;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
        }
        .btn {
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 15px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            margin: 10px;
            transition: transform 0.3s ease;
        }
        .btn:hover {
            transform: translateY(-3px);
        }
        .warning {
            background: rgba(255, 193, 7, 0.2);
            border: 1px solid rgba(255, 193, 7, 0.5);
            color: #ffc107;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Research Co-Pilot</h1>
            <p>AI-Powered Research Paper Generator</p>
        </div>
        
        <div class="info-box">
            <h2>📋 About This System</h2>
            <p>The Research Co-Pilot is a sophisticated AI system that helps researchers generate comprehensive academic papers using LangChain and Google Gemini AI.</p>
            <p>Due to Vercel's size limitations, this is a lightweight version. For the full functionality, please use the local version.</p>
        </div>
        
        <div class="info-box warning">
            <h2>⚠️ Vercel Limitation</h2>
            <p>This serverless function exceeds Vercel's 250MB limit due to AI/ML dependencies.</p>
            <p>For full functionality, please run locally or use alternative hosting.</p>
        </div>
        
        <div class="info-box">
            <h2>🔧 Local Setup</h2>
            <p>To run the full Research Co-Pilot locally:</p>
            <ol style="text-align: left; display: inline-block;">
                <li>Clone the repository</li>
                <li>Install dependencies: <code>pip install -r requirements.txt</code></li>
                <li>Set your GEMINI_API_KEY</li>
                <li>Run: <code>python3 launch.py</code></li>
                <li>Open: <code>http://localhost:5003</code></li>
            </ol>
        </div>
        
        <div class="info-box">
            <h2>🌐 Alternative Hosting</h2>
            <p>For production deployment, consider:</p>
            <a href="https://render.com" class="btn" target="_blank">Render.com</a>
            <a href="https://railway.app" class="btn" target="_blank">Railway.app</a>
            <a href="https://heroku.com" class="btn" target="_blank">Heroku</a>
        </div>
        
        <div class="info-box">
            <h2>📚 Repository</h2>
            <p>View the full source code and documentation:</p>
            <a href="https://github.com/anaszia60/ai_research_helper" class="btn" target="_blank">GitHub Repository</a>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    """Home page with information about the system"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/status')
def status():
    """API status endpoint"""
    return jsonify({
        'status': 'limited',
        'message': 'This is a lightweight version due to Vercel size limitations',
        'full_functionality': 'available_locally',
        'repository': 'https://github.com/anaszia60/ai_research_helper',
        'local_setup': 'python3 launch.py'
    })

@app.route('/api/initialize', methods=['POST'])
def initialize():
    """Initialize endpoint - returns info about limitations"""
    return jsonify({
        'success': False,
        'message': 'Full functionality not available on Vercel due to size limitations',
        'recommendation': 'Run locally for full Research Co-Pilot experience',
        'local_command': 'python3 launch.py'
    })

@app.route('/<path:path>')
def catch_all(path):
    """Catch all other routes and redirect to home"""
    return render_template_string(HTML_TEMPLATE)

# Vercel requires this export
app.debug = False

# Export the app for Vercel
if __name__ == '__main__':
    app.run(debug=False)
