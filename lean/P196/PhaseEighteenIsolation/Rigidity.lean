import P196.PhaseEighteenIsolation.Extremal

/-!
# Rigidity at the upper positional boundary

At a shared width, the normalized low observation determines at most two
bounded coefficient values when the target lies above one width scale.
The two positional values agree modulo nine. A high-value discrepancy of
at most two therefore rules out the missing low scale and forces the exact
high value as well. Existing two-value injectivity then recovers the word.
-/

namespace Agent5.PhaseEighteenIsolation

open Agent115.ExteriorFactorization Agent5.ExactDigitStreams
open Agent5.StreamObservationInjectivity

/-- A low residue at the target's upper width interval and the bounded high
tail relation recover the full word and force the tail quotient to be two.
All low-value upper bounds follow from the original coefficient bounds. -/
theorem boundary_values_rigidity (X Y : List Nat) (theta : Nat)
    (hlen : X.length = Y.length)
    (hX : ∀ x ∈ X, x ≤ 18) (hY : ∀ x ∈ Y, x ≤ 18)
    (hYlarge : 10 ^ Y.length ≤ lowValue Y)
    (hlow : lowValue X % 10 ^ Y.length = lowValue Y % 10 ^ Y.length)
    (hhigh : highValue X + theta = highValue Y + 2)
    (htheta : theta ≤ 2) :
    X = Y ∧ theta = 2 := by
  let P := 10 ^ Y.length
  change P ≤ lowValue Y at hYlarge
  change lowValue X % P = lowValue Y % P at hlow
  have hVX : lowValue X + 2 ≤ 2 * P := by
    have hb := highValue_lt X.reverse
      (fun x hx => hX x (List.mem_reverse.mp hx))
    simpa only [highValue_reverse_word, List.length_reverse, hlen] using hb
  have hVY : lowValue Y + 2 ≤ 2 * P := by
    have hb := highValue_lt Y.reverse
      (fun x hx => hY x (List.mem_reverse.mp hx))
    simpa only [highValue_reverse_word, List.length_reverse] using hb
  have hYmod : lowValue Y % P = lowValue Y - P := by
    rw [Nat.mod_eq_sub_mod hYlarge, Nat.mod_eq_of_lt (by omega)]
  have halternatives : lowValue X = lowValue Y ∨ lowValue X + P = lowValue Y := by
    by_cases hXL : P ≤ lowValue X
    · have hXmod : lowValue X % P = lowValue X - P := by
        rw [Nat.mod_eq_sub_mod hXL, Nat.mod_eq_of_lt (by omega)]
      rw [hXmod, hYmod] at hlow
      exact Or.inl (by omega)
    · have hXS : lowValue X < P := by omega
      rw [Nat.mod_eq_of_lt hXS, hYmod] at hlow
      exact Or.inr (by omega)
  have hmodX := lowValue_highValue_mod_nine X
  have hmodY := lowValue_highValue_mod_nine Y
  rcases halternatives with hsame | hmissing
  · have hlow9 := congrArg (fun v : Nat => v % 9) hsame
    have htheta2 : theta = 2 := by omega
    have hsameHigh : highValue X = highValue Y := by omega
    exact ⟨eq_of_values X Y hlen hX hY hsame hsameHigh, htheta2⟩
  · have hrepunit :
        9 * highValue (List.replicate Y.length 1) + 1 = P := by
      have hr := rhoNum_append_replicate 1 ([] : List Nat) Y.length
      have hz : rhoNum 1 [] = 1 := rfl
      rw [List.nil_append, hz, Nat.mul_one] at hr
      exact hr
    have hPmod : P % 9 = 1 := by omega
    have hlow9 := congrArg (fun v : Nat => v % 9) hmissing
    change (lowValue X + P) % 9 = lowValue Y % 9 at hlow9
    rw [Nat.add_mod, hPmod] at hlow9
    omega

#print axioms boundary_values_rigidity

end Agent5.PhaseEighteenIsolation
