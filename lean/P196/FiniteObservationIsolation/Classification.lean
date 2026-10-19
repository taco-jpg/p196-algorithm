import P196.FiniteObservationIsolation.Family
import P196.FiniteObservationIsolation.ZeroControl
import P196.PhaseEighteenIsolation.Isolation
import P196.StreamNonisolation.Extension

/-!
# Finite isolation in the ten even exterior phases

A finite observation consists of the actual high carry and the two original
coordinate prefixes. The cutoff may depend on the target, but must identify
it against every valid competing state in the ten even phases, without a
bound on the competitor's width. The isolated targets are exactly all valid
phase-eighteen states and the empty phase-zero state.
-/

namespace Agent5.FiniteObservationIsolation

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams Agent5.FiniteExteriorHistories

/-- A target is identified by one finite original observation against every
valid state in the ten even phases, with no competing-width bound. -/
def finitelyIsolated (s : Outer) : Prop :=
  ∃ cut : Nat, ∀ q : Outer,
    q.c ∈ [0, 2, 4, 6, 8, 10, 12, 14, 16, 18] →
    validOuter q = true →
    sameObservation cut s q → q = s

/-- Among valid states in the ten even phases, a finite original observation
isolates exactly the upper boundary phase or the empty lower boundary state.
The observation retains the actual carry and both original streams. -/
theorem finitely_isolated_iff (c : Nat) (B : List Nat)
    (hc : c ∈ [0, 2, 4, 6, 8, 10, 12, 14, 16, 18])
    (hv : validOuter { c := c, B := B } = true) :
    finitelyIsolated { c := c, B := B } ↔
      c = 18 ∨ (c = 0 ∧ B = []) := by
  constructor
  · intro hisolated
    by_cases h18 : c = 18
    · exact Or.inl h18
    by_cases hzero : c = 0
    · subst c
      refine Or.inr ⟨rfl, ?_⟩
      by_cases hempty : B = []
      · exact hempty
      · exfalso
        obtain ⟨cut, hcut⟩ := hisolated
        obtain ⟨A, hwidth, hfamily⟩ :=
          arbitrarily_wide_zero_all_phase_same_observation cut 0 B hv hempty
        obtain ⟨hvalid, _, hobs⟩ := hfamily 0 (by decide)
        have heq := hcut { c := 0, B := A } (by simp) hvalid hobs
        have hword : A = B := congrArg Outer.B heq
        have hlen := congrArg List.length hword
        have hmax := Nat.le_max_left B.length 0
        omega
    · exfalso
      have hphase : nonneutralPhase c := by
        simp only [List.mem_cons, List.mem_nil_iff, or_false] at hc
        simp only [nonneutralPhase, List.mem_cons, List.mem_nil_iff, or_false]
        omega
      obtain ⟨cut, hcut⟩ := hisolated
      obtain ⟨A, hvalid, _, hwidth, hcarry, hlo, hhi⟩ :=
        Agent5.StreamNonisolation.arbitrarily_wide_valid_same_prefixes
          c cut 0 B hphase hv
      have hobs : sameObservation cut { c := c, B := B }
          { c := c, B := A } := ⟨hcarry, hlo, hhi⟩
      have heq := hcut { c := c, B := A } hc hvalid hobs
      have hword : A = B := congrArg Outer.B heq
      have hlen := congrArg List.length hword
      have hmax := Nat.le_max_left B.length 0
      omega
  · rintro (h18 | ⟨hzero, hempty⟩)
    · subst c
      refine ⟨B.length + 2, ?_⟩
      intro q hphase hvalid hobs
      rcases q with ⟨d, A⟩
      have hd : d ≤ 18 := by
        simp only [List.mem_cons, List.mem_nil_iff, or_false] at hphase
        omega
      obtain ⟨rfl, rfl⟩ :=
        Agent5.PhaseEighteenIsolation.phase18_valid_state_isolated
          d A B hd hvalid hv hobs
      rfl
    · subst c
      subst B
      refine ⟨1, ?_⟩
      intro q _ hvalid hobs
      rcases q with ⟨d, A⟩
      obtain ⟨rfl, rfl⟩ := zero_empty_state_isolated d A hvalid hobs
      rfl

#print axioms finitely_isolated_iff

end Agent5.FiniteObservationIsolation
