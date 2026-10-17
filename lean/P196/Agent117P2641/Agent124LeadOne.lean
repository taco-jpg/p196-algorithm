import P196.Agent117P2641.Agent124PrefixR

/-!
# Last-step bridge without a leading-digit hypothesis (Agent #124)

Agent #104's `PalindromeBridge.canonical_last_step` excludes a final overflow
from a leading target digit above one.  Here the overflow is excluded instead
by any target digit above two: an overflow step yields a palindrome only when
every pair sum is 0 or 11 (`DecimalDigits.step_palindrome_iff_overflow`), and
then every digit of the result is at most two.  This covers three-digit
prefixes `1, b, c` with `b ≥ 3` or `c ≥ 3`, such as 119.

The prefix endpoints of `Agent124.PrefixR` are restated with the premise
`2 ≤ a ∨ 3 ≤ b ∨ 3 ≤ c` in place of `2 ≤ a`.
-/

namespace Agent124.LeadOne

open DecimalDigits FoldedDecimal Lychrel196 OverflowCarryNormalization
open NormalizationBridge CarryHistory SevenColumnProjection
open SevenColumn.Certificate SevenColumn.ShortBoundary
open SevenColumnKernel.PalindromeBridge Agent124.PrefixK Agent124.PrefixR

/-- Every digit of a palindromic overflow output is at most two. -/
theorem overflow_palindrome_digits_le_two
    {n P L W : Nat} {d e : Nat → Nat}
    (hsource : Canonical n d L) (htarget : Canonical P e W)
    (hstep : step n = P) (hpal : Palindrome P)
    (hc : carry (columnSum d L) L = 1) :
    ∀ i, i < W → e i ≤ 2 := by
  have hnext : Canonical P (extended (columnSum d L) L) (L + 1) := by
    rw [← hstep]
    exact canonical_next_overflow n d L hsource hc
  obtain ⟨hwidth, hdigit⟩ := canonical_unique hnext htarget
  have hpal' : Palindrome (step (value d L)) := by
    rw [hsource.2.2.2, hstep]
    exact hpal
  obtain ⟨_, hall⟩ := (step_palindrome_iff_overflow d L hsource.1 hsource.2.1
    hsource.2.2.1 hc).mp hpal'
  have hcb := carry_bounded (columnSum d L) L (columnSum_bounded d L hsource.2.1)
  intro i hi
  rw [← hdigit i (by omega)]
  unfold extended
  split
  · rename_i hil
    have hq := hall i hil
    have hci := hcb i (by omega)
    unfold output
    rcases hq with hq | hq <;> rw [hq] <;> omega
  · omega

/-- A target digit above two rules out a final overflow. -/
theorem no_overflow_of_digit_gt_two
    {n P L W : Nat} {d e : Nat → Nat}
    (hsource : Canonical n d L) (htarget : Canonical P e W)
    (hstep : step n = P) (hpal : Palindrome P)
    {j : Nat} (hj : j < W) (hbig : 2 < e j) :
    carry (columnSum d L) L = 0 := by
  rcases actual_overflow_cases d L hsource.2.1 with hc | hc
  · exact hc
  · have := overflow_palindrome_digits_le_two hsource htarget hstep hpal hc j hj
    omega

/-- Agent #104's exact fixed-width last-step bridge, with the absence of a
final overflow as the hypothesis instead of a leading digit above one.
The proof follows `PalindromeBridge.canonical_last_step` line by line. -/
theorem canonical_last_step_of_no_overflow
    {n P L W : Nat} {d e : Nat → Nat}
    (hsource : Canonical n d L) (htarget : Canonical P e W)
    (hstep : step n = P) (hpal : Palindrome P)
    (hc : carry (columnSum d L) L = 0) :
    L = W ∧
      (∀ i, i ≤ L → carry (columnSum d L) i = 0) ∧
      (∀ i, i < L → columnSum d L i = e i) ∧
      (∀ i, i < L → columnSum d L i ≤ 9) := by
  have hnext : Canonical P (output (columnSum d L)) L := by
    rw [← hstep]
    exact canonical_next_no_overflow n d L hsource hc
  obtain ⟨hwidth, hdigit⟩ := canonical_unique hnext htarget
  have hp : Palindrome (value (output (columnSum d L)) L) := by
    rw [hnext.2.2.2]
    exact hpal
  have hs := (palindrome_value_iff (output (columnSum d L)) L
    hnext.2.1 (Or.inr hnext.2.2.1)).mp hp
  obtain ⟨hcarry, hpair⟩ := DecimalCarry.no_overflow_palindrome_has_no_carries
    L (columnSum d L) (carry (columnSum d L)) (output (columnSum d L))
    hsource.1 (columnSum_symmetric d L) hs
    (fun i _ => column_equation (columnSum d L) i) rfl hc
  refine ⟨hwidth, hcarry, ?_, ?_⟩
  · intro i hi
    exact (hpair i hi).trans (hdigit i hi)
  · intro i hi
    rw [hpair i hi]
    exact output_bounded _ i

