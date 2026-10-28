import re, sys
fn = sys.argv[1]
cur_b = None
rows = []
for line in open(fn):
    m = re.match(r'### b=(\d+) p=(\d+)', line)
    if m: cur_b = int(m.group(1)); continue
    if line.startswith('CAPPED'):
        rows.append(('CAPPED', cur_b, line.strip())); continue
    m = re.match(r'SCC p=(\d+) g=(\w+) size=(\d+) cyclen=(\d+) depth=(\d+) path=(.*) cyc=(.*)', line.strip())
    if not m: continue
    p, g, size, cl, depth, path, cyc = m.groups()
    cols = [list(map(int, c.split(','))) for c in re.findall(r'\[([^\]]*)\]', cyc)]
    p = int(p); cl = int(cl); S = g.count('1')
    if len(cols) < cl or any(len(c) < p for c in cols):
        rows.append(('SCC', cur_b, p, g, S, int(size), cl, int(depth), 'TRUNC', 'm|S' if S % cl == 0 else '', '')); continue
    # lattice words per time
    sym = []
    for t in range(p):
        w = [cols[j][t] for j in range(cl)]
        ok = any(all(w[k] == w[(a - k) % cl] for k in range(cl)) for a in range(cl))
        sym.append(ok)
    neutral = all(all(c[t] == cur_b - 1 for t in range(p)) for c in cols) and cl == 1
    rows.append(('SCC', cur_b, p, g, S, int(size), cl, int(depth), 'neutral' if neutral else '', 'm|S' if S % cl == 0 else '', 'sym_all_t' if all(sym) else ('sym_some' if any(sym) else '')))
for r in rows:
    print(*r)
