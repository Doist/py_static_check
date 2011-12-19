"""
$ ./py_static_check/main.py tests/assigned_but_never_used.py

tests/assigned_but_never_used.py:8: local variable 'local_var' is assigned to but never used
"""
def function_with_error():
    def inner_fn():
        local_var = ""
