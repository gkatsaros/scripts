#!/usr/bin/env python
from urllib2 import Request, urlopen, URLError
from sys import argv
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer


def getopts(argv):
    opts = {}  # Empty dictionary to store key-value pairs.
    while argv:  # While there are arguments left to parse...
        if argv[0][0] == '-':  # Found a "-name value" pair.
            opts[argv[0]] = argv[1]  # Add key and value to the dictionary.
        argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
    return opts

myargs = getopts(argv)
if '-ip' in myargs:  # Example usage.
    ip = myargs['-ip']


class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        request = Request('http://'+ip+':8888')
        try:
	        response = urlopen(request)
	        returned_ip = response.read()
        except URLError, e:
            print 'No IP returned', e

        self.wfile.write("<html><body><h1>My IP is:"+returned_ip+"</h1></body></html>")

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")
        
def run(server_class=HTTPServer, handler_class=S, port=9999):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()



    
