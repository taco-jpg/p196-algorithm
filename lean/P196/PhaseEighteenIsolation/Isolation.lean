import P196.PhaseEighteenIsolation.Quotients
import P196.PhaseEighteenIsolation.Padding
import P196.PhaseEighteenIsolation.Rigidity

/-!
# Finite isolation at the upper exterior phase

Append one coefficient 18 to the target, and pad a competitor by its own
phase until it contains a block of that length. The two observed numeric
values force equality of these blocks and the maximal possible quotient
of the competitor's remaining tail. The maximal quotient determines phase
18 and a tail consisting entirely of 18, so suffix removal recovers the
original canonical cores regardless of the competitor's width.
-/

namespace Agent5.PhaseEighteenIsolation

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams Agent5.FiniteExteriorHistories

/-- The upper boundary is recovered from a low prefix one longer than the
target word, a high prefix additionally shifted by the target's actual
carry, and equality of the actual carries. The competitor can have any
natural phase at most 18 and arbitrary coefficient width. -/
theorem phase18_canonical_fiber_of_prefixes
    (d : Nat) (A B : List Nat)
    (hd : d ≤ 18)
    (hA : ∀ x ∈ A, x ≤ 18) (hB : ∀ x ∈ B, x ≤ 18)
    (hcarry : (normalize A.reverse (if 10 ≤ d then 1 else 0)).2 =
      (normalize B.reverse 1).2)
    (hlow : adicNumeratorDigits (B.length + 1) (zValue d A - (d : Int)) =
      adicNumeratorDigits (B.length + 1) (zValue 18 B - 18))
    (hhigh :
      fractionDigits (B.length + 1 + (normalize B.reverse 1).2) (rhoNum d A)
          (9 * 10 ^ A.length *
            10 ^ (normalize A.reverse (if 10 ≤ d then 1 else 0)).2) =
        fractionDigits (B.length + 1 + (normalize B.reverse 1).2) (rhoNum 18 B)
          (9 * 10 ^ B.length * 10 ^ (normalize B.reverse 1).2)) :
    d = 18 ∧ stripSuffix d A = stripSuffix 18 B := by
  let L := B.length + 1
  let gamma := (normalize B.reverse 1).2
  let Y := B ++ [18]
  let P := A ++ List.replicate L d
  let X := P.take L
  let S := P.drop L
  have hsplit : P = X ++ S := (List.take_append_drop L P).symm
  have hLP : L ≤ P.length := by
    simp only [P, List.length_append, List.length_replicate]
    omega
  have hXlen : X.length = L := by
    simp only [X, List.length_take, Nat.min_eq_left hLP]
  have hYlen : Y.length = L := by simp [Y, L]
  have hPbound : ∀ x ∈ P, x ≤ 18 := by
    intro x hx
    rcases List.mem_append.mp hx with hx | hx
    · exact hA x hx
    · simpa only [List.eq_of_mem_replicate hx] using hd
  have hXbound : ∀ x ∈ X, x ≤ 18 := by
    intro x hx
    exact hPbound x (List.mem_of_mem_take hx)
  have hSbound : ∀ x ∈ S, x ≤ 18 := by
    intro x hx
    exact hPbound x (List.mem_of_mem_drop hx)
  have hYbound : ∀ x ∈ Y, x ≤ 18 := by
    intro x hx
    rcases List.mem_append.mp hx with hx | hx
    · exact hB x hx
    · have heq := List.mem_singleton.mp hx
      omega
  have hYlarge : 10 ^ Y.length ≤ lowValue Y := by
    rw [hYlen]
    change 10 ^ (B.length + 1) ≤ lowValue (B ++ [18])
    rw [Nat.pow_succ, lowValue_append]
    simp only [lowValue, Nat.mul_zero, Nat.add_zero]
    have hmul := Nat.mul_le_mul_left (10 ^ B.length) (by decide : 10 ≤ 18)
    omega
  have hLow : adicNumeratorDigits L (zValue d P - (d : Int)) =
      adicNumeratorDigits L (zValue 18 Y - 18) :=
    (Agent5.TrimmedStreamObservation.phase_padding_low d L A L).trans
      (hlow.trans
        (Agent5.TrimmedStreamObservation.phase_padding_low 18 L B 1).symm)
  have hPlow := low_prefix_append_value d X S
  have hYlow := low_prefix_append_value 18 Y []
  have hlowValues : lowValue X % 10 ^ Y.length = lowValue Y % 10 ^ Y.length := by
    calc
      lowValue X % 10 ^ Y.length =
          lowValue (adicNumeratorDigits L (zValue d P - (d : Int))) := by
        rw [hYlen, ← hXlen, hsplit]
        exact hPlow.symm
      _ = lowValue (adicNumeratorDigits L (zValue 18 Y - 18)) :=
        congrArg lowValue hLow
      _ = lowValue Y % 10 ^ Y.length := by
        rw [← hYlen]
        simpa only [List.append_nil] using hYlow
  have hPobs := sameObservation_phase_padding (L + gamma) d A L hd
  have hYobs := sameObservation_phase_padding (L + gamma) 18 B 1 (by decide)
  have hPcarry : (normalize P.reverse (if 10 ≤ d then 1 else 0)).2 = gamma :=
    hPobs.1.trans hcarry
  have hYcarry : (normalize Y.reverse 1).2 = gamma := hYobs.1
  have hHigh :
      fractionDigits (L + gamma) (rhoNum d P)
          (9 * 10 ^ P.length * 10 ^ gamma) =
        fractionDigits (L + gamma) (rhoNum 18 Y)
          (9 * 10 ^ Y.length * 10 ^ gamma) := by
    have hh := hPobs.2.2.trans (hhigh.trans hYobs.2.2.symm)
    change fractionDigits (L + gamma) (rhoNum d P)
        (9 * 10 ^ P.length *
          10 ^ (normalize P.reverse (if 10 ≤ d then 1 else 0)).2) =
      fractionDigits (L + gamma) (rhoNum 18 Y)
        (9 * 10 ^ Y.length * 10 ^ (normalize Y.reverse 1).2) at hh
    rw [hPcarry, hYcarry] at hh
    exact hh
  have hpositive : 0 < L + gamma := by dsimp only [L]; omega
  have hPX := high_prefix_append_value d gamma X S (by rw [hXlen]; exact hpositive)
  have hPY := high_prefix_append_value 18 gamma Y [] (by rw [hYlen]; exact hpositive)
  have htwo : rhoNum 18 ([] : List Nat) / (9 * 10 ^ ([] : List Nat).length) = 2 :=
    by decide
  rw [htwo] at hPY
  simp only [List.append_nil] at hPY
  have hhighValues : highValue X + rhoNum d S / (9 * 10 ^ S.length) =
      highValue Y + 2 := by
    rw [← hPX, ← hPY, hXlen, hYlen, ← hsplit]
    simpa only [hYlen] using congrArg highValue hHigh
  obtain ⟨hXY, htheta⟩ := boundary_values_rigidity X Y
    (rhoNum d S / (9 * 10 ^ S.length)) (hXlen.trans hYlen.symm)
    hXbound hYbound hYlarge hlowValues hhighValues
    (rho_quotient_le_two d S hd hSbound)
  obtain ⟨hd18, hSrep⟩ := (rho_quotient_eq_two_iff d S hd hSbound).mp htheta
  refine ⟨hd18, ?_⟩
  calc
    stripSuffix d A = stripSuffix d P :=
      (Agent116.Exterior.stripSuffix_append_replicate d A L).symm
    _ = stripSuffix 18 X := by
      rw [hsplit, hd18, hSrep, Agent116.Exterior.stripSuffix_append_replicate]
    _ = stripSuffix 18 Y := congrArg (stripSuffix 18) hXY
    _ = stripSuffix 18 B := stripSuffix_append_single 18 B

