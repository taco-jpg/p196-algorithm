import P196.StreamObservationInjectivity.Sharpness
import P196.TrimmedStreamObservation.LowPrefix

/-!
# Both extra boundary digits are needed to recover an unknown phase

At every width, including zero, the same bounded word is valid at phases
ten and twelve and has equal low observations through its width and equal
high observations through one more digit. The next low digit distinguishes
the phases. The arbitrary-width words reuse the existing sharpness family.
At phases two and twelve, the same words give the complementary sharpness:
the low prefixes include their boundary, while the high prefixes agree only
through the width and differ at the next digit.

All high denominators retain the actual outgoing carry with the incoming
carry belonging to their own phase. These are finite exterior observations,
not an assertion that the witnesses occur along the orbit of 196.
-/

namespace Agent5.PhaseStreamRecovery

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams Agent5.StreamObservationInjectivity

theorem sharpWordB_valid_at_ten (m : Nat) :
    validOuter { c := 10, B := sharpWordB m } = true := by
  cases m <;> simp [validOuter, sharpWordB, List.replicate_succ',
    List.append_assoc, List.getLast?_cons]

theorem sharpWordB_valid_at_twelve (m : Nat) :
    validOuter { c := 12, B := sharpWordB m } = true := by
  cases m <;> simp [validOuter, sharpWordB, List.replicate_succ',
    List.append_assoc, List.getLast?_cons]

/-- The existing high-overflow witness still overflows from incoming carry
one, since its first reversed zero resets that incoming carry to zero. -/
theorem sharpWordB_high_carry_one (m : Nat) :
    (normalize (sharpWordB m).reverse 1).2 = 1 := by
  have hz : 0 :: List.replicate m 0 = List.replicate m 0 ++ [0] :=
    List.replicate_succ'
  have hrev : (sharpWordB m).reverse = 0 :: (List.replicate m 0 ++ [11]) := by
    simp only [sharpWordB, List.reverse_cons, List.reverse_replicate]
    rw [← hz]
    rfl
  have h := congrArg (fun z : List Nat × Nat => z.2)
    (sharpWordB_reverse_normalize m)
  rw [hrev] at h ⊢
  simpa [normalize] using h

/-- Changing the incoming high carry from zero to one changes just the first
reversed normalized digit in the existing witness. -/
theorem sharpWordB_reverse_normalize_one (m : Nat) :
    normalize (sharpWordB m).reverse 1 =
      (1 :: (List.replicate m 0 ++ [1]), 1) := by
  have hz : 0 :: List.replicate m 0 = List.replicate m 0 ++ [0] :=
    List.replicate_succ'
  have hrev : (sharpWordB m).reverse = 0 :: (List.replicate m 0 ++ [11]) := by
    simp only [sharpWordB, List.reverse_cons, List.reverse_replicate]
    rw [← hz]
    rfl
  have h := congrArg (fun z : List Nat × Nat => z.1.tail)
    (sharpWordB_reverse_normalize m)
  rw [hrev] at h
  have ht : (normalize (List.replicate m 0 ++ [11]) 0).1 =
      List.replicate m 0 ++ [1] := by
    simpa [normalize, List.replicate_succ] using h
  apply Prod.ext
  · rw [hrev]
    simp [normalize, ht]
  · exact sharpWordB_high_carry_one m

/-- In the overflow branch, these two phases have exactly the same complete
high prefix: the phase tail starts after the observed digits. -/
theorem phase_ten_twelve_high_prefix_eq (B : List Nat)
    (hB : ∀ x ∈ B, x ≤ 18) (hg : (normalize B.reverse 1).2 = 1) :
    fractionDigits (B.length + 1) (rhoNum 10 B)
        (9 * 10 ^ B.length *
          10 ^ (normalize B.reverse (if 10 ≤ 10 then 1 else 0)).2) =
      fractionDigits (B.length + 1) (rhoNum 12 B)
        (9 * 10 ^ B.length *
          10 ^ (normalize B.reverse (if 10 ≤ 12 then 1 else 0)).2) := by
  have h10 :
      fractionDigits (B.length + 1) (rhoNum 10 B)
          (9 * 10 ^ B.length * 10 ^ (normalize B.reverse 1).2) =
        [1] ++ (normalize B.reverse 1).1.reverse := by
    simpa [hg] using fractionDigits_exterior 10 B 0
      (by simp [nonneutralPhase]) hB
  have h12 :
      fractionDigits (B.length + 1) (rhoNum 12 B)
          (9 * 10 ^ B.length * 10 ^ (normalize B.reverse 1).2) =
        [1] ++ (normalize B.reverse 1).1.reverse := by
    simpa [hg] using fractionDigits_exterior 12 B 0
      (by simp [nonneutralPhase]) hB
  exact h10.trans h12.symm

