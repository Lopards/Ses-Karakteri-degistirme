import http.server as server

class ecohandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("content-type","html")
        self.end_headers()
        self.wfile.write("Metin aktarimi içindir.".encode())

def main():
    PORT = 7001
    httdp = server.HTTPServer(('',PORT),ecohandler)
    httdp.serve_forever()

if __name__ =="__main__":
    main()
