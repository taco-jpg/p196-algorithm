#!/usr/bin/env python3
"""r11f: window contents (all cyclic start slots, wrapped ones included) of target interfaces, in winbits.h index format.
index = c_window | d_window << w | (sum_j r_j B^j) << 2w, r_j = digit at the j-th overflow slot inside the window; phase = start mod len(clock).
usage: wtargets.py B CLOCK w cuts.json P_list out.txt [charge0only=1]
cuts.json: list of {L,H,Y,P,charge}; P_list: comma list of periods to include (or 'all')."""
import sys, json
B = int(sys.argv[1]); pat = sys.argv[2]; w = int(sys.argv[3]); cuts = json.load(open(sys.argv[4]))
Ps = None if sys.argv[5] == 'all' else set(int(x) for x in sys.argv[5].split(','))
out = sys.argv[6]; only0 = len(sys.argv) < 8 or sys.argv[7] == '1'
L0 = len(pat); res = set(); used = 0
for o in cuts:
    T = o['P']
    if Ps is not None and T not in Ps: continue
    if only0 and o.get('charge', 0) != 0: continue
    assert T % L0 == 0
    ov = [pat[t % L0] == '1' for t in range(T)]; ovi = {}; n = 0
    for t in range(T):
        if ov[t]: ovi[t] = n; n += 1
    assert n == len(o['Y']), (n, len(o['Y']))
    used += 1
    for s in range(T):
        c = d = rv = 0; j = 0
        for i in range(w):
            t = (s + i) % T
            c |= ((o['L'] >> t) & 1) << i; d |= ((o['H'] >> t) & 1) << i
            if ov[t]: rv += o['Y'][ovi[t]] * B ** j; j += 1
        res.add((s % L0, c | (d << w) | (rv << (2 * w))))
with open(out, 'w') as f:
    for ph, idx in sorted(res): f.write(f'{ph} {idx}\n')
print('targets used', used, 'distinct (phase, window) pairs', len(res))
