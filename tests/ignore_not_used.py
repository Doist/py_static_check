"""
Appending -i ignores unused names

$ ./py_static_check/main.py -i tests/ignore_not_used.py

$ ./py_static_check/main.py tests/ignore_not_used.py
tests/ignore_not_used.py:10: 'path' imported but unused

"""
from os import path
