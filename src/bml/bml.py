import sys
import os
import re
import copy
from collections import defaultdict
import argparse
from contextlib import contextmanager

__all__ = ['parse_arguments', 'content_from_file', 'Node', 'ContentType',
           'args', 'EMPTY', 'ROOT']

# constants
ROOT = 'root'
EMPTY = '{}'


class Args:
    """The default command line arguments"""
    verbose = None
    indentation = None
    tree = None
    include_external_files = None
    inputfile = None
    outputfile = None

    def __init__(self, verbose=0, indentation=2, tree=False,
                 include_external_files=True, inputfile='-', outputfile='-'):
        self.verbose = verbose
        self.indentation = indentation
        self.tree = tree
        self.include_external_files = include_external_files
        self.inputfile = inputfile
        self.outputfile = outputfile


args = Args()


class Content:
    """The content of a BML file"""
    nodes = None
    clipboard = None
    vulnerability = None
    seat = None
    meta = None

    def __init__(self):
        self.nodes = []  # A list of Nodes
        # where we keep copies
        self.clipboard = {}
        self.vulnerability = '00'
        self.seat = '0'
        # meta information about the BML-file, supported:
        # TITLE = the name of the system
        # DESCRIPTION = a short summary of the system
        # AUTHOR = the system's author(s)
        # data in meta is only set once, and isn't overwritten
        self.meta = defaultdict(str)


class Diagram:
    """A structure for deal diagrams"""
    # each hand can be None or a tuple of four strings (s, h, d, c)
    north = None
    east = None
    south = None
    west = None
    dealer = None  # can be None or "N", "E", "S", "W"
    vul = None  # can be None or "ALL", "NO", "NS", "EW"
    board = None  # can be None or a string
    lead = None  # can be None or a string tuple ([shdc], [2-9TAKQJ])"
    contract = None  # can be None or a tuple of strings

    def __init__(self, firstrow, hands):
        for h in hands:
            hand = h[0]
            if hand == 'N':
                self.north = h[1:]
            elif hand == 'E':
                self.east = h[1:]
            elif hand == 'S':
                self.south = h[1:]
            elif hand == 'W':
                self.west = h[1:]
            else:
                assert hand in ['N', 'E', 'S', 'W'], "Hand (%s) must be N, E, S or W" % (hand)

        dealer = re.search(r'(?:\A|\s)([NESW]),?(?:\Z|\s)', firstrow)
        if dealer:
            self.dealer = dealer.group(1)

        vul = re.search(r'(?:\A|\s)(All|None|EW|NS),?(?:\Z|\s)', firstrow)
        if vul:
            self.vul = vul.group(1)

        board = re.search(r'(?:\A|\s)#?(\d+),?(?:\Z|\s)', firstrow)
        if board:
            self.board = board.group(1)

        lead = re.search(r'(?:\A|\s)([shdc])([2-9AKQJT]),?(?:\Z|\s)', firstrow)
        if lead:
            self.lead = lead.groups()

        contract = re.search(r'(?:\A|\s)(PASS),?(?:\Z|\s)', firstrow)
        if contract:
            self.contract = ('P', None, None, None)
        else:
            expr = r'(?:\A|\s)([1-7])([SHDCN])(XX?)?([NESW]),?(?:\Z|\s)'
            contract = re.search(expr, firstrow)
            if contract:
                # level, suit, (re)double, declarer
                self.contract = contract.groups()
        self.check()

    def check(self):
        assert self.north is not None, 'North hand not defined'
        assert self.east is not None, 'East hand not defined'
        assert self.south is not None, 'South hand not defined'
        assert self.west is not None, 'West hand not defined'
        assert self.dealer is None or self.dealer in ['N', 'E', 'S', 'W'], 'Dealer must be N, E, S or W'
        assert self.vul is None or self.vul in ['All', 'None', 'EW', 'NS'], 'Vulnerability must be All, None, EW or NS'
        assert self.board is None or re.match(r'\d+\Z', self.board), 'Board (%s) must match \\d+\\Z' % (self.board)
        assert self.lead is None or len(self.lead) == 2 and re.match(r'[shdc][2-9AKQJT]\Z', self.lead[0] + self.lead[1]), 'Lead (%s) must match [shdc][2-9AKQJT]\\Z' % (str(self.lead))
        assert self.contract is None or len(self.contract) == 4, 'Contract (%s) must be a list of 4 elements' % (str(self.contract))
        assert self.contract is None or re.match(r'(P|[1-7])', self.contract[0])  # level: P or 1-7
        assert self.contract is None or self.contract[0] == 'P' or re.match(r'\d[SHDCN](XX?)?[NESW]\Z', self.contract[0] + self.contract[1] + self.contract[2] + self.contract[3])


