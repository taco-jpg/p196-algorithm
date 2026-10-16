import Agent107TransducerTables

/-! Exact finite-transition reachability of the original 46-state table.
Every noninitial witness is an explicit prior witness and a kernel-decided Transition. -/

namespace Agent107.FoldedTransducer

inductive Reachable : State → Prop where
  | initial (h : Nat) (bounded : h ≤ 1) : Reachable (initial h)
  | step {s t : State} (q : Nat) (previous : Reachable s)
      (transition : Transition s q t) : Reachable t

theorem reachable_mem_states {s : State} (h : Reachable s) : s ∈ Table.states := by
  induction h with
  | initial h hh => exact Table.starts_mem h hh
  | @step s t q _ htrans ih => exact Table.states_closed s t q ih htrans

theorem reachable_state0 : Reachable Table.state0 :=
  Reachable.initial 0 (by decide)

theorem reachable_state1 : Reachable Table.state1 :=
  Reachable.initial 1 (by decide)

theorem reachable_state2 : Reachable Table.state2 :=
  Reachable.step 1 reachable_state0 (by decide)

theorem reachable_state3 : Reachable Table.state3 :=
  Reachable.step 1 reachable_state0 (by decide)

theorem reachable_state4 : Reachable Table.state4 :=
  Reachable.step 9 reachable_state1 (by decide)

theorem reachable_state5 : Reachable Table.state5 :=
  Reachable.step 10 reachable_state1 (by decide)

theorem reachable_state6 : Reachable Table.state6 :=
  Reachable.step 10 reachable_state1 (by decide)

theorem reachable_state7 : Reachable Table.state7 :=
  Reachable.step 11 reachable_state1 (by decide)

theorem reachable_state8 : Reachable Table.state8 :=
  Reachable.step 11 reachable_state1 (by decide)

theorem reachable_state9 : Reachable Table.state9 :=
  Reachable.step 12 reachable_state1 (by decide)

theorem reachable_state10 : Reachable Table.state10 :=
  Reachable.step 12 reachable_state1 (by decide)

theorem reachable_state11 : Reachable Table.state11 :=
  Reachable.step 13 reachable_state1 (by decide)

theorem reachable_state12 : Reachable Table.state12 :=
  Reachable.step 13 reachable_state1 (by decide)

theorem reachable_state13 : Reachable Table.state13 :=
  Reachable.step 14 reachable_state1 (by decide)

theorem reachable_state14 : Reachable Table.state14 :=
  Reachable.step 14 reachable_state1 (by decide)

theorem reachable_state15 : Reachable Table.state15 :=
  Reachable.step 15 reachable_state1 (by decide)

theorem reachable_state16 : Reachable Table.state16 :=
  Reachable.step 15 reachable_state1 (by decide)

theorem reachable_state17 : Reachable Table.state17 :=
  Reachable.step 16 reachable_state1 (by decide)

theorem reachable_state18 : Reachable Table.state18 :=
  Reachable.step 16 reachable_state1 (by decide)

theorem reachable_state19 : Reachable Table.state19 :=
  Reachable.step 17 reachable_state1 (by decide)

theorem reachable_state20 : Reachable Table.state20 :=
  Reachable.step 17 reachable_state1 (by decide)

theorem reachable_state21 : Reachable Table.state21 :=
  Reachable.step 18 reachable_state1 (by decide)

theorem reachable_state22 : Reachable Table.state22 :=
  Reachable.step 18 reachable_state1 (by decide)

theorem reachable_state23 : Reachable Table.state23 :=
  Reachable.step 10 reachable_state3 (by decide)

theorem reachable_state24 : Reachable Table.state24 :=
  Reachable.step 10 reachable_state3 (by decide)

theorem reachable_state25 : Reachable Table.state25 :=
  Reachable.step 0 reachable_state5 (by decide)

theorem reachable_state26 : Reachable Table.state26 :=
  Reachable.step 0 reachable_state5 (by decide)

theorem reachable_state27 : Reachable Table.state27 :=
  Reachable.step 1 reachable_state5 (by decide)

theorem reachable_state28 : Reachable Table.state28 :=
  Reachable.step 1 reachable_state5 (by decide)

theorem reachable_state29 : Reachable Table.state29 :=
  Reachable.step 2 reachable_state5 (by decide)

theorem reachable_state30 : Reachable Table.state30 :=
  Reachable.step 2 reachable_state5 (by decide)

theorem reachable_state31 : Reachable Table.state31 :=
  Reachable.step 3 reachable_state5 (by decide)

theorem reachable_state32 : Reachable Table.state32 :=
  Reachable.step 3 reachable_state5 (by decide)

