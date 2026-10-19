import P196.EightCarryMaximalWidth.CandidateData

/-!
Finite coverage assembly for the short-core certificates. The list lemmas
separate exhaustive enumeration from the individual Boolean decisions.
The tactics below send each literal coefficient case to `decide +kernel`
separately, so no single decision reduces a whole list of search trees.
-/

namespace EightCarryMaximalWidth.Candidates

/-- Extending a concatenation is the concatenation of the two enumerations. -/
theorem extensions_append (leftOffset rightOffset count : Nat)
    (xs ys : List Pair) :
    extensions leftOffset rightOffset count (xs ++ ys) =
      extensions leftOffset rightOffset count xs ++
        extensions leftOffset rightOffset count ys := by
  exact List.flatMap_append

/-- Coverage of concatenated starts is the conjunction of the two covers. -/
theorem covered_append (xs ys allowed : List Pair) :
    covered (xs ++ ys) allowed = (covered xs allowed && covered ys allowed) := by
  exact List.all_append

/-- Coverage of all initial triples follows from the bounded coefficient
cases, with one independent Boolean proposition for each pair of indices. -/
theorem startsAt_cover_of_points (p : Nat) (allowed : List Pair)
    (h : ∀ b : Fin 19, ∀ a : Fin 18,
      (allowed.contains ([p, b.val, a.val + 1], [p, b.val, a.val]) ||
        !accepted ([p, b.val, a.val + 1], [p, b.val, a.val])) = true) :
    covered (startsAt p) allowed = true := by
  unfold covered startsAt
  rw [List.all_flatMap]
  apply List.all_eq_true.mpr
  intro b hb
  rw [List.all_map]
  apply List.all_eq_true.mpr
  intro a ha
  exact h ⟨b, List.mem_range.mp hb⟩ ⟨a, List.mem_range.mp ha⟩

/-- Extend every parent in a cover by every allowed appended coefficient.
The hypothesis can be supplied by separate proofs for individual parents. -/
theorem extensions_cover_of_points (leftOffset rightOffset count : Nat)
    (ps allowed : List Pair)
    (h : ∀ p, p ∈ ps → ∀ a : Fin count,
      (allowed.contains (p.1 ++ [a.val + leftOffset],
          p.2 ++ [a.val + rightOffset]) ||
        !accepted (p.1 ++ [a.val + leftOffset],
          p.2 ++ [a.val + rightOffset])) = true) :
    covered (extensions leftOffset rightOffset count ps) allowed = true := by
  unfold covered extensions
  rw [List.all_flatMap]
  apply List.all_eq_true.mpr
  intro p hp
  rw [List.all_map]
  apply List.all_eq_true.mpr
  intro a ha
  exact h p hp ⟨a, List.mem_range.mp ha⟩

/-- The same extension coverage principle with parents indexed by their
positions in the literal list. No uniqueness of the parent list is needed. -/
theorem extensions_cover_of_indices (leftOffset rightOffset count : Nat)
    (ps allowed : List Pair)
    (h : ∀ i : Fin ps.length, ∀ a : Fin count,
      (allowed.contains ((ps.get i).1 ++ [a.val + leftOffset],
          (ps.get i).2 ++ [a.val + rightOffset]) ||
        !accepted ((ps.get i).1 ++ [a.val + leftOffset],
          (ps.get i).2 ++ [a.val + rightOffset])) = true) :
    covered (extensions leftOffset rightOffset count ps) allowed = true := by
  apply extensions_cover_of_points
  intro p hp a
  obtain ⟨i, hi⟩ := List.mem_iff_get.mp hp
  simpa only [hi] using h i a

