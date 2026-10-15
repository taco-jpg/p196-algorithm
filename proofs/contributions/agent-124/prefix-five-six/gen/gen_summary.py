#!/usr/bin/env python3
"""Emit Agent124PrefixSummary.lean collecting every class of this contribution."""
import json, sys
k5 = json.load(open(sys.argv[1]))['bounds_ancestry']
k6 = json.load(open(sys.argv[2]))['bounds_ancestry']
out = sys.argv[3]
entries = []
for pre, B in sorted(list(k5.items()) + list(k6.items())):
    ns = 'CertK5' if pre in k5 else 'CertK6'
    entries.append((pre, B, ns))
lines = ['import A124K5Final', 'import A124K5Final119', 'import A124K6Final', '',
         '/-! Summary of the 33 three-digit prefix classes of Agent #124.',
         'Each entry `(a, b, c, B)` carries an ancestry bound `B`; every bound is at most 40,',
         'within the kernel-checked first 100 iterates of 196. No P196 claim. -/', '',
         'namespace Agent124.PrefixSummary', 'open Lychrel196 Agent124.PrefixK', '',
         '/-- `(a, b, c, B)`: palindromes beginning `a b c` are reached within `B` steps. -/',
         'def classes : List (Nat × Nat × Nat × Nat) :=']
lines.append('  [' + ',\n   '.join(f'({p[0]}, {p[1]}, {p[2]}, {B})' for p, B, _ in entries) + ']')
lines += ['', 'theorem classes_length : classes.length = %d := rfl' % len(entries), '']
n = len(entries)
pat = ' | '.join(['rfl'] * n)
lines += ['/-- Uniform ancestry bounds for every listed class. -/',
          'theorem ancestry_all : ∀ e ∈ classes, ∀ A P t, 0 < A →',
          '    PalStarts3 e.1 e.2.1 e.2.2.1 P → orbit A t = P → t ≤ e.2.2.2 := by',
          '  intro e he',
          '  simp only [classes, List.mem_cons, List.not_mem_nil, or_false] at he',
          f'  rcases he with {pat}']
for p, B, ns in entries:
    lines.append(f'  · exact Agent124.{ns}.ancestry_{p}')
lines += ['', '/-- The ordinary 196 orbit never contains a palindrome of any listed class. -/',
          'theorem no_196_all : ∀ t, ∀ e ∈ classes, ¬ PalStarts3 e.1 e.2.1 e.2.2.1 (orbit 196 t) := by',
          '  intro t e he',
          '  simp only [classes, List.mem_cons, List.not_mem_nil, or_false] at he',
          f'  rcases he with {pat}']
for p, B, ns in entries:
    lines.append(f'  · exact Agent124.{ns}.no_196_{p} t')
lines += ['', '#print axioms classes_length', '#print axioms ancestry_all', '#print axioms no_196_all',
          'end Agent124.PrefixSummary', '']
open(out, 'w').write('\n'.join(lines))
print(n, 'classes')
