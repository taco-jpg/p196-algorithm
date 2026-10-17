import P196.Agent5OrdinaryStreamPrefix.OrdinaryStreamStep

/-!
Agent #5: canonical all-gap sharpness families for finite stream agreement.
The normalization formulas reuse Agent #6's original surrounded_normalization.
The literal coordinate digits reuse Agent #5's existing arbitrary-tail stream
identities. The two families fail at the first digit beyond the proposed
uniform window, one family for each outgoing carry.
-/

namespace Agent5.OrdinaryStreamWindow.Sharpness

open P196.Agent6 Agent115.ExteriorFactorization Agent5.ExactDigitStreams

def D0 (g : Nat) : List Nat :=
  List.replicate (g + 2) 1 ++ [9] ++ List.replicate (g + 2) 1

def D1 (g : Nat) : List Nat :=
  List.replicate (g + 2) 5 ++ [0] ++ List.replicate (g + 2) 5

theorem D0_decimal (g : Nat) : DecimalDigits (D0 g) := by
  intro x hx
  simp [D0] at hx
  omega

theorem D1_decimal (g : Nat) : DecimalDigits (D1 g) := by
  intro x hx
  simp [D1] at hx
  omega

theorem D0_positive_last (g : Nat) : PositiveLast (D0 g) := by
  refine ⟨List.replicate (g + 2) 1 ++ [9] ++ List.replicate (g + 1) 1,
    1, ?_, by decide⟩
  simp only [D0, List.append_assoc, ← List.replicate_succ']

theorem D1_positive_last (g : Nat) : PositiveLast (D1 g) := by
  refine ⟨List.replicate (g + 2) 5 ++ [0] ++ List.replicate (g + 1) 5,
    5, ?_, by decide⟩
  simp only [D1, List.append_assoc, ← List.replicate_succ']

theorem D0_paired (g : Nat) : paired (D0 g) = surrounded [] 2 g [18] := by
  have hrev : (D0 g).reverse = D0 g := by
    simp [D0, List.reverse_append, List.append_assoc]
  simp only [paired, hrev, List.zipWith_self]
  simp [D0, surrounded]

theorem D1_paired (g : Nat) : paired (D1 g) = surrounded [] 10 g [0] := by
  have hrev : (D1 g).reverse = D1 g := by
    simp [D1, List.reverse_append, List.append_assoc]
  simp only [paired, hrev, List.zipWith_self]
  simp [D1, surrounded]

theorem D0_reverseAddDigits (g : Nat) :
    reverseAddDigits (D0 g) =
      List.replicate (g + 2) 2 ++ [8, 3] ++ List.replicate (g + 1) 2 := by
  unfold reverseAddDigits
  rw [D0_paired]
  unfold normalizedDigits
  rw [surrounded_normalization [] [18] 2 g (by simp [Nonneutral])
    (by simp [Coefficients]) (by simp [Coefficients])]
  simp [norm, carryPhase, digitPhase, List.replicate_succ, List.append_assoc]

theorem D1_reverseAddDigits (g : Nat) :
    reverseAddDigits (D1 g) =
      [0] ++ List.replicate (g + 2) 1 ++ [0] ++ List.replicate (g + 2) 1 := by
  unfold reverseAddDigits
  rw [D1_paired]
  unfold normalizedDigits
  rw [surrounded_normalization [] [0] 10 g (by simp [Nonneutral])
    (by simp [Coefficients]) (by simp [Coefficients])]
  simp [norm, carryPhase, digitPhase, List.replicate_succ', List.append_assoc]

/-- At the first excluded position in the zero-carry family, the actual pair
coefficient is five after an initial string of fours. -/
theorem D0_first_excluded_prefix (g : Nat) :
    (paired (reverseAddDigits (D0 g))).take (g + 2) =
      List.replicate (g + 1) 4 ++ [5] := by
  have hlo : (reverseAddDigits (D0 g)).take (g + 2) =
      List.replicate (g + 2) 2 := by
    simp [D0_reverseAddDigits, List.append_assoc]
  have hhi : (reverseAddDigits (D0 g)).reverse.take (g + 2) =
      List.replicate (g + 1) 2 ++ [3] := by
    have hlen : (List.replicate (g + 1) 2 ++ [3]).length = g + 2 := by simp
    have hpref := take_complete_prefix (List.replicate (g + 1) 2 ++ [3])
      ([8] ++ List.replicate (g + 2) 2)
    rw [hlen] at hpref
    have hrev : (reverseAddDigits (D0 g)).reverse =
        (List.replicate (g + 1) 2 ++ [3]) ++
          ([8] ++ List.replicate (g + 2) 2) := by
      simp [D0_reverseAddDigits, List.reverse_append, List.append_assoc]
    rw [hrev]
    exact hpref
  simp only [paired, List.take_zipWith, hlo, hhi]
  rw [show List.replicate (g + 2) 2 =
    List.replicate (g + 1) 2 ++ [2] from List.replicate_succ']
  rw [List.zipWith_append (by rfl)]
  simp

/-- At the first excluded position in the one-carry family, the actual pair
coefficient is one after the initial one and string of twos. -/
theorem D1_first_excluded_prefix (g : Nat) :
    (paired (reverseAddDigits (D1 g))).take (g + 3) =
      [1] ++ List.replicate (g + 1) 2 ++ [1] := by
  have hlo : (reverseAddDigits (D1 g)).take (g + 3) =
      [0] ++ List.replicate (g + 2) 1 := by
    simp [D1_reverseAddDigits, List.append_assoc]
  have hhi : (reverseAddDigits (D1 g)).reverse.take (g + 3) =
      List.replicate (g + 2) 1 ++ [0] := by
    have hlen : (List.replicate (g + 2) 1 ++ [0]).length = g + 3 := by simp
    have hpref := take_complete_prefix (List.replicate (g + 2) 1 ++ [0])
      (List.replicate (g + 2) 1 ++ [0])
    rw [hlen] at hpref
    have hrev : (reverseAddDigits (D1 g)).reverse =
        (List.replicate (g + 2) 1 ++ [0]) ++
          (List.replicate (g + 2) 1 ++ [0]) := by
      simp [D1_reverseAddDigits, List.reverse_append, List.append_assoc]
    rw [hrev]
    exact hpref
  simp only [paired, List.take_zipWith, hlo, hhi]
  have hhead : List.replicate (g + 2) 1 ++ [0] =
      1 :: (List.replicate (g + 1) 1 ++ [0]) := rfl
  rw [hhead]
  change 1 :: List.zipWith Nat.add (List.replicate (g + 2) 1)
    (List.replicate (g + 1) 1 ++ [0]) = _
  rw [show List.replicate (g + 2) 1 =
    List.replicate (g + 1) 1 ++ [1] from List.replicate_succ']
  rw [List.zipWith_append (by rfl)]
  simp

/-- The empty exterior has the stated actual carries and coordinate selectors. -/
theorem empty_exterior_carry_controls :
    Agent6.ExteriorCoordinates.overflow 2 [] = 0 ∧
    Agent6.ExteriorCoordinates.overflow 10 [] = 1 ∧
    (if 9 * 10 ^ ([] : List Nat).length ≤ rhoNum 2 [] then 1 else 0) = (0 : Nat) ∧
    (if 9 * 10 ^ ([] : List Nat).length ≤ rhoNum 10 [] then 1 else 0) = (1 : Nat) := by
  decide

/-- The literal streams predict only fours at the zero-carry excluded cutoff. -/
theorem D0_coordinate_streams (g : Nat) :
    List.zipWith Nat.add
      (adicNumeratorDigits (g + 2) (zValue 2 [] - (2 : Int)))
      (fractionDigits (g + 2) (rhoNum 2 [])
        (9 * 10 ^ ([] : List Nat).length *
          10 ^ (if 9 * 10 ^ ([] : List Nat).length ≤ rhoNum 2 [] then 1 else 0))) =
      List.replicate (g + 2) 4 := by
  have hlo : adicNumeratorDigits (g + 2) (zValue 2 [] - (2 : Int)) =
      List.replicate (g + 2) 2 := by
    simpa [P196.Agent7.Finite.normalize, List.replicate_succ,
      Nat.add_comm, Nat.add_left_comm, Nat.add_assoc] using
      adicNumeratorDigits_exterior 2 [] (g + 1)
        (by simp [nonneutralPhase]) (by simp)
  have hhi : fractionDigits (g + 2) (rhoNum 2 []) 9 =
      List.replicate (g + 2) 2 := by
    simpa [P196.Agent7.Finite.normalize, List.replicate_succ,
      Nat.add_comm, Nat.add_left_comm, Nat.add_assoc] using
      fractionDigits_exterior 2 [] (g + 1)
        (by simp [nonneutralPhase]) (by simp)
  have hscale : 9 * 10 ^ ([] : List Nat).length *
      10 ^ (if 9 * 10 ^ ([] : List Nat).length ≤ rhoNum 2 [] then 1 else 0) = 9 := by
    decide
  rw [hscale, hlo, hhi]
  simp

/-- The literal streams predict a one followed by twos at the one-carry
excluded cutoff. -/
theorem D1_coordinate_streams (g : Nat) :
    List.zipWith Nat.add
      (adicNumeratorDigits (g + 3) (zValue 10 [] - (10 : Int)))
      (fractionDigits (g + 3) (rhoNum 10 [])
        (9 * 10 ^ ([] : List Nat).length *
          10 ^ (if 9 * 10 ^ ([] : List Nat).length ≤ rhoNum 10 [] then 1 else 0))) =
      [1] ++ List.replicate (g + 2) 2 := by
  have hlo : adicNumeratorDigits (g + 3) (zValue 10 [] - (10 : Int)) =
      [0] ++ List.replicate (g + 2) 1 := by
    simpa [P196.Agent7.Finite.normalize, Nat.add_comm,
      Nat.add_left_comm, Nat.add_assoc] using
      adicNumeratorDigits_exterior 10 [] (g + 2)
        (by simp [nonneutralPhase]) (by simp)
  have hhi : fractionDigits (g + 3) (rhoNum 10 []) 90 =
      List.replicate (g + 3) 1 := by
    simpa [P196.Agent7.Finite.normalize, List.replicate_succ,
      Nat.add_comm, Nat.add_left_comm, Nat.add_assoc] using
      fractionDigits_exterior 10 [] (g + 2)
        (by simp [nonneutralPhase]) (by simp)
  have hscale : 9 * 10 ^ ([] : List Nat).length *
      10 ^ (if 9 * 10 ^ ([] : List Nat).length ≤ rhoNum 10 [] then 1 else 0) = 90 := by
    decide
  rw [hscale, hlo, hhi]
  change 1 :: List.zipWith Nat.add (List.replicate (g + 2) 1)
    (List.replicate (g + 2) 1) = _
  simp

/-- For every gap, the zero-carry canonical family fails at the first cutoff
beyond the uniform window. -/
theorem D0_stream_mismatch (g : Nat) :
    (paired (reverseAddDigits (D0 g))).take (g + 2) ≠
      List.zipWith Nat.add
        (adicNumeratorDigits (g + 2) (zValue 2 [] - (2 : Int)))
        (fractionDigits (g + 2) (rhoNum 2 [])
          (9 * 10 ^ ([] : List Nat).length *
            10 ^ (if 9 * 10 ^ ([] : List Nat).length ≤ rhoNum 2 [] then 1 else 0))) := by
  rw [D0_first_excluded_prefix, D0_coordinate_streams]
  rw [show List.replicate (g + 2) 4 =
    List.replicate (g + 1) 4 ++ [4] from List.replicate_succ']
  simp

/-- For every gap, the one-carry canonical family fails at the first cutoff
beyond the uniform window. -/
theorem D1_stream_mismatch (g : Nat) :
    (paired (reverseAddDigits (D1 g))).take (g + 3) ≠
      List.zipWith Nat.add
        (adicNumeratorDigits (g + 3) (zValue 10 [] - (10 : Int)))
        (fractionDigits (g + 3) (rhoNum 10 [])
          (9 * 10 ^ ([] : List Nat).length *
            10 ^ (if 9 * 10 ^ ([] : List Nat).length ≤ rhoNum 10 [] then 1 else 0))) := by
  rw [D1_first_excluded_prefix, D1_coordinate_streams]
  rw [show List.replicate (g + 2) 2 =
    List.replicate (g + 1) 2 ++ [2] from List.replicate_succ']
  simp [List.append_assoc]

/-- Both minimal-gap actual prefixes follow from the universal formulas. -/
theorem gap_zero_actual_prefixes :
    (paired (reverseAddDigits (D0 0))).take 2 = [4, 5] ∧
    (paired (reverseAddDigits (D1 0))).take 3 = [1, 2, 1] := by
  constructor
  · simpa using D0_first_excluded_prefix 0
  · simpa using D1_first_excluded_prefix 0

/-- The corresponding minimal-gap stream predictions have different final
coefficients in both carry branches. -/
theorem gap_zero_stream_prefixes :
    List.zipWith Nat.add
      (adicNumeratorDigits 2 (zValue 2 [] - (2 : Int)))
      (fractionDigits 2 (rhoNum 2 [])
        (9 * 10 ^ ([] : List Nat).length *
          10 ^ (if 9 * 10 ^ ([] : List Nat).length ≤ rhoNum 2 [] then 1 else 0))) = [4, 4] ∧
    List.zipWith Nat.add
      (adicNumeratorDigits 3 (zValue 10 [] - (10 : Int)))
      (fractionDigits 3 (rhoNum 10 [])
        (9 * 10 ^ ([] : List Nat).length *
          10 ^ (if 9 * 10 ^ ([] : List Nat).length ≤ rhoNum 10 [] then 1 else 0))) = [1, 2, 2] := by
  constructor
  · simpa using D0_coordinate_streams 0
  · simpa using D1_coordinate_streams 0

end Agent5.OrdinaryStreamWindow.Sharpness
