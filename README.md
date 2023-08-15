# SDF-Molecule-Viewer

This project was the final project for CIS*2750 at the University of Guelph. 
This version is an upgraded version of the one I submitted for the course. 

It is a full-stack web application that will generate and save custom (in the sense that the user can choose colours) SVG renderings of molecules based on a user-inputted .sdf file. 

## How to run

Step 1:
    Install the following if you do not have them already:
    <ol>
        <li>swig version 3.0 or higheri</li>
        <li>multipart package (```pip install multipart```)</li>
    </ol>
Step 2:
    Run the ```make``` command in the terminal (you may need to update the python paths in the makefile)

Step 3:
    Run the following export command in the terminal:
       ```export LD_LIBRARY_PATH=.```

Step 4:
    Run the program, specifying what port you want the server running on:
    ```python3 server.py <port_no>```

Step 5:
    Visit ```http://localhost:<port_no>``` 
At this point, you can interact with the website in any way that you would like. If you want to view the SVG that is generated, navigate to the "frontend" folder of the project, and open the file named "svg_temp.html"


### Potential future updates
Include radial gradients in the SVG file. <br>
Improve overall website design. <br>
Optionally have the browser render the SVG rather than save it to a file. <br>


### More information
The .sdf file format is a file format developed by MDL Information Systems. They describe attributes of a molecule, including things like how many atoms and bonds it has, as well as angles for all of the atoms and bonds (among other things). 
You can learn more about it <a href="https://en.wikipedia.org/wiki/Chemical_table_file#SDF">here</a>.

### Credits
The molecule.i file was not written by me, it was written by Dr. Stefan Kremer at the University of Guelph. 


