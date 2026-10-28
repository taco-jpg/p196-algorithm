import sys
sys.path.insert(0, '/home/claude/research/w3_formats/code')
from symfwd import loops_of
b = 10
done = set()
for fn in sys.argv[2:]:
    for ln in open(fn):
        if ln.startswith('TARGET') and ' CLOSED ' in ln:
            f = dict(x.split('=') for x in ln.split() if '=' in x)
            done.add((f['g'], int(f['loop0']), int(f['ph'])))
for w in open(sys.argv[1]).read().split():
    p = len(w)
    for lp in loops_of(b):
        ell = len(lp)
        if p % ell: continue
        for ph in range(ell):
            if (w, lp[0], ph) in done: continue
            if ell == 1: continue   # trivial: closed at depth 0 (checked by symbwd anyway)
            print(w, lp[0], ph)
