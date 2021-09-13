import sys
import re
import xml.etree.ElementTree as ET
import os.path

from bml import bml

__all__ = ['bml2html']  # only thing to export


EXTENSION = '.htm'


def html_bidtable(et_element, children, root=False):
    NBSP = u'\xa0'

    if len(children) > 0:
        ul = ET.SubElement(et_element, 'ul')
        for i in range(len(children)):
            c = children[i]
            li = ET.SubElement(ul, 'li')
            if not bml.args.tree:
                div = ET.SubElement(li, 'div')
                div.attrib['class'] = 'start'
            elif root:
                li.attrib['class'] = 'root'
            elif i == len(children) - 1:
                li.attrib['class'] = 'last node'
            else:
                li.attrib['class'] = 'node'

            root = False

            desc_rows = c.desc.split('\\n')  # can be more than one line
            bid = re.sub(r'^P$', 'Pass', c.bid)
            bid = re.sub(r'^R$', 'Rdbl', bid)
            bid = re.sub(r'^D$', 'Dbl', bid)
            bml.logger.debug("bid: %s; description line 1: %s" % (bid, desc_rows[0]))

            if not bml.args.tree:
                div.text = bid
                div.tail = desc_rows[0]
                desc_rows = desc_rows[1:]
                for r, dr in enumerate(desc_rows):
                    li = ET.SubElement(ul, 'li')
                    div = ET.SubElement(li, 'div')
                    div.attrib['class'] = 'start'
                    div.text = ' '
                    # GJP 2021-05-09 a single point in a line is also considered empty.
                    # See also https://github.com/gpaulissen/bml/issues/7.
                    div.tail = NBSP if dr == '.' and r == len(desc_rows) - 1 else dr
            elif len(desc_rows) == 1 and (not desc_rows[0] or desc_rows[0].isspace()):
                # empty description: just store the bid
                li.text = bid
            else:
                # use a table to store the bid (one column) and description lines (each line a row)
                table = ET.SubElement(li, 'table')
                for r, dr in enumerate(desc_rows):
                    tr = ET.SubElement(table, 'tr')
                    # bid only first time
                    if r == 0:
                        td = ET.SubElement(tr, 'td')
                        td.text = bid
                        td.attrib['rowspan'] = str(len(desc_rows))
                        td.attrib['class'] = 'node'
                    # description
                    td = ET.SubElement(tr, 'td')
                    # GJP 2021-05-09 a single point in a line is also considered empty.
                    # See also https://github.com/gpaulissen/bml/issues/7.
                    td.text = NBSP if dr == '.' and r == len(desc_rows) - 1 else dr
            html_bidtable(li, c.children)


def html_replace_suits(matchobj):
    text = matchobj.group(0)
    text = text.replace('C', '<span class="ccolor">&clubs;</span>')
    text = text.replace('D', '<span class="dcolor">&diams;</span>')
    text = text.replace('H', '<span class="hcolor">&hearts;</span>')
    text = text.replace('S', '<span class="scolor">&spades;</span>')
    text = text.replace('N', 'NT')
    return text


def replace_strong(matchobj):
    return '<strong>' + matchobj.group(1) + '</strong>'


def replace_italics(matchobj):
    return '<em>' + matchobj.group(1) + '</em>'


def replace_truetype(matchobj):
    return '<code>' + matchobj.group(1) + '</code>'


def to_html(content):
    html = ET.Element('html')
    head = ET.SubElement(html, 'head')
    meta = ET.SubElement(head, 'meta')
    meta.attrib['http-equiv'] = "Content-Type"
    meta.attrib['content'] = "text/html; charset=utf-8"

    title = ET.SubElement(head, 'title')
    title.text = content.meta['TITLE'] if content.meta['TITLE'] else 'No title supplied'

    if not bml.args.include_external_files:
        link = ET.SubElement(head, 'link')
        link.attrib['rel'] = 'stylesheet'
        link.attrib['type'] = 'text/css'
        link.attrib['href'] = 'bml.css'
    else:
        style = ET.SubElement(head, 'style')
        style.attrib['type'] = "text/css"
        with open(os.path.join(os.path.dirname(__file__), 'bml.css'), 'r') as bml_css:
            style.text = bml_css.read()

    body = ET.SubElement(html, 'body')

    for c in content.nodes:
        content_type, text = c
        if content_type == bml.ContentType.PARAGRAPH:
            element = ET.SubElement(body, 'p')
            element.text = text
        elif content_type == bml.ContentType.BIDTABLE:
            if not text.export:
                continue
            element = ET.SubElement(body, 'div')
            element.attrib['class'] = 'tree' if bml.args.tree else 'bidtable'
            html_bidtable(element, text.children, True)
        elif content_type == bml.ContentType.H1:
            element = ET.SubElement(body, 'h1')
            element.text = text
        elif content_type == bml.ContentType.H2:
            element = ET.SubElement(body, 'h2')
            element.text = text
        elif content_type == bml.ContentType.H3:
            element = ET.SubElement(body, 'h3')
            element.text = text
        elif content_type == bml.ContentType.H4:
            element = ET.SubElement(body, 'h4')
            element.text = text
        elif content_type == bml.ContentType.LIST:
            element = ET.SubElement(body, 'ul')
            for i in text:
                li = ET.SubElement(element, 'li')
                li.text = i
        elif content_type == bml.ContentType.ENUM:
            element = ET.SubElement(body, 'ol')
            for i in text:
                li = ET.SubElement(element, 'li')
                li.text = i

    bodystring = str(ET.tostring(body), 'UTF8')

    # Replace "empty bid"
    bodystring = bodystring.replace(bml.EMPTY, '&empty;')

    # GJP 2021-05-05 https://github.com/gpaulissen/bml/issues/4
    # If you use a font style like '/', '*' or '=' at the beginning of a bid description, the generated HTML does not translate it.
    # This was due to the fact that the parser expects whitespace before it. But a closing tag (>) should also be accepted.
    bodystring = re.sub(r'(?<=\s|>)\*(\S[^*<>]*)\*', replace_strong, bodystring, flags=re.DOTALL)
    bodystring = re.sub(r'(?<=\s|>)/(\S[^/<>]*)/', replace_italics, bodystring, flags=re.DOTALL)
    bodystring = re.sub(r'(?<=\s|>)=(\S[^=<>]*)=', replace_truetype, bodystring, flags=re.DOTALL)

    # Replaces !c!d!h!s with suit symbols
    bodystring = bodystring.replace('!c', '<span class="ccolor">&clubs;</span>')
    bodystring = bodystring.replace('!d', '<span class="dcolor">&diams;</span>')
    bodystring = bodystring.replace('!h', '<span class="hcolor">&hearts;</span>')
    bodystring = bodystring.replace('!s', '<span class="scolor">&spades;</span>')

    # Replace "long dashes"
    bodystring = bodystring.replace('---', '&mdash;')
    bodystring = bodystring.replace('--', '&ndash;')

    bodystring = re.sub(r'\d([CDHS]|N(?!T))+', html_replace_suits, bodystring)

    return '<!DOCTYPE html><html lang="en">' + str(ET.tostring(head), 'UTF8') + bodystring + '</html>'


def bml2html(input_filename, output_filename, content=None):
    if content is None:
        content = bml.content_from_file(input_filename)
    h = to_html(content)
    if output_filename == '-':
        sys.stdout.write(h)
    else:
        if os.path.isdir(output_filename):
            output_filename = os.path.join(output_filename, os.path.basename(re.sub(r'\..+\Z', EXTENSION, input_filename)))
        with open(output_filename, mode='w', encoding="utf-8") as f:
            f.write(h)
    return content
