#include "mol.h"

/*

    Anthony Colaiacovo
    1091370
    
    February 28th, 2023

    CIS 2750 - Assignment 2

*/


void atomset(atom *atom, char element[3], double *x, double *y, double *z)
{
    
    if (element[1] == '\0')
    { 
        atom->element[0] = element[0]; 
        atom->element[1] = '\0'; 
    }
    else if (element[2] == '\0')
    { 
        atom->element[0] = element[0]; 
        atom->element[1] = element[1]; 
    }
    else 
    {
        atom->.element[0] = '\0'; 
    }


    atom->element[2] = '\0'; 


    if (x != NULL) atom->x = *x; 
    if (y != NULL) atom->y = *y;
    if (z != NULL) atom->z = *z; 
    

    return; 
}


void atomget(atom *atom, char element[3], double *x, double *y, double *z)
{
    if (atom == NULL) return; 

    element[0] = atom->element[0]; 
    element[1] = atom->element[1]; 
    element[2] = '\0'; 

    *x = atom->x; 
    *y = atom->y; 
    *z = atom->z; 
    
    return;
}

void compute_coords(bond *bond)
{
    unsigned short index_one = (*bond).a1; 
    unsigned short index_two = (*bond).a2;

    double z_one = (*bond).atoms[index_one].z; 
    double z_two = (*bond).atoms[index_two].z; 

    (*bond).x1 = (*bond).atoms[index_one].x; 
    (*bond).x2 = (*bond).atoms[index_two].x; 

    (*bond).y1 = (*bond).atoms[index_one].y; 
    (*bond).y2 = (*bond).atoms[index_two].y; 

    (*bond).z = (z_one + z_two) / 2; 

    (*bond).dx = (*bond).x2 - (*bond).x1; 
    (*bond).dy = (*bond).y2 - (*bond).y1; 

    (*bond).len = sqrt((bond->dx * bond->dx) + (bond->dy * bond->dy)); // pythagorean theorem 

    (*bond).dx /= (*bond).len; 
    (*bond).dy /= (*bond).len; 

    return; 
}

void bondset( bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs)
{
    if (bond == NULL || a1 == NULL || a2 == NULL || atoms == NULL || epairs == NULL) return; 

    (*bond).a1 = *a1; 
    (*bond).a2 = *a2; 
    (*bond).atoms = *atoms; 
    (*bond).epairs = *epairs;  

    compute_coords(bond); 

    return; 
}


void bondget( bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs)
{
    if (bond == NULL) return; 

    *a1 = (*bond).a1; 
    *a2 = (*bond).a2; 
    *atoms = (*bond).atoms; 
    *epairs = (*bond).epairs; 

    return; 
}

molecule * molmalloc(unsigned short atom_max, unsigned short bond_max)
{

    // If at any point malloc fails, free everything up to that point and return NULL
    
    int fail_flag = 0; 


    molecule * mol = (molecule*)malloc(sizeof(molecule)); 
    if (mol == NULL) return NULL;
    
    (*mol).atom_max = atom_max; 
    (*mol).atom_no  = 0; 
    (*mol).bond_max = bond_max; 
    (*mol).bond_no  = 0; 
    
    (*mol).atoms     = (atom*)malloc(sizeof(atom) * atom_max); 
    (*mol).bonds     = (bond*)malloc(sizeof(bond) * bond_max); 
    (*mol).atom_ptrs = (atom**)malloc(sizeof(atom*) * atom_max); 
    (*mol).bond_ptrs = (bond**)malloc(sizeof(bond*) * bond_max); 

    
    if ( (*mol).atoms == NULL || (*mol).bonds == NULL || (*mol).atom_ptrs == NULL || (*mol).bond_ptrs == NULL)
    {
        free((*mol).atoms); 
        free((*mol).bonds);
        free((*mol).atom_ptrs); 
        free((*mol).bond_ptrs); 
        free(mol); 

        return NULL; 
    }

    // re-assign the pointers to their respective atoms/bonds
    for (int i = 0; i < atom_max; i++) (*mol).atom_ptrs[i] = &(*mol).atoms[i]; 
    for (int i = 0; i < bond_max; i++) (*mol).bond_ptrs[i] = &(*mol).bonds[i]; 
    
    return mol; 
}

