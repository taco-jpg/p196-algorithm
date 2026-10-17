import Agent1PeriodicZeroPeriod

/-!
Finite list/index compatibility for the original ordinary decimal update.
The zero-period quotient wrapper preserves the complete canonical realization,
including every finite column sum, rather than only the successor width.
-/

namespace Agent1.Periodic

open Agent8 Agent1.RepeatedBlock

theorem fixedDigits_getD_outputIn (W : Word) (e i : Nat) (hi : i < W.length) :
    ((fixedDigits W e)[i]?).getD 0 =
      IncomingCarry.outputIn (fun j => (W[j]?).getD 0) e i := by
  induction W generalizing e i with
  | nil => simp at hi
  | cons x xs ih =>
    cases i with
    | zero => rfl
    | succ i =>
      have hi' : i < xs.length := by simpa using hi
      rw [show i+1 = 1+i by omega, IncomingCarry.outputIn]
      rw [IncomingCarry.carryIn_add]
      simpa [fixedDigits, IncomingCarry.carryIn, IncomingCarry.outputIn,
        Nat.add_comm] using ih ((x+e)/10) i hi'

theorem normalize_length_nextWidth (W : Word) :
    (normalize W 0).length =
      FoldedDecimal.nextWidth (fun i => (W[i]?).getD 0) W.length := by
  rw [normalize_decompose, List.length_append, fixedDigits_length,
    terminalCarry_eq_carryIn, IncomingCarry.carryIn_zero_eq_carry]
  unfold FoldedDecimal.nextWidth
  split <;> simp_all

theorem normalize_getD_output (W : Word) (i : Nat) (hi : i < W.length) :
    ((normalize W 0)[i]?).getD 0 =
      DecimalDigits.output (fun j => (W[j]?).getD 0) i := by
  rw [normalize_decompose, List.getElem?_append_left]
  · rw [fixedDigits_getD_outputIn W 0 i hi,
      IncomingCarry.outputIn_zero_eq_output]
  · simpa only [fixedDigits_length] using hi

theorem normalize_getD_extended (W : Word)
    (hc : DecimalDigits.carry (fun j => (W[j]?).getD 0) W.length ≠ 0)
    (i : Nat) (hi : i < W.length+1) :
    ((normalize W 0)[i]?).getD 0 =
      DecimalDigits.extended (fun j => (W[j]?).getD 0) W.length i := by
  by_cases hlt : i < W.length
  · simp only [DecimalDigits.extended, if_pos hlt]
    exact normalize_getD_output W i hlt
  · have heq : i = W.length := by omega
    subst i
    rw [normalize_decompose, terminalCarry_eq_carryIn,
      IncomingCarry.carryIn_zero_eq_carry, if_neg hc]
    simp [List.getElem?_append_right, fixedDigits_length, DecimalDigits.extended]

theorem zipAdd_getD (A B : Word) (hlen : A.length = B.length) (i : Nat) :
    ((zipAdd A B)[i]?).getD 0 = (A[i]?).getD 0 + (B[i]?).getD 0 := by
  induction A generalizing B i with
  | nil => cases B <;> simp_all [zipAdd]
  | cons x xs ih =>
    cases B with
    | nil => simp at hlen
    | cons y ys =>
      cases i with
      | zero => rfl
      | succ i => exact ih ys (by simpa using hlen) i

theorem pair_getD_columnSum (W : Word) (i : Nat) (hi : i < W.length) :
    ((pair W)[i]?).getD 0 =
      DecimalDigits.columnSum (fun j => (W[j]?).getD 0) W.length i := by
  simp only [pair, zipAdd_getD W W.reverse (by simp), List.getElem?_reverse hi,
    DecimalDigits.columnSum, DecimalDigits.reflected]

theorem stepWord_length_nextWidth (W : Word) :
    (stepWord W).length =
      FoldedDecimal.nextWidth (fun i => (W[i]?).getD 0) W.length := by
  rw [stepWord, pair_length, normalize_length_nextWidth]

