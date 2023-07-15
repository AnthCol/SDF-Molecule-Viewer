import io
import sys
import cgi
import molsql
import urllib
import MolDisplay
from http.server import HTTPServer, BaseHTTPRequestHandler

db = molsql.Database(reset=True)
db.create_tables()


class http_server(BaseHTTPRequestHandler):
    
    def display(self, page):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", len(page))
        self.end_headers()
        self.wfile.write(bytes(page, "utf-8"))
    
    def error(self):
        self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes("404: not found", "utf-8"))




    def do_GET(self):
        if (self.path == "/"):
            self.path = "/sdf-form"
            fptr = open("frontend/sdf_upload.html")
            page = fptr.read()
            fptr.close()
            self.display(page)
        else:
            self.error()
        
        return 


    def do_POST(self):

        if (self.path == "/sdf-form"):
        
            form_data = cgi.FieldStorage(
                fp      = self.rfile, 
                headers = self.headers, 
                environ = {"REQUEST_METHOD" : "POST"}
            )
            
            name = form_data["sdf_molecule_name"]
            file = form_data["sdf_file"].read()
        
            sdf = io.TextIOWrapper(file)
            

            # Only add the molecule to the database if it isn't in there 
            if (not db.molecule_exists(name)):
                db.add_molecule(name, sdf)
            

            
            # At this point the molecule has been added to the database
            # Now just need to display a webpage as a response. 

            fptr = open("frontend/sdf_upload.html", "r")
            page = fptr.read()
            fptr.close()
            self.display(page)

        else:
            self.error()

        return 




httpd = HTTPServer(('localhost', int(sys.argv[1])), http_server)
httpd.serve_forever()

