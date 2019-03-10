from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>" 
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text"><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output.encode("utf-8"))
                print(output)
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>&#161 Hola !</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output.encode("utf-8"))
                print(output)
                return

        except IOError:
            self.send_error(404, f'File Not Found: {self.path}')

    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(
                self.headers.get('content-type'))
            print(pdict)
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                print(fields)
                messagecontent = fields.get('message')
            output = ""
            output += "<html><body>"
            output += " <h2> Okay, how about this: </h2>"
            messagecontent[0] = messagecontent[0].decode("utf-8")
            output += f"<h1> {messagecontent[0]} </h1>"
            output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            output += "</body></html>"
            self.wfile.write(output.encode("utf-8"))
            print(output)
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print(f"Web Server running on port {port}")
        server.serve_forever()
    except KeyboardInterrupt:
        print(" ^C entered, stopping web server....")
        server.socket.close()

if __name__ == '__main__':
    main()
