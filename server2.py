############################################################
#
#    Highlands Server
#
#    © Highlands Negotiations, 2018, v1.0
#
############################################################

import urllib.parse
import http.server

class Handler(http.server.BaseHTTPRequestHandler):
        
    def do_POST(self):
        self.do_GET()

    def do_GET(self):
        def sendHeaders():
            self.send_response(200)
            self.send_header("Content-type", "text/html")

        parsedUrl = urllib.parse.urlparse(self.path) # returns a 6-tuple
        fileName = parsedUrl[2]
        fileName = fileName[1:]  # remove leading '/'
        try:
            f = open(fileName, "r", encoding="UTF-8")
            data = f.read()
            sendHeaders()
            self.wfile.write(data.encode())
        except:
            sendHeaders(404)

PORT = 80
SERVER = "assessmydeal.com"
server = http.server.HTTPServer((SERVER, PORT), Handler)

print("server:", SERVER)
print("port:", PORT)
server.serve_forever()




