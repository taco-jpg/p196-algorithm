#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
c++ -O3 -std=c++17 universe.cpp -o /tmp/n17_universe
c++ -O3 -std=c++17 universe_gmp.cpp -lgmp -o /tmp/n17_universe_gmp
/tmp/n17_universe >/tmp/n17_universe_classes.csv
/tmp/n17_universe_gmp >/tmp/n17_universe_gmp_summary.txt
head -n 1 /tmp/n17_universe_classes.csv
cat /tmp/n17_universe_gmp_summary.txt
python3 - <<'PY'
from pathlib import Path
a=Path("/tmp/n17_universe_classes.csv").read_text().splitlines()
b=Path("/tmp/n17_universe_gmp_summary.txt").read_text()
assert len(a)==28 and sum(int(row.split(",")[0]) for row in a[1:])==361
for value in ("T=1500","minfront=157","last_44_failure=715"):
    assert value in a[0] and value in b,value
for value in ("late_checks=283385","distinct_heads_at_800=27"):
    assert value in a[0],value
for value in ("complete_late_checks=283385","distinct_head800=27"):
    assert value in b,value
assert "palfail=-1 oddfail=-1 overflowfail=-1" in a[0]
assert "badpal=-1 badodd=-1 badgamma=-1" in b
print("PASS: two independent complete 361-case engines and all controls.")
PY
