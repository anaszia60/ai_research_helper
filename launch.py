#!/usr/bin/env python3
"""
Research Co-Pilot Web Launcher
Launches the beautiful web interface directly
"""

import sys
import os

def print_banner():
    print("🚀" + "=" * 60 + "🚀")
    print("           RESEARCH CO-PILOT")
    print("🚀" + "=" * 60 + "🚀")
    print()

def print_info():
    print("🌐 Launching Research Co-Pilot Web Interface...")
    print("   - Beautiful, modern UI")
    print("   - Step-by-step workflow")
    print("   - Visual progress tracking")
    print("   - Interactive research guidance")
    print()

def launch_web():
    print("🚀 Starting Research Co-Pilot Web Frontend...")
    print("📱 Open your browser and go to: http://localhost:5003")
    print("⏹️  Press Ctrl+C to stop the server")
    print()
    
    try:
        from launch_co_pilot_web import app
        app.run(debug=True, host='0.0.0.0', port=5002)
    except ImportError as e:
        print(f"❌ Error: {e}")
        print("Please make sure all dependencies are installed:")
        print("pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print_banner()
    print_info()
    
    try:
        launch_web()
    except KeyboardInterrupt:
        print("\n\n👋 Research Co-Pilot stopped. Happy researching!")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
