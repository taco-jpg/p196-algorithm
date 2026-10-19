import P196.OriginalStreamSuccessor.Definitions

/-!
# Restoring the high scan at the two boundary phases

At phase zero the original high prefix already is the finite scan window.
At phase eighteen its positional value is one greater: the original long
division terminates in zeros, while the scan continues with nines. The
finite correction recovers the scan using the published value conservation,
positive-prefix quotient, phase-padding, and decimal reconstruction lemmas.
No new induction over digits or constant bands is needed.
-/

namespace Agent5.OriginalStreamSuccessor

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams Agent5.BoundedStreamCandidates
open Agent5.PhaseEighteenIsolation Agent5.FiniteObservationIsolation

private theorem fractionDigits_word (W : List Nat)
    (hW : ∀ x ∈ W, x < 10) :
    fractionDigits W.length (highValue W) (10 ^ W.length) = W := by
  have h := fractionDigits_of_highValue W 0 0 hW (by decide)
  simp only [Nat.add_zero, List.replicate_zero, List.append_nil] at h
  rw [fractionDigits_scale _ _ _ 9 (by decide)] at h
  exact h

private theorem fraction_value_nine (n q r g : Nat) (hg : g ≤ 1) :
    highValue (fractionDigits (n + 1 + q) (9 * r)
      (9 * 10 ^ n * 10 ^ g)) =
      10 ^ q * (if g = 0 then 10 * r else r) := by
  have hp : 0 < 9 * 10 ^ n :=
    Nat.mul_pos (by decide) (Nat.pow_pos (by decide))
  have hD : 0 < 9 * 10 ^ n * 10 ^ g :=
    Nat.mul_pos hp (Nat.pow_pos (by decide))
  rw [show n + 1 + q = (n + q) + 1 by omega,
    fractionDigits_value (n + q) _ _ hD]
  have hcases : g = 0 ∨ g = 1 := by omega
  rcases hcases with rfl | rfl
  · simp only [Nat.pow_zero, Nat.mul_one, if_pos rfl]
    have hnum : 10 ^ (n + q + 1) * (9 * r) =
        (9 * 10 ^ n) * (10 ^ q * (10 * r)) := by
      rw [Nat.pow_succ, Nat.pow_add]
      ac_rfl
    rw [hnum, Nat.mul_div_cancel_left _ hp]
    simp only [ite_true]
  · simp only [Nat.pow_one, if_neg (by decide : ¬(1 : Nat) = 0)]
    have hnum : 10 ^ (n + q + 1) * (9 * r) =
        (9 * 10 ^ n * 10) * (10 ^ q * r) := by
      rw [Nat.pow_succ, Nat.pow_add]
      ac_rfl
    rw [hnum, Nat.mul_div_cancel_left _ (Nat.mul_pos hp (by decide))]

