import sys
import os
import re

from bml import bml

__all__ = ['bml2latex']  # only thing to export

SUIT2LATEX = {'C': '\\BC', 'D': '\\BD', 'H': '\\BH', 'S': '\\BS'}

EXTENSION = '.tex'


def latex_replace_suits_bid(matchobj):
    text = matchobj.group(0)
    for s in ['C', 'D', 'H', 'S']:
        text = text.replace(s, SUIT2LATEX[s])
    text = text.replace('N', 'NT')
    text = text.replace('AP', 'All pass')
    return text


def latex_replace_suits_desc(matchobj):
    text = matchobj.group(1)
    for s in ['c', 'd', 'h', 's']:
        text = text.replace('!' + s, SUIT2LATEX[s.upper()])
    if matchobj.group(2) == ' ':
        text += '\\ '
    elif matchobj.group(2) == '\n':
        text += '\\ \n'
    else:
        text += ' ' + matchobj.group(2)
    return text


def latex_replace_suits_header(matchobj):
    text = matchobj.group(1)
    text = text.replace('!c', '\\pdfc')
    text = text.replace('!d', '\\pdfd')
    text = text.replace('!h', '\\pdfh')
    text = text.replace('!s', '\\pdfs')
    if matchobj.group(2) == ' ':
        text += '\\ '
    return text


def latex_bidtable(children, file, first=False):
    bid = None
    desc = None
    EOL = '\n'

    for i in range(len(children)):
        c = children[i]

        bml.logger.debug("child %d: %s" % (i, str(c)))

        if not first:
            if bml.args.tree:
                file.write('\n')
            else:
                file.write('\\\\\n')

        if c.bid != bml.EMPTY:
            bid = re.sub(r'\d([CDHS]|N(?!T))+', latex_replace_suits_bid, c.bid)
            bid = re.sub(r'^P$', 'Pass', bid)
            bid = re.sub(r'^R$', 'Rdbl', bid)
            bid = re.sub(r'^D$', 'Dbl', bid)
            bid = re.sub(r';(?=\S)', '; ', bid)
            bid = bid.replace('->', '$\\rightarrow$')
            dots = "........"[:-1 * len(bid.replace('\\B', ''))]
            # Some characters have a special meaning for LaTeX (issue #8).
            # Replace the backslash first otherwise it interferes with other LaTeX constructions.
            # But before that we need to replace the \n (backslash and n) by another substring that later will be replace by a line feed
            desc = latex_replace_characters(c.desc.replace('\\n', EOL))
        else:
            bid = "\\O"
            desc = None

        if bml.args.tree:
            file.write(' .%d ' % (c.level()))
        file.write(bid)

        if desc:
            desc = re.sub(r'(![cdhs])([^!]?)', latex_replace_suits_desc, desc)
            # Some characters have a special meaning for LaTeX (issue #8).
            # Replace the backslash first otherwise it interferes with other LaTeX constructions.
            # Now replace string EOL by a line feed
            if bml.args.tree:
                desc = desc.replace(EOL, '\\\\\n')
                file.write(dots + '\\begin{minipage}[t]{0.8\\textwidth}\n' + desc.replace('.', '{.}') + '\n\\end{minipage}')
            else:
                desc = desc.replace(EOL, '\\\\\n\\>')
                file.write(' \\> ' + desc)

        if bml.args.tree:
            file.write('. ')

        if len(c.children) > 0:
            if not bml.args.tree:
                file.write('\\+')
            latex_bidtable(c.children, file)
            if not bml.args.tree:
                file.write('\\-')

        first = False


