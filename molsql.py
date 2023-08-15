import os
import sqlite3
import molecule
import MolDisplay


class Database():

    def __init__(self, reset = True): #reset = False
        if (reset == True and os.path.exists('molecules.db')):
            os.remove('molecules.db')
        
        self.conn = sqlite3.connect('molecules.db')

    
    def create_tables(self):
        # If any of the tables exist, it should leave them alone and not create them
        fetch_result = self.conn.execute("SELECT name FROM sqlite_master WHERE name = 'Elements'")
        if (fetch_result.fetchone() == None):
            Elements =  """ CREATE TABLE Elements 
                            (
                            ELEMENT_NO          INTEGER         NOT NULL,
                            ELEMENT_CODE        VARCHAR(3)      NOT NULL, 
                            ELEMENT_NAME        VARCHAR(32)     NOT NULL, 
                            COLOUR1             CHAR(6)         NOT NULL, 
                            COLOUR2             CHAR(6)         NOT NULL, 
                            COLOUR3             CHAR(6)         NOT NULL, 
                            RADIUS              DECIMAL(3)      NOT NULL, 
                            PRIMARY KEY (ELEMENT_CODE)
                            );    
                        """
            self.conn.execute(Elements)
            self.conn.commit()
        



        fetch_result = self.conn.execute("SELECT name FROM sqlite_master WHERE name = 'Atoms'")
        if (fetch_result.fetchone() == None):
            Atoms = """ CREATE TABLE Atoms 
                        (
                        ATOM_ID        INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
                        ELEMENT_CODE   VARCHAR(3) NOT NULL, 
                        X              DECIMAL(7, 4) NOT NULL, 
                        Y              DECIMAL(7, 4) NOT NULL, 
                        Z              DECIMAL (7, 4) NOT NULL, 
                        FOREIGN KEY (ELEMENT_CODE) REFERENCES Elements(ELEMENT_CODE)
                        ); 
                    """
            self. conn.execute(Atoms)
            self.conn.commit()

        fetch_result = self.conn.execute("SELECT name FROM sqlite_master WHERE name = 'Bonds'")
        if (fetch_result.fetchone() == None):
            Bonds = """ CREATE TABLE Bonds 
                (
                BOND_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
                A1      INTEGER NOT NULL, 
                A2      INTEGER NOT NULL, 
                EPAIRS  INTEGER NOT NULL
                ); 
                """
            self.conn.execute(Bonds)
            self.conn.commit()
            



        fetch_result = self.conn.execute("SELECT name FROM sqlite_master WHERE name = 'Molecules'")
        if (fetch_result.fetchone() == None):
            Molecules = """ CREATE TABLE Molecules 
                        (
                        MOLECULE_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
                        NAME TEXT NOT NULL UNIQUE
                        ); 
                        """
            self.conn.execute(Molecules)
            self.conn.commit()




        fetch_result = self.conn.execute("SELECT name FROM sqlite_master WHERE name = 'MoleculeAtom'")
        if (fetch_result.fetchone() == None):
            MoleculeAtom =  """ CREATE TABLE MoleculeAtom 
                            (
                            MOLECULE_ID   INTEGER   NOT NULL,
                            ATOM_ID       INTEGER   NOT NULL,
                            PRIMARY KEY (MOLECULE_ID, ATOM_ID)
                            FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules(MOLECULE_ID), 
                            FOREIGN KEY (ATOM_ID) REFERENCES Atoms(ATOM_ID)
                            ); 
                            """
            self.conn.execute(MoleculeAtom)
            self.conn.commit()
        
        
        fetch_result = self.conn.execute("SELECT name FROM sqlite_master WHERE name = 'MoleculeBond'")
        if (fetch_result.fetchone() == None):
            MoleculeBond =  """ CREATE TABLE MoleculeBond
                            (
                            MOLECULE_ID INTEGER   NOT NULL, 
                            BOND_ID     INTEGER   NOT NULL, 
                            PRIMARY KEY (MOLECULE_ID, BOND_ID), 
                            FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules(MOLECULE_ID), 
                            FOREIGN KEY (BOND_ID) REFERENCES Bonds(BOND_ID)
                            );  
                            """

            self.conn.execute(MoleculeBond)
            self.conn.commit()

        return


    def __setitem__(self, table, values):
        self.conn.execute("INSERT INTO " + table + " VALUES " + str(values))
        self.conn.commit()
        return


    def add_atom(self, molname, atom):
        vals = (atom.element, atom.x, atom.y, atom.z)
        self.conn.execute("INSERT INTO Atoms (ELEMENT_CODE, X, Y, Z) VALUES " + str(vals))

        a_id = self.conn.execute("SELECT ATOM_ID FROM Atoms WHERE ELEMENT_CODE='" + atom.element + "' AND X=" + str(atom.x) + " AND Y=" + str(atom.y) + " AND Z=" + str(atom.z)).fetchone()[0]
        m_id = self.conn.execute("SELECT MOLECULE_ID FROM Molecules WHERE NAME='" + molname + "'").fetchone()[0]

        self.conn.execute("INSERT INTO MoleculeAtom (MOLECULE_ID, ATOM_ID) VALUES (" + str(m_id) + "," + str(a_id) + ")")
        self.conn.commit()
        return

    def add_bond(self, molname, bond):
        vals = (bond.a1, bond.a2, bond.epairs)
        self.conn.execute("INSERT INTO Bonds (A1, A2, EPAIRS) VALUES " + str(vals))

        bond_id = self.conn.execute("SELECT BOND_ID FROM Bonds WHERE A1=" + str(bond.a1) + " and A2=" + str(bond.a2) + " and EPAIRS=" + str(bond.epairs)).fetchone()[0]
        molecule_id = self.conn.execute("SELECT MOLECULE_ID FROM Molecules WHERE NAME='" + molname + "'").fetchone()[0]

        self.conn.execute("INSERT INTO MoleculeBond (MOLECULE_ID, BOND_ID) VALUES (" + str(molecule_id) + "," + str(bond_id) + ")")
        self.conn.commit()
        return

    def add_molecule(self, name, fp):
        m = MolDisplay.Molecule()
        m.parse(fp)

        self.conn.execute("INSERT INTO Molecules (NAME) VALUES ('" + name + "')")
        self.conn.commit()

        for i in range(0, m.atom_no):
            self.add_atom(name, m.get_atom(i))

        for i in range(0, m.bond_no):
            self.add_bond(name, m.get_bond(i))
        
        return
    
    def load_mol(self, name):
        m = MolDisplay.Molecule()

        information = self.conn.execute("SELECT ELEMENT_CODE, X, Y, Z FROM Atoms INNER JOIN MoleculeAtom ON MoleculeAtom.ATOM_ID=Atoms.ATOM_ID INNER JOIN Molecules ON Molecules.MOLECULE_ID=MoleculeAtom.MOLECULE_ID WHERE NAME='" + name + "' ORDER BY Atoms.ATOM_ID").fetchall()
        for i in range(len(information)):
            m.append_atom(str(information[i][0]), float(information[i][1]), float(information[i][2]), float(information[i][3]))

        information = self.conn.execute("SELECT A1, A2, EPAIRS FROM MoleculeBond INNER JOIN Bonds ON MoleculeBond.BOND_ID=Bonds.BOND_ID INNER JOIN Molecules ON Molecules.MOLECULE_ID=MoleculeBond.MOLECULE_ID WHERE NAME='" + name + "' ORDER BY Bonds.BOND_ID").fetchall()
        for i in range(len(information)):
            m.append_bond(int(information[i][0]), int(information[i][1]), int(information[i][2]))
        return m
    
    def radius(self):
        radius_map = {}

        data = self.conn.execute("SELECT ELEMENT_CODE, RADIUS FROM Elements").fetchall()

        for i in range(len(data)):
            radius_map[data[i][0]] = data[i][1]

        return radius_map
   
   
    def element_name(self):
        element_map = {}

        data = self.conn.execute("SELECT ELEMENT_CODE, ELEMENT_NAME FROM Elements").fetchall()

        for i in range(len(data)):
            element_map[data[i][0]] = data[i][1]

        return element_map 
  
    
    def add_element(self, data_list):
        self.conn.execute("INSERT INTO Elements WHERE " + 
                          "ELEMENT_CODE ='" + data_list[0] + "' " +
                          "AND ELEMENT_NAME ='" + data_list[1] + "' " +
                          "AND COLOUR1 = '" + data_list[2] + "' " + 
                          "AND COLOUR2 = '" + data_list[3] + "' " + 
                          "AND COLOUR3 = '" + data_list[4] + "' " +
                          "AND RADIUS = '" +data_list[5] + "'") 
        return

    def del_element(self, data_list): 
        self.conn.execute("DELETE FROM Elements WHERE " + 
                          "ELEMENT_CODE ='" + data_list[0] + "' " +
                          "AND ELEMENT_NAME ='" + data_list[1] + "' " + 
                          "AND COLOUR1 = '" + data_list[2] + "' " +
                          "AND COLOUR2 = '" + data_list[3] + "' " +
                          "AND COLOUR3 = '" + data_list[4] + "' " + 
                          "AND RADIUS = '" + data_list[5] + "'")
        return

    def radial_gradients(self):
        radialGradientSVG = """
                            <radialGradient id="%s" cx="-50%%" cy="-50%%" r="220%%" fx="20%%" fy="20%%">
                                <stop offset="0%%" stop-color="#%s"/>
                                <stop offset="50%%" stop-color="#%s"/>
                                <stop offset="100%%" stop-color="#%s"/>
                            </radialGradient>
                            """

        ret_string = ""
        data_list = self.conn.execute("SELECT ELEMENT_NAME, COLOUR1, COLOUR2, COLOUR3 FROM Elements").fetchall()

        for i in range(len(data_list)):
            ret_string += radialGradientSVG % (data_list[i][0], data_list[i][1], data_list[i][2], data_list[i][3])
        
        return ret_string 
   

    def fetch_all_molecules(self):
        ret_string = """
                    <p> Select a molecule from the table below and hit the "Display" button to display it. </p>
                    <br>
                    <form method = "POST" id = "display_form" enctype = "multipart/form-data"/ >
                    <input id = "display_button" type = "submit" value = "Display" />
                    <br><br>
                    <table style = \"width: 80%\">
                    <tr>
                        <th> Molecule Name </th>
                        <th> Atom Count </th>
                        <th> Bond Count </th>
                        <th> Select Molecule </th>
                    </tr>

                    """        
        format = f"""
                  <tr>
                    <td><center>%s</center></td>
                    <td><center>%d</center></td>
                    <td><center>%d</center></td>
                    <td><center><input type="radio" name="display_choice" value="%s"/></center></td>
                  </tr>
                  """
        
    
        molecule_names = self.conn.execute("SELECT NAME FROM Molecules").fetchall()
        
        if (len(molecule_names) == 0):
            return "<br><p> There are no molecules in the database. Upload a .sdf file to see information here </p>"

        for i in range(len(molecule_names)):
            m = self.load_mol(molecule_names[i][0]) 
            ret_string += format % (molecule_names[i][0], m.atom_no, m.bond_no,  molecule_names[i][0])


        ret_string += "</table></form>"
        return ret_string; 



    def molecule_exists(self, mol_name):
        found = self.conn.execute("SELECT NAME FROM Molecules WHERE NAME='" + mol_name +"'").fetchall()
        return (len(found) != 0)


