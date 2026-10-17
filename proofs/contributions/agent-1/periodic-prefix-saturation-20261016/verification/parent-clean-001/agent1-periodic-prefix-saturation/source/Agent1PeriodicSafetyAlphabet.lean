import Agent1PeriodicValidity

/-!
Finite alphabet and outside-head interfaces for the exact periodic word.
These use the original word powers and certified complete-block stripping.
They define no safety predicate and assert no forward safety preservation.
-/

namespace Agent1.Periodic

open Agent8 Agent1.RepeatedBlock

/-- A symbol occurs in a block power exactly when it occurs in the block
and the number of copies is positive. Empty blocks are included. -/
theorem mem_pow_iff (w : Word) (k x : Nat) :
    x ∈ pow w k ↔ x ∈ w ∧ 0 < k := by
  induction k with
  | zero => simp [pow]
  | succ k ih =>
    simp only [pow, List.mem_append, ih]
    constructor
    · intro h
      exact ⟨h.elim id And.left, by omega⟩
    · intro h
      exact Or.inl h.1

/-- Every stored block occurs at positive exponent, and the reflected pieces
introduce no additional symbols. There is no nonempty-period premise. -/
theorem mem_periodicWord_iff (B H w : Word) (k x : Nat) (hk : 0 < k) :
    x ∈ periodicWord B H w k ↔ x ∈ B ++ H ++ w := by
  simp only [periodicWord, List.mem_append, mem_pow_iff, hk, and_true,
    List.mem_reverse]
  constructor
  · rintro ((((hB | hw) | hH) | hw) | hB)
    · exact Or.inl (Or.inl hB)
    · exact Or.inr hw
    · exact Or.inl (Or.inr hH)
    · exact Or.inr hw
    · exact Or.inl (Or.inl hB)
  · rintro ((hB | hH) | hw)
    · exact Or.inr hB
    · exact Or.inl (Or.inl (Or.inr hH))
    · exact Or.inl (Or.inr hw)

/-- The outside coefficient depends only on exterior followed by one period.
This exposes the list fact used internally by periodicWord_canonical. -/
theorem periodicWord_head (B H w : Word) (k : Nat) (hk : 0 < k) (hw : w ≠ []) :
    (periodicWord B H w k).headD 0 = (B ++ w).headD 0 := by
  cases k with
  | zero => omega
  | succ k =>
    cases B with
    | cons b B => rfl
    | nil =>
      cases w with
      | nil => exact False.elim (hw rfl)
      | cons a w => rfl

/-- Keeping the period in the stored alphabet makes complete-block stripping
alphabet invariant, even when a remainder or the period itself is empty. -/
theorem mem_stripped_alphabet_iff (B H w : Word) (x : Nat) :
    x ∈ (stripPeriodSuffix w B).1 ++ (stripPeriodCenter w H).1 ++ w ↔
      x ∈ B ++ H ++ w := by
  by_cases hw : w = []
  · subst w
    simp only [stripPeriodSuffix_empty_block, stripPeriodCenter_empty]
  · have hB := Iff.of_eq
      (congrArg (fun D : Word => x ∈ D) (stripPeriodSuffix_spec w B hw))
    have hH := Iff.of_eq
      (congrArg (fun D : Word => x ∈ D) (stripPeriodCenter_decomposition w H))
    simp only [List.mem_append, mem_pow_iff, List.mem_reverse] at hB hH
    simp only [List.mem_append]
    constructor
    · rintro ((hB' | hH') | hw')
      · exact Or.inl (Or.inl (hB.mpr (Or.inl hB')))
      · exact Or.inl (Or.inr (hH.mpr (Or.inl (Or.inr hH'))))
      · exact Or.inr hw'
    · rintro ((hBin | hHin) | hw')
      · rcases hB.mp hBin with hB' | ⟨hw', _⟩
        · exact Or.inl (Or.inl hB')
        · exact Or.inr hw'
      · rcases hH.mp hHin with (⟨hw', _⟩ | hH') | ⟨hw', _⟩
        · exact Or.inr hw'
        · exact Or.inl (Or.inr hH')
        · exact Or.inr hw'
      · exact Or.inr hw'

end Agent1.Periodic

#print axioms Agent1.Periodic.mem_pow_iff
#print axioms Agent1.Periodic.mem_periodicWord_iff
#print axioms Agent1.Periodic.periodicWord_head
#print axioms Agent1.Periodic.mem_stripped_alphabet_iff
