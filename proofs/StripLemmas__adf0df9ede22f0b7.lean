import OuterBridge

/-!
Generic facts about maximal constant-suffix removal.  These lemmas use the
same `stripSuffix` as the checked outer projection and impose no phase or
integer-realizability assumptions.
-/
namespace Agent116.Exterior

open Agent109
open P196.Agent7.Finite (stripSuffix)

private theorem dropWhile_eq_idempotent (c : Nat) (w : Word) :
    (w.dropWhile (fun x => x == c)).dropWhile (fun x => x == c) =
      w.dropWhile (fun x => x == c) := by
  induction w with
  | nil => simp
  | cons x xs ih =>
    by_cases h : x = c
    · subst x
      simpa [List.dropWhile_cons] using ih
    · simp [List.dropWhile_cons, h]

/-- Removing the maximal constant suffix twice has the same result as once. -/
theorem stripSuffix_idempotent (c : Nat) (w : Word) :
    stripSuffix c (stripSuffix c w) = stripSuffix c w := by
  unfold stripSuffix
  rw [List.reverse_reverse, dropWhile_eq_idempotent]

/-- Appending copies of the stripped symbol does not change the result. -/
theorem stripSuffix_append_replicate (c : Nat) (w : Word) (j : Nat) :
    stripSuffix c (w ++ List.replicate j c) = stripSuffix c w := by
  unfold stripSuffix
  rw [List.reverse_append, List.reverse_replicate]
  rw [List.dropWhile_append_of_pos]
  intro a ha
  have h := (List.mem_replicate.mp ha).2
  simp [h]

/-- Suffix removal cannot increase word length. -/
theorem stripSuffix_length_le (c : Nat) (w : Word) :
    (stripSuffix c w).length ≤ w.length := by
  obtain ⟨j, hj⟩ := Agent109.Outer.stripSuffix_spec c w
  have hlen := congrArg List.length hj
  simp only [List.length_append, List.length_replicate] at hlen
  omega

/-- A nonempty stripped word ends in a symbol different from the removed one. -/
theorem stripSuffix_last (c : Nat) (w : Word) (a : Nat)
    (h : (stripSuffix c w).getLast? = some a) : a ≠ c := by
  have hn := List.head?_dropWhile_not (fun x : Nat => x == c) w.reverse
  simp only [stripSuffix, List.getLast?_reverse] at h
  rw [h] at hn
  simpa using hn

/-- Any nonempty result retains the positive first symbol of the input. -/
theorem stripSuffix_head_pos (c : Nat) (w : Word)
    (hw : ∀ a xs, w = a :: xs → 0 < a) :
    ∀ a xs, stripSuffix c w = a :: xs → 0 < a := by
  intro a xs hs
  obtain ⟨j, hj⟩ := Agent109.Outer.stripSuffix_spec c w
  apply hw a (xs ++ List.replicate j c)
  rw [hj, hs]
  rfl

/-- The boundedness result from the bridge, in this module's namespace. -/
theorem stripSuffix_bounded (c : Nat) (w : Word) (hw : Bounded w) :
    Bounded (stripSuffix c w) :=
  Agent109.Outer.bounded_strip c w hw

end Agent116.Exterior

#print axioms Agent116.Exterior.stripSuffix_idempotent
#print axioms Agent116.Exterior.stripSuffix_append_replicate
#print axioms Agent116.Exterior.stripSuffix_length_le
#print axioms Agent116.Exterior.stripSuffix_last
#print axioms Agent116.Exterior.stripSuffix_head_pos
#print axioms Agent116.Exterior.stripSuffix_bounded
