import P196.Agent101DigitSplit.Agent101NumericFibers

/-!
Agent #101: finite half/optional-center reconstruction of a symmetric list.
The construction does not decode a numerical target; it only repackages
an already given finite coefficient word, without counting digit functions.
-/

namespace Agent101

theorem reverse_wrapDigits (a b : Nat) (xs : List Nat) :
    (wrapDigits a b xs).reverse = wrapDigits b a xs.reverse := by
  simp [wrapDigits, List.reverse_append, List.append_assoc]

/-- Every finite symmetric coefficient list has a half and optional center. -/
theorem exists_coefficientWord_of_reverse (q : List Nat)
    (hq : q.reverse = q) : ∃ h c, q = coefficientWord h c := by
  have aux : ∀ N, ∀ q : List Nat, q.length = N → q.reverse = q →
      ∃ h c, q = coefficientWord h c := by
    intro N
    induction N using Nat.strongRecOn with
    | ind N ih =>
      intro q hlen hrev
      by_cases htwo : 2 ≤ q.length
      · obtain ⟨a, b, xs, rfl⟩ := exists_wrapDigits q htwo
        rw [reverse_wrapDigits] at hrev
        obtain ⟨hba, _, hxs⟩ := wrapDigits_injective _ _ _ _ _ _ hrev
        subst b
        have hsmall : xs.length < N := by
          rw [length_wrapDigits] at hlen
          omega
        obtain ⟨h, c, heq⟩ := ih xs.length hsmall xs rfl hxs
        refine ⟨a :: h, c, ?_⟩
        rw [coefficientWord_cons, heq]
      · cases q with
        | nil => exact ⟨[], none, rfl⟩
        | cons a xs =>
          have hx : xs = [] := by
            apply List.length_eq_zero_iff.mp
            simp only [List.length_cons] at htwo
            omega
          subst xs
          exact ⟨[], some a, rfl⟩
  exact aux q.length q rfl hq

theorem coefficientWord_half_length (h : List Nat) (c : Option Nat) :
    h.length = (coefficientWord h c).length / 2 := by
  rw [length_coefficientWord]
  cases c <;> simp only [Option.toList_none, Option.toList_some,
    List.length_nil, List.length_cons] <;> omega

theorem digitFn_coefficientWord_cons_zero (s : Nat) (h : List Nat)
    (c : Option Nat) : digitFn (coefficientWord (s :: h) c) 0 = s := by
  simp [coefficientWord, digitFn]

theorem digitPairSums_reverse (ds : List Nat) :
    (digitPairSums ds).reverse = digitPairSums ds := by
  unfold digitPairSums
  rw [List.reverse_zipWith (by simp)]
  simp only [List.reverse_reverse]
  apply List.ext_getElem (by simp [List.length_zipWith, Nat.min_comm])
  intro i hi hj
  simp only [List.getElem_zipWith] 
  exact Nat.add_comm _ _

/-- Reconstruction includes exact half-width and the numerical output. -/
theorem digitPairSums_profile (ds : List Nat) :
    ∃ h c, digitPairSums ds = coefficientWord h c ∧
      h.length = ds.length / 2 ∧
      (coefficientWord h c).length = ds.length := by
  obtain ⟨h, c, heq⟩ := exists_coefficientWord_of_reverse
    (digitPairSums ds) (digitPairSums_reverse ds)
  refine ⟨h, c, heq, ?_, ?_⟩
  · rw [coefficientWord_half_length, ← heq, length_digitPairSums]
  · rw [← heq, length_digitPairSums]

/-- A word of length at least two exposes its exact outer coefficient. -/
theorem digitPairSums_profile_cons (ds : List Nat) (hL : 2 ≤ ds.length) :
    ∃ s h c, digitPairSums ds = coefficientWord (s :: h) c ∧
      h.length = ds.length / 2 - 1 ∧
      (coefficientWord (s :: h) c).length = ds.length ∧
      s = DecimalDigits.columnSum (digitFn ds) ds.length 0 := by
  obtain ⟨half, c, heq, hh, hlen⟩ := digitPairSums_profile ds
  cases half with
  | nil => simp only [List.length_nil] at hh; omega
  | cons s h =>
    refine ⟨s, h, c, heq, ?_, hlen, ?_⟩
    · simp only [List.length_cons] at hh
      omega
    · rw [← digitFn_digitPairSums ds 0 (by omega), heq]
      exact (digitFn_coefficientWord_cons_zero s h c).symm

#print axioms reverse_wrapDigits
#print axioms exists_coefficientWord_of_reverse
#print axioms coefficientWord_half_length
#print axioms digitFn_coefficientWord_cons_zero
#print axioms digitPairSums_reverse
#print axioms digitPairSums_profile
#print axioms digitPairSums_profile_cons

end Agent101
