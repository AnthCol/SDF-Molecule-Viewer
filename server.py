import io
import sys
import molsql
import MolDisplay
from multipart import MultipartParser
from http.server import HTTPServer, BaseHTTPRequestHandler

db = molsql.Database(reset=True)
db.create_tables()

GET_list  = ["/add_remove.html", "/sdf_upload.html", "/select_display.html", "/style.css", "/script.js"]
prefix    = "frontend"

fptr = open(prefix + "/select_display.html")
display_header = fptr.read()
fptr.close()
    
fptr = open(prefix + "/svg_display.html")
svg_header = fptr.read()
fptr.close()

html_footer = "</body></html>"

element_map = {}

ELEMENT_CODE = 0
ELEMENT_NAME = 1
ELEMENT_R    = 2
ELEMENT_G    = 3
ELEMENT_B    = 4
ELEMENT_RAD  = 5


class http_server(BaseHTTPRequestHandler):
    
    def create_page(self, filename):
        fptr = open(prefix + filename, "r")
        page = fptr.read()
        fptr.close()
        return page; 

    def display(self, page):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
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
    
    def generate_list(self, raw_data):
        data_list = []

        for data in raw_data:
            data_list.append(data.value)

        return data_list

    def generate_hex(self, r, g, b):
        return "%02x%02x%02x" % (r, g, b)

    # Get method isto request data from a specified resource.  
    def do_GET(self):
        if (self.path == "/select_display.html"):
            page = display_header
            page += db.fetch_all_molecules()
            page += html_footer
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
            data_list = self.generate_list(self.parse_multipart())
            db.add_element(data_list) 

            hex_code = self.generate_hex(data_list[ELEMENT_R], data_list[ELEMENT_G], data_list[ELEMENT_B])
            temp_list = [hex_code, data_list[ELEMENT_RAD]]

            element_map[data_list[ELEMENT_CODE]] = temp_list 
            self.display(self.create_page("/add_remove.html"))

        elif (self.path == "/delete-form"):  
            data_list = self.generate_list(self.parse_multipart())
            db.del_element(data_list)
            del element_map[data_list[ELEMENT_CODE]] 
            self.display(self.create_page("/add_remove.html"))
        elif (self.path == "/svg-display"): 
            data_list = self.generate_list(self.parse_multipart()) 
            mol = db.load_mol(data_list[0])
            fptr = open(prefix + "/svg_temp.html", "w")
            fptr.write(mol.svg(element_map))
            fptr.close()
            self.display(display_header + db.fetch_all_molecules() + html_footer)
            #self.display_svg(self.create_page("/svg_temp.html"))
        else:
            self.error()

        return 

httpd = HTTPServer(('localhost', int(sys.argv[1])), http_server)
httpd.serve_forever()
    
