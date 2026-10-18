import P196.Foundations.LychrelDigitSums

/-!
# Agent #113: exact four-column prefix projection, every width at least four

For a canonical decimal numeral of width `L ≥ 4` with pair-sum word
`q = columnSum d L`, the four outermost pair sums of the canonical next
numeral (`output q` of width `L` without overflow, `extended q L` of width
`L + 1` with overflow) are a fixed function `nextQuad` of `q 0, q 1, q 2, q 3`
and the single actual carry `carry q (L - 4)`. Overlapping widths `4 ≤ L < 8`
need no special case. This is the four-column analogue of
`Agent113.TwoDigit.triple_no_overflow` / `triple_overflow`.

Semantics only; no claim about 196 or decimal Lychrel existence.
-/

namespace Agent113.FourColumn

open DecimalDigits FoldedDecimal

/-! ## The finite four-column update -/

/-- Carries entering the high columns `L-3, L-2, L-1`, and the final carry,
from the outer pair sums and the carry `e` entering column `L - 4`. -/
def hc3 (s3 e : Nat) : Nat := (s3 + e) / 10
def hc2 (s2 s3 e : Nat) : Nat := (s2 + hc3 s3 e) / 10
def hc1 (s1 s2 s3 e : Nat) : Nat := (s1 + hc2 s2 s3 e) / 10
def top4 (s0 s1 s2 s3 e : Nat) : Nat := (s0 + hc1 s1 s2 s3 e) / 10

/-- Carries entering the low columns 1, 2, 3. -/
def lc1 (s0 : Nat) : Nat := s0 / 10
def lc2 (s0 s1 : Nat) : Nat := (s1 + lc1 s0) / 10
def lc3 (s0 s1 s2 : Nat) : Nat := (s2 + lc2 s0 s1) / 10

abbrev Quad := Nat × Nat × Nat × Nat

/-- The outer four pair sums of the next state, outermost first. -/
def nextQuad (s0 s1 s2 s3 e : Nat) : Quad :=
  if top4 s0 s1 s2 s3 e = 0 then
    (s0 % 10 + (s0 + hc1 s1 s2 s3 e) % 10,
     (s1 + lc1 s0) % 10 + (s1 + hc2 s2 s3 e) % 10,
     (s2 + lc2 s0 s1) % 10 + (s2 + hc3 s3 e) % 10,
     (s3 + lc3 s0 s1 s2) % 10 + (s3 + e) % 10)
  else
    (s0 % 10 + 1,
     (s1 + lc1 s0) % 10 + (s0 + hc1 s1 s2 s3 e) % 10,
     (s2 + lc2 s0 s1) % 10 + (s1 + hc2 s2 s3 e) % 10,
     (s3 + lc3 s0 s1 s2) % 10 + (s2 + hc3 s3 e) % 10)

/-! ## Carries and digits of an actual word of width `k + 4` -/

theorem carry_succ (q : Nat → Nat) (i : Nat) :
    carry q (i + 1) = (q i + carry q i) / 10 := rfl

theorem symAt (d : Nat → Nat) (k j : Nat) (hj : j < k + 4) :
    columnSum d (k + 4) (k + 3 - j) = columnSum d (k + 4) j := by
  have h := columnSum_symmetric d (k + 4) j hj
  rw [show k + 4 - 1 - j = k + 3 - j by omega] at h
  exact h.symm

section
variable (d : Nat → Nat) (k : Nat)

local notation "q" => columnSum d (k + 4)

theorem low_carries :
    carry q 1 = lc1 (q 0) ∧ carry q 2 = lc2 (q 0) (q 1) ∧
      carry q 3 = lc3 (q 0) (q 1) (q 2) := by
  have c1 : carry q 1 = lc1 (q 0) := by simp [carry, lc1]
  have c2 : carry q 2 = lc2 (q 0) (q 1) := by
    rw [carry_succ, c1]; rfl
  have c3 : carry q 3 = lc3 (q 0) (q 1) (q 2) := by
    rw [carry_succ, c2]; rfl
  exact ⟨c1, c2, c3⟩

