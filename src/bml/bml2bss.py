from bml import bml
from bml import bss


def main():
    bml.args = bml.parse_arguments(description='Convert BML to BSS.', option_tree=False, option_include_external_files=False, option_indentation=False, output_extension=bss.EXTENSION)
    bss.bml2bss(bml.args.inputfile, bml.args.outputfile)


if __name__ == '__main__':
    main()
