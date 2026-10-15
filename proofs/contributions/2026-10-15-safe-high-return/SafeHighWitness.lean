import Std

/-!
An independent, finite ordinary-integer witness. Compile with Lean 4.19.0.
This file proves a lower bound only, not the existing all-width upper bound.
No native_decide, sorry, or user-declared axioms are used.
Verification status is tracked in FORMAL_STATUS.md; source is not a build log.
-/

set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace SafeHighWitness

/-- Structurally recursive digit extraction, with an explicit fuel argument. -/
def digitsAux : Nat → Nat → List Nat
  | 0, _ => []
  | fuel + 1, n =>
      if n = 0 then [] else n % 10 :: digitsAux fuel (n / 10)

/-- Canonical decimal digits, least significant first; zero uses [].
The initial fuel is n itself, not a fixed digit cap: every positive quotient
by ten is smaller than its input, so n recursive steps suffice for any n. -/
def digits10 (n : Nat) : List Nat := digitsAux n n

/-- Reverse canonical decimal digits, discarding any new leading zeros. -/
def reverse10 (n : Nat) : Nat :=
  (digits10 n).foldl (fun a d => 10 * a + d) 0

def step (n : Nat) : Nat := n + reverse10 n

def iterate (n : Nat) : Nat → Nat
  | 0 => n
  | t + 1 => step (iterate n t)

def pairWord (n : Nat) : List Nat :=
  let ds := digits10 n
  List.zipWith (fun x y => x + y) ds ds.reverse

def high (n : Nat) : Bool :=
  decide (10 ≤ (pairWord n).headD 0) &&
    (pairWord n).all (fun q => decide (9 ≤ q ∧ q ≤ 18))

def palindrome (n : Nat) : Bool :=
  decide (digits10 n = (digits10 n).reverse)

def orbit (t : Nat) : Nat := iterate 809999999 t

theorem exact_orbit :
    (List.range 9).map orbit =
      [809999999, 1809999907, 8909998988, 17808998086, 85898978957,
       161886968815, 680756656976, 1360413314062, 3964546454693] := by
  decide

theorem four_high_memberships :
    ∀ j : Fin 4, high (orbit (2 * j.val)) = true := by
  decide

theorem safe_before_eight :
    ∀ t : Fin 8, palindrome (orbit t.val) = false := by
  decide

theorem palindrome_at_eight : palindrome (orbit 8) = true := by
  decide

theorem exists_safe_three_returns :
    ∃ n : Nat, 0 < n ∧
      (∀ j : Fin 4, high (iterate n (2 * j.val)) = true) ∧
      (∀ t : Fin 7, palindrome (iterate n t.val) = false) := by
  exact ⟨809999999, by decide, by decide, by decide⟩

#print axioms exact_orbit
#print axioms four_high_memberships
#print axioms safe_before_eight
#print axioms palindrome_at_eight
#print axioms exists_safe_three_returns

end SafeHighWitness
