- [BML - Bridge Bidding Markup Language](#org115d667)
- [Using the BML converters](#org89d0d39)
  - [Help](#help)
    - [bml2bss](#bml2bss)
    - [bml2html](#bml2html)
    - [bml2latex](#bml2latex)
    - [bss2bml](#bss2bml)
    - [latexmk](#latexmk)
- [BML Syntax](#orgb7edaf0)
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
- [BSS Lifecycle Note](#bss_lifecycle_note)
- [BSS Syntax](#bss_syntax)
  - [Header Record](#bss_header_record)
  - [Stock Convention Card Record](#bss_stock_convention_card_record)
  - [Bidding Sequence](#bss_bidding_sequence)
  - [Convention Record](#bss_convention_record)
  - [Defensive Carding Record](#bss_defensive_carding_record)
- [Changelog](#changelog)

<a id="org115d667"></a>

# BML - Bridge Bidding Markup Language

This GitHub repository (<https://github.com/gpaulissen/bml>) created by Gert-Jan Paulissen is a fork of <https://github.com/Kungsgeten/bml> created by Erik Sjöstrand. The BML format and its utilities in this repository are supposed to be backwards compatible unless mentioned otherwise. In order to better distinguish between both BML versions, I may refer to BML 1 (Erik's version) and BML 2 (this version).

The purpose of the *Bridge Bidding Markup Language* (BML) is to offer an easy
way of documenting contract bridge bidding systems. The file(s) created are
supposed to be easy to read for both human and machines. A BML file is created
using an ordinary text editor (like *Notepad* or even better [Notepad++](https://notepad-plus-plus.org/)).

Programs have been written in order to export BML files to the following formats:

-   **HTML**: Outputs a .htm file which can be used on the web. Use bml2html.

-   **LaTeX**: Outputs a .tex file which can be converted to a pdf, using LaTeX. Use bml2latex.

-   **Full Disclosure**: Outputs a .bss file to be used on the popular bridge website [Bridge Base Online](http://www.bridgebase.com) (BBO) where the players are able to submit their own systems in order to have their bids alerted automatically when bidding. Use bml2bss.

Please note that this option is obsolete now. The BBO web version does not
support it anymore. An alternative may be
[BBOalert](https://github.com/stanmaz/BBOalert) that allows you to upload these
.bss files. In the past you could use the BBO desktop Windows client to upload
.bss files.

Checkout example.txt for an example of how BML looks. Also be sure to check
out example.htm, example.tex (and example.pdf) and example.bss to see how BML
converts to different formats.

There is also a program to convert back to BML format:

-   **BML**: Outputs a .bml file from a .bss file. Use bss2bml.

Allows you to reformat a .bml file by converting it first to .bss and then
back to .bml. You will loose all the features of BML except the bidding tables
though.

It may also be handy when you have received a BBO .bss file and you want to
create a first draft of a .bml file.

<a id="org89d0d39"></a>

# Using the BML converters

See the [BML Installation
Guide](https://gpaulissen.github.io/blog/bml-installation) for how to install
the converters of BML.

After the installation the BML converters are available on your system and you
can use them most easily using a command prompt.

<a id="help"></a>

## Help

<a id="bml2bss"></a>

### bml2bss

Convert to Bridge Base Online BSS format. See **Full Disclosure** above.

Open a command prompt and issue:

```
bml2bss -h
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

Open a command prompt and issue:

```
bml2html -h
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

Open a command prompt and issue:

```
bml2latex -h
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

<a id="bss2bml"></a>

### bss2bml

Convert BSS to BML format. See **BML** above.

Open a command prompt and issue:

```
bss2bml -h
```

You should see at least:

```
usage: Convert BSS to BML. [-h] [-i {1,2,3,4,5,6,7,8,9}] [-o OUTPUTFILE] [-v] inputfile

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

<a id="latexmk"></a>

### latexmk

This program (not part of BML) lets you convert LaTeX (.tex) file to a PDF (or other file types).

Open a command prompt and issue this command to get help:

```
latexmk -h
```

To generate PDFs from every .tex files found in the current directory you just issue:

```
latexmk -pdf
```

To generate file /tmp/test.pdf from file test.tex, you just issue:

```
latexmk -pdf -output-directory=/tmp test.tex
```

The installation of this program that belongs to LaTeX is covered by the [BML Installation
Guide](https://gpaulissen.github.io/blog/bml-installation).

<a id="orgb7edaf0"></a>

# BML Syntax

The goal of BML's syntax is to be readable and easy to write. It is heavily
inspired by [org-mode](http://orgmode.org/); a plugin included in the powerful
text editor [Emacs](http://www.gnu.org/software/emacs/). If using org-mode in
Emacs, there are some nifty features which might make it easier to work with BML.

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
  2CD  5+ suit, forcing to game (8+ hcp)
  2HS  6+ suit, 5--7 hcp
1D  Nebulous with 2+!d, 11--15 hcp
1HS 5+ suit, 11--15 hcp
1N  14--16 hcp
2C  6+!c or 5!c and 4!h/!s, 11--15 hcp
2D  4414. 4405, 4305 or 3405, 11--15 hcp
2HS Weak
2N  Weak with 5-5 minors
```

Pretty simple, right? A row is written according to the format &lt;bid&gt; &lt;description&gt;. Each bid may have sub-bids, by increasing the indentation (number of spaces). The text !c, !d, !h and !s will be converted to suit symbols when exported (and so will the bid names in the bid table).

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

As bids you could type for instance 1C, to show the bid of 1 club. D(iamond),
H(eart), S(spade) and N(o trump) work too. You could also use to suits, like
3CD to define both 3C and 3D at the same time. There are also some other
special cases: variable suits.

You can use variable suits m (minor), om (other minor), M (major), oM (other
major) and they can be used for suits **NOT** already used in the sequence
(neither literally nor variable). So for instance when you have a bidding
table of opening bids you can start with 1C and later use 3m for the 3 level
minor preempt openings since m is not used in the sequence yet (1C is not part
of the sequence). But if you use m for any bid in the sequence **after** the
opening bid 1C, m will be diamonds. And om is not possible.

-   **&lt;digit&gt;m**: Defines a minor suit, hence both &lt;digit&gt;C and &lt;digit&gt;D (not used already in the sequence).
-   **&lt;digit&gt;om**: Defines the other minor, hence both &lt;digit&gt;C and &lt;digit&gt;D (but only if &lt;digit&gt;m is used before).
-   **&lt;digit&gt;M**: Defines a major suit, hence both &lt;digit&gt;H and &lt;digit&gt;S (not used already in the sequence).
-   **&lt;digit&gt;oM**: Defines the other major suit, hence both &lt;digit&gt;H and &lt;digit&gt;S (but only if &lt;digit&gt;M is used before).

You can use variable suits X, Y and Z where X &lt; Y &lt; Z. Here too they can be
used for suits **NOT** already used in the sequence (neither literally nor
variable). So for instance if in a bidding table 2X, 1Y and 3Z are used then X
may be clubs, Y hearts and Z spades. But not X diamonds and Y clubs since then
Y &lt; X.

-   **&lt;digit&gt;X**: Defines &lt;digit&gt;C, &lt;digit&gt;D, &lt;digit&gt;H and &lt;digit&gt;S.
-   **&lt;digit&gt;Y**: Defines &lt;digit&gt;C, &lt;digit&gt;D, &lt;digit&gt;H and &lt;digit&gt;S.
-   **&lt;digit&gt;Z**: Defines &lt;digit&gt;C, &lt;digit&gt;D, &lt;digit&gt;H and &lt;digit&gt;S.

And here some more special variables:

-   **&lt;digit&gt;red**: Defines &lt;digit&gt;D and &lt;digit&gt;H
-   **&lt;digit&gt;black**: Defines &lt;digit&gt;C and &lt;digit&gt;S. Since BML 2.
-   **&lt;digit&gt;step[s]**: Defines the bid &lt;digit&gt; steps above the parent bid (the previous bid made). In response to 1C, 1step would be 1D, 2steps would be 1H etc.

In all cases you can not use two or more variables for the same suit so using
m and X for clubs is considered an error.

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

You could copy/cut sections of bidding tables. This is done by writing #COPY &lt;name&gt; or #CUT &lt;name&gt;. The &lt;name&gt; is later used when pasting the copy. The difference between #COPY and #CUT is that #COPY will preserve the copied rows, while #CUT will remove them (and hence they will not be parsed until pasted). Use #ENDCOPY or #ENDCUT to specify where the copying/cutting ends.

To paste a copied/cut section, use #PASTE &lt;name&gt;. #PASTE takes indentation into consideration, so for instance a #CUT may be done at the top level of the document and later pasted deep into a bidding table. You can also replace text in the copy when pasting, a somewhat complex but powerful tool. This is done by typing #PASTE &lt;name&gt; &lt;target&gt;=&lt;replacement&gt;. A paste may have several targets and replacements. Let's look at an example:

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

To change the vulnerability (for the forthcoming bidding tables) type #VUL &lt;we&gt;&lt;them&gt;. Both &lt;we&gt; and &lt;them&gt; can be Y, N or 0: Yes, No or Doesn't matter. #VUL Y0 would mean that where vulnerable, but it doesn't matter if the opponents are.

Seat is changed in a similar way: #SEAT &lt;seat&gt;, where &lt;seat&gt; can be 0 (doesn't matter), 1, 2, 3, 4, 12 (first or second) or 34 (third or fourth).


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

It is possible to split your system notes into different files. To include another file in a document, use #INCLUDE &lt;filename&gt;. The filename may be a relative path. Let's say you have made a BML file for a multi opening, and placed it into a subfolder called "modules". You could now write #INCLUDE modules/multi.txt where you want the file to be inserted.


<a id="org52b95c3"></a>

## Font styles

By surrounding words/sentences with / \* or = you can make them italic, bold or monospace.

```
/Here's/ *an* =example= (italic, bold, monospace)
```

<a id="bss_lifecycle_note"></a>

# BSS Lifecycle Note

Please note that BSS is not supported anymore by Bridge Base Online. The
documentation below will talk about a Full Disclosure editor, which was the
Windows program `bidedit.exe` if I remember it well. I do not know if that
program can still be installed.

But you can still upload BSS files using [BBOalert](https://github.com/stanmaz/BBOalert).

<a id="bss_syntax"></a>

# BSS Syntax

Convention Card Definition and Convention Definition files are ASCII text
files having a '.bss' file name extension. As might be surmised from the use
of a specific file name extension, the files have a well defined format,
including encoding of information. In a defined context, a specific character
will be an encoding of something, for example, a single character will
represent position at the table (including one character to indicate 1st or
2nd position, etc.).

The file consists of a series of 'records'. A record is a line of the text
file : it is terminated by a 'new line' character. The overall format of the
file is:

- A single header record
- Zero or one stock convention card records
- Zero or more bidding sequence records
- Zero or more include (convention) records
- Zero or one defensive carding records

<a id="bss_header_record"></a>

## Header Record

### Format
```
*00 [{<System Name>}] = NYYYYYY [<Summary>]
?00 [{<System Name>}] = NYYYYYY [<Summary>]
```

### Description
The first record in the file is a Header record. The '00' and the '= NYYYYYY'
are ignored (though they must be present).

### File Type
The first character in the record is either an '\*' or a '?'. An '\*' indicates
a standard Convention Card Definition or Convention Definition file; a '?'
identifies a Floating Convention Definition file. Currently the only stock
Floating convention is 'Roman Key Card Blackwood (1430)'.

Although the Full Disclosure editor can be used to open any Convention
Definition file, editing Floating conventions is not currently supported
(nothing will be visible in the editor except the name and description).

### System Name
System Name is the name entered in the Define dialog when editing the convention card file.

### Summary
Summary is the system summary entered in the Define dialog when editing the convention card file.

<a id="bss_stock_convention_card_record"></a>

## Stock Convention Card Record

### Format
```
$ <File Name>
```

### Description
When you edit one of the stock convention cards online, change it, and save it
under a new name, then rather than storing a complete copy of the Convention
Card Definition file, a reference to the stock card is put into your new file.

There can only be one Convention Card Record in a Convention Card Definition
file. If there is one, it appears immediately after the Header record.

### File Name
File Name is the name of the stock Convention Card Definition file. These
files are stored in the 'convcards\\default convcards' subdirectory of the
'Bridge Base Online' directory.

<a id="bss_bidding_sequence"></a>

## Bidding Sequence

### Format
```
  AB <Bidding Sequence> = CDEFGHI J [KL] [<Description>]
* AB <Bidding Sequence> = CDEFGHI J [KL] [<Description>]
```

Records that start with an asterisk represent competitive sequences where They
open; those without the asterisk represent sequences where We open.

The capital letters, except in the name of character strings, represent
encodings : each is a single character representing some information.

### Position
'A' represents the position in which the opening bid is made. Implicitly this
defines the Dealer, which is the label used in the Full Disclosure editor when
defining the bid.

The encoding is:

- 0 : Any position
- 1 : 1st position
- 2 : 2nd position
- 3 : 3rd position
- 4 : 4th position
- 5 : 1st or 2nd position
- 6 : 3rd or 4th position.

### Vulnerability
'B' represents the prevailing vulnerability conditions which apply to the bidding sequence.

In the following list of encodings, the labels used in the Full Disclosure
editor are included in parentheses.

- 0 : Any conditions (Any)
- 1 : Nobody vulnerable (None vul)
- 2 : We are vulnerable; they are not (Only we vul)
- 3 : We are not vulnerable; they are (Only they vul)
- 4 : Both sides are vulnerable (Both vul)
- 5 : We are not vulnerable; they may or may not be (We not vul)
- 6 : We are vulnerable; they may or may not be (We vul)
- 7 : We may or may not be vulnerable; they are not (They not vul)
- 8 : We may or may not be vulnerable; they are (They vul)

### Bidding Sequence
The Bidding Sequence starts immediately after the first two characters and is
terminated by the equals sign ('='). The calls in the sequence are either 'P'
for Pass, 'D' for Double, 'R' for Redouble, or a bid. A bid consists of a
single digit ('1' to '7') followed by the initial letter of the strain ('S',
'H', 'D', 'C', or 'N' for notrump).

Note: If a Qualification is entered for an opponent's bid, then that
qualification will appear as a string within braces (curly brackets). It will
appear after the bid that was qualified and after the intervention. The
qualified bid does not have to be the first one in the sequence; for example,
you might play one agreement over an opponent's transfer bid, but another if
their suit responses to 1NT are natural.

### Artificial Bid
'C' is used to indicate whether the last bid in the sequence is artificial ('Y') or not ('N').

### Possible Outcomes
The next six characters ('D' through 'I') represent the six possible
outcomes. If the outcome is possible, it is a 'Y'; otherwise an 'N'. The
outcomes (possible strains that are still open after the last bid in the
sequence) are, in order:

- D : Clubs
- E : Diamonds
- F : Hearts
- G : Spades
- H : Notrump
- I : Defend undoubled

### Disposition
'J' encodes the Disposition of the last bid in the sequence as defined in Full Disclosure.

The encoding is:

- 0 : no agreement
- 1 : Signoff
- 2 : Non-forcing
- 3 : Constructive
- 4 : Invitational
- 5 : Forcing
- 6 : Forcing to game
- 7 : Slam try
- 8 : Control bid
- 9 : Preemptive
- A : Transfer
- B : Puppet
- C : Relay
- D : Asking bid
- E : Asking bid response
 
### Suit Length
The minimum and maximum promised suit length that apply to the last bid in the bidding sequence are defined by 'K' and 'L' respectively.

If the last bid is a notrump bid, then 'K' and 'L' are omitted.

The digits '0' to '8' are used to represent the actual length for the minimum length ('K').

In the case of the maximum length ('L'), the digits '0' to '7' are used to represent the actual length, and '8' to represent 'Any'.

### Description
The Description string is whatever you entered under Description when you defined the last bid in the bidding sequence.

<a id="bss_convention_record"></a>

## Convention Record

### Format
```
+ <File Name>
```

### Description
When you use Manage Conventions in the Full Disclosure editor, it creates (or
removes) Convention records. These are simply pointers to the appropriate
Convention Definition files.

Multiple Convention Records are allowed, however they cannot be nested (the
Convention Definition file cannot contain further Convention Records).

### File Name
File Name is the name of the Convention Definition file. These files are
stored in the 'conventions' subdirectory of the 'Bridge Base Online'
directory.

<a id="bss_defensive_carding_record"></a>

## Defensive Carding Record

### Comment
There should never be a need to edit or generate this record other than by
using the Full Disclosure editor.

### Format
```
% <Leads vs NT> <Leads vs Suits> <Defensive Signals> [<Description and Other agreements>]
```

### Description
This record represents your carding agreements and, if there is one, is the
last record in the file.

### Leads vs NT
There are 22 characters in this string, each representing one of the card
combinations listed in the Leads vs NT section of the Full Disclosure editor's
Opening Leads section.

The choices you can make in the editor do not always include every card in the
combination; for example, you cannot choose to lead the Queen from Qxx. Of the
available choices, 'B' indicates the top card, 'C' the next lower card, and so
on.

Here is the full list of 22 card combinations:

xx, xxx, xxxx, xxxxx, Qxx, Qxxx, Qxxxx, Qxxxxx, Qxxxxxx, AKx, KQJ, QJ10, J109, 1098, KQ109, AKJ10, AQJ, AJ10, A109, KJ10, K109, Q109

### Leads vs Suits
There are 18 characters in this string, each representing one of the card
combinations listed in the Leads vs Suits section of the Full Disclosure
editor's Opening Leads section.

The encoding is exactly the same as described above.

Here is the full list of 18 card combinations:

xx, xxx, xxxx, xxxxx, Qxx, Qxxx, Qxxxx, Qxxxxx, Qxxxxxx, AK, AKx, KQJ, QJ10, J109, 1098, KJ10, K109, Q109

### Defensive Signals
In the Full Disclosure editor section on Defensive Signals, there are three
sections for signals against notrump contract and three for suit
contracts. Each of those has an agreement for first, second, and third
priority.

Thus the following six sections each have a first, second, and third priority for a total of 18 characters in the Defensive Carding record:

- Partner leads vs NT
- Declarer leads vs NT
- Discards vs NT
- Partner leads vs suit
- Declarer leads vs suit
- Discards vs suit

The choice of agreements listed in the Full Disclosure editor is the same for each of the 18 situations. The encoding is:

- A : No agreement
- B : Attitude (Hi=Enc.)
- C : Attitude (Hi=Disc.)
- D : Attitude (Odd=Enc.)
- E : Attitude (Odd=Disc.)
- F : Count (Hi=Even)
- G : Count (Hi=Odd)
- H : Count (Odd/Even)
- I : Suit Preference (Hi-Hi)
- J : Suit Preference (Hi-Low)
- K : Other

<a id="changelog"></a>

# Change history

See the Changelog (CHANGELOG.md).
