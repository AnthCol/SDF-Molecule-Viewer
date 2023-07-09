CC = clang
CFLAGS = -std=c99 -Wall -pedantic -g
PY_PATH = /usr/include/python3.11
PY_LIB_PATH = /usr/lib/python3.11/config-3.7m-x86_64-linux-gnu

all: libmol.so mol.o swig molecule_wrap.o _molecule.so 

clean:
	rm -f *.o *so 

swig:
	swig -python molecule.i

libmol.so: mol.o
	$(CC) mol.o -shared -o libmol.so -lm

mol.o: mol.c mol.h
	$(CC) $(CFLAGS) -c mol.c -fPIC -o mol.o

molecule_wrap.o: molecule_wrap.c
	$(CC) $(CFLAGS) -I$(PY_PATH) -c molecule_wrap.c -fPIC -o molecule_wrap.o

_molecule.so: molecule_wrap.o libmol.so
	$(CC) molecule_wrap.o -shared -L. -lmol -L$(PY_LIB_PATH) -lpython3.7m -dynamiclib -o _molecule.so 
