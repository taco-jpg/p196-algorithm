import P196.MaximalDigitSplitFibers.AllTargets
import P196.MaximalDigitSplitFibers.SubmaxEquality

/-!
Agent #7: exact maximum and second-largest complete digit-splitting fibers.
The final bound quantifies over arbitrary integer targets at a fixed source
width; explicit complete fibers attain the bound at every covered parity.
-/

namespace Agent7.MaximalDigitSplitFibers

open Agent101 Lychrel196

/-- The second-largest numerical fiber has exactly one inner factor nine,
with every other factor maximal. This requires a positive inner length. -/
theorem numericFiber_submax_iff (s : Nat) (h : List Nat) (c : Option Nat)
    (hlen : 0 < h.length) :
    (numericFiber (s :: h) c).length = 81 * 10 ^ (h.length - 1) ↔
      (s = 9 ∨ s = 10) ∧ singleInnerDefect h ∧ centerCount c = 1 := by
  rw [length_numericFiber]
  exact profileCount_submax_iff s h c hlen

/-- The arbitrary-target gap and complete ordinary-integer attainers.
The universal bound includes empty fibers, and every witness concerns
exactly one source width, given explicitly by its inner length and center. -/
theorem sharp_fixed_width_preimages_gap (k : Nat) (c : Option Nat)
    (hc : centerCount c = 1) :
    (∀ Y L : Nat, ∀ xs : List Nat,
      4 ≤ L →
      xs.Nodup →
      (∀ n, n ∈ xs ↔ decimalWidth n L ∧ step n = Y) →
      xs.length ≠ 9 * 10 ^ (L / 2 - 1) →
      xs.length ≤ 81 * 10 ^ (L / 2 - 2)) ∧
    ∃ target : Nat, ∃ xs : List Nat,
      xs.Nodup ∧
      (∀ n, n ∈ xs ↔
        decimalWidth n (2 * (k + 2) + c.toList.length) ∧ step n = target) ∧
      xs.length = 81 * 10 ^ k ∧ xs.length < 9 * 10 ^ (k + 1) := by
  refine ⟨?_, submax_complete_numeric_fiber k c hc⟩
  intro Y L xs hL hxs hm hne
  exact fixed_width_preimages_gap Y L xs hL hxs hm hne

#print axioms numericFiber_submax_iff
#print axioms sharp_fixed_width_preimages_gap

end Agent7.MaximalDigitSplitFibers
