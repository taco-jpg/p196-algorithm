import P196.TrimmedStreamObservation.LowPrefix
import P196.StreamObservationInjectivity.Sharpness

/-!
# Optimality of the low cutoff with complete high observation

At every positive width, phase four has two distinct valid exterior words
whose first one-fewer low digits agree and whose entire original high
streams agree. The next low digit separates the words. The general family
appends one terminal coefficient to the existing sharpness witnesses.

Equality at every high cutoff follows from exact simultaneous scaling of
the high numerator and its actual denominator. These are statements about
exterior observations and do not assert occurrence along the orbit of 196.
-/

namespace Agent5.TrimmedStreamObservation

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams Agent5.StreamObservationInjectivity

theorem lowSharpA_normalize (m : Nat) :
    normalize (sharpWordA m ++ [1]) 0 = (sharpWordA m ++ [1], 0) := by
  simp [normalize_append_single, sharpWordA_normalize]

theorem lowSharpB_normalize (m : Nat) :
    normalize (sharpWordB m ++ [14]) 0 = (sharpWordA m ++ [4], 1) := by
  simp [normalize_append_single, sharpWordB_normalize]

theorem lowSharpA_valid (m : Nat) :
    validOuter { c := 4, B := sharpWordA m ++ [1] } = true := by
  simp [validOuter, sharpWordA, List.getLast?_cons]

theorem lowSharpB_valid (m : Nat) :
    validOuter { c := 4, B := sharpWordB m ++ [14] } = true := by
  simp [validOuter, sharpWordB, List.getLast?_cons]

theorem lowSharpA_high_carry (m : Nat) :
    (normalize (sharpWordA m ++ [1]).reverse 0).2 = 0 := by
  simp [List.reverse_append, normalize, sharpWordA_reverse_normalize]

theorem lowSharpB_high_carry (m : Nat) :
    (normalize (sharpWordB m ++ [14]).reverse 0).2 = 1 := by
  have hz : 0 :: List.replicate m 0 = List.replicate m 0 ++ [0] :=
    List.replicate_succ'
  have hrev : (sharpWordB m).reverse = 0 :: (List.replicate m 0 ++ [11]) := by
    simp only [sharpWordB, List.reverse_cons, List.reverse_replicate]
    rw [← hz]
    rfl
  have h := congrArg (fun z : List Nat × Nat => z.2)
    (sharpWordB_reverse_normalize m)
  rw [hrev] at h
  rw [List.reverse_append, show ([14] : List Nat).reverse = [14] from rfl,
    List.singleton_append, hrev]
  simpa [normalize] using h

private theorem highValue_zero_replicate (m : Nat) :
    highValue (List.replicate m 0) = 0 := by
  induction m with
  | zero => rfl
  | succ m ih => simp [List.replicate_succ, highValue_cons_digit, ih]

/-- The high values differ by one decimal shift and the phase coefficient. -/
theorem lowSharp_highValue_relation (m : Nat) :
    highValue (sharpWordB m ++ [14]) =
      10 * highValue (sharpWordA m ++ [1]) + 4 := by
  rw [highValue_append_single, highValue_append_single]
  simp only [sharpWordA, sharpWordB, highValue_cons_digit, List.length_cons,
    List.length_replicate, highValue_zero_replicate, Nat.pow_succ,
    Nat.mul_zero, Nat.zero_mul, Nat.one_mul, Nat.add_zero]
  omega

private theorem high_stream_eq_of_highValue (A B : List Nat)
    (hlen : A.length = B.length)
    (hgA : (normalize A.reverse 0).2 = 0)
    (hgB : (normalize B.reverse 0).2 = 1)
    (hH : highValue B = 10 * highValue A + 4) (cut : Nat) :
    fractionDigits cut (rhoNum 4 A)
      (9 * 10 ^ A.length * 10 ^ (normalize A.reverse 0).2) =
      fractionDigits cut (rhoNum 4 B)
        (9 * 10 ^ B.length * 10 ^ (normalize B.reverse 0).2) := by
  have hr : rhoNum 4 B = 10 * rhoNum 4 A := by
    simp only [rhoNum]
    rw [hH]
    omega
  rw [hr, hgA, hgB, ← hlen]
  simp only [Nat.pow_zero, Nat.pow_one, Nat.mul_one]
  rw [show 9 * 10 ^ A.length * 10 = 10 * (9 * 10 ^ A.length) by ac_rfl]
  exact (fractionDigits_scale cut (rhoNum 4 A) (9 * 10 ^ A.length) 10
    (by decide)).symm

/-- Every finite cutoff of the two original high streams agrees. -/
theorem lowSharp_high_stream_eq (m highCut : Nat) :
    fractionDigits highCut (rhoNum 4 (sharpWordA m ++ [1]))
      (9 * 10 ^ (sharpWordA m ++ [1]).length *
        10 ^ (normalize (sharpWordA m ++ [1]).reverse 0).2) =
      fractionDigits highCut (rhoNum 4 (sharpWordB m ++ [14]))
        (9 * 10 ^ (sharpWordB m ++ [14]).length *
          10 ^ (normalize (sharpWordB m ++ [14]).reverse 0).2) := by
  exact high_stream_eq_of_highValue _ _ (by simp)
    (lowSharpA_high_carry m) (lowSharpB_high_carry m)
    (lowSharp_highValue_relation m) highCut

