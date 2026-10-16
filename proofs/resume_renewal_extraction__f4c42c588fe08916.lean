import resume_renewal_numeric

namespace OverflowCarryNormalization
open DecimalDigits FoldedDecimal Lychrel196

/-- The exact pair-sum state after k operations, including changing width. -/
def iterPairs (q : Nat → Nat) (L : Nat) : Nat → Nat × (Nat → Nat)
  | 0 => (L,q)
  | k+1 =>
    let prev := iterPairs q L k
    (nextWidth prev.2 prev.1, nextColumns prev.2 prev.1)

/-- A numeric orbit realizes every iterated pair-sum state exactly. -/
theorem iterPairs_representation (n : Nat) (d q : Nat → Nat) (L k : Nat)
    (hcan : Canonical n d L)
    (hrep : ∀ i, i < L → columnSum d L i = q i) :
    ∃ e, Canonical (orbit n k) e (iterPairs q L k).1 ∧
      (∀ i, i < (iterPairs q L k).1 →
        columnSum e (iterPairs q L k).1 i = (iterPairs q L k).2 i) := by
  induction k with
  | zero => exact ⟨d,hcan,hrep⟩
  | succ k ih =>
    obtain ⟨e,he,hr⟩ := ih
    obtain ⟨f,hf,hfr⟩ := representation_next (orbit n k) e
      (iterPairs q L k).2 (iterPairs q L k).1 he hr
    exact ⟨f,hf,hfr⟩

/-- If an exact iterated pair-sum state is low, the following numeric iterate
is a palindrome. This transfers the finite graph conclusion to the orbit. -/
theorem iterPairs_low_palindrome (n : Nat) (d q : Nat → Nat) (L k : Nat)
    (hcan : Canonical n d L)
    (hrep : ∀ i, i < L → columnSum d L i = q i)
    (hlow : ∀ i, i < (iterPairs q L k).1 → (iterPairs q L k).2 i ≤ 9) :
    Palindrome (orbit n (k+1)) := by
  obtain ⟨e,he,hr⟩ := iterPairs_representation n d q L k hcan hrep
  rcases he with ⟨heL,heb,hep,hev⟩
  change Palindrome (step (orbit n k))
  rw [← hev]
  apply (step_palindrome_iff e (iterPairs q L k).1 heL heb hep).mpr
  left
  intro i hi
  rw [hr i hi]
  exact hlow i hi

/-- Numeric extraction once the normalized graph has established a low state.
No finite-digit or time-testing assumption is used here. -/
theorem normalizedZero_low_extraction (q : Nat → Nat) (L k : Nat)
    (hL : 0 < L)
    (hq : ∀ i, i < L → q i ≤ 18)
    (hs : ∀ i, i < L → q i = q (L-1-i))
    (hc : carry q L = 1)
    (hlow : ∀ i, i < (iterPairs (normalizedZero q L) L k).1 →
      (iterPairs (normalizedZero q L) L k).2 i ≤ 9) :
    ∃ n d, 0 < n ∧ Canonical n d L ∧
      (∀ i, i ≤ L → carry (columnSum d L) i = carry q i) ∧
      Palindrome (orbit n (k+1)) := by
  obtain ⟨n,d,hn,hcan,hrep,hcarry⟩ := normalizedZero_realizable q L hL hq hs hc
  exact ⟨n,d,hn,hcan,hcarry,
    iterPairs_low_palindrome n d (normalizedZero q L) L k hcan hrep hlow⟩

/-- A reusable final extraction statement. The two low-state hypotheses are
supplied by the independent graph-to-numeric bridge. -/
theorem all_carry_words_terminate_by_four_of_low
    (h10 : ∀ q : Nat → Nat, ∀ L : Nat,
      0 < L → (∀ i, i < L → q i ≤ 18) →
      (∀ i, i < L → q i = q (L-1-i)) → carry q L = 1 →
      normalizedZero q L 0 = 10 →
      ∀ i, i < (iterPairs (normalizedZero q L) L 2).1 →
        (iterPairs (normalizedZero q L) L 2).2 i ≤ 9)
    (h9 : ∀ q : Nat → Nat, ∀ L : Nat,
      0 < L → (∀ i, i < L → q i ≤ 18) →
      (∀ i, i < L → q i = q (L-1-i)) → carry q L = 1 →
      normalizedZero q L 0 = 9 →
      ∀ i, i < (iterPairs (normalizedZero q L) L 3).1 →
        (iterPairs (normalizedZero q L) L 3).2 i ≤ 9)
    (q : Nat → Nat) (L : Nat)
    (hL : 0 < L)
    (hq : ∀ i, i < L → q i ≤ 18)
    (hs : ∀ i, i < L → q i = q (L-1-i)) :
    ∃ n d k, 0 < n ∧ Canonical n d L ∧
      (∀ i, i ≤ L → carry (columnSum d L) i = carry q i) ∧
      0 < k ∧ k ≤ 4 ∧ Palindrome (orbit n k) := by
  have hc := carry_bounded q L hq L (by omega)
  have hh : carry q L=0 ∨ carry q L=1 := by omega
  rcases hh with hh|hh
  · obtain ⟨n,d,hn,hcan,hcarry,hpal⟩ :=
      CarryNormalization.same_carries_two_step_palindrome q L hL hq hs hh
    exact ⟨n,d,2,hn,hcan,hcarry,by omega,by omega,hpal⟩
  · rcases normalizedZero_outer q L hh with hfirst|hfirst
    · obtain ⟨n,d,hn,hcan,hcarry,hpal⟩ :=
        normalizedZero_low_extraction q L 3 hL hq hs hh (h9 q L hL hq hs hh hfirst)
      exact ⟨n,d,4,hn,hcan,hcarry,by omega,by omega,hpal⟩
    · obtain ⟨n,d,hn,hcan,hcarry,hpal⟩ :=
        normalizedZero_low_extraction q L 2 hL hq hs hh (h10 q L hL hq hs hh hfirst)
      exact ⟨n,d,3,hn,hcan,hcarry,by omega,by omega,hpal⟩

#print axioms normalizedZero_low_extraction
#print axioms all_carry_words_terminate_by_four_of_low
end OverflowCarryNormalization
