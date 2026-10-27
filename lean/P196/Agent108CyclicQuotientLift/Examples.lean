import P196.Agent108CyclicQuotientLift.QuotientLift

/-!
# Boundary examples for quotient power lifting

These small labelled graphs distinguish positive-power lifting from one-lap
lifting, a periodic vertex from a prescribed transient source, and pointwise
edge lifting from a homomorphism alone. They are abstract graph examples,
not the separate base-six exterior example of Agent105.
-/

namespace Agent108.CyclicQuotientLift.Examples

def collapse (_ : Bool) : Unit := ()
def selfLoop (_ : Unit) (_ : Unit) (_ : Unit) : Prop := True
def toggleEdge (x : Bool) (_ : Unit) (y : Bool) : Prop := y = !x
def transientEdge (_ : Bool) (_ : Unit) (y : Bool) : Prop := y = true
def acyclicEdge (x : Bool) (_ : Unit) (y : Bool) : Prop :=
  x = false ∧ y = true

/-- The toggle quotient has both a homomorphism and pointwise lifting. -/
theorem toggle_quotient :
    (∀ x a y, toggleEdge x a y → selfLoop (collapse x) a (collapse y)) ∧
    (∀ x a q, selfLoop (collapse x) a q →
      ∃ y, toggleEdge x a y ∧ collapse y = q) := by
  constructor
  · intro x a y _
    trivial
  · intro x a q _
    cases q
    exact ⟨!x, rfl, rfl⟩

/-- The quotient has a one-letter loop, but the original requires two laps. -/
theorem toggle_requires_two_laps :
    Walk selfLoop () [()] () ∧
    (∀ x, ¬ Walk toggleEdge x [()] x) ∧
    (∀ x, Walk toggleEdge x (wordPower [()] 2) x) := by
  refine ⟨⟨(), trivial, rfl⟩, ?_, ?_⟩
  · intro x h
    obtain ⟨z, hfirst, hrest⟩ := h
    have hz : z = x := hrest
    have htoggle : x = !x := hz.symm.trans hfirst
    cases x <;> cases htoggle
  · intro x
    refine ⟨!x, rfl, x, ?_, rfl⟩
    cases x <;> rfl

/-- A quotient with pointwise lifting can still contain a transient source. -/
theorem transient_quotient :
    (∀ x a y, transientEdge x a y → selfLoop (collapse x) a (collapse y)) ∧
    (∀ x a q, selfLoop (collapse x) a q →
      ∃ y, transientEdge x a y ∧ collapse y = q) := by
  constructor
  · intro x a y _
    trivial
  · intro x a q _
    cases q
    exact ⟨true, rfl, rfl⟩

/-- State false never returns after a nonempty word, although true loops. -/
theorem transient_returns_only_at_true :
    (∀ w, w ≠ [] → ¬ Walk transientEdge false w false) ∧
    Walk transientEdge true [()] true := by
  have ends_false : ∀ w (x : Bool), Walk transientEdge x w false → w = [] := by
    intro w
    induction w with
    | nil => intro x _; rfl
    | cons a w ih =>
        intro x h
        obtain ⟨z, hfirst, hrest⟩ := h
        have hempty := ih z hrest
        subst w
        have hz_false : z = false := hrest
        have hz_true : z = true := hfirst
        cases hz_false.symm.trans hz_true
  constructor
  · intro w hnonempty h
    exact hnonempty (ends_false w false h)
  · exact ⟨true, rfl, rfl⟩

/-- Merging an acyclic edge creates a loop but fails pointwise lifting. -/
theorem homomorphism_without_lifting :
    (∀ x a y, acyclicEdge x a y → selfLoop (collapse x) a (collapse y)) ∧
    Walk selfLoop () [()] () ∧
    ¬ (∀ x a q, selfLoop (collapse x) a q →
      ∃ y, acyclicEdge x a y ∧ collapse y = q) := by
  refine ⟨?_, ⟨(), trivial, rfl⟩, ?_⟩
  · intro x a y _
    trivial
  · intro h
    obtain ⟨y, hfirst, _⟩ := h true () () trivial
    cases hfirst.1

/-- The original acyclic graph has no nonempty closed word of any length. -/
theorem merged_acyclic_no_return :
    ∀ x w, w ≠ [] → ¬ Walk acyclicEdge x w x := by
  have from_true : ∀ w (y : Bool), Walk acyclicEdge true w y → w = [] := by
    intro w y h
    cases w with
    | nil => rfl
    | cons a w =>
        obtain ⟨z, hfirst, _⟩ := h
        cases hfirst.1
  intro x w hnonempty h
  cases w with
  | nil => exact hnonempty rfl
  | cons a w =>
      obtain ⟨z, hfirst, hrest⟩ := h
      obtain ⟨hx, hz⟩ := hfirst
      subst x
      subst z
      have hempty := from_true w false hrest
      subst w
      cases hrest

def emptyCollapse (_ : Empty) : Unit := ()
def emptyEdge (_ : Empty) (_ : Unit) (_ : Empty) : Prop := True

/-- Vacuous pointwise lifting cannot replace a nonempty fiber assumption. -/
theorem empty_fiber_boundary :
    (∀ x a q, selfLoop (emptyCollapse x) a q →
      ∃ y, emptyEdge x a y ∧ emptyCollapse y = q) ∧
    ¬ (∃ x, emptyCollapse x = ()) ∧
    Walk selfLoop () [()] () ∧
    ¬ ClosedWith emptyEdge (fun _ => True) := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro x
    exact nomatch x
  · rintro ⟨x, _⟩
    exact nomatch x
  · exact ⟨(), trivial, rfl⟩
  · rintro ⟨x, _, _, _, _⟩
    exact nomatch x

end Agent108.CyclicQuotientLift.Examples
