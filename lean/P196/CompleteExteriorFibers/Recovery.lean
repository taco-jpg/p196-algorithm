import P196.CompleteExteriorFibers.Definitions
import P196.CompleteExteriorFibers.Values

/-!
# Finite recovery at a fixed phase with the actual carry

Phase padding puts both bounded words at one positive width. Their low
prefixes determine the low positional residues, while the high prefixes,
using the equal actual carries, determine their high positional values.
The existing phase-suffix retraction then recovers the canonical words.
Every natural phase at most eighteen is allowed, including odd phases.
-/

namespace Agent5.CompleteExteriorFibers

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams Agent5.FiniteExteriorHistories
open Agent5.PhaseEighteenIsolation

/-- At every fixed phase at most eighteen, sufficiently long original
prefixes and the actual carry determine the canonical coefficient word.
No positive-head or initial suffix-trimming assumption is required. -/
theorem same_phase_core_eq_of_observation
    (c cut : Nat) (A B : List Nat) (hc : c ≤ 18)
    (hA : ∀ x ∈ A, x ≤ 18) (hB : ∀ x ∈ B, x ≤ 18)
    (hcut : max A.length B.length + 2 ≤ cut)
    (hobs : sameObservation cut { c := c, B := B } { c := c, B := A }) :
    stripSuffix c A = stripSuffix c B := by
  let N := max A.length B.length + 1
  have hAN : A.length ≤ N := by
    have := Nat.le_max_left A.length B.length
    omega
  have hBN : B.length ≤ N := by
    have := Nat.le_max_right A.length B.length
    omega
  have hNpos : 0 < N := by omega
  have hNcut : N + 1 ≤ cut := by omega
  let X := A ++ List.replicate (N - A.length) c
  let Y := B ++ List.replicate (N - B.length) c
  have hXlen : X.length = N := by
    simp only [X, List.length_append, List.length_replicate]
    omega
  have hYlen : Y.length = N := by
    simp only [Y, List.length_append, List.length_replicate]
    omega
  have hX : ∀ x ∈ X, x ≤ 18 := by
    have h := coefficientPrefix_bounded N { c := c, B := A } hc hA
    rw [coefficientPrefix_of_length_le N { c := c, B := A } hAN] at h
    exact h
  have hY : ∀ x ∈ Y, x ≤ 18 := by
    have h := coefficientPrefix_bounded N { c := c, B := B } hc hB
    rw [coefficientPrefix_of_length_le N { c := c, B := B } hBN] at h
    exact h
  have hpA := sameObservation_phase_padding cut c A (N - A.length) hc
  have hpB := sameObservation_phase_padding cut c B (N - B.length) hc
  have hpadded : sameObservation cut { c := c, B := Y } { c := c, B := X } := by
    exact ⟨hpA.1.trans (hobs.1.trans hpB.1.symm),
      hpA.2.1.trans (hobs.2.1.trans hpB.2.1.symm),
      hpA.2.2.trans (hobs.2.2.trans hpB.2.2.symm)⟩
  have hlo := (sameObservation_take N cut
    { c := c, B := Y } { c := c, B := X } (by omega) hpadded).2.1
  have hXL := low_prefix_append_value c X []
  have hYL := low_prefix_append_value c Y []
  simp only [List.append_nil, hXlen] at hXL
  simp only [List.append_nil, hYlen] at hYL
  have hresidue := congrArg lowValue hlo
  rw [hXL, hYL] at hresidue
  let k : Nat := if 10 ≤ c then 1 else 0
  let g := (normalize Y.reverse k).2
  have hk : k ≤ 1 := by dsimp only [k]; split <;> decide
  have hg : g ≤ 1 := normalize_carry_le Y.reverse k
    (fun x hx => hY x (List.mem_reverse.mp hx)) hk
  have hhi := (sameObservation_take (N + g) cut
    { c := c, B := Y } { c := c, B := X } (by omega) hpadded).2.2
  have hXH := high_prefix_append_value c g X [] (by rw [hXlen]; omega)
  have hYH := high_prefix_append_value c g Y [] (by rw [hYlen]; omega)
  have hempty : rhoNum c [] = c := by simp [rhoNum, highValue]
  simp only [List.append_nil, List.length_nil, Nat.pow_zero, Nat.mul_one,
    hempty, hXlen] at hXH
  simp only [List.append_nil, List.length_nil, Nat.pow_zero, Nat.mul_one,
    hempty, hYlen] at hYH
  have hhigh := congrArg highValue hhi
  simp only [hXlen, hYlen, hpadded.1] at hhigh
  change highValue (fractionDigits (N + g) (rhoNum c X)
      (9 * 10 ^ N * 10 ^ g)) =
    highValue (fractionDigits (N + g) (rhoNum c Y)
      (9 * 10 ^ N * 10 ^ g)) at hhigh
  rw [hXH, hYH] at hhigh
  have hword : X = Y := eq_of_low_residue_highValue X Y
    (hXlen.trans hYlen.symm) hX hY
    (by simpa only [hYlen] using hresidue) (by omega)
  have hcore := congrArg (stripSuffix c) hword
  simpa only [X, Y, Agent116.Exterior.stripSuffix_append_replicate] using hcore

/-- Original valid states are fully recovered by the same finite
observation at any fixed natural phase at most eighteen. -/
theorem same_phase_valid_eq_of_observation
    (c cut : Nat) (A B : List Nat) (hc : c ≤ 18)
    (hvA : validOuter { c := c, B := A } = true)
    (hvB : validOuter { c := c, B := B } = true)
    (hcut : max A.length B.length + 2 ≤ cut)
    (hobs : sameObservation cut { c := c, B := B } { c := c, B := A }) :
    A = B := by
  have h := same_phase_core_eq_of_observation c cut A B hc
    (entries_le_of_valid c A hvA) (entries_le_of_valid c B hvB) hcut hobs
  simpa only [stripSuffix_eq_of_valid c A hvA, stripSuffix_eq_of_valid c B hvB] using h

/-- At a known phase, equality of both complete original streams recovers
valid words whenever the separately calculated high carries also agree. -/
theorem same_phase_eq_of_streams_and_carry
    (c : Nat) (A B : List Nat) (hc : c ≤ 18)
    (hvA : validOuter { c := c, B := A } = true)
    (hvB : validOuter { c := c, B := B } = true)
    (hcarry : (normalize A.reverse (if 10 ≤ c then 1 else 0)).2 =
      (normalize B.reverse (if 10 ≤ c then 1 else 0)).2)
    (hstreams : sameStreams { c := c, B := B } { c := c, B := A }) :
    A = B := by
  apply same_phase_valid_eq_of_observation c
    (max A.length B.length + 2) A B hc hvA hvB (Nat.le_refl _)
  exact ⟨hcarry, hstreams _⟩

#print axioms same_phase_core_eq_of_observation
#print axioms same_phase_valid_eq_of_observation
#print axioms same_phase_eq_of_streams_and_carry

end Agent5.CompleteExteriorFibers
