import Std
namespace ExactLengthResidues

theorem bounded_sequence_repeats (q : Nat) :
    ∀ (f : Nat → Nat), (∀ i, f i < q) → ∃ i j, i < j ∧ f i = f j := by
  classical
  induction q with
  | zero =>
    intro f hf
    have := hf 0
    omega
  | succ q ih =>
    intro f hf
    by_cases hit : ∃ j, 0 < j ∧ f 0 = f j
    · obtain ⟨j, hj, heq⟩ := hit
      exact ⟨0, j, hj, heq⟩
    · have hav : ∀ n, f (n + 1) ≠ f 0 := by
        intro n heq
        apply hit
        exact ⟨n + 1, by omega, heq.symm⟩
      let g : Nat → Nat := fun n =>
        if f (n + 1) < f 0 then f (n + 1) else f (n + 1) - 1
      have hg : ∀ n, g n < q := by
        intro n
        have hn := hf (n + 1)
        have hzero := hf 0
        have hne := hav n
        dsimp [g]
        split <;> omega
      obtain ⟨i, j, hij, heq⟩ := ih g hg
      refine ⟨i + 1, j + 1, by omega, ?_⟩
      have hi := hav i
      have hj := hav j
      dsimp [g] at heq
      split at heq <;> split at heq <;> omega

end ExactLengthResidues
#print axioms ExactLengthResidues.bounded_sequence_repeats
