import P196.Drafts.Agent3PrefixContraction.PathCounts

/-!
A four-column obstruction to three original no-overflow inverse paths.

The boundary is suggested by the preserved `astra_counting_nooverflow_depth`
table. All arithmetic below is checked against Agent #9's original `Local`,
and all path conclusions use the original complete `Path` predicate.
-/

namespace P196.Agent3.ThreeLayer

open P196.Agent9.InverseFibers

/-- A forced next carry state and predecessor coefficient for one column. -/
def Forced (s : Symbol) (p q : State) (x : Symbol) : Prop :=
  ∀ r : State, ∀ y : Symbol, Local s p r y.val → r = q ∧ y = x

theorem forced_14_0 : Forced 14 0 0 7 := by unfold Forced; decide
theorem forced_7_0 : Forced 7 0 1 3 := by unfold Forced; decide
theorem forced_3_0 : Forced 3 0 1 1 := by unfold Forced; decide
theorem forced_7_1 : Forced 7 1 3 13 := by unfold Forced; decide
theorem forced_13_1 : Forced 13 1 3 16 := by unfold Forced; decide
theorem forced_7_3 : Forced 7 3 2 13 := by unfold Forced; decide
theorem forced_13_3 : Forced 13 3 2 16 := by unfold Forced; decide
theorem forced_5_0 : Forced 5 0 1 2 := by unfold Forced; decide
theorem forced_2_2 : Forced 2 2 1 0 := by unfold Forced; decide

/-- Target zero has no inverse transition from carry state `(1,0)`. -/
theorem local_zero_two_impossible :
    ∀ q : State, ∀ x : Symbol, ¬ Local 0 2 q x.val := by
  decide

/-- Peel a forced column when the predecessor is a symbol-valued list. -/
theorem path_symbol_forced {s x : Symbol} {p q : State}
    (hf : Forced s p q x) (ss a : List Symbol)
    (h : Path (s :: ss) p (a.map Fin.val)) :
    ∃ as, a = x :: as ∧ Path ss q (as.map Fin.val) := by
  cases a with
  | nil => exact False.elim h
  | cons y ys =>
      obtain ⟨r, hl, ht⟩ := h
      obtain ⟨rfl, rfl⟩ := hf r y hl
      exact ⟨ys, rfl, ht⟩

/-- Peel a forced column without assuming a symbol-valued final ancestor. -/
theorem path_nat_forced {s x : Symbol} {p q : State}
    (hf : Forced s p q x) (ss : List Symbol) (a : List Nat)
    (h : Path (s :: ss) p a) :
    ∃ as, a = x.val :: as ∧ Path ss q as := by
  cases a with
  | nil => exact False.elim h
  | cons y ys =>
      obtain ⟨r, hl, ht⟩ := h
      have hr := hf r ⟨y, hl.1⟩ hl
      have hy : y = x.val := congrArg Fin.val hr.2
      obtain ⟨rfl, rfl⟩ := And.intro hr.1 hy
      exact ⟨ys, rfl, ht⟩

theorem path_zero_two_impossible (ss : List Symbol) (a : List Nat) :
    ¬ Path (0 :: ss) 2 a := by
  intro h
  cases a with
  | nil => exact h
  | cons x xs =>
      obtain ⟨q, hl, _⟩ := h
      exact local_zero_two_impossible q ⟨x, hl.1⟩ hl

/-- No suffix can repair this four-column failure of three no-overflow layers.
The final ancestor remains an arbitrary natural-coefficient list. -/
theorem no_three_paths_dead_prefix (tail a b : List Symbol) (c : List Nat) :
    ¬ (Path ([14, 14, 14, 5] ++ tail) 0 (a.map Fin.val) ∧
      Path a 0 (b.map Fin.val) ∧ Path b 0 c) := by
  rintro ⟨ha, hb, hc⟩
  change Path (14 :: 14 :: 14 :: 5 :: tail) 0 (a.map Fin.val) at ha
  obtain ⟨a1, rfl, ha1⟩ := path_symbol_forced forced_14_0 _ _ ha
  obtain ⟨a2, rfl, ha2⟩ := path_symbol_forced forced_14_0 _ _ ha1
  obtain ⟨a3, rfl, ha3⟩ := path_symbol_forced forced_14_0 _ _ ha2
  obtain ⟨a4, rfl, _⟩ := path_symbol_forced forced_5_0 _ _ ha3
  obtain ⟨b1, rfl, hb1⟩ := path_symbol_forced forced_7_0 _ _ hb
  obtain ⟨b2, rfl, hb2⟩ := path_symbol_forced forced_7_1 _ _ hb1
  obtain ⟨b3, rfl, hb3⟩ := path_symbol_forced forced_7_3 _ _ hb2
  obtain ⟨b4, rfl, _⟩ := path_symbol_forced forced_2_2 _ _ hb3
  obtain ⟨c1, rfl, hc1⟩ := path_nat_forced forced_3_0 _ _ hc
  obtain ⟨c2, rfl, hc2⟩ := path_nat_forced forced_13_1 _ _ hc1
  obtain ⟨c3, rfl, hc3⟩ := path_nat_forced forced_13_3 _ _ hc2
  exact path_zero_two_impossible b4 c3 hc3

end P196.Agent3.ThreeLayer
