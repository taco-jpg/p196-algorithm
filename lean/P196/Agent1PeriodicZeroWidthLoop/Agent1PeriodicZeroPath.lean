import P196.Foundations.Agent1PeriodicWidthPath
import P196.Agent1PeriodicZeroCycle.Agent1PeriodicZeroCycle

/-!
The original finite exact quotient path, when its initial period is four
zeros, agrees with the existing literal zero-state iteration through its
endpoint. The established no-cycle theorem then excludes a positive complete
state return under original initial validity. No abstract catalog edge or
zero-phase graph cycle is removed, and no safety or exponent guard is added.
-/
namespace Agent1.Periodic
open Agent8

/-- Every state of a finite zero-period exact quotient path is the existing
zero-state iterate, including both endpoints. Only the path's own coefficient
bounds are used; this identification does not need initial full validity. -/
theorem quotient_path_zeroStateOrbit (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N) (hzero : w 0 = [0,0,0,0]) :
    ∀ i, i ≤ N → w i = [0,0,0,0] ∧
      (B i, H i) = zeroStateOrbit (B 0, H 0) i := by
  intro i hi
  induction i with
  | zero => exact ⟨hzero, rfl⟩
  | succ i ih =>
      obtain ⟨hw, hs⟩ := ih (by omega)
      obtain ⟨hB, hH, _, _, hnextB, hnextH, hnextw⟩ := hp i (by omega)
      constructor
      · rw [hnextw, hw]
        exact rawPeriod_zero (B i) (H i) hB hH
      · calc
          (B (i+1), H (i+1)) = zeroNext (B i, H i) := by
            simp only [zeroNext, hnextB, hnextH, hw]
          _ = zeroNext (zeroStateOrbit (B 0, H 0) i) := congrArg zeroNext hs
          _ = zeroStateOrbit (B 0, H 0) (i+1) := rfl

/-- A positive zero-period exact path from original valid data cannot return
even its exterior/center pair. This reuses the established no-cycle result. -/
theorem quotient_path_zero_interface_ne (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N)
    (hv : ValidPeriodic (B 0) (H 0) (w 0))
    (hzero : w 0 = [0,0,0,0]) (hN : 0 < N) :
    (B N, H N) ≠ (B 0, H 0) := by
  have hvzero : ValidPeriodic (B 0) (H 0) [0,0,0,0] := by
    simpa only [hzero] using hv
  have hs := (quotient_path_zeroStateOrbit B H w N hp hzero N (Nat.le_refl N)).2
  intro hreturn
  exact zeroStateOrbit_no_cycle (B 0, H 0) hvzero N hN (hs.symm.trans hreturn)

/-- No positive complete-tuple return is possible for the original exact
finite quotient path starting at a valid state with literal zero period. -/
theorem quotient_path_zero_no_return (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N)
    (hv : ValidPeriodic (B 0) (H 0) (w 0))
    (hzero : w 0 = [0,0,0,0]) (hN : 0 < N) :
    ¬ (B N = B 0 ∧ H N = H 0 ∧ w N = w 0) := by
  rintro ⟨hB, hH, _⟩
  apply quotient_path_zero_interface_ne B H w N hp hv hzero hN
  exact Prod.ext hB hH

end Agent1.Periodic

#print axioms Agent1.Periodic.quotient_path_zeroStateOrbit
#print axioms Agent1.Periodic.quotient_path_zero_interface_ne
#print axioms Agent1.Periodic.quotient_path_zero_no_return