class Node:
    """
A node in a bidding table.

The indentation must be a multiple (>= 0) of the global indentation (program option).

The level indicates the node depth in the tree.

Level is 0 for root and otherwise the indentation divided by the global indentation incremented by 1.


"""
    vul = None  # Vulnerability
    seat = None
    export = None  # Export HTML or Latex? Export to BSS will take place anyway
    # Either:
    # 1) a single bid
    # 2) a history (sequence) of bids (the first line in a bidding table) separated by a dash (-)
    bid = None
    desc = None
    desc_indentation = None
    children = None  # A list of child bids
    parent = None  # The parent bid

    def __init__(self, bid, desc, indentation, parent=None, desc_indentation=-1):
        # precondition
        # checks for non root
        if parent is not None and indentation:
            if indentation % args.indentation != 0:
                raise IndentationError("Indentation (%d) must be a multiple of %d for a non root Node" % (indentation, args.indentation))
            if (indentation / args.indentation) != parent.level():
                raise IndentationError("Indentation (%d) must be the level of its parent (%d) mutiplied by the indentation argument (%d)" % (indentation, parent.level(), args.indentation))

        self.vul = '00'
        self.seat = '0'
        self.export = True
        self.bid = bid
        self.desc = desc
        self.desc_indentation = desc_indentation
        self.children = []
        self.parent = parent
        bid = re.sub(r'[-;]', '', bid)
        bid = bid.replace('NT', 'N')

        if bid != ROOT and self.level() < 1:
            raise IndentationError("Level (%d) must be at least 1 for a non root Node" % (self.level()))

        # bid sanity check
        assert self.bid_type() is not None

    def level(self):
        nr = 0
        p = self.parent
        while p:
            nr = nr + 1
            p = p.parent
        return nr

    def indentation(self):
        return (self.level() - 1) * args.indentation

    def add_child(self, bid, desc, indentation, desc_indentation):
        """appends a new child Node to the node"""
        child = Node(bid, desc, indentation, self, desc_indentation)
        child.vul = self.vul
        child.seat = self.seat
        self.children.append(child)
        if child.level() != self.level() + 1:
            raise IndentationError("Child node level (%d) must be equal to the parent node level (%d) + 1" % (child.level(), self.level()))
        return self.children[-1]

    # A bid can be either:
    # 1) a single bid
    # 2) a history (sequence) of bids (the first line in a bidding table) separated by a dash (-)
    def all_bids(self):
        return self.bid.rstrip(';-').split('-')

    def get_sequence(self):
        """List with all the parent and the current bids including generated passes in between"""

        # Get a list of nodes in the right order
        nodes = []
        p = self
        while p and p.bid != ROOT and p.bid != EMPTY:
            nodes.append(p)
            p = p.parent

        nodes.reverse()

        bids = []
        for p in nodes:
            # A bid can be either:
            # 1) a single bid
            # 2) a history (sequence) of bids (the first line in a bidding table) separated by a dash (-)
            for bid in p.all_bids():
                # When the previous bid belongs to the same party we must add a pass
                if len(bids) > 0:
                    if bid[0:1] == '(' and bids[-1][0:1] == '(':
                        bids.append('P')
                    elif bid[0:1] != '(' and bids[-1][0:1] != '(':
                        bids.append('(P)')
                bids.append(bid)
            p = p.parent

        if args.verbose > 1:
            print("get_sequence (%s): %s" % (self, bids))

        # Check whether this sequence is correct, i.e. every 2nd belongs to the same party
        we_bid = len(bids) == 0 or bids[0][0] != '('
        for b in bids[1:]:
            assert (b[0] != '(') != we_bid, 'Every 2nd bid must belong to the same party: %s' % (''.join(bids))
            we_bid = not(we_bid)

        return bids

    def set_children(self, children):
        """Used when copying from another Node"""
        self.children = copy.deepcopy(children)
        for c in self.children:
            c.parent = self
            # c.vul = self.vul
            # c.seat = self.vul

    def __getitem__(self, arg):
        return self.children[arg]

    def __str__(self):
        str = 'bid: %s; level: %d; desc: %s' % (self.bid, self.level(), self.desc)
        return str

    def bid_type(self, index=-1):
        # Matches <digit>[CDHSN], P, D and R, all possibly surrounded by ()
        dict = None
        bid = self.all_bids()[index]
        m = re.search(r'\((.+)\)\Z', bid)
        if m:
            bid = m.group(1)

        if bid in ['P', 'D', 'R'] or re.match(r'[1-7][CDHSN]\Z', bid):
            dict = {'normal': True}
        else:
            # special bids of the form <level><strain>
            # for instance 1HS, 2M, 3m, 10steps, etc
            m = re.search(r'(?P<level>\d+)(?P<strain>[a-zA-Z]+)\Z', bid)
            if m:
                strain = m.group('strain')
                assert strain in ['M', 'm', 'oM', 'om'] or strain.upper() in ['BLACK', 'RED', 'X', 'STEP', 'STEPS'] or re.match(r'[CDHSN]+\Z', strain), 'Last bid in "%s" incorrect; strain is "%s"' % (bid, strain)
                dict = {'normal': False, 'level': m.group('level'), 'strain': strain}
            else:
                assert bid in [EMPTY, ROOT], 'Last bid in "%s" must be "%s" or "%s"' % (bid, EMPTY, ROOT)
                dict = {'normal': False, 'level': None, 'strain': None}
        if args.verbose > 1:
            print("bid_type; bid: %s; dict: %s" % (self.bid, str(dict)))
        return dict


