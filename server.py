from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        SimpleHTTPRequestHandler.end_headers(self)

def run(server_class=HTTPServer, handler_class=CORSRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Serveur démarré sur le port {port}")
    print(f"Accédez au dashboard à l'adresse : http://localhost:{port}/dashboard.html")
    httpd.serve_forever()

if __name__ == '__main__':
    run() 