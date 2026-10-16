import Saturation

/-!
Agent #111: bounded width-dependent congruence conditions.

The original ExactLengthResidues fixed-modulus theorem is reused verbatim.
No conclusion about an actual palindrome hit of an orbit, nor about 196, is claimed.
The elementary factorial-like modulus below uses no Mathlib dependency.
-/

namespace Agent111.BoundedVariableModulus

open Lychrel196 DecimalDigits ExactLengthResidues

/-- Product of all positive integers up to K, defined without Mathlib. -/
def universalModulus : Nat → Nat
  | 0 => 1
  | k + 1 => (k + 1) * universalModulus k

theorem universalModulus_pos (K : Nat) : 0 < universalModulus K := by
  induction K with
  | zero => decide
  | succ k ih =>
      change 0 < (k + 1) * universalModulus k
      exact Nat.mul_pos (Nat.zero_lt_succ k) ih

/-- Every positive modulus bounded by K divides the common modulus. -/
theorem dvd_universalModulus (K : Nat) :
    ∀ m : Nat, 0 < m → m ≤ K → m ∣ universalModulus K := by
  induction K with
  | zero =>
      intro m hm hle
      omega
  | succ k ih =>
      intro m hm hle
      by_cases hmk : m ≤ k
      · obtain ⟨q, hq⟩ := ih m hm hmk
        refine ⟨(k + 1) * q, ?_⟩
        change (k + 1) * universalModulus k = m * ((k + 1) * q)
        rw [hq]
        ac_rfl
      · have heq : m = k + 1 := by omega
        subst m
        refine ⟨universalModulus k, ?_⟩
        rfl

/-- Congruence modulo a common multiple implies congruence modulo a factor. -/
theorem mod_eq_of_dvd {N d a b : Nat} (hd : d ∣ N)
    (hab : a % N = b % N) : a % d = b % d := by
  calc
    a % d = (a % N) % d := (Nat.mod_mod_of_dvd a hd).symm
    _ = (b % N) % d := congrArg (fun x : Nat => x % d) hab
    _ = b % d := Nat.mod_mod_of_dvd b hd

/-- A uniformly bounded but width-varying modulus cannot express more
eventual same-width membership information than one fixed common modulus. -/
theorem bounded_variable_saturation
    (S : Nat → Prop) (mu : Nat → Nat) (B K : Nat)
    (hmu : ∀ L, B ≤ L → 0 < mu L ∧ mu L ≤ K)
    (hsat : ∀ L, B ≤ L → ∀ n m (d e : Nat → Nat),
      Canonical n d L → Canonical m e L →
      n % (mu L) = m % (mu L) → (S n ↔ S m)) :
    SetSaturatedAbove S (universalModulus K) B := by
  intro L hL n m d e hn hm heq
  have hd : mu L ∣ universalModulus K :=
    dvd_universalModulus K (mu L) (hmu L hL).1 (hmu L hL).2
  exact hsat L hL n m d e hn hm (mod_eq_of_dvd hd heq)

/-- Obstruction for arbitrary width-dependent moduli with a uniform bound:
a nonempty positive reverse-add forward-closed set satisfying the above
saturation condition must include a genuine ordinary positive palindrome. -/
theorem bounded_variable_modulus_closed_set_contains_palindrome
    (S : Nat → Prop) (mu : Nat → Nat) (B K : Nat)
    (hmu : ∀ L, B ≤ L → 0 < mu L ∧ mu L ≤ K)
    (hsat : ∀ L, B ≤ L → ∀ n m (d e : Nat → Nat),
      Canonical n d L → Canonical m e L →
      n % (mu L) = m % (mu L) → (S n ↔ S m))
    (hne : ∃ n, 0 < n ∧ S n)
    (hclosed : ∀ n, 0 < n → S n → S (step n)) :
    ∃ p, 0 < p ∧ S p ∧ Palindrome p := by
  exact ExactLengthResidues.fixed_modulus_closed_set_contains_palindrome
    (universalModulus K) (universalModulus_pos K) S hne hclosed
    ⟨B, bounded_variable_saturation S mu B K hmu hsat⟩

end Agent111.BoundedVariableModulus

#print axioms Agent111.BoundedVariableModulus.universalModulus_pos
#print axioms Agent111.BoundedVariableModulus.dvd_universalModulus
#print axioms Agent111.BoundedVariableModulus.mod_eq_of_dvd
#print axioms Agent111.BoundedVariableModulus.bounded_variable_saturation
#print axioms Agent111.BoundedVariableModulus.bounded_variable_modulus_closed_set_contains_palindrome