/-- Split both bounded coefficients of an initial triple before invoking
kernel decision. The exterior coefficient and allowed list must be closed. -/
macro "certify_starts" : tactic =>
  `(tactic| (
    apply EightCarryMaximalWidth.Candidates.startsAt_cover_of_points
    intro b a
    rcases b with ⟨b, hb⟩
    rcases a with ⟨a, ha⟩
    have hbCases : b = 0 ∨ b = 1 ∨ b = 2 ∨ b = 3 ∨ b = 4 ∨
        b = 5 ∨ b = 6 ∨ b = 7 ∨ b = 8 ∨ b = 9 ∨ b = 10 ∨
        b = 11 ∨ b = 12 ∨ b = 13 ∨ b = 14 ∨ b = 15 ∨ b = 16 ∨
        b = 17 ∨ b = 18 := by omega
    have haCases : a = 0 ∨ a = 1 ∨ a = 2 ∨ a = 3 ∨ a = 4 ∨
        a = 5 ∨ a = 6 ∨ a = 7 ∨ a = 8 ∨ a = 9 ∨ a = 10 ∨
        a = 11 ∨ a = 12 ∨ a = 13 ∨ a = 14 ∨ a = 15 ∨ a = 16 ∨
        a = 17 := by omega
    rcases hbCases with hbCase | hbCase | hbCase | hbCase | hbCase |
      hbCase | hbCase | hbCase | hbCase | hbCase | hbCase | hbCase |
      hbCase | hbCase | hbCase | hbCase | hbCase | hbCase | hbCase <;>
      rcases haCases with haCase | haCase | haCase | haCase | haCase |
        haCase | haCase | haCase | haCase | haCase | haCase | haCase |
        haCase | haCase | haCase | haCase | haCase | haCase <;>
      subst b <;> subst a <;>
      simp only [Fin.val_mk] <;>
      decide +kernel))

/-- Certify a universal `Fin 13` coefficient goal by independent literals. -/
macro "certify_fin13" : tactic =>
  `(tactic| (
    intro a
    rcases a with ⟨a, ha⟩
    have haCases : a = 0 ∨ a = 1 ∨ a = 2 ∨ a = 3 ∨ a = 4 ∨
        a = 5 ∨ a = 6 ∨ a = 7 ∨ a = 8 ∨ a = 9 ∨ a = 10 ∨
        a = 11 ∨ a = 12 := by omega
    rcases haCases with haCase | haCase | haCase | haCase | haCase |
      haCase | haCase | haCase | haCase | haCase | haCase | haCase |
      haCase <;>
      subst a <;> simp only [Fin.val_mk] <;>
      decide +kernel))

/-- Certify a universal `Fin 14` coefficient goal by independent literals. -/
macro "certify_fin14" : tactic =>
  `(tactic| (
    intro a
    rcases a with ⟨a, ha⟩
    have haCases : a = 0 ∨ a = 1 ∨ a = 2 ∨ a = 3 ∨ a = 4 ∨
        a = 5 ∨ a = 6 ∨ a = 7 ∨ a = 8 ∨ a = 9 ∨ a = 10 ∨
        a = 11 ∨ a = 12 ∨ a = 13 := by omega
    rcases haCases with haCase | haCase | haCase | haCase | haCase |
      haCase | haCase | haCase | haCase | haCase | haCase | haCase |
      haCase | haCase <;>
      subst a <;> simp only [Fin.val_mk] <;>
      decide +kernel))

/-- Certify a universal `Fin 16` coefficient goal by independent literals. -/
macro "certify_fin16" : tactic =>
  `(tactic| (
    intro a
    rcases a with ⟨a, ha⟩
    have haCases : a = 0 ∨ a = 1 ∨ a = 2 ∨ a = 3 ∨ a = 4 ∨
        a = 5 ∨ a = 6 ∨ a = 7 ∨ a = 8 ∨ a = 9 ∨ a = 10 ∨
        a = 11 ∨ a = 12 ∨ a = 13 ∨ a = 14 ∨ a = 15 := by omega
    rcases haCases with haCase | haCase | haCase | haCase | haCase |
      haCase | haCase | haCase | haCase | haCase | haCase | haCase |
      haCase | haCase | haCase | haCase <;>
      subst a <;> simp only [Fin.val_mk] <;>
      decide +kernel))

end EightCarryMaximalWidth.Candidates
