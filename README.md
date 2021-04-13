- [BML - Bridge Bidding Markup Language](#org115d667)
- [Using the BML converters](#org89d0d39)
  - [Installation using PyPI](#installation_using_pypi)
  - [Installation from source](#installation_from_source)
    - [Download and install](#download_and_install)
    - [Test](#test)
  - [Help](#help)
    - [bml2bss](#bml2bss)
    - [bml2html](#bml2html)
    - [bml2latex](#bml2latex)
- [Syntax](#orgb7edaf0)
  - [Editor](#editor)
  - [Bidding tables](#org7d04bc7)
    - [Competitive auctions](#orgb09a520)
    - [Hiding from export](#org1ad58a1)
    - [Copy/Cut/Paste](#org6245610)
    - [Seat and vulnerability dependency](#orgedebd00)
  - [Headers and paragraphs](#org611b48c)
  - [Metadata](#orgcac4b8a)
  - [Deal diagrams](#orgd8dc689)
  - [Lists](#org686568f)
  - [Comments](#org423e46a)
  - [Including other files](#orgc6198d8)
  - [Font styles](#org52b95c3)
- [Changelog](#changelog)

<a id="org115d667"></a>

# BML - Bridge Bidding Markup Language

This GitHub repository (<https://github.com/gpaulissen/bml>) created by Gert-Jan Paulissen is a fork of <https://github.com/Kungsgeten/bml> created by Erik Sjöstrand. The BML format and its utilities in this repository are supposed to be backwards compatible unless mentioned otherwise. In order to better distinguish between both BML versions, I may refer to BML 1 (Erik's version) and BML 2 (this version).

The purpose of the *Bridge Bidding Markup Language* (BML) is to offer an easy
way of documenting contract bridge bidding systems. The file(s) created are
supposed to be easy to read for both human and machines. A BML file is created
using an ordinary text editor (like *Notepad* or even better [Notepad++](https://notepad-plus-plus.org/)).

Programs have been written in order to export BML files to the following formats:

-   **HTML:** Outputs a .htm file which can be used on the web. Use bml2html.

-   **LaTeX:** Outputs a .tex file which can be converted to a pdf, using LaTeX. Use bml2latex.

-   **Full Disclosure:** Outputs a .bss file to be used on the popular bridge website [Bridge Base Online](http://www.bridgebase.com) (BBO) where the players are able to submit their own systems in order to have their bids alerted automatically when bidding. Use bml2bss, which can be put on BBO using the BBO desktop Windows client.

Checkout example.txt for an example of how BML looks. Also be sure to check out example.htm, example.tex (and example.pdf) and example.bss to see how BML converts to different formats.

<a id="org89d0d39"></a>

# Using the BML converters

You need Python version 3 or higher in order to use the BML converters. Get it
from <http://www.python.org> or, even better, use
[Miniconda](https://docs.conda.io/en/latest/miniconda.html) so you can have
easily several versions of a Python environment.

<a id="installation_using_pypi"></a>

## Installation using PyPI

To install the BML converters, issue this command from a command line:

```
$ pip install bridge-markup
```

<a id="installation_from_source"></a>

## Installation from source

<a id="download_and_install"></a>

### Download and install

```
$ git clone https://github.com/gpaulissen/bml.git
$ pip install -e .
```

<a id="test"></a>

### Test

To run the tests from the development version you can use the py.test command:

```
$ py.test
```

You may need to install the required test packages first:

```
$ pip install -r test_requirements.txt
```

<a id="help"></a>

## Help

<a id="bml2bss"></a>

### bml2bss

Convert to Bridge Base Online BSS format. See **Full Disclosure** above.

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

<a id="bml2html"></a>

### bml2html

Convert to HTML format. See **HTML** above.

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

The `--tree` command line option creates nice looking bidtable trees (this is the
default). The `--no-tree` does not create such trees.

The `--include-external-files` includes the bml.css style sheet into the
generated output file (this is the default). The `--no-include-external-files`
just creates a link reference to that file but then at run-time that style
sheet should be present.

<a id="bml2latex"></a>

### bml2latex

Convert to LaTeX format. See **LaTeX** above.

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

The `--tree` command line option creates nice looking bidtable trees (this is the
default). The `--no-tree` does not create such trees.

The `--include-external-files` includes the bml.tex package into the generated
output file (this is the default). The `--no-include-external-files`
just adds \\include{bml} to the generated output file but then you must have
the bml.tex at some point where LaTeX can find it.

<a id="orgb7edaf0"></a>

# Syntax

The goal of BML's syntax is to be readable and easy to write. It is heavily inspired by [org-mode](http://orgmode.org/); a plugin included in the powerful text editor [Emacs](http://www.gnu.org/software/emacs/). If using org-mode in Emacs, there's some nifty features which might make it easier to work with BML.

Perhaps the best way to get an introduction to BML is to read example.txt, as it show of a lot of the features of BML.

A BML file can contain a number of elements: bidding tables, text paragraphs, section names, lists and metadata. All elements must be separated by a blank line.


<a id="editor"></a>

## Editor

Please be aware of TAB characters in your BML file. They count as 1 character
but may look like 1 or more spaces. The rules for indentation (described later
on) count the number of whitespace characters (so a SPACE and a TAB count both
for one). So please try to avoid using TAB characters (or convert them to
SPACEs using your editor settings).

The [Notepad++](https://notepad-plus-plus.org/) is a free source code editor
that may be useful to edit BML files. Of course you may use *Notepad* but be
warned about the TAB character.

<a id="org7d04bc7"></a>

## Bidding tables

The most powerful part of BML is the ability to write bidding tables easily. Let's take a look at this basic precision structure:

```
1C  Any hand with 16+ hcp
  1D  Artificial. 0--7 hcp
    1H  Any hand with 20+ hcp
  1HS 5+ suit, forcing to game (8+ hcp)
  1N  Natural game force, 8+ hcp
  2m  5+ suit, forcing to game (8+ hcp)
  2M  6+ suit, 5--7 hcp
1D  Nebulous with 2+!d, 11--15 hcp
1HS 5+ suit, 11--15 hcp
1N  14--16 hcp
2C  6+!c or 5!c and 4!h/!s, 11--15 hcp
2D  4414. 4405, 4305 or 3405, 11--15 hcp
2HS Weak
2N  Weak with 5-5 minors
```

Pretty simple, right? A row is written according to the format <bid> <description>. Each bid may have sub-bids, by increasing the indentation (number of spaces). The text !c, !d, !h and !s will be converted to suit symbols when exported (and so will the bid names in the bid table).

When writing bidding tables you may sometimes want to have a description with linebreaks. This can be done in BML by indenting the description lines at the same level. Here's an example:

```
1C  Polish club, one of three:
    a) 12--14 NT
    b) 15+ hcp and 5+!c
    c) 18+ hcp any distribution
```

Because of the description linebreak feature it isn't possible to start a sub-bid at the same indentation level as the previous bid's description.

You may add equal signs when separating bids and descriptions, instead of only whitespaces, if you prefer that notation. This can make the bidtable easier to read:

```
1m = 3+ minor
1M = 5+ major
1N = 15--17
     May have 5M, 6m or 5-4 minors
2C = Strong and forcing
2X = Weak
2N = 20--21
```

As bids you could type for instance 1C, to show the bid of 1 club. D(iamond), H(eart), S(spade) and N(o trump) work too. You could also use to suits, like 3CD to define both 3C and 3D at the same time. There's also some other special cases:

-   **<digit>m:** Defines both <digit>C and <digit>D
-   **<digit>M:** Defines both <digit>H and <digit>S
-   **<digit>X:** Defines <digit>C, <digit>D, <digit>H and <digit>S
-   **<digit>red:** Defines <digit>D and <digit>H
-   **<digit>black:** Defines <digit>C and <digit>S. Since BML 2.
-   **<digit>step[s]:** Defines the bid <digit> steps above the parent bid (the previous bid made). In response to 1C, 1step would be 1D, 2steps would be 1H etc.

It is worth noticing that whitespace before the **first bid** in the bidding table is ignored. Other indentation whitespace is part of the syntax.

You probably do not want to add your entire system to a single bidding table. The first line in a bidding table is the start of a sequence, if the characters - and/or ; are included in the bid. Here's an example of adding the answers to Stayman to an already existing sequence.

```
1N-2C;
2D No 4 card major
  2H 5+!h, 4!s, invitational
  2S 5+!s, invitational
  3HS Smolen (5+ cards in other major)
2HS 4+ suit
2N  4-4 majors, minimum
3C  4-4 majors, maximum
```

If a bid has already been defined, it will not be overwritten; the first definition stands. Normal bids (like 2C) are evaluated before special bids (like 2X), hence this would work:

```
2C Strong, forcing
  2D Waiting
2X Weak
  2N Ogust
```

<a id="orgb09a520"></a>

### Competitive auctions

In order to describe competitive auctions, use parantheses around the opponents' bids. All bids, even passes, needs to be described in an competitive auction. P stands for Pass, D is for Double and R is for Redouble. Here's an example of a defense to 1NT:

```
(1NT)---
D   Strength, ca 15+
2C  At least 5-4 majors
  (D)
    P  5+!c, suggestion to play
    R  Asking for better/longer major
    2D 5+!d, suggestion to play
  (P)
    2D Asking for better/longer major
2D  A weak major or a strong minor
2HS Constructive
2N  5-5 minors
3X  Preemptive
```

Note that the above only defines competing directly over 1NT, balancing over 1NT would be written as `(1NT)-P-(P)---` instead of `(1NT)---`.


<a id="org1ad58a1"></a>

### Hiding from export

If you add #HIDE at the beginning of a row somewhere in the bidding table, the bidding table will only be exported to Full Disclosure; not HTML nor LaTeX.


<a id="org6245610"></a>

### Copy/Cut/Paste

You could copy/cut sections of bidding tables. This is done by writing #COPY <name> or #CUT <name>. The <name> is later used when pasting the copy. The difference between #COPY and #CUT is that #COPY will preserve the copied rows, while #CUT will remove them (and hence they will not be parsed until pasted). Use #ENDCOPY or #ENDCUT to specify where the copying/cutting ends.

To paste a copied/cut section, use #PASTE <name>. #PASTE takes indentation into consideration, so for instance a #CUT may be done at the top level of the document and later pasted deep into a bidding table. You can also replace text in the copy when pasting, a somewhat complex but powerful tool. This is done by typing #PASTE <name> <target>=<replacement>. A paste may have several targets and replacements. Let's look at an example:

```
#CUT transfer
2\R Transfer
  2\M Transfer accept
  3\M Super accept
#ENDCUT

1N---
2C Stayman
#PASTE transfer \R=D \M=H
#PASTE transfer \R=H \M=S
```


<a id="orgedebd00"></a>

### Seat and vulnerability dependency

By default it doesn't matter which seat you're in, or which vulnerability it is, when you bid. Full Disclosure, however, allows for different meanings of sequences depending on these factors.

To change the vulnerability (for the forthcoming bidding tables) type #VUL <we><them>. Both <we> and <them> can be Y, N or 0: Yes, No or Doesn't matter. #VUL Y0 would mean that where vulnerable, but it doesn't matter if the opponents are.

Seat is changed in a similar way: #SEAT <seat>, where <seat> can be 0 (doesn't matter), 1, 2, 3, 4, 12 (first or second) or 34 (third or fourth).


<a id="org611b48c"></a>

## Headers and paragraphs

In order to write text, just write normal text and separate the paragraphs by blank lines. Any whitespace in the beginning of a row will be ignored.

In order to separate the document into sections, asterisks are used. One for the first level, two for the second level etc.

The character combinations !c, !d, !h and !s will be converted into suit symbols when exported, just as in the case of bidding tables.

```
* The 1!c opening

  Opening 1!c shows at least 16+ hcp, and is forcing. The
  continuation is fairly natural.

  Some hands might be upgraded to 1!c due to distribution, but
  wildly distributional hands might also be downgraded to avoid
  problems if the opponents preempt.

** The 1!d negative

   Responding 1!d shows a hand which doesn't have enough values to
   establish a game force.
```

In the examples above whitespace are used in the beginning of the paragraph lines, in order to make the text easier to read, but doing this is optional.


<a id="orgcac4b8a"></a>

## Metadata

Metadata are written like `#+METADATA:data`, where `METADATA` is the type of the data and `data` is the actual content. The available type of metadata is:

-   **TITLE:** The system's title, and also the title of the document
-   **DESCRIPTION:** A short description of the system
-   **AUTHOR:** The author of the document

```
#+TITLE: Precision club
#+AUTHOR: John Smith
#+DESCRIPTION: Strong club system. Nebulous diamond and 5 card majors
```

The metadata can be set anywhere in the BML file. If the metadata has already been set, it will not be overwritten.


<a id="orgd8dc689"></a>

## Deal diagrams

It is possible to create deal diagrams with BML. **Right now these can only be exported to LaTeX.** Here's an example of a deal diagram:

```
N None 35 4SXS hK
N Kxx T9 xxx Q987x
E Jx AJxxx AJx KTx
S A987xx - Q9xx Axx
W QT KQxxxx KTx Jx
```

The first row is the header row. The header row adds additional information about the deal, and may be excluded if you only want to show the cards. The header row can include the following information:

-   **Dealer:** The dealer of this deal. You simply write the first letter of the player: `N E S W`
-   **Vulnerability:** Who is vulnerable on this deal? You write `NS` (north/south), `EW` (east/west), `None` or `All`
-   **Board number:** If you write a digit, this will be interpreted as the board number. 35 in the example above.
-   **Final contract and declarer:** To specify the final contract of the deal, you simply write the contract (capital letters) and the player which played the contract. In the example above this is `4SXS` (four spades doubled, played by south). If the board is passed out, write `P`.
-   **Lead:** The deal is written with a lower-case suit (`s h d c`), followed by the card (a number or `A K Q J T`).

Any of the above parameters may be excluded from the header row if you do not want to include all the info. They may also be entered in any order. They may be followed by a comma, to make it more readable. The board number may have a # in front of it. You may have any other words in the header row as well, to increase readability.

After the (optional) header row, the hands are specified. Each hand is written on its own row, starting with the player holding the hand (`N E S W`), optionally followed by a colon. Any hand may be excluded if you'd like a diagram not showing all hands. A hand may have any number of cards but all four suits must be specified, separated by space, in the order spades, hearts, diamonds clubs. A dash `-` is used to notate a void. A card is notated by a number, `A K Q J T` or `x`.

Here's an example of how the above example diagram may be more readable:

```
#35, Dealer N, None vul, played 4SXS with hK lead
N: Kxx    T9     xxx  Q987x
E: Jx     AJxxx  AJx  KTx
S: A987xx -      Q9xx Axx
W: QT     KQxxxx KTx  Jx
```


<a id="org686568f"></a>

## Lists

There are two types of lists available in BML; ordered lists and unordered lists. The syntax is easy:

```
- The first item in an unordered list
- The second item
- Etc..

1. The first item in an ordered list
2. The second item
3. Etc..
```

At the moment it is not possible to have different levels in a BML list.


<a id="org423e46a"></a>

## Comments

If you want to write text which shouldn't be shown in the export, use `//comment here`. Since BML 2 a comment must start at the beginning of a line. If this would not be enforced it is impossible to write internet addresses in your text.


<a id="orgc6198d8"></a>

## Including other files

It is possible to split your system notes into different files. To include another file in a document, use #INCLUDE <filename>. The filename may be a relative path. Let's say you have made a BML file for a multi opening, and placed it into a subfolder called "modules". You could now write #INCLUDE modules/multi.txt where you want the file to be inserted.


<a id="org52b95c3"></a>

## Font styles

By surrounding words/sentences with / \* or = you can make them italic, bold or monospace.

```
/Here's/ *an* =example= (italic, bold, monospace)
```

<a id="changelog"></a>

# Change history

See the Changelog (CHANGELOG.md).