def create_bidtree(text, content):
    root = Node(ROOT, ROOT, -1)
    root.vul = content.vulnerability
    root.seat = content.seat
    lastnode = root

    # breaks when no more CUT in bidtable
    while True:
        cut = re.search(r'^(\s*)#\s*CUT\s+(\S+)\s*\n(.*)#ENDCUT[ ]*\n?',
                        text, flags=re.DOTALL | re.MULTILINE)
        if not cut:
            break
        value = cut.group(3).split('\n')
        for i in range(len(value)):
            value[i] = value[i][len(cut.group(1)):]
        value = '\n'.join(value)
        content.clipboard[cut.group(2)] = value  # group2=key
        text = text[:cut.start()] + text[cut.end():]

    # breaks when no more COPY in bidtable
    while True:
        copy = re.search(r'^(\s*)#\s*COPY\s+(\S+)\s*\n(.*)#ENDCOPY[ ]*\n?',
                         text, flags=re.DOTALL | re.MULTILINE)
        if not copy:
            break
        value = copy.group(3).split('\n')
        for i in range(len(value)):
            value[i] = value[i][len(copy.group(1)):]
        value = '\n'.join(value)
        content.clipboard[copy.group(2)] = value  # group2=key
        text = text[:copy.end(3)] + text[copy.end():]
        text = text[:copy.start()] + text[copy.start(3):]

    # breaks when no more PASTE in bidtable
    while True:
        paste = re.search(r'^(\s*)#\s*PASTE\s+(\S+)\s*(.*)\n?', text, flags=re.MULTILINE)
        if not paste:
            break
        indentation = paste.group(1)
        lines = content.clipboard[paste.group(2)]
        for r in paste.group(3).split():
            target, replacement = r.split('=')
            lines = lines.replace(target, replacement)
        lines = lines.split('\n')
        for l in range(len(lines)):
            lines[l] = indentation + lines[l]
        text = text[:paste.start()] + '\n'.join(lines) + text[paste.end():]

    hide = re.search(r'^\s*#\s*HIDE\s*\n', text, flags=re.MULTILINE)
    if hide:
        root.export = False
        text = text[:hide.start()] + text[hide.end():]

    text = re.sub(r'^\s*#\s*BIDTABLE\s*\n', '', text)

    if text.strip() == '':
        return None

    for row in text.split('\n'):
        original_row = row
        if row.strip() == '':
            continue  # could perhaps be nicer by stripping spaces resulting from copy/paste
        indentation = len(row) - len(row.lstrip())

        # If the indentation is at the same level as the last bids
        # description indentation, the description should just
        # continue but with a line break
        if indentation > 0 and indentation == lastnode.desc_indentation:
            lastnode.desc += '\\n' + row.lstrip()
            continue
        row = row.strip()
        bid = row.split(' ')[0]
        desc = ' '.join(row.split(' ')[1:]).strip()
        desc_indentation = original_row.find(desc)
        # removes equal signs at the beginning of the description
        new_desc = re.sub(r'^=\s*', '', desc)
        desc_indentation += len(desc) - len(new_desc)
        desc = new_desc
        prev_lastnode = lastnode
        while indentation < lastnode.indentation():
            lastnode = lastnode.parent
        if indentation > lastnode.indentation():
            lastnode = lastnode.add_child(bid, desc, indentation, desc_indentation)
        elif indentation == lastnode.indentation():
            lastnode = lastnode.parent.add_child(bid, desc, indentation, desc_indentation)
        # Only first line may contain a bidding history
        assert prev_lastnode == root or (bid.find('-') < 0 and bid.find(';') < 0)

    # The latex dirtree package states this:
    # --------------------------------------
    # There are two rules you must respect:
    # 1. The first node (first child of root) must have the level one.
    # 2. When you create a node, if the last node had level n, the created node
    # must have a level between 2 and n + 1.
    # --------------------------------------
    # So this means that if there is more than one child of root
    # this principle will be violated.
    # We can solve this:
    # a) If the first bid ends with a semi-colon or dash it is actually a continuation.
    #    1 - In that case the first child should not have children and
    #    2 - we will move root children 2 till the end to the children of root child 1.
    # b) Otherwise (a table of opening bids for example).
    #    1 - Now we just create a copy of root as the first child of root and
    #    2 - the original children of root will be moved to the copy
    #
    # In both cases we have to:
    # c) reparent all the children of the first non root node

    if len(root.children) > 1:
        # (a)
        intermediate = None
        if root.children[0].bid[-1] in ";-":
            intermediate = root.children[0]
            # a1
            assert len(intermediate.children) == 0, "Bid %s should not have children" % (intermediate.bid)
            intermediate.bid = intermediate.bid[0:len(intermediate.bid) - 1]
            # a2
            intermediate.children = root.children[1:]
        else:
            # b1
            intermediate = Node(EMPTY, '', 0, root)
            # b2
            intermediate.children = root.children

        root.children = [intermediate]  # one left
        # c
        for c in intermediate.children:
            c.parent = intermediate

        if args.verbose > 1:
            print("intermediate: %s" % (str(intermediate)))

        assert intermediate.parent == root
        assert len(root.children) == 1
        assert root.children[0] == intermediate
        assert intermediate.children[0].parent == intermediate
        assert intermediate.level() == 1
        assert intermediate.children[0].level() == 2

    return root


