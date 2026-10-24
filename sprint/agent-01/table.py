"""Per-prefix table from the exact width-k computations (COMPUTED).
For every 4-digit prefix P: hitF_k (some digit word of F_k starts with P),
hitC_k (same for the infinite-history core C_k), first width k<=K at which P is
not hit, and whether noOverflowPre(P) holds (lead-one prefixes fail it)."""
import sys, os
here = os.path.dirname(os.path.abspath(__file__))
ks = [k for k in range(4, 11) if os.path.exists(f'{here}/out/peel{k}.tsv') or os.path.exists(f'{here}/out/L{k}.pre4')]
def no_overflow_pre(p):
    d = [int(c) for c in str(p)]
    return d[0] >= 2 or any(x >= 3 for x in d)
hitF, hitC = {}, {}
for k in ks:
    if os.path.exists(f'{here}/out/peel{k}.tsv'):
        rows = [l.split() for l in open(f'{here}/out/peel{k}.tsv')]
        hitF[k] = {int(r[0]): int(r[1]) for r in rows}
        hitC[k] = {int(r[0]): int(r[2]) for r in rows}
    else:
        s = open(f'{here}/out/L{k}.pre4').read()
        hitF[k] = {1000 + i: int(ch) for i, ch in enumerate(s)}
print('widths available:', ks)
for k in ks:
    nF = sum(hitF[k].values()); nC = sum(hitC[k].values()) if k in hitC else None
    diff = sum(1 for p in hitF[k] if k in hitC and hitF[k][p] != hitC[k][p]) if k in hitC else None
    print(f'k={k}: prefixes hit by F_k = {nF}, by C_k = {nC}, disagreements F vs C = {diff}')
first = {}
for p in range(1000, 10000):
    first[p] = next((k for k in ks if not hitF[k][p]), None)
    # monotonicity check: once not hit, never hit again at larger k
    seen_off = False
    for k in ks:
        if not hitF[k][p]: seen_off = True
        elif seen_off: print('MONOTONICITY VIOLATION', p, k)
lead = [p for p in range(1000, 10000) if not no_overflow_pre(p)]
print('lead-one prefixes (noOverflowPre false):', len(lead))
cum = 0
for k in ks:
    newly = [p for p in range(1000, 10000) if first[p] == k and no_overflow_pre(p)]
    newly_lead = [p for p in lead if first[p] == k]
    cum += len(newly)
    print(f'  first excluded at k={k}: {len(newly)} (noOverflowPre)  cumulative {cum}  [+{len(newly_lead)} lead-one, not usable]')
open_ = [p for p in range(1000, 10000) if first[p] is None and no_overflow_pre(p)]
open_lead = [p for p in lead if first[p] is None]
print(f'hit at every width {ks[0]}..{ks[-1]}: {len(open_)} noOverflowPre + {len(open_lead)} lead-one')
with open(f'{here}/out/prefix_table.tsv', 'w') as f:
    f.write('prefix\tnoOverflowPre\t' + '\t'.join(f'hitF{k}' for k in ks) + '\tfirst_excluded_k\n')
    for p in range(1000, 10000):
        f.write(f'{p}\t{int(no_overflow_pre(p))}\t' + '\t'.join(str(hitF[k][p]) for k in ks) + f'\t{first[p] or "-"}\n')
