from os import listdir
from os.path import isfile, join, dirname

import logging

from bml.bml import content_from_file, logger
from bml.bss import bml2bss
from bml.html import bml2html
from bml.latex import bml2latex
from bss.bss2bml import bss2bml

DATA_DIR = join(dirname(__file__), 'data')
DATA_FILES = [f for f in listdir(DATA_DIR) if isfile(join(DATA_DIR, f)) and f != 'test_include.bml']

TMP_DIR = join(dirname(__file__), 'tmp')
EXPECTED_DIR = join(dirname(__file__), 'expected')


def _filecmp(file1, file2):
    with open(file1) as f1, open(file2) as f2:
        for line1, line2 in zip(f1, f2):
            line1 = line1.rstrip()
            line2 = line2.rstrip()

            if (not line1 and not line2) or line1 == line2:
                pass
            else:
                return False
    return True


def _check(output_filename=None, output_filename_expected=None, content=None):
    if output_filename:
        assert isfile(output_filename), 'File %s must exist' % (output_filename)
    if output_filename_expected:
        assert isfile(output_filename_expected), 'Expected file %s must exist' % (output_filename_expected)
    if output_filename and output_filename_expected:
        assert _filecmp(output_filename, output_filename_expected), 'Files %s and %s must be the same' % (output_filename, output_filename_expected)
    if content:
        assert len(content.nodes) > 0, 'Something must have been parsed'


def test_content_from_file():
    print("")
    for file in DATA_FILES:
        print("Testing content_from_file(%s)" % (file))
        content = content_from_file(join(DATA_DIR, file))
        _check(content=content)
    return


def test_bml2bss():
    print("")
    for file in DATA_FILES:
        print("Testing bml2bss(%s)" % (file))
        if file == "example.bml":
            logger.setLevel(logging.DEBUG)
        output_filename = file[0:len(file) - 4] + '.bss'
        output_filename_expected = join(EXPECTED_DIR, output_filename)
        output_filename = join(TMP_DIR, output_filename)
        content = bml2bss(join(DATA_DIR, file), output_filename)
        _check(output_filename, output_filename_expected, content)
    logger.setLevel(logging.INFO)
    return


def test_bml2html():
    print("")
    for file in DATA_FILES:
        print("Testing bml2html(%s)" % (file))
        output_filename = file[0:len(file) - 4] + '.htm'
        output_filename_expected = join(EXPECTED_DIR, output_filename)
        output_filename = join(TMP_DIR, output_filename)
        content = bml2html(join(DATA_DIR, file), output_filename)
        _check(output_filename, output_filename_expected, content)
    return


def test_bml2latex():
    print("")
    for file in DATA_FILES:
        print("Testing bml2latex(%s)" % (file))
        output_filename = file[0:len(file) - 4] + '.tex'
        output_filename_expected = join(EXPECTED_DIR, output_filename)
        output_filename = join(TMP_DIR, output_filename)
        content = bml2latex(join(DATA_DIR, file), output_filename)
        _check(output_filename, output_filename_expected, content)
    return


def test_bss2bml():
    print("")
    for file in [f for f in DATA_FILES if f != 'example.bml']:
        try:
            print("Testing bss.bss2bml(%s)" % (file))
            if file in ["example2.bml"]:
                logger.setLevel(logging.DEBUG)
            input_filename = join(DATA_DIR, file)
            output_filename = file[0:len(file) - 4] + '.bss'
            output_filename_expected = join(EXPECTED_DIR, output_filename)
            output_filename = join(TMP_DIR, output_filename)
            bml2bss(input_filename, output_filename)
            # so we did bml -> bss, now the other way around
            input_filename = output_filename
            output_filename = file
            output_filename_expected = join(EXPECTED_DIR, output_filename)
            output_filename = join(TMP_DIR, output_filename)
            bss2bml(input_filename, output_filename)
            _check(output_filename, output_filename_expected)
        except Exception as e:
            print("ERROR for input file %s" % (input_filename))
            raise e
    logger.setLevel(logging.INFO)
    return


if __name__ == '__main__':
    from bml.bml import args
    args.verbose = 1
    test_content_from_file()
    test_bml2bss()
    test_bml2html()
    test_bml2latex()
    test_bss2bml()
