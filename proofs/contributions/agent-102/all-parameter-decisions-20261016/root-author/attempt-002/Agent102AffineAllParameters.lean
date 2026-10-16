import Agent102AffineDecision
import Agent102RunDecision

/-!
Agent #102: complete decisions over all natural template parameters.
These quantify over the static `wordAt` family, not reverse-add iteration time.
Only the finite prefix uses evaluated run counts; tail comparison uses the
proved coefficient checker. Neither executable branch expands a digit word.
-/

namespace Agent102

def allEqual (A B : List RunSpec) : Bool :=
  fastEqualOnTail A B && (List.range (equalityCutoff A B)).all (equalAt A B)

def someEqual (A B : List RunSpec) : Bool :=
  fastEqualOnTail A B || (List.range (equalityCutoff A B)).any (equalAt A B)

def allUnequal (A B : List RunSpec) : Bool := !someEqual A B

def someUnequal (A B : List RunSpec) : Bool := !allEqual A B

theorem allEqual_spec (A B : List RunSpec) :
    allEqual A B = true ↔ ∀ k : Nat, wordAt A k = wordAt B k := by
  simp only [allEqual, Bool.and_eq_true, fastEqualOnTail_spec,
    List.all_eq_true, List.mem_range, equalAt_eq_true_iff]
  constructor
  · rintro ⟨htail, hprefix⟩ k
    by_cases hk : equalityCutoff A B ≤ k
    · exact htail k hk
    · exact hprefix k (by omega)
  · intro h
    exact ⟨fun k _ => h k, fun k _ => h k⟩

theorem someEqual_spec (A B : List RunSpec) :
    someEqual A B = true ↔ ∃ k : Nat, wordAt A k = wordAt B k := by
  simp only [someEqual, Bool.or_eq_true, List.any_eq_true,
    List.mem_range, equalAt_eq_true_iff]
  constructor
  · rintro (htail | ⟨k, _, he⟩)
    · exact ⟨equalityCutoff A B, (fastEqualOnTail_spec A B).mp htail _ (Nat.le_refl _)⟩
    · exact ⟨k, he⟩
  · rintro ⟨k, he⟩
    by_cases hk : equalityCutoff A B ≤ k
    · exact Or.inl ((fastEqualOnTail_iff_wordAt A B k hk).mpr he)
    · exact Or.inr ⟨k, by omega, he⟩

theorem allUnequal_spec (A B : List RunSpec) :
    allUnequal A B = true ↔ ∀ k : Nat, wordAt A k ≠ wordAt B k := by
  change (!someEqual A B) = true ↔ _
  constructor
  · intro h k he
    have hb := (someEqual_spec A B).mpr ⟨k, he⟩
    simp [hb] at h
  · intro h
    cases hb : someEqual A B with
    | false => rfl
    | true =>
        obtain ⟨k, he⟩ := (someEqual_spec A B).mp hb
        exact False.elim (h k he)

theorem someUnequal_spec (A B : List RunSpec) :
    someUnequal A B = true ↔ ∃ k : Nat, wordAt A k ≠ wordAt B k := by
  classical
  change (!allEqual A B) = true ↔ _
  constructor
  · intro h
    by_cases hex : ∃ k : Nat, wordAt A k ≠ wordAt B k
    · exact hex
    · have heall : ∀ k : Nat, wordAt A k = wordAt B k := by
        intro k
        by_cases he : wordAt A k = wordAt B k
        · exact he
        · exact False.elim (hex ⟨k, he⟩)
      have hb := (allEqual_spec A B).mpr heall
      simp [hb] at h
  · rintro ⟨k, he⟩
    cases hb : allEqual A B with
    | false => rfl
    | true => exact False.elim (he ((allEqual_spec A B).mp hb k))

/-- A negative universal result has an actual natural-parameter counterexample. -/
theorem allEqual_false_iff (A B : List RunSpec) :
    allEqual A B = false ↔ ∃ k : Nat, wordAt A k ≠ wordAt B k := by
  simpa only [someUnequal, Bool.not_eq_true'] using someUnequal_spec A B

theorem someEqual_false_iff (A B : List RunSpec) :
    someEqual A B = false ↔ ∀ k : Nat, wordAt A k ≠ wordAt B k := by
  simpa only [allUnequal, Bool.not_eq_true'] using allUnequal_spec A B

def allPalindromic (A : List RunSpec) : Bool := allEqual A A.reverse

def somePalindromic (A : List RunSpec) : Bool := someEqual A A.reverse

def allNonpalindromic (A : List RunSpec) : Bool := allUnequal A A.reverse

def someNonpalindromic (A : List RunSpec) : Bool := someUnequal A A.reverse

theorem allPalindromic_spec (A : List RunSpec) :
    allPalindromic A = true ↔ ∀ k : Nat, wordAt A k = (wordAt A k).reverse := by
  simpa only [allPalindromic, wordAt_reverse] using allEqual_spec A A.reverse

theorem somePalindromic_spec (A : List RunSpec) :
    somePalindromic A = true ↔ ∃ k : Nat, wordAt A k = (wordAt A k).reverse := by
  simpa only [somePalindromic, wordAt_reverse] using someEqual_spec A A.reverse

theorem allNonpalindromic_spec (A : List RunSpec) :
    allNonpalindromic A = true ↔ ∀ k : Nat, wordAt A k ≠ (wordAt A k).reverse := by
  simpa only [allNonpalindromic, wordAt_reverse] using allUnequal_spec A A.reverse

theorem someNonpalindromic_spec (A : List RunSpec) :
    someNonpalindromic A = true ↔ ∃ k : Nat, wordAt A k ≠ (wordAt A k).reverse := by
  simpa only [someNonpalindromic, wordAt_reverse] using someUnequal_spec A A.reverse

theorem allPalindromic_false_iff (A : List RunSpec) :
    allPalindromic A = false ↔ ∃ k : Nat, wordAt A k ≠ (wordAt A k).reverse := by
  simpa only [allPalindromic, wordAt_reverse] using allEqual_false_iff A A.reverse

theorem somePalindromic_false_iff (A : List RunSpec) :
    somePalindromic A = false ↔ ∀ k : Nat, wordAt A k ≠ (wordAt A k).reverse := by
  simpa only [somePalindromic, wordAt_reverse] using someEqual_false_iff A A.reverse

#print axioms allEqual_spec
#print axioms someEqual_spec
#print axioms allUnequal_spec
#print axioms someUnequal_spec
#print axioms allEqual_false_iff
#print axioms someEqual_false_iff
#print axioms allPalindromic_spec
#print axioms somePalindromic_spec
#print axioms allNonpalindromic_spec
#print axioms someNonpalindromic_spec
#print axioms allPalindromic_false_iff
#print axioms somePalindromic_false_iff

end Agent102