class ContentType:
    BIDTABLE = 1      # HTML, BSS
    PARAGRAPH = 2     # HTML, Latex
    H1 = 3            # HTML, Latex
    H2 = 4            # HTML, Latex
    H3 = 5            # HTML, Latex
    H4 = 6            # HTML, Latex
    LIST = 7          # HTML, Latex
    ENUM = 8          # HTML, Latex
    DIAGRAM = 9       # Latex
    TABLE = 10        # Latex
    DESCRIPTION = 11  # Latex
    BIDDING = 12      # Latex


def ContentTypeStr(self):
    switcher = {
        ContentType.BIDTABLE: "BIDTABLE",
        ContentType.PARAGRAPH: "PARAGRAPH",
        ContentType.H1: "H1",
        ContentType.H2: "H2",
        ContentType.H3: "H3",
        ContentType.H4: "H4",
        ContentType.LIST: "LIST",
        ContentType.ENUM: "ENUM",
        ContentType.DIAGRAM: "DIAGRAM",
        ContentType.TABLE: "TABLE",
        ContentType.DESCRIPTION: "DESCRIPTION",
        ContentType.BIDDING: "BIDDING"
    }
    return switcher.get(self, "nothing")


def get_content_type(text, content):
    if text.startswith('****'):
        return (ContentType.H4, text[4:].lstrip())
    if text.startswith('***'):
        return (ContentType.H3, text[3:].lstrip())
    if text.startswith('**'):
        return (ContentType.H2, text[2:].lstrip())
    if text.startswith('*'):
        return (ContentType.H1, text[1:].lstrip())

    # The first element is empty, therefore [1:]
    if(re.match(r'^\s*-', text)):
        return (ContentType.DESCRIPTION if text.find(' :: ') >= 0 else ContentType.LIST,
                re.split(r'^\s*-\s*', text, flags=re.MULTILINE)[1:])

    if(re.match(r'^\s*#VUL', text)):
        content.vulnerability = text.split()[1]
        return None

    if(re.match(r'^\s*#SEAT', text)):
        content.seat = text.split()[1]
        return None

    if(re.match(r'^\s*1\.', text)):
        return (ContentType.ENUM, re.split(r'^\s*\d*\.\s*', text, flags=re.MULTILINE)[1:])

    if(re.match(r'^\s*\(?[1-7]?[NTPDRCDHS]\)?\s+\(?[1-7]?[NTPDRCDHS]\)?\s+\(?[1-7]?[NTPDRCDHS]\)?\s+\(?[1-7]?[NTPDRCDHS]\)?\s*', text)):
        table = []
        for r in text.split('\n'):
            if r:
                table.append(r.split())
        return (ContentType.BIDDING, table)

    if(re.match(r'^\s*\(?\d[A-Za-z]+', text)):
        bidtree = create_bidtree(text, content)
        if bidtree:
            return (ContentType.BIDTABLE, bidtree)
        return None

    # Tables
    if(re.match(r'^\s*\|', text)):
        table = []
        rows = text.split('\n')
        for r in rows:
            table.append([c.strip() for c in re.findall(r'(?<=\|)[^\|]+', r)])
        return (ContentType.TABLE, table)

    # diagrams
    hands = re.findall(r"""^\s*([NESW]):?\s*
                           ([2-9AKQJTx-]+)\s+
                           ([2-9AKQJTx-]+)\s+
                           ([2-9AKQJTx-]+)\s+
                           ([2-9AKQJTx-]+)""",
                       text, flags=re.MULTILINE | re.VERBOSE)

    if hands and len(hands) + 2 >= len(text.split('\n')):
        return (ContentType.DIAGRAM, Diagram(text.split('\n')[0], hands))

    metamatch = re.match(r'^\s*#\+(\w+):\s*(.*)', text)

    if(metamatch):
        keyword = metamatch.group(1)
        if keyword in content.meta:
            return None
        value = metamatch.group(2)
        content.meta[keyword] = value
        return None

    if(re.match(r'^\s*#', text)):
        bidtree = create_bidtree(text, content)
        if bidtree:
            return (ContentType.BIDTABLE, bidtree)
        return None

    if(re.search(r'\S', text)):
        text = re.sub(r'\n +', '\n', text.strip())
        return (ContentType.PARAGRAPH, text)

    return None


