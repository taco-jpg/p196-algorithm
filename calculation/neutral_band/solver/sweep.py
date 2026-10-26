#!/usr/bin/env python3
"""Parallel sweep over length schedules.  Run on the Mac Studio (see README_STUDIO.txt).

Work unit = (b, p, G, gam-positions, u-composition): the worker enumerates every v-composition and every
(n_0,m_0) offset inside the length box, skips non-canonical / non-primitive shapes and (base 10) schedules that
touch the exhaustively refuted box |B|<=3,|C|<=6, and solves each remaining schedule with CP-SAT (1 thread).
One JSONL line is appended per finished unit; SAT results are also appended to FOUND.jsonl (loud).
Resumable: re-running the same command skips units already present in --out.
"""
import sys, os, json, time, argparse, itertools, multiprocessing as mp
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import p196cp as P

def wcomp(total, parts):
    if parts == 1: yield (total,); return
    for i in range(total + 1):
        for rest in wcomp(total - i, parts - 1): yield (i,) + rest

def rot(x, r): return x[r:] + x[:r]

def units(b, plist, Glist, shard=(0, 1)):
    idx = 0
    for G in Glist:
        for p in plist:
            if G > p or G % 2: continue
            for pos in itertools.combinations(range(1, p), G - 1):
                gam = tuple(1 if (k == 0 or k in pos) else 0 for k in range(p))
                for u in wcomp(G, p):
                    idx += 1
                    if idx % shard[1] != shard[0]: continue
                    yield (b, p, G, gam, u)

def canonical_primitive(sh):
    p = len(sh)
    for r in range(1, p):
        if sh[r][0] != 1: continue
        t = rot(sh, r)
        if t == sh: return False          # proper repetition: a shorter cycle covers it
        if t < sh: return False           # another rotation is the canonical one
    return True

COV_B, COV_C = 3, 6
def covered(S): return any(n <= COV_B and m <= COV_C for n, m in S)

def run_unit(args):
    (b, p, G, gam, u), cfg = args
    NMAX, MMAX, NMIN, MMIN, TL, COVER, MAXIMAL, BACKEND = cfg
    t0 = time.time(); cnt = unsat = sat = unk = 0; tsum = 0.0; tmax = 0.0
    slow, found, unknown, bad = [], [], [], []
    for v in wcomp(G // 2, p):
        sh = tuple(zip(gam, u, v))
        if not canonical_primitive(sh): continue
        pn = [0]; pm = [0]
        for (g, uu, vv) in sh[:-1]: pn.append(pn[-1] + g - uu); pm.append(pm[-1] + g - 2 * vv)
        lo_n = max(NMIN - x for x in pn); hi_n = min(NMAX - x for x in pn)
        lo_m = max(MMIN - x for x in pm); hi_m = min(MMAX - x for x in pm)
        for n0 in range(lo_n, hi_n + 1):
            for m0 in range(lo_m, hi_m + 1):
                S = tuple((n0 + pn[k], m0 + pm[k]) for k in range(p))
                if COVER and b == 10 and covered(S): continue
                r = P.solve(b, S, backend=BACKEND, maximal=MAXIMAL, time_limit=TL, workers=1)
                cnt += 1; tsum += r['time']; tmax = max(tmax, r['time'])
                st = r['status']
                if st == 'UNSAT': unsat += 1
                elif st == 'SAT':
                    sat += 1; found.append({"S": S, "cert": r['certificate']})
                elif st == 'UNKNOWN': unk += 1; unknown.append(S)
                else: bad.append((S, st))
                if r['time'] > 2.0 and st != 'UNKNOWN': slow.append([S, r['time'], st])
    return {"key": [b, p, G, list(gam), list(u)], "n": cnt, "unsat": unsat, "sat": sat, "unknown": unk,
            "t_solver": round(tsum, 2), "t_wall": round(time.time() - t0, 2), "tmax": round(tmax, 2),
            "slow": slow[:20], "found": found, "unknown_S": unknown, "invalid": bad[:5]}

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", type=int, default=10)
    ap.add_argument("--p", default="2-12", help="range a-b or list a,b,c of cycle lengths (number of edges)")
    ap.add_argument("--G", default="2", help="list of total overflow counts (even), e.g. 2 or 2,4")
    ap.add_argument("--nmax", type=int, default=20); ap.add_argument("--mmax", type=int, default=20)
    ap.add_argument("--nmin", type=int, default=0); ap.add_argument("--mmin", type=int, default=0)
    ap.add_argument("--tl", type=float, default=120, help="per-instance CP-SAT time limit (s)")
    ap.add_argument("--jobs", type=int, default=30); ap.add_argument("--shard", default="0/1", help="i/N for several machines")
    ap.add_argument("--no-cover", action="store_true", help="do not skip schedules touching the refuted base-10 box")
    ap.add_argument("--nonmax", action="store_true", help="allow non-maximal trimming (slower, same answers)")
    ap.add_argument("--backend", default="cpsat", choices=["cpsat", "z3"])
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    def rng(s):
        return list(range(int(s.split('-')[0]), int(s.split('-')[1]) + 1)) if '-' in s else [int(x) for x in s.split(',')]
    plist, Glist = rng(a.p), rng(a.G)
    sh = tuple(int(x) for x in a.shard.split('/'))
    cfg = (a.nmax, a.mmax, a.nmin, a.mmin, a.tl, not a.no_cover, not a.nonmax, a.backend)
    done = set()
    if os.path.exists(a.out):
        for line in open(a.out):
            try: done.add(json.dumps(json.loads(line)["key"]))
            except Exception: pass
    todo = [x for x in units(a.base, plist, Glist, sh) if json.dumps([x[0], x[1], x[2], list(x[3]), list(x[4])]) not in done]
    print(f"[sweep] base={a.base} p={plist} G={Glist} n<={a.nmax} m<={a.mmax} jobs={a.jobs}: {len(todo)} units to run ({len(done)} already done)", flush=True)
    found_path = os.path.join(os.path.dirname(os.path.abspath(a.out)), "FOUND.jsonl")
    tot = {"n": 0, "unsat": 0, "sat": 0, "unknown": 0}; t0 = time.time(); k = 0
    with mp.Pool(a.jobs, maxtasksperchild=200) as pool, open(a.out, "a") as fo:
        for res in pool.imap_unordered(run_unit, [(x, cfg) for x in todo], chunksize=1):
            fo.write(json.dumps(res) + "\n"); fo.flush(); k += 1
            for key in tot: tot[key] += res[key]
            if res["sat"]:
                with open(found_path, "a") as ff:
                    for f in res["found"]: ff.write(json.dumps({"base": a.base, **f}) + "\n")
                print("!!!!!!!! SAT FOUND base", a.base, res["found"][0]["S"], flush=True)
            if k % 50 == 0 or k == len(todo):
                print(f"[sweep] {k}/{len(todo)} units, {time.time()-t0:.0f}s, totals {tot}", flush=True)
    print("[sweep] DONE", tot, f"{time.time()-t0:.0f}s")

if __name__ == "__main__":
    main()
