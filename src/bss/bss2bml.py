from typing import Dict, Any

import re

import bml.bss

SEAT_DICT = {v: k for k, v in bml.bss.SEAT_DICT.items()}
VUL_DICT = {v: k for k, v in bml.bss.VUL_DICT.items()}

# key: parent prefix from a BSS bidding sequence
# data: the parent (type bml.Node)
#
# An example:
# if we scan this sequence
#
#   001C=NYYYYYY0082+!c, NAT or BAL, 11+ HCP (11+ if BAL)
#
# the parent key is "00" (parents.bid is empty) and we will add the node 1C to the parent children array
#
parents: Dict[str, Any] = {}

state = ['header', 'stock convention card', 'bidding sequence', 'include', 'defensive carding']
state_nr = 0  # state to parse
file_type = None
system_name = None
summary = None


def bss2bml(input, output):
    """
Convention Card Definition and Convention Definition files are ASCII text files having a “.bss” file name extension. As might be surmised from the use of a specific file name extension, the files have a well defined format, including encoding of information. In a defined context, a specific character will be an encoding of something, for example, a single character will represent position at the table (including one character to indicate 1st or 2nd position, etc.).

The file consists of a series of “records”. A record is a line of the text file — it is terminated by a “new line” character. The overall format of the file is:

A single header record
Zero or one stock convention card records
Zero or more bidding sequence records
Zero or more include records
Zero or one defensive carding records
    """

    global state, state_nr

    state_nr = 0
    for line in input:
        while state_nr < len(state) and not parse_line(line):
            state_nr = state_nr + 1

    print_bml(output)