theorem high_carries :
    carry q (k + 1) = hc3 (q 3) (carry q k) ∧
    carry q (k + 2) = hc2 (q 2) (q 3) (carry q k) ∧
    carry q (k + 3) = hc1 (q 1) (q 2) (q 3) (carry q k) ∧
    carry q (k + 4) = top4 (q 0) (q 1) (q 2) (q 3) (carry q k) := by
  have s0 := symAt d k 0 (by omega)
  have s1 := symAt d k 1 (by omega)
  have s2 := symAt d k 2 (by omega)
  have s3 := symAt d k 3 (by omega)
  rw [show k + 3 - 0 = k + 3 by omega] at s0
  rw [show k + 3 - 1 = k + 2 by omega] at s1
  rw [show k + 3 - 2 = k + 1 by omega] at s2
  rw [show k + 3 - 3 = k by omega] at s3
  have e1 : carry q (k + 1) = hc3 (q 3) (carry q k) := by
    rw [carry_succ, s3]; rfl
  have e2 : carry q (k + 2) = hc2 (q 2) (q 3) (carry q k) := by
    rw [show k + 2 = (k + 1) + 1 from rfl, carry_succ, s2, e1]; rfl
  have e3 : carry q (k + 3) = hc1 (q 1) (q 2) (q 3) (carry q k) := by
    rw [show k + 3 = (k + 2) + 1 from rfl, carry_succ, s1, e2]; rfl
  have e4 : carry q (k + 4) = top4 (q 0) (q 1) (q 2) (q 3) (carry q k) := by
    rw [show k + 4 = (k + 3) + 1 from rfl, carry_succ, s0, e3]; rfl
  exact ⟨e1, e2, e3, e4⟩

/-- Output digits in the four low columns. -/
theorem low_digits :
    output q 0 = q 0 % 10 ∧ output q 1 = (q 1 + lc1 (q 0)) % 10 ∧
      output q 2 = (q 2 + lc2 (q 0) (q 1)) % 10 ∧
      output q 3 = (q 3 + lc3 (q 0) (q 1) (q 2)) % 10 := by
  obtain ⟨c1, c2, c3⟩ := low_carries d k
  refine ⟨?_, ?_, ?_, ?_⟩
  · simp [output, carry]
  · simp only [output, c1]
  · simp only [output, c2]
  · simp only [output, c3]

/-- Output digits in the four high columns. -/
theorem high_digits :
    output q (k + 3) = (q 0 + hc1 (q 1) (q 2) (q 3) (carry q k)) % 10 ∧
    output q (k + 2) = (q 1 + hc2 (q 2) (q 3) (carry q k)) % 10 ∧
    output q (k + 1) = (q 2 + hc3 (q 3) (carry q k)) % 10 ∧
    output q k = (q 3 + carry q k) % 10 := by
  obtain ⟨e1, e2, e3, _⟩ := high_carries d k
  have s0 := symAt d k 0 (by omega)
  have s1 := symAt d k 1 (by omega)
  have s2 := symAt d k 2 (by omega)
  have s3 := symAt d k 3 (by omega)
  rw [show k + 3 - 0 = k + 3 by omega] at s0
  rw [show k + 3 - 1 = k + 2 by omega] at s1
  rw [show k + 3 - 2 = k + 1 by omega] at s2
  rw [show k + 3 - 3 = k by omega] at s3
  refine ⟨?_, ?_, ?_, ?_⟩
  · simp only [output, s0, e3]
  · simp only [output, s1, e2]
  · simp only [output, s2, e1]
  · simp only [output, s3]

end

/-! ## The projection in both branches -/

/-- Pair sum of any word, unfolded (definitional). -/
theorem cs_unfold (r : Nat → Nat) (L j : Nat) :
    columnSum r L j = r j + r (L - 1 - j) := rfl

