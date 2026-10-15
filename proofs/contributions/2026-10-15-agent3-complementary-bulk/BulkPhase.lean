import Lean

/-!
Agent #3: local arithmetic supporting the complementary-bulk quotient.
This file is self-contained (Lean 4.19.0 core only). The all-word quotient
identity is NOT formalized here. No statement concerns the infinite orbit
of 196. The carry reset and complement identities formalize Section 3 of
2026-10-15-complementary-bulk-quotient/METHOD_AND_PROOF.md. The exact phase
classification is an additional finite arithmetic observation.
-/

namespace P196.Agent3

def Admissible (x : Nat) : Prop := 1 <= x /\ x <= 17 /\ x ≠ 9

def carry (x : Nat) : Nat := if x < 9 then 0 else 1

def bulkDigit (x : Nat) : Nat := if x < 9 then x else x - 9

def phase (x : Nat) : Nat := 2 * bulkDigit x

def iterPhase : Nat -> Nat -> Nat
  | 0, x => x
  | n + 1, x => iterPhase n (phase x)

theorem carry_reset (x e : Nat) (hx : Admissible x) (he : e <= 1) :
    (x + e) / 10 = carry x := by
  unfold Admissible at hx
  unfold carry
  split <;> omega

theorem steady_digit (x : Nat) (hx : Admissible x) :
    (x + carry x) % 10 = bulkDigit x := by
  unfold Admissible at hx
  unfold carry bulkDigit
  split <;> omega

theorem complement_admissible (x : Nat) (hx : Admissible x) :
    Admissible (18 - x) := by
  unfold Admissible at *
  omega

theorem complementary_carries (x : Nat) (hx : Admissible x) :
    carry x + carry (18 - x) = 1 := by
  unfold Admissible at hx
  unfold carry
  split <;> split <;> omega

theorem complementary_digits (x : Nat) (hx : Admissible x) :
    bulkDigit x + bulkDigit (18 - x) = 9 := by
  unfold Admissible at hx
  unfold bulkDigit
  split <;> split <;> omega

theorem complementary_phases (x : Nat) (hx : Admissible x) :
    phase x + phase (18 - x) = 18 := by
  have h := complementary_digits x hx
  unfold phase
  omega

theorem phase_admissible (x : Nat) (hx : Admissible x) :
    Admissible (phase x) := by
  unfold Admissible at *
  unfold phase bulkDigit
  split <;> omega

theorem phase_even (x : Nat) : phase x % 2 = 0 := by
  unfold phase
  omega

theorem even_phase_classification (x : Nat) (hx : Admissible x)
    (he : x % 2 = 0) :
    x = 2 \/ x = 4 \/ x = 6 \/ x = 8 \/
    x = 10 \/ x = 12 \/ x = 14 \/ x = 16 := by
  unfold Admissible at hx
  omega

theorem even_phase_period_six (x : Nat) (hx : Admissible x)
    (he : x % 2 = 0) : iterPhase 6 x = x := by
  rcases even_phase_classification x hx he with h | h | h | h | h | h | h | h
  all_goals subst x; decide

theorem all_phases_eventually_period_six (x : Nat) (hx : Admissible x) :
    iterPhase 6 (phase x) = phase x :=
  even_phase_period_six (phase x) (phase_admissible x hx) (phase_even x)

theorem period_two_iff (x : Nat) (hx : Admissible x) (he : x % 2 = 0) :
    iterPhase 2 x = x <-> x = 6 \/ x = 12 := by
  rcases even_phase_classification x hx he with h | h | h | h | h | h | h | h
  all_goals subst x; decide

theorem no_fixed_phase (x : Nat) (hx : Admissible x) : phase x ≠ x := by
  unfold Admissible at hx
  unfold phase bulkDigit
  split <;> omega

#print axioms carry_reset
#print axioms steady_digit
#print axioms complement_admissible
#print axioms complementary_carries
#print axioms complementary_digits
#print axioms complementary_phases
#print axioms phase_admissible
#print axioms phase_even
#print axioms even_phase_classification
#print axioms even_phase_period_six
#print axioms all_phases_eventually_period_six
#print axioms period_two_iff
#print axioms no_fixed_phase

end P196.Agent3
