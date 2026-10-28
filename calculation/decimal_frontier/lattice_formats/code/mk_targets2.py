import sys
sys.path.insert(0, '/home/claude/research/w3_formats/code')
from symfwd import loops_of
b = 10
done = set()
for fn in sys.argv[2:]:
    for ln in open(fn):
        if ln.startswith('TARGET') and (' CLOSED ' in ln):
            f = dict(x.split('=') for x in ln.split() if '=' in x)
            done.add((f['g'], int(f['loop0']), int(f['ph'])))
def partner(lp, ph, ell):
    # CS maps u -> 18-u : doubling loop phase ph -> ph+3 ; {6,12}: ph -> ph+1
    return (ph + ell // 2) % ell
for w in open(sys.argv[1]).read().split():
    p = len(w)
    for lp in loops_of(b):
        ell = len(lp)
        if p % ell or ell == 1: continue
        for ph in range(ell // 2):
            q = partner(lp, ph, ell)
            if (w, lp[0], ph) in done and (w, lp[0], q) in done: continue
            print(w, lp[0], ph)
