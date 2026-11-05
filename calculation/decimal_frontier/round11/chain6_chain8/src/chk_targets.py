#!/usr/bin/env python3
"""r11f chain 6: per-target window test.  For every charge-0 cut key (L,H,Y) of period P (cuts6.json) and every cyclic window start s
(wrapped windows included), test membership of the window content in A_w(s mod 2) (bitset wsets/win_B10_01_w{w}_ph{ph}.bits, index
c | d<<w | (sum r_j 10^j)<<2w as in winbits.h).  A cut with a window outside A_w is unreachable (premise A, FILTER_R8 + r9u wrap).
Cuts k -> k+1 of one cycle are real reach edges (chk_conv6.py), so a cycle with ONE excluded cut has ALL its cuts excluded.
usage: chk_targets.py w [P_list]"""
import sys, json, mmap, collections
w = int(sys.argv[1]); Ps = None if len(sys.argv) < 3 else set(int(x) for x in sys.argv[2].split(","))
B = 10; pat = "01"
mm = []
for ph in range(2):
    f = open(f"wsets/win_B10_01_w{w}_ph{ph}.bits", "rb"); mm.append(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ))
def inA(ph, idx): return (mm[ph][idx >> 3] >> (idx & 7)) & 1
cuts = json.load(open("cuts6.json"))
bycyc = collections.defaultdict(list)
for o in cuts:
    if o["charge"] != 0: continue
    if Ps and o["P"] not in Ps: continue
    bycyc[(o["P"], o["cycle"])].append(o)
memo = {}
res = collections.defaultdict(lambda: [0, 0, 0, 0])   # P: cycles, cycles surviving, cut keys, cut keys surviving
for (P, ci), lst in sorted(bycyc.items()):
    ov = [t % 2 == 1 for t in range(P)]; oi = {}; n = 0
    for t in range(P):
        if ov[t]: oi[t] = n; n += 1
    cyc_ok = True
    for o in lst:
        key = (P, o["L"], o["H"], tuple(o["Y"]))
        if key not in memo:
            ok = True
            for s in range(P):
                c = d = rv = 0; j = 0
                for i in range(w):
                    t = (s + i) % P
                    c |= ((o["L"] >> t) & 1) << i; d |= ((o["H"] >> t) & 1) << i
                    if ov[t]: rv += o["Y"][oi[t]] * B ** j; j += 1
                if not inA(s % 2, c | (d << w) | (rv << (2 * w))): ok = False; break
            memo[key] = ok
        cyc_ok &= memo[key]
    r = res[P]; r[0] += 1; r[1] += cyc_ok
for key, ok in memo.items():
    r = res[key[0]]; r[2] += 1; r[3] += ok
for P in sorted(res):
    r = res[P]; print(f"w={w} P={P}: charge-0 cycles {r[0]}, cycles with every cut inside A_w {r[1]}; distinct cut keys {r[2]}, keys inside A_w {r[3]}", flush=True)
