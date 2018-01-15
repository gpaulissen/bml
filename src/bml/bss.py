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
        """Stringrep should be <level><strain>"""
        stringrep = stringrep[-2:] # only the last two characters
        level = int(stringrep[0])
        assert level >0 and level <8, 'level must be 1--7'
        strain = stringrep[1]
        assert strain in ['C', 'D', 'H', 'S', 'N'], 'strain must be one of CDHSN'

        self.value = self.value(level, strain)

    def __str__(self):
        bids = ['C', 'D', 'H', 'S', 'N']
        strain = bids[(self.value) % 5]
        level = str((self.value) // 5 + 1)
        return level + strain

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

    def value(self, level, strain):
        bids = ['C', 'D', 'H', 'S', 'N']
        val = bids.index(strain)
        return val + (level-1)* 5

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

def systemdata_bidtable(children, systemdata, vars={}):
    bids_processed = []

    for c in children:
        if not systemdata_normal(c):
            if bml.args.verbose > 1:
                print("Special child: %s" % (c))

            var = None # A strain variable 
            strain = None

            # special bids of the form <digit><strain>
            # for instance 1HS, 2M, 3m etc
            bid = c.bid_type()
            if bid and bid['level']:
                level = bid['level']
                strain = bid['strain']
                if re.match(r'[CDHS]+\Z', strain):
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
                elif strain.upper() == 'X':
                    var = 'X'
                    strain = 'CDHS'
                elif strain.upper() in ['STEP', 'STEPS']:
                    parentbid = Bid(c.parent.all_bids()[-1])
                    parentbid += int(level)
                    m = re.match('(?P<level>[1-7])(?P<strain>[CDHSN])\Z', str(parentbid))
                    assert m != None
                    level = m.group['level']
                    strain = m.group['strain']
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

                for k in strain:
                    bid = level + k
                    
                    # We must not add such a new bid if that bid was already processed here before
                    if bid not in bids_processed:
                        if add_var:
                            vars[var] = k
                        h = copy.deepcopy(c)
                        h.bid = bid
                        systemdata_bidtable([h], systemdata, vars)
                        if add_var:
                            vars.pop(var, None) # remove M
                        bids_processed.append(bid)
            else:
                assert c.all_bids()[-1] == bml.EMPTY, 'Bid (%s) must be empty' % (c.bid)
                assert len(children) == 1
                systemdata_bidtable(c.children, systemdata, vars) # the function will stop after this call since there are no other children
        else: # systemdata_normal(c):
            if bml.args.verbose > 1:
                print("Normal child: %s" % (c))

            seq = Sequence(c)
            if not seq in systemdata:
                systemdata.append(seq)
            else:
                si = systemdata.index(seq)
                seq = systemdata[si]
                if not systemdata[si].desc:
                    systemdata[si].desc = c.desc

            if bml.args.verbose > 1:
                print("Seq: %s" % (seq))

            systemdata_bidtable(c.children, systemdata, vars)
            bids_processed.append(c.all_bids()[-1])
        
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
        bid = str(i)[-2:]
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
        ## if re.match(r'\d[CDHSN]', bid):
        # characteristics (signoff, control bid etc)
        f.write('0')
        if bid[0] in "1234567" and bid[1] in "CDHS":
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
