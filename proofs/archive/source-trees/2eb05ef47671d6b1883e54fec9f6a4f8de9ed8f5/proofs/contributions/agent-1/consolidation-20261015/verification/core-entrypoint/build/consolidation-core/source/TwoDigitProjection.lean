import LychrelDigitSums

/-!
# Agent #113: exact three-column prefix projection, every width at least three

For a canonical decimal numeral of width `L ≥ 3` with pair-sum word
`q = columnSum d L`, the three outermost pair sums of the canonical
representation of `step n` are a fixed finite function `nextTriple` of
`q 0, q 1, q 2` and the single actual carry `carry q (L - 3)` entering column
`L - 3`. Both the no-overflow (same width) and the overflow (width `L + 1`)
branches are covered. Overlapping widths `3 ≤ L < 6` need no special case:
every formula below is an identity about the actual computed carries.

This module proves semantics only. It makes no claim about 196 or about
decimal Lychrel existence.
-/

namespace Agent113.TwoDigit

open DecimalDigits FoldedDecimal

/-! ## The finite three-column update -/

/-- Carry into column `L - 2`, given the third pair sum and the carry `e`
entering column `L - 3`. -/
def hiCarry2 (s2 e : Nat) : Nat := (s2 + e) / 10

/-- Carry into column `L - 1`. -/
def hiCarry1 (s1 s2 e : Nat) : Nat := (s1 + hiCarry2 s2 e) / 10

/-- Final carry out of column `L - 1`: one exactly in the overflow branch. -/
def topCarry (s0 s1 s2 e : Nat) : Nat := (s0 + hiCarry1 s1 s2 e) / 10

/-- The outer three pair sums of the next state. Triples are listed from
the outside in; they are not three-digit integers. -/
def nextTriple (s0 s1 s2 e : Nat) : Nat × Nat × Nat :=
  if topCarry s0 s1 s2 e = 0 then
    (s0 % 10 + (s0 + hiCarry1 s1 s2 e) % 10,
     (s1 + s0 / 10) % 10 + (s1 + hiCarry2 s2 e) % 10,
     (s2 + (s1 + s0 / 10) / 10) % 10 + (s2 + e) % 10)
  else
    (s0 % 10 + 1,
     (s1 + s0 / 10) % 10 + (s0 + hiCarry1 s1 s2 e) % 10,
     (s2 + (s1 + s0 / 10) / 10) % 10 + (s1 + hiCarry2 s2 e) % 10)

/-! ## Small carry identities -/

theorem carry_one (q : Nat → Nat) : carry q 1 = q 0 / 10 := by
  simp [carry]

theorem carry_two (q : Nat → Nat) : carry q 2 = (q 1 + q 0 / 10) / 10 := by
  simp [carry]

theorem carry_succ (q : Nat → Nat) (i : Nat) :
    carry q (i + 1) = (q i + carry q i) / 10 := rfl

/-- The pair-sum word is symmetric; normalized index form for width `k + 3`. -/
theorem sym0 (d : Nat → Nat) (k : Nat) :
    columnSum d (k + 3) (k + 2) = columnSum d (k + 3) 0 := by
  have h := columnSum_symmetric d (k + 3) 0 (by omega)
  have hi : k + 3 - 1 - 0 = k + 2 := by omega
  rw [hi] at h
  exact h.symm

theorem sym1 (d : Nat → Nat) (k : Nat) :
    columnSum d (k + 3) (k + 1) = columnSum d (k + 3) 1 := by
  have h := columnSum_symmetric d (k + 3) 1 (by omega)
  have hi : k + 3 - 1 - 1 = k + 1 := by omega
  rw [hi] at h
  exact h.symm

theorem sym2 (d : Nat → Nat) (k : Nat) :
    columnSum d (k + 3) k = columnSum d (k + 3) 2 := by
  have h := columnSum_symmetric d (k + 3) 2 (by omega)
  have hi : k + 3 - 1 - 2 = k := by omega
  rw [hi] at h
  exact h.symm