/-- The first low digit beyond any bounded word distinguishes phases ten
and twelve, even though every low digit within the word is phase-independent. -/
theorem phase_ten_twelve_low_boundary_ne (B : List Nat)
    (hB : ∀ x ∈ B, x ≤ 18) :
    adicNumeratorDigits (B.length + 1) (zValue 10 B - 10) ≠
      adicNumeratorDigits (B.length + 1) (zValue 12 B - 12) := by
  have h10 := adicNumeratorDigits_exterior 10 B 0
    (by simp [nonneutralPhase]) hB
  have h12 := adicNumeratorDigits_exterior 12 B 0
    (by simp [nonneutralPhase]) hB
  simp only [Nat.add_zero, List.replicate_zero, List.append_nil] at h10 h12
  intro h
  have heq : 10 + (normalize B 0).2 - 10 = 12 + (normalize B 0).2 - 10 := by
    simpa using List.append_cancel_left (h10.symm.trans (h.trans h12))
  omega

/-- At every width, a single valid bounded word has indistinguishable
observations at two different phases if the low cutoff omits its boundary
digit, even while the high cutoff includes its complete prefix. -/
theorem phase_low_cutoff_sharp (n : Nat) :
    ∃ B : List Nat,
      B.length = n ∧ (∀ x ∈ B, x ≤ 18) ∧
      validOuter { c := 10, B := B } = true ∧
      validOuter { c := 12, B := B } = true ∧
      adicNumeratorDigits n (zValue 10 B - 10) =
        adicNumeratorDigits n (zValue 12 B - 12) ∧
      fractionDigits (n + 1) (rhoNum 10 B)
          (9 * 10 ^ B.length *
            10 ^ (normalize B.reverse (if 10 ≤ 10 then 1 else 0)).2) =
        fractionDigits (n + 1) (rhoNum 12 B)
          (9 * 10 ^ B.length *
            10 ^ (normalize B.reverse (if 10 ≤ 12 then 1 else 0)).2) ∧
      adicNumeratorDigits (n + 1) (zValue 10 B - 10) ≠
        adicNumeratorDigits (n + 1) (zValue 12 B - 12) := by
  obtain ⟨B, hlen, hB, hv10, hv12, hg⟩ :
      ∃ B : List Nat,
        B.length = n ∧ (∀ x ∈ B, x ≤ 18) ∧
        validOuter { c := 10, B := B } = true ∧
        validOuter { c := 12, B := B } = true ∧
        (normalize B.reverse 1).2 = 1 := by
    cases n with
    | zero => exact ⟨[], rfl, by simp, by decide, by decide, by decide⟩
    | succ n =>
        cases n with
        | zero => exact ⟨[11], rfl, by simp, by decide, by decide, by decide⟩
        | succ m =>
            exact ⟨sharpWordB m, sharpWordB_length m, sharpWordB_bounded m,
              sharpWordB_valid_at_ten m, sharpWordB_valid_at_twelve m,
              sharpWordB_high_carry_one m⟩
  refine ⟨B, hlen, hB, hv10, hv12, ?_, ?_, ?_⟩
  · have h10 := Agent5.TrimmedStreamObservation.low_prefix_normalized 10 B
    have h12 := Agent5.TrimmedStreamObservation.low_prefix_normalized 12 B
    simpa only [hlen] using h10.trans h12.symm
  · simpa only [hlen] using phase_ten_twelve_high_prefix_eq B hB hg
  · simpa only [hlen] using phase_ten_twelve_low_boundary_ne B hB

/-- Phases two and twelve have the same low boundary digit for a fixed
bounded word, including its actual outgoing low carry. -/
theorem phase_two_twelve_low_prefix_eq (B : List Nat)
    (hB : ∀ x ∈ B, x ≤ 18) :
    adicNumeratorDigits (B.length + 1) (zValue 2 B - 2) =
      adicNumeratorDigits (B.length + 1) (zValue 12 B - 12) := by
  have hb : 12 + (normalize B 0).2 - 10 = 2 + (normalize B 0).2 := by omega
  have h2 : adicNumeratorDigits (B.length + 1) (zValue 2 B - 2) =
      (normalize B 0).1 ++ [2 + (normalize B 0).2] := by
    simpa using adicNumeratorDigits_exterior 2 B 0
      (by simp [nonneutralPhase]) hB
  have h12 : adicNumeratorDigits (B.length + 1) (zValue 12 B - 12) =
      (normalize B 0).1 ++ [2 + (normalize B 0).2] := by
    simpa [hb] using adicNumeratorDigits_exterior 12 B 0
      (by simp [nonneutralPhase]) hB
  exact h2.trans h12.symm

/-- At phase twelve the existing word's complete high prefix ends in one. -/
theorem sharpWordB_phase_twelve_high_boundary (m : Nat) :
    fractionDigits (m + 3) (rhoNum 12 (sharpWordB m))
      (9 * 10 ^ (sharpWordB m).length *
        10 ^ (normalize (sharpWordB m).reverse (if 10 ≤ 12 then 1 else 0)).2) =
      sharpWordA m ++ [1] := by
  simpa [sharpWordB_reverse_normalize_one, sharpWordA, List.reverse_cons,
    List.reverse_append, List.reverse_replicate, List.append_assoc, Nat.add_assoc] using
    fractionDigits_exterior 12 (sharpWordB m) 0
      (by simp [nonneutralPhase]) (sharpWordB_bounded m)

