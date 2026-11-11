#!/usr/bin/env python3
"""r12g2 mkrows_json.py -- explicit lattice rows (header 'p nB m base') from a Lean-verified certificate JSON
(lattice_formats/cert_b9_rec*.json: keys base, gam (clock), B_t (exterior rows), w_t (bulk rows)), plus its phase orbits.
usage: mkrows_json.py CERT.json OUT.rows"""
import sys, json
J = json.load(open(sys.argv[1])); b, g, B, W = J['base'], J['gam'], J['B_t'], J['w_t']
p, nB, m = len(g), len(B[0]), len(W[0]); assert len(B) == p and len(W) == p
with open(sys.argv[2], 'w') as f:
    f.write(f'{p} {nB} {m} {b}\n' + ' '.join(map(str, g)) + '\n')
    for t in range(p): f.write(' '.join(map(str, B[t])) + '\n')
    for t in range(p): f.write(' '.join(map(str, W[t])) + '\n')
seen = {}; orbs = []
for t in range(p):
    for j in range(m):
        for par in range(2):
            if (t, j, par) in seen: continue
            o = []; s = (t, j, par)
            while s not in seen:
                seen[s] = len(orbs); o.append(s); gg = g[s[0]]; dh = 1 if (gg == 1 and s[2] == 0) else 0
                s = ((s[0] + 1) % p, (s[1] + dh) % m, (s[2] + gg) % 2)
            orbs.append(o)
print(f'{sys.argv[2]}: base {b} p {p} nB {nB} m {m} clock {"".join(map(str, g))}; phase orbits {len(orbs)} of lengths {[len(o) for o in orbs]}')
for i, o in enumerate(orbs): print(f'  orbit {i}: representative {o[0]}, t=0 phases {sorted(x for x in o if x[0] == 0)}')
