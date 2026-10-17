import P196.Agent10EightCarry.PrefixCarryBound

/-!
Finite necessary-graph exclusion for the coefficient-six witness prefix.
The dynamic update is imported unchanged. Full carry-word agreement implies
the weak observations used here; the actual-width bridge is a separate step.

`survives n` checks observations at times 0 through n-1, using a shared control
bit at every step. The state after the final transition is unconstrained.
-/

set_option maxHeartbeats 0
set_option maxRecDepth 100000

namespace Agent10PrefixWitness
open CarryObservability

def compatible (s r : State) (v : Bool) : Bool :=
  decide (s.1 / 10 = r.1 / 10 ∧
    (s.2 + s.1 / 10) / 10 = (r.2 + r.1 / 10) / 10 ∧
    overflow s v = overflow r v)

def survives : Nat → State → State → Bool
  | 0, _, _ => true
  | n + 1, s, r =>
      (compatible s r false && survives n (next s false) (next r false)) ||
      (compatible s r true && survives n (next s true) (next r true))

/-- All 272 possible ordered starts are included, with both control bits at
every observation. The literal offset orientation is q-r=(1,-3). -/
theorem seven_prefix_exclusion_fin :
    ∀ p : Fin 17, ∀ q : Fin 16,
      survives 7 (p.val + 2, q.val) (p.val + 1, q.val + 3) = false := by
  decide +kernel

/-- Six observations remain possible in this necessary graph. -/
theorem six_prefix_survival : survives 6 (17, 3) (16, 6) = true := by
  decide +kernel

theorem seven_prefix_exclusion (s r : State)
    (hs : Valid s) (hr : Valid r)
    (hp : s.1 = r.1 + 1) (hq : r.2 = s.2 + 3) :
    survives 7 s r = false := by
  rcases s with ⟨p, q⟩
  rcases r with ⟨p', q'⟩
  rcases hs with ⟨hsp, hsp', hsq⟩
  rcases hr with ⟨hrp, hrp', hrq⟩
  simp only at hp hq
  have h := seven_prefix_exclusion_fin
    ⟨p' - 1, by omega⟩ ⟨q, by omega⟩
  have h1 : p' - 1 + 1 = p' := by omega
  have h2 : p' - 1 + 2 = p := by omega
  simpa only [h1, h2, ←hq] using h

#print axioms seven_prefix_exclusion_fin
#print axioms six_prefix_survival
#print axioms seven_prefix_exclusion

end Agent10PrefixWitness
