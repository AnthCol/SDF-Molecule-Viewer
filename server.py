import io
import sys
import molsql
import urllib
import MolDisplay
from http.server import HTTPServer, BaseHTTPRequestHandler

db = molsql.Database(reset=True)
db.create_tables()


class http_server(BaseHTTPRequestHandler):

    def do_GET(self):
        if (self.path == "/"):
            fptr = open("sdf_upload.html")
            page = fptr.read()

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(page))
            self.end_headers()

            # Display the web form in the browser 
            self.wfile.write(bytes(page, "utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("404: not found", "utf-8"))
        return 


    def do_POST(self):

        if (self.path == "/sdf-form"):
            print("INSIDE POST")

            form_data = cgi.FieldStorage(
                fp      = self.rfile, 
                headers = self.headers, 
                environ = {"REQUEST_METHOD" : "POST"}
            )
            
            name = form_data.getvalue("filename")
            file = form_data["file"]
        
            sdf = io.TextIOWrapper(uploaded_file.file, encoding = "utf-8")
            
            db.add_molecule(name, sdf)

            print("printing name: " + name)
            print("printing contents of file: " + str(std.read()))

            
            self.send_response(200)
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("404: not found", "utf-8"))

        return 




httpd = HTTPServer(('localhost', int(sys.argv[1])), http_server)
httpd.serve_forever()

