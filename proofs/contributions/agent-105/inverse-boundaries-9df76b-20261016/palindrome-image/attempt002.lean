import Lychrel196Research
import Agent105WidthSupport9df76b

/-!
# Which positive decimal palindromes have reverse-and-add predecessors?

This module formalizes the target classification in the preserved
`research/persist_inverse_notes.txt`, section 3.  Digits and iteration use
the unchanged ordinary-natural-number definitions in Lychrel196Research.
No counting, arbitrary-time termination, or 196 avoidance theorem is claimed.
-/

namespace P196.Agent105.PalindromeImage9df76b

open DecimalDigits FoldedDecimal Lychrel196 Agent105WidthSupport9df76b

/-- A palindromic target whose only possible middle digit is even has a
canonical predecessor at the same actual width.  Its complete column word
is the target digit word and every carry, including the final one, is zero.
The explicit existing `realizingDigit` construction is retained. -/
theorem same_width_zero_carry_predecessor
    (P : Nat) (e : Nat → Nat) (W : Nat)
    (htarget : Canonical P e W) (hpal : Palindrome P)
    (hcenter : W % 2 = 0 ∨ e (W / 2) % 2 = 0) :
    ∃ n, 0 < n ∧ Canonical n (realizingDigit e W) W ∧
      step n = P ∧
      (∀ i, i < W → columnSum (realizingDigit e W) W i = e i) ∧
      (∀ i, i ≤ W → carry (columnSum (realizingDigit e W) W) i = 0) := by
  have hsym : ∀ i, i < W → e i = e (W - 1 - i) := by
    apply (palindrome_value_iff e W htarget.2.1
      (Or.inr htarget.2.2.1)).mp
    simpa only [htarget.2.2.2] using hpal
  have hmiddle : ∀ i, i < W → i = W - 1 - i → e i % 2 = 0 := by
    intro i hi heq
    rcases hcenter with heven | hmid
    · omega
    · have hiMid : i = W / 2 := by omega
      simpa only [hiMid] using hmid
  have houter : 0 < e 0 := by
    have hs := hsym 0 htarget.1
    have hlead := htarget.2.2.1
    simpa only [Nat.sub_zero] using hs ▸ hlead
  have hbound : ∀ i, i < W → e i ≤ 18 := by
    intro i hi
    have hb := htarget.2.1 i hi
    omega
  let d := realizingDigit e W
  have hd : ∀ i, i < W → d i ≤ 9 := realizingDigit_bounded e W hbound
  have hlead : 0 < d (W - 1) :=
    realizingDigit_leading_positive e W htarget.1 houter hsym hmiddle
  have hrep : ∀ i, i < W → columnSum d W i = e i :=
    realizingDigit_columns e W hsym hmiddle
  have hsmall : ∀ i, i < W → columnSum d W i ≤ 9 := by
    intro i hi
    rw [hrep i hi]
    exact htarget.2.1 i hi
  have hcarry : ∀ i, i ≤ W → carry (columnSum d W) i = 0 :=
    (DecimalCarry.small_digit_sums_give_palindrome W (columnSum d W)
      (carry (columnSum d W)) (output (columnSum d W))
      (columnSum_symmetric d W) hsmall
      (fun i _ => column_equation (columnSum d W) i) rfl).1
  have hstep : step (value d W) = P := by
    rw [step_value d W hd (Or.inr hlead), value_output]
    exact (value_congr (columnSum d W) e W hrep).trans htarget.2.2.2
  exact ⟨value d W, value_positive d W htarget.1 hlead,
    ⟨htarget.1, hd, hlead, rfl⟩, hstep, hrep, hcarry⟩

/-- If an unchanged-width output is palindromic, an odd middle output
digit is twice the actual input middle digit. -/
theorem no_overflow_palindrome_center_even
    (n : Nat) (d : Nat → Nat) (L : Nat)
    (hsource : Canonical n d L)
    (hcarry : carry (columnSum d L) L = 0)
    (hpal : Palindrome (step n)) (hodd : L % 2 = 1) :
    output (columnSum d L) (L / 2) % 2 = 0 := by
  have hp : Palindrome (step (value d L)) := by
    simpa only [hsource.2.2.2] using hpal
  have hsmall := (step_palindrome_iff_no_overflow d L hsource.1
    hsource.2.1 hsource.2.2.1 hcarry).mp hp
  have hzero := (DecimalCarry.small_digit_sums_give_palindrome L (columnSum d L)
    (carry (columnSum d L)) (output (columnSum d L))
    (columnSum_symmetric d L) hsmall
    (fun i _ => column_equation (columnSum d L) i) rfl).1
  have hmid : L / 2 < L := by omega
  have hmirror : L - 1 - L / 2 = L / 2 := by omega
  have hpairs : columnSum d L (L / 2) = 2 * d (L / 2) := by
    simp only [columnSum, reflected, hmirror]
    omega
  have hcol := column_equation (columnSum d L) (L / 2)
  rw [hzero (L / 2) (by omega), hzero (L / 2 + 1) (by omega), hpairs] at hcol
  omega

