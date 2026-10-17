import P196.Agent6CertificateCoordinateAudit.OuterBridge

/-!
Generic facts about maximal constant-suffix removal.  These lemmas use the
same `stripSuffix` as the checked outer projection and impose no phase or
integer-realizability assumptions.
-/
namespace Agent116.Exterior

open Agent109
open P196.Agent7.Finite (Outer outerNext stripSuffix)
set_option maxHeartbeats 0

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

/-- Moving one final phase letter into the band appends precisely one new phase
letter to the untrimmed returned exterior. -/
theorem Br_append_phase (c : Nat) (B A C : Word) (hc : Phase c) (hB : Bounded B) :
    Br c (B ++ [c]) A C = Br c B A C ++ [tOf c + tOf c] := by
  have hc18 : c ≤ 18 := by have := hc.2.1; omega
  have hcnine := hc.2.2
  have he := norm_carry_le B 0 hB (by decide)
  have hleft : norm (B ++ [c]) 0 =
      ((norm B 0).1 ++ [c + (norm B 0).2 - 10 * kOf c], kOf c) := by
    rw [norm_append]
    have hb := norm_band c 0 (norm B 0).2 hc18 hcnine he
    simpa using congrArg (fun p : Word × Nat => ((norm B 0).1 ++ p.1, p.2)) hb
  have hr0 : norm [c] (kOf c) = ([tOf c], kOf c) := by
    exact norm_band_tail c 1 hc18
  have hright : norm (B ++ [c]).reverse (kOf c) =
      ([tOf c] ++ (norm B.reverse (kOf c)).1, (norm B.reverse (kOf c)).2) := by
    rw [List.reverse_append]
    simp only [List.reverse_cons, List.reverse_nil, List.nil_append]
    rw [norm_append, hr0]
  have hut : c + kOf c - 10 * kOf c = tOf c := by
    unfold tOf kOf; split <;> omega
  simp only [Br, data, u0]
  simp only [data, hleft, hright]
  simp only [List.reverse_append, List.reverse_cons, List.reverse_nil,
    List.nil_append, hut]
  by_cases hγ : (norm B.reverse (kOf c)).2 = 0
  · simp only [hγ, if_true]
    rw [zipAdd_append _ _ _ _ (by simp [norm_length])]
    rfl
  · simp only [hγ, if_false]
    rw [← List.append_assoc [1] _ [tOf c]]
    rw [zipAdd_append _ _ _ _ (by simp [norm_length])]
    rfl


/-- Moving any number of phase letters into the band appends exactly the same
number of new-phase letters before maximal exterior normalization. -/
theorem Br_append_replicate (c : Nat) (B A C : Word) (j : Nat)
    (hc : Phase c) (hB : Bounded B) :
    Br c (B ++ List.replicate j c) A C =
      Br c B A C ++ List.replicate j (tOf c + tOf c) := by
  induction j with
  | zero => simp
  | succ j ih =>
    have hBj : Bounded (B ++ List.replicate j c) := by
      intro x hx
      rcases List.mem_append.mp hx with hx | hx
      · exact hB x hx
      · have heq := (List.mem_replicate.mp hx).2
        subst x
        have := hc.2.1
        omega
    rw [List.replicate_succ', ← List.append_assoc,
      Br_append_phase c (B ++ List.replicate j c) A C hc hBj, ih]
    simp only [List.replicate_succ', List.append_assoc]

/-- The deterministic outer map is invariant under an appended constant
phase suffix.  No nonempty-word or positive-head assumption is needed. -/
theorem outerNext_append_replicate (c : Nat) (B : Word) (j : Nat)
    (hc : Phase c) (hB : Bounded B) :
    outerNext ⟨c, B ++ List.replicate j c⟩ = outerNext ⟨c, B⟩ := by
  rw [Agent109.Outer.outerNext_eq c (B ++ List.replicate j c) [] [],
    Agent109.Outer.outerNext_eq c B [] [], Br_append_replicate c B [] [] j hc hB,
    stripSuffix_append_replicate]

/-- Canonicalizing the input exterior leaves the actual outer successor
unchanged.  This bridges arbitrary certificate suffix trims to the deterministic
maximally trimmed exterior map. -/
theorem outerNext_stripSuffix_eq (c : Nat) (B : Word)
    (hc : Phase c) (hB : Bounded B) :
    outerNext ⟨c, stripSuffix c B⟩ = outerNext ⟨c, B⟩ := by
  obtain ⟨j, hj⟩ := Agent109.Outer.stripSuffix_spec c B
  have h := outerNext_append_replicate c (stripSuffix c B) j hc
    (stripSuffix_bounded c B hB)
  rw [← hj] at h
  exact h.symm

/-- A partial exterior trim in a local certificate induces exactly the
canonical deterministic outer transition. -/
theorem outerNext_of_partial_trim (c c' : Nat) (B B' A C : Word) (j : Nat)
    (hc : Phase c) (hB : Bounded B) (hc' : c' = tOf c + tOf c)
    (htrim : Br c B A C = B' ++ List.replicate j c') :
    outerNext ⟨c, stripSuffix c B⟩ = ⟨c', stripSuffix c' B'⟩ := by
  rw [outerNext_stripSuffix_eq c B hc hB,
    Agent109.Outer.outerNext_eq c B A C, ← hc', htrim,
    stripSuffix_append_replicate]

end Agent116.Exterior

#print axioms Agent116.Exterior.stripSuffix_idempotent
#print axioms Agent116.Exterior.stripSuffix_append_replicate
#print axioms Agent116.Exterior.stripSuffix_length_le
#print axioms Agent116.Exterior.stripSuffix_last
#print axioms Agent116.Exterior.stripSuffix_head_pos
#print axioms Agent116.Exterior.stripSuffix_bounded
#print axioms Agent116.Exterior.Br_append_phase
#print axioms Agent116.Exterior.Br_append_replicate
#print axioms Agent116.Exterior.outerNext_append_replicate
#print axioms Agent116.Exterior.outerNext_stripSuffix_eq
#print axioms Agent116.Exterior.outerNext_of_partial_trim
