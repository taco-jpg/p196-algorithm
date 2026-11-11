#!/usr/bin/env python3
"""r12d final_tables.py -- markdown tables of every result log (for FINAL.md)."""
import os, re, glob, collections
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def res_lines(f):
    return [l.strip() for l in open(f, errors='replace') if l.startswith('RESULT')]

# ---- fixed centres: SAT (logs/prod, tsrun ret) + enumeration (logs/cen, cen3)
sat = collections.defaultdict(dict)
for f in glob.glob('logs/prod/ret_*.log'):
    m = re.match(r'logs/prod/ret_(rec\d)_K(\d+)_L(\d+)(r?)\.log', f)
    if not m: continue
    lat, K, L = m.group(1), int(m.group(2)), int(m.group(3))
    for l in res_lines(f):
        st = 'UNSAT' if 'RESULT UNSAT' in l else 'SAT'
        t = float(re.search(r' ([\d.]+)s', l).group(1))
        sat[(lat, K)][L] = (st, t)
for f in glob.glob('logs/test/cubes2_*.log') + glob.glob('logs/prod/cubes2_*.log'):
    for l in res_lines(f):
        m = re.search(r'lat=(rec\d) q0=\d+ K=(\d+) L=(\d+) first=\[(\d+),(\d+)\)', l)
        if m and m.group(4) == '0' and m.group(5) == '19':
            st = 'UNSAT' if 'RESULT UNSAT' in l else 'SAT'
            t = float(re.search(r'total=([\d.]+)s', l).group(1))
            sat[(m.group(1), int(m.group(2)))].setdefault(int(m.group(3)), (st, t))
enum = collections.defaultdict(dict)
for f in glob.glob('logs/cen/cen_*.log'):
    m = re.match(r'logs/cen/cen_(rec\d)_K(\d+)_L(\d+)b?\.log', f)
    for l in res_lines(f):
        c = int(re.search(r'centres=(\d+)', l).group(1)); r = int(re.search(r'returns=(\d+)', l).group(1))
        mp = int(re.search(r'maxprefix=(\d+)', l).group(1)); tl = int(re.search(r'targetlen=(\d+)', l).group(1))
        dev = sum(int(re.search(k + r'=(\d+)', l).group(1)) for k in ('clockdev', 'lenerr', 'guardfail'))
        enum[(m.group(1), int(m.group(2)))][int(m.group(3))] = (c, r, mp, tl, dev)

def ranges(Ls):
    Ls = sorted(Ls); out = []; s = p = None
    for x in Ls:
        if s is None: s = p = x
        elif x == p + 1: p = x
        else: out.append((s, p)); s = p = x
    if s is not None: out.append((s, p))
    return ', '.join(f'{a}' if a == b else f'{a}..{b}' for a, b in out)

print('### Fixed centres, SAT (tsat exact encoding, CaDiCaL 1.9.5)\n')
print('| exterior | K (period) | q0 | |C| UNSAT | |C| SAT | times (s) |')
print('|---|---|---|---|---|---|')
q0 = {('rec0', 1): 5, ('rec1', 1): 5, ('rec0', 2): 8, ('rec1', 2): 8, ('rec0', 3): 11, ('rec1', 3): 11,
      ('rec0', 4): 15, ('rec1', 4): 15, ('rec0', 5): 18, ('rec1', 5): 18, ('rec0', 6): 21, ('rec1', 6): 21,
      ('rec2', 1): 4, ('rec2', 2): 6, ('rec2', 3): 9}
per = lambda lat, K: (192 if lat == 'rec2' else 80) * K
for key in sorted(sat):
    d = sat[key]
    un = [L for L in d if d[L][0] == 'UNSAT']; sa = [L for L in d if d[L][0] == 'SAT']
    ts = ', '.join(f'{L}:{d[L][1]:.0f}' for L in sorted(d))
    print(f'| {key[0]} | {key[1]} ({per(*key)}) | {q0.get(key)} | {ranges(un)} | {ranges(sa) or "-"} | {ts} |')
