import LychrelDigitSums

/-!
# Exact final-step bridge and a conditional ordinary-196 reduction

The final-step theorems below prove equation (2) of `P196_739_Proof.md`
for every positive source and every palindromic target whose leading
decimal digit exceeds one. Neither width preservation nor carry freedom
is assumed: both are proved from canonical decimal representations.

The final 196 corollary is deliberately conditional on a uniform bound
of 39 on the ancestry depth of 739-prefix palindromes. This file does not
prove that finite-graph certificate and does not assert the full 196
conjecture. The finite computation through time 100 is imported from the
existing kernel-checked `LychrelDigitSums` module.
-/

namespace SevenColumnKernel.PalindromeBridge

open DecimalDigits FoldedDecimal Lychrel196

/-- Canonical decimal representations of the same positive numeral have
the same width and agree at every position within that width. -/
theorem canonical_unique {n : Nat} {d e : Nat → Nat} {L W : Nat}
    (hd : Canonical n d L) (he : Canonical n e W) :
    L = W ∧ ∀ i, i < L → d i = e i := by
  have hL := DecimalQuantitativeMass.decimalLength_of_canonical n d L hd
  have hW := DecimalQuantitativeMass.decimalLength_of_canonical n e W he
  have hwidth : L = W := hL.symm.trans hW
  refine ⟨hwidth, ?_⟩
  clear hL hW
  subst W
  exact value_injective d e L hd.2.1 he.2.1
    (hd.2.2.2.trans he.2.2.2.symm)

/-- A target leading digit greater than one rules out an appended carry.
This uses the independently given canonical target representation, so
equal source and target widths are not a premise. -/
theorem no_overflow_of_target_leading_gt_one
    {n P L W : Nat} {d e : Nat → Nat}
    (hsource : Canonical n d L) (htarget : Canonical P e W)
    (hstep : step n = P) (hlead : 1 < e (W - 1)) :
    carry (columnSum d L) L = 0 := by
  rcases actual_overflow_cases d L hsource.2.1 with hc | hc
  · exact hc
  · have hnext : Canonical P (extended (columnSum d L) L) (L + 1) := by
      rw [← hstep]
      exact canonical_next_overflow n d L hsource hc
    obtain ⟨hwidth, hdigit⟩ := canonical_unique hnext htarget
    have heL : 1 < e L := by
      simpa only [← hwidth, Nat.add_sub_cancel] using hlead
    have hlast := hdigit L (by omega)
    simp only [extended, Nat.lt_irrefl, if_false, hc] at hlast
    omega

/-- Exact fixed-width form of the final-step bridge: the output has the
source width, all computed carries vanish, and each source pair-column
is the corresponding target digit. -/
theorem canonical_last_step
    {n P L W : Nat} {d e : Nat → Nat}
    (hsource : Canonical n d L) (htarget : Canonical P e W)
    (hstep : step n = P) (hpal : Palindrome P)
    (hlead : 1 < e (W - 1)) :
    L = W ∧
      (∀ i, i ≤ L → carry (columnSum d L) i = 0) ∧
      (∀ i, i < L → columnSum d L i = e i) ∧
      (∀ i, i < L → columnSum d L i ≤ 9) := by
  have hc := no_overflow_of_target_leading_gt_one hsource htarget hstep hlead
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

/-- Numeric form: for any positive ordinary predecessor, its canonical
width equals the target width and its complete pair-column word equals
the target's complete digit word. -/
theorem numeric_last_step
    {n P W : Nat} {e : Nat → Nat}
    (hn : 0 < n) (htarget : Canonical P e W)
    (hstep : step n = P) (hpal : Palindrome P)
    (hlead : 1 < e (W - 1)) :
    ∃ d, Canonical n d W ∧
      (∀ i, i ≤ W → carry (columnSum d W) i = 0) ∧
      (∀ i, i < W → columnSum d W i = e i) ∧
      (∀ i, i < W → columnSum d W i ≤ 9) := by
  obtain ⟨d, L, hsource⟩ := canonical_exists n hn
  obtain ⟨hwidth, hcarry, hpair, hsmall⟩ :=
    canonical_last_step hsource htarget hstep hpal hlead
  subst L
  exact ⟨d, hsource, hcarry, hpair, hsmall⟩

