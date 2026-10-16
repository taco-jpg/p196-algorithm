import Lychrel196Research

/- Every realizable non-overflow carry word has an admissible representative
whose next mirrored-sum word is entirely at most 9. This is an obstruction to
single-carry-word invariant proofs, not a proof of decimal Lychrel existence. -/
namespace CarryNormalization
open DecimalDigits FoldedDecimal

def norm (a b : Nat) : Nat := if a = b then if a = 0 then 2 else 10 else 9

theorem norm_local (x a b : Nat) (hx : x ≤ 18) (ha : a ≤ 1) (hb : b ≤ 1) :
    let u := (x + a) / 10
    let v := (x + b) / 10
    (norm u v + a) / 10 = u ∧
    (norm u v + b) / 10 = v ∧
    (norm u v + a) % 10 + (norm u v + b) % 10 ≤ 9 := by
  dsimp
  unfold norm
  split <;> rename_i h
  · split <;> omega
  · omega

theorem norm_symmetric (a b : Nat) : norm a b = norm b a := by
  unfold norm
  by_cases h : a = b
  · subst b; simp
  · simp [h, Ne.symm h]

theorem norm_range (a b : Nat) : 0 < norm a b ∧ norm a b ≤ 10 := by
  unfold norm
  split <;> simp_all
  split <;> omega

def normalized (q : Nat → Nat) (L i : Nat) : Nat :=
  norm (carry q (i + 1)) (carry q (L - i))

theorem normalized_preserves_carry (q : Nat → Nat) (L : Nat)
    (hq : ∀ i, i < L → q i ≤ 18)
    (hs : ∀ i, i < L → q i = q (L - 1 - i)) :
    ∀ i, i ≤ L → carry (normalized q L) i = carry q i := by
  intro i
  induction i with
  | zero => intro _; rfl
  | succ i ih =>
    intro hi
    have him : L - 1 - i < L := by omega
    have hf : L - 1 - i + 1 = L - i := by omega
    have hlocal := norm_local (q i) (carry q i) (carry q (L - 1 - i))
      (hq i (by omega))
      (carry_bounded q L hq i (by omega))
      (carry_bounded q L hq (L - 1 - i) (by omega))
    have hout : (q i + carry q (L - 1 - i)) / 10 = carry q (L - i) := by
      rw [hs i (by omega), ← hf]
      rfl
    dsimp at hlocal
    rw [hout] at hlocal
    change (normalized q L i + carry (normalized q L) i) / 10 = carry q (i + 1)
    rw [ih (by omega)]
    exact hlocal.1

theorem normalized_symmetric (q : Nat → Nat) (L i : Nat) (hi : i < L) :
    normalized q L i = normalized q L (L - 1 - i) := by
  have h1 : L - 1 - i + 1 = L - i := by omega
  have h2 : L - (L - 1 - i) = i + 1 := by omega
  simp only [normalized, h1, h2]
  exact norm_symmetric _ _

theorem normalized_admissible (q : Nat → Nat) (L : Nat) (hL : 0 < L) :
    Admissible L (normalized q L) := by
  refine ⟨hL, (norm_range _ _).1, ?_, ?_, ?_⟩
  · intro i hi; have := (norm_range (carry q (i+1)) (carry q (L-i))).2
    exact Nat.le_trans this (by decide)
  · exact normalized_symmetric q L
  · intro i hi hm
    have heq : L - i = i + 1 := by omega
    simp only [normalized, heq, norm, if_true]
    split <;> decide

theorem normalized_next_low (q : Nat → Nat) (L : Nat)
    (hq : ∀ i, i < L → q i ≤ 18)
    (hs : ∀ i, i < L → q i = q (L - 1 - i)) :
    ∀ i, i < L →
      output (normalized q L) i + output (normalized q L) (L - 1 - i) ≤ 9 := by
  intro i hi
  have him : L - 1 - i < L := by omega
  have hf : L - 1 - i + 1 = L - i := by omega
  have hlocal := norm_local (q i) (carry q i) (carry q (L - 1 - i))
    (hq i hi)
    (carry_bounded q L hq i (by omega))
    (carry_bounded q L hq (L - 1 - i) (by omega))
  have hout : (q i + carry q (L - 1 - i)) / 10 = carry q (L - i) := by
    rw [hs i hi, ← hf]
    rfl
  dsimp at hlocal
  rw [hout] at hlocal
  unfold output
  rw [normalized_preserves_carry q L hq hs i (by omega),
    normalized_preserves_carry q L hq hs (L - 1 - i) (by omega),
    ← normalized_symmetric q L i hi]
  exact hlocal.2.2

/-- Every complete non-overflow carry trace has a concrete positive decimal
representative reaching a palindrome after exactly two applications (possibly
earlier as well). In particular carry data alone cannot certify nontermination. -/
theorem same_carries_two_step_palindrome (q : Nat → Nat) (L : Nat)
    (hL : 0 < L)
    (hq : ∀ i, i < L → q i ≤ 18)
    (hs : ∀ i, i < L → q i = q (L - 1 - i))
    (hover : carry q L = 0) :
    ∃ n d, 0 < n ∧ Canonical n d L ∧
      (∀ i, i ≤ L → carry (columnSum d L) i = carry q i) ∧
      Lychrel196.Palindrome (Lychrel196.step (Lychrel196.step n)) := by
  have had := normalized_admissible q L hL
  obtain ⟨n, d, hn, hcan, hrep⟩ := valid_word_realizable (normalized q L) L
    had.1 had.2.1 had.2.2.1 had.2.2.2.1 had.2.2.2.2
  have hcarry : ∀ i, i ≤ L → carry (columnSum d L) i = carry q i := by
    intro i hi
    exact (carry_congr_upto _ _ L hrep i hi).trans
      (normalized_preserves_carry q L hq hs i hi)
  have hncarry : carry (normalized q L) L = 0 :=
    (normalized_preserves_carry q L hq hs L (by omega)).trans hover
  have hwidth : nextWidth (normalized q L) L = L := by
    simp [nextWidth, hncarry]
  obtain ⟨e, hecan, herep⟩ := representation_next n d (normalized q L) L hcan hrep
  rw [hwidth] at hecan herep
  refine ⟨n, d, hn, hcan, hcarry, ?_⟩
  rcases hecan with ⟨heL, heb, hep, hev⟩
  rw [← hev]
  apply (step_palindrome_iff e L heL heb hep).mpr
  left
  intro i hi
  rw [herep i hi]
  simp only [nextColumns, hncarry, if_true, columnSum, reflected]
  exact normalized_next_low q L hq hs i hi

#print axioms same_carries_two_step_palindrome
#print axioms normalized_next_low
#print axioms normalized_admissible
end CarryNormalization
