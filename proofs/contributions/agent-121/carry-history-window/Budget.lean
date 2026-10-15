import Std

namespace Agent121.CarryWindow

/-- Two exterior pair sums; a one-column word is represented separately. -/
structure State where
  single : Bool
  a : Nat
  b : Nat
  deriving DecidableEq, Repr

/-- The final carry predicted by the exterior and the incoming inner bit. -/
def boundaryCarry (s : State) (e : Nat) : Nat :=
  if s.single = true then s.a / 10
  else (s.a + (s.b + e) / 10) / 10

/-- Exact two-column candidate successor; the inner bit is free. -/
def nextState (s : State) (e : Nat) : State :=
  if s.single = true then
    if boundaryCarry s e = 0 then ⟨true, 2 * (s.a % 10), 0⟩
    else ⟨false, s.a % 10 + 1, s.a % 10 + 1⟩
  else
    let lo := (s.b + s.a / 10) % 10
    let hi := (s.a + (s.b + e) / 10) % 10
    if boundaryCarry s e = 0 then
      ⟨false, s.a % 10 + hi, lo + (s.b + e) % 10⟩
    else ⟨false, s.a % 10 + 1, lo + hi⟩

def stepCost (s : State) (e : Nat) : Nat :=
  if boundaryCarry s e = 0 then 1 else 0

/-- Minimum accumulated cost over every free inner-bit continuation. -/
def budget : Nat → State → Nat
  | 0, _ => 0
  | k+1, s => min (stepCost s 0 + budget k (nextState s 0))
                 (stepCost s 1 + budget k (nextState s 1))

theorem budget_step (k : Nat) (s : State) (e : Nat) (he : e ≤ 1) :
    budget (k+1) s ≤ stepCost s e + budget k (nextState s e) := by
  by_cases hz : e = 0
  · subst e
    exact Nat.min_le_left _ _
  · have h1 : e = 1 := by omega
    subst e
    exact Nat.min_le_right _ _

/-- A superset of the canonical exterior states, including odd singleton
pair sums. The enlargement only makes a lower bound harder to prove. -/
def states : List State :=
  (List.range 18).map (fun a => ⟨true, a+1, 0⟩) ++
  (List.range 18).flatMap (fun a =>
    (List.range 19).map (fun b => ⟨false, a+1, b⟩))

set_option maxRecDepth 100000 in
set_option maxHeartbeats 100000000 in
/-- A finite kernel reduction, with no hypothesis about an external table. -/
theorem checked_nine_budget : ∀ s ∈ states, 4 ≤ budget 9 s := by decide

theorem mem_states (s : State) (ha : 0 < s.a) (hb : s.a ≤ 18)
    (hc : s.b ≤ 18) (hs : s.single = true → s.b = 0) : s ∈ states := by
  cases s with
  | mk single a b =>
    cases single with
    | false =>
      apply List.mem_append_right
      apply List.mem_flatMap.mpr
      refine ⟨a-1, ?_, ?_⟩
      · simp only [List.mem_range]; omega
      · apply List.mem_map.mpr
        refine ⟨b, ?_, ?_⟩
        · simp only [List.mem_range]; omega
        · have he : a-1+1 = a := by omega
          simp only [he]
    | true =>
      have hz : b = 0 := hs rfl
      subst b
      apply List.mem_append_left
      apply List.mem_map.mpr
      refine ⟨a-1, ?_, ?_⟩
      · simp only [List.mem_range]; omega
      · have he : a-1+1 = a := by omega
        simp only [he]

/-- Dynamic-programming lower bounds apply to every genuine path in this
relation; no realizability of arbitrary free-bit paths is asserted. -/
theorem budget_le_path_cost (s : Nat → State) (e g : Nat → Nat) (K : Nat)
    (he : ∀ t, e t ≤ 1)
    (ht : ∀ t, s (t+1) = nextState (s t) (e t))
    (hg : ∀ t, g (t+1) = g t + stepCost (s t) (e t))
    (hzero : g 0 = 0) : budget K (s 0) ≤ g K := by
  have hp : ∀ k, k ≤ K → budget K (s 0) ≤ budget (K-k) (s k) + g k := by
    intro k
    induction k with
    | zero => intro _; simp only [Nat.sub_zero, hzero, Nat.add_zero, Nat.le_refl]
    | succ k ih =>
      intro hk
      have hprev := ih (by omega)
      have hlen : K-k = (K-(k+1))+1 := by omega
      have hstep := budget_step (K-(k+1)) (s k) (e k) (he k)
      rw [← hlen, ← ht k] at hstep
      rw [hg k]
      omega
  have hfinal := hp K (Nat.le_refl K)
  simpa only [Nat.sub_self, budget, Nat.zero_add] using hfinal

#print axioms budget_step
#print axioms checked_nine_budget
#print axioms mem_states
#print axioms budget_le_path_cost
end Agent121.CarryWindow
