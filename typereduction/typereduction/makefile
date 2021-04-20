all: 
	gcc -c -fPIC typereduction.c -o typereduction.o
	gcc -shared -Wl,-soname,libtypereduction.so -o libtypereduction.so typereduction.o