/-- The actual high-end carries, in terms of the outer three pair sums and
the carry entering column `L - 3 = k`. -/
theorem high_carries (d : Nat → Nat) (k : Nat) :
    let q := columnSum d (k + 3)
    carry q (k + 1) = hiCarry2 (q 2) (carry q k) ∧
    carry q (k + 2) = hiCarry1 (q 1) (q 2) (carry q k) ∧
    carry q (k + 3) = topCarry (q 0) (q 1) (q 2) (carry q k) := by
  intro q
  have e1 : carry q (k + 1) = hiCarry2 (q 2) (carry q k) := by
    rw [carry_succ, hiCarry2, show q k = q 2 from sym2 d k]
  have e2 : carry q (k + 2) = hiCarry1 (q 1) (q 2) (carry q k) := by
    rw [show k + 2 = (k + 1) + 1 from rfl, carry_succ, e1, hiCarry1,
      show q (k + 1) = q 1 from sym1 d k]
  have e3 : carry q (k + 3) = topCarry (q 0) (q 1) (q 2) (carry q k) := by
    rw [show k + 3 = (k + 2) + 1 from rfl, carry_succ, e2, topCarry,
      show q (k + 2) = q 0 from sym0 d k]
  exact ⟨e1, e2, e3⟩

/-! ## The projection in both branches -/

/-- No-overflow branch: the canonical next word is `output q` of width
`k + 3`; its outer three pair sums are `nextTriple`. -/
theorem triple_no_overflow (d : Nat → Nat) (k : Nat)
    (hc : carry (columnSum d (k + 3)) (k + 3) = 0) :
    let q := columnSum d (k + 3)
    (columnSum (output q) (k + 3) 0, columnSum (output q) (k + 3) 1,
      columnSum (output q) (k + 3) 2) =
      nextTriple (q 0) (q 1) (q 2) (carry q k) := by
  intro q
  obtain ⟨e1, e2, e3⟩ := high_carries d k
  have htop : topCarry (q 0) (q 1) (q 2) (carry q k) = 0 := by
    rw [← e3]; exact hc
  have i0 : k + 3 - 1 - 0 = k + 2 := by omega
  have i1 : k + 3 - 1 - 1 = k + 1 := by omega
  have i2 : k + 3 - 1 - 2 = k := by omega
  simp only [nextTriple, htop, if_true, columnSum, reflected, i0, i1, i2,
    output, e1, e2, carry_one, carry_two, carry]
  rw [show q (k + 2) = q 0 from sym0 d k, show q (k + 1) = q 1 from sym1 d k,
    show q k = q 2 from sym2 d k]
  simp [hiCarry1, hiCarry2]

/-- Overflow branch: the canonical next word is `extended q (k + 3)` of
width `k + 4`; its outer three pair sums are again `nextTriple`. -/
theorem triple_overflow (d : Nat → Nat) (k : Nat)
    (hc : carry (columnSum d (k + 3)) (k + 3) = 1) :
    let q := columnSum d (k + 3)
    (columnSum (extended q (k + 3)) (k + 4) 0,
      columnSum (extended q (k + 3)) (k + 4) 1,
      columnSum (extended q (k + 3)) (k + 4) 2) =
      nextTriple (q 0) (q 1) (q 2) (carry q k) := by
  intro q
  have hc' : carry q (k + 3) = 1 := hc
  obtain ⟨e1, e2, e3⟩ := high_carries d k
  have htop : topCarry (q 0) (q 1) (q 2) (carry q k) = 1 := by
    rw [← e3]; exact hc
  have htop' : ¬ topCarry (q 0) (q 1) (q 2) (carry q k) = 0 := by omega
  have i0 : k + 4 - 1 - 0 = k + 3 := by omega
  have i1 : k + 4 - 1 - 1 = k + 2 := by omega
  have i2 : k + 4 - 1 - 2 = k + 1 := by omega
  have l0 : (0 : Nat) < k + 3 := by omega
  have l1 : (1 : Nat) < k + 3 := by omega
  have l2 : (2 : Nat) < k + 3 := by omega
  have l3 : ¬ (k + 3 < k + 3) := by omega
  have l4 : k + 2 < k + 3 := by omega
  have l5 : k + 1 < k + 3 := by omega
  simp only [nextTriple, htop', if_false, columnSum, reflected, i0, i1, i2,
    extended, l0, l1, l2, l3, l4, l5, if_true, output, hc', e1, e2,
    carry_one, carry_two]
  rw [show q (k + 2) = q 0 from sym0 d k, show q (k + 1) = q 1 from sym1 d k]
  have e1' : carry q (k + 1) = hiCarry2 (q 2) (carry q k) := e1
  have e2' : carry q (k + 2) = hiCarry1 (q 1) (q 2) (carry q k) := e2
  simp only [Prod.mk.injEq]
  refine ⟨by simp [carry], ?_, ?_⟩
  · rw [e2']
  · rw [e1']

end Agent113.TwoDigit
