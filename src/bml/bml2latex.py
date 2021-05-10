from bml import bml
from bml import latex


def main():
    bml.args = bml.parse_arguments(description='Convert BML to LaTeX.', output_extension=latex.EXTENSION)
    latex.bml2latex(bml.args.inputfile, bml.args.outputfile)


if __name__ == '__main__':
    main()