/-- One uniform finite cutoff recovers the phase and canonical core of a
phase-18 target among all bounded words at natural phases at most 18. -/
theorem phase18_canonical_fiber_of_observation
    (d : Nat) (A B : List Nat)
    (hd : d ≤ 18)
    (hA : ∀ x ∈ A, x ≤ 18) (hB : ∀ x ∈ B, x ≤ 18)
    (hobs : sameObservation (B.length + 2)
      { c := 18, B := B } { c := d, B := A }) :
    d = 18 ∧ stripSuffix d A = stripSuffix 18 B := by
  have hgamma : (normalize B.reverse 1).2 ≤ 1 :=
    normalize_carry_le B.reverse 1 (by simpa using hB) (by decide)
  have hlow := sameObservation_take (B.length + 1) (B.length + 2)
    _ _ (by omega) hobs
  have hhigh := sameObservation_take
    (B.length + 1 + (normalize B.reverse 1).2) (B.length + 2)
    _ _ (by omega) hobs
  exact phase18_canonical_fiber_of_prefixes d A B hd hA hB
    hobs.1 hlow.2.1 hhigh.2.2

/-- A valid phase-18 target is completely isolated, including its phase
and full word, without any upper bound on the competing word's width. -/
theorem phase18_valid_state_isolated
    (d : Nat) (A B : List Nat)
    (hd : d ≤ 18)
    (hvA : validOuter { c := d, B := A } = true)
    (hvB : validOuter { c := 18, B := B } = true)
    (hobs : sameObservation (B.length + 2)
      { c := 18, B := B } { c := d, B := A }) : d = 18 ∧ A = B := by
  obtain ⟨hd18, hcore⟩ := phase18_canonical_fiber_of_observation d A B hd
    (entries_le_of_valid d A hvA) (entries_le_of_valid 18 B hvB) hobs
  rw [stripSuffix_eq_of_valid d A hvA, stripSuffix_eq_of_valid 18 B hvB] at hcore
  exact ⟨hd18, hcore⟩

/-- The literal upper-boundary stream need not consist of decimal digits.
The state is valid and its actual carry is zero, but its first high output
is ten. No ordinary-template realization is asserted for this control. -/
theorem phase18_high_coefficient_ten :
    validOuter { c := 18, B := [8] } = true ∧
      (normalize ([8] : List Nat).reverse 1).2 = 0 ∧
      fractionDigits 1 (rhoNum 18 [8])
        (9 * 10 ^ ([8] : List Nat).length *
          10 ^ (normalize ([8] : List Nat).reverse 1).2) = [10] := by decide

#print axioms phase18_canonical_fiber_of_prefixes
#print axioms phase18_canonical_fiber_of_observation
#print axioms phase18_valid_state_isolated
#print axioms phase18_high_coefficient_ten

end Agent5.PhaseEighteenIsolation
