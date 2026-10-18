import P196.Drafts.D20261014SafePrefixOverflowSafeRuns.OverflowSafeRuns

/-!
Finite-horizon safety from finite mirrored blocks of nine digits.
The finite counting and density argument is written in README.md;
it is not asserted to be formalized by these lemmas.
-/

namespace FiniteHorizonBlocks

open Lychrel196 DecimalDigits FoldedDecimal OverflowCarryNormalization
  CarryHistory DecimalSafeRuns OverflowSafeRuns

/-- Run length sufficient for the first R+1 positive steps. -/
def blockLength (R : Nat) : Nat := min (1 + 2 * R) (1 + (7 * R + 4) / 4)

theorem blockLength_positive (R : Nat) : 0 < blockLength R := by
  unfold blockLength
  omega

/-- Uses the better of the previous two-column bound and the new
overflow-sensitive bound; no probabilistic hypothesis is involved. -/
theorem safe_prefix_of_run (n : Nat) (d q : Nat → Nat) (L R k : Nat)
    (hc : Canonical n d L) (hr : ∀ i, i < L → columnSum d L i = q i)
    (ha : Admissible L q) (hk : k ≤ R)
    (h18 : HasRun18 q L (blockLength R)) :
    ¬ Palindrome (orbit n (k + 1)) := by
  by_cases h : 1 + 2 * R ≤ 1 + (7 * R + 4) / 4
  · have he : blockLength R = 1 + 2 * R := by
      unfold blockLength
      omega
    rw [he] at h18
    exact iter_not_palindrome_of_run n d q L k hc hr ha
      (hasRun18_mono q L _ _ (by omega) h18)
  · have he : blockLength R = 1 + (7 * R + 4) / 4 := by
      unfold blockLength
      omega
    rw [he] at h18
    exact safe_prefix_of_uniform_run n d q L R k hc hr ha hk h18

/-- The low-index interval and its reflected interval consist of nines.
Disjointness is needed for the counting argument, not for this implication. -/
def MirroredNines (d : Nat → Nat) (L a r : Nat) : Prop :=
  a + r ≤ L ∧ ∀ i, a ≤ i → i < a + r → d i = 9 ∧ d (L - 1 - i) = 9

theorem mirroredNines_hasRun18 (d : Nat → Nat) (L a r : Nat)
    (hm : MirroredNines d L a r) : HasRun18 (columnSum d L) L r := by
  refine ⟨a, hm.1, ?_⟩
  intro i hia hir
  obtain ⟨hlo, hhi⟩ := hm.2 i hia hir
  simp only [columnSum, reflected, hlo, hhi]

/-- A deterministic certificate for safety at every positive index 1,...,R+1. -/
theorem mirroredNines_safe_prefix (n : Nat) (d : Nat → Nat) (L a R k : Nat)
    (hc : Canonical n d L) (hk : k ≤ R)
    (hm : MirroredNines d L a (blockLength R)) :
    ¬ Palindrome (orbit n (k + 1)) := by
  apply safe_prefix_of_run n d (columnSum d L) L R k hc
    (by intro i hi; rfl) (NormalizationBridge.canonical_admissible n d L hc) hk
  exact mirroredNines_hasRun18 d L a (blockLength R) hm

#print axioms blockLength_positive
#print axioms safe_prefix_of_run
#print axioms mirroredNines_hasRun18
#print axioms mirroredNines_safe_prefix

end FiniteHorizonBlocks