theorem sharpWordB_phase_twelve_high_prefix (m : Nat) :
    fractionDigits (m + 2) (rhoNum 12 (sharpWordB m))
      (9 * 10 ^ (sharpWordB m).length *
        10 ^ (normalize (sharpWordB m).reverse (if 10 ≤ 12 then 1 else 0)).2) =
      sharpWordA m := by
  have h := fractionDigits_prefix (m + 2) 1 (rhoNum 12 (sharpWordB m))
    (9 * 10 ^ (sharpWordB m).length *
      10 ^ (normalize (sharpWordB m).reverse (if 10 ≤ 12 then 1 else 0)).2)
  have ht : (sharpWordA m ++ [1]).take (m + 2) = sharpWordA m := by
    rw [← sharpWordA_length m]
    simp
  rw [sharpWordB_phase_twelve_high_boundary, ht] at h
  exact h.symm

theorem sharpWordB_two_twelve_high_boundary_ne (m : Nat) :
    fractionDigits (m + 3) (rhoNum 2 (sharpWordB m))
        (9 * 10 ^ (sharpWordB m).length *
          10 ^ (normalize (sharpWordB m).reverse (if 10 ≤ 2 then 1 else 0)).2) ≠
      fractionDigits (m + 3) (rhoNum 12 (sharpWordB m))
        (9 * 10 ^ (sharpWordB m).length *
          10 ^ (normalize (sharpWordB m).reverse (if 10 ≤ 12 then 1 else 0)).2) := by
  intro h
  have ht : ([0] : List Nat) = [1] := List.append_cancel_left
    ((sharpWordB_high_boundary m).symm.trans
      (h.trans (sharpWordB_phase_twelve_high_boundary m)))
  simp at ht

/-- At every width, a single valid bounded word also prevents lowering the
high cutoff when the low cutoff is held at one more than the width. The
next high digit distinguishes the two phases. -/
theorem phase_high_cutoff_sharp (n : Nat) :
    ∃ B : List Nat,
      B.length = n ∧ (∀ x ∈ B, x ≤ 18) ∧
      validOuter { c := 2, B := B } = true ∧
      validOuter { c := 12, B := B } = true ∧
      adicNumeratorDigits (n + 1) (zValue 2 B - 2) =
        adicNumeratorDigits (n + 1) (zValue 12 B - 12) ∧
      fractionDigits n (rhoNum 2 B)
          (9 * 10 ^ B.length *
            10 ^ (normalize B.reverse (if 10 ≤ 2 then 1 else 0)).2) =
        fractionDigits n (rhoNum 12 B)
          (9 * 10 ^ B.length *
            10 ^ (normalize B.reverse (if 10 ≤ 12 then 1 else 0)).2) ∧
      fractionDigits (n + 1) (rhoNum 2 B)
          (9 * 10 ^ B.length *
            10 ^ (normalize B.reverse (if 10 ≤ 2 then 1 else 0)).2) ≠
        fractionDigits (n + 1) (rhoNum 12 B)
          (9 * 10 ^ B.length *
            10 ^ (normalize B.reverse (if 10 ≤ 12 then 1 else 0)).2) := by
  cases n with
  | zero =>
      exact ⟨[], rfl, by simp, by decide, by decide, by decide, by decide, by decide⟩
  | succ n =>
      cases n with
      | zero =>
          exact ⟨[11], rfl, by simp, by decide, by decide, by decide,
            by decide, by decide⟩
      | succ m =>
          refine ⟨sharpWordB m, sharpWordB_length m, sharpWordB_bounded m,
            sharpWordB_valid m, sharpWordB_valid_at_twelve m, ?_, ?_,
            sharpWordB_two_twelve_high_boundary_ne m⟩
          · simpa only [sharpWordB_length] using
              phase_two_twelve_low_prefix_eq (sharpWordB m) (sharpWordB_bounded m)
          · exact (sharpWordB_high_prefix m).trans
              (sharpWordB_phase_twelve_high_prefix m).symm

#print axioms sharpWordB_valid_at_ten
#print axioms sharpWordB_valid_at_twelve
#print axioms sharpWordB_high_carry_one
#print axioms sharpWordB_reverse_normalize_one
#print axioms phase_ten_twelve_high_prefix_eq
#print axioms phase_ten_twelve_low_boundary_ne
#print axioms phase_low_cutoff_sharp
#print axioms phase_two_twelve_low_prefix_eq
#print axioms sharpWordB_phase_twelve_high_boundary
#print axioms sharpWordB_phase_twelve_high_prefix
#print axioms sharpWordB_two_twelve_high_boundary_ne
#print axioms phase_high_cutoff_sharp

end Agent5.PhaseStreamRecovery