def latex_diagram(diagram, file):
    header = []
    suits = {'S': '\\BS ',
             'H': '\\BH ',
             'D': '\\BD ',
             'C': '\\BC '}
    players = {'N': 'North',
               'E': 'East',
               'S': 'South',
               'W': 'West'}
    if diagram.board:
        header.append('Board %s' % diagram.board)
    if diagram.dealer and diagram.vul:
        header.append('%s / %s' % (players[diagram.dealer], diagram.vul))
    elif diagram.dealer:
        header.append(diagram.dealer)
    elif diagram.vul:
        header.append(diagram.vul)
    if diagram.contract:
        level, suit, double, player = diagram.contract
        if level == 'P':
            header.append("Pass")
        else:
            contract = level + suits[suit]
            if double:
                contract += double
            contract += ' by %s' % players[player]
            header.append(contract)
    if diagram.lead:
        suit, card = diagram.lead
        lead = 'Lead ' + suits[suit.upper()]
        lead += card
        header.append(lead)

    header = '\\\\'.join(header)

    def write_hand(hand, handtype):
        if hand:
            handstring = '{\\%s{%s}{%s}{%s}{%s}}\n' % \
                         (handtype, hand[0], hand[1], hand[2], hand[3])
            handstring = handstring.replace('-', '\\void')
            file.write(handstring)
        else:
            file.write('{}\n')
    if diagram.south:
        file.write('\\dealdiagram\n')
        handtype = 'hand'
        if(diagram.west or diagram.east):
            handtype = 'vhand'
        write_hand(diagram.west, handtype)
        write_hand(diagram.north, handtype)
        write_hand(diagram.east, handtype)
        write_hand(diagram.south, handtype)
        file.write('{%s}\n\n' % header)
    elif diagram.north:
        file.write('\\dealdiagramenw\n')
        handtype = 'vhand'
        write_hand(diagram.west, handtype)
        write_hand(diagram.north, handtype)
        write_hand(diagram.east, handtype)
        file.write('{%s}\n\n' % header)
    else:
        file.write('\\dealdiagramew\n')
        handtype = 'vhand'
        write_hand(diagram.west, handtype)
        write_hand(diagram.east, handtype)


def replace_quotes(matchobj):
    return "``" + matchobj.group(1) + "''"


def replace_strong(matchobj):
    return '\\textbf{' + matchobj.group(1) + '}'


def replace_italics(matchobj):
    return '\\emph{' + matchobj.group(1) + '}'


def replace_truetype(matchobj):
    return '\\texttt{' + matchobj.group(1) + '}'


def latex_replace_characters(text):
    # Some characters have a special meaning for LaTeX (issue #8).
    # Replace the backslash first otherwise it interferes with other LaTeX constructions.
    text = text.replace('\\', '\\textbackslash')
    text = text.replace('->', '$\\rightarrow$')
    # see https://tex.stackexchange.com/questions/34580/escape-character-in-latex
    # replace & % $ # _ { } ~ ^ \ by
    # \& \% \$ \# \_ \{ \} \textasciitilde \textasciicircum \textbackslash
    for ch in "&%$#_{}":
        text = text.replace(ch, '\\' + ch)
    text = text.replace('~', '\\textasciitilde')
    text = text.replace('^', '\\textasciicircum')
    text = re.sub(r'(?<=\s)"(\S[^"]*)"', replace_quotes, text, flags=re.DOTALL)
    text = re.sub(r'(?<=\s)\*(\S[^*]*)\*', replace_strong, text, flags=re.DOTALL)
    text = re.sub(r'(?<=\s)/(\S[^/]*)/', replace_italics, text, flags=re.DOTALL)
    text = re.sub(r'(?<=\s)=(\S[^=]*)=', replace_truetype, text, flags=re.DOTALL)
    return text


