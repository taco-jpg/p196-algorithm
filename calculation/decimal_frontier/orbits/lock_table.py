import re, sys
def parse(fn):
    rows = []; cur = None
    for line in open(fn):
        if line.startswith('=='): name = line.strip(); continue
        m = re.match(r'base (\d+) seedlen (\d+) seed (\d+) steps (\d+) pal (\d) finaldigits (\d+) gamdens ([\d.]+)', line)
        if m:
            cur = {'base': int(m[1]), 'steps': int(m[4]), 'pal': int(m[5]), 'n': int(m[6]), 'gd': float(m[7]), 'K': {}, 'name': name if 'name' in dir() else ''}
            rows.append(cur); continue
        m = re.match(r' K=(\d+) best p=(\d+) L=(\d+)  runs>=20/50/100 at best p: (\d+)/(\d+)/(\d+)\s+\| shuffled max L=(\d+)', line)
        if m and cur: cur['K'][int(m[1])] = (int(m[2]), int(m[3]), int(m[4]), int(m[5]), int(m[6]), int(m[7]))
        m = re.match(r' gam stream longest p-periodic stretch \(p=1\.\.(\d+)\): (.*)', line)
        if m and cur: cur['gam'] = list(map(int, m[2].split()))
    return rows
if __name__ == '__main__':
    rows = parse(sys.argv[1])
    print('base steps n  gamdens | gam stretch: p=2 / best any p>=2 (p) | K=1 (p,L) | K=2 | K=3 | K=4 | K=6   [L = run+p; shuffled max in brackets]')
    for r in rows:
        g = r['gam']; ge = max(g[1:]); gp = g.index(ge) + 1
        s = lambda K: '%d,%d[%d]' % (r['K'][K][0], r['K'][K][1], r['K'][K][5]) if K in r['K'] else '-'
        print(f"{r['base']:3d} {r['steps']:6d} {r['n']:6d} {r['gd']:.3f} | {g[1]:4d} / {ge:4d} (p{gp:2d}) | {s(1):9s} | {s(2):9s} | {s(3):9s} | {s(4):9s} | {s(6):9s}")
