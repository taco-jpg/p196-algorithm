#!/usr/bin/env python3
"""Compare forward-scan observations (fwdscan output) with the Lean ancestry bounds.

Usage: compare_fwd.py entries.json fwd_output.txt [more fwd outputs ...]

A Lean ancestry endpoint says: orbit A t = P, P a palindrome beginning with p
=> t <= T(p).  For 4-digit entries T = bound + 1; the 2- and 3-digit endpoints
state T directly.  A VIOLATION is an observed palindrome with t > T(p).
"""
import json, sys

TWO = {"10": 1, "20": 2, "32": 2, "40": 3, "41": 3, "60": 3, "64": 3, "65": 6, "76": 3,
       "80": 4, "81": 4, "82": 4, "83": 4}
THREE = {"217": 23, "218": 34, "777": 25, "620": 12, "739": 39}
for a, b, c, B in [(1,1,9,8),(2,1,3,23),(2,1,6,10),(2,5,7,16),(2,7,6,31),(2,7,7,31),(2,7,8,31),
                   (3,4,8,16),(3,7,7,8),(3,8,4,7),(3,8,5,8),(4,2,6,24),(4,2,9,24),(4,7,4,7),
                   (6,7,4,5),(7,3,7,12),(7,5,5,12),(7,7,8,25),(7,8,3,14),(7,8,4,14),(7,8,5,40),
                   (7,8,6,27),(7,8,7,25),(7,8,8,14),(7,8,9,38),(8,5,6,38),(8,5,7,25),(8,5,8,36),
                   (8,5,9,36),(9,0,5,11),(9,0,6,11),(9,2,3,7),(9,3,5,10)]:
    THREE[f"{a}{b}{c}"] = B


def main():
    ents = json.load(open(sys.argv[1]))
    T = dict(TWO); T.update(THREE)
    src = {p: "Core.TwoDigit" for p in TWO}
    src.update({p: "3-digit endpoint" for p in THREE})
    for e in ents:
        p = "".join(map(str, e["prefix"]))
        T[p] = e["bound"] + 1
        src[p] = e["module"]
    obs = {}
    for f in sys.argv[2:]:
        for line in open(f):
            p, t, seed, hits = line.split()
            t, hits = int(t), int(hits)
            if p not in obs or t > obs[p][0]:
                obs[p] = (t, seed, obs.get(p, (0, "", 0))[2] + hits)
            else:
                obs[p] = (obs[p][0], obs[p][1], obs[p][2] + hits)
    viol, sharp, seen = [], [], 0
    gap = {}
    for p, bound in T.items():
        if p not in obs:
            continue
        seen += 1
        t, seed, hits = obs[p]
        if t > bound:
            viol.append((p, bound, t, seed, src[p]))
        elif t == bound:
            sharp.append((p, bound, seed))
        gap[bound - t] = gap.get(bound - t, 0) + 1
    print(f"claimed prefixes: {len(T)}; observed (some palindrome hit): {seen}")
    print(f"VIOLATIONS (observed t > Lean bound): {len(viol)}")
    for v in viol[:50]:
        print("   ", v)
    print(f"bound attained exactly: {len(sharp)}  e.g. {sharp[:12]}")
    print(f"histogram of (bound - max observed t): {dict(sorted(gap.items()))}")
    allmax = max(((v[0], k, v[1]) for k, v in obs.items() if len(k) == 4), default=None)
    print(f"largest delay seen for any 4-digit prefix (t, prefix, seed): {allmax}")
    cert_max = max(((obs[p][0], p, obs[p][1]) for p in T if p in obs and len(p) == 4), default=None)
    print(f"largest delay seen for a CERTIFIED 4-digit prefix (t, prefix, seed): {cert_max}")


if __name__ == "__main__":
    main()
