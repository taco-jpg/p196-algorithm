import P196.Agent102AffineParameterIntervals.Agent102AffineRunParameterSets

/-!
Agent #102: finite interval certificates and complete quantified decisions.
Every executable operation examines only finite interval lists and endpoints;
no natural-parameter prefix is traversed and no represented word is expanded.
-/

namespace Agent102.ParameterSets

theorem inhabited_false_iff (R : Region) :
    inhabited R = false ↔ ∀ k, ¬holds R k := by
  constructor
  · intro h k hk
    have ht := (inhabited_eq_true_iff R).mpr ⟨k, hk⟩
    simp [h] at ht
  · intro h
    cases hb : inhabited R with
    | false => rfl
    | true =>
        obtain ⟨k, hk⟩ := (inhabited_eq_true_iff R).mp hb
        exact False.elim (h k hk)

/-- A certificate compares represented sets, not interval order or multiplicity. -/
def equivalentRegions (R S : Region) : Bool :=
  !inhabited (fastInter R (fastComplement S)) &&
    !inhabited (fastInter S (fastComplement R))

theorem equivalentRegions_spec (R S : Region) :
    equivalentRegions R S = true ↔ ∀ k, (holds R k ↔ holds S k) := by
  classical
  simp only [equivalentRegions, Bool.and_eq_true, Bool.not_eq_true',
    inhabited_false_iff, holds_fastInter, holds_fastComplement]
  constructor
  · rintro ⟨hrs, hsr⟩ k
    constructor
    · intro hr
      apply Classical.byContradiction
      intro hs
      exact hrs k ⟨hr, hs⟩
    · intro hs
      apply Classical.byContradiction
      intro hr
      exact hsr k ⟨hs, hr⟩
  · intro h
    constructor
    · rintro k ⟨hr, hs⟩
      exact hs ((h k).mp hr)
    · rintro k ⟨hs, hr⟩
      exact hr ((h k).mpr hs)

def hasEqualParameter (A B : List RunSpec) : Bool :=
  inhabited (equalityRegions A B)

def hasUnequalParameter (A B : List RunSpec) : Bool :=
  inhabited (fastComplement (equalityRegions A B))

def everyParameterEqual (A B : List RunSpec) : Bool := !hasUnequalParameter A B

def everyParameterUnequal (A B : List RunSpec) : Bool := !hasEqualParameter A B

theorem hasEqualParameter_spec (A B : List RunSpec) :
    hasEqualParameter A B = true ↔ ∃ k, wordAt A k = wordAt B k := by
  simp only [hasEqualParameter, inhabited_eq_true_iff, holds_equalityRegions]

theorem hasUnequalParameter_spec (A B : List RunSpec) :
    hasUnequalParameter A B = true ↔ ∃ k, wordAt A k ≠ wordAt B k := by
  simp only [hasUnequalParameter, inhabited_eq_true_iff,
    holds_fastComplement, holds_equalityRegions]

theorem everyParameterEqual_spec (A B : List RunSpec) :
    everyParameterEqual A B = true ↔ ∀ k, wordAt A k = wordAt B k := by
  classical
  simp only [everyParameterEqual, hasUnequalParameter, Bool.not_eq_true',
    inhabited_false_iff, holds_fastComplement, holds_equalityRegions]
  constructor
  · intro h k
    exact Classical.byContradiction (h k)
  · intro h k hn
    exact hn (h k)

theorem everyParameterUnequal_spec (A B : List RunSpec) :
    everyParameterUnequal A B = true ↔ ∀ k, wordAt A k ≠ wordAt B k := by
  simp only [everyParameterUnequal, hasEqualParameter, Bool.not_eq_true',
    inhabited_false_iff, holds_equalityRegions]

def hasPalindromicParameter (A : List RunSpec) : Bool := hasEqualParameter A A.reverse

def hasNonpalindromicParameter (A : List RunSpec) : Bool := hasUnequalParameter A A.reverse

def everyParameterPalindromic (A : List RunSpec) : Bool := everyParameterEqual A A.reverse

def everyParameterNonpalindromic (A : List RunSpec) : Bool := everyParameterUnequal A A.reverse

theorem hasPalindromicParameter_spec (A : List RunSpec) :
    hasPalindromicParameter A = true ↔ ∃ k, wordAt A k = (wordAt A k).reverse := by
  simpa only [hasPalindromicParameter, wordAt_reverse] using hasEqualParameter_spec A A.reverse

theorem hasNonpalindromicParameter_spec (A : List RunSpec) :
    hasNonpalindromicParameter A = true ↔ ∃ k, wordAt A k ≠ (wordAt A k).reverse := by
  simpa only [hasNonpalindromicParameter, wordAt_reverse] using hasUnequalParameter_spec A A.reverse

theorem everyParameterPalindromic_spec (A : List RunSpec) :
    everyParameterPalindromic A = true ↔ ∀ k, wordAt A k = (wordAt A k).reverse := by
  simpa only [everyParameterPalindromic, wordAt_reverse] using everyParameterEqual_spec A A.reverse

theorem everyParameterNonpalindromic_spec (A : List RunSpec) :
    everyParameterNonpalindromic A = true ↔ ∀ k, wordAt A k ≠ (wordAt A k).reverse := by
  simpa only [everyParameterNonpalindromic, wordAt_reverse] using everyParameterUnequal_spec A A.reverse

#print axioms inhabited_false_iff
#print axioms equivalentRegions_spec
#print axioms hasEqualParameter_spec
#print axioms hasUnequalParameter_spec
#print axioms everyParameterEqual_spec
#print axioms everyParameterUnequal_spec
#print axioms hasPalindromicParameter_spec
#print axioms hasNonpalindromicParameter_spec
#print axioms everyParameterPalindromic_spec
#print axioms everyParameterNonpalindromic_spec

end Agent102.ParameterSets
