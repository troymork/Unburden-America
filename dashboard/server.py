#!/usr/bin/env python3
"""
Simple HTTP Server for IsThereEnoughMoney Dashboard
Serves the web-based management dashboard for campaign operations
"""

import os
import http.server
import socketserver
from http.server import SimpleHTTPRequestHandler
import json

class DashboardHandler(SimpleHTTPRequestHandler):
    """Custom handler for dashboard with CORS support"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(os.path.abspath(__file__)), **kwargs)
    
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests"""
        # Serve unified.html for root path
        if self.path == '/':
            self.path = '/unified.html'
        
        return super().do_GET()

def main():
    """Start the dashboard server"""
    port = int(os.environ.get('DASHBOARD_PORT', '8080'))
    
    with socketserver.TCPServer(("", port), DashboardHandler) as httpd:
        dashboard_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"🚀 IsThereEnoughMoney Dashboard Server")
        print(f"📁 Serving directory: {dashboard_dir}")
        print(f"🌐 Dashboard URL: http://localhost:{port}")
        print(f"📡 MCP Server: http://127.0.0.1:7802")
        print(f"🔄 Auto-refresh: Every 30 seconds")
        print("-" * 50)
        print("🇺🇸 Tax the System, Not the People!")
        print("Press Ctrl+C to stop the server")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(f"\n🛑 Shutting down dashboard server...")

if __name__ == '__main__':
    main()