/-- An ordinary numeral has leading decimal digits 739. Width is exact
and digits are indexed from the units end. -/
def Starts739 (P : Nat) : Prop :=
  ∃ e W, Canonical P e W ∧ 3 ≤ W ∧
    e (W - 1) = 7 ∧ e (W - 2) = 3 ∧ e (W - 3) = 9

/-- The target family; palindromicity is explicit rather than inferred
from a finite prefix. -/
def PalindromeStarts739 (P : Nat) : Prop :=
  Palindrome P ∧ Starts739 P

/-- The final predecessor of any 739-prefix palindrome has low-end
pair-column prefix 7,3,9, has the exact target width, and has no carries. -/
theorem predecessor_of_739_palindrome
    {n P : Nat} (hn : 0 < n) (hstep : step n = P)
    (hP : PalindromeStarts739 P) :
    ∃ d e W, Canonical n d W ∧ Canonical P e W ∧ 3 ≤ W ∧
      (∀ i, i ≤ W → carry (columnSum d W) i = 0) ∧
      (∀ i, i < W → columnSum d W i = e i) ∧
      columnSum d W 0 = 7 ∧ columnSum d W 1 = 3 ∧
      columnSum d W 2 = 9 := by
  obtain ⟨hpal, e, W, htarget, hW, h7, h3, h9⟩ := hP
  have hlead : 1 < e (W - 1) := by omega
  obtain ⟨d, hsource, hcarry, hpair, _⟩ :=
    numeric_last_step hn htarget hstep hpal hlead
  have hp : Palindrome (value e W) := by
    rw [htarget.2.2.2]
    exact hpal
  have hsym := (palindrome_value_iff e W htarget.2.1
    (Or.inr htarget.2.2.1)).mp hp
  refine ⟨d, e, W, hsource, htarget, hW, hcarry, hpair, ?_, ?_, ?_⟩
  · rw [hpair 0 (by omega), hsym 0 (by omega)]
    simpa using h7
  · rw [hpair 1 (by omega), hsym 1 (by omega)]
    simpa only [Nat.sub_sub] using h3
  · rw [hpair 2 (by omega), hsym 2 (by omega)]
    simpa only [Nat.sub_sub] using h9

/-- Generic ordinary-196 reduction. A uniform ancestry bound within the
already verified first 100 steps excludes the entire target family from
the infinite 196 orbit. The uniform bound is an explicit premise. -/
theorem no_196_target_of_ancestry_bound
    (Target : Nat → Prop) (B : Nat) (hB : B ≤ 100)
    (hpal : ∀ P, Target P → Palindrome P)
    (hdepth : ∀ A P t, 0 < A → Target P → orbit A t = P → t ≤ B) :
    ∀ t, ¬ Target (orbit 196 t) := by
  intro t htarget
  have ht : t ≤ B := hdepth 196 (orbit 196 t) t (by decide) htarget rfl
  exact no_palindrome_through_100 t (by omega) (hpal _ htarget)

/-- Conditional endpoint of the seven-column certificate program.
Proving the 39-step ancestry premise would exclude all 739-prefix
palindromes from the ordinary 196 orbit, at every time. -/
theorem no_196_739_palindrome_of_ancestry_bound39
    (hdepth : ∀ A P t, 0 < A → PalindromeStarts739 P →
      orbit A t = P → t ≤ 39) :
    ∀ t, ¬ PalindromeStarts739 (orbit 196 t) := by
  exact no_196_target_of_ancestry_bound PalindromeStarts739 39 (by decide)
    (fun _ h => h.1) hdepth

#print axioms canonical_unique
#print axioms no_overflow_of_target_leading_gt_one
#print axioms canonical_last_step
#print axioms numeric_last_step
#print axioms predecessor_of_739_palindrome
#print axioms no_196_target_of_ancestry_bound
#print axioms no_196_739_palindrome_of_ancestry_bound39

end SevenColumnKernel.PalindromeBridge
