#!/usr/bin/env bash
# Repeatable, bounded non-Lean regression for bauto6's packed key, candidate
# quota and directed path/cycle serialization.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
CXX="${CXX:-g++}"
"$CXX" -O2 -std=c++17 "$HERE/bauto6.cpp" -o "$TMP/bauto6"
cat > "$TMP/key_roundtrip.cpp" <<'CPP'
#define main bauto6_unused_main
#include "bauto6.cpp"
#undef main
#include <cassert>
#include <cstdio>
int main() {
  b = 10; p = 48; ng = 24; ydig = 4;
  const u64 mask = (1ULL << 48) - 1;
  u64 rng = 0xB734DEADBEEFULL;
  for (int round = 0; round < 1024; round++) {
    rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
    const u64 L = rng & mask;
    rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
    const u64 H = rng & mask;
    int Y[64] = {};
    for (int i = 0; i < ng; i++) Y[i] = (i * 7 + round) % b;
    Y[23] = (round & 1) ? 9 : 0; // exercise both values of bit 191
    const Key k = pack(L, H, Y);
    assert(bool(k.w[2] & (1ULL << 63)) == bool(round & 1));
    u64 LR = 0, HR = 0; int YR[64] = {};
    unpack(k, LR, HR, YR);
    assert(LR == L && HR == H);
    for (int i = 0; i < ng; i++) assert(YR[i] == Y[i]);
  }
  puts("KEY192 PASS 1024 round-trips, bit191 both values");
}
CPP
"$CXX" -O2 -std=c++17 -I"$HERE" "$TMP/key_roundtrip.cpp" -o "$TMP/key_roundtrip"
"$TMP/key_roundtrip"

(ulimit -v 8000000; nice -n 19 "$TMP/bauto6" 10 48 48 -g "$(printf '01%.0s' {1..24})" -cap 1 -maxlen 1) > "$TMP/bit192.txt"
grep -q '^CAPPED p=48 ' "$TMP/bit192.txt"
grep -q 'skipped=0' "$TMP/bit192.txt"

(ulimit -v 8000000; nice -n 19 "$TMP/bauto6" 13 10 10 -g 1010010000 -cap 350000) > "$TMP/b13.txt"
grep -q '^CYC p=10 g=1010010000 S=3 minc=1 depth=55 states=250302 capped=0 ' "$TMP/b13.txt"
python3 "$HERE/verify_bauto6_witness.py" 13 "$TMP/b13.txt"

(ulimit -v 8000000; nice -n 19 "$TMP/bauto6" 9 10 10 -g 1100011000 -cap 1200000) > "$TMP/b9.txt"
grep -q '^CYC p=10 g=1100011000 S=4 minc=1 depth=46 states=956310 capped=0 ' "$TMP/b9.txt"
python3 "$HERE/verify_bauto6_witness.py" 9 "$TMP/b9.txt"

(ulimit -v 8000000; nice -n 19 "$TMP/bauto6" 13 10 10 -g 1010010000 -cap 350000 -maxcand 0) > "$TMP/cap0.txt"
grep -q '^CAPPED p=10 g=1010010000 ' "$TMP/cap0.txt"
grep -q 'capped=1 short_cycle_streams=0 skipped=0' "$TMP/cap0.txt"

(ulimit -v 8000000; nice -n 19 "$TMP/bauto6" 13 10 10 -g 1010010000 -cap 350000 -maxcand 100) > "$TMP/cap100.txt"
grep -q '^CYC_PARTIAL p=10 g=1010010000 S=3 len_upper_bound=1 depth=55 ' "$TMP/cap100.txt"
python3 "$HERE/verify_bauto6_witness.py" 13 "$TMP/cap100.txt"
echo 'ALL BAUTO6 CORRECTNESS TESTS PASSED'