molecule * molcopy(molecule *src)
{

    if (src == NULL) return NULL; 

    molecule * m = molmalloc((*src).atom_max, (*src).bond_max); 

    if (m == NULL) return NULL; 


    // append each atom/bond to the newly created molecule 
    for (int i = 0; i < (*src).atom_no; i++) molappend_atom(m, &(*src).atoms[i]); 
    for (int i = 0; i < (*src).bond_no; i++) molappend_bond(m, &(*src).bonds[i]); 


    return m; 
}

void molfree(molecule *ptr)
{
    if (ptr == NULL) return; 

    free((*ptr).atoms); 
    free((*ptr).bonds); 
    free((*ptr).atom_ptrs); 
    free((*ptr).bond_ptrs); 
    free(ptr); 

    return; 
}


void molappend_atom(molecule *molecule, atom *atom)
{
   
    if (molecule == NULL || atom == NULL) return; 
    
    if ((*molecule).atom_no == (*molecule).atom_max)
    {

        (*molecule).atom_max = ((*molecule).atom_max < 1) ? 1 : (*molecule).atom_max * 2;

        (*molecule).atoms = realloc((*molecule).atoms, (*molecule).atom_max * sizeof(struct atom)); 
       
        if ((*molecule).atoms == NULL)
        {
            printf("##### Realloc for atoms returned NULL #####\n"); 
            exit(1); 
        }

        (*molecule).atom_ptrs = realloc((*molecule).atom_ptrs, (*molecule).atom_max * sizeof(struct atom*)); 
        
        if ((*molecule).atom_ptrs == NULL)
        {
            printf("##### Realloc for atom_ptrs returned NULL #####\n"); 
            exit(1); 
        }

        
        for (int i = 0; i < (*molecule).atom_no; i++)
        {
            (*molecule).atom_ptrs[i] = &(*molecule).atoms[i]; 
        }


        for (int i = 0; i < (*molecule).bond_no; i++)
        {
            unsigned short a1 = (*molecule).bonds[i].a1; 
            unsigned short a2 = (*molecule).bonds[i].a2; 
            (*molecule).bonds[i].atoms[a1] = (*molecule).atoms[a1]; 
            (*molecule).bonds[i].atoms[a2] = (*molecule).atoms[a2]; 
        }
    
    }

    memcpy(&(*molecule).atoms[(*molecule).atom_no], &(*atom), sizeof(struct atom)); 
    
    (*molecule).atom_ptrs[(*molecule).atom_no] = &(*molecule).atoms[(*molecule).atom_no];
    (*molecule).atom_no++; 
    

    return; 
}

void molappend_bond(molecule *molecule, bond *bond)
{

    if (molecule == NULL || bond == NULL) return; 

    if ((*molecule).bond_no == (*molecule).bond_max){                                                                         
        (*molecule).bond_max = ((*molecule).bond_max < 1) ? 1 : (*molecule).bond_max * 2; 

        (*molecule).bonds = realloc((*molecule).bonds, (*molecule).bond_max * sizeof(struct bond)); 
        if ((*molecule).bonds == NULL){
            printf("##### Realloc for bonds returned NULL #####\n"); 
            exit(1); 
        }

        (*molecule).bond_ptrs = realloc((*molecule).bond_ptrs, (*molecule).bond_max * sizeof(struct bond*)); 
        if ((*molecule).bond_ptrs == NULL){
            printf("##### Realloc for bond_ptrs returned NULL #####\n"); 
            exit(1); 
        }
        
        for (int i = 0; i < (*molecule).bond_no; i++) (*molecule).bond_ptrs[i] = &(*molecule).bonds[i]; 
    }
   
    memcpy(&(*molecule).bonds[(*molecule).bond_no], &(*bond), sizeof(struct bond)); 
    (*molecule).bond_ptrs[(*molecule).bond_no] = &(*molecule).bonds[(*molecule).bond_no]; 
    (*molecule).bond_no++; 

    return; 
}

