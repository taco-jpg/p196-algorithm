"""run_btransfer.py -- STEP 1 on the Mac Studio: exact decision of "does a p-periodic B-block exist?" in a given base,
for every overflow pattern, with no bound on |B|.  Parallel over patterns.

  python3 run_btransfer.py --base 10 --pmin 1 --pmax 18 --procs 16 --maxstates 30000000 --out b10.jsonl

Output: one JSON line per (p, overflow pattern):
  {"base":10,"p":11,"O":[...],"status":"EXISTS"|"NONE"|"LIMIT","states":N,"streams":[{"e1":[...],"B":[...]}, ...]}
 * NONE   = proved: no p-periodic B with this overflow pattern at any length (exact; the state space is finite).
 * LIMIT  = state cap hit (rerun that pattern with a larger --maxstates).
 * EXISTS = B cycle(s) found; "streams" lists each distinct e1-stream with one B (time 0) - these are the inputs of full_search.py.
Memory: ~150-250 bytes per state in the parent map; a pattern with 20M states needs ~5 GB.  Use --procs so that
procs * maxstates * 250 B fits in RAM (150 GB: --procs 16 --maxstates 30000000 is safe).
Expected runtime base 10 (single-thread Python, measured): p<=10 <1 s each, p=11 3 s, p=12 15 s, p=13 0.4 s, p=14 21 s, p=15 5 s;
p=16 has a few patterns with millions of states (minutes each) - parallelism matters from p>=16.
Heavy patterns first: patterns are submitted with the largest number of overflows first."""
import argparse, json, sys, time, os, multiprocessing as mp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bcore import decide, patterns


def work(args):
    b, p, O, maxstates = args
    t0 = time.time()
    st, ns, res = decide(b, p, O, maxstates, collect=True)
    rec = {"base": b, "p": p, "O": list(O), "status": st, "states": ns, "secs": round(time.time() - t0, 2)}
    if res:
        rec["streams"] = [{"e1": list(e), "B": B} for e, B in res]
    return rec


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', type=int, required=True)
    ap.add_argument('--pmin', type=int, default=1)
    ap.add_argument('--pmax', type=int, required=True)
    ap.add_argument('--procs', type=int, default=4)
    ap.add_argument('--maxstates', type=int, default=20_000_000)
    ap.add_argument('--maxones', type=int, default=None, help='only patterns with at most this many overflows')
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    with open(a.out, 'a') as f, mp.Pool(a.procs) as pool:
        for p in range(a.pmin, a.pmax + 1):
            pats = sorted(patterns(p, 1, a.maxones), key=lambda O: -sum(O))
            tasks = [(a.base, p, O, a.maxstates) for O in pats]
            t0 = time.time()
            cnt = {}
            for rec in pool.imap_unordered(work, tasks, chunksize=1):
                f.write(json.dumps(rec) + "\n"); f.flush()
                cnt[rec["status"]] = cnt.get(rec["status"], 0) + 1
            print(f"base {a.base} p={p}: {len(pats)} patterns -> {cnt}  ({time.time()-t0:.0f}s)", flush=True)
