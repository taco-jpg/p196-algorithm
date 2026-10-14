import resume_renewal_extraction
import resume_normalization_ten
import resume_normalization_nine

namespace CarryWordTermination
open DecimalDigits FoldedDecimal Lychrel196

/-- Every realizable complete decimal carry word is also the complete carry
word of a positive integer whose reverse-and-add orbit reaches a palindrome
within four steps. The normalization retains the whole first carry word,
including overflow, but changes the digit pair sums. -/
theorem same_carry_word_palindrome_within_four
    (q : Nat → Nat) (L : Nat)
    (hL : 0 < L)
    (hq : ∀ i, i < L → q i ≤ 18)
    (hs : ∀ i, i < L → q i = q (L-1-i)) :
    ∃ n d k, 0 < n ∧ Canonical n d L ∧
      (∀ i, i ≤ L → carry (columnSum d L) i = carry q i) ∧
      0 < k ∧ k ≤ 4 ∧ Palindrome (orbit n k) := by
  exact OverflowCarryNormalization.all_carry_words_terminate_by_four_of_low
    NormalizationTen.normalized10_low_after_two
    OverflowNormalizationNine.normalized9_iterPairs_low_after_three
    q L hL hq hs

/-- Numeric form of the theorem: every positive input has a same-width,
same-complete-carry-word representative terminating in at most four steps. -/
theorem every_positive_integer_has_fast_same_carry_representative
    (a : Nat) (ha : 0 < a) :
    ∃ L da n dn k, Canonical a da L ∧ 0 < n ∧ Canonical n dn L ∧
      (∀ i, i ≤ L → carry (columnSum dn L) i = carry (columnSum da L) i) ∧
      0 < k ∧ k ≤ 4 ∧ Palindrome (orbit n k) := by
  obtain ⟨da,L,hcan⟩ := canonical_exists a ha
  have hq : ∀ i, i < L → columnSum da L i ≤ 18 := by
    intro i hi
    have h1 := hcan.2.1 i hi
    have h2 := hcan.2.1 (L-1-i) (by omega)
    simp only [columnSum,reflected]
    omega
  have hs : ∀ i, i < L → columnSum da L i = columnSum da L (L-1-i) := by
    intro i hi
    have hind : L-1-(L-1-i)=i := by omega
    simp only [columnSum,reflected,hind,Nat.add_comm]
  obtain ⟨n,dn,k,hn,hncan,hcarry,hk,hk4,hpal⟩ :=
    same_carry_word_palindrome_within_four (columnSum da L) L hcan.1 hq hs
  exact ⟨L,da,n,dn,k,hcan,hn,hncan,hcarry,hk,hk4,hpal⟩

#print axioms same_carry_word_palindrome_within_four
#print axioms every_positive_integer_has_fast_same_carry_representative
end CarryWordTermination
