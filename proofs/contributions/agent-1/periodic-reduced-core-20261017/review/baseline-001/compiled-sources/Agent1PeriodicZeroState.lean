import Agent1PeriodicZeroPeriod

/-!
Finite-state consequences of an exact return under the original maximal
quotient with literal period [0,0,0,0]. No cycle is asserted to exist, and
no integer seed or numeric orbit is introduced here.
-/

namespace Agent1.Periodic

open Agent8 Agent1.RepeatedBlock

abbrev ZeroState := Word × Word

/-- The exact exterior/center quotient with the period fixed to four zeros. -/
def zeroNext (s : ZeroState) : ZeroState :=
  (quotientOuter s.1 s.2 [0,0,0,0], quotientCenter s.1 s.2 [0,0,0,0])

/-- Iteration of the literal zero-period quotient state. -/
def zeroStateOrbit (s : ZeroState) : Nat → ZeroState
  | 0 => s
  | t + 1 => zeroNext (zeroStateOrbit s t)

/-- Splitting the number of actual quotient transitions. -/
theorem zeroStateOrbit_add (s : ZeroState) (m n : Nat) :
    zeroStateOrbit s (m + n) = zeroStateOrbit (zeroStateOrbit s m) n := by
  induction n with
  | zero => rfl
  | succ n ih =>
    simpa only [Nat.add_succ, zeroStateOrbit] using congrArg zeroNext ih

/-- Full original validity propagates through every literal quotient step. -/
theorem zeroStateOrbit_valid (s : ZeroState)
    (hv : ValidPeriodic s.1 s.2 [0,0,0,0]) (t : Nat) :
    ValidPeriodic (zeroStateOrbit s t).1 (zeroStateOrbit s t).2 [0,0,0,0] := by
  induction t with
  | zero => exact hv
  | succ t ih =>
    simpa only [zeroStateOrbit, zeroNext] using
      zero_quotient_valid (zeroStateOrbit s t).1 (zeroStateOrbit s t).2 ih

/-- A positive exact return reduces every orbit state to the finite prefix. -/
theorem zeroStateOrbit_cycle_reduce (s : ZeroState) (P : Nat)
    (hP : 0 < P) (hcycle : zeroStateOrbit s P = s) (t : Nat) :
    ∃ j, j < P ∧ zeroStateOrbit s t = zeroStateOrbit s j := by
  induction t using Nat.strongRecOn with
  | ind t ih =>
    by_cases ht : t < P
    · exact ⟨t, ht, rfl⟩
    · have hlt : t - P < t := by omega
      obtain ⟨j, hj, heq⟩ := ih (t - P) hlt
      refine ⟨j, hj, ?_⟩
      have hsplit : t = P + (t - P) := by omega
      calc
        zeroStateOrbit s t = zeroStateOrbit s (P + (t - P)) := by rw [← hsplit]
        _ = zeroStateOrbit (zeroStateOrbit s P) (t - P) := zeroStateOrbit_add s P (t - P)
        _ = zeroStateOrbit s (t - P) := by rw [hcycle]
        _ = zeroStateOrbit s j := heq

/-- A nonnegative quantity dominating both finite interface size and mass. -/
def zeroStateMeasure (s : ZeroState) : Nat :=
  (2 * s.1.length + s.2.length) + (2 * s.1.sum + s.2.sum)

/-- An explicit finite sum over the first P states, including time zero. -/
def zeroStatePrefixBound (s : ZeroState) : Nat → Nat
  | 0 => 0
  | P + 1 => zeroStatePrefixBound s P + zeroStateMeasure (zeroStateOrbit s P)

theorem zeroStateMeasure_le_prefix (s : ZeroState) (P j : Nat) (hj : j < P) :
    zeroStateMeasure (zeroStateOrbit s j) ≤ zeroStatePrefixBound s P := by
  induction P with
  | zero => omega
  | succ P ih =>
    by_cases hlt : j < P
    · have h := ih hlt
      simp only [zeroStatePrefixBound]
      omega
    · have heq : j = P := by omega
      subst j
      simp only [zeroStatePrefixBound]
      omega

/-- Any positive exact quotient cycle has uniformly bounded interface size
and mass. Validity is not needed for this finite-orbit implication. -/
theorem zeroStateOrbit_cycle_bounded (s : ZeroState) (P : Nat)
    (hP : 0 < P) (hcycle : zeroStateOrbit s P = s) :
    ∃ M, ∀ t,
      2 * (zeroStateOrbit s t).1.length + (zeroStateOrbit s t).2.length ≤ M ∧
      2 * (zeroStateOrbit s t).1.sum + (zeroStateOrbit s t).2.sum ≤ M := by
  refine ⟨zeroStatePrefixBound s P, ?_⟩
  intro t
  obtain ⟨j, hj, heq⟩ := zeroStateOrbit_cycle_reduce s P hP hcycle t
  have h := zeroStateMeasure_le_prefix s P j hj
  rw [← heq] at h
  unfold zeroStateMeasure at h
  constructor <;> omega

end Agent1.Periodic

#print axioms Agent1.Periodic.zeroStateOrbit_add
#print axioms Agent1.Periodic.zeroStateOrbit_valid
#print axioms Agent1.Periodic.zeroStateOrbit_cycle_reduce
#print axioms Agent1.Periodic.zeroStateMeasure_le_prefix
#print axioms Agent1.Periodic.zeroStateOrbit_cycle_bounded
