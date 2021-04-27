from bml import bml
from bml import html


def main():
    bml.args = bml.parse_arguments(description='Convert BML to HTML.', output_extension='.htm')
    html.bml2html(bml.args.inputfile, bml.args.outputfile)


if __name__ == '__main__':
    main()
