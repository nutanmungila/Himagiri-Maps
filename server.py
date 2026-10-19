#!/usr/bin/env python3
"""
Himagiri Meadows Android & Local Network Server
Serves the layout map on 0.0.0.0 so any Android phone on Wi-Fi can access it.
"""
import http.server
import socket
import socketserver
import os
import sys

PORT = 8080

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = socket.gethostbyname(socket.gethostname())
    finally:
        s.close()
    return ip

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(os.path.abspath(__file__)), **kwargs)
    
    def end_headers(self):
        # Enable CORS and caching headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

def run_server():
    ip = get_local_ip()
    handler = CustomHandler
    
    # Allow port reuse
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(('0.0.0.0', PORT), handler) as httpd:
        print("="*60)
        print("  HIMAGIRI MEADOWS NAVIGATOR - LIVE LOCAL NETWORK SERVER")
        print("="*60)
        print(f"  • Computer Browser:  http://localhost:{PORT}")
        print(f"  • Android Phone URL: http://{ip}:{PORT}")
        print("="*60)
        print("  Open this URL on your Android Chrome browser or scan QR code.")
        print("  Press Ctrl+C to stop the server.")
        print("="*60)
        sys.stdout.flush()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == '__main__':
    run_server()
