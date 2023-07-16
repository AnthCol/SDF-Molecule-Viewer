import io
import sys
import json
import molsql
import MolDisplay
from urllib.parse import parse_qs
from multipart import MultipartParser
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



    # GET requests should only retrieve data
    # In our case, this should occur when we need to retrieve a molecule
    # from the database, and display it on the screen. 
    # We will create a custom svg screen with a back-button. 
 
    def do_GET(self):
        content_length = self.headers.get("Content-Length")
        #body           = self.rfile.read(content_length)
        #get_variables  = urllib.parse.parse_qs(body.decode("utf-8"))
        
        #if (self.path not in do_GET_list):
        #    self.error()
        #else:
        #    fptr = open("self.path")
        #    page = fptr.read()
        #    fptr.close()
        #    self.display(page)
       
        if (self.path == "/"):
            self.path = "/sdf-form"
            fptr = open("frontend/sdf_upload.html")
            page = fptr.read()
            fptr.close()
            self.display(page)
        elif (self.path == "/style.css"):
            fptr = open("frontend/style.css")
            page = fptr.read()
            fptr.close()
            self.display(page)
        elif (self.path == "/script.js"):
            fptr = open("frontend/script.js")
            page = fptr.read()
            fptr.close()
            self.display(page)
        else:
            self.error()
        
        return 

    # POST requests should only deal with things that cause a change in state, 
    # or side effects on the server. In this case, it would be 
    # add/remove an element to/from the database, as well as 
    # adding a molecule through the file upload

    def do_POST(self):
        
        if (self.path == "/sdf-form" or self.path == "/"):
            
            content_type = self.headers["Content-Type"]

            post_data = self.rfile.read(int(self.headers["Content-Length"]))
            post_data = MultipartParser(io.BytesIO(post_data), content_type.split("boundary=")[1])
            

            for data in post_data:
                if (data.name == "sdf_file"):
                    file = io.BytesIO(data.file.read())
                elif (data.name == "molecule_name"):
                    name = data.value

            if (not db.molecule_exists(name)):
                db.add_molecule(name, io.TextIOWrapper(file))

            
            fptr = open("frontend/sdf_upload.html", "r")
            page = fptr.read()
            fptr.close()
            self.display(page)

        else:
            self.error()

        return 




httpd = HTTPServer(('localhost', int(sys.argv[1])), http_server)
httpd.serve_forever()

