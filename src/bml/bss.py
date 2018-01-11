import re
import bml
import sys
import copy

__all__ = ['bml2bss', 'VUL_DICT', 'SEAT_DICT'] # only thing to export

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
    '12':'5',
    '34':'6'
}

class Bid:
    """Numeric representation of a bid"""
    def __init__(self, stringrep):
        """Stringrep should be <denomination><kind>"""
        stringrep = stringrep[-2:] # only the last two characters
        denomination = int(stringrep[0])
        assert denomination >0 and denomination <8, 'denomination must be 1--7'
        kind = stringrep[1]
        assert kind in ['C', 'D', 'H', 'S', 'N'], 'kind must be one of CDHSN'

        self.value = self.value(kind, denomination)

    def __str__(self):
        bids = ['C', 'D', 'H', 'S', 'N']
        kind = bids[(self.value) % 5]
        denomination = str((self.value) // 5 + 1)
        return denomination + kind

    def __repr__(self):
        return str(self.value)

    def __cmp__(self, other):
        return self.value - other.value

    def __iadd__(self, other):
        self.value += other
        return self

    def __isub__(self, other):
        self.value -= other
        return self

    def __imul__(self, other):
        # raises the bid by a level. so 2C*2 == 3C, 2C*-1 == 1C
        if other > 0:
            self.value += (other-1)*5
        elif other < 0:
            self.value += other*5
        return self

    def value(self, kind, denomination):
        bids = ['C', 'D', 'H', 'S', 'N']
        val = bids.index(kind)
        return val + (denomination-1)* 5

class Sequence:
    sequence = []
    desc = ''
    vul = '0'
    seat = '0'
    contested = False
    we_open = False
    #art
    #type

    def __init__(self, node):
        self.sequence = node.get_sequence()
        self.desc = node.desc
        # if the first letter of the sequence is (, then they make the first bid
        self.we_open = self.sequence[0][0] != '('
        self.vul = VUL_DICT[node.vul]
        self.seat = SEAT_DICT[node.seat]
        self.contested = '(' in ''.join(self.sequence)

    def __str__(self):
        seq=''
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
    return child.bid_type()['normal'] == True

def systemdata_bidtable(children, systemdata):
    children_special = [x for x in children if not systemdata_normal(x)]
    children[:] = [x for x in children if systemdata_normal(x)]

    for i in children_special:
        if bml.args.verbose > 1:
            print("Special child: %s" % (i))

        bids_to_add = []

        # special bids of the form <digit><kind>
        # for instance 1HS, 2M, 3m etc
        bid = i.bid_type()
        if bid and bid['denomination']:
            denomination = bid['denomination']
            kind = bid['kind']
            if(re.match(r'[CDHS]+\Z', kind)):
                for k in kind:
                    bids_to_add.append(denomination + k)
            elif(kind == 'M'):
                bids_to_add.append(denomination + 'H')
                bids_to_add.append(denomination + 'S')
            elif(kind == 'm'):
                bids_to_add.append(denomination + 'C')
                bids_to_add.append(denomination + 'D')
            elif(kind.upper() == 'BLACK'):
                bids_to_add.append(denomination + 'C')
                bids_to_add.append(denomination + 'S')
            elif(kind.upper() == 'RED'):
                bids_to_add.append(denomination + 'D')
                bids_to_add.append(denomination + 'H')
            elif(kind.upper() == 'X'):
                bids_to_add.append(denomination + 'C')
                bids_to_add.append(denomination + 'D')
                bids_to_add.append(denomination + 'H')
                bids_to_add.append(denomination + 'S')
            elif(kind.upper() in ['STEP', 'STEPS']):
                parentbid = Bid(i.parent.all_bids()[-1])
                parentbid += int(denomination)
                bids_to_add.append(str(parentbid))
            elif (kind in ['oM', 'om']):
                # TO DO: oM and om
                raise NotImplementedError(kind)
            else:
                raise Exception("Unknown kind (%s)" % (kind))
        else:
            assert i.all_bids()[-1] == bml.EMPTY, 'Bid (%s) must be empty' % (i.bid)
            assert len(children_special) == 1
            assert len(bids_to_add) == 0
            assert len(children) == 0
            systemdata_bidtable(i.children, systemdata) # the function will stop after this call since bids_to_add and children are empty

        for add in bids_to_add:
            # We must not add such a new bid if that bid already existed as a normal bid
            if add not in [c.all_bids()[-1] for c in children]:
                h = copy.deepcopy(i)
                h.bid = add
                children.append(h)

    for r in children:
        if bml.args.verbose > 1:
            print("Normal child: %s" % (r))

        seq = Sequence(r)
        if not seq in systemdata:
            systemdata.append(seq)
        else:
            si = systemdata.index(seq)
            seq = systemdata[si]
            if not systemdata[si].desc:
                systemdata[si].desc = r.desc

        if bml.args.verbose > 1:
            print("Seq: %s" % (seq))

        systemdata_bidtable(r.children, systemdata)

def to_systemdata(content):
    systemdata = []

    for c in content.nodes:
        content_type, content = c
        if content_type == bml.ContentType.BIDTABLE:
            systemdata_bidtable(content.children, systemdata)

    return systemdata

def systemdata_to_bss(content, systemdata, f):
    f.write('*00{'+ content.meta['TITLE'] +'}=NYYYYYY' + content.meta['DESCRIPTION'] + '\n')
    for i in systemdata:
        kind = str(i)[-2:]
        if not i.we_open:
            f.write('*')
        f.write(i.seat)
        f.write(i.vul)
        f.write(str(i)+'=')
        # artificial?
        f.write('N')
        # result: clubs, diamonds, hearts, spades, NT, opponents undoubled
        f.write('YYYYYY')

        # GJP 2017-12-24 This seems to be a mandatory field
        ## if re.match(r'\d[CDHSN]', kind):
        # characteristics (signoff, control bid etc)
        f.write('0')
        if kind[0] in "1234567" and kind[1] in "CDHS":
            # least/most amount of cards in suit
            f.write('08')
        f.write(i.desc+'\n')
    return

def bml2bss(input_filename, output_filename):
    content = bml.content_from_file(input_filename)
    systemdata = to_systemdata(content)
    if output_filename == '-':
        systemdata_to_bss(content, systemdata, sys.stdout)
    else:
        with open(output_filename, mode='w', encoding="utf-8") as f:
            systemdata_to_bss(content, systemdata, f)
    return content
