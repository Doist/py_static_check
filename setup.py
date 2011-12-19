#!/usr/bin/python
from setuptools import setup

setup(
    name="py_static_check",
    license="MIT",
    version="1.1",
    author="amix",
    author_email="amix@amix.dk",
    url="http://www.amix.dk/",
    packages=["py_static_check", "py_static_check.pyflakes"],
    install_requires = ['pyflakes>=0.5'],
    scripts=["bin/py_static_check"],
    classifiers=[
        "Development Status :: 6 - Mature",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Topic :: Software Development",
        "Topic :: Utilities",
    ],

    description="Statically check your Python code",
      long_description="""\
py_static_check
---------------

py_static_check can statically check your Python code for a lot of common errors.
It uses a modified pyflakes code and extends with following things:

 * Ability to specify what star imports resolve to (-s argument)
 * Ability to ignore unused import warnings (-i argument)
 * Better sorting of warnings/errors

For more information check out:

 * http://amix.dk/blog/post/19665#py-static-check-Statically-check-your-Python-code
 * http://amix.dk/blog/post/19361#Static-checking-Python-code

To install it do following:

    sudo easy_install py_static_check


Here are some of the things py_static_check can do.


Catch undefined names, even for star imports
--------------------------------------------

Example code::

    from os import *

    def function_with_error():
        print path
        print paths

star_imports.py::

    import os
    STAR_IMPORTS = {
        'os': os.__all__,
    }

When ran with py_static_check::

    $ py_static_check -s tests/star_import.py tests/undefined_name_star.py
    tests/undefined_name.py:5: undefined name 'paths


Ignore not used warnings
------------------------

Exampel code::

    from os import path

When ran with py_static_check -i option::

    $ py_static_check -i tests/ignore_not_used.py

    $ py_static_check tests/ignore_not_used.py
    tests/ignore_not_used.py:10: 'path' imported but unused


Assigned but never used
-----------------------

Like pyflakes it can catch a lot of errors, such as defining a variable without using it.

Exampel code::

    def some_function():
        def inner_fn():
            local_var = ""

When ran with py_static_check::

    $ py_static_check tests/assigned_but_never_used.py

    tests/assigned_but_never_used.py:8: local variable 'local_var' is assigned to but never used

Copyright: 2011 by amix
License: MIT."""
)
