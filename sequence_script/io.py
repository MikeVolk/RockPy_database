from copy import deepcopy
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

def prepare_seq_list(seq):

    steps = {}
    #remove \n
    seq = [i.rstrip() for i in seq]

    for i, line in enumerate(seq):

        steps[i] = deepcopy(seq_entry)


        # print(i, line)
        # split for 4 spaces
        if line.startswith('    '):
            indent = line.split('    ')
        elif line.startswith('\t'):
            indent = line.split('\t')
        else:
            indent = [line]

        steps[i]['indent'] = len(indent)-1

        #removed indentation (4 spaces)
        line = indent[steps[i]['indent']]
        instruction = line.split(' ')[0]
        steps[i]['instruction'] = instruction

        quantity = line.split(' ')[1]
        steps[i]['quantity'] = quantity
        # rest = line.split(' ')[2:]

        if instruction == 'measure':
            continue

        lstgen = line.split(' ')[2].split('[')[0]
        steps[i]['lstgen'] = lstgen

        start, stop, n = line.split('[')[1].split(']')[0].split(',')
        steps[i]['start'] = float(start)
        steps[i]['stop'] = float(stop)
        steps[i]['n'] = int(n)

        # get rate of change and label
        if len(line.split(']'))>1:
            if line.split(']')[1]:
                rate = line.split(']')[1]
                rate[i]['stop'] = float(rate)

            if '#' in line:
                label = line.split('#')[1]

    return steps

if __name__ == '__main__':
    file = read_seq_file('/Users/mike/Documents/GitHub/RockPy_database/testing/hysteresis.seq')
    for k in prepare_seq_list(file):
        print(k, prepare_seq_list(file)[k])