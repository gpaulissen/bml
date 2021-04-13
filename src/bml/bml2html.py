import re

from bml import bml
from bml import html


def main():
    bml.args = bml.parse_arguments(description='Convert BML to HTML.')
    if not bml.args.outputfile:
        bml.args.outputfile = '-' if bml.args.inputfile == '-' else re.sub(r'\..+\Z', '.htm', bml.args.inputfile)
    bml.logger.debug("Output file:", bml.args.outputfile)
    html.bml2html(bml.args.inputfile, bml.args.outputfile)
