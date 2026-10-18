import P196.Drafts.Agent1Agent104MonitorVerification.Agent107DFA

/-!
# A finite Boolean checker for the folded Horn certificate

The checker enumerates the two initial states, every literal edge and terminal
row, and every pair in `Fin N` using `List.all`.  It never enumerates the infinite
ambient `State` type.  The reflection theorem identifies the Boolean relation
with the proposition that its value is `true`.
-/

namespace Agent107.FoldedDFA

open Agent107.FoldedTransducer

/-- Boolean implication, used for each finite Horn clause. -/
def boolImplies (a b : Bool) : Bool := !a || b

theorem boolImplies_iff (a b : Bool) :
    boolImplies a b = true ↔ (a = true → b = true) := by
  cases a <;> cases b <;> simp [boolImplies]

/-- Explicit finite enumeration, including the empty `Fin 0` case. -/
def allFin {N : Nat} (p : Fin N → Bool) : Bool :=
  (List.finRange N).all p

theorem allFin_iff {N : Nat} (p : Fin N → Bool) :
    allFin p = true ↔ ∀ i : Fin N, p i = true := by
  rw [allFin, List.all_eq_true]
  constructor
  · intro h i
    exact h i (List.mem_ofFn.mpr ⟨i, rfl⟩)
  · intro h i _
    exact h i

def checkStarts {N : Nat} (M : DFA N)
    (rb : State → Fin N → Fin N → Bool) : Bool :=
  ([0, 1] : List Nat).all (fun h => rb (initial h) M.start M.start)

def checkEdges {N : Nat} (M : DFA N)
    (rb : State → Fin N → Fin N → Bool) : Bool :=
  Table.edges.all fun e => allFin fun a => allFin fun b =>
    boolImplies (rb e.source a b)
      (rb e.target (M.step a e.input) (M.step b e.output))

def checkTerminals {N : Nat} (M : DFA N)
    (rb : State → Fin N → Fin N → Bool) : Bool :=
  Table.terminals.all fun r => allFin fun a => allFin fun b =>
    boolImplies (rb r.source a b)
      (boolImplies (M.final a r.center)
        (M.final (M.run b r.extra.toList) r.outputCenter))

/-- The exact finite conjunction of the three families of Horn clauses. -/
def checkHorn {N : Nat} (M : DFA N)
    (rb : State → Fin N → Fin N → Bool) : Bool :=
  (checkStarts M rb && checkEdges M rb) && checkTerminals M rb

theorem checkStarts_iff {N : Nat} (M : DFA N)
    (rb : State → Fin N → Fin N → Bool) :
    checkStarts M rb = true ↔
      ∀ h : Nat, h ≤ 1 → rb (initial h) M.start M.start = true := by
  rw [checkStarts, List.all_eq_true]
  constructor
  · intro hc h hh
    apply hc h
    simp only [List.mem_cons, List.mem_singleton]
    omega
  · intro hc h hh
    apply hc h
    simp only [List.mem_cons, List.mem_singleton, List.not_mem_nil, or_false] at hh
    omega

theorem checkEdges_iff {N : Nat} (M : DFA N)
    (rb : State → Fin N → Fin N → Bool) :
    checkEdges M rb = true ↔
      ∀ e ∈ Table.edges, ∀ a b : Fin N,
        rb e.source a b = true →
        rb e.target (M.step a e.input) (M.step b e.output) = true := by
  simp only [checkEdges, List.all_eq_true, allFin_iff, boolImplies_iff]

theorem checkTerminals_iff {N : Nat} (M : DFA N)
    (rb : State → Fin N → Fin N → Bool) :
    checkTerminals M rb = true ↔
      ∀ r ∈ Table.terminals, ∀ a b : Fin N,
        rb r.source a b = true → M.final a r.center = true →
        M.final (M.run b r.extra.toList) r.outputCenter = true := by
  simp only [checkTerminals, List.all_eq_true, allFin_iff, boolImplies_iff]

theorem checkHorn_iff {N : Nat} (M : DFA N)
    (rb : State → Fin N → Fin N → Bool) :
    checkHorn M rb = true ↔ Horn M (fun s a b => rb s a b = true) := by
  rw [checkHorn, Bool.and_eq_true, Bool.and_eq_true,
    checkStarts_iff, checkEdges_iff, checkTerminals_iff]
  constructor
  · rintro ⟨⟨hs, he⟩, ht⟩
    exact ⟨hs, he, ht⟩
  · intro h
    exact ⟨⟨h.starts, h.edges⟩, h.terminals⟩

end Agent107.FoldedDFA

#print axioms Agent107.FoldedDFA.boolImplies_iff
#print axioms Agent107.FoldedDFA.allFin_iff
#print axioms Agent107.FoldedDFA.checkStarts_iff
#print axioms Agent107.FoldedDFA.checkEdges_iff
#print axioms Agent107.FoldedDFA.checkTerminals_iff
#print axioms Agent107.FoldedDFA.checkHorn_iff
