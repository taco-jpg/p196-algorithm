#!/usr/bin/env python3
"""Two-stage exterior/interior search for neutral one-band return cycles in many bases, parallel over tasks.

Theory (validated, see decouple.py / ext_transfer.py / interior_cp.py):
  * hyp forces e2 = 1-e1, so the exterior B evolves autonomously (map G_b) and the interior C evolves autonomously given the
    overflow word s (C-length changes by s_t - 2 v_t).  A cycle exists iff an exterior cycle (period p, overflow word s, carry
    word E) and an interior cycle (period k*p) agree on (s, E).  sumGain = 1.5 sumGam holds for every closed cycle.
  * stage 1 (exterior): breadth-first search in the transfer graph over carry bit-words (ext_transfer.exterior_cycles): finds
    EVERY exterior cycle of minimal period p<=PMAX and any length L<=LMAX.  Fast (ms-s per overflow word).
  * stage 2 (interior): CP-SAT on the padded register (interior_cp.solve_interior): one model per (s,E,k,parity) covers ALL
    interior widths <= W0MAX of that parity.  INFEASIBLE = proof (for that k and width bound).  Any hit is rebuilt as (B0,C0)
    and confirmed by the exact mirror (run -> cycle, cycleOK).

usage (Mac Studio, 32 cores, ~64-150 GB RAM):
   python3 studio_pipeline.py --bases 3-40 --pmax 6 --lmax 60 --kmax 3 --w0max 100 --tl 600 --jobs 31 --out pipe_all.jsonl
   python3 studio_pipeline.py --bases 10   --pmax 15 --lmax 80 --kmax 4 --w0max 160 --tl 1800 --jobs 31 --out pipe_b10.jsonl
output: JSON lines  {"type":"exterior"|"interior"|"cycle", ...};  summary table printed at the end (per base: #exterior cycles,
#(s,E) words, interior statuses, cycles found).  Re-running with the same --out resumes (finished (b,s,E,k,parity) are skipped).
cost: stage 1 ~ seconds per base for pmax<=6 (minutes for pmax 12-15); stage 2: seconds for infeasible/feasible narrow cases,
up to --tl per undecided instance.  One CP-SAT model with W0=100,k=3,p=6: ~50-200 MB.  UNKNOWN = time limit, NOT a proof.
"""
import sys, os, json, time, argparse, itertools, multiprocessing as mp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ext_transfer import exterior_cycles, to_B0
from decouple import G_ext
from interior_cp import solve_interior
from nb_mirror import run, cycleOK, gam as GAM


def parse_bases(txt):
    out = []
    for part in txt.split(','):
        if '-' in part:
            lo, hi = part.split('-'); out += list(range(int(lo), int(hi) + 1))
        else:
            out.append(int(part))
    return out


def stage1(args):
    b, pmax, lmax = args
    res = {}
    for p in range(1, pmax + 1):
        for s in itertools.product((0, 1), repeat=p):
            if not any(s) or s != min(s[i:] + s[:i] for i in range(p)): continue
            for L, items in exterior_cycles(b, p, s, lmax).items():
                for pth, cw in items:
                    B0 = to_B0(b, pth)
                    cur = list(B0); orb = []
                    for t in range(p):
                        orb.append(tuple(cur)); cur = G_ext(b, cur)[0]
                    if len(set(orb)) != p: continue
                    res.setdefault((s, tuple(cw)), []).append((L, list(B0)))
    return b, res


