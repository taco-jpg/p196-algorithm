#!/bin/sh
# Exact two-engine exhaustive replay and independent arithmetic controls.
# Run from root: sh calculation/decimal_frontier/lattice_kinks/code/rec2_t24_run.sh
set -eu
C=calculation/decimal_frontier/lattice_kinks/code
D=calculation/decimal_frontier/lattice_kinks/data
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT HUP INT TERM
python3 "$C/rec2_t24_controls.py" "$D/lat2.txt" "$D/rec2_t24_rows.txt"
c++ -O3 -std=c++17 "$C/rec2_t24_raw.cpp" -o "$TMP/raw"
c++ -O3 -std=c++17 "$C/rec2_t24_kahn.cpp" -o "$TMP/kahn"
ulimit -v 8388608 2>/dev/null || true
for j in $(seq 0 47); do
  printf 'BEGIN j=%s\n' "$j" >>"$TMP/raw.txt"
  nice -n 15 "$TMP/raw" "$D/rec2_t24_rows.txt" "$j" 3000000 >>"$TMP/raw.txt"
  printf 'END j=%s\n' "$j" >>"$TMP/raw.txt"
  nice -n 15 "$TMP/kahn" "$D/rec2_t24_rows.txt" "$j" 3000000 >>"$TMP/kahn.txt"
done
python3 - "$TMP/raw.txt" "$TMP/kahn.txt" <<'PY'
import sys,re
raw=open(sys.argv[1]).read()
kahn=open(sys.argv[2]).read()
assert 'CAP=' not in raw and 'FOUND' not in raw and 'CAP=' not in kahn
assert len(re.findall(r'^END j=',raw,re.M))==48
A={}
for jj,out in re.findall(r'BEGIN j=(\d+)\n(.*?)END j=\1',raw,re.S):
    j=int(jj)
    if 'EXHAUSTED visited=' in out:
        mt=re.search(r'EXHAUSTED visited=(\d+) edges=(\d+)',out)
        assert mt
        A[j]=(int(mt[1]),int(mt[2]))
    else:
        assert 'unique_states=0' in out,(j,out)
        A[j]=(0,0)
B={}
for line in kahn.splitlines():
    mt=re.fullmatch(r'j=(\d+) boundary=(\d+) seeds=(\d+) unique_roots=(\d+) reachable=(\d+) edges=(\d+) cyclic_core=(\d+)',line)
    assert mt,line
    j=int(mt[1]);B[j]=tuple(map(int,mt.groups()[1:]))
assert len(A)==len(B)==48
assert all(v[-1]==0 for v in B.values())
assert (sum(v[0] for v in A.values()),sum(v[1] for v in A.values()))==(10393040,8273248)
assert (sum(v[3] for v in B.values()),sum(v[4] for v in B.values()))==(3466248,2758832)
# The order-three time-shift quotient has 1 or 3 states per orbit.
assert all(B[j][3]<=A[j][0]<=3*B[j][3] for j in A)
print('COMPUTED: raw T=24 stationary rec2 all 48 EXHAUSTED; 10,393,040 states, 8,273,248 edges')
print('CONTROL: independent shift-8 quotient Kahn core empty 48/48; 3,466,248 states, 2,758,832 edges')
PY
