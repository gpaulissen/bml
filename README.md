# BML

This project defines a Bridge Markup Language that can be used to describe a
bridge system in text format. The advantage is that you can store it in a
source code repository like GitHub and thus easily can see the differences
between versions. Plus it is much quicker to write with a text editor than a
WYSIWYG editor, in my humble opinion.

This README describes how to install the following three executables that
convert a BML file (see Usage):
- bml2bss
- bml2html
- bml2latex

See also the [README.org](README.org) for a description of the Bridge Markup
Language. This is a text file that can be read in any text editor. However,
the best way to read it is in the Emacs editor with [Emacs Org
mode](https://orgmode.org/).

## Installation

This utility uses Python version 3 or higher. Install [Python](http://www.python.org) (and pip) first.

### Using pip

To install the utility, issue:

```
$ pip install bridge-markup
```

### Development version from source

```
$ git clone https://github.com/gpaulissen/bml.git
$ pip install -e .
```

## Test

To run the tests from the development version you can use the py.test command:

```
$ py.test
```

You may need to install the required test packages first:

```
$ pip install -r test_requirements.txt
```

## Usage

### bml2bss

Convert to Bridge Base Online BSS format. See **Full Disclosure** in README.org.

```
$ bml2bss -h
```

You should see at least:

```
usage: Convert BML to BSS. [-h] [-i {1,2,3,4,5,6,7,8,9}] [-o OUTPUTFILE] [-v] inputfile

positional arguments:
  inputfile             the input file (- is stdin)

optional arguments:
  -h, --help            show this help message and exit
  -i {1,2,3,4,5,6,7,8,9}, --indentation {1,2,3,4,5,6,7,8,9}
                        the indentation of a bidtable
  -o OUTPUTFILE, --outputfile OUTPUTFILE
                        the output file (- is stdout)
  -v, --verbose         increase output verbosity
```

### bml2html

Convert to HTML format. See **HTML** in README.org.

```
$ bml2html -h
```

You should see at least:

```
usage: Convert BML to HTML. [-h] [-i {1,2,3,4,5,6,7,8,9}] [-o OUTPUTFILE] [-v] [--tree | --no-tree] [--include-external-files | --no-include-external-files] inputfile

positional arguments:
  inputfile             the input file (- is stdin)

optional arguments:
  -h, --help            show this help message and exit
  -i {1,2,3,4,5,6,7,8,9}, --indentation {1,2,3,4,5,6,7,8,9}
                        the indentation of a bidtable
  -o OUTPUTFILE, --outputfile OUTPUTFILE
                        the output file (- is stdout)
  -v, --verbose         increase output verbosity
  --tree
  --no-tree
  --include-external-files
  --no-include-external-files
```

If no output file is supplied, it is constructed from the input file by
replacing that extension by `.htm` (except of course when the input is `-`).

The `--tree` command line option creates bidtable trees. The default is `--no-tree`.

The `--include-external-files` adds the bml.css style sheet to the generated
output file which adds colours and tree graphics (if set). The default is
`--no-include-external-files`.

### bml2latex

Convert to LaTeX format. See **LaTeX** in README.org.

```
$ bml2latex -h
```

You should see at least:

```
usage: Convert BML to LaTeX. [-h] [-i {1,2,3,4,5,6,7,8,9}] [-o OUTPUTFILE] [-v] [--tree | --no-tree] [--include-external-files | --no-include-external-files] inputfile

positional arguments:
  inputfile             the input file (- is stdin)

optional arguments:
  -h, --help            show this help message and exit
  -i {1,2,3,4,5,6,7,8,9}, --indentation {1,2,3,4,5,6,7,8,9}
                        the indentation of a bidtable
  -o OUTPUTFILE, --outputfile OUTPUTFILE
                        the output file (- is stdout)
  -v, --verbose         increase output verbosity
  --tree
  --no-tree
  --include-external-files
  --no-include-external-files
```

The `--tree` command line option creates bidtable trees. The default is `--no-tree`.

The `--include-external-files` adds the bml.tex package to the generated
output file. The default is `--no-include-external-files`. 

## Change history

See the Changelog (CHANGELOG.md).
