#!/usr/bin/env python
from urllib2 import Request, urlopen, URLError
from sys import argv
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer



class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()

        filename = "/opt/ipam_ip"
        # The function readlines() reads the file.             
        with open(filename) as f:
            content = f.readlines()
 
        # Show the file contents line by line.
        # We added the comma to print single newlines and not double newlines.
        # This is because the lines contain the newline character '\n'. 
        #for line in content:
        #    print(line)
        ipam_server_ip = content[0].replace('\n', '')
        name=content[1].replace('\n', '')

        request = Request('http://'+ipam_server_ip+':8888?username='+name)
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



    
