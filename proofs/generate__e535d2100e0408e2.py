#!/usr/bin/env python3
"""Generate finite data, checked independently by Lean's kernel."""
import gzip
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def step(i, w):
    A, B, C = i//100+10, (i//10)%10+9, i%10+9
    a, x, y = A-9, A+B-18, B+C-18
    lo, v = x//10, (y+w)//10
    z = (x+v)//10
    out = (2*a+z, x%10+(x+v)%10, (y+lo)%10+(y+w)%10)
    if a+z < 10 and 10 <= out[0] <= 18 and all(9 <= q <= 18 for q in out[1:]):
        return 100*(out[0]-10)+10*(out[1]-9)+out[2]-9
    return None


def main():
    table = [[step(i,w) for w in range(2)] for i in range(900)]
    ranks, active = {}, set()
    def rank(i):
        if i in ranks:
            return ranks[i]
        assert i not in active, 'cycle'
        active.add(i)
        ranks[i] = max([1+rank(j) for j in table[i] if j is not None] or [0])
        active.remove(i)
        return ranks[i]
    for i in range(900):
        rank(i)
    def tree(lo, hi):
        if len({ranks[i] for i in range(lo,hi)}) == 1:
            return str(ranks[lo])
        mid=(lo+hi)//2
        return f'(if i < {mid} then {tree(lo,mid)} else {tree(mid,hi)})'
    source='''import Std

namespace HighReturnRank

def next (i w : Nat) : Option Nat :=
  let A := i / 100 + 10
  let B := i / 10 % 10 + 9
  let C := i % 10 + 9
  let a := A - 9
  let x := A + B - 18
  let y := B + C - 18
  let lo := x / 10
  let v := (y + w) / 10
  let z := (x + v) / 10
  let U := 2 * a + z
  let V := x % 10 + (x + v) % 10
  let W := (y + lo) % 10 + (y + w) % 10
  if a + z < 10 ∧ 10 ≤ U ∧ U ≤ 18 ∧ 9 ≤ V ∧ V ≤ 18 ∧ 9 ≤ W ∧ W ≤ 18
  then some (100 * (U - 10) + 10 * (V - 9) + W - 9)
  else none

def rank (i : Nat) : Nat := RANKTREE

def checkVertex (i : Nat) : Bool :=
  decide (rank i ≤ 3) && (List.range 2).all (fun w =>
    match next i w with
    | none => true
    | some j => decide (j < 900 ∧ rank j < rank i))

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
theorem finite_check : (List.range 900).all checkVertex = true := by decide

theorem checked_vertex (i : Nat) (hi : i < 900) : checkVertex i = true := by
  exact (List.all_eq_true.mp finite_check) i (List.mem_range.mpr hi)

theorem rank_le_three (i : Nat) (hi : i < 900) : rank i ≤ 3 := by
  have h := (Bool.and_eq_true_iff.mp (checked_vertex i hi)).1
  exact of_decide_eq_true h

theorem edge_decreases (i w j : Nat) (hi : i < 900) (hw : w < 2)
    (he : next i w = some j) : j < 900 ∧ rank j < rank i := by
  have h := (Bool.and_eq_true_iff.mp (checked_vertex i hi)).2
  have hv := (List.all_eq_true.mp h) w (List.mem_range.mpr hw)
  rw [he] at hv
  exact of_decide_eq_true hv

theorem no_four_edges (a b c d e w x y z : Nat) (ha : a < 900)
    (hw : w < 2) (hx : x < 2) (hy : y < 2) (hz : z < 2)
    (hab : next a w = some b) (hbc : next b x = some c)
    (hcd : next c y = some d) (hde : next d z = some e) : False := by
  have h0 := rank_le_three a ha
  obtain ⟨hb, h1⟩ := edge_decreases a w b ha hw hab
  obtain ⟨hc, h2⟩ := edge_decreases b x c hb hx hbc
  obtain ⟨hd, h3⟩ := edge_decreases c y d hc hy hcd
  obtain ⟨_, h4⟩ := edge_decreases d z e hd hz hde
  omega

#print axioms finite_check
#print axioms checked_vertex
#print axioms rank_le_three
#print axioms edge_decreases
#print axioms no_four_edges

end HighReturnRank
'''.replace('RANKTREE',tree(0,900))
    (HERE/'HighReturnRank.lean').write_text(source)
    raw=(json.dumps({'rows':table,'ranks':[ranks[i] for i in range(900)]},separators=(',',':'))+'\n').encode()
    packed=gzip.compress(raw,mtime=0)
    (HERE/'finite_data.json.gz').write_bytes(packed)
    report={'vertices':900,'controls':1800,'accepted_edges':sum(j is not None for row in table for j in row),
            'rank_counts':{r:sum(v==r for v in ranks.values()) for r in sorted(set(ranks.values()))},
            'source_sha256':hashlib.sha256(source.encode()).hexdigest(),
            'compressed_sha256':hashlib.sha256(packed).hexdigest(),'raw_sha256':hashlib.sha256(raw).hexdigest(),
            'scope':'Generated data; Lean compilation and actual-orbit bridge are separate obligations.'}
    (HERE/'generation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
