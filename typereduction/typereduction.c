#include <Python.h>

static PyObject *KM_Algorithm(PyObject *self, PyObject *args)
{
	return Py_BuildValue("s", "KM type reduction algorithm!");
}

static char KM_Algorithm_docs[] = "KM Algorithm docs!\n";

static PyMethodDef TypeReduction_funcs[] = {
    {"KM_Algorithm", (PyCFunction)KM_Algorithm, METH_NOARGS, KM_Algorithm_docs},
    {NULL,NULL,0,NULL}
};

static struct PyModuleDef typereduction =
{
	PyModuleDef_HEAD_INIT,
	"typereduction", 
	"A set of type reduction algorithms.\n", /* module documentation, may be NULL */
	-1,   /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
	TypeReduction_funcs
};


PyMODINIT_FUNC PyInit_typereduction(void)
{
    return PyModule_Create(&typereduction);
}









