#!/bin/sh
set -eu
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
TMP=$(printenv TMPDIR 2>/dev/null || echo /tmp)
c++ -O3 -std=c++17 "$HERE/symbolic_search.cpp" -o "$TMP/w42_symbolic_search"
c++ -O3 -std=c++17 "$HERE/integer_replay.cpp" -o "$TMP/w42_integer_replay"

# Exact affine symbolic search: all mod-11-admissible J words, split into bounded chunks.
"$TMP/w42_symbolic_search" 3 0 6859
"$TMP/w42_symbolic_search" 4 0 30000
"$TMP/w42_symbolic_search" 4 30000 60000
"$TMP/w42_symbolic_search" 4 60000 90000
"$TMP/w42_symbolic_search" 4 90000 120000
"$TMP/w42_symbolic_search" 4 120000 130321

# Independent ordinary decimal digit-vector arithmetic at all four required widths.
for q in 20 40 80 160; do
  "$TMP/w42_integer_replay" "$q" "$q"
done

# Independent Python unbounded-integer engine.
python3 "$HERE/bigint_replay.py"
