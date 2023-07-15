import io
import os
import sys
import molsql 
import urllib
import MolDisplay
from http.server import HTTPServer, BaseHTTPRequestHandler


db = molsql.Database(reset=True)
db.create_tables()

select_display_head = """
                    <html>
                        <head>
                            <title> Select and Display Moelcules </title>
                            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"> </script>
                            <script src="script.js"></script>
                            <link rel="stylesheet" href="style.css" type="text/css" />
                        </head>
                        
                        <body>
                            <h1> Select and Display Molecules </h1>

                            <ul>
                                <li><a href="add_remove.html">Add and/or Remove Elements</a></li>
                                <li><a href="sdf_upload.html">Upload .sdf file</a></li>
                                <li><a href="select_display.html">Select and Display Molecules</a></li>
                            </ul>

                            <br>
                      """

select_display_foot = """
                        </body>
                      </html>
                      """
website_files = ['/add_remove.html', '/successful_upload.html', '/unsuccessful_upload.html', '/sdf_upload.html', '/select_display.html', '/style.css', '/script.js']



class sub_BaseHTTP(BaseHTTPRequestHandler): 

    def do_GET(self):
        if (self.path in website_files):
            if (self.path == "/select_display.html"):
                page = select_display_head + db.fetch_all_molecules() + select_display_foot
            else:
                fp = open(self.path[1:])
                page = fp.read()
                fp.close()
            print("PATH IN DO GET TAKEN")
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(page))
            self.end_headers()

            self.wfile.write(bytes(page, "utf-8"))
        elif (self.path == "/"):
            fp = open("sdf_upload.html")
            page = fp.read()
            fp.close()

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(page))
            self.end_headers()

            self.wfile.write(bytes(page, "utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("404: not found", "utf-8"))
        
        return 

 # self.path == "/" or self.path == "/successful_upload.html" or self.path == "/unsuccessful_upload.html")
    def do_POST(self):
        if (self.path == "/sdf_upload.html"):
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)

            postvars = urllib.parse.parse_qs(body.decode("utf-8"))


            # if (len(postvars) != 2):
            #     print("PATH TAKEN")
            #     self.send_header("Content_type", "text/html")
            #     self.end_headers()
            #     self.wfile.write(bytes("Incomplete form submission. Hit the back arrow in the browser to go back.", "utf-8"))
            #     return

            print("\n\n######################printing postvars in function \n\n" + str(postvars) + "\n\n#######################################################\n\n")
            

            file_path = postvars['filename'][0]
            mol_name = postvars['molecule_name'][0]
                

            print("printing filename = " + file_path + " printing mol_name " + mol_name)
            
            l = len(file_path)
            extension = file_path[l-4] + file_path[l-3] + file_path[l-2] + file_path[l-1]

            page = ""

            if (extension == ".sdf" and not db.molecule_exists(mol_name)):
                
                exclude = f"C:\\fakepath\\"
                new_path = file_path.replace(exclude, "")

                print("printing new_path = " + new_path)
                
                sdf_fp = open(new_path)

                db.add_molecule(mol_name, sdf_fp)

                sdf_fp.close()

                print("path taken")
                fp = open("sdf_upload.html")
                page = fp.read()
                fp.close()
            else:
                fp = open("sdf_upload.html")
                page = fp.read()
                fp.close()

            self.send_response(200)
            self.send_header("Content-type", "text/html") # image/svg+xml
            self.end_headers()
            self.wfile.write(bytes(page, "utf-8"))
        elif (self.path == "/add_remove.html"):
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            postvars = urllib.parse.parse_qs(body.decode("utf-8"))

            print("printing postvars ")
            print(postvars)

            fp = open("add_remove.html")
            page = fp.read()
            fp.close()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(page, "utf-8"))

            print("printing page -> " + page)
        elif (self.path == "/select_display.html"):
            print("hi")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("404: not found", "utf-8"))

        return 


httpd = HTTPServer(('localhost', int(sys.argv[1])), sub_BaseHTTP)
httpd.serve_forever()
