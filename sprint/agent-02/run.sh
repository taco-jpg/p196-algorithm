#!/usr/bin/env bash
# Reproduce every COMPUTED number of sprint/agent-02/REPORT.md.
# Run from the repository root. Needs gcc and python3 (3.13 used). Single-threaded.
# Memory: k<=7 < 1 GB; k=7 peel 3.2 GB; k=8 direct closure 4.3 GB; k=9 lifted closure 4.6 GB.
set -euo pipefail
S=sprint/agent-02
B=${BUILD:-/tmp/agent02-build}
D=${DATA:-/tmp/agent02-data}
mkdir -p "$B" "$D"
for t in fwdclosure prefixes peel scc bitstats liftclosure backclosure; do
  gcc -O2 -march=native -o "$B/$t" "$S/src/$t.c"
done
W=$(python3 -I "$S/src/orbit.py" 196 100)   # 3-.. column sums of orbit(196,100)
echo "w0 = $W"

# 1. Reproduce Agent #124's width-3 package byte for byte (needs the archive tag):
#    git fetch origin 'refs/tags/archive/2026-10-17/research/agent-124/*:refs/tags/archive/2026-10-17/research/agent-124/*'
python3 -I "$S/repro/gen_fwd_agent124.py" 3 "$D/w3" --leaf 512 > /dev/null
for f in lean/P196/Agent124ForwardInvariant/A124W3*.lean; do
  b=$(basename "$f")
  cmp -s <(sed 's/import P196.Agent124ForwardInvariant./import /; s/import P196.Agent117P2641./import /' "$f") "$D/w3/$b" \
    && echo "identical $b" || echo "DIFFERENT $b"
done

# 2. Forward closures F_k of 196 at time 100, k = 3..8 (direct bitset), excluded prefixes
for k in 3 4 5 6 7 8; do
  "$B/fwdclosure" $k "$D/F_k$k" "$W"
  for n in 3 4 5; do
    [ $n -le $k ] && "$B/prefixes" $k "$D/F_k$k.bits" $n "$D/excl_k${k}_n$n.txt"
  done
done

# 3. Recurrent part R_k (peeling of the positive abstraction graph) and comparison with F_k
for k in 3 4 5 6 7; do "$B/peel" $k "$D/F_k$k.bits" "$D/P_k$k"; done
# 4. Strong connectivity of R_k
for k in 3 4 5 6; do "$B/scc" $k "$D/P_k$k.R.bits"; done

# 5. Start-time / seed independence (k = 6, 7)
for spec in "196 1000" "196 10000" "89 20" "10911 40" "1186060307891929990 100"; do
  set -- $spec
  W2=$(python3 -I "$S/src/orbit.py" $1 $2)
  for k in 6 7; do
    "$B/fwdclosure" $k "$D/o" "$W2" > /dev/null
    cmp -s "$D/o.bits" "$D/F_k$k.bits" && echo "seed $1 t=$2 k=$k: same closure" || echo "seed $1 t=$2 k=$k: DIFFERENT"
  done
done

# 6. k = 9 by lifting over F_8 (4.6 GB), then the prefix census at k = 9
"$B/liftclosure" 8 "$D/F_k8.bits" "$D/L_k9" "$W"
for n in 3 4 5; do "$B/liftclosure" 8 "$D/F_k8.bits" "$D/L_k9" "$W" --prefixes $n "$D/excl_k9_n$n.txt"; done

# 7. Backward closures (exact inverse, long words) of the prefixes new at k = 8 and k = 9
for p in 2342 3749 3958 3986 4258 4347 4673 5967 6676 7383 7386 7699 7700 9137 9149 9523; do
  "$B/backclosure" 8 $p --cap 3000000; done
for p in 3537 3899 3984 4307 5838 6311 9123; do "$B/backclosure" 9 $p --cap 6000000; done
"$B/backclosure" 7 2641 --cap 2000000        # sanity: 25,624 nodes, rank 5

# 8. Real-orbit witness for 4456 (261-step seed)
python3 -I "$S/src/witness.py" "$D" 1186060307891929990 3 4 5 6 7 8
