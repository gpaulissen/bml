from bml import bml


def main():
    bml.args = bml.parse_arguments(description='Generate BML make dependencies.', option_tree=False, option_include_external_files=False, option_indentation=False, output_extension='.mk')
    bml.makedepend(bml.args.inputfile, bml.args.outputfile)


if __name__ == '__main__':
    main()
