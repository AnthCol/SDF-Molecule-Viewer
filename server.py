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


GET_list  = []
POST_list = []
prefix    = "frontend/"
CSS_FILE  = "style.css"
JS_FILE   = "script.js"

GET_list.append("add_remove.html")
GET_list.append("sdf_upload.html")
GET_list.append("select_display.html")
GET_list.append("successful_upload.html")
GET_list.append("unsuccessful_upload.html")
GET_list.append("style.css")
GET_list.append("script.js")


POST_list.append("/")
POST_list.append("/sdf-form")


class http_server(BaseHTTPRequestHandler):
    
    def create_page(self, filename):
        filename = prefix + filename
        fptr = open(filename)
        page = fptr.read()
        fptr.close()
        return page; 

    def display(self, filename):
        page = self.create_page(filename)
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
            self.display("sdf_upload.html")
        elif (self.path in GET_list):
            self.display(self.path)
        else:
            self.error()
        
        return 


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

