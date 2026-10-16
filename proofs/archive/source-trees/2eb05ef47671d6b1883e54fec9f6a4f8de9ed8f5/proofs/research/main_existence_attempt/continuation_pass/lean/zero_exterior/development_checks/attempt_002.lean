import LychrelDigitSums

/-!
Three zero pair-sum columns following a positive outer column can occur
only in the first five states of an actual decimal reverse-and-add orbit.
The theorem concerns actual carries and actual changing decimal widths.
It does not imply decimal Lychrel existence or termination of 196.
-/

namespace ZeroExterior

open DecimalDigits FoldedDecimal OverflowCarryNormalization

/-- The displayed four columns are inside the finite word. -/
def ThreeZero (L : Nat) (q : Nat → Nat) : Prop :=
  4 ≤ L ∧ q 1 = 0 ∧ q 2 = 0 ∧ q 3 = 0

theorem threeZero_min_width (L : Nat) (q : Nat → Nat)
    (ha : Admissible L q) (hz : ThreeZero L q) : 5 ≤ L := by
  have hL := hz.1
  have ho := ha.2.1
  have hs := ha.2.2.2.1 0 ha.1
  have hthree := hz.2.2.2
  by_cases he : L = 4
  · subst L
    simp only [Nat.sub_zero, Nat.reduceSub] at hs
    omega
  · omega

/-- Finite local arithmetic: overflow cannot emit three consecutive zeros. -/
theorem overflow_three_zeros_impossible (q a c : Nat → Nat)
    (hq : ∀ i, i < 4 → q i ≤ 18)
    (ha : ∀ i, i ≤ 4 → a i ≤ 1)
    (hc : ∀ i, i ≤ 4 → c i ≤ 1)
    (hzero : a 0 = 0) (hover : c 0 = 1)
    (hstep : ∀ i, i < 4 → a (i + 1) = (q i + a i) / 10 ∧
      c i = (q i + c (i + 1)) / 10)
    (hz1 : (q 1 + a 1) % 10 + (q 0 + c 1) % 10 = 0)
    (hz2 : (q 2 + a 2) % 10 + (q 1 + c 2) % 10 = 0)
    (hz3 : (q 3 + a 3) % 10 + (q 2 + c 3) % 10 = 0) : False := by
  have hq0 := hq 0 (by decide)
  have hq1 := hq 1 (by decide)
  have hq2 := hq 2 (by decide)
  have hq3 := hq 3 (by decide)
  have ha1 := ha 1 (by decide)
  have ha2 := ha 2 (by decide)
  have ha3 := ha 3 (by decide)
  have hc1 := hc 1 (by decide)
  have hc2 := hc 2 (by decide)
  have hc3 := hc 3 (by decide)
  have h0 := hstep 0 (by decide)
  have h1 := hstep 1 (by decide)
  have h2 := hstep 2 (by decide)
  simp only [Nat.reduceAdd] at h0 h1 h2
  omega

/-- Without overflow, those three zeros force the same predecessor zeros. -/
theorem no_overflow_three_zeros_rigidity (q a c : Nat → Nat)
    (hq : ∀ i, i < 4 → q i ≤ 18)
    (ha : ∀ i, i ≤ 4 → a i ≤ 1)
    (hc : ∀ i, i ≤ 4 → c i ≤ 1)
    (hzero : a 0 = 0) (hover : c 0 = 0)
    (hstep : ∀ i, i < 4 → a (i + 1) = (q i + a i) / 10 ∧
      c i = (q i + c (i + 1)) / 10)
    (hz1 : (q 1 + a 1) % 10 + (q 1 + c 2) % 10 = 0)
    (hz2 : (q 2 + a 2) % 10 + (q 2 + c 3) % 10 = 0)
    (hz3 : (q 3 + a 3) % 10 + (q 3 + c 4) % 10 = 0) :
    q 1 = 0 ∧ q 2 = 0 ∧ q 3 = 0 ∧ c 1 = 0 ∧ q 0 ≤ 9 := by
  have hq0 := hq 0 (by decide)
  have hq1 := hq 1 (by decide)
  have hq2 := hq 2 (by decide)
  have hq3 := hq 3 (by decide)
  have ha1 := ha 1 (by decide)
  have ha2 := ha 2 (by decide)
  have ha3 := ha 3 (by decide)
  have hc1 := hc 1 (by decide)
  have hc2 := hc 2 (by decide)
  have hc3 := hc 3 (by decide)
  have hc4 := hc 4 (by decide)
  have h0 := hstep 0 (by decide)
  have h1 := hstep 1 (by decide)
  have h2 := hstep 2 (by decide)
  have h3 := hstep 3 (by decide)
  simp only [Nat.reduceAdd] at h0 h1 h2 h3
  omega

end ZeroExterior
