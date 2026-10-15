import TwoDigitProjection
import TwoDigitGrowth
import PalindromeBridge

/-!
# Agent #113: number-level digits, the outer triple, and the last two steps

Everything here is stated for ordinary natural numbers through
`Lychrel196.step`. `digitAt n i` is the `i`-th decimal digit from the units
end, `width n` the canonical decimal length, and `tri n` the three outermost
pair sums of `n` (outermost first). The bridge lemmas connect these to the
canonical representations of `LychrelDigitSums`.

Main results:

* `tri_step`: for `width n ≥ 3`, `tri (step n) = nextT (tri n) e` for the
  actual carry `e ≤ 1`, and the width grows by exactly `topT (tri n) e`.
* `width_step_eq_of_small_descending`: Lemma 1 at the number level.
* `no_overflow_of_descending_target`, `descending_last_step`,
  `last_step_triple`: the immediate predecessor of a palindrome beginning
  with digits `a > b` has width at least three, all pair sums at most nine,
  and outer triple `(a, b, c)` with `c ≤ 9`. This adapts Agent #104's
  reviewed `PalindromeBridge.canonical_last_step` (leading digit above one)
  to every strictly descending prefix, including `a = 1`.

No claim about 196 or decimal Lychrel existence is made in this module.
-/

namespace Agent113.TwoDigit

open DecimalDigits FoldedDecimal Lychrel196 DecimalQuantitativeMass

/-! ## Digits, width and the outer triple -/

/-- The `i`-th decimal digit, counted from the units position. -/
def digitAt (n i : Nat) : Nat := n / 10 ^ i % 10

/-- Canonical decimal width (zero has width zero). -/
def width (n : Nat) : Nat := decimalLength n

/-- The pair sum in position `i` of the canonical numeral of `n`. -/
def pairAt (n i : Nat) : Nat := digitAt n i + digitAt n (width n - 1 - i)

/-- The three outermost pair sums, outermost first. -/
def tri (n : Nat) : Nat × Nat × Nat := (pairAt n 0, pairAt n 1, pairAt n 2)

/-- `nextTriple` and `topCarry` on triples. -/
def nextT (w : Nat × Nat × Nat) (e : Nat) : Nat × Nat × Nat :=
  nextTriple w.1 w.2.1 w.2.2 e

def topT (w : Nat × Nat × Nat) (e : Nat) : Nat :=
  topCarry w.1 w.2.1 w.2.2 e

