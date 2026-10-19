import P196.OrdinaryImageCensus.Balance
import P196.TerminalCarryCensus.Terminal

/-!
# Exact ordinary-image counts by decimal width

The original coefficient-word counts and terminal-carry counts evaluate
the two source-width contributions. The already-counted common targets
give the exact correction for distinct numerical outputs.
-/

set_option autoImplicit false

namespace OrdinaryImageCensus

open Agent124.PrefixK SevenColumn.ShortBoundary DecimalDigits
open CrossWidthTargetRecurrence

private theorem wordCount_even (k : Nat) :
    SymmetricCarryCensus.wordCount (2 * k + 2) = 18 * 19 ^ k := by
  have hzero : 2 * k + 2 ≠ 0 := by omega
  have hone : 2 * k + 2 ≠ 1 := by omega
  have hhalf : (2 * k + 2) / 2 - 1 = k := by omega
  have heven : (2 * k + 2) % 2 = 0 := by omega
  simp only [SymmetricCarryCensus.wordCount, hzero, hone, if_false,
    hhalf, heven, if_true, Nat.mul_one]

private theorem wordCount_odd (k : Nat) :
    SymmetricCarryCensus.wordCount (2 * k + 3) = 180 * 19 ^ k := by
  have hzero : 2 * k + 3 ≠ 0 := by omega
  have hone : 2 * k + 3 ≠ 1 := by omega
  have hhalf : (2 * k + 3) / 2 - 1 = k := by omega
  have hodd : (2 * k + 3) % 2 ≠ 0 := by omega
  simp only [SymmetricCarryCensus.wordCount, hzero, hone, if_false,
    hhalf, hodd]
  omega

private theorem twice_even_terminal (m : Nat) :
    2 * ((19 ^ m - 1) / 2) + 1 = 19 ^ m := by
  have hr : 19 ^ m % 2 = 1 := by
    induction m with
    | zero => decide
    | succ m ih =>
      rw [Nat.pow_succ, Nat.mul_mod, ih]
  have hp : 0 < 19 ^ m := Nat.pow_pos (by decide)
  omega

/-- No positive ordinary target has decimal width zero. -/
theorem count_zero : (widthTargets 0).length = 0 := by
  have h : OrdinaryImageSparsity.allBelow (10 ^ 0) = [] :=
    OrdinaryImageSparsity.allBelow_eq_nil_small 1 (by decide)
  simp only [widthTargets, h, List.filter_nil, List.length_nil]

/-- The one-digit ordinary outputs are counted with the empty shorter
source-width contribution retained. -/
theorem count_one : (widthTargets 1).length = 4 := by
  have h := count_balance 1 (by decide)
  have hzero : (symWords 0).countP
      (fun w => carry (wordFun w) 0 == 1) = 0 := by
    simpa using TerminalCarryCensus.terminal_ones_even 0
  have hone : (symWords 1).countP
      (fun w => carry (wordFun w) 1 == 1) = 5 := by
    simpa using TerminalCarryCensus.terminal_ones_odd 0
  simp [SymmetricCarryCensus.wordCount, targetCount, hzero, hone] at h
  omega

/-- Exact distinct ordinary-output count at every positive even width,
with the common-target correction indexed by the shorter source width. -/
theorem count_even (k : Nat) :
    2 * (widthTargets (2 * k + 2)).length +
        2 * targetCount (2 * k + 1) = 27 * 19 ^ k + 1 := by
  have h := count_balance (2 * k + 2) (by omega)
  have heven : (symWords (2 * k + 2)).countP
      (fun w => carry (wordFun w) (2 * k + 2) == 1) =
      (19 ^ (k + 1) - 1) / 2 := by
    simpa only [show 2 * (k + 1) = 2 * k + 2 by omega] using
      TerminalCarryCensus.terminal_ones_even (k + 1)
  have hodd := TerminalCarryCensus.terminal_ones_odd k
  rw [show 2 * k + 2 - 1 = 2 * k + 1 by omega,
    wordCount_even, heven, hodd] at h
  have ht := twice_even_terminal (k + 1)
  rw [Nat.pow_succ] at h ht
  omega

/-- Exact distinct ordinary-output count at every odd width at least
three, including the shorter-width overlap correction. -/
theorem count_odd (k : Nat) :
    2 * (widthTargets (2 * k + 3)).length +
        2 * targetCount (2 * k + 2) + 1 = 189 * 19 ^ k := by
  have h := count_balance (2 * k + 3) (by omega)
  have hodd : (symWords (2 * k + 3)).countP
      (fun w => carry (wordFun w) (2 * k + 3) == 1) =
      5 * 19 ^ (k + 1) := by
    simpa only [show 2 * (k + 1) + 1 = 2 * k + 3 by omega] using
      TerminalCarryCensus.terminal_ones_odd (k + 1)
  have heven : (symWords (2 * k + 2)).countP
      (fun w => carry (wordFun w) (2 * k + 2) == 1) =
      (19 ^ (k + 1) - 1) / 2 := by
    simpa only [show 2 * (k + 1) = 2 * k + 2 by omega] using
      TerminalCarryCensus.terminal_ones_even (k + 1)
  rw [show 2 * k + 3 - 1 = 2 * k + 2 by omega,
    wordCount_odd, hodd, heven] at h
  have ht := twice_even_terminal (k + 1)
  rw [Nat.pow_succ] at h ht
  omega

end OrdinaryImageCensus

#print axioms OrdinaryImageCensus.count_zero
#print axioms OrdinaryImageCensus.count_one
#print axioms OrdinaryImageCensus.count_even
#print axioms OrdinaryImageCensus.count_odd
