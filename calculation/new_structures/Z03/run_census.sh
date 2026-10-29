#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$ROOT"
OUT="${TMPDIR:-/tmp}/z03-census"
mkdir -p "$OUT"
g++ -O3 -std=c++20 -march=native -Wall -Wextra calculation/new_structures/Z03/census.cpp -o "$OUT/census"
python3 calculation/new_structures/Z03/verify_bigint.py
for rank in 3 15 27; do
  "$OUT/census" --u-rank "$rank" --j-start 0 --j-limit 1000000 --out "$OUT/u${rank}_0_1m.tsv"
  "$OUT/census" --u-rank "$rank" --j-start 1000000 --j-limit 2000000 --out "$OUT/u${rank}_1m_2m.tsv"
  "$OUT/census" --u-rank "$rank" --j-start 2000000 --j-limit 2476099 --out "$OUT/u${rank}_2m_end.tsv"
done
python3 calculation/new_structures/Z03/summarize.py --input-dir "$OUT" --output calculation/new_structures/Z03/census_summary.tsv
