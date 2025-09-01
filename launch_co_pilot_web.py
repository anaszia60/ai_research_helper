#!/usr/bin/env python3
"""
Launcher script for Research Co-Pilot Web Frontend
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from co_pilot_web import app
    print("🚀 Launching Research Co-Pilot Web Frontend...")
    print("📱 Open your browser and go to: http://localhost:5002")
    print("⏹️  Press Ctrl+C to stop the server")
    print("\n" + "=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5002)
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please make sure all dependencies are installed:")
    print("pip install langchain langchain-google-genai python-dotenv flask")
except Exception as e:
    print(f"❌ Error: {e}")
    print("Please check your setup and try again.")
