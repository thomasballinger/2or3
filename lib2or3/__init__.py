__version__ = '0.1.0'

import os
import sys
import re

# TODO use ast
# TODO use 2to3
# TODO use pyflakes


def classify_string(s):
    "Returns 2 or 3 based on a string s of Python source code, defaulting to 3"
    first_line = s.splitlines()[0]
    if '#!' in first_line:
        if 'python3' in first_line:
            return 3
        elif 'python2' in first_line:
            return 2
    if 'yield from' in s:
        return 3
    if 'Error, e' in s:
        return 2
    if 'xrange' in s:
        return 2
    if (re.search(r'''u"[^"]*"[.]decode''', s) or
            re.search(r'''u'[^']*'[.]decode''', s) or
            re.search(r'''b"[^"]*"[.]encode''', s) or
            re.search(r'''b'[^']*'[.]encode''', s)):
        return 2
    return 3


def has_pycache(filename):
    "Returns bool for if there exists a __pycache__ directory next to a file"
    neighbors = os.listdir(os.path.dirname(os.path.abspath(filename)))
    if '__pycache__' in neighbors:
        return True
    else:
        return False


def pycache_classify(filename):
    """Returns 3, 2, or None for prediction from  __pycache__ directory

    prefers 3 if both found, returns None if neither found"""
    dirname, name = os.path.split(os.path.abspath(filename))
    neighbors = os.listdir(dirname)
    if '__pycache__' in neighbors:
        classifications = [
            n[-6:-5]
            for n in os.listdir(os.path.join(dirname, '__pycache__'))
            if n.split('.', 1)[0] == name.split('.', 1)[0]]
        if '3' in classifications:
            return 3
        elif '2' in classifications:
            return 2
    return None


def classify(filename):
    r = pycache_classify(filename)
    if r:
        return r
    return classify_string(open(filename).read())


def main(error_if_not=None):
    """Writes 2 or 3 and a newline to stdout, uses exit code for error_if_not"""
    r = classify(sys.argv[-1])
    print r
    if error_if_not is not None:
        sys.exit(0 if r == error_if_not else r)

if __name__ == '__main__':
    main()
