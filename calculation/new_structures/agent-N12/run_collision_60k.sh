#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
"${CXX:-g++}" -std=c++17 -O3 "$HERE/seed_cones.cpp" -o "$TMP/digit"
"${CXX:-g++}" -std=c++17 -O3 "$HERE/chunk_bigint_replay.cpp" -o "$TMP/bigint"
"$TMP/digit" 39 31000 43 60000 0 "$TMP/digit.csv"
"$TMP/bigint" 39 31000 43 60000 0 "$TMP/bigint.csv"
cmp "$TMP/digit.csv" "$TMP/bigint.csv"
ACTUAL="$(sha256sum "$TMP/digit.csv" | cut -d' ' -f1)"
test "$ACTUAL" = 6e0a9285178df82218b6529e59bef201fa139e1bfc13640a5ef7579fdbce6854
"$TMP/digit" 39 31001 43 51465 0 "$TMP/padded.csv"
python3 - "$TMP/digit.csv" "$TMP/padded.csv" "$HERE/checkpoints_60k.csv" <<'PY'
import csv,sys
base=list(csv.DictReader(open(sys.argv[1])))
pad=list(csv.DictReader(open(sys.argv[2])))
assert len(base)==60001 and len(pad)==51466
for row in csv.DictReader(open(sys.argv[3])):
    actual=base[int(row['t'])]
    for key in ('length','width','central_zeros','mismatch'):
        assert actual[key]==row[key],(row,key)
assert min(int(r['central_zeros']) for r in base[:50001])==878
assert all(int(r['central_zeros'])>0 for r in base[:51464])
assert base[51464]['central_zeros']=='0'
for i in range(51465):
    a,b=base[i],pad[i]
    assert int(b['length'])==int(a['length'])+1
    assert int(b['central_zeros'])==int(a['central_zeros'])+1
    assert a['width']==b['width']
    assert a['mismatch']==b['mismatch']
    assert a['first16pairs']==b['first16pairs']
a,b=base[51465],pad[51465]
assert int(b['width'])!=int(a['width'])
assert b['central_zeros']=='0' and a['central_zeros']=='1'
print('FIRST_ZERO_CORRIDOR_COLLISION=51464')
print('FIRST_PADDING_TRACE_DIVERGENCE=51465')
print('AGENT_N12_60K_COLLISION_PASS')
PY