def to_latex(content, f):
    # the preamble
    # TODO: Config file for the preamble?
    if bml.args.tree:
        usepackage_dirtree = r"""\usepackage{dirtree}"""
    else:
        usepackage_dirtree = ""

    bml_tex_str = None
    if not bml.args.include_external_files:
        bml_tex_str = "\\include{bml}"
    else:
        with open(os.path.join(os.path.dirname(__file__), 'bml.tex'), 'r') as bml_tex:
            bml_tex_str = bml_tex.read()

    preamble = r"""\documentclass[a4paper]{article}
\usepackage[margin=1in]{geometry}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{newcent}
\usepackage{helvet}
\usepackage{graphicx}
%s
\usepackage[pdftex, pdfborder={0 0 0}]{hyperref}
\frenchspacing

%s
""" % (usepackage_dirtree, bml_tex_str)

    f.write(preamble)
    for s in ['TITLE', 'AUTHOR']:
        f.write('\\%s{%s}\n' % (s.lower(), content.meta[s] if s in content.meta else 'No ' + s.lower() + ' defined'))

    f.write('\\begin{document}\n')
    f.write('\\maketitle\n')
    f.write('\\tableofcontents\n\n')

    new_paragraph = '\n\\bigbreak\n'

    # then start the document
    for c in content.nodes:
        content_type, text = c
        if content_type == bml.ContentType.PARAGRAPH:
            # Some characters have a special meaning for LaTeX (issue #8).
            # Replace characters (and thus backslash) before suits are replaced.
            text = latex_replace_characters(text)
            text = re.sub(r'(![cdhs])([^!]?)', latex_replace_suits_desc, text)
            f.write(text + new_paragraph)
        elif content_type == bml.ContentType.BIDTABLE:
            if not text.export:
                continue
            if bml.args.tree:
                f.write('\\\n')
                f.write('\\dirtree{%%\n')
            else:
                f.write('\\begin{bidtable}\n')
            latex_bidtable(text.children, f, True)
            if bml.args.tree:
                f.write('\n}')
            else:
                f.write('\n\\end{bidtable}')
            f.write(new_paragraph)
        elif content_type == bml.ContentType.DIAGRAM:
            latex_diagram(text, f)
        elif content_type == bml.ContentType.H1:
            text = latex_replace_characters(text)
            text = re.sub(r'(![cdhs])( ?)', latex_replace_suits_header, text)
            f.write('\\section{%s}' % text + '\n\n')
        elif content_type == bml.ContentType.H2:
            text = latex_replace_characters(text)
            text = re.sub(r'(![cdhs])( ?)', latex_replace_suits_header, text)
            f.write('\\subsection{%s}' % text + '\n\n')
        elif content_type == bml.ContentType.H3:
            text = latex_replace_characters(text)
            text = re.sub(r'(![cdhs])( ?)', latex_replace_suits_header, text)
            f.write('\\subsubsection{%s}' % text + '\n\n')
        elif content_type == bml.ContentType.H4:
            text = latex_replace_characters(text)
            text = re.sub(r'(![cdhs])( ?)', latex_replace_suits_header, text)
            f.write('\\paragraph{%s}' % text + '\n\n')
        elif content_type == bml.ContentType.LIST:
            f.write('\\begin{itemize}\n')
            for i in text:
                i = latex_replace_characters(i)
                i = re.sub(r'(![cdhs])([^!]?)', latex_replace_suits_desc, i)
                f.write('\\item %s\n' % i)
            f.write('\n\\end{itemize}')
            f.write(new_paragraph)
        elif content_type == bml.ContentType.DESCRIPTION:
            f.write('\\begin{description}\n')
            for i in text:
                i = latex_replace_characters(i)
                i = re.sub(r'(![cdhs])([^!]?)', latex_replace_suits_desc, i)
                i = i.split(' :: ')
                f.write('\\item[%s] %s\n' % (i[0], i[1]))
            f.write('\n\\end{description}')
            f.write(new_paragraph)
        elif content_type == bml.ContentType.ENUM:
            f.write('\\begin{enumerate}\n')
            for i in text:
                i = latex_replace_characters(i)
                i = re.sub(r'(![cdhs])([^!]?)', latex_replace_suits_desc, i)
                f.write('\\item %s\n' % i)
            f.write('\n\\end{enumerate}')
            f.write(new_paragraph)
        elif content_type == bml.ContentType.TABLE:
            f.write('\\begin{tabular}{')
            columns = 0
            for i in text:
                if len(i) > columns:
                    columns = len(i)
            f.write('l' * columns)
            f.write('}\n')
            for i in text:
                if re.match(r'[+-]+$', i[0]):
                    f.write('\\hline\n')
                else:
                    f.write(' & '.join(i))
                    f.write(' \\\\\n')
            f.write('\\end{tabular}\n\n')
            f.write(new_paragraph)
        elif content_type == bml.ContentType.BIDDING:
            f.write('\\begin{bidding}\n')
            for i, r in enumerate(text):
                r = ' \\> '.join(r)
                r = re.sub(r'\d([CDHS]|N(?!T))+', latex_replace_suits_bid, r)
                r = r.replace('AP', 'All pass')
                r = r.replace('D', 'Dbl')
                r = r.replace('P', 'Pass')
                r = r.replace('R', 'Rdbl')

                f.write(r)
                if i < len(text) - 1:
                    f.write('\\\\\n')
            f.write('\n\\end{bidding}')
            f.write(new_paragraph)

    f.write('\\end{document}\n')


def bml2latex(input_filename, output_filename, content=None):
    if content is None:
        content = bml.content_from_file(input_filename)
    if output_filename == '-':
        to_latex(content, sys.stdout)
    else:
        if os.path.isdir(output_filename):
            output_filename = os.path.join(output_filename, os.path.basename(re.sub(r'\..+\Z', EXTENSION, input_filename)))
        with open(output_filename, mode='w', encoding="utf-8") as f:
            to_latex(content, f)
    return content
