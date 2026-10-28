#!/bin/sh
# Exact controls and all-48 independent replication, run from repository root.
set -eu
C=calculation/decimal_frontier/lattice_kinks/code
D=calculation/decimal_frontier/lattice_kinks/data
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT HUP INT TERM
c++ -O3 -std=c++17 "$C/rec2_t8_transfer.cpp" -o "$TMP/rec2_t8"
python3 "$C/rec2_t8_checker.py" "$D/lat2.txt" >"$TMP/python.txt"
ulimit -v 8388608 2>/dev/null || true
for J in $(seq 0 47); do
  nice -n 15 "$TMP/rec2_t8" "$D/rec2_t8_rows.txt" "$J" 2000000 >>"$TMP/cpp.txt"
done
python3 - "$D/lat2.txt" "$D/rec2_t8_rows.txt" "$TMP/cpp.txt" "$TMP/python.txt" <<'PY'
import sys,re
z=list(map(int,open(sys.argv[1]).read().split()))
p,nb,m,b=z[:4];assert (p,nb,m,b)==(8,11,48,10)
k=4+p;W=[z[k+t*m:k+(t+1)*m] for t in range(p)];k+=2*p*m
B=[z[k+t*nb:k+(t+1)*nb] for t in range(p)]
rows=[[W[t][j] for t in range(p)] for j in range(m)]
rows += [[B[t][j] for t in range(p)] for j in range(nb)]
assert rows==[list(map(int,l.split())) for l in open(sys.argv[2])]
print("CONTROL: committed spatial rows equal existing lat2.txt data")
cs={};j=None
for line in open(sys.argv[3]):
    h=re.match(r'j=(\d+) initial_variants=(\d+) first_defect_seeds=(\d+) unique_states=(\d+)',line)
    if h:
        j=int(h[1]);cs[j]=list(map(int,h.groups()[1:]));continue
    h=re.match(r'EXHAUSTED visited=(\d+)',line)
    if h:cs[j][2]=int(h[1])
ps={}
for line in open(sys.argv[4]):
    h=re.match(r'j=(\d+) initial=(\d+) first_defect=(\d+) visited=(\d+) edges=(\d+) cyclic=(\d+)',line)
    if h:ps[int(h[1])]=tuple(map(int,h.groups()[1:]))
assert len(cs)==len(ps)==48
for j in range(48):
    assert tuple(cs[j])==ps[j][:3],(j,cs[j],ps[j])
    assert ps[j][-1]==0
print("COMPUTED: 48/48 EXHAUSTED (no caps); C++ and independent Python agree")
print("TOTAL visited",sum(v[2] for v in ps.values()),
      "distinct directed edges",sum(v[3] for v in ps.values()))
PY
