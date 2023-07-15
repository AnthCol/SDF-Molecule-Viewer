import io
import sys
import json
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



    # GET requests should only retrieve data
    # In our case, this should occur when we need to retrieve a molecule
    # from the database, and display it on the screen. 
    # We will create a custom svg screen with a back-button. 
 
    def do_GET(self):
        content_length = self.headers.get("Content-Length")
        #body           = self.rfile.read(content_length)
        #get_variables  = urllib.parse.parse_qs(body.decode("utf-8"))
        

        if (self.path == "/"):
            self.path = "/sdf-form"
            fptr = open("frontend/sdf_upload.html")
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
            content_length = int(self.headers["Content-Length"])
            post_data      = self.rfile.read(content_length)
            
            print("#################################")
            print(post_data)
            print("##################################")

            data           = json.loads(post_data.decode("utf-8"))

            print("printing with do_POST")
            print(data)

            # Only add the molecule to the database if it isn't in there 
            #if (not db.molecule_exists(name)):
            #    db.add_molecule(name, sdf_file)
            

            
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

