from copy import deepcopy
from pprint import pprint
import re

seq_entry = {'instruction':None,
             'quantity':None,
             'lstgen':None,
             'start':None,
             'stop':None,
             'n':None,
             'rate':None,
             'label':None,
             'indent':None}

def read_seq_file(seq):
    with open(seq) as f:
        return f.readlines()

def translate_lst2lin(steplist):
    pass

def prepare_steplist(raw_steplist):
    """
    Prepares the sequence file to be read by the database.
    Does not read comment lines (#) or blank lines.
    Will check for basic consistency of the file (i.e. all values are given)

    Parameters
    ----------
    raw_steplist: list of sequence lines, read by `read_seq_file`

    Returns
    -------
    list
        List of strings,

    Raises
    ------
    ValueError if there is a problem with reading the list. #todo make better checks
    """
    steplist = []

    #remove \n, comments and empty lines
    steplist_stripped = [(i+1, v.rstrip()) for i, v in enumerate(raw_steplist) if v.strip() != '' if not v.startswith('#') ]

    reOptFloat = r'([+-]?[0-9]*\.?[0-9]*?[eE]?[+-]?[0-9]+?)'

    try:
        for n, (i, line) in enumerate(steplist_stripped):

            line = line.rstrip()
            remove_indent = re.split(r'\s{4}|\t{1}?', line)
            indents = remove_indent.count('')
            rest = remove_indent[-1]

            try:
                valrange = re.split('[\[\]]', rest)[1]
                valrange = re.findall(reOptFloat, valrange)
            except IndexError:
                valrange = None


            instruction, quantity = re.findall(r'(\w+)\b', rest)[:2]
            lstgen = re.findall(r'\s(\w+)\[', rest)
            rate = re.search(r'\@('+reOptFloat+')', rest)
            if rate:
                rate = rate.group()
            label = re.search(r'\#[\w\s]+', rest)

            if label:
                label = label.group()

            steplist.append([n, instruction, quantity, lstgen, valrange, rate, label, indents])

    except ValueError:
        raise ValueError('Error found in line %i\n\t [%i] >>> %s \nplease check the file'%(i, i, line))
    return steplist

def convert_steplist(steplist):
    """

    Parameters
    ----------
    steplist

    Returns
    -------

    """
    return steplist

def import_seq(seq_file):
    raw_steplist = read_seq_file(seq_file)
    steplist = prepare_steplist(raw_steplist)

    steplist = convert_steplist(steplist)

if __name__ == '__main__':

    d =  import_seq('/Users/mike/Documents/GitHub/RockPy_database/testing/hysteresis.seq')
    # for k in d:
    #     print(k, d[k])
    pprint(d)