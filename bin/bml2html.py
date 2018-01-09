#/usr/bin/env python

import re

import _pythonpath # necessary to find package bml in development
import bml

bml.args = bml.parse_arguments(description='Convert BML to HTML.')
if not bml.args.outputfile:
    bml.args.outputfile = '-' if bml.args.inputfile == '-' else re.sub(r'\..+\Z', '.htm', bml.args.inputfile)
if bml.args.verbose >= 1:
    print("Output file:", bml.args.outputfile)
bml.bml2html(bml.args.inputfile, bml.args.outputfile)
