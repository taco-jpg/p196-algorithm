import sys
sys.path.insert(0,'/home/claude/research/w3_formats/code')
import kink_sat
from kink_sat import *
def dump(fn, ri, out, base):
    kink_sat.b = base
    L = kink_sat.lattice_data(parse(fn)[ri])
    with open(out, 'w') as f:
        f.write(f"{L['p']} {L['nB']} {L['m']} {base}\n" + ' '.join(map(str, L['gam'])) + '\n')
        for t in range(L['p']): f.write(' '.join(map(str, L['Wt'][t])) + '\n')
        for t in range(L['p']): f.write(' '.join(map(str, L['cup'][t])) + '\n')
    return L
if __name__ == '__main__':
    fn, ri, out, base = sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4])
    L = dump(fn, ri, out, base)
    print('p', L['p'], '|B|', L['nB'], 'm', L['m'], 'gam', ''.join(map(str, L['gam'])), 'S', sum(L['gam']))
