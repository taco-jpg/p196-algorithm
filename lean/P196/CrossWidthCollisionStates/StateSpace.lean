import P196.Foundations.LychrelDigitSums

/-!
# Finite states for ordinary cross-width collisions

The state records one coefficient and two carry differences, each shifted
by one. A fifteen-state enclosure is closed under the local edge relation.
Four of those states have no outgoing edge, so a closed walk from the
initial state uses only the eleven states in `productive`.
-/

set_option autoImplicit false

namespace CrossWidthCollisionStates

open DecimalDigits

/-- A coefficient and two carry differences encoded by natural numbers. -/
structure State where
  x : Nat
  u : Nat
  v : Nat
  deriving DecidableEq, Repr

/-- The boundary state forced by an ordinary cross-width collision. -/
def initial : State := ⟨11, 2, 2⟩

/-- The state at a pair of complementary column boundaries.
Adding one before subtraction preserves a carry difference of minus one. -/
def stateAt (q r : Nat → Nat) (L i : Nat) : State :=
  ⟨q (i - 1), carry q i + 1 - carry r i,
    carry q (L - i + 1) + 1 - carry r (L - i + 1)⟩

/-- The eleven states that can occur in the closed collision trace. -/
def productive : List State :=
  [⟨11, 2, 2⟩, ⟨7, 0, 0⟩,
   ⟨0, 1, 1⟩, ⟨8, 1, 0⟩, ⟨10, 1, 2⟩, ⟨18, 1, 1⟩,
   ⟨8, 0, 1⟩, ⟨9, 1, 1⟩, ⟨10, 2, 1⟩,
   ⟨9, 0, 2⟩, ⟨9, 2, 0⟩]

/-- The possible next short and long coefficients at the initial edge. -/
def secondPairs : List (Nat × Nat) := [(0, 1), (9, 0), (10, 1), (11, 2)]

/-- A bounded local transition, retaining both inequalities for the
intermediate long coefficient before natural-number subtraction. -/
def Edge (s t : State) : Prop :=
  s.x ≤ 18 ∧ s.u ≤ 2 ∧ s.v ≤ 2 ∧
  t.x ≤ 18 ∧ t.u ≤ 2 ∧ t.v ≤ 2 ∧
  10 * s.v ≤ s.x + t.v + 9 ∧
  s.x + t.v + 9 ≤ 10 * s.v + 18 ∧
  t.x + s.u + 10 * s.v = s.x + t.v + 10 * t.u

instance edgeDecidable (s t : State) : Decidable (Edge s t) := by
  unfold Edge
  infer_instance

private def dead : List State :=
  [⟨0, 0, 2⟩, ⟨1, 1, 2⟩, ⟨17, 1, 0⟩, ⟨18, 2, 0⟩]

private def reachable : List State := productive ++ dead

private theorem reachable_closed_checked :
    reachable.all (fun s => decide (
      ∀ x : Fin 19, ∀ u v : Fin 3,
        Edge s ⟨x.val, u.val, v.val⟩ →
          (⟨x.val, u.val, v.val⟩ : State) ∈ reachable)) = true := by
  decide +kernel

private theorem dead_no_outgoing_checked :
    dead.all (fun s => decide (
      ∀ x : Fin 19, ∀ u v : Fin 3,
        ¬ Edge s ⟨x.val, u.val, v.val⟩)) = true := by
  decide +kernel

private theorem initial_edge_cases_checked :
    productive.all (fun t =>
      decide (Edge initial t → (t.x, t.v) ∈ secondPairs)) = true := by
  decide +kernel

private theorem reachable_closed {s t : State}
    (hs : s ∈ reachable) (he : Edge s t) : t ∈ reachable := by
  rcases t with ⟨x, u, v⟩
  have hx : x ≤ 18 := he.2.2.2.1
  have hu : u ≤ 2 := he.2.2.2.2.1
  have hv : v ≤ 2 := he.2.2.2.2.2.1
  have h := of_decide_eq_true (List.all_eq_true.mp reachable_closed_checked s hs)
  exact h ⟨x, by omega⟩ ⟨u, by omega⟩ ⟨v, by omega⟩ he

private theorem dead_no_outgoing {s t : State}
    (hs : s ∈ dead) (he : Edge s t) : False := by
  rcases t with ⟨x, u, v⟩
  have hx : x ≤ 18 := he.2.2.2.1
  have hu : u ≤ 2 := he.2.2.2.2.1
  have hv : v ≤ 2 := he.2.2.2.2.2.1
  have h := of_decide_eq_true (List.all_eq_true.mp dead_no_outgoing_checked s hs)
  exact h ⟨x, by omega⟩ ⟨u, by omega⟩ ⟨v, by omega⟩ he

/-- The productive catalogue has no repeated state. -/
theorem productive_nodup : productive.Nodup := by
  decide +kernel

/-- The productive catalogue contains exactly eleven states. -/
theorem productive_length : productive.length = 11 := by
  decide +kernel

/-- Every position in a closed walk from the initial state belongs to the
productive catalogue. The index range includes both boundary positions. -/
theorem closed_walk_mem_productive {L : Nat} (f : Nat → State)
    (hL : 1 ≤ L) (hfirst : f 1 = initial) (hlast : f L = initial)
    (hstep : ∀ i, 1 ≤ i → i < L → Edge (f i) (f (i + 1)))
    {i : Nat} (hi : 1 ≤ i) (hiL : i ≤ L) : f i ∈ productive := by
  have hreach : ∀ j, 1 ≤ j → j ≤ L → f j ∈ reachable := by
    intro j
    induction j with
    | zero =>
        intro hj _
        omega
    | succ j ih =>
        intro hj hjL
        by_cases hz : j = 0
        · subst j
          rw [hfirst]
          decide +kernel
        · exact reachable_closed (ih (by omega) (by omega))
            (hstep j (by omega) (by omega))
  by_cases hilast : i = L
  · rw [hilast, hlast]
    decide +kernel
  have hmem := hreach i hi hiL
  have hsplit : f i ∈ productive ∨ f i ∈ dead := by
    simpa only [reachable, List.mem_append] using hmem
  rcases hsplit with hp | hd
  · exact hp
  · exact False.elim (dead_no_outgoing hd (hstep i hi (by omega)))

/-- A productive successor of the initial state gives one of four
possible pairs of second coefficients. -/
theorem initial_edge_cases {t : State} (ht : t ∈ productive)
    (he : Edge initial t) : (t.x, t.v) ∈ secondPairs := by
  exact (of_decide_eq_true
    (List.all_eq_true.mp initial_edge_cases_checked t ht)) he

end CrossWidthCollisionStates

#print axioms CrossWidthCollisionStates.State
#print axioms CrossWidthCollisionStates.instDecidableEqState
#print axioms CrossWidthCollisionStates.instReprState
#print axioms CrossWidthCollisionStates.initial
#print axioms CrossWidthCollisionStates.stateAt
#print axioms CrossWidthCollisionStates.productive
#print axioms CrossWidthCollisionStates.secondPairs
#print axioms CrossWidthCollisionStates.Edge
#print axioms CrossWidthCollisionStates.edgeDecidable
#print axioms CrossWidthCollisionStates.productive_nodup
#print axioms CrossWidthCollisionStates.productive_length
#print axioms CrossWidthCollisionStates.closed_walk_mem_productive
#print axioms CrossWidthCollisionStates.initial_edge_cases
