#!/usr/bin/env bash
# Reproduce every COMPUTED number in sprint/agent-03/REPORT.md.
# Usage: sprint/agent-03/run_all.sh [WORKDIR] [KMAX_DIRECT] [KMAX_LIFT]
#   WORKDIR      scratch directory for binaries and bitsets (default: ./a3work)
#   KMAX_DIRECT  largest width computed with a full 19^k bitset (default 8; needs ~4.2 GB at k=8)
#   KMAX_LIFT    largest width computed by lifting (default 9; k=9 needs ~4.6 GB, k=10 needs a
#                full F_9 bitset of 40 GB: run with KMAX_DIRECT=9 on a large machine)
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
W="${1:-./a3work}"; KD="${2:-8}"; KL="${3:-9}"
if [ "$KL" -gt $((KD + 1)) ]; then echo "KMAX_LIFT must be <= KMAX_DIRECT + 1 (lifting reads a full bitset)"; exit 1; fi
mkdir -p "$W"; cd "$W"
CC="${CC:-cc}"; FLAGS="-O3 -march=native"
for p in orbit196 fwdbfs settool peel scc fwdlift; do $CC $FLAGS -o $p "$HERE/$p.c"; done

echo "== 1. reference model self-test (forward == converse of prefixPredecessors; integer soundness)"
python3 "$HERE/fwdref.py"

echo "== 2. orbit of 196 to t = 200000 (outer columns, inner carries, mod 99, palindrome flag)"
./orbit196 3000 > orb3000.txt && python3 "$HERE/chk_orbit.py" orb3000.txt
./orbit196 200000 > orb200k.txt
awk '$5==1' orb200k.txt | wc -l | sed 's/^/palindromes found: /'
W100=$(awk '$1==100{print $6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17}' orb200k.txt)
echo "w(196,100) = $W100"
word() { echo $W100 | cut -d' ' -f1-"$1"; }

echo "== 3. plain forward closures F_k from 196 at t = 100"
for k in $(seq 3 "$KD"); do ./fwdbfs $k none F${k}.bin $(word $k); done
python3 "$HERE/chk_bfs.py"

echo "== 4. enrichments (soundness checked along the orbit t = 100..200000), k = 3..6"
for k in 3 4 5 6; do
  python3 "$HERE/gen_tables.py" orb200k.txt 100 $k tables_k$k > /dev/null
  for t in lmod2 lmod3 lmod4 lmod5 lmod6 lmod7 lmod8 lmod10 lmod12 r99p r11p r9 clock6 preve prevbe combo; do
    [ $k = 6 ] && [ $t = combo ] && continue
    out=$(./fwdbfs $k tables_k$k/$t.tbl P.bin $(word $k))
    cmp -s P.bin F$k.bin && same=yes || same=NO
    echo "$out | $t projection_equals_F_k=$same"
  done
done
rm -f P.bin

echo "== 5. infinite-rank region R_k (Kahn peeling of the full graph) vs F_k, SCC of w(196,100)"
for k in $(seq 3 $(( KD < 7 ? KD : 7 ))); do
  ./peel $k R$k.bin | head -1
  ./settool diff F$k.bin R$k.bin $k
  ./scc $k F$k.bin S$k.bin D$k.bin $(word $k)
done
python3 "$HERE/entry_and_cycle.py" $(seq 3 $(( KD < 7 ? KD : 7 )))
# k >= 8: is w(196,100) on a cycle?  (closure from w(196,101) must contain w(196,100))
W101=$(awk '$1==101{print $6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17}' orb200k.txt)
for k in $(seq 8 "$KL"); do
  QUERY="$(word $k)" ./fwdlift $((k-1)) F$((k-1)).bin /dev/null $(echo $W101 | cut -d' ' -f1-$k) | grep -E "K\+1|QUERY"
done

echo "== 6. width refinement: pi_k F_{k+1} vs F_k, excluded prefixes"
for k in $(seq 4 "$KD"); do
  ./settool proj F$k.bin $k Pr.bin; ./settool diff F$((k-1)).bin Pr.bin $((k-1)); rm -f Pr.bin
  ./settool excl F$k.bin $k excl4_k$k.txt
done
for k in $(seq $((KD + 1)) "$KL"); do
  ./fwdlift $((k-1)) F$((k-1)).bin excl4_k$k.txt $(word $k)
done

echo "== 7. no-guard realizations"
python3 "$HERE/realize.py" F3.bin 3
for k in 4 5 6 7; do [ -f F$k.bin ] && python3 "$HERE/realize.py" F$k.bin $k 2000; done
echo done
