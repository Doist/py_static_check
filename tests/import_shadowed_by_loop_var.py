"""
$ ./py_static_check/main.py tests/import_shadowed_by_loop_var.py

tests/import_shadowed_by_loop_var.py:10: import 'os' from line 6 shadowed by loop variable
"""
import os

print os

for os in range(0, 10):
    pass
