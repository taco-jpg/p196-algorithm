import P196.FiniteObservationIsolation.Extension

/-!
# One wider valid word at all ten even phases

The existing universal word at phase zero retains a nonempty target's
positive head and ends in one. It is therefore valid at every natural
phase except one. Choosing enough zero padding gives one arbitrarily wide
canonical word with the same original observation at all ten even phases.
-/

namespace Agent5.FiniteObservationIsolation

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.FiniteExteriorHistories Agent5.UniversalPhasePrefixes

/-- The zero-phase extension is valid at every natural phase except its
terminal coefficient one. The nonempty target supplies the positive head. -/
theorem zero_extension_valid (d : Nat) (B : List Nat) (m : Nat)
    (hd : d ≠ 1)
    (hv : validOuter { c := 0, B := B } = true) (hne : B ≠ []) :
    validOuter { c := d, B := universalWord 0 B m } = true := by
  have hB := entries_le_of_valid 0 B hv
  have hall : ∀ x ∈ universalWord 0 B m, x ≤ 18 := by
    intro x hx
    change x ∈ (B ++ List.replicate m 0) ++ [1] at hx
    rcases List.mem_append.mp hx with hx | hx
    · rcases List.mem_append.mp hx with hx | hx
      · exact hB x hx
      · rw [List.eq_of_mem_replicate hx]
        decide
    · have heq := List.mem_singleton.mp hx
      omega
  simp only [validOuter, Bool.and_eq_true, List.all_eq_true,
    decide_eq_true_eq]
  refine ⟨⟨hall, ?_⟩, ?_⟩
  · cases B with
    | nil => exact False.elim (hne rfl)
    | cons b bs =>
        have hb : 0 < b := by
          simp only [validOuter, Bool.and_eq_true, decide_eq_true_eq] at hv
          exact hv.1.2
        simpa [universalWord] using hb
  · simp [universalWord, relayLetter, List.getLast?_append, Ne.symm hd]

/-- Every finite observation of a nonempty valid zero-phase target admits
one arbitrarily wider canonical word at all ten even phases. The word is
chosen before the alternative phase, and the actual carry is observed. -/
theorem arbitrarily_wide_zero_all_phase_same_observation
    (cut W : Nat) (B : List Nat)
    (hv : validOuter { c := 0, B := B } = true) (hne : B ≠ []) :
    ∃ A : List Nat,
      max B.length W < A.length ∧
      ∀ d : Nat, d ∈ [0, 2, 4, 6, 8, 10, 12, 14, 16, 18] →
        validOuter { c := d, B := A } = true ∧
        stripSuffix d A = A ∧
        sameObservation cut { c := 0, B := B } { c := d, B := A } := by
  refine ⟨universalWord 0 B (max cut W), ?_, ?_⟩
  · rw [universalWord_length]
    have := Nat.le_max_right cut W
    omega
  · intro d hd
    have hdFacts : d ≤ 18 ∧ d ≠ 1 := by
      simp only [List.mem_cons, List.mem_nil_iff, or_false] at hd
      omega
    have hvA := zero_extension_valid d B (max cut W) hdFacts.2 hv hne
    exact ⟨hvA,
      Agent5.PhaseEighteenIsolation.stripSuffix_eq_of_valid d _ hvA,
      zero_extension_sameObservation d cut (max cut W) B hdFacts.1
        (Nat.le_max_left cut W)⟩

#print axioms zero_extension_valid
#print axioms arbitrarily_wide_zero_all_phase_same_observation

end Agent5.FiniteObservationIsolation
