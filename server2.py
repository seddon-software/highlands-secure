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
        def getMimeType():
            extension = fileName.split(".")[-1]
            if(extension == "ico"): return "image/x-icon"
            if(extension == "css"): return "text/css"
            if(extension == "jpg"): return "image/jpeg"
            if(extension == "png"): return "image/png"
            if(extension == "svg"): return "image/svg+xml"
            return "text/html"
            
        def sendHeaders(code=200):
            if code == 200:
                self.send_response(code)
                self.send_header("Content-type", getMimeType())
            else:
                self.send_response(code)
            self.end_headers()

        parsedUrl = urllib.parse.urlparse(self.path) # returns a 6-tuple
        fileName = parsedUrl[2]
        fileName = fileName[1:]  # remove leading '/'
        try:
            f = open(fileName, "r", encoding="UTF-8")
            data = f.read()
            sendHeaders()
            self.wfile.write(data.encode())
        except:
            sendHeaders(200)

PORT = 9096
SERVER = "localhost" # "assessmydeal.com"
server = http.server.HTTPServer((SERVER, PORT), Handler)

print("server:", SERVER)
print("port:", PORT)
server.serve_forever()




