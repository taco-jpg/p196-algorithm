import P196.CrossWidthCollisionPaths.Profiles

/-!
# Reflection and terminal extension for collision prefixes

The two terminal predicates express the possible center joins of a
reflected collision path. On the existing productive state catalogue,
an even terminal has one explicitly determined odd terminal successor.
Uniqueness of an odd terminal successor holds for the entire edge relation.
-/

set_option autoImplicit false

namespace FoldedCollisionPrefixes

open CrossWidthCollisionStates CrossWidthCollisionPaths

/-- A doubled center is joined by a reflected edge whose coefficient
is even. The edge includes the necessary bounds and subtraction guard. -/
def EvenTerminal (s : State) : Prop :=
  Edge s (flip s) ∧ (s.x + s.u + 9 - 10 * s.v) % 2 = 0

/-- A single center is fixed by reflection and has an even coefficient. -/
def OddTerminal (s : State) : Prop := s.u = s.v ∧ s.x % 2 = 0

instance evenTerminalDecidable (s : State) : Decidable (EvenTerminal s) := by
  unfold EvenTerminal
  infer_instance

instance oddTerminalDecidable (s : State) : Decidable (OddTerminal s) := by
  unfold OddTerminal
  infer_instance

/-- Exchanging the two carry coordinates twice restores the state. -/
theorem flip_involution (s : State) : flip (flip s) = s := by
  cases s
  rfl

/-- The boundary state is fixed by reflection. -/
theorem flip_initial : flip initial = initial := rfl

/-- Reflection reverses every edge, including its coefficient bounds. -/
theorem edge_flip_iff (s t : State) :
    Edge s t ↔ Edge (flip t) (flip s) := by
  rcases s with ⟨x, u, v⟩
  rcases t with ⟨y, p, z⟩
  simp only [Edge, CrossWidthCollisionPaths.flip]
  omega

/-- An odd terminal is fixed by the reflection map. -/
theorem oddTerminal_flip {s : State} (h : OddTerminal s) : flip s = s := by
  rcases s with ⟨x, u, v⟩
  have huv : u = v := h.1
  cases huv
  rfl

/-- Two odd terminal successors of the same state must coincide.
Their even coefficients cannot differ by a nonzero even multiple of eleven
while both remain between zero and eighteen. -/
theorem odd_successor_unique {s t t' : State}
    (he : Edge s t) (he' : Edge s t')
    (ht : OddTerminal t) (ht' : OddTerminal t') : t = t' := by
  rcases s with ⟨x, u, v⟩
  rcases t with ⟨y, p, z⟩
  rcases t' with ⟨y', p', z'⟩
  simp only [Edge, OddTerminal] at he he' ht ht'
  have hcoords : y = y' ∧ p = p' ∧ z = z' := by omega
  obtain ⟨rfl, rfl, rfl⟩ := hcoords
  rfl

/-- The explicit odd terminal extension of a productive even terminal. -/
def terminalExtension (s : State) : State :=
  ⟨s.x + 11 - s.u - 10 * s.v, 1, 1⟩

/-- A productive state has an odd terminal successor exactly when it
is an even terminal, and that successor is the explicit extension. -/
theorem productive_terminal_extension_iff {s t : State}
    (hs : s ∈ productive) :
    (Edge s t ∧ OddTerminal t) ↔
      (EvenTerminal s ∧ t = terminalExtension s) := by
  rcases t with ⟨x, u, v⟩
  simp [productive] at hs
  rcases hs with rfl | rfl | rfl | rfl | rfl | rfl |
    rfl | rfl | rfl | rfl | rfl <;>
    simp [EvenTerminal, OddTerminal, Edge, CrossWidthCollisionPaths.flip,
      terminalExtension, State.mk.injEq] <;>
    omega

#print axioms EvenTerminal
#print axioms OddTerminal
#print axioms evenTerminalDecidable
#print axioms oddTerminalDecidable
#print axioms flip_involution
#print axioms flip_initial
#print axioms edge_flip_iff
#print axioms oddTerminal_flip
#print axioms odd_successor_unique
#print axioms terminalExtension
#print axioms productive_terminal_extension_iff

end FoldedCollisionPrefixes