def stage2(task):
    b, s, E, k, W0, tl, Bs = task
    t0 = time.time()
    st, C0 = solve_interior(b, list(s), list(E), k, W0, tl)
    rec = {'type': 'interior', 'base': b, 's': ''.join(map(str, s)), 'E': ''.join(map(str, E)), 'k': k, 'W0': W0, 'status': st,
           'secs': round(time.time() - t0, 1)}
    cyc = None
    if C0 is not None:
        for L, B0 in Bs:
            r = run(b, list(B0), list(C0), maxsteps=20000, maxlen=5000)
            if r[0] == 'cycle':
                es = r[1]
                cyc = {'type': 'cycle', 'base': b, 's': rec['s'], 'E': rec['E'], 'k': k, 'W0': W0, 'cycleOK': cycleOK(b, es, es[0][0], es[0][1]),
                       'edges': len(es), 'sumGam': sum(GAM(b, e[0], e[1]) for e in es), 'B0': B0, 'C0': C0,
                       'edge_list': [[e[0], e[1], e[2], e[3], e[4], e[5]] for e in es]}
                break
    return rec, cyc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--bases', default='3-40'); ap.add_argument('--pmax', type=int, default=6); ap.add_argument('--lmax', type=int, default=60)
    ap.add_argument('--kmax', type=int, default=3); ap.add_argument('--w0max', type=int, default=100); ap.add_argument('--tl', type=float, default=600)
    ap.add_argument('--jobs', type=int, default=2); ap.add_argument('--out', default='pipe.jsonl')
    a = ap.parse_args()
    bases = parse_bases(a.bases)
    done = set(); prev = []
    if os.path.exists(a.out):
        for line in open(a.out):
            r = json.loads(line); prev.append(r)
            if r['type'] == 'interior' and r['status'] != 'UNKNOWN': done.add((r['base'], r['s'], r['E'], r['k'], r['W0'] % 2))
    t0 = time.time()
    with mp.Pool(a.jobs) as pool, open(a.out, 'a') as fo:
        ext = {}
        for b, res in pool.imap_unordered(stage1, [(b, a.pmax, a.lmax) for b in bases]):
            ext[b] = res
            fo.write(json.dumps({'type': 'exterior_summary', 'base': b, 'cycles': sum(len(v) for v in res.values()), 'words': len(res),
                                 'examples': [{'s': ''.join(map(str, s)), 'E': ''.join(map(str, E)), 'L': v[0][0], 'B0': v[0][1]} for (s, E), v in sorted(res.items())]}) + '\n'); fo.flush()
            print(f"stage1 base {b}: {sum(len(v) for v in res.values())} exterior cycles, {len(res)} (s,E) words  [{time.time()-t0:.0f}s]", flush=True)
        tasks = []
        for b in bases:
            for (s, E), Bs in sorted(ext[b].items(), key=lambda kv: (len(kv[0][0]), kv[0])):
                for k in range(1, a.kmax + 1):
                    if (sum(s) * k) % 2: continue
                    for par in (0, 1):
                        W0 = a.w0max - ((a.w0max - par) % 2)
                        if (b, ''.join(map(str, s)), ''.join(map(str, E)), k, par) in done: continue
                        tasks.append((b, s, E, k, W0, a.tl, Bs))
        print(f"stage2: {len(tasks)} interior instances", flush=True)
        for rec, cyc in pool.imap_unordered(stage2, tasks):
            fo.write(json.dumps(rec) + '\n')
            if cyc: fo.write(json.dumps(cyc) + '\n'); print("*** CYCLE", cyc['base'], cyc['s'], cyc['E'], 'k', cyc['k'], 'cycleOK', cyc['cycleOK'], flush=True)
            fo.flush()
            print(rec, flush=True)
    # summary
    rows = {}
    for line in open(a.out):
        r = json.loads(line)
        if r['base'] not in bases if 'base' in r else True: continue
        d = rows.setdefault(r['base'], {'ext': 0, 'words': 0, 'status': {}, 'cycles': 0})
        if r['type'] == 'exterior_summary': d['ext'] = r['cycles']; d['words'] = r['words']
        if r['type'] == 'interior': d['status'][r['status']] = d['status'].get(r['status'], 0) + 1
        if r['type'] == 'cycle' and r['cycleOK']: d['cycles'] += 1
    print(f"{'base':>4} {'ext.cycles':>10} {'(s,E)':>6} {'interior statuses':<40} {'full cycles (cycleOK)':>8}")
    for b in sorted(rows):
        d = rows[b]; print(f"{b:>4} {d['ext']:>10} {d['words']:>6} {str(d['status']):<40} {d['cycles']:>8}")
    print(f"elapsed {time.time()-t0:.0f}s")


if __name__ == '__main__':
    main()
