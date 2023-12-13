import http.server
import socketserver

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

PORT = 7000

with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    print("Server started at localhost:" + str(PORT))
    httpd.serve_forever()
