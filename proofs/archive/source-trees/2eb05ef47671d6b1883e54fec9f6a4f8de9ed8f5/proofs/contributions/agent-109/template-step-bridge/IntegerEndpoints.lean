import Compat
import ActualWordBridge

/-!
Agent #109: Agent #8's premise-free canonical template obstructions
(`ActualWordBridge.lean`) transported to ordinary integers under the accepted
`Lychrel196.step`/`Lychrel196.orbit`, via `Agent109.Compat.pairWord_orbit`.
These are obstructions to specific returns only; no palindrome-avoidance claim.
-/

namespace Agent109.Endpoints

open Agent109

theorem pairWord_canonical (n : Nat) (hn : n ≠ 0) : Agent8.CanonicalPair (pairWord n) := by
  have hne : pairWord n ≠ [] := by
    have hlen := Agent8.pair_length (digits n)
    rw [Compat.pair_eq] at hlen
    apply List.ne_nil_of_length_pos
    unfold pairWord; rw [hlen, digits_pos n hn]; simp
  have hsym : (pairWord n).reverse = pairWord n := by
    have := Agent8.pair_symmetric (digits n)
    rw [Compat.pair_eq] at this; exact this
  refine ⟨hne, hsym, fun x hx => bounded_pair_digits n x hx, ?_⟩
  -- head of a symmetric word is its last coefficient, which is positive
  have hl := lastPos_pairWord n
  cases hw : pairWord n with
  | nil => exact absurd hw hne
  | cons x xs =>
    have h1 : (pairWord n).getLast? = some x := by
      rw [← hsym, List.getLast?_reverse, hw]; rfl
    simpa using hl x h1

/-- No positive integer whose pair word is a canonical two-gap template with
positive outer band returns to the same template shape after two actual
reverse-and-add steps (any band lengths). -/
theorem no_two_step_actual_template_return (n c : Nat) (B A C : Word)
    (g0 h0 g1 h1 : Nat) (hn : n ≠ 0) (hg0 : 0 < g0) (hg1 : 0 < g1)
    (hq : pairWord n = Agent8.template c B A C g0 h0) :
    pairWord (Lychrel196.orbit n 2) ≠ Agent8.template c B A C g1 h1 := by
  rw [Compat.pairWord_orbit, hq]
  have hw := pairWord_canonical n hn; rw [hq] at hw
  exact Agent8.no_two_step_canonical_template_return c B A C g0 h0 g1 h1 hg0 hg1 hw

/-- For the six-cycle phases, no positive integer realizing a template returns
after six actual steps to the same blocks with both band lengths not decreased. -/
theorem no_repeatable_six_step_actual_template_return (n c : Nat) (B A C : Word)
    (g0 h0 g1 h1 : Nat) (hn : n ≠ 0) (hc : Agent8.SixPhase c) (hg0 : 0 < g0)
    (hg : g0 ≤ g1) (hh : h0 ≤ h1)
    (hq : pairWord n = Agent8.template c B A C g0 h0) :
    pairWord (Lychrel196.orbit n 6) ≠ Agent8.template c B A C g1 h1 := by
  rw [Compat.pairWord_orbit, hq]
  have hw := pairWord_canonical n hn; rw [hq] at hw
  exact Agent8.no_repeatable_six_step_canonical_template_return c B A C g0 h0 g1 h1
    hc hg0 hw hg hh

end Agent109.Endpoints

#print axioms Agent109.Endpoints.pairWord_canonical
#print axioms Agent109.Endpoints.no_two_step_actual_template_return
#print axioms Agent109.Endpoints.no_repeatable_six_step_actual_template_return
