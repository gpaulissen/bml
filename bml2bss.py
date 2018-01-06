import re
import bml
import sys

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

    def __init__(self, sequence, desc=''):
        self.sequence = sequence
        self.desc = desc
        # if the first letter of the sequence is (, then they make the first bid
        self.we_open = sequence[0][0] != '('
    def __str__(self):
        seq=''
        if not self.contested:
            seq = 'P'.join(self.sequence)
        else:
            seq = ''.join(self.sequence)
        seq = seq.replace('(', '')
        return seq.replace(')', '')

    def __repr__(self):
        if not self.contested:
            return self.vul + self.seat + 'P'.join(self.sequence)
        return self.vul + self.seat + ''.join(self.sequence)

    def __eq__(self, other):
        return repr(self) == repr(other)

    def __ne__(self, other):
        return repr(self) != repr(other)

## in module bml the bidding history is solved in a different way    
## rootsequence = ''
systemdata = []

def systemdata_normal(child):
    # Matches <digit>[CDHSN], P, D and R, all possibly surrounded by ()
    return re.match(r'^((\(?\d[CDHSN]\)?)|(\(?P\)?)|(\(?D\)?)|(\(?R\)?))+\Z', child.bidrepr)

def systemdata_bidtable(children):
    ## global rootsequence
    children_special = [x for x in children if not systemdata_normal(x)]
    children[:] = [x for x in children if systemdata_normal(x)]
    
    for i in children_special:
        if bml.args.verbose > 1:
            print("Special child: %s" % (i))

        bids_to_add = []

        # special bids of the form <digit><kind>
        # for instance 1HS, 2M, 3m etc
        bid = re.search(r'(\d+)(\w+)', i.bidrepr)
        if bid:
            denomination = bid.group(1)
            kind = bid.group(2)
            if(re.match(r'[CDHS]+\Z', kind)):
                for k in kind:
                    bids_to_add.append(denomination + k)
            elif(kind == 'M'):
                bids_to_add.append(denomination + 'H')
                bids_to_add.append(denomination + 'S')
            elif(kind == 'm'):
                bids_to_add.append(denomination + 'C')
                bids_to_add.append(denomination + 'D')
            elif(kind.upper() == 'RED'):
                bids_to_add.append(denomination + 'D')
                bids_to_add.append(denomination + 'H')
            elif(kind.upper() == 'X'):
                bids_to_add.append(denomination + 'C')
                bids_to_add.append(denomination + 'D')
                bids_to_add.append(denomination + 'H')
                bids_to_add.append(denomination + 'S')
            elif(kind.upper() in ['STEP', 'STEPS']):
                parentbid = Bid(i.parent.bidrepr[-2:])
                parentbid += int(denomination)
                bids_to_add.append(str(parentbid))
        else:
            assert i.bidrepr == bml.EMPTY, 'Bid (%s) must be empty' % (i.bidrepr)
            assert len(children_special) == 1
            assert len(bids_to_add) == 0
            assert len(children) == 0
            systemdata_bidtable(i.children) # the function will stop after this call since bids_to_add and children are empty
                
        for add in bids_to_add:
            h = bml.Node(add, i.desc, i.indentation(), i.parent)
            h.vul = i.vul
            h.seat = i.seat
            h.set_children(i.children)
            children.append(h)

    for r in children:
        if bml.args.verbose > 1:
            print("Normal child: %s" % (r))

        bid = re.sub(r'[-;]', '', r.bid)
        sequence = r.get_sequence()
        ##if len(bid) < len(r.bid):
        ##    rootsequence = ''
        ##if bml.args.verbose > 1:
        ##    print("Sequence: %s; root sequence: %s" % (sequence, rootsequence))
        ##if rootsequence:
        ##    sequence.reverse()
        ##    sequence.append(rootsequence)
        ##    sequence.reverse()
        contested = '(' in ''.join(sequence)
        seq = Sequence(sequence, r.desc)
        seq.vul = VUL_DICT[r.vul]
        seq.seat = SEAT_DICT[r.seat]
        seq.contested = contested
        if not seq in systemdata:
            systemdata.append(seq)
        else:
            si = systemdata.index(seq)
            seq = systemdata[si]
            if not systemdata[si].desc:
                systemdata[si].desc = r.desc                

        if bml.args.verbose > 1:
            print("Sequence: %s; desc: %s" % (seq, seq.desc))
                
        ##if len(bid) < len(r.bid):
        ##    rootsequence = r.bidrepr

        ## assert rootsequence == '', 'Root sequence (%s) should be empty; bid (%s); bidrepr (%s)' % (rootsequence, bid, r.bid)
                
        systemdata_bidtable(r.children)

def to_systemdata(contents):
    ## global rootsequence
    for c in contents:
        ## rootsequence = ''
        contested = False # unused?
        content_type, content = c
        if content_type == bml.ContentType.BIDTABLE:
            systemdata_bidtable(content.children)

def systemdata_to_bss(f):
    global systemdata

    f.write('*00{'+ bml.meta['TITLE'] +'}=NYYYYYY' + bml.meta['DESCRIPTION'] + '\n')
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

if __name__ == '__main__':
    bml.args = bml.parse_arguments(description='Convert BML to BSS.', option_tree=False, option_include_external_files=False)
    bml.content_from_file(bml.args.inputfile)
    if not bml.args.outputfile:
        bml.args.outputfile = '-' if bml.args.inputfile == '-' else bml.args.inputfile.split('.')[0] + '.bss'
    if bml.args.verbose >= 1:
        print("Output file:", bml.args.outputfile)
    to_systemdata(bml.content)
    if bml.args.outputfile == '-':
        systemdata_to_bss(sys.stdout)
    else:
        with open(bml.args.outputfile, 'w') as f:
            systemdata_to_bss(f)

