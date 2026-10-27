import Std

namespace Agent115.CentralWindow

/-- O(a,2m) has code 10*a+m; E(a,b) has code 190+19*a+b. -/
abbrev State := Fin 551

def outer (s : State) : Nat :=
  if s.val < 190 then s.val / 10 else (s.val - 190) / 19

def middle (s : State) : Nat :=
  if s.val < 190 then 2 * (s.val % 10) else (s.val - 190) % 19

/-- The selected central window supplies both standard one-step witnesses.
This is a Boolean predicate on the abstract state, not an integer theorem. -/
def safe (s : State) : Bool :=
  decide ((10 ≤ outer s ∨ 10 ≤ middle s) ∧
    ((outer s ≠ 0 ∧ outer s ≠ 11) ∨ (middle s ≠ 0 ∧ middle s ≠ 11)))

/-- A control code is g + 2*c + 4*z, with g,c in {0,1}, z in {0,...,18}.
For an odd state, normalize [z,a,r,a,z] from carry c. For an even state,
normalize [a,b,b,a] from carry c; z is unused. The result is encoded in
the same odd/even convention. This definition specifies only a local graph. -/
def rawNext (s : State) (control : Nat) : Nat :=
  let g := control % 2
  let c := (control / 2) % 2
  let z := control / 4
  if s.val < 190 then
    let a := s.val / 10
    let r := 2 * (s.val % 10)
    let n1 := a + (z + c) / 10
    let n2 := r + n1 / 10
    let n3 := a + n2 / 10
    let n4 := z + n3 / 10
    if g = 0 then
      10 * (n1 % 10 + n3 % 10) + n2 % 10
    else
      190 + 19 * (n1 % 10 + n4 % 10) + (n2 % 10 + n3 % 10)
  else
    let a := (s.val - 190) / 19
    let b := (s.val - 190) % 19
    let n0 := a + c
    let n1 := b + n0 / 10
    let n2 := b + n1 / 10
    let n3 := a + n2 / 10
    if g = 0 then
      190 + 19 * (n0 % 10 + n3 % 10) + (n1 % 10 + n2 % 10)
    else
      10 * (n1 % 10 + n3 % 10) + n2 % 10

theorem rawNext_bounded (s : State) (control : Nat) : rawNext s control < 551 := by
  unfold rawNext
  split <;> dsimp only
  all_goals split <;> omega

def Edge (s t : State) : Prop :=
  ∃ control : Fin 76, rawNext s control.val = t.val

/-- Closure under every local edge, with every included state safe. -/
def UniversallySafe (S : State → Prop) : Prop :=
  (∀ s, S s → safe s = true) ∧
  (∀ s t, S s → Edge s t → S t)

/-- One chosen legal rank-decreasing edge per safe state suffices.
No assertion that all graph edges decrease the rank is required. -/
theorem no_invariant_of_selected_descent
    (rank : State → Nat) (selected : State → State)
    (hlegal : ∀ s, safe s = true → Edge s (selected s))
    (hdrop : ∀ s, safe s = true → rank (selected s) < rank s)
    (S : State → Prop) (hS : UniversallySafe S) : ∀ s, ¬ S s := by
  have h : ∀ n s, rank s = n → ¬ S s := by
    intro n
    induction n using Nat.strongRecOn with
    | ind n ih =>
      intro s hr hs
      have hsafe := hS.1 s hs
      have ht := hS.2 s (selected s) hs (hlegal s hsafe)
      have hlt := hdrop s hsafe
      exact ih (rank (selected s)) (by omega) (selected s) rfl ht
  intro s hs
  exact h (rank s) s rfl hs

end Agent115.CentralWindow