theorem stepWord_getD_nextColumns (W : Word) (i : Nat)
    (hi : i < (stepWord W).length) :
    ((stepWord W)[i]?).getD 0 =
      FoldedDecimal.nextColumns (fun j => (W[j]?).getD 0) W.length i := by
  have hn : i < (normalize W 0).length := by
    simpa only [stepWord, pair_length] using hi
  rw [stepWord, pair_getD_columnSum _ i hn]
  by_cases hc : DecimalDigits.carry (fun j => (W[j]?).getD 0) W.length = 0
  · have hl : (normalize W 0).length = W.length := by
      rw [normalize_length_nextWidth, FoldedDecimal.nextWidth, if_pos hc]
    rw [hl, FoldedDecimal.nextColumns, if_pos hc]
    simp only [DecimalDigits.columnSum, DecimalDigits.reflected]
    rw [normalize_getD_output W i (by omega),
      normalize_getD_output W (W.length-1-i) (by omega)]
  · have hl : (normalize W 0).length = W.length+1 := by
      rw [normalize_length_nextWidth, FoldedDecimal.nextWidth, if_neg hc]
    rw [hl, FoldedDecimal.nextColumns, if_neg hc]
    simp only [DecimalDigits.columnSum, DecimalDigits.reflected]
    rw [normalize_getD_extended W hc i (by omega),
      normalize_getD_extended W hc (W.length+1-1-i) (by omega)]

theorem actual_step_representation (n : Nat) (d : Nat → Nat) (W : Word)
    (hcan : DecimalDigits.Canonical n d W.length)
    (hrep : ∀ i, i < W.length →
      DecimalDigits.columnSum d W.length i = (W[i]?).getD 0) :
    ∃ d', DecimalDigits.Canonical (Lychrel196.step n) d' (stepWord W).length ∧
      ∀ i, i < (stepWord W).length →
        DecimalDigits.columnSum d' (stepWord W).length i =
          ((stepWord W)[i]?).getD 0 := by
  obtain ⟨d', hc, hr⟩ := FoldedDecimal.representation_next n d
    (fun i => (W[i]?).getD 0) W.length hcan hrep
  rw [← stepWord_length_nextWidth W] at hc hr
  refine ⟨d', hc, ?_⟩
  intro i hi
  exact (hr i hi).trans (stepWord_getD_nextColumns W i hi).symm

theorem zero_quotient_actual_step (B H : Word) (k n : Nat) (d : Nat → Nat)
    (hB : Bounded B 18) (hH : Bounded H 18) (hk : 3 ≤ k)
    (hcan : DecimalDigits.Canonical n d (periodicWord B H [0,0,0,0] k).length)
    (hrep : ∀ i, i < (periodicWord B H [0,0,0,0] k).length →
      DecimalDigits.columnSum d (periodicWord B H [0,0,0,0] k).length i =
        ((periodicWord B H [0,0,0,0] k)[i]?).getD 0) :
    let Q' := periodicWord (quotientOuter B H [0,0,0,0])
      (quotientCenter B H [0,0,0,0]) [0,0,0,0]
      ((k-2)+outerPeriods B H [0,0,0,0]+centerPeriods B H [0,0,0,0])
    ∃ d', DecimalDigits.Canonical (Lychrel196.step n) d' Q'.length ∧
      ∀ i, i < Q'.length → DecimalDigits.columnSum d' Q'.length i = (Q'[i]?).getD 0 := by
  have hz : Bounded [0,0,0,0] 18 := by
    intro x hx
    simp only [List.mem_cons, List.not_mem_nil, or_false, or_self] at hx
    subst x
    decide
  have hs := quotient_step_bounded B H [0,0,0,0] k hB hH hz rfl hk
  rw [rawPeriod_zero B H hB hH] at hs
  have h := actual_step_representation n d (periodicWord B H [0,0,0,0] k) hcan hrep
  rw [hs] at h
  exact h

end Agent1.Periodic

#print axioms Agent1.Periodic.fixedDigits_getD_outputIn
#print axioms Agent1.Periodic.normalize_length_nextWidth
#print axioms Agent1.Periodic.normalize_getD_output
#print axioms Agent1.Periodic.normalize_getD_extended
#print axioms Agent1.Periodic.zipAdd_getD
#print axioms Agent1.Periodic.pair_getD_columnSum
#print axioms Agent1.Periodic.stepWord_length_nextWidth
#print axioms Agent1.Periodic.stepWord_getD_nextColumns
#print axioms Agent1.Periodic.actual_step_representation
#print axioms Agent1.Periodic.zero_quotient_actual_step