/-- The corrected original high prefix is exactly the high scan followed
by its constant phase tail, including empty and noncanonical words. -/
theorem boundary_high_reconstruction (c q : Nat) (B : List Nat)
    (hc : c = 0 ∨ c = 18) (hB : ∀ x ∈ B, x ≤ 18) :
    let k := if 10 ≤ c then 1 else 0
    let t := c - 9 * k
    correctedHigh c (B.length + 1 + q)
      (originalHigh (B.length + 1 + q) { c := c, B := B }) =
      (if (normalize B.reverse k).2 == 0 then
        (normalize B.reverse k).1.reverse ++ [t]
       else [1] ++ (normalize B.reverse k).1.reverse) ++
        List.replicate q t := by
  let k := if 10 ≤ c then 1 else 0
  let t := c - 9 * k
  let g := (normalize B.reverse k).2
  let A := (normalize B.reverse k).1.reverse
  let W := if g == 0 then A ++ [t] else [1] ++ A
  let E := W ++ List.replicate q t
  let K := B.length + 1 + q
  change correctedHigh c K (originalHigh K { c := c, B := B }) = E
  have hk : k ≤ 1 := by dsimp only [k]; split <;> decide
  have hg : g ≤ 1 := normalize_carry_le B.reverse k
    (fun x hx => hB x (List.mem_reverse.mp hx)) hk
  have ht : t = 9 * (c / 18) := by
    rcases hc with rfl | rfl <;> rfl
  have ht10 : t < 10 := by
    rcases hc with rfl | rfl <;> decide
  have hlen : A.length = B.length := by
    simp only [A, List.length_reverse, normalize_length]
  have ha : ∀ x ∈ A, x < 10 := by
    intro x hx
    exact normalize_digits_lt_ten B.reverse k x (List.mem_reverse.mp hx)
  have hv : highValue A + 10 ^ B.length * g = highValue B + k := by
    dsimp only [A, g]
    rw [highValue_reverse_word]
    simpa only [List.length_reverse, lowValue_reverse] using
      normalize_value_conservation B.reverse k
  have hWlen : W.length = B.length + 1 := by
    dsimp only [W]
    split <;> simp [hlen]
  have hElen : E.length = K := by
    simp only [E, K, List.length_append, List.length_replicate, hWlen]
  have hWdigits : ∀ x ∈ W, x < 10 := by
    intro x hx
    change x ∈ (if g == 0 then A ++ [t] else [1] ++ A) at hx
    split at hx
    · rcases List.mem_append.mp hx with hx | hx
      · exact ha x hx
      · have hxt : x = t := by simpa only [List.mem_singleton] using hx
        simpa only [hxt] using ht10
    · rcases List.mem_append.mp hx with hx | hx
      · have hx1 : x = 1 := by simpa only [List.mem_singleton] using hx
        omega
      · exact ha x hx
  have hEdigits : ∀ x ∈ E, x < 10 := by
    intro x hx
    rcases List.mem_append.mp hx with hx | hx
    · exact hWdigits x hx
    · have hxt := List.eq_of_mem_replicate hx
      omega
  have hWvalue : highValue W + c / 18 =
      if g = 0 then 10 * (highValue B + c / 9) else highValue B + c / 9 := by
    by_cases hg0 : g = 0
    · have hAvalue : highValue A = highValue B + k := by
        rw [hg0] at hv
        omega
      have hW : highValue W = 10 * (highValue B + k) + t := by
        simp [W, hg0, highValue_append_single, hAvalue]
      rw [if_pos hg0, hW]
      rcases hc with rfl | rfl <;> simp [k, t, Nat.mul_add] <;> omega
    · have hg1 : g = 1 := by omega
      have hAvalue : 10 ^ B.length + highValue A = highValue B + k := by
        rw [hg1] at hv
        omega
      have hW : highValue W = highValue B + k := by
        simpa [W, hg1, highValue_cons_digit, hlen] using hAvalue
      rw [if_neg hg0, hW]
      rcases hc with rfl | rfl <;> simp [k] <;> omega
  have hEvalue : highValue E + c / 18 =
      10 ^ q * (highValue W + c / 18) := by
    have h := rhoNum_append_replicate t W q
    change 9 * highValue E + t = 10 ^ q * (9 * highValue W + t) at h
    simp only [ht, ← Nat.mul_add] at h
    have hm : 10 ^ q * (9 * (highValue W + c / 18)) =
        9 * (10 ^ q * (highValue W + c / 18)) := by ac_rfl
    rw [hm] at h
    omega
  have hrho : rhoNum c B = 9 * (highValue B + c / 9) := by
    rcases hc with rfl | rfl <;> simp [rhoNum, Nat.mul_add]
  have hreading := fraction_value_nine B.length q (highValue B + c / 9) g hg
  rw [← hrho] at hreading
  change highValue (originalHigh K { c := c, B := B }) =
    10 ^ q * (if g = 0 then 10 * (highValue B + c / 9)
      else highValue B + c / 9) at hreading
  rw [← hWvalue] at hreading
  have hvalue : highValue (originalHigh K { c := c, B := B }) =
      highValue E + c / 18 := hreading.trans hEvalue.symm
  have hdecode : fractionDigits K (highValue E) (10 ^ K) = E := by
    simpa only [hElen] using fractionDigits_word E hEdigits
  rcases hc with rfl | rfl
  · change originalHigh K { c := 0, B := B } = E
    have hD : 0 < 9 * 10 ^ B.length * 10 ^ g :=
      Nat.mul_pos (Nat.mul_pos (by decide) (Nat.pow_pos (by decide)))
        (Nat.pow_pos (by decide))
    apply (fractionDigits_eq_of_highValue_eq K (rhoNum 0 B) (highValue E)
      (9 * 10 ^ B.length * 10 ^ g) (10 ^ K) hD
      (Nat.pow_pos (by decide)) ?_).trans hdecode
    change highValue (originalHigh K { c := 0, B := B }) =
      highValue (fractionDigits K (highValue E) (10 ^ K))
    rw [hdecode]
    simpa only [Nat.zero_div, Nat.add_zero] using hvalue
  · change fractionDigits K
      (highValue (originalHigh K { c := 18, B := B }) - 1) (10 ^ K) = E
    rw [hvalue]
    simpa only [Nat.reduceDiv, Nat.add_sub_cancel] using hdecode

#print axioms boundary_high_reconstruction

end Agent5.OriginalStreamSuccessor
