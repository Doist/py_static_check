"""
$ ./py_static_check/main.py tests/redefinition_of_function.py

tests/redefinition_of_function.py:7: redefinition of function 'redefined_function' from line 6
"""
def redefined_function(): pass
def redefined_function(): pass