@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)


def include_file(matchobj):
    filename = matchobj.group(1)
    text = ''
    with open(filename, mode='r', encoding="utf-8") as f:
        text = f.read()
    return '\n' + text + '\n'


def content_from_file(filename):
    content = None
    if filename == '-':
        content = content_from_string(sys.stdin.read())
    else:
        # move to the directory of the filename so INCLUDEs will work correctly
        with cd(os.path.dirname(os.path.abspath(filename))):
            with open(os.path.basename(os.path.abspath(filename)), mode='r', encoding="utf-8") as f:
                content = content_from_string(f.read())
    return content


def content_from_string(text):
    global args

    content = Content()

    if args.verbose > 1:
        print("# nodes: %s" % (len(content.nodes)))

    paragraphs = []
    text = re.sub(r'^\s*#\s*INCLUDE\s*(\S+)\s*\n?', include_file, text, flags=re.MULTILINE)
    text = re.sub(r'^//.*\n', '', text, flags=re.MULTILINE)
    # GJP 2018-01-07 A comment must start at the beginning of a line
    # text = re.sub(r'//.*', '', text)
    paragraphs = re.split(r'([ ]*\n){2,}', text)

    nr = 0
    for c in paragraphs:
        try:
            nr = nr + 1
            content_type = get_content_type(c, content)
            if content_type:
                content.nodes.append(content_type)
                if args.verbose > 1:
                    print("[%d] Content type: %s; # nodes: %s\n%s\n" % (nr, ContentTypeStr(content_type[0]), len(content.nodes), c))
        except Exception:
            print("\nERROR in paragraph %d:\n\n%s\n" % (nr + 1, c))
            raise
    return content


