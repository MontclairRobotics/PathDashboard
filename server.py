from http.server import BaseHTTPRequestHandler, HTTPServer
from networktables import NetworkTables
import logging

NetworkTables.initialize(server='roborio-555-frc.local')  
auto_table = NetworkTables.getTable("Auto")

logging.basicConfig(level=logging.DEBUG)

class SimpleHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length']) 
        post_data = self.rfile.read(content_length).decode('utf-8')  
        auto_table.putString("Auto String", post_data)  
        print(f"Received Auto String: {post_data}")

        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Auto String received")

server_address = ('', 5809) 
httpd = HTTPServer(server_address, SimpleHandler)
print("Server running on port 5809...")
httpd.serve_forever()
