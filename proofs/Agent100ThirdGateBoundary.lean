import Agent100DoubleGate

/-! Local two-column obstruction after an overflow followed by a
non-overflow.  These lemmas inspect only the first two columns of an
admissible finite pair word.  They make no assumptions about its tail
outside the represented width and no claims about later returns. -/

namespace Agent100.ThirdGate

set_option maxHeartbeats 2000000
set_option maxRecDepth 10000

open DecimalDigits FoldedDecimal OverflowCarryNormalization

theorem penultimate_carry_low (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) (hL : 2 ≤ L) (h1 : q 1 ≤ 8) :
    carry q (L - 1) = 0 := by
  have hc := carry_bounded q L ha.2.2.1 (L - 2) (by omega)
  have hs := ha.2.2.2.1 1 (by omega)
  have he : L - 1 - 1 = L - 2 := by omega
  rw [he] at hs
  have hstep : carry q (L - 1) = (q (L - 2) + carry q (L - 2)) / 10 := by
    have he' : L - 1 = (L - 2) + 1 := by omega
    exact (congrArg (carry q) he').trans (by rfl)
  rw [hstep, ← hs]
  omega

theorem penultimate_carry_high (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) (hL : 2 ≤ L) (h1 : 10 ≤ q 1) :
    carry q (L - 1) = 1 := by
  have hc := carry_bounded q L ha.2.2.1 (L - 2) (by omega)
  have hb := ha.2.2.1 1 (by omega)
  have hs := ha.2.2.2.1 1 (by omega)
  have he : L - 1 - 1 = L - 2 := by omega
  rw [he] at hs
  have hstep : carry q (L - 1) = (q (L - 2) + carry q (L - 2)) / 10 := by
    have he' : L - 1 = (L - 2) + 1 := by omega
    exact (congrArg (carry q) he').trans (by rfl)
  rw [hstep, ← hs]
  omega

/-- Prefix (16,z), z at most 1, becomes (7,7+z) after overflow. -/
theorem sixteen_low_one_step (q : Nat → Nat) (L z : Nat)
    (ha : Admissible L q) (hL : 2 ≤ L)
    (h0 : q 0 = 16) (h1 : q 1 = z) (hz : z ≤ 1) :
    carry q L = 1 ∧ nextWidth q L = L + 1 ∧
      nextColumns q L 0 = 7 ∧ nextColumns q L 1 = 7 + z := by
  have hc := OverflowNormalizationNine.outer_large_overflow q L ha (by omega)
  have hc1 : carry q 1 = 1 := by
    simp only [carry, h0]
  have hc2 : carry q 2 = 0 := by
    change (q 1 + carry q 1) / 10 = 0
    rw [h1, hc1]
    omega
  have hp := penultimate_carry_low q L ha hL (by omega)
  have ho := next_column_overflow_outer q L ha.1 hc
  have hi := next_column_overflow_interior q L 1 (by omega) (by omega)
    ha.2.2.2.1 hc
  have he : L - 1 + 1 = L := by omega
  rw [he] at hi
  simp only [Nat.sub_self, hc1, hc2, hc, hp, h0, h1] at hi
  rw [hc1, h0] at ho
  exact ⟨hc, by simp [nextWidth, hc], by omega, by omega⟩

/-- Prefix (16,16+z), z at most 1, becomes (7,14+z) after overflow. -/
theorem sixteen_high_one_step (q : Nat → Nat) (L z : Nat)
    (ha : Admissible L q) (hL : 2 ≤ L)
    (h0 : q 0 = 16) (h1 : q 1 = 16 + z) (hz : z ≤ 1) :
    carry q L = 1 ∧ nextWidth q L = L + 1 ∧
      nextColumns q L 0 = 7 ∧ nextColumns q L 1 = 14 + z := by
  have hc := OverflowNormalizationNine.outer_large_overflow q L ha (by omega)
  have hc1 : carry q 1 = 1 := by
    simp only [carry, h0]
  have hc2 : carry q 2 = 1 := by
    change (q 1 + carry q 1) / 10 = 1
    rw [h1, hc1]
    omega
  have hp := penultimate_carry_high q L ha hL (by omega)
  have ho := next_column_overflow_outer q L ha.1 hc
  have hi := next_column_overflow_interior q L 1 (by omega) (by omega)
    ha.2.2.2.1 hc
  have he : L - 1 + 1 = L := by omega
  rw [he] at hi
  simp only [Nat.sub_self, hc1, hc2, hc, hp, h0, h1] at hi
  rw [hc1, h0] at ho
  exact ⟨hc, by simp [nextWidth, hc], by omega, by omega⟩

theorem next_outer_seven_low (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) (hL : 2 ≤ L) (h0 : q 0 = 7) (h1 : q 1 ≤ 8) :
    carry q L = 0 ∧ nextWidth q L = L ∧ nextColumns q L 0 = 14 := by
  have hc := NormalizationBridge.outer_small_no_overflow q L ha (by omega)
  have hc0 : carry q 0 = 0 := rfl
  have hc1 : carry q 1 = 0 := by
    simp only [carry, h0]
  have hp := penultimate_carry_low q L ha hL h1
  have ho := next_column_no_overflow q L 0 (by omega) ha.2.2.2.1 hc
  simp only [Nat.zero_add, Nat.sub_zero, hc0, hc1, hc, hp, h0] at ho
  exact ⟨hc, by simp [nextWidth, hc], by omega⟩

theorem next_outer_seven_high (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) (hL : 2 ≤ L) (h0 : q 0 = 7) (h1 : 10 ≤ q 1) :
    carry q L = 0 ∧ nextWidth q L = L ∧ nextColumns q L 0 = 15 := by
  have hc := NormalizationBridge.outer_small_no_overflow q L ha (by omega)
  have hc0 : carry q 0 = 0 := rfl
  have hc1 : carry q 1 = 0 := by
    simp only [carry, h0]
  have hp := penultimate_carry_high q L ha hL h1
  have ho := next_column_no_overflow q L 0 (by omega) ha.2.2.2.1 hc
  simp only [Nat.zero_add, Nat.sub_zero, hc0, hc1, hc, hp, h0] at ho
  exact ⟨hc, by simp [nextWidth, hc], by omega⟩

theorem two_steps_outer_fourteen (q : Nat → Nat) (L z : Nat)
    (ha : Admissible L q) (hL : 2 ≤ L)
    (h0 : q 0 = 16) (h1 : q 1 = z) (hz : z ≤ 1) :
    (iterPairs q L 2).1 = L + 1 ∧ (iterPairs q L 2).2 0 = 14 := by
  have hf := sixteen_low_one_step q L z ha hL h0 h1 hz
  have hs : Admissible (L + 1) (nextColumns q L) := by
    simpa only [hf.2.1] using NormalizationBridge.admissible_next q L ha
  have hg := next_outer_seven_low (nextColumns q L) (L + 1) hs (by omega)
    hf.2.2.1 (by have := hf.2.2.2; omega)
  change nextWidth (nextColumns q L) (nextWidth q L) = L + 1 ∧
    nextColumns (nextColumns q L) (nextWidth q L) 0 = 14
  rw [hf.2.1]
  exact ⟨hg.2.1, hg.2.2⟩

theorem two_steps_outer_fifteen (q : Nat → Nat) (L z : Nat)
    (ha : Admissible L q) (hL : 2 ≤ L)
    (h0 : q 0 = 16) (h1 : q 1 = 16 + z) (hz : z ≤ 1) :
    (iterPairs q L 2).1 = L + 1 ∧ (iterPairs q L 2).2 0 = 15 := by
  have hf := sixteen_high_one_step q L z ha hL h0 h1 hz
  have hs : Admissible (L + 1) (nextColumns q L) := by
    simpa only [hf.2.1] using NormalizationBridge.admissible_next q L ha
  have hg := next_outer_seven_high (nextColumns q L) (L + 1) hs (by omega)
    hf.2.2.1 (by have := hf.2.2.2; omega)
  change nextWidth (nextColumns q L) (nextWidth q L) = L + 1 ∧
    nextColumns (nextColumns q L) (nextWidth q L) 0 = 15
  rw [hf.2.1]
  exact ⟨hg.2.1, hg.2.2⟩

end Agent100.ThirdGate

#print axioms Agent100.ThirdGate.penultimate_carry_low
#print axioms Agent100.ThirdGate.penultimate_carry_high
#print axioms Agent100.ThirdGate.sixteen_low_one_step
#print axioms Agent100.ThirdGate.sixteen_high_one_step
#print axioms Agent100.ThirdGate.next_outer_seven_low
#print axioms Agent100.ThirdGate.next_outer_seven_high
#print axioms Agent100.ThirdGate.two_steps_outer_fourteen
#print axioms Agent100.ThirdGate.two_steps_outer_fifteen
