import re 
import molecule

# radius = { 'H': 25, 
#            'C': 40, 
#            'O': 40, 
#            'N': 40
#          }

# element_name = { 'H': 'grey', 
#                  'C': 'black', 
#                  'O': 'red',
#                  'N': 'blue'
#                }

radius = {}
element_name = {}

header = """<svg version="1.1" width="1000" height="1000" xmlns="http://www.w3.org/2000/svg">"""
footer = """</svg>"""

offsetx = 500
offsety = 500


class Atom:

    def __init__(self, c_atom):
        self.member_atom = c_atom
        self.z_val= c_atom.z
    
    def __str__(self):
        e = self.member_atom.element 
        x = self.member_atom.x
        y = self.member_atom.y
        z = self.member_atom.z
        return "[element] = " + e + " | [x-value] = " + x + " | [y-value] = " + y + " | [z-value] = " + z + "\n"
    
    def svg(self):
        cx = (self.member_atom.x * 100) + offsetx
        cy = (self.member_atom.y * 100) + offsety
        
        if (self.member_atom.element in radius):
            r = radius[self.member_atom.element]
        else:
            r = 10
        
        if (self.member_atom.element in element_name):
            fill = element_name[self.member_atom.element]
        else:
            fill = "purple"

        return '  <circle cx="%.2f" cy="%.2f" r="%d" fill="%s"/>\n' % (cx, cy, r, fill)

class Bond:
    def __init__(self, c_bond):
        self.member_bond = c_bond
        self.z_val = c_bond.z
    
    def __str__(self):
        x1 = self.member_bond.x1
        x2 = self.member_bond.x2
        y1 = self.member_bond.y1
        y2 = self.member_bond.y2
        z = self.z_val
        l = self.member_bond.len 
        dx = self.member_bond.dx 
        dy = self.member_bond.dy 
        return "[x1] = %.2f | [x2] = %.2f | [y1] = %.2f | [y2] = %.2f | [z] = %.2f | [len] = %.2f | [dx] = %.2f | [dy] = %.2f \n" % (x1, x2, y1, y2, z, l, dx, dy) 

    def svg(self):

        x1 = self.member_bond.x1 * 100
        y1 = self.member_bond.y1 * 100
        x2 = self.member_bond.x2 * 100
        y2 = self.member_bond.y2 * 100
        dx = self.member_bond.dx * 10
        dy = self.member_bond.dy * 10

        # t = top b = bottom
        # l = left r = right 


        # point 2 is northeast or southwest 
        if ((x1 < x2 and y1 > y2) or (x1 > x2 and y1 < y2)):
            tl_x = (x1) + (dy) + offsetx
            tl_y = (y1) - (dx) + offsety

            tr_x = (x2) + (dy) + offsetx
            tr_y = (y2) - (dx) + offsety

            br_x = (x2) - (dy) + offsetx
            br_y = (y2) + (dx) + offsety

            bl_x = (x1) - (dy) + offsetx
            bl_y = (y1) + (dx) + offsety 
        # point 2 is northwest or southeast 
        elif ((x1 < x2 and y1 < y2) or (x1 > x2 and y1 > y2)):
            tl_x = (x1) - (dy) + offsetx
            tl_y = (y1) + (dx) + offsety

            tr_x = (x2) - (dy) + offsetx
            tr_y = (y2) + (dx) + offsety

            br_x = (x2) + (dy) + offsetx
            br_y = (y2) - (dx) + offsety

            bl_x = (x1) + (dy) + offsetx
            bl_y = (y1) - (dx) + offsety

            return '  <polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="green"/>\n' % (tl_x, tl_y, bl_x, bl_y, br_x, br_y, tr_x, tr_y)
        # when they are equal horizontally or vertically. 
        elif (x1 == x2 or y1 == y2):
            tl_x = (x1) - (dy) + offsetx
            tl_y = (y1) - (dx) + offsety

            tr_x = (x2) - (dy) + offsetx
            tr_y = (y2) - (dx) + offsety

            br_x = (x2) + (dy) + offsetx
            br_y = (y2) + (dx) + offsety

            bl_x = (x1) + (dy) + offsetx
            bl_y = (y1) + (dx) + offsety 

        return '  <polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="green"/>\n' % (bl_x, bl_y, tl_x, tl_y, tr_x, tr_y, br_x, br_y)


class Molecule(molecule.molecule):

    def __str__(self):
        print("########## PRINTING ATOMS ##########")

        for i in range(0, self.atom_no):
            temp_string = self.get_atom(i).element
            x = self.get_atom(i).x
            y = self.get_atom(i).y
            z = self.get_atom(i).z
            print("atom[" + str(i) + "] -> " + temp_string + " atom [x] -> " + str(x) + " atom [y] -> " + str(y) + " atom [z] -> " + str(z))

        print("########## NOW PRINTING BONDS ##########\n")

        for i in range(0, self.bond_no):
            if (self.get_bond(i) == None):
                break
            print("\nbond[" + str(i) + "]")
            print("    bond atom 1 [x1] = " + str(self.get_bond(i).x1) + " [y1] = " + str(self.get_bond(i).y1))
            print("    bond atom 2 [x2] = " + str(self.get_bond(i).x2) + " [y2] = " + str(self.get_bond(i).y2))
            print("    bond z val  [z]  = " + str(self.get_bond(i).z))
        
        return 


    def svg(self):

        atom_list = []
        bond_list = []


        # Create a list of atom and bond structs from the molecule
        for i in range(0, self.atom_no):
            a = self.get_atom(i)
            atom_list.append(a)
        for i in range(0, self.bond_no):
            b = self.get_bond(i)
            bond_list.append(b)


        ret = header 
        i = 0
        j = 0
        
        # merge sort stuff - calling svg methods to build the return string as we find values in order. 
        while (i < self.atom_no and j < self.bond_no):  
            if (atom_list[i].z < bond_list[j].z):
                a = Atom(atom_list[i])
                ret += a.svg()
                i += 1
            else:
                b = Bond(bond_list[j])
                ret += b.svg()
                j += 1
        
        while (i < self.atom_no):
            a = Atom(atom_list[i])
            ret += a.svg()
            i += 1
        while (j < self.bond_no):
            b = Bond(bond_list[j])
            ret += b.svg()
            j += 1
        

        ret += footer

        return ret

    
    def parse(self, file):
        data = file.read()

        # Regex to parse the atom info first, and then the bond info. 
        a = re.findall(r"([-]?[0-9]+[.]?[0-9]+\s+[-]?[0-9]+[.]?[0-9]+\s+[-]?[0-9]+[.]?[0-9]+\s[C,H,N,O])+", data)
        b = re.findall(r"(([0-9]+\s+){6}([0-9]+\n+){1})+", data)

        # Creating element from the regex 
        for i in range(len(a)): 
            vals = re.split('\s+', a[i])
            x = float(vals[0])
            y = float(vals[1])
            z = float(vals[2])
            element = vals[3]
            self.append_atom(element, x, y, z)

        for i in range(len(b)):
            
            vals = re.split('\s+', b[i][0])
            # We only care about the first three values from the regex. 
            # Because the regex isn't perfect we need to manually check for the first three being zero
            # We don't want to use this data. If the first 3 are numbers greater than zero though, we are good to go. 
            if (int(vals[0]) != 0 and int(vals[1]) != 0 and int(vals[2]) != 0):

                # Minus one added by Kremer recomendation. 
                a1 = int(vals[0])
                a2 = int(vals[1])
                epairs = int(vals[2])
                self.append_bond(a1 - 1, a2 - 1, epairs) 

        return 
