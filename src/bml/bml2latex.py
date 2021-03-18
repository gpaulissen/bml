import re

from bml import bml
from bml import latex


def main():
    bml.args = bml.parse_arguments(description='Convert BML to LaTeX.')
    if not bml.args.outputfile:
        bml.args.outputfile = '-' if bml.args.inputfile == '-' else re.sub(r'\..+\Z', '.tex', bml.args.inputfile)
    if bml.args.verbose >= 1:
        print("Output file:", bml.args.outputfile)
    latex.bml2latex(bml.args.inputfile, bml.args.outputfile)
