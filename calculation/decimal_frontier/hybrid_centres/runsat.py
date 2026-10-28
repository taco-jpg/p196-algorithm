#!/usr/bin/env python3
"""runsat.py -- scan hybrid centre existence by CP-SAT.
usage: runsat.py <stream:p11|p12|p12b|p12c> <k> <W0lo> <W0hi> [tl_per_instance] [loops: comma list of 0,18,6,2]
Iterates loops, loop phases, A in 0..floor(S/2), W0 in range; prints one line per instance (flush)."""
import sys, time, json
from hyb import *
from ext import *
from hsat import solve
from sim1 import load_ext, LOOPS

STREAMS = {}
def stream(name):
    if name in STREAMS: return STREAMS[name]
    if name == 'p11':
        cyc = load_ext('p11')
    else:
        idx = {'p12': 0, 'p12b': 1, 'p12c': 2}[name]
        a = parse_accepts('/home/claude/research/w1_bases/out/ext4/b10_p12.txt')[idx]
        cyc = cycle_from(10, a['Bs'][0])
    STREAMS[name] = cyc
    return cyc

def loop_seq(loop, s, T):
    per = len(loop)
    return [loop[(s + t) % per] for t in range(T)]

if __name__ == '__main__':
    name = sys.argv[1]; k = int(sys.argv[2]); lo = int(sys.argv[3]); hi = int(sys.argv[4])
    tl = float(sys.argv[5]) if len(sys.argv) > 5 else 120
    which = sys.argv[6].split(',') if len(sys.argv) > 6 else ['0', '18', '6', '2']
    b = 10
    cyc = stream(name); p = len(cyc); T = p * k
    gam = [cyc[t % p][1] for t in range(T)]; e1 = [cyc[t % p][2] for t in range(T)]
    S = sum(gam)
    names = {'0': ('0', [0]), '18': ('18', [18]), '6': ('6/12', [6, 12]), '2': ('2..', [2, 4, 8, 16, 14, 10])}
    for w in which:
        lname, loop = names[w]
        per = len(loop)
        if T % per != 0:
            print(f"# skip loop {lname}: T={T} not a multiple of loop period {per}", flush=True); continue
        for s in range(per):
            cs = loop_seq(loop, s, T)
            for A in range(0, S // 2 + 1):
                for W0 in range(lo, hi + 1):
                    t0 = time.time()
                    st, Q0 = solve(b, gam, e1, cs, W0, A, tl=tl)
                    print(f"{name} k={k} T={T} S={S} loop={lname} phase={s} A={A} W0={W0}: {st} {Q0 if Q0 else ''} ({time.time()-t0:.1f}s)", flush=True)
                    if Q0:
                        json.dump(dict(stream=name, k=k, loop=lname, phase=s, A=A, Q0=Q0, cs=cs), open(f'out/HIT_{name}_k{k}_{lname.replace("/","-")}_s{s}_A{A}_W{W0}.json', 'w'))
