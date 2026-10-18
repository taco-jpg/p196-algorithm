import P196.Agent101ProtectedFamily.FamilyCardinality

namespace P196.Agent3.OverflowHorizon.CardinalityIndependentReview

open P196.Agent3.OverflowHorizon

theorem exact_enumeration (xs : List Bool) (m : Nat) :
    xs ∈ allBits m ↔ xs.length = m := mem_allBits_iff xs m

theorem no_unpaired_center (xs : List Bool) (k i : Nat) :
    2 * i + 1 ≠ (inputWord xs k).length := by
  rw [inputWord_length]
  omega

theorem exact_distinct_family (m k : Nat) :
    (familyWords m k).length = 2 ^ m ∧
    (familyWords m k).Nodup ∧
    ∀ w ∈ familyWords m k,
      Agent8.CanonicalPair w ∧ w.length = 2 * (m + k + 1) ∧
        w.length % 2 = 0 := familyWords_exact m k

#print axioms exact_enumeration
#print axioms no_unpaired_center
#print axioms exact_distinct_family
#print axioms P196.Agent3.OverflowHorizon.choice
#print axioms P196.Agent3.OverflowHorizon.inputHalf
#print axioms P196.Agent3.OverflowHorizon.inputWord
#print axioms P196.Agent3.OverflowHorizon.target

end P196.Agent3.OverflowHorizon.CardinalityIndependentReview
