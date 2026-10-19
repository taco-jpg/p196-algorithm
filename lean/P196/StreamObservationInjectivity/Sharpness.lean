import P196.Agent5ExactDigitStreams.CoordinateStreams

/-!
# Sharpness of the exterior-stream observation cutoff

At every positive width there are two distinct valid exterior words at phase
two whose low and high streams agree through that width.  The high streams
differ at the next digit.  The arbitrary-width witnesses are proved by the
existing exact normalization and stream identities, not bounded enumeration.

These are statements about the original exterior-coordinate streams.  They
do not assert that either word occurs along the orbit of 196.
-/

namespace Agent5.StreamObservationInjectivity

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams

/-- The first witness at width `m + 2`. -/
def sharpWordA (m : Nat) : List Nat := 1 :: 1 :: List.replicate m 0

/-- The second witness has the same low value and a different high overflow. -/
def sharpWordB (m : Nat) : List Nat := 11 :: 0 :: List.replicate m 0

@[simp] theorem sharpWordA_length (m : Nat) : (sharpWordA m).length = m + 2 := by
  simp [sharpWordA, Nat.add_assoc]

@[simp] theorem sharpWordB_length (m : Nat) : (sharpWordB m).length = m + 2 := by
  simp [sharpWordB, Nat.add_assoc]

theorem sharpWords_ne (m : Nat) : sharpWordA m ≠ sharpWordB m := by
  simp [sharpWordA, sharpWordB]

theorem sharpWordA_bounded (m : Nat) : ∀ x ∈ sharpWordA m, x ≤ 18 := by
  simp [sharpWordA]

theorem sharpWordB_bounded (m : Nat) : ∀ x ∈ sharpWordB m, x ≤ 18 := by
  simp [sharpWordB]

theorem sharpWordA_valid (m : Nat) : validOuter { c := 2, B := sharpWordA m } = true := by
  cases m <;> simp [validOuter, sharpWordA, List.replicate_succ',
    List.append_assoc, List.getLast?_cons]

theorem sharpWordB_valid (m : Nat) : validOuter { c := 2, B := sharpWordB m } = true := by
  cases m <;> simp [validOuter, sharpWordB, List.replicate_succ',
    List.append_assoc, List.getLast?_cons]

private theorem normalize_zero_prefix (m : Nat) (xs : List Nat) :
    normalize (List.replicate m 0 ++ xs) 0 =
      (List.replicate m 0 ++ (normalize xs 0).1, (normalize xs 0).2) := by
  induction m with
  | zero => simp
  | succ m ih => simp [List.replicate_succ, normalize, ih]

private theorem normalize_zeros (m : Nat) :
    normalize (List.replicate m 0) 0 = (List.replicate m 0, 0) := by
  simpa [normalize] using normalize_zero_prefix m []

theorem sharpWordA_normalize (m : Nat) :
    normalize (sharpWordA m) 0 = (sharpWordA m, 0) := by
  simp [sharpWordA, normalize, normalize_zeros]

theorem sharpWordB_normalize (m : Nat) :
    normalize (sharpWordB m) 0 = (sharpWordA m, 0) := by
  simp [sharpWordA, sharpWordB, normalize, normalize_zeros]

theorem sharpWordA_reverse_normalize (m : Nat) :
    normalize (sharpWordA m).reverse 0 = ((sharpWordA m).reverse, 0) := by
  simp [sharpWordA, List.reverse_cons, List.reverse_replicate,
    normalize_zero_prefix, normalize, List.append_assoc]