theorem value_digit (d : Nat → Nat) (L : Nat) (hd : ∀ i, i < L → d i ≤ 9) :
    ∀ i, i < L → value d L / 10 ^ i % 10 = d i := by
  induction L generalizing d with
  | zero => intro i hi; omega
  | succ L ih =>
    intro i hi
    have hd0 := hd 0 (by omega)
    rw [value_shift]
    cases i with
    | zero => simp; omega
    | succ i =>
      have h := ih (fun j => d (j + 1)) (fun j hj => hd (j + 1) (by omega)) i
        (by omega)
      have hdiv : (d 0 + 10 * value (fun i => d (i + 1)) L) / 10 =
          value (fun i => d (i + 1)) L := by omega
      rw [Nat.pow_succ', ← Nat.div_div_eq_div_mul, hdiv]
      exact h

theorem canonical_width {n : Nat} {d : Nat → Nat} {L : Nat}
    (h : Canonical n d L) : width n = L :=
  decimalLength_of_canonical n d L h

theorem canonical_digitAt {n : Nat} {d : Nat → Nat} {L : Nat}
    (h : Canonical n d L) : ∀ i, i < L → digitAt n i = d i := by
  intro i hi
  simp only [digitAt]
  rw [← h.2.2.2]
  exact value_digit d L h.2.1 i hi

theorem canonical_pairAt {n : Nat} {d : Nat → Nat} {L : Nat}
    (h : Canonical n d L) : ∀ i, i < L → pairAt n i = columnSum d L i := by
  intro i hi
  simp only [pairAt, columnSum, reflected, canonical_width h]
  rw [canonical_digitAt h i hi, canonical_digitAt h (L - 1 - i) (by omega)]

theorem canonical_tri {n : Nat} {d : Nat → Nat} {L : Nat}
    (h : Canonical n d L) (hL : 3 ≤ L) :
    tri n = (columnSum d L 0, columnSum d L 1, columnSum d L 2) := by
  simp only [tri, canonical_pairAt h 0 (by omega), canonical_pairAt h 1 (by omega),
    canonical_pairAt h 2 (by omega)]

/-- The outer triple of a canonical numeral of width at least three lies in
the finite box `1 ≤ s0 ≤ 18`, `s1, s2 ≤ 18`. -/
theorem tri_box (n : Nat) (hn : 0 < n) (hw : 3 ≤ width n) :
    1 ≤ (tri n).1 ∧ (tri n).1 ≤ 18 ∧ (tri n).2.1 ≤ 18 ∧ (tri n).2.2 ≤ 18 := by
  obtain ⟨d, L, hcan⟩ := canonical_exists n hn
  have hwL := canonical_width hcan
  rw [hwL] at hw
  rw [canonical_tri hcan hw]
  have hb := columnSum_bounded d L hcan.2.1
  have hlead := hcan.2.2.1
  have h0 : columnSum d L 0 = d 0 + d (L - 1) := by
    simp [columnSum, reflected]
  refine ⟨?_, hb 0 (by omega), hb 1 (by omega), hb 2 (by omega)⟩
  show 1 ≤ columnSum d L 0
  omega

/-! ## Width facts -/

theorem width_ge_three (m : Nat) (h : 100 ≤ m) : 3 ≤ width m := by
  simp only [width]
  rw [decimalLength]
  simp only [show m ≠ 0 by omega, ↓reduceDIte]
  rw [decimalLength]
  simp only [show m / 10 ≠ 0 by omega, ↓reduceDIte]
  rw [decimalLength]
  simp only [show m / 10 / 10 ≠ 0 by omega, ↓reduceDIte]
  omega

theorem width_three (m : Nat) (h1 : 100 ≤ m) (h2 : m < 1000) : width m = 3 := by
  simp only [width]
  rw [decimalLength]
  simp only [show m ≠ 0 by omega, ↓reduceDIte]
  rw [decimalLength]
  simp only [show m / 10 ≠ 0 by omega, ↓reduceDIte]
  rw [decimalLength]
  simp only [show m / 10 / 10 ≠ 0 by omega, ↓reduceDIte]
  rw [show m / 10 / 10 / 10 = 0 by omega, decimalLength_zero]

/-- Explicit outer triple of a three-digit number. -/
def tri3 (m : Nat) : Nat × Nat × Nat :=
  (m % 10 + m / 100 % 10, m / 10 % 10 + m / 10 % 10, m / 100 % 10 + m % 10)

theorem tri_eq_tri3 (m : Nat) (h1 : 100 ≤ m) (h2 : m < 1000) : tri m = tri3 m := by
  simp only [tri, tri3, pairAt, width_three m h1 h2, digitAt]
  simp

/-! ## The projection for ordinary numbers -/

theorem tri_step (n : Nat) (hn : 0 < n) (hw : 3 ≤ width n) :
    ∃ e, e ≤ 1 ∧ tri (step n) = nextT (tri n) e ∧
      width (step n) = width n + topT (tri n) e := by
  obtain ⟨d, L, hcan⟩ := canonical_exists n hn
  have hwL := canonical_width hcan
  rw [hwL] at hw ⊢
  obtain ⟨k, rfl⟩ : ∃ k, L = k + 3 := ⟨L - 3, by omega⟩
  have htri := canonical_tri hcan hw
  have hb := carry_bounded (columnSum d (k + 3)) (k + 3)
    (columnSum_bounded d (k + 3) hcan.2.1)
  obtain ⟨_, _, e3⟩ := high_carries d k
  refine ⟨carry (columnSum d (k + 3)) k, hb k (by omega), ?_⟩
  rw [htri]
  simp only [nextT, topT]
  rcases actual_overflow_cases d (k + 3) hcan.2.1 with hc | hc
  · have hnext := canonical_next_no_overflow n d (k + 3) hcan hc
    rw [canonical_tri hnext (by omega), canonical_width hnext]
    refine ⟨triple_no_overflow d k hc, ?_⟩
    have : topCarry (columnSum d (k + 3) 0) (columnSum d (k + 3) 1)
        (columnSum d (k + 3) 2) (carry (columnSum d (k + 3)) k) = 0 := by
      rw [← e3]; exact hc
    omega
  · have hnext := canonical_next_overflow n d (k + 3) hcan hc
    rw [canonical_tri hnext (by omega), canonical_width hnext]
    refine ⟨triple_overflow d k hc, ?_⟩
    have : topCarry (columnSum d (k + 3) 0) (columnSum d (k + 3) 1)
        (columnSum d (k + 3) 2) (carry (columnSum d (k + 3)) k) = 1 := by
      rw [← e3]; exact hc
    omega

/-! ## Lemma 1 at the number level -/

theorem width_step_eq_of_small_descending (m : Nat) (hm : 0 < m)
    (hsmall : ∀ i, i < width (step m) → pairAt (step m) i ≤ 9)
    (hdesc : pairAt (step m) 1 < pairAt (step m) 0) :
    width (step m) = width m := by
  obtain ⟨d, n, hcan⟩ := canonical_exists m hm
  rw [canonical_width hcan]
  rcases actual_overflow_cases d n hcan.2.1 with hc | hc
  · exact canonical_width (canonical_next_no_overflow m d n hcan hc)
  · exfalso
    have hnext := canonical_next_overflow m d n hcan hc
    have hwn := canonical_width hnext
    have hn1 : 1 ≤ n := hcan.1
    have hsm : ∀ i, i < n + 1 →
        columnSum (extended (columnSum d n) n) (n + 1) i ≤ 9 := by
      intro i hi
      rw [← canonical_pairAt hnext i hi]
      exact hsmall i (by omega)
    have hle := overflow_not_descending d n hn1 hcan.2.1 hc hsm
    rw [← canonical_pairAt hnext 0 (by omega),
      ← canonical_pairAt hnext 1 (by omega)] at hle
    omega

/-! ## The target family and the last step -/

/-- The canonical numeral of `P` begins with the two digits `a, b`
(most significant first). Width is exact; digits are indexed from the
units end. -/
def StartsTwo (a b P : Nat) : Prop :=
  ∃ e W, Canonical P e W ∧ 2 ≤ W ∧ e (W - 1) = a ∧ e (W - 2) = b

/-- The target family: palindromes beginning with `a, b`. -/
def PalindromeStartsTwo (a b P : Nat) : Prop :=
  Palindrome P ∧ StartsTwo a b P

/-- A palindrome whose two leading digits strictly descend cannot be the
overflowing image of reverse-and-add. (If it were, its leading digit would be
the appended carry 1, its units digit would be 1, so the outer pair sum of
the source is 11 and the second digit would be at least 1.) -/
theorem no_overflow_of_descending_target
    {n P L W : Nat} {d e : Nat → Nat}
    (hsource : Canonical n d L) (htarget : Canonical P e W)
    (hstep : step n = P) (hpal : Palindrome P) (hW : 2 ≤ W)
    (hdesc : e (W - 2) < e (W - 1)) :
    carry (columnSum d L) L = 0 := by
  rcases actual_overflow_cases d L hsource.2.1 with hc | hc
  · exact hc
  · exfalso
    have hnext : Canonical P (extended (columnSum d L) L) (L + 1) := by
      rw [← hstep]; exact canonical_next_overflow n d L hsource hc
    obtain ⟨hwidth, hdigit⟩ :=
      SevenColumnKernel.PalindromeBridge.canonical_unique hnext htarget
    have hp : Palindrome (value (extended (columnSum d L) L) (L + 1)) := by
      rw [hnext.2.2.2]; exact hpal
    have hsym := (palindrome_value_iff _ (L + 1) hnext.2.1
      (Or.inr hnext.2.2.1)).mp hp
    have h0 := hsym 0 (by omega)
    rw [show L + 1 - 1 - 0 = L by omega] at h0
    have hL := hsource.1
    have hext0 : extended (columnSum d L) L 0 = output (columnSum d L) 0 := by
      simp [extended, hL]
    have hextL : extended (columnSum d L) L L = 1 := by simp [extended, hc]
    have htop : e (W - 1) = 1 := by
      rw [← hwidth, show L + 1 - 1 = L by omega, ← hdigit L (by omega), hextL]
    have hout0 : output (columnSum d L) 0 = 1 := by rw [← hext0, h0, hextL]
    have hsecond : e (W - 2) = extended (columnSum d L) L (L - 1) := by
      rw [← hwidth, show L + 1 - 2 = L - 1 by omega, hdigit (L - 1) (by omega)]
    by_cases hL1 : L = 1
    · subst hL1
      rw [hsecond, show 1 - 1 = 0 by rfl, hext0, hout0] at hdesc
      omega
    · have hextm : extended (columnSum d L) L (L - 1) = output (columnSum d L) (L - 1) := by
        simp [extended, show L - 1 < L by omega]
      have hcolTop := column_equation (columnSum d L) (L - 1)
      rw [show L - 1 + 1 = L by omega, hc] at hcolTop
      have hsymq := columnSum_symmetric d L 0 (by omega)
      rw [Nat.sub_zero] at hsymq
      have hcol0 : output (columnSum d L) 0 + 10 * carry (columnSum d L) 1 =
          columnSum d L 0 + 0 := column_equation (columnSum d L) 0
      have hq0 := columnSum_bounded d L hsource.2.1 0 (by omega)
      have hcb := carry_bounded (columnSum d L) L (columnSum_bounded d L hsource.2.1)
        (L - 1) (by omega)
      rw [hsecond, hextm, htop] at hdesc
      rw [← hsymq] at hcolTop
      omega

/-- The final step into a descending-prefix palindrome: the predecessor has
the target width, and its pair-sum word equals the target's digit word.
This adapts Agent #104's `PalindromeBridge.canonical_last_step` (which
assumes a leading digit above one) to every strictly descending prefix,
including leading digit one. -/
theorem descending_last_step
    {n P W : Nat} {e : Nat → Nat} (hn : 0 < n)
    (htarget : Canonical P e W) (hstep : step n = P) (hpal : Palindrome P)
    (hW : 2 ≤ W) (hdesc : e (W - 2) < e (W - 1)) :
    ∃ d, Canonical n d W ∧ (∀ i, i < W → columnSum d W i = e i) ∧
      (∀ i, i < W → columnSum d W i ≤ 9) := by
  obtain ⟨d, L, hsource⟩ := canonical_exists n hn
  have hc := no_overflow_of_descending_target hsource htarget hstep hpal hW hdesc
  have hnext : Canonical P (output (columnSum d L)) L := by
    rw [← hstep]
    exact canonical_next_no_overflow n d L hsource hc
  obtain ⟨hwidth, hdigit⟩ :=
    SevenColumnKernel.PalindromeBridge.canonical_unique hnext htarget
  have hp : Palindrome (value (output (columnSum d L)) L) := by
    rw [hnext.2.2.2]
    exact hpal
  have hs := (palindrome_value_iff (output (columnSum d L)) L
    hnext.2.1 (Or.inr hnext.2.2.1)).mp hp
  obtain ⟨_, hpair⟩ := DecimalCarry.no_overflow_palindrome_has_no_carries
    L (columnSum d L) (carry (columnSum d L)) (output (columnSum d L))
    hsource.1 (columnSum_symmetric d L) hs
    (fun i _ => column_equation (columnSum d L) i) rfl hc
  subst hwidth
  refine ⟨d, hsource, ?_, ?_⟩
  · intro i hi
    exact (hpair i hi).trans (hdigit i hi)
  · intro i hi
    rw [hpair i hi]
    exact output_bounded _ i

