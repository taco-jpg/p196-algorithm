import GrowingSuffix

/-!
WIP target for the odd-center boundary of exact decimal palindrome suffix
realization. This file states the intended universal property and begins
the symmetry extension; it does not claim a complete proof.
-/

namespace Agent105.CeilHalfSuffix

open Lychrel196 DecimalDigits ExactLengthResidues

/-- Every nonzero-units integer admits an exact-width positive canonical
palindrome with the same residue modulo 10^k. -/
def UniversalSuffixRealization (k L : Nat) : Prop :=
  ∀ n : Nat, ¬ 10 ∣ n →
    ∃ P e : Nat, 0 < P ∧ Canonical P e L ∧ Palindrome P ∧
      P % (10 ^ k) = n % (10 ^ k)

/-- Candidate sharp range: a prescribed suffix can occupy at most the
low half plus the one shared odd center digit. -/
def CeilHalfRange (k L : Nat) : Prop :=
  0 < k ∧ 2 * k ≤ L + 1

/-- The mirrored outer-digit function remains symmetric when the two
prescribed blocks meet at the unique center position. -/
theorem outerDigits_symmetric_ceil (d : Nat → Nat) (k L i : Nat)
    (hL : 2 * k ≤ L + 1) (hi : i < L) :
    outerDigits d k L i = outerDigits d k L (L - 1 - i) := by
  have hinv : L - 1 - (L - 1 - i) = i := by omega
  simp only [outerDigits, hinv]
  by_cases ha : i < k
  · by_cases hb : L - 1 - i < k
    · have hcenter : i = L - 1 - i := by omega
      simp [ha, hb, hcenter]
    · simp [ha, hb]
  · by_cases hb : L - 1 - i < k
    · simp [ha, hb]
    · simp [ha, hb]

/-- Unproved research target. This is deliberately a proposition definition,
not an accepted theorem. A counterexample must be preserved if the proposed
converse is false under the exact original Canonical/Palindrome semantics. -/
def UniversalSuffixRealizationIffCeilHalf : Prop :=
  ∀ k L : Nat, 0 < k →
    (UniversalSuffixRealization k L ↔ 2 * k ≤ L + 1)

end Agent105.CeilHalfSuffix
