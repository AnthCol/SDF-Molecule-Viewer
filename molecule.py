# This file was automatically generated by SWIG (https://www.swig.org).
# Version 4.1.1
#
# Do not make changes to this file unless you know what you are doing - modify
# the SWIG interface file instead.

from sys import version_info as _swig_python_version_info
# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _molecule
else:
    import _molecule

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)


def _swig_setattr_nondynamic_instance_variable(set):
    def set_instance_attr(self, name, value):
        if name == "this":
            set(self, name, value)
        elif name == "thisown":
            self.this.own(value)
        elif hasattr(self, name) and isinstance(getattr(type(self), name), property):
            set(self, name, value)
        else:
            raise AttributeError("You cannot add instance attributes to %s" % self)
    return set_instance_attr


def _swig_setattr_nondynamic_class_variable(set):
    def set_class_attr(cls, name, value):
        if hasattr(cls, name) and not isinstance(getattr(cls, name), property):
            set(cls, name, value)
        else:
            raise AttributeError("You cannot add class attributes to %s" % cls)
    return set_class_attr


def _swig_add_metaclass(metaclass):
    """Class decorator for adding a metaclass to a SWIG wrapped class - a slimmed down version of six.add_metaclass"""
    def wrapper(cls):
        return metaclass(cls.__name__, cls.__bases__, cls.__dict__.copy())
    return wrapper


class _SwigNonDynamicMeta(type):
    """Meta class to enforce nondynamic attributes (no new attributes) for a class"""
    __setattr__ = _swig_setattr_nondynamic_class_variable(type.__setattr__)


M_PI = _molecule.M_PI
class atom(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    element = property(_molecule.atom_element_get, _molecule.atom_element_set)
    x = property(_molecule.atom_x_get, _molecule.atom_x_set)
    y = property(_molecule.atom_y_get, _molecule.atom_y_set)
    z = property(_molecule.atom_z_get, _molecule.atom_z_set)

    def __init__(self, element, x, y, z):
        _molecule.atom_swiginit(self, _molecule.new_atom(element, x, y, z))
    __swig_destroy__ = _molecule.delete_atom

# Register atom in _molecule:
_molecule.atom_swigregister(atom)
class bond(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    a1 = property(_molecule.bond_a1_get, _molecule.bond_a1_set)
    a2 = property(_molecule.bond_a2_get, _molecule.bond_a2_set)
    epairs = property(_molecule.bond_epairs_get, _molecule.bond_epairs_set)
    atoms = property(_molecule.bond_atoms_get, _molecule.bond_atoms_set)
    x1 = property(_molecule.bond_x1_get, _molecule.bond_x1_set)
    x2 = property(_molecule.bond_x2_get, _molecule.bond_x2_set)
    y1 = property(_molecule.bond_y1_get, _molecule.bond_y1_set)
    y2 = property(_molecule.bond_y2_get, _molecule.bond_y2_set)
    z = property(_molecule.bond_z_get, _molecule.bond_z_set)
    len = property(_molecule.bond_len_get, _molecule.bond_len_set)
    dx = property(_molecule.bond_dx_get, _molecule.bond_dx_set)
    dy = property(_molecule.bond_dy_get, _molecule.bond_dy_set)

    def __init__(self, bond):
        _molecule.bond_swiginit(self, _molecule.new_bond(bond))
    __swig_destroy__ = _molecule.delete_bond

# Register bond in _molecule:
_molecule.bond_swigregister(bond)
class molecule(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    atom_max = property(_molecule.molecule_atom_max_get, _molecule.molecule_atom_max_set)
    atom_no = property(_molecule.molecule_atom_no_get, _molecule.molecule_atom_no_set)
    atoms = property(_molecule.molecule_atoms_get, _molecule.molecule_atoms_set)
    atom_ptrs = property(_molecule.molecule_atom_ptrs_get, _molecule.molecule_atom_ptrs_set)
    bond_max = property(_molecule.molecule_bond_max_get, _molecule.molecule_bond_max_set)
    bond_no = property(_molecule.molecule_bond_no_get, _molecule.molecule_bond_no_set)
    bonds = property(_molecule.molecule_bonds_get, _molecule.molecule_bonds_set)
    bond_ptrs = property(_molecule.molecule_bond_ptrs_get, _molecule.molecule_bond_ptrs_set)

    def __init__(self):
        _molecule.molecule_swiginit(self, _molecule.new_molecule())
    __swig_destroy__ = _molecule.delete_molecule

    def append_atom(self, element, x, y, z):
        return _molecule.molecule_append_atom(self, element, x, y, z)

    def append_bond(self, a1, a2, epairs):
        return _molecule.molecule_append_bond(self, a1, a2, epairs)

    def get_atom(self, i):
        return _molecule.molecule_get_atom(self, i)

    def get_bond(self, i):
        return _molecule.molecule_get_bond(self, i)

    def sort(self):
        return _molecule.molecule_sort(self)

    def xform(self, xform_matrix):
        return _molecule.molecule_xform(self, xform_matrix)

# Register molecule in _molecule:
_molecule.molecule_swigregister(molecule)
class mx_wrapper(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    xform_matrix = property(_molecule.mx_wrapper_xform_matrix_get, _molecule.mx_wrapper_xform_matrix_set)

    def __init__(self, xrot, yrot, zrot):
        _molecule.mx_wrapper_swiginit(self, _molecule.new_mx_wrapper(xrot, yrot, zrot))
    __swig_destroy__ = _molecule.delete_mx_wrapper

# Register mx_wrapper in _molecule:
_molecule.mx_wrapper_swigregister(mx_wrapper)

def atomset(atom, element, x, y, z):
    return _molecule.atomset(atom, element, x, y, z)

def atomget(atom, element, x, y, z):
    return _molecule.atomget(atom, element, x, y, z)

def molmalloc(atom_max, bond_max):
    return _molecule.molmalloc(atom_max, bond_max)

def molcopy(src):
    return _molecule.molcopy(src)

def molfree(ptr):
    return _molecule.molfree(ptr)

def molappend_atom(molecule, atom):
    return _molecule.molappend_atom(molecule, atom)

def molappend_bond(molecule, bond):
    return _molecule.molappend_bond(molecule, bond)

def molsort(molecule):
    return _molecule.molsort(molecule)

def xrotation(xform_matrix, deg):
    return _molecule.xrotation(xform_matrix, deg)

def yrotation(xform_matrix, deg):
    return _molecule.yrotation(xform_matrix, deg)

def zrotation(xform_matrix, deg):
    return _molecule.zrotation(xform_matrix, deg)

def mol_xform(molecule, matrix):
    return _molecule.mol_xform(molecule, matrix)

def cmp_atom(a, b):
    return _molecule.cmp_atom(a, b)

def bondset(bond, a1, a2, atoms, epairs):
    return _molecule.bondset(bond, a1, a2, atoms, epairs)

def bondget(bond, a1, a2, atoms, epairs):
    return _molecule.bondget(bond, a1, a2, atoms, epairs)

def compute_coords(bond):
    return _molecule.compute_coords(bond)

def bond_comp(a, b):
    return _molecule.bond_comp(a, b)
class rotations(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    x = property(_molecule.rotations_x_get, _molecule.rotations_x_set)
    y = property(_molecule.rotations_y_get, _molecule.rotations_y_set)
    z = property(_molecule.rotations_z_get, _molecule.rotations_z_set)

    def __init__(self):
        _molecule.rotations_swiginit(self, _molecule.new_rotations())
    __swig_destroy__ = _molecule.delete_rotations

# Register rotations in _molecule:
_molecule.rotations_swigregister(rotations)

