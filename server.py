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
prefix    = "frontend"
CSS_FILE  = "style.css"
JS_FILE   = "script.js"

GET_list.append("/add_remove.html")
GET_list.append("/sdf_upload.html")
GET_list.append("/select_display.html")
GET_list.append("/successful_upload.html")
GET_list.append("/unsuccessful_upload.html")
GET_list.append("/style.css")
GET_list.append("/script.js")


POST_list.append("/")
POST_list.append("/sdf-form")


class http_server(BaseHTTPRequestHandler):
    
    def create_page(self, filename):
        filename = prefix + filename
        fptr = open(filename)
        page = fptr.read()
        fptr.close()
        return page; 

    def display(self, page):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", len(page))
        self.end_headers()
        self.wfile.write(bytes(page, "utf-8"))
        return

    def error(self):
        self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes("404: not found", "utf-8"))
        return
    
    
    def post_retrieve_parse(self):
        data = self.rfile.read(int(self.headers["Content-Length"]))
        data = MultipartParser(io.BytesIO(data), self.headers["Content-Type"].split("boundary=")[1])
        return data
    
    # Get method isto request data from a specified resource.  
    def do_GET(self):
        if (self.path in GET_list):
            page = self.create_page(self.path) 
            self.display(page)
        elif (self.path == "/"):
            page = self.create_page("/sdf_upload.html")
            self.display(page)
        else:
            self.error()
        
        return 

    # Post method is to send data to a server the create/update a resource. 
    def do_POST(self):
        
        post_data = self.post_retrieve_parse()

        if (self.path == "/sdf-form" or self.path == "/"):

            for data in post_data:
                if (data.name == "sdf_file"):
                    file = io.BytesIO(data.file.read())
                elif (data.name == "molecule_name"):
                    name = data.value
            
            if (len(name) == 0):
                # TODO
                # Make it so this does not send a 200 response. Find a way to check for lack of file input. 
                # This might be doable in JavaScript
                # Maybe have some sort of if-statement to check that everything is filled out, and 
                # we will be able to interact with the HTML from there to tell the user they made a mistake. 
                error_string = "Not enough data provided. Please make sure to add the name and file of your molecule.\n"
                self.display(error_string)
                return 

            if (not db.molecule_exists(name)):
                db.add_molecule(name, io.TextIOWrapper(file))
            
            fptr = open(prefix + "/sdf_upload.html", "r")
            page = fptr.read()
            fptr.close()
            self.display(page)
        elif (self.path == "/add-form"): 
            print(post_data)
            print("in add form")
        elif (self.path == "/delete-form"):
            print(post_data)
            print("in delete form")
        else:
            self.error()

        return 




httpd = HTTPServer(('localhost', int(sys.argv[1])), http_server)
httpd.serve_forever()
    
