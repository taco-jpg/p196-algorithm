#!/usr/bin/env python3
"""Re-run every instance that a sweep left UNKNOWN (CP-SAT time limit) with a longer limit and several threads.
usage: retry_unknown.py --base 10 --tl 3600 --jobs 6 --threads 4 --out retry.jsonl  sweep_results/*.jsonl"""
import sys, os, json, argparse, time, multiprocessing as mp
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import p196cp as P
def work(a):
    b, S, tl, th, nonmax = a
    r = P.solve(b, tuple(map(tuple, S)), maximal=not nonmax, time_limit=tl, workers=th)
    return {"base": b, "S": S, "status": r["status"], "time": r["time"], "cert": r.get("certificate")}
if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--base", type=int, default=10); ap.add_argument("--tl", type=float, default=3600)
    ap.add_argument("--jobs", type=int, default=6); ap.add_argument("--threads", type=int, default=4); ap.add_argument("--nonmax", action="store_true")
    ap.add_argument("--out", required=True); ap.add_argument("files", nargs="+")
    a = ap.parse_args(); todo = []
    for fn in a.files:
        for line in open(fn):
            r = json.loads(line)
            if r["key"][0] == a.base: todo += r["unknown_S"]
    done = set()
    if os.path.exists(a.out):
        for line in open(a.out): done.add(json.dumps(json.loads(line)["S"]))
    todo = [S for S in todo if json.dumps(S) not in done]
    print(f"[retry] {len(todo)} instances", flush=True)
    with mp.Pool(a.jobs) as pool, open(a.out, "a") as fo:
        for r in pool.imap_unordered(work, [(a.base, S, a.tl, a.threads, a.nonmax) for S in todo]):
            fo.write(json.dumps(r) + "\n"); fo.flush(); print(r["status"], r["S"][0], r["time"], flush=True)
            if r["status"] == "SAT":
                with open(os.path.join(os.path.dirname(os.path.abspath(a.out)), "FOUND.jsonl"), "a") as ff:
                    ff.write(json.dumps({"base": a.base, "S": r["S"], "cert": r["cert"]}) + "\n")
                print("!!!!!!!! SAT FOUND", flush=True)
