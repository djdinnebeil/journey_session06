#!/usr/bin/env python3
"""
AI Social Media Post Generator Server
Run with: python server.py
"""
import uvicorn
import os
import sys

def main():
    """Start the FastAPI server"""
    print("🚀 Starting AI Social Media Post Generator Server...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("api/main.py"):
        print("❌ Error: api/main.py not found!")
        print("Please run this script from the project root directory.")
        sys.exit(1)
    
    print("✅ Found API files")
    print("📡 Starting server on http://127.0.0.1:8000")
    print("📚 API Documentation: http://127.0.0.1:8000/docs")
    print("🔍 Health Check: http://127.0.0.1:8000/health")
    print("-" * 50)
    print("Press CTRL+C to stop the server")
    print()
    
    try:
        # Start the server
        uvicorn.run(
            "api.main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 