def parse_line(line):
    global state_nr, file_type, system_name, summary

    if bml.args.verbose > 1:
        print("state_nr: %s; line: %s" % (state_nr, line))

    stock_convention_card_file_name = None
    convention_file_name = []
    leads_vs_nt = None
    leads_vs_suits = None
    defensive_signals = None
    description_and_other_agreements = None
    opener = None
    party = None
    THEY = 0
    WE = 1
    position = None
    vulnerability = None
    bidding_sequence = None
    # artificial = None
    # possible_outcomes = None
    # disposition = None
    # suit_length = None
    description = None

    result = False

    if state[state_nr] == 'header':
        """
Header Record

Format
*00 [{<System Name>}] = NYYYYYY [<Summary>]
?00 [{<System Name>}] = NYYYYYY [<Summary>]

Description
The first record in the file is a Header record. The “00” and the “= NYYYYYY” are ignored (though they must be present).

File Type
The first character in the record is either an “*” or a “?”. An “*” indicates a standard Convention Card Definition or Convention Definition file; a “?” identifies a Floating Convention Definition file. Currently the only stock Floating convention is “Roman Key Card Blackwood (1430)”.

Although the Full Disclosure editor can be used to open any Convention Definition file, editing Floating conventions is not currently supported (nothing will be visible in the editor except the name and description).

System Name
System Name is the name entered in the Define dialog when editing the convention card file.

Summary
Summary is the system summary entered in the Define dialog when editing the convention card file.
        """

        m = re.match(r"(?P<file_type>.)00(?P<system_name>\{[^\}]+\})=NYYYYYY(?P<summary>.*$)", line)
        assert m, "line (%s) does not match header record" % (line)
        file_type = m.group('file_type')
        system_name = m.group('system_name')
        summary = m.group('summary')
        if bml.args.verbose > 1:
            print("file_type: %s; system_name: %s; summary: %s" % (file_type, system_name, summary))
        state_nr = state_nr + 1  # only one header
        result = True
    elif state[state_nr] == 'stock convention card':
        """
Stock Convention Card Record

Format
$ <File Name>

Description
When you edit one of the stock convention cards online, change it, and save it under a new name, then rather than storing a complete copy of the Convention Card Definition file, a reference to the stock card is put into your new file.

There can only be one Convention Card Record in a Convention Card Definition file. If there is one, it appears immediately after the Header record.

File Name is the name of the stock Convention Card Definition file. These files are stored in the “convcards\\default convcards” subdirectory of the “Bridge Base Online” directory.

        """
        m = re.match(r"\$(?P<stock_convention_card_file_name>.*$)", line)
        if m:
            stock_convention_card_file_name = m.group('stock_convention_card_file_name')
            if bml.args.verbose > 1:
                print("stock_convention_card_file_name: %s" % (stock_convention_card_file_name))
            state_nr = state_nr + 1  # there is only one
            result = True
    elif state[state_nr] == 'include':
        """
Convention Record

Format
+ <File Name>

Description
When you use Manage Conventions in the Full Disclosure editor, it creates (or removes) Convention records. These are simply pointers to the appropriate Convention Definition files.

Multiple Convention Records are allowed, however they cannot be nested (the Convention Definition file cannot contain further Convention Records).

File Name is the name of the Convention Definition file. These files are stored in the “conventions” subdirectory of the “Bridge Base Online” directory.
        """

        m = re.match(r"\+(?P<convention_file_name>.*$)", line)
        if m:
            convention_file_name.append(m.group('convention_file_name'))
            if bml.args.verbose > 1:
                print("convention_file_name: %s" % (m.group('convention_file_name')))
            # there may be another convention file so do not increment state_nr
            result = True
    elif state[state_nr] == 'defensive carding':
        """
Defensive Carding Record

Comment
There should never be a need to edit or generate this record other than by using the Full Disclosure editor.

Format
% <Leads vs NT> <Leads vs Suits> <Defensive Signals> [<Description and Other agreements>]

Description
This record represents your carding agreements and, if there is one, is the last record in the file.

Leads vs NT
There are 22 characters in this string, each representing one of the card combinations listed in the Leads vs NT section of the Full Disclosure editor’s Opening Leads section.

The choices you can make in the editor do not always include every card in the combination; for example, you cannot choose to lead the Queen from Qxx. Of the available choices, “B” indicates the top card, “C” the next lower card, and so on.

Here is the full list of 22 card combinations:

xx, xxx, xxxx, xxxxx, Qxx, Qxxx, Qxxxx, Qxxxxx, Qxxxxxx, AKx, KQJ, QJ10, J109, 1098, KQ109, AKJ10, AQJ, AJ10, A109, KJ10, K109, Q109

Leads vs Suits
There are 18 characters in this string, each representing one of the card combinations listed in the Leads vs Suits section of the Full Disclosure editor’s Opening Leads section.

The encoding is exactly the same as described above.

Here is the full list of 18 card combinations:

xx, xxx, xxxx, xxxxx, Qxx, Qxxx, Qxxxx, Qxxxxx, Qxxxxxx, AK, AKx, KQJ, QJ10, J109, 1098, KJ10, K109, Q109

Defensive Signals
In the Full Disclosure editor section on Defensive Signals, there are three sections for signals against notrump contract and three for suit contracts. Each of those has an agreement for first, second, and third priority.

Thus the following six sections each have a first, second, and third priority for a total of 18 characters in the Defensive Carding record:

Partner leads vs NT
Declarer leads vs NT
Discards vs NT
Partner leads vs suit
Declarer leads vs suit
Discards vs suit
The choice of agreements listed in the Full Disclosure editor is the same for each of the 18 situations. The encoding is:

A — No agreement
B — Attitude (Hi=Enc.)
C — Attitude (Hi=Disc.)
D — Attitude (Odd=Enc.)
E — Attitude (Odd=Disc.)
F — Count (Hi=Even)
G — Count (Hi=Odd)
H — Count (Odd/Even)
I — Suit Preference (Hi-Hi)
J — Suit Preference (Hi-Low)
K — Other
        """

        m = re.match(r"%(?P<leads_vs_nt>.{22})(?P<leads_vs_suits>.{18})(?P<defensive_signals>[A-K]{18})(?P<description_and_other_agreements>.*)$", line)
        if m:
            leads_vs_nt = m.group('leads_vs_nt')
            leads_vs_suits = m.group('leads_vs_suits')
            defensive_signals = m.group('defensive_signals')
            description_and_other_agreements = m.group('description_and_other_agreements')
            if bml.args.verbose > 1:
                print("leads_vs_nt: %s; leads_vs_suits: %s; defensive_signals: %s; description_and_other_agreements: %s" %
                      (leads_vs_nt, leads_vs_suits, defensive_signals, description_and_other_agreements))
            state_nr = state_nr + 1  # there is only one
            result = True

    elif state[state_nr] == 'bidding sequence':
        """
Bidding Sequence

Format
  AB <Bidding Sequence> = CDEFGHI J [KL] [<Description>]
* AB <Bidding Sequence> = CDEFGHI J [KL] [<Description>]

Records that start with an asterisk represent competitive sequences where They open; those without the asterisk represent sequences where We open.

The capital letters, except in the name of character strings, represent encodings — each is a single character representing some information.

Position
“A” represents the position in which the opening bid is made. Implicitly this defines the Dealer, which is the label used in the Full Disclosure editor when defining the bid.

The encoding is:

0 — Any position
1 — 1st position
2 — 2nd position
3 — 3rd position
4 — 4th position
5 — 1st or 2nd position
6 — 3rd or 4th position.
Vulnerability
“B” represents the prevailing vulnerability conditions which apply to the bidding sequence.

In the following list of encodings, the labels used in the Full Disclosure editor are included in parentheses.

0 — Any conditions (Any)
1 — Nobody vulnerable (None vul)
2 — We are vulnerable; they are not (Only we vul)
3 — We are not vulnerable; they are (Only they vul)
4 — Both sides are vulnerable (Both vul)
5 — We are not vulnerable; they may or may not be (We not vul)
6 — We are vulnerable; they may or may not be (We vul)
7 — We may or may not be vulnerable; they are not (They not vul)
8 — We may or may not be vulnerable; they are (They vul)
Bidding Sequence
The Bidding Sequence starts immediately after the first two characters and is terminated by the equals sign (“=”). The calls in the sequence are either “P” for Pass, “D” for Double, “R” for Redouble, or a bid. A bid consists of a single digit (“1” to “7”) followed by the initial letter of the strain (“S”, “H”, “D”, “C”, or “N” for notrump).

Note: If a Qualification is entered for an opponent’s bid, then that qualification will appear as a string within braces (curly brackets). It will appear after the bid that was qualified and after the intervention. The qualified bid does not have to be the first one in the sequence; for example, you might play one agreement over an opponent’s transfer bid, but another if their suit responses to 1NT are natural.

Artificial Bid
“C” is used to indicate whether the last bid in the sequence is artificial (“Y”) or not (“N”).

Possible Outcomes
The next six characters (“D” through “I”) represent the six possible outcomes. If the outcome is possible, it is a “Y”; otherwise an “N”. The outcomes (possible strains that are still open after the last bid in the sequence) are, in order:

D — Clubs
E — Diamonds
F — Hearts
G — Spades
H — Notrump
I — Defend undoubled
Disposition
“J” encodes the Disposition of the last bid in the sequence as defined in Full Disclosure.

The encoding is:

0 — no agreement
1 — Signoff
2 — Non-forcing
3 — Constructive
4 — Invitational
5 — Forcing
6 — Forcing to game
7 — Slam try
8 — Control bid
9 — Preemptive
A — Transfer
B — Puppet
C — Relay
D — Asking bid
E — Asking bid response
Suit Length
The minimum and maximum promised suit length that apply to the last bid in the bidding sequence are defined by “K” and “L” respectively.

If the last bid is a notrump bid, then “K” and “L” are omitted.

The digits “0” to “8” are used to represent the actual length for the minimum length (“K”).

In the case of the maximum length (“L”), the digits “0” to “7” are used to represent the actual length, and “8” to represent “Any”.

Description
The Description string is whatever you entered under Description when you defined the last bid in the bidding sequence.

        """
        m = re.match(r"(?P<opener>\*)?(?P<position>[0-6])(?P<vulnerability>[0-8])(?P<bidding_sequence>[^=]+)=(?P<artificial>[YN])(?P<possible_outcomes>[YN]{6})(?P<disposition>[0-9A-E])(?P<description>.*)$", line)
        if m:
            opener = m.group('opener')
            if not opener:
                opener = ''
            party = THEY if m.group('opener') else WE
            position = m.group('position')
            vulnerability = m.group('vulnerability')
            bidding_sequence = m.group('bidding_sequence')
            description = m.group('description')

            if bml.args.verbose > 1:
                print("party: %s; bidding_sequence: %s; description: %s" % (party, bidding_sequence, description))
            m = re.search(r"(?P<bid>(P|D|R|[1-7][CDHSN]))$", bidding_sequence)
            assert m, 'Bidding sequence (%s) must end with a bid' % (bidding_sequence)
            if m:
                bid = m.group('bid')
                if len(bid) == 2 and bid[0] in "1234567" and bid[1] in "CDHS":
                    # suit_length = description[0:2]
                    description = description[2:]
                # else:
                #    suit_length = ''

                parent_bidding_sequence = opener + position + vulnerability + bidding_sequence[0:(len(bidding_sequence) - len(bid))]
                if bml.args.verbose > 1:
                    print("parent bidding sequence: %s; found: %s; last bid: %s" % (parent_bidding_sequence, str(parent_bidding_sequence in parents), bid))
                if parent_bidding_sequence in parents:
                    parent = parents[parent_bidding_sequence]
                else:
                    # first is ROOT, second is EMPTY
                    parent = bml.Node(bid=bml.ROOT, desc=bml.ROOT, indentation=None, parent=None, desc_indentation=None)
                    parent = parent.add_child(bid=bml.EMPTY, desc='', indentation=None, desc_indentation=None)
                    parents[parent_bidding_sequence] = parent
                child = parent.add_child(bid=bid, desc=description, indentation=None, desc_indentation=None)
                if bml.args.verbose > 1:
                    print("# childs for %s: %s" % (parent_bidding_sequence, len(parents[parent_bidding_sequence].children)))
                if bml.args.verbose > 1:
                    print("parent: %s; child: %s" % (parent, child))
                parents[parent_bidding_sequence + bid] = child
                # there may be more than one bidding sequence so do not increase state_nr
                result = True

    return result


def print_bml(output):
    global system_name, summary

    output.write("#+TITLE: %s\n\n#+DESCRIPTION: %s\n" % (system_name, summary))
    for opener in ['', '*']:
        for seat in SEAT_DICT.keys():
            for vul in VUL_DICT.keys():
                parent_bidding_sequence = opener + seat + vul
                if parent_bidding_sequence in parents:
                    if bml.args.verbose > 1:
                        print("# childs for %s: %s" % (parent_bidding_sequence, len(parents[parent_bidding_sequence].children)))
                    print_bidtable(output, parents[parent_bidding_sequence], opener, seat, vul)


def print_bidtable(output, parent, opener=None, seat=None, vul=None):
    if vul:
        output.write("\n#VUL %s\n\n" % (VUL_DICT[vul]))
    if seat:
        output.write("#SEAT %s\n\n" % (SEAT_DICT[seat]))

    for c in parent.children:
        output.write("%s%s%s%s\n" % (" " * c.level(), c.bid, ' = ' if c.desc else '', c.desc))
        print_bidtable(output, c)
