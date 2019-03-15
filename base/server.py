#-----------------------------------------------------------
# Imports
#-----------------------------------------------------------

from http.server import HTTPServer, CGIHTTPRequestHandler

#-----------------------------------------------------------
# Classes
#-----------------------------------------------------------

class Handler(CGIHTTPRequestHandler):
    
    def do_GET(self):
        #print('GET', self.path)
        if self.path == '/':
            self.path = '/index.py'
        super(CGIHTTPRequestHandler, self).do_GET()


class Server:

    def __init__(self, port=8080):
        self.port = port
        self.address = ("", port)
        self.server_class = HTTPServer
        self.handler_class = Handler
        self.handler_class.cgi_directories = ["/"]

    def run(self):
        print("Listening on :", self.port)
        httpd = self.server_class(self.address, self.handler_class)
        httpd.serve_forever()

#-----------------------------------------------------------
# Main
#-----------------------------------------------------------

if __name__ == '__main__':
    Server().run()
