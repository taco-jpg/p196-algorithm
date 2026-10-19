import P196.Foundations.LychrelDigitSums

/-!
Complementary coefficient scans start with two zero carries. A neutral
column preserves that mismatch; the first non-nine column repairs it.
Every later complementary column then preserves a carry sum of one.
The empty scan is included.
-/

set_option autoImplicit false

namespace TerminalCarryCensus

open DecimalDigits

/-- Complementary scans have terminal carry sum zero exactly for an all-nine
prefix, including the empty prefix, and terminal carry sum one otherwise. -/
theorem complementary_carry_sum (q r : Nat → Nat) (L : Nat)
    (hcomp : ∀ i, i < L → q i + r i = 18) :
    DecimalDigits.carry q L + DecimalDigits.carry r L =
      if (List.range L).all (fun i => q i == 9) then 0 else 1 := by
  revert hcomp
  induction L with
  | zero =>
    intro _
    simp [carry]
  | succ L ih =>
    intro hcomp
    have hprev := ih (fun i hi => hcomp i (by omega))
    have hcol := hcomp L (by omega)
    have hrange :
        (List.range (L + 1)).all (fun i => q i == 9) =
          ((List.range L).all (fun i => q i == 9) && (q L == 9)) := by
      simp only [List.range_succ, List.all_append, List.all_cons,
        List.all_nil, Bool.and_true]
    rw [hrange]
    cases hn : (List.range L).all (fun i => q i == 9) with
    | false =>
      have hsum : carry q L + carry r L = 1 := by
        simpa only [hn] using hprev
      have hnext := (AstraLanguages.complementary_column
        (q L) (r L) (carry q L) (carry r L) hcol hsum).1
      simpa [carry, hn] using hnext
    | true =>
      have hsum : carry q L + carry r L = 0 := by
        simpa only [hn] using hprev
      have hqzero : carry q L = 0 := by omega
      have hrzero : carry r L = 0 := by omega
      by_cases hq : q L = 9
      · have hr : r L = 9 := by omega
        simp [carry, hn, hqzero, hrzero, hq, hr]
      · have hnext := (AstraLanguages.mismatched_column_repair
          (q L) (r L) hcol hq).1
        simpa [carry, hn, hqzero, hrzero, hq] using hnext

#print axioms complementary_carry_sum

end TerminalCarryCensus