def parse_arguments(description, option_tree=True, option_include_external_files=True):
    global args

    parser = argparse.ArgumentParser(description)
    # default arguments
    parser.add_argument('-i', '--indentation', type=int, choices=range(1, 10), default=args.indentation, help='the indentation of a bidtable')
    parser.add_argument('-o', '--outputfile', help='the output file (- is stdout)')
    parser.add_argument("-v", "--verbose", action="count", default=args.verbose,
                        help="increase output verbosity")
    parser.add_argument('inputfile', help='the input file (- is stdin)')
    if option_tree:
        tree_parser = parser.add_mutually_exclusive_group(required=False)
        tree_parser.add_argument('--tree', dest='tree', action='store_true')
        tree_parser.add_argument('--no-tree', dest='tree', action='store_false')
        parser.set_defaults(tree=args.tree)  # BML 1.0

    if option_include_external_files:
        include_external_files_parser = parser.add_mutually_exclusive_group(required=False)
        include_external_files_parser.add_argument('--include-external-files', dest='include_external_files', action='store_true')
        include_external_files_parser.add_argument('--no-include-external-files', dest='include_external_files', action='store_false')
        parser.set_defaults(include_external_files=args.include_external_files)  # BML 1.0

    args = parser.parse_args()

    if args.verbose >= 1:
        print("Input file:", args.inputfile)
    if args.inputfile != '-':
        args.inputfile = os.path.realpath(args.inputfile)
        if not os.path.exists(args.inputfile):
            sys.exit('ERROR: File %s was not found!' % (args.inputfile))
    return args


if __name__ == '__main__':
    args = parse_arguments(description='Parse BML.')
    content_from_file(args.inputfile)
