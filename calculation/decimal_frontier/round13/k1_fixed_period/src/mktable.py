#!/usr/bin/env python3
# r13b: table of an eset2 log: usage mktable.py LOG [T]
import re, sys
cyc = {15: 9140287, 16: 19389807, 17: 40126496, 18: 80883639, 19: 160733468}
TC = r'trimmed\(Core\)'
lines = [l for l in open(sys.argv[1]) if re.match(r'K=\d+ T=\d+', l)]
print('| K | parents | parents kept | candidates | core (trim) | edges | anchor | closed src | **E(K,T)** | accepting | exact orbits | total s |')
print('|---|---|---|---|---|---|---|---|---|---|---|---|')
for l in lines:
    g = lambda k: re.search(k + r'=([0-9.e+]+)', l).group(1) if re.search(k + r'=([0-9.e+]+)', l) else '-'
    K = int(g('K'))
    e = int(g('E'))
    tot = re.search(r'total ([0-9.]+)s', l).group(1)
    print(f"| {K} | {g('parents')} | {g('parentsKept')} | {g('candidates')} | {g(TC)} | {g('edges')} | {g('anchor')} | {g('closedSources')} | {e:,} | {g('accepting')} | {g('exactOrbits')} | {tot} |")
