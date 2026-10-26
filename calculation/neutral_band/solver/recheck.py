#!/usr/bin/env python3
"""python3 recheck.py FOUND.jsonl  -> re-verify every SAT with the mirror's cycleOK and print the Lean Edge list."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import p196cp as P
L = lambda x: "[" + ", ".join(map(str, x)) + "]"
for line in open(sys.argv[1]):
    r = json.loads(line); b = r["base"]; c = r["cert"]
    es = [(e[0], e[1], e[2], e[3], e[4], e[5]) for e in c["edges"]]
    ok = P.mirror.cycleOK(b, es, c["start_B"], c["start_C"])
    print(f"base {b} p={len(es)} schedule={r['S']} mirror cycleOK={ok} sum_gam={c['sum_gam']} sum_gain={c['sum_gain']}")
    print(f"def certB{b} : List Edge := [")
    print(",\n".join(f"  ⟨{L(e[0])}, {L(e[1])}, {L(e[2])}, {L(e[3])}, {e[4]}, {e[5]}⟩" for e in es) + "]")
    print(f"-- Lean check: cycleOK {b} certB{b} {L(c['start_B'])} {L(c['start_C'])} = true   (by decide / rfl)")