/-- Overflow from an even-width source to a palindrome produces middle
digit zero or two.  The two middle source columns are distinct reflections;
this conclusion does not assume an even central source coefficient. -/
theorem overflow_palindrome_center_zero_or_two
    (n : Nat) (d : Nat → Nat) (L : Nat)
    (hsource : Canonical n d L)
    (hcarry : carry (columnSum d L) L = 1)
    (hpal : Palindrome (step n)) (heven : L % 2 = 0) :
    extended (columnSum d L) L (L / 2) = 0 ∨
      extended (columnSum d L) L (L / 2) = 2 := by
  let q := columnSum d L
  have hp : Palindrome (step (value d L)) := by
    simpa only [hsource.2.2.2] using hpal
  have hspecial : q 0 = 11 ∧ ∀ i, i < L → q i = 0 ∨ q i = 11 :=
    (step_palindrome_iff_overflow d L hsource.1 hsource.2.1
      hsource.2.2.1 hcarry).mp hp
  have hL : 0 < L := hsource.1
  have hmidPos : 0 < L / 2 := by omega
  have hmid : L / 2 < L := by omega
  have hprev : L / 2 - 1 < L := by omega
  have hreflect : L - 1 - (L / 2 - 1) = L / 2 := by omega
  have hsame : q (L / 2 - 1) = q (L / 2) := by
    simpa only [hreflect] using columnSum_symmetric d L (L / 2 - 1) hprev
  have hcb : carry q (L / 2 - 1) ≤ 1 :=
    carry_bounded q L (columnSum_bounded d L hsource.2.1)
      (L / 2 - 1) (by omega)
  have hcmid : carry q (L / 2) =
      (q (L / 2 - 1) + carry q (L / 2 - 1)) / 10 := by
    have hi : L / 2 - 1 + 1 = L / 2 := by omega
    simpa only [hi] using
      (show carry q (L / 2 - 1 + 1) =
        (q (L / 2 - 1) + carry q (L / 2 - 1)) / 10 from rfl)
  rcases hspecial.2 (L / 2) hmid with hz | ho
  · have hcz : carry q (L / 2) = 0 := by
      rw [hcmid, hsame, hz]
      omega
    left
    change extended q L (L / 2) = 0
    simp [extended, hmid, output, hz, hcz]
  · have hco : carry q (L / 2) = 1 := by
      rw [hcmid, hsame, ho]
      omega
    right
    change extended q L (L / 2) = 2
    simp [extended, hmid, output, ho, hco]

/-- Every positive predecessor of a positive palindrome target satisfies
the target parity obstruction, irrespective of the predecessor's width
and of whether its final carry is zero or one. -/
theorem target_parity_of_positive_predecessor
    (P : Nat) (e : Nat → Nat) (W : Nat)
    (htarget : Canonical P e W) (hpal : Palindrome P)
    (n : Nat) (hn : 0 < n) (hstep : step n = P) :
    W % 2 = 0 ∨ e (W / 2) % 2 = 0 := by
  by_cases heven : W % 2 = 0
  · exact Or.inl heven
  right
  have hodd : W % 2 = 1 := by omega
  obtain ⟨d, L, hsource⟩ := canonical_exists n hn
  have hpalstep : Palindrome (step n) := by
    simpa only [hstep] using hpal
  rcases actual_overflow_cases d L hsource.2.1 with hc | hc
  · have hout : Canonical P (output (columnSum d L)) L := by
      simpa only [hstep] using canonical_next_no_overflow n d L hsource hc
    obtain ⟨hwidth, hdigit⟩ := canonical_width_and_digits_unique hout htarget
    have hLodd : L % 2 = 1 := by omega
    have hmid : L / 2 < L := by omega
    have hcenter := no_overflow_palindrome_center_even n d L hsource hc hpalstep hLodd
    have heq := hdigit (L / 2) hmid
    rw [heq, hwidth] at hcenter
    exact hcenter
  · have hout : Canonical P (extended (columnSum d L) L) (L + 1) := by
      simpa only [hstep] using canonical_next_overflow n d L hsource hc
    obtain ⟨hwidth, hdigit⟩ := canonical_width_and_digits_unique hout htarget
    have hLeven : L % 2 = 0 := by omega
    have hmid : L / 2 < L + 1 := by omega
    have hmidwidth : W / 2 = L / 2 := by omega
    have heq := hdigit (L / 2) hmid
    have hcenter := overflow_palindrome_center_zero_or_two n d L
      hsource hc hpalstep hLeven
    rw [heq] at hcenter
    rw [hmidwidth]
    rcases hcenter with hz | ht
    · rw [hz]
    · rw [ht]

/-- Complete one-step image classification for ordinary positive decimal
palindromes.  A palindrome has a positive reverse-and-add predecessor
exactly when its width is even or its middle digit is even.  The predecessor
is existentially quantified over all positive natural numbers. -/
theorem palindrome_target_has_positive_predecessor_iff
    (P : Nat) (e : Nat → Nat) (W : Nat)
    (htarget : Canonical P e W) (hpal : Palindrome P) :
    (∃ n, 0 < n ∧ step n = P) ↔
      W % 2 = 0 ∨ e (W / 2) % 2 = 0 := by
  constructor
  · rintro ⟨n, hn, hstep⟩
    exact target_parity_of_positive_predecessor P e W htarget hpal n hn hstep
  · intro hcenter
    obtain ⟨n, hn, _, hstep, _, _⟩ :=
      same_width_zero_carry_predecessor P e W htarget hpal hcenter
    exact ⟨n, hn, hstep⟩

#print axioms same_width_zero_carry_predecessor
#print axioms no_overflow_palindrome_center_even
#print axioms overflow_palindrome_center_zero_or_two
#print axioms target_parity_of_positive_predecessor
#print axioms palindrome_target_has_positive_predecessor_iff

end P196.Agent105.PalindromeImage9df76b