private theorem low_prefix_before_final (c : Nat) (B : List Nat) (x : Nat) :
    adicNumeratorDigits B.length (zValue c (B ++ [x]) - (c : Int)) =
      (normalize B 0).1 := by
  have h := adicNumeratorDigits_prefix B.length 1
    (zValue c (B ++ [x]) - (c : Int))
  have hlen : B.length + 1 = (B ++ [x]).length := by simp
  rw [hlen, low_prefix_normalized, normalize_append_single] at h
  have ht :
      ((normalize B 0).1 ++ [(x + (normalize B 0).2) % 10]).take B.length =
        (normalize B 0).1 := by
    rw [← normalize_length B 0]
    simp
  rw [ht] at h
  exact h.symm

/-- The low prefixes ending immediately before the final coefficient agree. -/
theorem lowSharp_low_prefix_eq (m : Nat) :
    adicNumeratorDigits (m + 2) (zValue 4 (sharpWordA m ++ [1]) - 4) =
      adicNumeratorDigits (m + 2) (zValue 4 (sharpWordB m ++ [14]) - 4) := by
  have ha := low_prefix_before_final 4 (sharpWordA m) 1
  have hb := low_prefix_before_final 4 (sharpWordB m) 14
  rw [sharpWordA_length, sharpWordA_normalize] at ha
  rw [sharpWordB_length, sharpWordB_normalize] at hb
  exact ha.trans hb.symm

/-- The final low digit is one in the first word and four in the second. -/
theorem lowSharp_low_boundary_ne (m : Nat) :
    adicNumeratorDigits (m + 3) (zValue 4 (sharpWordA m ++ [1]) - 4) ≠
      adicNumeratorDigits (m + 3) (zValue 4 (sharpWordB m ++ [14]) - 4) := by
  have ha := low_prefix_normalized 4 (sharpWordA m ++ [1])
  have hb := low_prefix_normalized 4 (sharpWordB m ++ [14])
  simp only [List.length_append, List.length_singleton, sharpWordA_length,
    sharpWordB_length, Nat.add_assoc, lowSharpA_normalize, lowSharpB_normalize] at ha hb
  intro h
  have ht : ([1] : List Nat) = [4] :=
    List.append_cancel_left (ha.symm.trans (h.trans hb))
  simp at ht

/-- At every positive width, complete high observation and one fewer low
digit fail to identify a valid exterior word. The next low digit separates
the same pair, so the low cutoff is uniformly optimal. -/
theorem low_cutoff_sharp_with_complete_high (n : Nat) (hn : 0 < n) :
    ∃ A B : List Nat,
      A.length = n ∧ B.length = n ∧ A ≠ B ∧
      (∀ x ∈ A, x ≤ 18) ∧ (∀ x ∈ B, x ≤ 18) ∧
      validOuter { c := 4, B := A } = true ∧
      validOuter { c := 4, B := B } = true ∧
      adicNumeratorDigits (n - 1) (zValue 4 A - 4) =
        adicNumeratorDigits (n - 1) (zValue 4 B - 4) ∧
      (∀ highCut : Nat,
        fractionDigits highCut (rhoNum 4 A)
          (9 * 10 ^ A.length * 10 ^ (normalize A.reverse 0).2) =
          fractionDigits highCut (rhoNum 4 B)
            (9 * 10 ^ B.length * 10 ^ (normalize B.reverse 0).2)) ∧
      adicNumeratorDigits n (zValue 4 A - 4) ≠
        adicNumeratorDigits n (zValue 4 B - 4) := by
  cases n with
  | zero => exact (Nat.not_lt_zero 0 hn).elim
  | succ n =>
      cases n with
      | zero =>
          refine ⟨[1], [14], rfl, rfl, by decide, ?_, ?_, by decide, by decide,
            by decide, ?_, by decide⟩
          · simp
          · simp
          · intro highCut
            exact high_stream_eq_of_highValue [1] [14] rfl (by decide) (by decide)
              (by decide) highCut
      | succ n =>
          cases n with
          | zero =>
              refine ⟨[1, 2], [11, 14], rfl, rfl, by decide, ?_, ?_, by decide,
                by decide, by decide, ?_, by decide⟩
              · simp
              · simp
              · intro highCut
                exact high_stream_eq_of_highValue [1, 2] [11, 14] rfl (by decide)
                  (by decide) (by decide) highCut
          | succ m =>
              refine ⟨sharpWordA m ++ [1], sharpWordB m ++ [14], by simp,
                by simp, ?_, entries_le_of_valid 4 _ (lowSharpA_valid m),
                entries_le_of_valid 4 _ (lowSharpB_valid m), lowSharpA_valid m,
                lowSharpB_valid m, ?_, lowSharp_high_stream_eq m,
                lowSharp_low_boundary_ne m⟩
              · simp [sharpWordA, sharpWordB]
              · simpa using lowSharp_low_prefix_eq m

#print axioms lowSharpA_normalize
#print axioms lowSharpB_normalize
#print axioms lowSharpA_valid
#print axioms lowSharpB_valid
#print axioms lowSharpA_high_carry
#print axioms lowSharpB_high_carry
#print axioms lowSharp_highValue_relation
#print axioms lowSharp_high_stream_eq
#print axioms lowSharp_low_prefix_eq
#print axioms lowSharp_low_boundary_ne
#print axioms low_cutoff_sharp_with_complete_high

end Agent5.TrimmedStreamObservation
