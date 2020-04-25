from http.server import BaseHTTPRequestHandler, HTTPServer
import detect
import time
from io import BytesIO
from urllib.parse import urlparse, parse_qs

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.getheader('content-length'))
        field_data = self.rfile.read(length)
        fields = urlparse.parse_qs(field_data)
        if(fields.text is None):
            self.send_response(200)
            self.end_headers()
            response = BytesIO()
            response.write("No text given")
            self.wfile.write(response.getvalue())
        else:
            self.send_response(200)
            self.end_headers()
            response = BytesIO()
            response.write(detect.detect(fields.text))
            self.wfile.write(response.getvalue())

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
