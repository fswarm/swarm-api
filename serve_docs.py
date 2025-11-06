#!/usr/bin/env python3
"""
Simple HTTP server to serve the offline Swagger documentation locally.
This avoids CORS issues when testing the API from local HTML files.

Usage:
    python serve_docs.py
    
Then open: http://localhost:8888 in your browser
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

def serve_documentation():
    """Serve the offline documentation on a local HTTP server"""
    
    # Configuration
    PORT = 8888
    DOCS_FILE = "biobot_swagger_offline.html"
    
    # Check if documentation file exists
    if not os.path.exists(DOCS_FILE):
        print(f"❌ Error: {DOCS_FILE} not found!")
        print("Please run 'python create_offline_docs.py' first to generate the documentation.")
        return False
    
    # Create a custom handler that serves the docs as index
    class CustomHandler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            # Add comprehensive CORS headers
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS, HEAD')
            self.send_header('Access-Control-Allow-Headers', '*')
            self.send_header('Access-Control-Allow-Credentials', 'true')
            self.send_header('Access-Control-Max-Age', '3600')
            super().end_headers()
            
        def do_OPTIONS(self):
            # Handle preflight requests
            self.send_response(200)
            self.end_headers()
            
        def do_GET(self):
            # Serve the documentation as index page
            if self.path == '/' or self.path == '/index.html':
                self.path = f'/{DOCS_FILE}'
            return super().do_GET()
    
    try:
        # Start the server
        with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
            print("🚀 Starting local documentation server...")
            print(f"📄 Serving: {DOCS_FILE}")
            print(f"🌐 URL: http://localhost:{PORT}")
            print(f"🔑 API Endpoint: https://swarm-api-smzv.onrender.com")
            print("\n📋 Instructions:")
            print("1. The documentation will open in your browser automatically")
            print("2. Click 'Authorize' and enter your API key")
            print("3. Test endpoints directly against the live API")
            print("4. Press Ctrl+C to stop the server")
            print("\n" + "="*60)
            
            # Open browser automatically
            url = f"http://localhost:{PORT}"
            try:
                webbrowser.open(url)
                print(f"✅ Browser opened: {url}")
            except Exception as e:
                print(f"⚠️  Could not open browser automatically: {e}")
                print(f"Please manually open: {url}")
            
            print(f"\n🔴 Server running on port {PORT}... (Press Ctrl+C to stop)")
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        return True
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Error: Port {PORT} is already in use!")
            print("Either:")
            print(f"  1. Use a different port by editing this script")
            print(f"  2. Stop the process using port {PORT}")
            print(f"  3. Try: netstat -ano | findstr :{PORT}")
        else:
            print(f"❌ Error starting server: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("🔧 BioBot API Documentation Server")
    print("=" * 40)
    
    success = serve_documentation()
    
    if success:
        print("\n✅ Documentation server stopped successfully")
    else:
        print("\n❌ Documentation server failed to start")
        sys.exit(1)