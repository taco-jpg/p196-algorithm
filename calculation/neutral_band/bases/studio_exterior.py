#!/usr/bin/env python3
"""Exhaustive exterior-cycle search (transfer-graph BFS) for large periods p, parallel over overflow words.

For base b and every period p in [PLO, PHI] and every overflow word s in {0,1}^p (up to rotation) the BFS from the start
interface runs until the layer set is EMPTY ('dead' = PROOF that no exterior of that period/word exists, for any length L) or
LMAX layers pass without death ('alive' = undecided, usually an overflow word that is a repetition of a shorter word) or a
closing state is hit ('found': all exterior cycles for the word are then extracted and verified with G_ext).

usage (Mac Studio):
   python3 studio_exterior.py --base 10 --plo 16 --phi 24 --lmax 80 --jobs 31 --out ext_b10_p16_24.jsonl
   python3 studio_exterior.py --base 3-40 --plo 7 --phi 14 --lmax 80 --jobs 31 --out ext_all_p7_14.jsonl
output: one JSON line per word (status dead/alive/found) + a summary per (base,p).  Resumes if --out exists.
cost (this laptop, 1 core): base 10, p=14: 1181 words in 24 s; p=15: 2191 words in 5 s; words that are repetitions of a short
word can keep 1e4 states per layer (p=8 '01010101': 17 s).  Expect p=20 ~ 52k words ~ minutes on 31 cores, p=24 ~ 700k words ~
an hour.  Memory < 300 MB per process (layer sets only).  --wordtime caps seconds per word (then status 'timeout').
"""
import sys, os, json, time, argparse, itertools, multiprocessing as mp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ext_transfer import cell_transitions, exterior_cycles, to_B0
from decouple import G_ext
from studio_pipeline import parse_bases


def words(p):
    for s in itertools.product((0, 1), repeat=p):
        if any(s) and s == min(s[i:] + s[:i] for i in range(p)):
            yield s


def classify(task):
    b, s, lmax, wordtime = task
    p = len(s); shifted = [t for t in range(p) if s[t]]
    layer = {(tuple([0] * p), tuple(s), tuple([1] * len(shifted))): 1}
    t0 = time.time(); hit = False; maxsz = 0
    for j in range(lmax):
        nxt = {}
        for st in layer:
            cw, dw, T = st
            for ns, qo in cell_transitions(b, p, s, cw, dw, T, first=(j == 0)):
                nxt[ns] = 1
        layer = nxt; maxsz = max(maxsz, len(layer))
        if not layer:
            return {'base': b, 'p': p, 's': ''.join(map(str, s)), 'status': 'dead', 'layer': j + 1, 'maxlayer': maxsz}
        if any(all(st[1][t] == 1 - st[0][t] for t in range(p)) and all(st[2][i] == (b - 1) * st[0][t] for i, t in enumerate(shifted)) for st in layer):
            hit = True; break
        if time.time() - t0 > wordtime:
            return {'base': b, 'p': p, 's': ''.join(map(str, s)), 'status': 'timeout', 'layer': j + 1, 'maxlayer': maxsz}
    if not hit:
        return {'base': b, 'p': p, 's': ''.join(map(str, s)), 'status': 'alive', 'layer': lmax, 'maxlayer': maxsz}
    out = []
    for L, items in sorted(exterior_cycles(b, p, s, lmax).items()):
        for pth, cw in items:
            B0 = to_B0(b, pth); cur = list(B0); ok = True; Ew = []; Gw = []
            for t in range(p):
                r = G_ext(b, cur)
                if r is None: ok = False; break
                Ew.append(r[2]); Gw.append(r[3]); cur = r[0]
            ok = ok and tuple(cur) == B0 and tuple(Gw) == s and tuple(Ew) == tuple(cw)
            out.append({'L': L, 'E': ''.join(map(str, cw)), 'B0': list(B0), 'verified': ok})
    return {'base': b, 'p': p, 's': ''.join(map(str, s)), 'status': 'found' if out else 'closing-only', 'cycles': out, 'maxlayer': maxsz}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', default='10'); ap.add_argument('--plo', type=int, default=1); ap.add_argument('--phi', type=int, default=12)
    ap.add_argument('--lmax', type=int, default=80); ap.add_argument('--jobs', type=int, default=2); ap.add_argument('--wordtime', type=float, default=900)
    ap.add_argument('--out', default='ext.jsonl')
    a = ap.parse_args()
    done = set()
    if os.path.exists(a.out):
        for line in open(a.out):
            r = json.loads(line)
            if 's' in r: done.add((r['base'], r['s']))
    tasks = [(b, s, a.lmax, a.wordtime) for b in parse_bases(a.base) for p in range(a.plo, a.phi + 1) for s in words(p)
             if (b, ''.join(map(str, s))) not in done]
    t0 = time.time(); stat = {}
    with mp.Pool(a.jobs) as pool, open(a.out, 'a') as fo:
        for r in pool.imap_unordered(classify, tasks, chunksize=8):
            fo.write(json.dumps(r) + '\n')
            key = (r['base'], r['p']); d = stat.setdefault(key, {})
            d[r['status']] = d.get(r['status'], 0) + 1
            if r['status'] in ('found', 'alive', 'timeout', 'closing-only'): print(r, flush=True); fo.flush()
    print(f"{'base':>4} {'p':>3}  statuses (dead = no exterior for any length)")
    for (b, p), d in sorted(stat.items()): print(f"{b:>4} {p:>3}  {d}")
    print(f"elapsed {time.time()-t0:.0f}s")


if __name__ == '__main__':
    main()
