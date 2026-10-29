import P196.F1Semigroup.F1Power
/-!
Nilpotency-index histogram of the 258 diagonal-free reachable relations (kernel computation on the matrices;
`Mpowk M k` is the `k`-th relational power computed with `mmul`).
-/
namespace F1

def Mpowk (M : Rel) : Nat → Rel
  | 0 => initRel
  | k + 1 => mmul M (Mpowk M k)

/-- least `k ∈ 1..5` with `M^k = 0` (6 if none) -/
def nilIdx (M : Rel) : Nat :=
  if zeroRel (Mpowk M 1) then 1 else if zeroRel (Mpowk M 2) then 2 else if zeroRel (Mpowk M 3) then 3
  else if zeroRel (Mpowk M 4) then 4 else if zeroRel (Mpowk M 5) then 5 else 6

def hist (j : Nat) : Nat := ((List.range nS).filter fun i => !accQ i && nilIdx (Sget i) == j).length

theorem diag_free_count : ((List.range nS).filter fun i => !accQ i).length = 258 := by decide +kernel

theorem nilpotency_histogram : [hist 1, hist 2, hist 3, hist 4, hist 5, hist 6] = [1, 251, 4, 1, 1, 0] := by
  decide +kernel

end F1
