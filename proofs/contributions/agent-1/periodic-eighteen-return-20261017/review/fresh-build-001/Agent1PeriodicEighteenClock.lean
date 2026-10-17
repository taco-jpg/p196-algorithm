import Agent1PeriodicWidthPath

/-!
The indexed decimal carry of a positive-exponent periodic word is the actual
raw quotient clock. This is a transport of the existing stable list-carry
theorem through the existing list/index carry identity, not a new carry law.
It needs only coefficient bounds and a positive exponent; original validity
and the usual exponent-three guard imply these hypotheses.

The finite recursion adapters retain every used source guard and include
zero-length paths. They assert no return, safety, or population theorem.
-/

namespace Agent1.Periodic

open Agent8 Agent1.RepeatedBlock

/-- The original indexed terminal carry equals the quotient's actual raw
clock for every positive exponent, with no chosen abstract clock bit. -/
theorem periodicWord_carry_eq_rawGamma (B H w : Word) (k : Nat)
    (hB : Bounded B 18) (hH : Bounded H 18) (hw : Bounded w 18)
    (hk : 0 < k) :
    DecimalDigits.carry (fun j => ((periodicWord B H w k)[j]?).getD 0)
      (periodicWord B H w k).length = rawGamma B H w := by
  have hscan := scan_carry_stable B H w (k-1) hB hH hw
  rw [show k-1+1 = k by omega] at hscan
  rw [terminalCarry_eq_carryIn, IncomingCarry.carryIn_zero_eq_carry] at hscan
  exact hscan

/-- The already defined raw-clock sum obeys the literal indexed-carry
recurrence on each guarded source of the supplied full quotient path. -/
theorem quotient_path_actual_carry_step (B H w : Nat → Word)
    (k : Nat → Nat) (N : Nat) (hp : QuotientPath B H w N)
    (i : Nat) (hi : i < N) (hk : 0 < k i) :
    quotientClockSum B H w (i+1) = quotientClockSum B H w i +
      DecimalDigits.carry
        (fun j => ((periodicWord (B i) (H i) (w i) (k i))[j]?).getD 0)
        (periodicWord (B i) (H i) (w i) (k i)).length := by
  obtain ⟨hB, hH, hw, _, _, _, _⟩ := hp i hi
  rw [periodicWord_carry_eq_rawGamma (B i) (H i) (w i) (k i) hB hH hw hk]
  rfl

/-- Any literal finite cumulative indexed-carry sequence agrees with the
existing quotientClockSum on the complete used prefix, including N=0. -/
theorem quotient_path_actual_carry_sum (B H w : Nat → Word)
    (k C : Nat → Nat) (N : Nat) (hp : QuotientPath B H w N)
    (hguard : ∀ i, i < N → 0 < k i) (hzero : C 0 = 0)
    (hstep : ∀ i, i < N → C (i+1) = C i +
      DecimalDigits.carry
        (fun j => ((periodicWord (B i) (H i) (w i) (k i))[j]?).getD 0)
        (periodicWord (B i) (H i) (w i) (k i)).length) :
    ∀ t, t ≤ N → C t = quotientClockSum B H w t := by
  intro t
  induction t with
  | zero => intro _; exact hzero
  | succ t ih =>
      intro ht
      rw [hstep t (by omega), ih (by omega),
        quotient_path_actual_carry_step B H w k N hp t (by omega)
          (hguard t (by omega))]

end Agent1.Periodic

#print axioms Agent1.Periodic.periodicWord_carry_eq_rawGamma
#print axioms Agent1.Periodic.quotient_path_actual_carry_step
#print axioms Agent1.Periodic.quotient_path_actual_carry_sum