theorem sharpWordB_reverse_normalize (m : Nat) :
    normalize (sharpWordB m).reverse 0 = (List.replicate (m + 1) 0 ++ [1], 1) := by
  simp [sharpWordB, List.reverse_cons, List.reverse_replicate,
    normalize_zero_prefix, normalize, List.replicate_succ', List.append_assoc]

/-- The entire displayed low prefix, including its boundary digit. -/
theorem sharpWordA_low_boundary (m : Nat) :
    adicNumeratorDigits (m + 3) (zValue 2 (sharpWordA m) - 2) =
      sharpWordA m ++ [2] := by
  simpa [sharpWordA_normalize, Nat.add_assoc] using
    adicNumeratorDigits_exterior 2 (sharpWordA m) 0
      (by simp [nonneutralPhase]) (sharpWordA_bounded m)

theorem sharpWordB_low_boundary (m : Nat) :
    adicNumeratorDigits (m + 3) (zValue 2 (sharpWordB m) - 2) =
      sharpWordA m ++ [2] := by
  simpa [sharpWordB_normalize, Nat.add_assoc] using
    adicNumeratorDigits_exterior 2 (sharpWordB m) 0
      (by simp [nonneutralPhase]) (sharpWordB_bounded m)

/-- With no high overflow, the boundary high digit is the phase digit two. -/
theorem sharpWordA_high_boundary (m : Nat) :
    fractionDigits (m + 3) (rhoNum 2 (sharpWordA m))
      (9 * 10 ^ (sharpWordA m).length *
        10 ^ (normalize (sharpWordA m).reverse 0).2) = sharpWordA m ++ [2] := by
  simpa [sharpWordA_reverse_normalize, Nat.add_assoc] using
    fractionDigits_exterior 2 (sharpWordA m) 0
      (by simp [nonneutralPhase]) (sharpWordA_bounded m)

/-- The other high stream inserts its overflow digit and ends this prefix in zero. -/
theorem sharpWordB_high_boundary (m : Nat) :
    fractionDigits (m + 3) (rhoNum 2 (sharpWordB m))
      (9 * 10 ^ (sharpWordB m).length *
        10 ^ (normalize (sharpWordB m).reverse 0).2) = sharpWordA m ++ [0] := by
  have hz : 0 :: List.replicate m 0 = List.replicate m 0 ++ [0] :=
    List.replicate_succ'
  simpa [sharpWordB_reverse_normalize, sharpWordA, List.reverse_append,
    List.reverse_replicate, List.replicate_succ', List.append_assoc, Nat.add_assoc, hz] using
    fractionDigits_exterior 2 (sharpWordB m) 0
      (by simp [nonneutralPhase]) (sharpWordB_bounded m)

private theorem take_sharpWordA_boundary (m d : Nat) :
    (sharpWordA m ++ [d]).take (m + 2) = sharpWordA m := by
  rw [← sharpWordA_length m]
  simp

theorem sharpWordA_low_prefix (m : Nat) :
    adicNumeratorDigits (m + 2) (zValue 2 (sharpWordA m) - 2) = sharpWordA m := by
  have h := adicNumeratorDigits_prefix (m + 2) 1 (zValue 2 (sharpWordA m) - 2)
  rw [sharpWordA_low_boundary, take_sharpWordA_boundary] at h
  exact h.symm

theorem sharpWordB_low_prefix (m : Nat) :
    adicNumeratorDigits (m + 2) (zValue 2 (sharpWordB m) - 2) = sharpWordA m := by
  have h := adicNumeratorDigits_prefix (m + 2) 1 (zValue 2 (sharpWordB m) - 2)
  rw [sharpWordB_low_boundary, take_sharpWordA_boundary] at h
  exact h.symm

theorem sharpWordA_high_prefix (m : Nat) :
    fractionDigits (m + 2) (rhoNum 2 (sharpWordA m))
      (9 * 10 ^ (sharpWordA m).length *
        10 ^ (normalize (sharpWordA m).reverse 0).2) = sharpWordA m := by
  have h := fractionDigits_prefix (m + 2) 1 (rhoNum 2 (sharpWordA m))
    (9 * 10 ^ (sharpWordA m).length * 10 ^ (normalize (sharpWordA m).reverse 0).2)
  rw [sharpWordA_high_boundary, take_sharpWordA_boundary] at h
  exact h.symm

theorem sharpWordB_high_prefix (m : Nat) :
    fractionDigits (m + 2) (rhoNum 2 (sharpWordB m))
      (9 * 10 ^ (sharpWordB m).length *
        10 ^ (normalize (sharpWordB m).reverse 0).2) = sharpWordA m := by
  have h := fractionDigits_prefix (m + 2) 1 (rhoNum 2 (sharpWordB m))
    (9 * 10 ^ (sharpWordB m).length * 10 ^ (normalize (sharpWordB m).reverse 0).2)
  rw [sharpWordB_high_boundary, take_sharpWordA_boundary] at h
  exact h.symm

/-- The general witnesses become distinguishable at exactly the boundary digit. -/
theorem sharpWords_high_boundary_ne (m : Nat) :
    fractionDigits (m + 3) (rhoNum 2 (sharpWordA m))
      (9 * 10 ^ (sharpWordA m).length * 10 ^ (normalize (sharpWordA m).reverse 0).2) ≠
    fractionDigits (m + 3) (rhoNum 2 (sharpWordB m))
      (9 * 10 ^ (sharpWordB m).length * 10 ^ (normalize (sharpWordB m).reverse 0).2) := by
  rw [sharpWordA_high_boundary, sharpWordB_high_boundary]
  intro h
  have ht : ([2] : List Nat) = [0] := List.append_cancel_left h
  simp at ht

/-- At width one the witness is `[1]` versus `[11]`; its next high digits are
two and one respectively. -/
theorem singleton_stream_control :
    adicNumeratorDigits 1 (zValue 2 [1] - 2) = [1] ∧
    adicNumeratorDigits 1 (zValue 2 [11] - 2) = [1] ∧
    fractionDigits 1 (rhoNum 2 [1]) (9 * 10 ^ ([1] : List Nat).length *
      10 ^ (normalize ([1] : List Nat).reverse 0).2) = [1] ∧
    fractionDigits 1 (rhoNum 2 [11]) (9 * 10 ^ ([11] : List Nat).length *
      10 ^ (normalize ([11] : List Nat).reverse 0).2) = [1] ∧
    fractionDigits 2 (rhoNum 2 [1]) (9 * 10 ^ ([1] : List Nat).length *
      10 ^ (normalize ([1] : List Nat).reverse 0).2) = [1, 2] ∧
    fractionDigits 2 (rhoNum 2 [11]) (9 * 10 ^ ([11] : List Nat).length *
      10 ^ (normalize ([11] : List Nat).reverse 0).2) = [1, 1] := by
  decide

/-- At every positive width, observing exactly that many digits of both
streams fails to identify a bounded valid exterior word.  One more high digit
separates the explicit witnesses. -/
theorem observation_cutoff_sharp (n : Nat) (hn : 0 < n) :
    ∃ A B : List Nat,
      A.length = n ∧ B.length = n ∧ A ≠ B ∧
      (∀ x ∈ A, x ≤ 18) ∧ (∀ x ∈ B, x ≤ 18) ∧
      validOuter { c := 2, B := A } = true ∧
      validOuter { c := 2, B := B } = true ∧
      adicNumeratorDigits n (zValue 2 A - 2) =
        adicNumeratorDigits n (zValue 2 B - 2) ∧
      fractionDigits n (rhoNum 2 A)
        (9 * 10 ^ A.length * 10 ^ (normalize A.reverse 0).2) =
        fractionDigits n (rhoNum 2 B)
          (9 * 10 ^ B.length * 10 ^ (normalize B.reverse 0).2) ∧
      fractionDigits (n + 1) (rhoNum 2 A)
        (9 * 10 ^ A.length * 10 ^ (normalize A.reverse 0).2) ≠
        fractionDigits (n + 1) (rhoNum 2 B)
          (9 * 10 ^ B.length * 10 ^ (normalize B.reverse 0).2) := by
  cases n with
  | zero => exact (Nat.not_lt_zero 0 hn).elim
  | succ n =>
      cases n with
      | zero =>
          refine ⟨[1], [11], rfl, rfl, by decide, ?_, ?_, by decide, by decide,
            ?_, ?_, ?_⟩
          · simp
          · simp
          · decide
          · decide
          · decide
      | succ m =>
          refine ⟨sharpWordA m, sharpWordB m, sharpWordA_length m,
            sharpWordB_length m, sharpWords_ne m, sharpWordA_bounded m,
            sharpWordB_bounded m, sharpWordA_valid m, sharpWordB_valid m,
            ?_, ?_, sharpWords_high_boundary_ne m⟩
          · rw [sharpWordA_low_prefix, sharpWordB_low_prefix]
          · rw [sharpWordA_high_prefix, sharpWordB_high_prefix]

#print axioms sharpWordA_valid
#print axioms sharpWordB_valid
#print axioms sharpWordA_normalize
#print axioms sharpWordB_normalize
#print axioms sharpWordA_reverse_normalize
#print axioms sharpWordB_reverse_normalize
#print axioms sharpWordA_low_boundary
#print axioms sharpWordB_low_boundary
#print axioms sharpWordA_high_boundary
#print axioms sharpWordB_high_boundary
#print axioms sharpWordA_low_prefix
#print axioms sharpWordB_low_prefix
#print axioms sharpWordA_high_prefix
#print axioms sharpWordB_high_prefix
#print axioms sharpWords_high_boundary_ne
#print axioms singleton_stream_control
#print axioms observation_cutoff_sharp

end Agent5.StreamObservationInjectivity
