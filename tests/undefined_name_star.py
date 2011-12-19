"""
$ ./py_static_check/main.py -s tests/star_import.py tests/undefined_name_star.py

tests/undefined_name.py:5: undefined name 'paths
"""
from os import *

def function_with_error():
    print path
    print paths
