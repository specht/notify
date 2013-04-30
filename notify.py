#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from subprocess import Popen, PIPE, STDOUT
import json

tokens = {}

class HttpHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        global tokens
        try:
            contentLength = int(self.headers['Content-Length'])
            if contentLength < 1:
                raise Exception()
            if contentLength > 1024 * 64:
                raise Exception("Content too long.")
            content = self.rfile.read(contentLength)
            print(content)
            data = json.loads(content)
            print(data)
            
            token = data['token']
            if len(token) != 16:
                raise Exception("Invalid token.")
            title = 'Notification from nhcham.org'
            message = data['message']
            title = message
            if "\n" in title:
                title = title[:title.index("\n")]
            if len(title) > 256:
                title = title[:256]
            
            if token in tokens:
                command = []
                command.append("mail")
                command.append("-s")
                command.append(title)
                command.append(tokens[token]['name'] + " <" + tokens[token]['email'] + ">")
                command.append("--")
                command.append("-f")
                command.append("no-reply@notify.nhcham.org")
                p = Popen(command, stdout=PIPE, stdin=PIPE, stderr=PIPE)
                p.communicate(input = message)
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
            else:
                self.send_error(404, 'Invalid token.')
            
            return
        except:
            self.send_error(404, 'Well, this is embarassing')
            raise
     
def main():
    global tokens
    try:
        tokens = json.load(open('tokens.json'))
        server = HTTPServer(('', 13380), HttpHandler)
        print("Starting server...")
        server.serve_forever()
    except KeyboardInterrupt:
        print 'Shutting down server...'
        server.socket.close()

if __name__ == '__main__':
    main()
    
