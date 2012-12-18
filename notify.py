#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json

class HttpHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        try:
            self.send_response(200)
            self.send_header('Content-type',	'text/html')
            self.end_headers()
            print(self.headers)
            contentLength = int(self.headers['Content-Length'])
            content = self.rfile.read(contentLength)
            data = json.load(content)
            message = data['message']
            return
        except:
            self.send_error(404, 'Well, this is embarassing')
     
def main():
    try:
        server = HTTPServer(('', 13380), HttpHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print 'Shutting down server...'
        server.socket.close()

if __name__ == '__main__':
    main()