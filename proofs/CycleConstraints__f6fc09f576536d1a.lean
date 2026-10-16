import Lean.Elab.Tactic.Omega

/-!
Agent #4: arithmetic constraints for complementary-bulk cycles.
The actual whole-word quotient bridge is a written proof, not established by
this module. Every premise of the arithmetic reductions remains explicit.
Compile with Lean 4.19.0; see STATUS.md for actual build/audit status.
-/
namespace P196.Agent4

/-- Sum of digits after carry normalization, including the final carry.
For canonical pair coefficients the final carry is a bit and this is exactly
the ordinary output digit sum. The congruence below needs no digit bounds. -/
def normalizedMass : List Nat → Nat → Nat
  | [], carry => carry
  | a :: w, carry => (a + carry) % 10 + normalizedMass w ((a + carry) / 10)

theorem normalizedMass_mod_nine (w : List Nat) (carry : Nat) :
    normalizedMass w carry % 9 = (w.sum + carry) % 9 := by
  induction w generalizing carry with
  | nil => simp [normalizedMass]
  | cons a w ih =>
      have htail := ih ((a + carry) / 10)
      have hdiv := Nat.mod_add_div (a + carry) 10
      simp only [normalizedMass, List.sum_cons]
      omega

/-- This is the exact outer-pair update for an incoming last-column carry bit. -/
def outerOverflow (p e : Nat) : Nat := if 10 ≤ p + e then 1 else 0

def outerNext (p e : Nat) : Nat :=
  if 10 ≤ p + e then 1 + p % 10 else 2*p + e

def upperPotential : Nat → Nat
  | 4 | 6 | 7 | 8 | 10 | 11 | 12 | 14 => 1
  | 9 | 13 | 15 | 16 | 17 => 2
  | 18 => 3
  | _ => 0

/-- Complete 18-by-2 arithmetic check; kernel reduction, not native_decide. -/
theorem outer_upper_step :
    ∀ p : Fin 19, ∀ e : Fin 2, 0 < p.val →
      2 * outerOverflow p.val e.val + upperPotential (outerNext p.val e.val)
        ≤ 1 + upperPotential p.val := by decide

def total (f : Nat → Nat) : Nat → Nat
  | 0 => 0
  | n + 1 => total f n + f n

theorem upper_telescope (u f : Nat → Nat) (n : Nat) :
    (∀ i < n, 2 * f i + u (i+1) ≤ 1 + u i) →
    2 * total f n + u n ≤ n + u 0 := by
  induction n with
  | zero => intro h; simp [total]
  | succ n ih =>
      intro h
      have hprev := ih (fun i hi => h i (by omega))
      have hlast := h n (by omega)
      simp only [total]
      omega

theorem periodic_overflow_budget (u f : Nat → Nat) (n : Nat)
    (hstep : ∀ i < n, 2 * f i + u (i+1) ≤ 1 + u i)
    (hreturn : u n = u 0) : 2 * total f n ≤ n := by
  have h := upper_telescope u f n hstep
  omega

/-- The six-cycle phases are units modulo nine. -/
def SixPhase (c : Nat) : Prop := c = 2 ∨ c = 4 ∨ c = 8 ∨ c = 16 ∨ c = 14 ∨ c = 10

theorem six_phase_cancel (c g h : Nat) (hc : SixPhase c)
    (hz : (c*g + (18-c)*h) % 9 = 0) : g % 9 = h % 9 := by
  rcases hc with hc | hc | hc | hc | hc | hc <;> subst c <;> omega

theorem returned_mass_balance (c g h m : Nat) (hc : SixPhase c)
    (hm : (m + c*g + (18-c)*h) % 9 = m % 9) : g % 9 = h % 9 := by
  rcases hc with hc | hc | hc | hc | hc | hc <;> subst c <;> omega

theorem small_balanced_gains_equal (g h : Nat)
    (hbalance : g % 9 = h % 9) (hsmall : g+h < 9) : g = h := by omega

/-- All premises are necessary cycle arithmetic, not a supplied quotient cycle. -/
theorem qualifying_six_phase_period_at_least_twelve (period overflows g h : Nat)
    (hperiod : 0 < period) (hsix : period % 6 = 0)
    (hwidth : overflows = 2*(g+h)) (hpositive : 0 < overflows)
    (hbudget : 2*overflows ≤ period) (hbalance : g % 9 = h % 9) :
    12 ≤ period := by
  omega

theorem positive_cycle_period_at_least_four (period overflows g h : Nat)
    (hwidth : overflows = 2*(g+h)) (hpositive : 0 < overflows)
    (hbudget : 2*overflows ≤ period) : 4 ≤ period := by omega

theorem small_cycle_overflows_multiple_four (overflows g h : Nat)
    (hwidth : overflows = 2*(g+h)) (hsmall : g+h < 9)
    (hbalance : g % 9 = h % 9) : overflows = 4*g := by
  have heq := small_balanced_gains_equal g h hbalance hsmall
  omega

end P196.Agent4

#print axioms P196.Agent4.normalizedMass_mod_nine
#print axioms P196.Agent4.outer_upper_step
#print axioms P196.Agent4.upper_telescope
#print axioms P196.Agent4.periodic_overflow_budget
#print axioms P196.Agent4.six_phase_cancel
#print axioms P196.Agent4.returned_mass_balance
#print axioms P196.Agent4.small_balanced_gains_equal
#print axioms P196.Agent4.qualifying_six_phase_period_at_least_twelve
#print axioms P196.Agent4.positive_cycle_period_at_least_four
#print axioms P196.Agent4.small_cycle_overflows_multiple_four