/-- No-overflow branch (next width `k + 4`). -/
theorem quad_no_overflow (d : Nat → Nat) (k : Nat)
    (hc : carry (columnSum d (k + 4)) (k + 4) = 0) :
    (columnSum (output (columnSum d (k + 4))) (k + 4) 0,
     columnSum (output (columnSum d (k + 4))) (k + 4) 1,
     columnSum (output (columnSum d (k + 4))) (k + 4) 2,
     columnSum (output (columnSum d (k + 4))) (k + 4) 3) =
    nextQuad (columnSum d (k + 4) 0) (columnSum d (k + 4) 1)
      (columnSum d (k + 4) 2) (columnSum d (k + 4) 3)
      (carry (columnSum d (k + 4)) k) := by
  obtain ⟨_, _, _, e4⟩ := high_carries d k
  obtain ⟨o0, o1, o2, o3⟩ := low_digits d k
  obtain ⟨p0, p1, p2, p3⟩ := high_digits d k
  have htop : top4 (columnSum d (k + 4) 0) (columnSum d (k + 4) 1)
      (columnSum d (k + 4) 2) (columnSum d (k + 4) 3)
      (carry (columnSum d (k + 4)) k) = 0 := by rw [← e4]; exact hc
  rw [cs_unfold (output (columnSum d (k + 4))) (k + 4) 0,
    cs_unfold (output (columnSum d (k + 4))) (k + 4) 1,
    cs_unfold (output (columnSum d (k + 4))) (k + 4) 2,
    cs_unfold (output (columnSum d (k + 4))) (k + 4) 3,
    show k + 4 - 1 - 0 = k + 3 by omega, show k + 4 - 1 - 1 = k + 2 by omega,
    show k + 4 - 1 - 2 = k + 1 by omega, show k + 4 - 1 - 3 = k by omega,
    o0, o1, o2, o3, p0, p1, p2, p3, nextQuad, if_pos htop]

/-- Overflow branch (next width `k + 5`, leading digit the carry 1). -/
theorem quad_overflow (d : Nat → Nat) (k : Nat)
    (hc : carry (columnSum d (k + 4)) (k + 4) = 1) :
    (columnSum (extended (columnSum d (k + 4)) (k + 4)) (k + 5) 0,
     columnSum (extended (columnSum d (k + 4)) (k + 4)) (k + 5) 1,
     columnSum (extended (columnSum d (k + 4)) (k + 4)) (k + 5) 2,
     columnSum (extended (columnSum d (k + 4)) (k + 4)) (k + 5) 3) =
    nextQuad (columnSum d (k + 4) 0) (columnSum d (k + 4) 1)
      (columnSum d (k + 4) 2) (columnSum d (k + 4) 3)
      (carry (columnSum d (k + 4)) k) := by
  obtain ⟨_, _, _, e4⟩ := high_carries d k
  obtain ⟨o0, o1, o2, o3⟩ := low_digits d k
  obtain ⟨p0, p1, p2, _⟩ := high_digits d k
  have htop : ¬ top4 (columnSum d (k + 4) 0) (columnSum d (k + 4) 1)
      (columnSum d (k + 4) 2) (columnSum d (k + 4) 3)
      (carry (columnSum d (k + 4)) k) = 0 := by rw [← e4]; omega
  have x : ∀ j, j < k + 4 →
      extended (columnSum d (k + 4)) (k + 4) j = output (columnSum d (k + 4)) j := by
    intro j hj; simp only [extended, if_pos hj]
  have xt : extended (columnSum d (k + 4)) (k + 4) (k + 4) = 1 := by
    simp only [extended, Nat.lt_irrefl, if_false]; exact hc
  rw [cs_unfold (extended (columnSum d (k + 4)) (k + 4)) (k + 5) 0,
    cs_unfold (extended (columnSum d (k + 4)) (k + 4)) (k + 5) 1,
    cs_unfold (extended (columnSum d (k + 4)) (k + 4)) (k + 5) 2,
    cs_unfold (extended (columnSum d (k + 4)) (k + 4)) (k + 5) 3,
    show k + 5 - 1 - 0 = k + 4 by omega, show k + 5 - 1 - 1 = k + 3 by omega,
    show k + 5 - 1 - 2 = k + 2 by omega, show k + 5 - 1 - 3 = k + 1 by omega,
    xt, x 0 (by omega), x 1 (by omega), x 2 (by omega), x 3 (by omega),
    x (k + 3) (by omega), x (k + 2) (by omega), x (k + 1) (by omega),
    o0, o1, o2, o3, p0, p1, p2, nextQuad, if_neg htop]

#print axioms quad_no_overflow
#print axioms quad_overflow

end Agent113.FourColumn
