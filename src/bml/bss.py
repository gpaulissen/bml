from typing import List

import os
import re
import sys
import copy

from bml import bml

__all__ = ['bml2bss', 'VUL_DICT', 'SEAT_DICT']

VUL_DICT = {
    # key: bml representation
    # value: bss representation
    '00': '0',
    'NN': '1',
    'YN': '2',
    'NY': '3',
    'YY': '4',
    'N0': '5',
    'Y0': '6',
    '0N': '7',
    '0Y': '8'
}

SEAT_DICT = {
    # key: bml representation
    # value: bss representation
    '0': '0',
    '1': '1',
    '2': '2',
    '3': '3',
    '4': '4',
    '12': '5',
    '34': '6'
}


class Bid:
    """Numeric representation of a bid"""
    bids = ['C', 'D', 'H', 'S', 'N']

    def __init__(self, stringrep, we=True):
        """Stringrep should be <level><strain> or (<level><strain>)"""
        if stringrep.startswith('(') and stringrep.endswith(')'):
            stringrep = stringrep[1:-1]
            self.we = False
        else:
            self.we = we
        stringrep = stringrep[-2:]  # only the last two characters
        level = int(stringrep[0])
        assert level > 0 and level < 8, 'level must be 1--7 for bid %s' % (stringrep)
        strain = stringrep[1]
        assert strain in Bid.bids, 'strain must be one of CDHSN for bid %s' % (stringrep)
        val = Bid.bids.index(strain)
        self.value = val + (level - 1) * 5

    def __str__(self):
        if self.we:
            return self.level() + self.strain()
        else:
            return '(' + self.level() + self.strain() + ')'

    def __repr__(self):
        return str(self.value)

    def __cmp__(self, other):
        return self.value - other.value

    def __le__(self, other):
        return self.value <= other.value

    def __lt__(self, other):
        return self.value < other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __gt__(self, other):
        return self.value > other.value

    def __iadd__(self, other):
        self.value += other
        return self

    def __isub__(self, other):
        self.value -= other
        return self

    def __imul__(self, other):
        # raises the bid by a level. so 2C*2 == 3C, 2C*-1 == 1C
        if other > 0:
            self.value += (other - 1) * 5
        elif other < 0:
            self.value += other * 5
        return self

    def strain(self):
        return Bid.bids[(self.value) % 5]

    def level(self):
        return str((self.value) // 5 + 1)


class Sequence:
    sequence: List[str] = []
    desc = ''
    vul = '0'
    seat = '0'
    contested = False
    we_open = False

    def __init__(self, node):
        self.sequence = node.get_sequence()
        self.desc = node.desc
        # if the first letter of the sequence is (, then they make the first bid
        self.we_open = self.sequence[0][0] != '('
        self.vul = VUL_DICT[node.vul]
        self.seat = SEAT_DICT[node.seat]
        self.contested = '(' in ''.join(self.sequence)
        assert self.contested or len(self.sequence) == 1, "There must be at least one opponent's bid: %s" % (''.join(self.sequence))

    def __str__(self):
        seq = ''
        if not self.contested:
            seq = 'P'.join(self.sequence)
        else:
            seq = ''.join(self.sequence)
        seq = seq.replace('(', '')
        return seq.replace(')', '')

    def __repr__(self):
        # do not use desc in __repr__ because we do not want to add the same sequence with another description (e.g. 1C is defined and later on 1X)
        return self.vul + self.seat + ('P' if not self.contested else '').join(self.sequence)

    def __eq__(self, other):
        return repr(self) == repr(other)

    def __ne__(self, other):
        return repr(self) != repr(other)


def systemdata_normal(child):
    return child.bid_type()['normal'] is True


def get_last_normal_bid(parent):
    # Could be:
    #
    # 1N-(P)-2red-(D)
    #   P = no 3 cards fit
    #     R = retransfer
    #     1step = to play
    #
    # So find the last 'normal' bid backwards.
    idx = len(parent.all_bids()) - 1
    while idx >= 0:
        try:
            return Bid(parent.all_bids()[idx])  # Creation succeeds: stop
        except Exception:
            idx = idx - 1
    return get_last_normal_bid(parent.parent)  # No bid was normal: continue recursively with the parent


def systemdata_bidtable(children, systemdata, vars, last_bids_by_strain, depth):
    def check_vars(var, level, strain, we):
        """Check that a new variable is not already part of the vars.values() and X < Y < Z"""
        assert var is not None, "Variable should not be None."
        assert var not in vars, "Variable %s should not already be defined." % (var)

        bid = Bid(level + strain, we)
        last_bid = max(last_bids_by_strain.values()) if len(last_bids_by_strain) > 0 else None
        info = "vars=%s; last_bids_by_strain=%s; bid=%s; last bid=%s" % (vars, last_bids_by_strain, bid, last_bid)
        result = True

        # Must we replace a variable and is there a last bid?
        # Then not every k is eligible.
        if last_bid and bid <= last_bid:  # is new bid not sufficient: ignore
            info += "; rejecting bid since it is not greater than the last bid"
            result = False
        elif strain in last_bids_by_strain:
            info += "; rejecting bid since the strain is already used"
            result = False
        # X < Y < Z
        elif var in ['X', 'Y', 'Z'] and len(vars) > 0:
            if var == 'X' and 'Y' in vars and strain >= vars['Y']:
                result = False
            elif var == 'X' and 'Z' in vars and strain >= vars['Z']:
                result = False
            elif var == 'Y' and 'X' in vars and strain <= vars['X']:
                result = False
            elif var == 'Y' and 'Z' in vars and strain >= vars['Z']:
                result = False
            elif var == 'Z' and 'X' in vars and strain <= vars['X']:
                result = False
            elif var == 'Z' and 'Y' in vars and strain <= vars['Y']:
                result = False

            if not result:
                info += "; rejecting bid since it is does not confirm to XYZ rules"

        bml.logger.debug("check_vars(var=%s, level=%s, strain=%s, we=%s) = %s (%s)" % (var, level, strain, we, result, info))

        return result

    bml.logger.debug("systemdata_bidtable(children=%s, systemdata=%s, vars=%s, last_bids_by_strain=%s, depth=%s)" % (children, systemdata, vars, last_bids_by_strain, depth))

    bids_processed = []
    bid = None
    prev_bid = None
    level = None
    strain = None

    for c in children:
        if not systemdata_normal(c):
            bml.logger.debug("Special child: %s" % (c))

            var = None  # A strain variable
            strain = None

            # special bids of the form <digit><strain>
            # for instance 1HS, 2M, 3m etc
            bid = c.bid_type()
            we = bid['we']
            if bid and bid['level']:
                level = bid['level']
                strain = bid['strain']
                if re.match(r'[CDHSN]+\Z', strain):
                    pass
                elif strain == 'M':
                    var = strain
                    strain = 'HS'
                elif strain == 'm':
                    var = strain
                    strain = 'CD'
                elif strain.upper() == 'BLACK':
                    strain = 'CS'
                elif strain.upper() == 'RED':
                    strain = 'DH'
                elif strain.upper() in ['X', 'Y', 'Z']:
                    var = strain.upper()
                    strain = 'CDHS'
                elif strain.upper() in ['STEP', 'STEPS']:
                    last_normal_bid = get_last_normal_bid(c.parent)
                    last_normal_bid += int(level)
                    m = re.match(r'(?P<level>[1-7])(?P<strain>[CDHSN])\Z', str(last_normal_bid))
                    assert m is not None, 'last normal bid: %s: %s' % (last_normal_bid)
                    level = m.group('level')
                    strain = m.group('strain')
                elif strain == 'oM':
                    assert 'M' in vars, 'When variable "oM" is used, variable "M" must already be defined'
                    var = strain
                    strain = 'S' if vars['M'] == 'H' else 'H'
                elif strain == 'om':
                    assert 'm' in vars, 'When variable "om" is used, variable "m" must already be defined'
                    var = strain
                    strain = 'D' if vars['m'] == 'C' else 'C'
                else:
                    raise Exception("Unknown strain (%s)" % (strain))

                # If the variable is already defined use that definition else add the variable (temporarily)
                add_var = False
                if var:
                    if var in vars:
                        strain = vars[var]
                    else:
                        add_var = True

                found = False
                for k in strain:
                    bid = str(Bid(level + k, we))

                    # We must not add such a new bid if that bid was already processed here before
                    if bid not in bids_processed and (not add_var or check_vars(var, level, k, we)):
                        found = True
                        if add_var:
                            vars[var] = k
                        h = copy.deepcopy(c)
                        h.bid = bid
                        if var:
                            # Replace the variable by its definition.
                            # So "1M" and "1 M" must be replaced but be aware
                            # that the first is a Python word.
                            s = r'([0-9]+)' + var + r'\b'
                            d = '\1!' + vars[var].lower()
                            h.desc = re.sub(s, d, h.desc)
                            s = r'\b' + var + r'\b'
                            d = '!' + vars[var].lower()
                            h.desc = re.sub(s, d, h.desc)

                        prev_bid = last_bids_by_strain.pop(k, None)
                        last_bids_by_strain[k] = bid

                        # Now the depth does not increase: we are just replacing a variable bid by a normal bid
                        systemdata_bidtable([h], systemdata, vars, last_bids_by_strain, depth)

                        if prev_bid:
                            last_bids_by_strain[k] = prev_bid
                        else:
                            last_bids_by_strain.pop(k, None)
                        if add_var:
                            vars.pop(var, None)  # remove variable

                        bids_processed.append(bid)

                if not found:
                    bid = c.bid_type()
                    if bid and bid['level']:
                        level = bid['level']
                        strain = bid['strain']
                        bml.logger.info('Could not find a bid (%s%s) (seq=%s; vars=%s)' % (level, strain, Sequence(c), vars))

            else:
                assert c.all_bids()[-1] == bml.EMPTY, 'Bid (%s) must be empty' % (c.bid)
                assert len(children) == 1
                systemdata_bidtable(c.children, systemdata, vars, last_bids_by_strain, depth + 1)  # the function will stop after this call since there are no other children
        else:  # systemdata_normal(c):
            bml.logger.debug("Normal child: %s" % (c))

            seq = Sequence(c)
            if seq not in systemdata:
                systemdata.append(seq)
            else:
                si = systemdata.index(seq)
                seq = systemdata[si]
                if not systemdata[si].desc:
                    systemdata[si].desc = c.desc

            bml.logger.debug("Seq: %s" % (seq))

            # Is it a normal bid (level + strain)?
            try:
                bid = Bid(c.all_bids()[-1])
                prev_bid = last_bids_by_strain.pop(bid.strain(), None)
                last_bids_by_strain[bid.strain()] = bid  # add the latest normal bid
            except Exception as e:
                bml.logger.debug('Could not determine last bid: %s' % (e))
                bid = None
                prev_bid = None
                pass

            systemdata_bidtable(c.children, systemdata, vars, last_bids_by_strain, depth + 1)
            if prev_bid:
                last_bids_by_strain[bid.strain()] = prev_bid
            elif bid:
                last_bids_by_strain.pop(bid.strain(), None)
            bids_processed.append(c.all_bids()[-1])


def to_systemdata(content):
    systemdata = []

    for c in content.nodes:
        content_type, content = c
        if content_type == bml.ContentType.BIDTABLE:
            assert content.bid == bml.ROOT, 'The first node must be root'
            assert len(content.children) == 1
            # Bidding history is the first child of root.
            #
            # The idea is to expand the bidding history so
            # systemdata_bidtable() can also define the variables in the history.
            #
            # We do this by creating new nodes after the first bid in the history.
            #
            # For example we start with:
            #
            # history.children = C
            # history.desc = D
            # history.bid = "b1-b2"
            #
            # After expanding we get:
            #
            # history.children = [node]
            # history.desc = ''
            # history.bid = "b1"
            #
            # node.bid = "b2"
            # node.desc = D
            # node.children = C

            history = content.children[0]
            bids = history.all_bids()
            if len(bids) > 1:
                indentation = bml.args.indentation
                children = history.children
                desc = history.desc
                history.children = []
                history.desc = ''
                history.bid = bids[0]
                parent = history
                for bid in bids[1:]:
                    child = parent.add_child(bid=bid, desc='', indentation=indentation, desc_indentation=-1)
                    indentation = indentation + bml.args.indentation
                    assert child.parent == parent
                    assert len(child.children) == 0
                    parent = child
                else:  # at the end of the loop
                    parent.set_children(children)
                    parent.desc = desc
            systemdata_bidtable(content.children, systemdata, {}, {}, 1)

    return systemdata


def systemdata_to_bss(content, systemdata, f):
    f.write('*00{' + content.meta['TITLE'] + '}=NYYYYYY' + content.meta['DESCRIPTION'] + '\n')
    for i in systemdata:
        bid = str(i)[-2:]
        if not i.we_open:
            f.write('*')
        f.write(i.seat)
        f.write(i.vul)
        f.write(str(i) + '=')
        # artificial?
        f.write('N')
        # result: clubs, diamonds, hearts, spades, NT, opponents undoubled
        f.write('YYYYYY')

        # GJP 2017-12-24 This seems to be a mandatory field
        # # if re.match(r'\d[CDHSN]', bid):
        # characteristics (signoff, control bid etc)
        f.write('0')
        if bid[0] in "1234567" and bid[1] in "CDHS":
            # least/most amount of cards in suit
            f.write('08')
        f.write(i.desc + '\n')
    return


def bml2bss(input_filename, output_filename):
    content = bml.content_from_file(input_filename)
    systemdata = to_systemdata(content)
    if output_filename == '-':
        systemdata_to_bss(content, systemdata, sys.stdout)
    else:
        if os.path.isdir(output_filename):
            output_filename = os.path.join(output_filename, os.path.basename(re.sub(r'\..+\Z', '.bss', input_filename)))
        with open(output_filename, mode='w', encoding="utf-8") as f:
            systemdata_to_bss(content, systemdata, f)
    return content