int cmp_atom(const void * a, const void * b)
{ 

    double a_val = (*(*(atom**)a)).z; 
    double b_val = (*(*(atom**)b)).z; 

    return (a_val > b_val) - (a_val < b_val); 
}

int bond_comp(const void *a, const void *b)
{

    double a_val = (*(*(bond**)a)).z; 
    double b_val = (*(*(bond**)b)).z; 

    return (a_val > b_val) - (a_val < b_val); 
}

void molsort(molecule *molecule)
{

    if (molecule == NULL) return; 

    if ((*molecule).atom_no > 1) 
    {
        qsort((*molecule).atom_ptrs, (*molecule).atom_no, sizeof(atom**), cmp_atom); 
    }
    
    if ((*molecule).bond_no > 1)
    {
        qsort((*molecule).bond_ptrs, (*molecule).bond_no, sizeof(bond**), bond_comp); 
    }

    return; 
}


void xrotation(xform_matrix xform_matrix, unsigned short deg)
{

    double rad = deg * (M_PI / 180.0); 

    xform_matrix[0][0] = 1; 
    xform_matrix[0][1] = 0; 
    xform_matrix[0][2] = 0; 

    xform_matrix[1][0] = 0; 
    xform_matrix[1][1] = cos(rad); 
    xform_matrix[1][2] = sin(rad); 
    xform_matrix[1][2] -= (2 * xform_matrix[1][2]); // turn it into -sin(rad)

    xform_matrix[2][0] = 0; 
    xform_matrix[2][1] = sin(rad); 
    xform_matrix[2][2] = cos(rad); 

    return; 
}


void yrotation(xform_matrix xform_matrix, unsigned short deg)
{

    double rad = deg * (M_PI / 180.0); 

    xform_matrix[0][0] = cos(rad);
    xform_matrix[0][1] = 0; 
    xform_matrix[0][2] = sin(rad); 

    xform_matrix[1][0] = 0; 
    xform_matrix[1][1] = 1; 
    xform_matrix[1][2] = 0; 

    xform_matrix[2][0] = sin(rad); 
    xform_matrix[2][0] -= (2 * xform_matrix[2][0]); // make it -sin(rad)
    xform_matrix[2][1] = 0; 
    xform_matrix[2][2] = cos(rad); 

    return; 
}


void zrotation(xform_matrix xform_matrix, unsigned short deg)
{

    double rad = deg * (M_PI / 180.0); 

    xform_matrix[0][0] = cos(rad);
    xform_matrix[0][1] = sin(rad); 
    xform_matrix[0][1] -= (2 * xform_matrix[0][1]); 
    xform_matrix[0][2] = 0; 

    xform_matrix[1][0] = sin(rad); 
    xform_matrix[1][1] = cos(rad); 
    xform_matrix[1][2] = 0; 

    xform_matrix[2][0] = 0; 
    xform_matrix[2][1] = 0; 
    xform_matrix[2][2] = 1; 

    return; 
}


void mol_xform(molecule *molecule, xform_matrix matrix)
{

    double x_val, y_val, z_val; 

    for (int i = 0; i < molecule->atom_no; i++)
    {

        x_val = molecule->atoms[i].x; 
        y_val = molecule->atoms[i].y; 
        z_val = molecule->atoms[i].z; 

        // multiply row 1 of the matrix by column 1 of the vector 

        (*molecule).atoms[i].x = (matrix[0][0] * x_val) + (matrix[0][1] * y_val) + (matrix[0][2] * z_val); 
        // multiply row 2 of the matrix by column 1 of the vector 
        (*molecule).atoms[i].y = (matrix[1][0] * x_val) + (matrix[1][1] * y_val) + (matrix[1][2] * z_val); 
        // multiply row 3 of the matrix by column 1 of the vector 
        (*molecule).atoms[i].z = (matrix[2][0] * x_val) + (matrix[2][1] * y_val) + (matrix[2][2] * z_val);  
    }

    for (int i = 0; i < (*molecule).bond_no; i++)
    {
        compute_coords(&(*molecule).bonds[i]); 
    }

    return; 
}

void rotationsfree( rotations *rotations ){
    return; 
}

rotations *spin( molecule *mol ){
    return NULL; 
}

