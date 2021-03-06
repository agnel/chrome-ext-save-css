#!/usr/bin/python
# -*- coding: utf-8 -*-

# server.py: receive CSS and JS files from Chrome extension
#   and save files locally
#
# Author: Tomi.Mickelsson@iki.fi
#   30.10.2011 - Created

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

class MyServer(BaseHTTPRequestHandler):

    def do_POST(self):
        hd = self.headers

        # chrome sent data:
        url   = hd.get("X-origurl")
        fpath = hd.get("X-filepath")
        bodylen = int(hd['content-length'])
        body    = self.rfile.read(bodylen)
        print url, " ->", fpath, len(body)

        reply = "OK"

        # save file
        try:
            f = open(fpath, "w")
            f.write(body)
            f.close()
        except Exception, e:
            print e
            reply = "Server couldn't save "+fpath

        # return reply
        self.send_response(200)
        self.end_headers()
        self.wfile.write(reply)

# start http server
server = HTTPServer(('localhost', 8080), MyServer)
print "Server running in port 8080..."
server.serve_forever()

