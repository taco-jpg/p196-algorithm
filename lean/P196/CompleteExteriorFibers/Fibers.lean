import P196.CompleteExteriorFibers.Recovery
import P196.CompleteExteriorFibers.LowTail
import P196.PhaseStreamRecovery.CanonicalFibers

/-!
# At most two valid states in a complete stream fiber

The complete low stream identifies the phase among the ten even phases.
At a fixed phase at most eighteen, the remaining ambiguity is at most the
two possible actual high carries. Two representatives with the same carry
coincide by the finite recovery theorem. The published interior-phase
classification retains its stronger singleton conclusion.
-/

namespace Agent5.CompleteExteriorFibers

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams

/-- Equal complete original streams have the same phase among the ten
even phases, without an a priori competing-width bound. -/
theorem phase_eq_of_complete_streams (c d : Nat) (A B : List Nat)
    (hc : c ∈ [0, 2, 4, 6, 8, 10, 12, 14, 16, 18])
    (hd : d ∈ [0, 2, 4, 6, 8, 10, 12, 14, 16, 18])
    (hA : ∀ x ∈ A, x ≤ 18) (hB : ∀ x ∈ B, x ≤ 18)
    (hstreams : sameStreams { c := c, B := A } { c := d, B := B }) :
    c = d := by
  exact phase_eq_of_low_prefix c d (max A.length B.length + 2)
    A B hc hd hA hB (Nat.le_refl _) (hstreams _).1.symm

private theorem carry_le_of_valid (c : Nat) (B : List Nat)
    (hv : validOuter { c := c, B := B } = true) :
    (normalize B.reverse (if 10 ≤ c then 1 else 0)).2 ≤ 1 := by
  apply normalize_carry_le B.reverse _
    (fun x hx => entries_le_of_valid c B hv x (List.mem_reverse.mp hx))
  split <;> decide

/-- At any fixed natural phase at most eighteen, three valid words with
the same two complete streams contain an equal pair. The actual carry is
not part of the supplied stream equality. -/
theorem same_phase_complete_fiber_at_most_two
    (c : Nat) (A B C : List Nat) (hc : c ≤ 18)
    (hvA : validOuter { c := c, B := A } = true)
    (hvB : validOuter { c := c, B := B } = true)
    (hvC : validOuter { c := c, B := C } = true)
    (hAB : sameStreams { c := c, B := A } { c := c, B := B })
    (hAC : sameStreams { c := c, B := A } { c := c, B := C }) :
    A = B ∨ A = C ∨ B = C := by
  have hgA := carry_le_of_valid c A hvA
  have hgB := carry_le_of_valid c B hvB
  have hgC := carry_le_of_valid c C hvC
  have hpair :
      (normalize A.reverse (if 10 ≤ c then 1 else 0)).2 =
          (normalize B.reverse (if 10 ≤ c then 1 else 0)).2 ∨
      (normalize A.reverse (if 10 ≤ c then 1 else 0)).2 =
          (normalize C.reverse (if 10 ≤ c then 1 else 0)).2 ∨
      (normalize B.reverse (if 10 ≤ c then 1 else 0)).2 =
          (normalize C.reverse (if 10 ≤ c then 1 else 0)).2 := by omega
  rcases hpair with hABcarry | hACcarry | hBCcarry
  · exact Or.inl (same_phase_eq_of_streams_and_carry
      c B A hc hvB hvA hABcarry.symm hAB).symm
  · exact Or.inr (Or.inl (same_phase_eq_of_streams_and_carry
      c C A hc hvC hvA hACcarry.symm hAC).symm)
  · have hCB : sameStreams { c := c, B := C } { c := c, B := B } := by
      intro cut
      exact ⟨(hAB cut).1.trans (hAC cut).1.symm,
        (hAB cut).2.trans (hAC cut).2.symm⟩
    exact Or.inr (Or.inr (same_phase_eq_of_streams_and_carry
      c B C hc hvB hvC hBCcarry hCB))

/-- Among the ten even phases, no complete two-stream fiber contains three
distinct original valid states, with arbitrary and unequal word widths. -/
theorem complete_fiber_at_most_two (s a b : Outer)
    (hs : s.c ∈ [0, 2, 4, 6, 8, 10, 12, 14, 16, 18])
    (ha : a.c ∈ [0, 2, 4, 6, 8, 10, 12, 14, 16, 18])
    (hb : b.c ∈ [0, 2, 4, 6, 8, 10, 12, 14, 16, 18])
    (hvs : validOuter s = true) (hva : validOuter a = true)
    (hvb : validOuter b = true)
    (hsa : sameStreams s a) (hsb : sameStreams s b) :
    s = a ∨ s = b ∨ a = b := by
  rcases s with ⟨c, S⟩
  rcases a with ⟨d, A⟩
  rcases b with ⟨e, B⟩
  have hcd := phase_eq_of_complete_streams c d S A hs ha
    (entries_le_of_valid c S hvs) (entries_le_of_valid d A hva) hsa
  have hce := phase_eq_of_complete_streams c e S B hs hb
    (entries_le_of_valid c S hvs) (entries_le_of_valid e B hvb) hsb
  subst d
  subst e
  have hc : c ≤ 18 := by
    simp only [List.mem_cons, List.mem_nil_iff, or_false] at hs
    omega
  rcases same_phase_complete_fiber_at_most_two c S A B hc hvs hva hvb hsa hsb
    with hSA | hSB | hAB
  · left
    cases hSA
    rfl
  · right
    left
    cases hSB
    rfl
  · right
    right
    cases hAB
    rfl

/-- A valid interior-phase target is the unique valid state in its complete
two-stream fiber even when competitors may use either boundary phase.
The original interior classification supplies the word recovery. -/
theorem interior_complete_fiber_singleton (c d : Nat) (A B : List Nat)
    (hc : nonneutralPhase c)
    (hd : d ∈ [0, 2, 4, 6, 8, 10, 12, 14, 16, 18])
    (hvA : validOuter { c := c, B := A } = true)
    (hvB : validOuter { c := d, B := B } = true)
    (hstreams : sameStreams { c := c, B := A } { c := d, B := B }) :
    c = d ∧ A = B := by
  have hcEven : c ∈ [0, 2, 4, 6, 8, 10, 12, 14, 16, 18] := by
    simp only [nonneutralPhase, List.mem_cons, List.mem_nil_iff, or_false] at hc
    simp only [List.mem_cons, List.mem_nil_iff, or_false]
    omega
  have hphase := phase_eq_of_complete_streams c d A B hcEven hd
    (entries_le_of_valid c A hvA) (entries_le_of_valid d B hvB) hstreams
  subst d
  refine ⟨rfl, ?_⟩
  have h := (Agent5.PhaseStreamRecovery.all_streams_eq_iff c c B A hc hc
    (entries_le_of_valid c B hvB) (entries_le_of_valid c A hvA)).mp hstreams
  have hword := h.2
  rw [Agent5.PhaseEighteenIsolation.stripSuffix_eq_of_valid c B hvB,
    Agent5.PhaseEighteenIsolation.stripSuffix_eq_of_valid c A hvA] at hword
  exact hword.symm

#print axioms phase_eq_of_complete_streams
#print axioms same_phase_complete_fiber_at_most_two
#print axioms complete_fiber_at_most_two
#print axioms interior_complete_fiber_singleton

end Agent5.CompleteExteriorFibers