/-- The final ordinary step into a palindrome beginning `a, b, c` produces an
initial word whenever `2 ≤ a`, `3 ≤ b` or `3 ≤ c`. -/
theorem canonical_last_step_initialK' (k a b c : Nat) (hk : 3 ≤ k)
    (habc : 2 ≤ a ∨ 3 ≤ b ∨ 3 ≤ c)
    {n P L : Nat} {d : Nat → Nat}
    (hsource : Canonical n d L) (hstep : step n = P) (hP : PalStarts3 a b c P) :
    projectK k (columnSum d L) L ∈ initialWordsK k a b c := by
  obtain ⟨hpal, e, W, htarget, hW, hea, heb, hec⟩ := hP
  have hc : carry (columnSum d L) L = 0 := by
    rcases habc with h | h | h
    · have hlead : 1 < e (W - 1) := by omega
      exact no_overflow_of_target_leading_gt_one hsource htarget hstep hlead
    · exact no_overflow_of_digit_gt_two hsource htarget hstep hpal
        (j := W - 2) (by omega) (by omega)
    · exact no_overflow_of_digit_gt_two hsource htarget hstep hpal
        (j := W - 3) (by omega) (by omega)
  obtain ⟨hwidth, _, hpair, hsmall⟩ :=
    canonical_last_step_of_no_overflow hsource htarget hstep hpal hc
  have hp : Palindrome (value e W) := by
    rw [htarget.2.2.2]
    exact hpal
  have hsym := (palindrome_value_iff e W htarget.2.1
    (Or.inr htarget.2.2.1)).mp hp
  apply target_project_mem_initialWordsK k a b c hk (columnSum d L) L
    (canonical_admissible n d L hsource) (by omega) hsmall
  refine ⟨?_, ?_, ?_⟩
  · rw [hpair 0 (by omega), hsym 0 (by omega)]
    simpa using hea
  · rw [hpair 1 (by omega), hsym 1 (by omega)]
    simpa only [Nat.sub_sub] using heb
  · rw [hpair 2 (by omega), hsym 2 (by omega)]
    simpa only [Nat.sub_sub] using hec

theorem ancestry_bound_of_R' (k a b c bound : Nat) (hk : 3 ≤ k)
    (habc : 2 ≤ a ∨ 3 ≤ b ∨ 3 ≤ c)
    (R : List Nat → Option Nat) (rows : RowsClosed k R) (short : ShortClosed k R)
    (initial : InitialBounded k a b c bound R) :
    ∀ A P t, 0 < A → PalStarts3 a b c P → orbit A t = P → t ≤ bound + 1 := by
  intro A P t hA hP hreach
  cases t with
  | zero => omega
  | succ t =>
      obtain ⟨d, L, hcan⟩ := canonical_exists A hA
      let q := columnSum d L
      have hadm : Admissible L q := canonical_admissible A d L hcan
      obtain ⟨e, he, hrep⟩ := iterPairs_representation A d q L t hcan (fun _ _ => rfl)
      have hlast : step (orbit A t) = P := hreach
      have hm := canonical_last_step_initialK' k a b c hk habc he hlast hP
      have hproj := projectK_congr k (columnSum e (iterPairs q L t).1)
        (iterPairs q L t).2 (iterPairs q L t).1 hrep
      rw [hproj] at hm
      obtain ⟨r, hr, hb⟩ := initial _ hm
      have ht := actual_iterPairs_rank_R (by omega) rows short q L hadm t hr
      omega

theorem no_196_of_R' (k a b c bound : Nat) (hk : 3 ≤ k)
    (habc : 2 ≤ a ∨ 3 ≤ b ∨ 3 ≤ c) (hb : bound + 1 ≤ 100)
    (R : List Nat → Option Nat) (rows : RowsClosed k R) (short : ShortClosed k R)
    (initial : InitialBounded k a b c bound R) :
    ∀ t, ¬ PalStarts3 a b c (orbit 196 t) :=
  no_196_target_of_ancestry_bound (PalStarts3 a b c) (bound + 1) hb
    (fun _ h => h.1) (ancestry_bound_of_R' k a b c bound hk habc R rows short initial)

end Agent124.LeadOne

#print axioms Agent124.LeadOne.overflow_palindrome_digits_le_two
#print axioms Agent124.LeadOne.no_overflow_of_digit_gt_two
#print axioms Agent124.LeadOne.canonical_last_step_of_no_overflow
#print axioms Agent124.LeadOne.canonical_last_step_initialK'
#print axioms Agent124.LeadOne.ancestry_bound_of_R'
#print axioms Agent124.LeadOne.no_196_of_R'
