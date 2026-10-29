#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
CXX=${CXX:-g++}
"$CXX" -O3 -std=c++17 affine_rle_fast.cpp -lgmpxx -lgmp -o "$TMP/x05_affine_fast"
# Exact all-parameter symbolic certification; this must not sample A,B.
"$TMP/x05_affine_fast" 20000 20000 20000 0 > "$TMP/symbolic.log"
grep -Fx 'SYMBOLIC_ALL_PARAMETER_STEPS_OK 20000' "$TMP/symbolic.log"
# Whole-number GMP replay with exact pairword equality and palindrome tests
# at EVERY time slice; six 3000-step segments, then a 2000-step segment.
prev='-'
for end in 3000 6000 9000 12000 15000 18000 20000; do
  if [ "$end" -eq 20000 ]; then amount=2000; else amount=3000; fi
  next="$TMP/ckpt-$end.txt"
  "$TMP/x05_affine_fast" "$amount" 20000 20000 1 20000 20017 "$prev" "$next" > "$TMP/run-$end.log"
  grep -Fx "SYMBOLIC_ALL_PARAMETER_STEPS_OK $end" "$TMP/run-$end.log"
  prev="$next"
done
python3 - "$TMP" <<'PY'
import json,sys,pathlib,hashlib
root=pathlib.Path(sys.argv[1]); expected=json.load(open('evidence20k.json'))
for x in expected['checkpoints']:
    t=x['step'];p=root/f'ckpt-{t}.txt';head=p.read_text().splitlines()[0].split()
    assert int(head[0])==t
    assert hashlib.sha256(head[5].encode()).hexdigest()==x['gmp_decimal_sha256'],t
    assert hashlib.sha256(p.read_bytes()).hexdigest()==x['sha256_checkpoint'],t
    assert int(head[6])==x['symbolic_terms'],t
assert expected['full_gmp_replay_steps']==20000
print('X05_GMP_20K_ALL_PAIRWORDS_AND_SHA256_PASS')
PY