theorem last_step_triple (a b : Nat) (hab : b < a)
    {M P : Nat} (hM : 0 < M) (hstep : step M = P)
    (hP : PalindromeStartsTwo a b P) :
    3 ≤ width M ∧ (∀ i, i < width M → pairAt M i ≤ 9) ∧
      pairAt M 0 = a ∧ pairAt M 1 = b ∧ pairAt M 2 ≤ 9 := by
  obtain ⟨hpal, e, W, htarget, hW, hea, heb⟩ := hP
  obtain ⟨d, hsource, hpair, hsmall⟩ :=
    descending_last_step hM htarget hstep hpal hW (by omega)
  have hp : Palindrome (value e W) := by
    rw [htarget.2.2.2]
    exact hpal
  have hsym := (palindrome_value_iff e W htarget.2.1
    (Or.inr htarget.2.2.1)).mp hp
  have hwM := canonical_width hsource
  have h0 : e 0 = a := by
    rw [hsym 0 (by omega)]; simpa using hea
  have h1 : e 1 = b := by
    rw [hsym 1 (by omega)]; simpa only [Nat.sub_sub] using heb
  have hW3 : 3 ≤ W := by
    by_cases hW2 : W = 2
    · subst hW2
      have := hsym 0 (by omega)
      simp at this
      omega
    · omega
  refine ⟨by omega, ?_, ?_, ?_, ?_⟩
  · intro i hi
    rw [canonical_pairAt hsource i (by omega)]
    exact hsmall i (by omega)
  · rw [canonical_pairAt hsource 0 (by omega), hpair 0 (by omega), h0]
  · rw [canonical_pairAt hsource 1 (by omega), hpair 1 (by omega), h1]
  · rw [canonical_pairAt hsource 2 (by omega)]
    exact hsmall 2 (by omega)

#print axioms tri_step
#print axioms width_step_eq_of_small_descending
#print axioms no_overflow_of_descending_target
#print axioms descending_last_step
#print axioms last_step_triple
#print axioms tri_eq_tri3
#print axioms tri_box

end Agent113.TwoDigit
