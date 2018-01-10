#/usr/bin/env python

from os import listdir
from os.path import isfile, join, dirname
import sys
import re
import filecmp

import _pythonpath # necessary to find package bml in development
import bml

DATA_DIR = join(dirname(__file__), 'data')
DATA_FILES = [f for f in listdir(DATA_DIR) if isfile(join(DATA_DIR, f)) and re.search(r'\.bml\Z', f) and f != 'test_include.bml']

TMP_DIR = join(dirname(__file__), 'tmp')
EXPECTED_DIR = join(dirname(__file__), 'expected')

def test_content_from_file():
    print("")
    for file in DATA_FILES:
        print("Testing bml.content_from_file(%s)" % (file))
        content = bml.content_from_file(join(DATA_DIR, file))
        assert len(content.nodes) > 0, 'Something must have been parsed'
    return

def test_bml2bss():
    print("")
    for file in DATA_FILES:
        print("Testing bml.bml2bss(%s)" % (file))
        output_filename = file[0:len(file)-4] + '.bss'
        output_filename_expected = join(EXPECTED_DIR, output_filename)
        output_filename = join(TMP_DIR, output_filename)
        content = bml.bml2bss(join(DATA_DIR, file), output_filename)
        assert len(content.nodes) > 0, 'Something must have been parsed'
        assert not(isfile(join(TMP_DIR, file)))
        assert isfile(output_filename)
        assert not(isfile(output_filename_expected)) or filecmp.cmp(output_filename, output_filename_expected)
    return

def test_bml2html():
    print("")
    for file in DATA_FILES:
        print("Testing bml.bml2html(%s)" % (file))
        output_filename = file[0:len(file)-4] + '.htm'
        output_filename_expected = join(EXPECTED_DIR, output_filename)
        output_filename = join(TMP_DIR, output_filename)
        content = bml.bml2html(join(DATA_DIR, file), output_filename)
        assert len(content.nodes) > 0, 'Something must have been parsed'
        assert not(isfile(join(TMP_DIR, file)))
        assert isfile(output_filename)
        assert not(isfile(output_filename_expected)) or filecmp.cmp(output_filename, output_filename_expected)
    return

def test_bml2latex():
    print("")
    for file in DATA_FILES:
        print("Testing bml.bml2latex(%s)" % (file))
        output_filename = file[0:len(file)-4] + '.tex'
        output_filename_expected = join(EXPECTED_DIR, output_filename)
        output_filename = join(TMP_DIR, output_filename)
        content = bml.bml2latex(join(DATA_DIR, file), output_filename)
        assert len(content.nodes) > 0, 'Something must have been parsed'
        assert not(isfile(join(TMP_DIR, file)))
        assert isfile(output_filename)
        assert not(isfile(output_filename_expected)) or filecmp.cmp(output_filename, output_filename_expected)
    return

if __name__ == '__main__':
    test_content_from_file()
    test_bml2bss()
    test_bml2html()
    test_bml2latex()
