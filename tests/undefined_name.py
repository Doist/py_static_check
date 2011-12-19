"""
$ ./py_static_check/main.py tests/undefined_name.py

tests/undefined_name.py:5: undefined name 'paths
"""
from os import path

def function_with_error():
    print path
    print paths
