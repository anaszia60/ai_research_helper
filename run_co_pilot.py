#!/usr/bin/env python3
"""
Launcher script for Research Co-Pilot
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from research_co_pilot import main
    print("🚀 Launching Research Co-Pilot...")
    main()
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please make sure all dependencies are installed:")
    print("pip install langchain langchain-google-genai python-dotenv")
except Exception as e:
    print(f"❌ Error: {e}")
    print("Please check your setup and try again.")
