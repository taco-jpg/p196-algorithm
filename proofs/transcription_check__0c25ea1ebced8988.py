#!/usr/bin/env python3
"""Independent check (Agent #103): every BoundaryDataK literal table equals the
original string table under Lean's `(s.splitOn " ").filterMap String.toNat?`."""
import json, re, sys, hashlib
D = sys.argv[1]
orig = open(f'{D}/BoundaryData.lean').read()
kfile = open(f'{D}/BoundaryDataK.lean').read()

def to_nat(tok):  # Lean String.toNat?: nonempty, all chars '0'..'9' (no '_' in 4.19? be strict: digits only)
    return int(tok) if tok and all('0' <= c <= '9' for c in tok) else None

def parse_nats(s):
    return [v for v in (to_nat(t) for t in s.split(' ')) if v is not None]

O = {}
for name, kind, s in re.findall(r'^def (\w+) : (Graph|Array Nat) := parse(?:Graph|Nats) "([^"]*)"', orig, re.M):
    O[name] = (kind, parse_nats(s))
for name, kind in re.findall(r'^def (\w+) : (Graph|Array Nat) := parseNats "', orig, re.M):
    pass
# check the suffix used for Array tables in the original (toArray) and graph decode
arr_suffix = set(re.findall(r'^def \w+ : Array Nat := parseNats "[^"]*"\s*(\|>\.toArray|\.toArray)?', orig, re.M))
K = {}
for name, kind, body, tail in re.findall(r'^def (\w+)K : (Graph|Array Nat) := \(\[([^\]]*)\] : List Nat\)(.*)$', kfile, re.M):
    K[name] = (kind, [int(x) for x in body.split(',')] if body.strip() else [], tail.strip())
res = dict(original_tables=len(O), k_tables=len(K), mismatches=[], k_tails=sorted({v[2] for v in K.values()}),
           original_array_suffixes=sorted(arr_suffix))
assert set(O) == set(K), (set(O) ^ set(K))
for n in sorted(O):
    if O[n][0] != K[n][0] or O[n][1] != K[n][1]:
        res['mismatches'].append(n)
res['entries'] = sum(len(v[1]) for v in O.values())
res['status'] = 'PASS' if not res['mismatches'] else 'FAIL'
res['BoundaryData_sha256'] = hashlib.sha256(orig.encode()).hexdigest()
res['BoundaryDataK_sha256'] = hashlib.sha256(kfile.encode()).hexdigest()
print(json.dumps(res, indent=1))
