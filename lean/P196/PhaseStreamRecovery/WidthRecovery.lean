import P196.PhaseStreamRecovery.Injectivity
import P196.TrimmedStreamObservation.WidthRecovery

/-!
# Recovery of a trimmed exterior state without a supplied width or phase

Padding each word with its own phase preserves its original low and high
streams. The common-width recovery theorem therefore identifies the phases.
The existing fixed-phase theorem then recovers the original trimmed words.
Positive heads are not required.
-/

namespace Agent5.PhaseStreamRecovery

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams

/-- A common complete cutoff determines both the nonneutral phase and the
bounded trimmed word, even when the initial widths differ. -/
theorem state_eq_of_common_prefixes (c d cut : Nat) (A B : List Nat)
    (hc : nonneutralPhase c) (hd : nonneutralPhase d)
    (hA : ∀ x ∈ A, x ≤ 18) (hB : ∀ x ∈ B, x ≤ 18)
    (htA : A.getLast? ≠ some c) (htB : B.getLast? ≠ some d)
    (hcut : max A.length B.length + 1 ≤ cut)
    (hlo : adicNumeratorDigits cut (zValue c A - (c : Int)) =
      adicNumeratorDigits cut (zValue d B - (d : Int)))
    (hhi : fractionDigits cut (rhoNum c A)
        (9 * 10 ^ A.length *
          10 ^ (normalize A.reverse (if 10 ≤ c then 1 else 0)).2) =
      fractionDigits cut (rhoNum d B)
        (9 * 10 ^ B.length *
          10 ^ (normalize B.reverse (if 10 ≤ d then 1 else 0)).2)) :
    c = d ∧ A = B := by
  let N := max A.length B.length
  let A' := A ++ List.replicate (N - A.length) c
  let B' := B ++ List.replicate (N - B.length) d
  have hlenA : A'.length = N := by
    have hle : A.length ≤ N := Nat.le_max_left _ _
    simp only [A', List.length_append, List.length_replicate]
    omega
  have hlenB : B'.length = N := by
    have hle : B.length ≤ N := Nat.le_max_right _ _
    simp only [B', List.length_append, List.length_replicate]
    omega
  have hc18 : c ≤ 18 := (phase_facts c 0 hc (by decide)).2.2.2.2
  have hd18 : d ≤ 18 := (phase_facts d 0 hd (by decide)).2.2.2.2
  have hA' : ∀ x ∈ A', x ≤ 18 := by
    intro x hx
    rcases List.mem_append.mp hx with hx | hx
    · exact hA x hx
    · rw [List.eq_of_mem_replicate hx]
      exact hc18
  have hB' : ∀ x ∈ B', x ≤ 18 := by
    intro x hx
    rcases List.mem_append.mp hx with hx | hx
    · exact hB x hx
    · rw [List.eq_of_mem_replicate hx]
      exact hd18
  have hphase : c = d := by
    have hstate : c = d ∧ A' = B' := by
      apply state_eq_of_streams_at_cutoff c d cut A' B' hc hd hA' hB'
        (hlenA.trans hlenB.symm)
      · rw [hlenA]
        exact hcut
      · dsimp only [A', B']
        rw [Agent5.TrimmedStreamObservation.phase_padding_low,
          Agent5.TrimmedStreamObservation.phase_padding_low]
        exact hlo
      · dsimp only [A', B']
        rw [Agent5.TrimmedStreamObservation.phase_padding_high c cut A _ hc,
          Agent5.TrimmedStreamObservation.phase_padding_high d cut B _ hd]
        exact hhi
    exact hstate.1
  subst d
  refine ⟨rfl, ?_⟩
  exact Agent5.TrimmedStreamObservation.exterior_eq_of_common_prefixes
    c cut A B hc hA hB htA htB hcut hlo hhi

/-- Original exterior validity supplies the coefficient bounds and the
terminal trimming. Each nonneutral phase hypothesis remains explicit. -/
theorem valid_state_eq_of_common_prefixes (c d cut : Nat) (A B : List Nat)
    (hc : nonneutralPhase c) (hd : nonneutralPhase d)
    (hvA : validOuter { c := c, B := A } = true)
    (hvB : validOuter { c := d, B := B } = true)
    (hcut : max A.length B.length + 1 ≤ cut)
    (hlo : adicNumeratorDigits cut (zValue c A - (c : Int)) =
      adicNumeratorDigits cut (zValue d B - (d : Int)))
    (hhi : fractionDigits cut (rhoNum c A)
        (9 * 10 ^ A.length *
          10 ^ (normalize A.reverse (if 10 ≤ c then 1 else 0)).2) =
      fractionDigits cut (rhoNum d B)
        (9 * 10 ^ B.length *
          10 ^ (normalize B.reverse (if 10 ≤ d then 1 else 0)).2)) :
    c = d ∧ A = B := by
  exact state_eq_of_common_prefixes c d cut A B hc hd
    (entries_le_of_valid c A hvA) (entries_le_of_valid d B hvB)
    (last_ne_of_valid c A hvA) (last_ne_of_valid d B hvB) hcut hlo hhi

#print axioms state_eq_of_common_prefixes
#print axioms valid_state_eq_of_common_prefixes

end Agent5.PhaseStreamRecovery