print('\n### Fixed centres, exhaustive enumeration (cen3 = cen2 with general period; no pruning)\n')
print('| exterior | K (period) | q0 | |C| | centres | returns | dev | max prefix / target |')
print('|---|---|---|---|---|---|---|---|')
for key in sorted(enum):
    d = enum[key]
    for L in sorted(d):
        c, r, mp, tl, dev = d[L]
        print(f'| {key[0]} | {key[1]} ({per(*key)}) | {q0.get(key)} | {L} | {c:,} | {r} | {dev} | {mp} / {tl} |')

print('\n### Walls with an absorbing core (wallscan.py)\n')
print('| exterior | S | Kb | w | r | cores | instances | result |')
print('|---|---|---|---|---|---|---|---|')
for f in sorted(glob.glob('logs/wall/*.log')):
    head = [l for l in open(f) if l.startswith('SCAN')]
    done = [l for l in open(f) if l.startswith('DONE')]
    if not head: continue
    h = head[0]
    lat = re.search(r'lat=(\w+)', h).group(1); S = re.search(r' S=(\d+)', h).group(1); Kb = re.search(r'Kb=(\d+)', h).group(1)
    w = re.search(r' w=(\d+)', h).group(1); cores = re.search(r'cores=(\[[^\]]*\])', h).group(1)
    nres = sum(1 for l in open(f) if l.startswith('RES '))
    nsat = sum(1 for l in open(f) if l.startswith('RES SAT'))
    st = ('DONE ' if done else 'PARTIAL ') + (f'{nres} UNSAT' if nsat == 0 else f'{nsat} SAT!')
    rr = re.search(r'r=\[(\d+),(\d+)\)', h).group(0)
    killed = any('KILLED' in l for l in open(f))
    if killed: st += ' (stopped)'
    print(f'| {lat} | {S} | {Kb} | {w} | {rr} | {cores} | {nres} | {st} |')

print('\n### Seams into a periodic inner band (bandscan.py)\n')
print('| exterior | S | w | mU | l0 | result |')
print('|---|---|---|---|---|---|')
for f in sorted(glob.glob('logs/band/*.log')):
    h = [l for l in open(f) if l.startswith('BANDSCAN')]
    if not h: continue
    h = h[0]
    res = [l.split()[1] for l in open(f) if l.startswith('RES ')]
    done = any(l.startswith('DONE') for l in open(f))
    print(f'| {re.search(r"lat=(\w+)", h).group(1)} | {re.search(r" S=(\d+)", h).group(1)} | {re.search(r" w=(\d+)", h).group(1)} | '
          f'{re.search(r"mU=(\d+)", h).group(1)} | {re.search(r"l0=(\d+)", h).group(1)} | {",".join(res) or "-"}{"" if done else " (running)"} |')

print('\n### Confined kinks of any period: survival lifetimes (survscan.py; one representative per class o = n mod 4)\n')
print('| exterior | w | lifetime o=0 | o=1 | o=2 | o=3 | all classes die |')
print('|---|---|---|---|---|---|---|')
for f in sorted(glob.glob('logs/surv/*.log'), key=lambda x: (re.search(r'(rec\d)', x).group(1), int(re.search(r'_w(\d+)', x).group(1)))):
    lt = {}
    for l in open(f):
        if l.startswith('LIFETIME'):
            m = re.search(r'o=(\d) lifetime=(\S+)', l); lt[m.group(1)] = m.group(2)
    lat = re.search(r'(rec\d)', f).group(1); w = re.search(r'_w(\d+)', f).group(1)
    alld = len(lt) == 4
    print(f'| {lat} | {w} | {lt.get("0","-")} | {lt.get("1","-")} | {lt.get("2","-")} | {lt.get("3","-")} | {"yes" if alld else "partial"} |')
