import P196.Foundations.Agent1PeriodicSafetyAlphabet

/-!
The physical outside coefficient of the exact period-four quotient.
The appended period supplies the head when a stored exterior is empty.
All decimal outer arithmetic comes from the original canonical-step theorem;
the carry is the actual one entering the final exponent-three column.
-/

namespace Agent1.Periodic
open Agent8

/-- Physical outside coefficient, including an empty stored exterior. -/
def outside (B w : Word) : Nat := (B ++ w).headD 0

private theorem valid_period_nonempty (B H w : Word)
    (hv : ValidPeriodic B H w) : w ≠ [] := by
  intro he
  have hlen := hv.period_length
  simp only [he, List.length_nil] at hlen
  omega

/-- Original validity places the physical outside coefficient in 1..18. -/
theorem outside_bounds (B H w : Word) (hv : ValidPeriodic B H w) :
    0 < outside B w ∧ outside B w ≤ 18 := by
  have hh := canonical_head_bounds (periodicWord B H w 3)
    (periodicWord_canonical B H w 3 hv (by omega))
  rw [periodicWord_head B H w 3 (by omega) (valid_period_nonempty B H w hv)] at hh
  exact hh

private theorem rawOuter_head (B H w : Word) :
    (rawOuter B H w).headD 0 = (stepWord (periodicWord B H w 3)).headD 0 := by
  unfold rawOuter
  cases stepWord (periodicWord B H w 3) <;> rfl

private theorem quotient_outside_eq_rawHead (B H w : Word)
    (hv : ValidPeriodic B H w) :
    outside (quotientOuter B H w) (rawPeriod B H w) = (rawOuter B H w).headD 0 := by
  have hl := raw_block_lengths B H w hv.outer_bounded hv.center_bounded
    hv.period_bounded hv.period_length
  have hw : rawPeriod B H w ≠ [] := by
    intro he
    have hp := hl.2.1
    simp only [he, List.length_nil] at hp
    omega
  unfold outside quotientOuter
  rw [stripPeriodSuffix_outside (rawPeriod B H w) (rawOuter B H w) hw]
  cases he : rawOuter B H w with
  | nil =>
    have hp := hl.1
    simp only [he, List.length_nil] at hp
    omega
  | cons a R => rfl

/-- Exact outer-head and clock projection through the maximal quotient.
The inner bit is the actual carry entering the last column of Q_3.
No boundary bit or clock is chosen freely, even when stripping empties B. -/
theorem quotient_outside_step (B H w : Word) (hv : ValidPeriodic B H w) :
    let e := lastInput (periodicWord B H w 3)
    e ≤ 1 ∧ rawGamma B H w = overflow (outside B w) e ∧
      outside (quotientOuter B H w) (rawPeriod B H w) =
        nextExterior (outside B w) e := by
  dsimp only
  have hcan := periodicWord_canonical B H w 3 hv (by omega)
  have hstep := canonical_step (periodicWord B H w 3) hcan
  have hhead : (periodicWord B H w 3).headD 0 = outside B w :=
    periodicWord_head B H w 3 (by omega) (valid_period_nonempty B H w hv)
  refine ⟨hstep.2.2.2, ?_, ?_⟩
  · exact (terminalCarry_eq_actual_overflow (periodicWord B H w 3) hcan).trans
      (congrArg (fun p => overflow p (lastInput (periodicWord B H w 3))) hhead)
  · rw [quotient_outside_eq_rawHead B H w hv, rawOuter_head B H w,
      hstep.2.1, hhead]

end Agent1.Periodic

#print axioms Agent1.Periodic.outside
#print axioms Agent1.Periodic.outside_bounds
#print axioms Agent1.Periodic.quotient_outside_step
