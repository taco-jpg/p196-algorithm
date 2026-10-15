#!/usr/bin/env python3
"""Emit Agent124FourDigitSummary.lean collecting every four-digit class."""
import json, sys
metas = sys.argv[1:-1]
out = sys.argv[-1]
parts = []  # (namespace, module, nchunks, nprefixes)
for mp in metas:
    m = json.load(open(mp))
    tag = m['tag']
    n = len(m['prefixes']); ch = m['entries_per_chunk']
    parts.append((f'Agent124.Cert{tag}', f'A124{tag}Final', (n + ch - 1) // ch, n))
total = sum(p[3] for p in parts)
names = [(ns, i) for ns, _, nc, _ in parts for i in range(nc)]
L = []
L += [f'import {mod}' for _, mod, _, _ in parts]
L += ['', '/-! Summary of the four-digit prefix classes of Agent #124: every listed',
      'prefix has the stated ancestry bound, and the ordinary 196 orbit never contains a',
      'palindrome beginning with it. Restricted families only; no P196 claim. -/', '',
      'namespace Agent124.FourDigitSummary', 'open Lychrel196 Agent124.PrefixL', '',
      'theorem forall_mem_append {α : Type} {P : α → Prop} {a b : List α}',
      '    (ha : ∀ e ∈ a, P e) (hb : ∀ e ∈ b, P e) : ∀ e ∈ a ++ b, P e := by',
      '  intro e he',
      '  rcases List.mem_append.mp he with h | h',
      '  · exact ha e h',
      '  · exact hb e h', '']
def nest(items):
    if len(items) == 1:
        return items[0]
    return f'{items[0]} ++ ({nest(items[1:])})'
ents = [f'{ns}.entries{i:02d}' for ns, i in names]
L += ['/-- Every four-digit class of this contribution, as (digits, rank bound). -/',
      'def allEntries : List (List Nat × Nat) :=', '  ' + nest(ents), '',
      f'theorem allEntries_length : allEntries.length = {total} := by decide', '']
def proof(kind, items, arg=''):
    if len(items) == 1:
        return f'{items[0][0]}.{kind}_{items[0][1]:02d}{arg}'
    return f'forall_mem_append ({items[0][0]}.{kind}_{items[0][1]:02d}{arg}) ({proof(kind, items[1:], arg)})'
L += ['/-- Uniform ancestry bounds for every listed four-digit class. -/',
      'theorem ancestry_all : ∀ e ∈ allEntries, ∀ A P t, 0 < A →',
      '    PalStartsL e.1 P → orbit A t = P → t ≤ e.2 + 1 :=',
      '  ' + proof('ancestry', names), '',
      '/-- The ordinary 196 orbit never contains a palindrome beginning with a listed prefix. -/',
      'theorem no_196_all : ∀ t, ∀ e ∈ allEntries, ¬ PalStartsL e.1 (orbit 196 t) := fun t =>',
      '  ' + proof('no_196', names, ' t'), '',
      '#print axioms allEntries_length', '#print axioms ancestry_all', '#print axioms no_196_all',
      'end Agent124.FourDigitSummary', '']
open(out, 'w').write('\n'.join(L))
print(total, 'classes in', len(names), 'chunks')
