#!/usr/bin/python
import sys
import os
import _ast
import pyflakes
import getopt

from modified_checker import Checker


#--- Globals ----------------------------------------------
STAR_IMPORTS = None
IGNORE_UNUSED_IMPORT = False


#--- Checker ----------------------------------------------
def check(codeString, filename):
    """
    Check the Python source given by C{codeString} for flakes.

    @param codeString: The Python source to check.
    @type codeString: C{str}

    @param filename: The name of the file the source came from, used to report
        errors.
    @type filename: C{str}

    @return: The number of warnings emitted.
    @rtype: C{list}
    """
    # First, compile into an AST and handle syntax errors.
    try:
        tree = compile(codeString, filename, "exec", _ast.PyCF_ONLY_AST)
    except SyntaxError, value:
        msg = value.args[0]

        (lineno, offset, text) = value.lineno, value.offset, value.text

        # If there's an encoding problem with the file, the text is None.
        if text is None:
            # Avoid using msg, since for the only known case, it contains a
            # bogus message that claims the encoding the file declared was
            # unknown.
            print >> sys.stderr, "%s: problem decoding source" % (filename, )
        else:
            line = text.splitlines()[-1]

            if offset is not None:
                offset = offset - (len(text) - len(line))

            print >> sys.stderr, '%s:%d: %s' % (filename, lineno, msg)
            print >> sys.stderr, line

            if offset is not None:
                print >> sys.stderr, " " * offset, "^"

        return []
    else:
        # Okay, it's syntactically valid. Now check it.
        w = Checker(tree, filename, STAR_IMPORTS)
        return w.messages


def print_messages(messages):
    type_messages = {}

    for m in messages:
        str_type = str(type(m))

        if IGNORE_UNUSED_IMPORT:
            if 'UnusedImport' in str_type:
                continue
            if 'RedefinedWhileUnused' in str_type:
                continue

        lst = type_messages.setdefault(str_type, [])
        lst.append(m)

    #Sort after line number
    sorted_by_type = {}
    for e_type, messages in type_messages.items():
        sort_tuple = ( (m.filename, m.lineno, m) for m in messages )
        sorted_messages = (t[2] for t in sorted(sort_tuple))
        sorted_by_type[e_type] = sorted_messages

    #Sort after types
    types = sorted_by_type.keys()
    types.sort(reverse=True)

    for t in types:
        for w in sorted_by_type[t]:
            print w


def check_path(filename):
    return check(file(filename).read(), filename)


#--- Script processing ----------------------------------------------
def usage():
    print 'py_static_check a Lint-like tool for Python. It is focused on identifying common errors quickly without executing Python code.'
    print 'py_static_check is based on pyflakes and offers some additioanl features such as handling of star imports.'
    print ''
    print 'Usage:'
    print '    py_static_check file.py directory/'
    print ''
    print 'Options:'
    print '    -h, --help: Displays this message'
    print '    -i, --ignore_unused_imports: Ignore unused imports warning'
    print '    -s, --star_imports: Define a Python file that resolves star imports'
    print '                        this file should export a dictionary (STAR_IMPORTS)'
    print '                        that maps from module_name to a list of names it exports, e.g.'
    print "                        STAR_IMPORTS = {'os': ['path', 'uname']}"
    sys.exit(2)


def run():
    global STAR_IMPORTS, IGNORE_UNUSED_IMPORT

    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   "his:",
                                   ["help", "ignore_unused_imports", "star_imports="])
    except getopt.GetoptError:
        usage()

    #--- Resolve arguments ----------------------------------------------
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()

        if opt in ('-s', '--star_imports'):
            d = {}
            execfile(arg, d)

            star_imports = d.get('STAR_IMPORTS')

            if not star_imports:
                print '%s does not export STAR_IMPORTS!' % (d)
                sys.exit(-1)

            if type(star_imports) != type({}):
                print "%s's STAR_IMPORTS is not a dictionary!" % (d)
                sys.exit(-1)

            STAR_IMPORTS = d['STAR_IMPORTS']

        if opt in ('-i', '--ignore_unused_imports'):
            IGNORE_UNUSED_IMPORT = True


    #--- Run ----------------------------------------------
    messages = []
    if args:
        for arg in args:
            if os.path.isdir(arg):
                for dirpath, dirnames, filenames in os.walk(arg):
                    for filename in filenames:
                        if filename.endswith('.py'):
                            messages.extend( check_path(os.path.join(dirpath, filename)) )
            else:
                messages.extend( check_path(arg) )
    else:
        messages.extend( check(sys.stdin.read(), '<stdin>') )

    print_messages(messages)


if __name__ == "__main__":
    run()
