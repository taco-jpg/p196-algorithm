import Std

/-!
Finite choices for one ordered low/high decimal digit pair and for an
optional center column. These are ordinary finite lists; the high digit
of an outer pair must be nonzero.
-/

namespace Agent101

/-- Ordered `(low digit, high digit)` choices for a prescribed pair sum. -/
def pairChoices (outer : Bool) (s : Nat) : List (Nat × Nat) :=
  ((List.range 10).flatMap fun a => (List.range 10).map fun b => (a, b)).filter fun p =>
    decide (p.1 + p.2 = s ∧ (outer = true → 0 < p.2))

/-- Exact number of choices for a bounded decimal digit pair. -/
def pairCount (outer : Bool) (s : Nat) : Nat :=
  if s ≤ 9 then (if outer then s else s + 1)
  else if s ≤ 18 then 19 - s else 0

/-- An absent center contributes no digits; an even center sum fixes one digit. -/
def centerWords (c : Option Nat) : List (List Nat) :=
  match c with
  | none => [[]]
  | some s => if s ≤ 18 ∧ s % 2 = 0 then [[s / 2]] else []

/-- The explicit zero-or-one count of optional-center realizations. -/
def centerCount (c : Option Nat) : Nat :=
  match c with
  | none => 1
  | some s => if s ≤ 18 ∧ s % 2 = 0 then 1 else 0

/-- Membership states the complete decimal and nonzero-leading restrictions. -/
theorem mem_pairChoices (outer : Bool) (s a b : Nat) :
    (a, b) ∈ pairChoices outer s ↔
      a ≤ 9 ∧ b ≤ 9 ∧ a + b = s ∧ (outer = true → 0 < b) := by
  cases outer <;> simp [pairChoices, List.mem_flatMap, List.mem_map] <;> omega

/-- Every ordered digit split appears once. -/
theorem pairChoices_nodup (outer : Bool) (s : Nat) :
    (pairChoices outer s).Nodup := by
  apply List.Pairwise.filter
  decide

/-- Pair sums above eighteen have no decimal realizations. -/
theorem pairChoices_eq_nil_of_large (outer : Bool) (s : Nat) (hs : 18 < s) :
    pairChoices outer s = [] := by
  apply List.eq_nil_iff_forall_not_mem.mpr
  intro p hp
  rcases p with ⟨a, b⟩
  have h := (mem_pairChoices outer s a b).mp hp
  omega

/-- The finite decimal-pair enumeration has the stated triangular count. -/
theorem length_pairChoices (outer : Bool) (s : Nat) :
    (pairChoices outer s).length = pairCount outer s := by
  by_cases hs : s ≤ 18
  · have finiteCounts : ∀ o : Bool, ∀ t : Fin 19,
        (pairChoices o t.val).length = pairCount o t.val := by decide
    exact finiteCounts outer ⟨s, by omega⟩
  · rw [pairChoices_eq_nil_of_large outer s (by omega)]
    simp [pairCount, hs, show ¬ s ≤ 9 by omega]

/-- Imposing a nonzero high digit only removes choices. -/
theorem pairChoices_true_subset_false (s : Nat) :
    pairChoices true s ⊆ pairChoices false s := by
  intro p hp
  rcases p with ⟨a, b⟩
  have h := (mem_pairChoices true s a b).mp hp
  exact (mem_pairChoices false s a b).mpr ⟨h.1, h.2.1, h.2.2.1, by simp⟩

/-- Exact membership for an absent or present center column. -/
theorem mem_centerWords (c : Option Nat) (w : List Nat) :
    w ∈ centerWords c ↔
      match c with
      | none => w = []
      | some s => s ≤ 18 ∧ s % 2 = 0 ∧ w = [s / 2] := by
  cases c with
  | none => simp [centerWords]
  | some s =>
    by_cases h : s ≤ 18 ∧ s % 2 = 0
    · simp [centerWords, h, h.1, h.2]
    · simp [centerWords, h]
      omega

theorem mem_centerWords_none (w : List Nat) :
    w ∈ centerWords none ↔ w = [] := by
  exact mem_centerWords none w

theorem mem_centerWords_some (s : Nat) (w : List Nat) :
    w ∈ centerWords (some s) ↔ s ≤ 18 ∧ s % 2 = 0 ∧ w = [s / 2] := by
  exact mem_centerWords (some s) w

/-- The empty center or its unique digit never repeats. -/
theorem centerWords_nodup (c : Option Nat) : (centerWords c).Nodup := by
  cases c with
  | none => simp [centerWords]
  | some s =>
    by_cases h : s ≤ 18 ∧ s % 2 = 0 <;> simp [centerWords, h]

/-- The explicit center indicator equals the enumeration length. -/
theorem length_centerWords (c : Option Nat) :
    (centerWords c).length = centerCount c := by
  cases c with
  | none => rfl
  | some s =>
    by_cases h : s ≤ 18 ∧ s % 2 = 0 <;> simp [centerWords, centerCount, h]

#print axioms pairChoices
#print axioms pairCount
#print axioms centerWords
#print axioms centerCount
#print axioms mem_pairChoices
#print axioms pairChoices_nodup
#print axioms pairChoices_eq_nil_of_large
#print axioms length_pairChoices
#print axioms pairChoices_true_subset_false
#print axioms mem_centerWords
#print axioms mem_centerWords_none
#print axioms mem_centerWords_some
#print axioms centerWords_nodup
#print axioms length_centerWords

end Agent101
