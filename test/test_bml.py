#/usr/bin/env python

from os import listdir
from os.path import isfile, join
import sys
import re

import _pythonpath # necessary to find package bml in development
import bml

DATA_PATH = 'data'
DATA_FILES = [join(DATA_PATH, f) for f in listdir(DATA_PATH) if isfile(join(DATA_PATH, f)) and re.search(r'\.bml\Z', f) and f != 'test_include.bml']

def test_content_from_file():
    print("")
    for file in DATA_FILES:
        print("Testing bml.content_from_file(%s)" % (file))
        content = bml.content_from_file(file)
        assert(len(content.nodes) > 0)
    return

def test_bml2bss():
    print("")
    for file in DATA_FILES:
        print("Testing bml.bml2bss(%s)" % (file))
        content = bml.bml2bss(file, '-')
        assert(len(content.nodes) > 0)
    return

def test_bml2html():
    print("")
    for file in DATA_FILES:
        print("Testing bml.bml2html(%s)" % (file))
        content = bml.bml2html(file, '-')
        assert(len(content.nodes) > 0)
    return

def test_bml2latex():
    print("")
    for file in DATA_FILES:
        print("Testing bml.bml2latex(%s)" % (file))
        content = bml.bml2latex(file, '-')
        assert(len(content.nodes) > 0)
    return

if __name__ == '__main__':
    test_content_from_file()
    test_bml2bss()
    test_bml2html()
    test_bml2latex()