theorem reachable_state33 : Reachable Table.state33 :=
  Reachable.step 4 reachable_state5 (by decide)

theorem reachable_state34 : Reachable Table.state34 :=
  Reachable.step 4 reachable_state5 (by decide)

theorem reachable_state35 : Reachable Table.state35 :=
  Reachable.step 5 reachable_state5 (by decide)

theorem reachable_state36 : Reachable Table.state36 :=
  Reachable.step 5 reachable_state5 (by decide)

theorem reachable_state37 : Reachable Table.state37 :=
  Reachable.step 6 reachable_state5 (by decide)

theorem reachable_state38 : Reachable Table.state38 :=
  Reachable.step 6 reachable_state5 (by decide)

theorem reachable_state39 : Reachable Table.state39 :=
  Reachable.step 7 reachable_state5 (by decide)

theorem reachable_state40 : Reachable Table.state40 :=
  Reachable.step 7 reachable_state5 (by decide)

theorem reachable_state41 : Reachable Table.state41 :=
  Reachable.step 8 reachable_state5 (by decide)

theorem reachable_state42 : Reachable Table.state42 :=
  Reachable.step 8 reachable_state5 (by decide)

theorem reachable_state43 : Reachable Table.state43 :=
  Reachable.step 9 reachable_state5 (by decide)

theorem reachable_state44 : Reachable Table.state44 :=
  Reachable.step 9 reachable_state6 (by decide)

theorem reachable_state45 : Reachable Table.state45 :=
  Reachable.step 9 reachable_state25 (by decide)

theorem mem_states_reachable (s : State) (hs : s ∈ Table.states) : Reachable s := by
  simp only [Table.states, List.mem_cons, List.mem_nil_iff, or_false] at hs
  rcases hs with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · exact reachable_state0
  · exact reachable_state1
  · exact reachable_state2
  · exact reachable_state3
  · exact reachable_state4
  · exact reachable_state5
  · exact reachable_state6
  · exact reachable_state7
  · exact reachable_state8
  · exact reachable_state9
  · exact reachable_state10
  · exact reachable_state11
  · exact reachable_state12
  · exact reachable_state13
  · exact reachable_state14
  · exact reachable_state15
  · exact reachable_state16
  · exact reachable_state17
  · exact reachable_state18
  · exact reachable_state19
  · exact reachable_state20
  · exact reachable_state21
  · exact reachable_state22
  · exact reachable_state23
  · exact reachable_state24
  · exact reachable_state25
  · exact reachable_state26
  · exact reachable_state27
  · exact reachable_state28
  · exact reachable_state29
  · exact reachable_state30
  · exact reachable_state31
  · exact reachable_state32
  · exact reachable_state33
  · exact reachable_state34
  · exact reachable_state35
  · exact reachable_state36
  · exact reachable_state37
  · exact reachable_state38
  · exact reachable_state39
  · exact reachable_state40
  · exact reachable_state41
  · exact reachable_state42
  · exact reachable_state43
  · exact reachable_state44
  · exact reachable_state45

theorem reachable_iff_mem_states (s : State) : Reachable s ↔ s ∈ Table.states :=
  ⟨reachable_mem_states, mem_states_reachable s⟩

#print axioms reachable_mem_states
#print axioms reachable_state0
#print axioms reachable_state1
#print axioms reachable_state2
#print axioms reachable_state3
#print axioms reachable_state4
#print axioms reachable_state5
#print axioms reachable_state6
#print axioms reachable_state7
#print axioms reachable_state8
#print axioms reachable_state9
#print axioms reachable_state10
#print axioms reachable_state11
#print axioms reachable_state12
#print axioms reachable_state13
#print axioms reachable_state14
#print axioms reachable_state15
#print axioms reachable_state16
#print axioms reachable_state17
#print axioms reachable_state18
#print axioms reachable_state19
#print axioms reachable_state20
#print axioms reachable_state21
#print axioms reachable_state22
#print axioms reachable_state23
#print axioms reachable_state24
#print axioms reachable_state25
#print axioms reachable_state26
#print axioms reachable_state27
#print axioms reachable_state28
#print axioms reachable_state29
#print axioms reachable_state30
#print axioms reachable_state31
#print axioms reachable_state32
#print axioms reachable_state33
#print axioms reachable_state34
#print axioms reachable_state35
#print axioms reachable_state36
#print axioms reachable_state37
#print axioms reachable_state38
#print axioms reachable_state39
#print axioms reachable_state40
#print axioms reachable_state41
#print axioms reachable_state42
#print axioms reachable_state43
#print axioms reachable_state44
#print axioms reachable_state45
#print axioms mem_states_reachable
#print axioms reachable_iff_mem_states

end Agent107.FoldedTransducer
