#/usr/bin/env python

import re

import _pythonpath
import bml

bml.args = bml.parse_arguments(description='Convert BML to BSS.', option_tree=False, option_include_external_files=False)
if not bml.args.outputfile:
    bml.args.outputfile = '-' if bml.args.inputfile == '-' else re.sub(r'\..+\Z', '.bss', bml.args.inputfile)
if bml.args.verbose >= 1:
    print("Output file:", bml.args.outputfile)
bml.bml2bss(bml.args.inputfile, bml.args.outputfile)
