import io
import sys
import molsql
import urllib
import MolDisplay
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
GET_list.append("/style.css")
GET_list.append("/script.js")

fptr = open(prefix + "/select_display.html")
display_header = fptr.read()
fptr.close()
display_footer = "</body></html>"

class http_server(BaseHTTPRequestHandler):
    
    def create_page(self, filename):
        fptr = open(prefix + filename, "r")
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
    
    
    def parse_multipart(self):
        data = self.rfile.read(int(self.headers["Content-Length"]))
        data = MultipartParser(io.BytesIO(data), self.headers["Content-Type"].split("boundary=")[1])
        return data

    # Get method isto request data from a specified resource.  
    def do_GET(self):
        if (self.path == "/select_display.html"):
            page = display_header
            page += db.fetch_all_molecules()
            page += display_footer
            self.display(page)
        elif (self.path in GET_list):
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
        
        if (self.path == "/sdf-form" or self.path == "/"):
            post_data = self.parse_multipart() 

            for data in post_data:
                if (data.name == "sdf_file"):
                    file = io.TextIOWrapper(io.BytesIO(data.file.read()))
                elif (data.name == "molecule_name"):
                    name = data.value
                    if (not db.molecule_exists(name)):
                        db.add_molecule(name, file)
                
            self.display(self.create_page("/sdf_upload.html"))
        elif (self.path == "/add-form"): 
            
            post_data = self.rfile.read(int(self.headers["Content-Length"])).decode("utf-8")
            post_data = urllib.parse.parse_qs(post_data)

            for key, value in post_data.iteritems():
                print ("%s = %s" % (key, value))
            print("DONE ITERATING OVER IT\n"); 
            data_list = [] 
            for data in post_data:
                data_list.append(data)
            
            db.add_element(data_list)
            
            self.display(self.create_page("/add_remove.html"))
        elif (self.path == "/delete-form"): 
            
            post_data = self.rfile.read(int(self.headers["Content-Length"])).decode("utf-8")
            post_data = urllib.parse.parse_qs(post_data)
        
            print(str(post_data))

            print("DONE PRINTING POST_DATA")

           
            data_list = []
            db.del_element(data_list)
            self.display(self.create_page("/add_remove.html"))
        elif (self.path == "/sdf-display"):
            
            for data in post_data:
                if (data.name == " " ):
                    print("YO\n")

        else:
            self.error()

        return 




httpd = HTTPServer(('localhost', int(sys.argv[1])), http_server)
httpd.serve_forever()
    
