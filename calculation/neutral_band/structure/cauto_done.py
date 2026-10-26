#!/usr/bin/env python3
"""Bookkeeping for cauto / cauto_fast runs.
  cauto_done.py indices E G FILE...      print the pattern indices that are finished (old 'allm v=' stderr lines, new 'DONE' lines)
  cauto_done.py coverage E G FILE...     check that every trim pattern is finished, directly or through a shift-equivalent pattern
E, G = the (already repeated) driver streams exactly as given to cauto, e.g. 10100110011 10100110011 ... (E E) and (G G).
A pattern counts as finished if some file has an 'allm v=<pattern> ...' line (old stderr) or a 'DONE ... v=<pattern> status=none' line (new stdout),
and no CAPPED / NOPERIOD / FEASIBLE line or DONE status other than none mentions it.
Index = position of the pattern in the order of cauto's -vall enumeration (lexicographic over the sorted positions of the 1s)."""
import sys, itertools, re
def patterns(P, K):
    for c in itertools.combinations(range(P), K):
        p = ['0'] * P
        for i in c: p[i] = '1'
        yield ''.join(p)
def load(files, P):
    good, bad = set(), set()
    for fn in files:
        for line in open(fn, errors='replace'):
            t = line.split()
            if not t: continue
            m = re.search(r" v=([01]{%d})\b" % P, line)
            if not m: continue
            pat = m.group(1)
            if t[0] in ('CAPPED', 'NOPERIOD', 'FEASIBLE', 'FEASIBLE_CLASS'): bad.add(pat)
            elif t[0] == 'allm':
                (bad if re.search(r"feasible_classes=[1-9]", line) else good).add(pat)
            elif t[0] == 'DONE':
                (good if ('status=none' in line and not re.search(r"feasible_classes=[1-9]", line)) else bad).add(pat)
    return good - bad, bad
def main():
    cmd, E, G, files = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
    P = len(E); K = G.count('1') // 2
    shifts = [s for s in range(1, P) if all(E[(t + s) % P] == E[t] and G[(t + s) % P] == G[t] for t in range(P))]
    good, bad = load(files, P)
    allp = list(patterns(P, K))
    if cmd == 'indices':
        for i, p in enumerate(allp):
            if p in good: print(i)
        return
    def shifted(p, s): return ''.join(p[(t - s) % P] for t in range(P))
    direct = [p for p in allp if p in good]
    cov = [p for p in allp if p in good or any(shifted(p, s) in good for s in shifts)]
    unc = [p for p in allp if p not in set(cov)]
    print(f"patterns {len(allp)}, finished directly {len(direct)}, covered incl. shift-equivalents {len(cov)}, "
          f"NOT covered {len(unc)}, flagged (CAPPED/NOPERIOD/FEASIBLE/hit) {len(bad)}; shifts used {shifts}")
    if bad: print("flagged patterns:", *sorted(bad)[:20])
    sys.exit(0 if not unc and not bad else 1)
main()
