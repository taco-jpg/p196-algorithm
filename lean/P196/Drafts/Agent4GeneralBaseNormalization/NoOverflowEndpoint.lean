import P196.Drafts.Agent4GeneralBaseNormalization.NoOverflow

/-!
Agent #4: exact two-step numeric termination for the source's no-overflow case.
The same positive input width is certified at both actual iterates, so fixed
width in addAtWidth is not an omitted arithmetic correspondence hypothesis.
-/
namespace P196.Agent4.GeneralBase

theorem normalized_nooverflow_two_steps (b n : Nat) (q d : Nat → Nat)
    (hb : 8 ≤ b) (hs : Symmetric n q) (hd : CanonicalDigits b n d)
    (hpairs : ∀ i < n, pairCoeff n d i = normalized b 2 n q i)
    (hno : carryAt b q n = 0) :
    CanonicalNumeral b n (addAtWidth b n (value b d n)) ∧
      CanonicalNumeral b n (addAtWidth b n (addAtWidth b n (value b d n))) ∧
      reverseAtWidth b n (addAtWidth b n (addAtWidth b n (value b d n))) =
        addAtWidth b n (addAtWidth b n (value b d n)) := by
  have hcarry : arithmeticCarry b (pairCoeff n d) n = 0 := by
    calc
      arithmeticCarry b (pairCoeff n d) n =
          arithmeticCarry b (normalized b 2 n q) n :=
        arithmeticCarry_congr b n _ _ hpairs n (by omega)
      _ = carryAt b q n :=
        normalized_quotient_carry b 2 n q (by omega) (by omega) hs n (by omega)
      _ = 0 := hno
  have hout := canonical_output_nooverflow b n d (by omega) hd hcarry
  have hcongr : ∀ i < n, arithmeticOutput b (pairCoeff n d) i =
      arithmeticOutput b (normalized b 2 n q) i :=
    arithmeticOutput_congr b n _ _ hpairs
  have hlow : ∀ i < n, pairCoeff n (arithmeticOutput b (pairCoeff n d)) i < b := by
    intro i hi
    rw [pairCoeff_congr n _ _ hcongr i hi]
    have h := normalized_output_pairs_low b n q hb hs i hi
    omega
  have hfirst : value b (arithmeticOutput b (pairCoeff n d)) n =
      addAtWidth b n (value b d n) := by
    have h := reverse_add_arithmetic b n d
    simp only [hcarry, Nat.zero_mul, Nat.add_zero] at h
    unfold addAtWidth
    rw [reverseAtWidth_value b n d (by omega) hd.2.1]
    exact h
  have hc := (canonical_extracted_digits b n
    (arithmeticOutput b (pairCoeff n d)) (by omega) hout).1
  have hp := low_pairs_palindrome b n
    (arithmeticOutput b (pairCoeff n d)) (by omega) hout hlow
  rw [hfirst] at hc hp
  exact ⟨hc, hp.1, hp.2⟩

/-- Every non-overflow carry class has a normalized two-step palindromic member. -/
theorem nonoverflow_two_step_representative (b n a : Nat)
    (hb : 8 ≤ b) (hbe : b % 2 = 0) (ha : CanonicalNumeral b n a)
    (hno : firstCarry b n a n = 0) :
    ∃ z : Nat, CanonicalNumeral b n z ∧ 0 < z ∧
      (∀ i < n, pairCoeff n (integerDigit b z) i =
        normalized b 2 n (pairCoeff n (integerDigit b a)) i) ∧
      (∀ k ≤ n, firstCarry b n z k = firstCarry b n a k) ∧
      CanonicalNumeral b n (addAtWidth b n z) ∧
      CanonicalNumeral b n (addAtWidth b n (addAtWidth b n z)) ∧
      reverseAtWidth b n (addAtWidth b n (addAtWidth b n z)) =
        addAtWidth b n (addAtWidth b n z) := by
  have hbridge := arithmeticCarry_eq_carryAt b n (pairCoeff n (integerDigit b a))
    (by omega) (pairCoeff_bound b n (integerDigit b a) ha.1.2.1) n (by omega)
  have hthreshold : carryAt b (pairCoeff n (integerDigit b a)) n = 0 := by
    change arithmeticCarry b (pairCoeff n (integerDigit b a)) n = 0 at hno
    omega
  have hchosen : chosenLow b n (pairCoeff n (integerDigit b a)) = 2 := by
    simp [chosenLow, hthreshold]
  obtain ⟨e, he, hpair, hc⟩ := canonical_normalization_representative b n
    (integerDigit b a) (by omega) hbe ha.1
  have hpair2 : ∀ i < n, pairCoeff n e i =
      normalized b 2 n (pairCoeff n (integerDigit b a)) i := by
    simpa only [hchosen] using hpair
  have hterm := normalized_nooverflow_two_steps b n (pairCoeff n (integerDigit b a))
    e hb (pairCoeff_symmetric n (integerDigit b a)) he hpair2 hthreshold
  have hdec := canonical_extracted_digits b n e (by omega) he
  refine ⟨value b e n, hdec.1, canonical_value_positive b n e (by omega) he,
    ?_, ?_, hterm.1, hterm.2.1, hterm.2.2⟩
  · intro i hi
    calc
      pairCoeff n (integerDigit b (value b e n)) i = pairCoeff n e i :=
        pairCoeff_congr n _ _ hdec.2 i hi
      _ = _ := hpair2 i hi
  · intro k hk
    change arithmeticCarry b (pairCoeff n (integerDigit b (value b e n))) k =
      arithmeticCarry b (pairCoeff n (integerDigit b a)) k
    calc
      arithmeticCarry b (pairCoeff n (integerDigit b (value b e n))) k =
          arithmeticCarry b (pairCoeff n e) k :=
        arithmeticCarry_congr b n _ _ (pairCoeff_congr n _ _ hdec.2) k hk
      _ = _ := hc k hk

/-- The decimal specialization preserves the complete first carry word. -/
theorem decimal_nonoverflow_two_step_representative (n a : Nat)
    (ha : CanonicalNumeral 10 n a) (hno : firstCarry 10 n a n = 0) :
    ∃ z : Nat, CanonicalNumeral 10 n z ∧ 0 < z ∧
      (∀ k ≤ n, firstCarry 10 n z k = firstCarry 10 n a k) ∧
      CanonicalNumeral 10 n (addAtWidth 10 n z) ∧
      CanonicalNumeral 10 n (addAtWidth 10 n (addAtWidth 10 n z)) ∧
      reverseAtWidth 10 n (addAtWidth 10 n (addAtWidth 10 n z)) =
        addAtWidth 10 n (addAtWidth 10 n z) := by
  obtain ⟨z, hz, hp, _, hc, h1, h2, hpal⟩ :=
    nonoverflow_two_step_representative 10 n a (by decide) (by decide) ha hno
  exact ⟨z, hz, hp, hc, h1, h2, hpal⟩

end P196.Agent4.GeneralBase

#print axioms P196.Agent4.GeneralBase.normalized_nooverflow_two_steps
#print axioms P196.Agent4.GeneralBase.nonoverflow_two_step_representative
#print axioms P196.Agent4.GeneralBase.decimal_nonoverflow_two_step_representative
