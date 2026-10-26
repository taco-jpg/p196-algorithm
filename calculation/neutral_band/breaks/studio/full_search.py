"""full_search.py -- STEP 2 on the Mac Studio: turn B-cycles (from run_btransfer.py) into complete certificates.

  python3 full_search.py --in b10.jsonl --procs 30 --zlo 5 --zhi 90 --tl 120 --out certs10.jsonl

For every EXISTS record and every distinct e1-stream it asks CP-SAT (ccycle_padded.solve_C) for a symmetric C that is periodic under the
streams (e1(t), gam(t)).  If sum(gam) is odd the B-cycle is repeated twice (a certificate needs an even number of overflows per cycle:
proved from the length bookkeeping, 2*(g'-g) = sum gam).  Scans Z0 = (first+last real index of C at time 0) upward: Z0 ~ |C| + 3.
Every hit is re-verified with the Lean-mirror library (neutral_band_search.run / cycleOK / is_cert) and by 3 full periods of genuine
big-integer reverse-and-add on the template number with gap g = 2 + sum gam; only then it is reported as CERTIFICATE.
Cost: one CP-SAT solve per (stream, Z0); each is seconds for |C|<=30, minutes for |C|~45 (base 11 certificate: |C|=42..44).
Use --workers 1 and many --procs (embarrassingly parallel).  Results: JSONL with status per (stream, Z0)."""
import argparse, json, sys, os, time, multiprocessing as mp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from ccycle_padded import solve_C, real_part


def integer_check(b, B, C, nedges, gsum, periods=3):
    """genuine big-integer check: build the number whose pair word is the template tmpl(B,C,g) with a generous gap,
    run reverse-and-add for `periods` full periods; it must never hit a palindrome and at EVERY step the template found in the
    integer must be a state of a library cycle (same test as neutral_band_search.selftest)."""
    n = b - 1
    g = 6 + 2 * gsum * periods
    W = B + [n] * g + C + [n] * g + B[::-1]
    x = sum(w * b ** i for i, w in enumerate(W))
    for _ in range(periods * nedges):
        d = N.digits(b, x)
        if d == d[::-1]:
            return False
        tp = N.template_of(b, x)
        if tp is None:
            return False
        rr = run(b, tp[0], tp[1], maxsteps=4000, maxlen=2000)
        if rr[0] != 'cycle' or not is_cert(b, rr[1]):
            return False
        x = N.rev_add(b, x)
    return True


def task(args):
    b, p, O, e1, B, Z0, tl = args
    gs = list(O); es = list(e1)
    if sum(gs) % 2:
        gs = gs * 2; es = es * 2
    t0 = time.time()
    st, rows = solve_C(b, es, gs, Z0, tl, 1)
    rec = {"base": b, "p": p, "O": list(O), "e1": list(e1), "Z0": Z0, "status": st, "secs": round(time.time() - t0, 1)}
    if rows:
        C0 = real_part(b, rows[0])
        rec["B"] = B; rec["C"] = C0
        r = run(b, list(B), C0, maxsteps=4000, maxlen=2000)
        rec["library"] = r[0]
        if r[0] == 'cycle':
            edges = r[1]
            ok = cycleOK(b, edges, edges[0][0], edges[0][1]) and is_cert(b, edges)
            rec["cycleOK"] = bool(ok)
            gsum = sum(gam(b, E[0], E[1]) for E in edges)
            rec["period"] = len(edges)
            rec["sumGam"] = gsum
            rec["integer_check"] = bool(ok and integer_check(b, edges[0][0], edges[0][1], len(edges), gsum, 3))
            rec["CERTIFICATE"] = bool(rec["integer_check"])
    return rec


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('--in', dest='inp', required=True)
    ap.add_argument('--procs', type=int, default=8)
    ap.add_argument('--zlo', type=int, default=5)
    ap.add_argument('--zhi', type=int, default=60)
    ap.add_argument('--tl', type=float, default=120)
    ap.add_argument('--out', required=True)
    ap.add_argument('--minp', type=int, default=1)
    ap.add_argument('--maxp', type=int, default=99)
    a = ap.parse_args()
    tasks = []
    for line in open(a.inp):
        r = json.loads(line)
        if r["status"] != "EXISTS" or not (a.minp <= r["p"] <= a.maxp):
            continue
        for s in r["streams"]:
            for Z0 in range(a.zlo, a.zhi + 1):
                tasks.append((r["base"], r["p"], r["O"], s["e1"], s["B"], Z0, a.tl))
    print(len(tasks), "CP-SAT tasks", flush=True)
    found = 0
    with open(a.out, 'a') as f, mp.Pool(a.procs) as pool:
        for rec in pool.imap_unordered(task, tasks, chunksize=1):
            f.write(json.dumps(rec) + "\n"); f.flush()
            if rec.get("CERTIFICATE"):
                found += 1
                print("CERTIFICATE FOUND:", json.dumps(rec), flush=True)
    print("done; certificates found:", found)
