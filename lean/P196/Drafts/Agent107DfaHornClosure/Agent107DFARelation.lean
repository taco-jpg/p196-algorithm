import P196.Drafts.Agent1Agent104MonitorVerification.Agent107DFA

/-!
# The original 46-row Boolean relation as a relation on transducer states

The row order is the literal order of `Table.states`.  Lookup uses the executable
finite-list operation `List.finIdxOf?`; the verified absence of duplicate states
ensures that reading a row and looking it up returns its original index.
-/

namespace Agent107.FoldedDFA.Encoding

open Agent107.FoldedTransducer

abbrev TableIndex := Fin Table.states.length

def stateAt (i : TableIndex) : State := Table.states.get i

/-- A terminating first-match lookup in the original finite state table. -/
def stateIndex? (s : State) : Option TableIndex := Table.states.finIdxOf? s

theorem stateAt_injective {i j : TableIndex} (h : stateAt i = stateAt j) :
    i = j :=
  nodup_get_injective Table.states Table.states_nodup i j h

theorem stateAt_mem (i : TableIndex) : stateAt i ∈ Table.states :=
  List.get_mem Table.states i

@[simp] theorem stateIndex?_stateAt (i : TableIndex) :
    stateIndex? (stateAt i) = some i := by
  apply List.finIdxOf?_eq_some_iff.mpr
  refine ⟨rfl, ?_⟩
  intro j hj he
  have hji : j = i := stateAt_injective he
  have hv : j.val = i.val := congrArg Fin.val hji
  exact Nat.ne_of_lt hj hv

theorem stateIndex?_eq_some_iff (s : State) (i : TableIndex) :
    stateIndex? s = some i ↔ stateAt i = s := by
  constructor
  · intro h
    exact (List.finIdxOf?_eq_some_iff.mp h).1
  · intro h
    rw [← h]
    exact stateIndex?_stateAt i

@[simp] theorem stateIndex?_eq_none_iff (s : State) :
    stateIndex? s = none ↔ s ∉ Table.states :=
  List.finIdxOf?_eq_none_iff

theorem state_mem_iff_exists_stateAt (s : State) :
    s ∈ Table.states ↔ ∃ i : TableIndex, stateAt i = s :=
  List.mem_iff_get

theorem state_mem_iff_exists_index (s : State) :
    s ∈ Table.states ↔ ∃ i : TableIndex, stateIndex? s = some i := by
  rw [state_mem_iff_exists_stateAt]
  constructor
  · rintro ⟨i, hi⟩
    exact ⟨i, (stateIndex?_eq_some_iff s i).2 hi⟩
  · rintro ⟨i, hi⟩
    exact ⟨i, (stateIndex?_eq_some_iff s i).1 hi⟩

/-- Original row 0: the non-overflow initial state. -/
def initial0Index : TableIndex := ⟨0, by rw [Table.states_length]; decide⟩

/-- Original row 1: the overflow initial state, with delay 1. -/
def initial1Index : TableIndex := ⟨1, by rw [Table.states_length]; decide⟩

@[simp] theorem initial0Index_val : initial0Index.val = 0 := rfl
@[simp] theorem initial1Index_val : initial1Index.val = 1 := rfl

@[simp] theorem stateAt_initial0Index : stateAt initial0Index = initial 0 := rfl
@[simp] theorem stateAt_initial1Index : stateAt initial1Index = initial 1 := rfl

@[simp] theorem stateIndex?_initial0 : stateIndex? (initial 0) = some initial0Index := by
  rw [← stateAt_initial0Index]
  exact stateIndex?_stateAt initial0Index

@[simp] theorem stateIndex?_initial1 : stateIndex? (initial 1) = some initial1Index := by
  rw [← stateAt_initial1Index]
  exact stateIndex?_stateAt initial1Index

/-- Outside the literal table the lifted Boolean relation is false. -/
def liftRelation {N : Nat} (rawR : TableIndex → Fin N → Fin N → Bool)
    (s : State) (a b : Fin N) : Bool :=
  match stateIndex? s with
  | none => false
  | some i => rawR i a b

@[simp] theorem liftRelation_stateAt {N : Nat}
    (rawR : TableIndex → Fin N → Fin N → Bool) (i : TableIndex) (a b : Fin N) :
    liftRelation rawR (stateAt i) a b = rawR i a b := by
  simp only [liftRelation, stateIndex?_stateAt]

theorem liftRelation_of_not_mem {N : Nat}
    (rawR : TableIndex → Fin N → Fin N → Bool) (s : State) (a b : Fin N)
    (hs : s ∉ Table.states) : liftRelation rawR s a b = false := by
  simp only [liftRelation, (stateIndex?_eq_none_iff s).2 hs]

@[simp] theorem liftRelation_initial0 {N : Nat}
    (rawR : TableIndex → Fin N → Fin N → Bool) (a b : Fin N) :
    liftRelation rawR (initial 0) a b = rawR initial0Index a b := by
  simp only [liftRelation, stateIndex?_initial0]

@[simp] theorem liftRelation_initial1 {N : Nat}
    (rawR : TableIndex → Fin N → Fin N → Bool) (a b : Fin N) :
    liftRelation rawR (initial 1) a b = rawR initial1Index a b := by
  simp only [liftRelation, stateIndex?_initial1]

theorem liftRelation_initial0_start {N : Nat} (M : DFA N)
    (rawR : TableIndex → Fin N → Fin N → Bool) :
    liftRelation rawR (initial 0) M.start M.start =
      rawR initial0Index M.start M.start :=
  liftRelation_initial0 rawR M.start M.start

theorem liftRelation_initial1_start {N : Nat} (M : DFA N)
    (rawR : TableIndex → Fin N → Fin N → Bool) :
    liftRelation rawR (initial 1) M.start M.start =
      rawR initial1Index M.start M.start :=
  liftRelation_initial1 rawR M.start M.start

end Agent107.FoldedDFA.Encoding

#print axioms Agent107.FoldedDFA.Encoding.stateAt_injective
#print axioms Agent107.FoldedDFA.Encoding.stateIndex?_stateAt
#print axioms Agent107.FoldedDFA.Encoding.stateIndex?_eq_some_iff
#print axioms Agent107.FoldedDFA.Encoding.state_mem_iff_exists_index
#print axioms Agent107.FoldedDFA.Encoding.stateIndex?_initial0
#print axioms Agent107.FoldedDFA.Encoding.stateIndex?_initial1
#print axioms Agent107.FoldedDFA.Encoding.liftRelation_stateAt
#print axioms Agent107.FoldedDFA.Encoding.liftRelation_initial0_start
#print axioms Agent107.FoldedDFA.Encoding.liftRelation_initial1_start
