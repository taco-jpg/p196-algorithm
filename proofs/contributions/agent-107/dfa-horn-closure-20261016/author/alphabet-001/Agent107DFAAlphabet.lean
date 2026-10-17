import Agent107DFA

/-!
The exact finite alphabet used by the original Boolean learner: 19 pair
symbols and 11 distinct terminal slots. These bounds are derived from the
already checked literal tables, including the odd-overflow extra pair.
-/

namespace Agent107.FoldedDFA.Encoding

open Agent107.FoldedTransducer

def CenterValid (c : Option Nat) : Prop :=
  match c with
  | none => True
  | some v => v < 19 ∧ v % 2 = 0

instance (c : Option Nat) : Decidable (CenterValid c) := by
  unfold CenterValid
  cases c <;> infer_instance

def centerCode : Option Nat → Nat
  | none => 0
  | some v => v / 2 + 1

@[simp] theorem centerCode_none : centerCode none = 0 := rfl

@[simp] theorem centerCode_some_zero : centerCode (some 0) = 1 := rfl

theorem centerCode_lt (c : Option Nat) (hc : CenterValid c) : centerCode c < 11 := by
  cases c with
  | none => decide
  | some v =>
    have hv := hc.1
    simp only [centerCode]
    omega

/-- The sole finite state bound needed for all output alphabet bounds. -/
private theorem state_delay_lt (s : State) (hs : s ∈ Table.states) :
    s.delay.toNat < 10 := by
  have h : Table.states.all (fun t => decide (t.delay.toNat < 10)) = true := by decide
  exact of_decide_eq_true (List.all_eq_true.mp h s hs)

theorem edge_input_lt (e : Table.Edge) (he : e ∈ Table.edges) : e.input < 19 := by
  have h := (Table.edge_sound e he).2.2.1.1
  omega

theorem edge_output_lt (e : Table.Edge) (he : e ∈ Table.edges) : e.output < 19 := by
  have hs := Table.edge_sound e he
  have hd := state_delay_lt e.source hs.1
  rw [hs.2.2.2]
  unfold emit
  split <;> omega

theorem terminal_input_valid (r : Table.TerminalRow) (hr : r ∈ Table.terminals) :
    CenterValid r.center := by
  have ht := (Table.terminal_sound r hr).2.1
  cases hc : r.center with
  | none => simp [CenterValid, hc]
  | some v =>
    simp only [Terminal, hc] at ht
    simp only [CenterValid, hc]
    exact ⟨by have := ht.2.1; omega, ht.2.2.1⟩

theorem terminal_output_valid (r : Table.TerminalRow) (hr : r ∈ Table.terminals) :
    CenterValid r.outputCenter := by
  have hs := Table.terminal_sound r hr
  have hd := state_delay_lt r.source hs.1
  rw [hs.2.2.2]
  by_cases ho : r.source.overflow = 0
  · cases hc : r.center <;> simp [terminalCenter, ho, hc, CenterValid] <;> omega
  · cases hc : r.center <;> simp [terminalCenter, ho, hc, CenterValid] <;> omega

theorem terminal_extra_lt (r : Table.TerminalRow) (hr : r ∈ Table.terminals)
    (q : Nat) (hq : r.extra = some q) : q < 19 := by
  have hs := Table.terminal_sound r hr
  have hd := state_delay_lt r.source hs.1
  rw [hs.2.2.1] at hq
  by_cases ho : r.source.overflow = 0
  · simp [terminalExtra, ho] at hq
  · cases hc : r.center <;> simp [terminalExtra, ho, hc] at hq
    omega

theorem terminal_extra_center_none (r : Table.TerminalRow) (hr : r ∈ Table.terminals)
    (hx : r.extra ≠ none) : r.outputCenter = none := by
  have hs := Table.terminal_sound r hr
  rw [hs.2.2.1] at hx
  rw [hs.2.2.2]
  by_cases ho : r.source.overflow = 0
  · simp [terminalExtra, ho] at hx
  · cases hc : r.center with
    | none => simp [terminalExtra, ho, hc] at hx
    | some v => simp [terminalCenter, ho, hc]

#print axioms centerCode_none
#print axioms centerCode_some_zero
#print axioms centerCode_lt
#print axioms state_delay_lt
#print axioms edge_input_lt
#print axioms edge_output_lt
#print axioms terminal_input_valid
#print axioms terminal_output_valid
#print axioms terminal_extra_lt
#print axioms terminal_extra_center_none

end Agent107.FoldedDFA.Encoding
