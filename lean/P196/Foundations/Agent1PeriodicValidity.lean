import P196.Foundations.Agent1PeriodicParity
import P196.Foundations.Agent1PeriodicPositivity

/-!
Preservation of the unchanged period-four validity predicate by the literal
raw and maximally stripped one-step constructions. The predecessor need not
be safe; no safety, future exponent threshold, or return cycle is asserted.
-/

namespace Agent1.Periodic

open Agent8 Agent1.RepeatedBlock

/-- The three literal slices of the actual exponent-three image satisfy
every field of the original validity predicate. -/
theorem raw_valid (B H w : Word) (hv : ValidPeriodic B H w) :
    ValidPeriodic (rawOuter B H w) (rawCenter B H w) (rawPeriod B H w) := by
  obtain ⟨hB, hw, hH⟩ := raw_blocks_bounded B H w
    hv.outer_bounded hv.center_bounded hv.period_bounded
  refine ⟨hB, hH, hw,
    (raw_block_lengths B H w hv.outer_bounded hv.center_bounded
      hv.period_bounded hv.period_length).2.1,
    raw_center_symmetric B H w hv.outer_bounded hv.center_bounded
      hv.period_bounded hv.period_length,
    raw_center_even B H w hv.outer_bounded hv.center_bounded
      hv.period_bounded hv.period_length, ?_⟩
  have hp := raw_outer_positive B H w hv
  cases he : rawOuter B H w with
  | nil => simp only [he, List.headD_nil] at hp; omega
  | cons a as => simpa only [he, List.cons_append, List.headD_cons] using hp

/-- Complete-period stripping preserves validity even when either remainder
is empty. Positivity is about exterior followed by period, as originally. -/
theorem strip_valid (B H w : Word) (hv : ValidPeriodic B H w) :
    ValidPeriodic (stripPeriodSuffix w B).1 (stripPeriodCenter w H).1 w := by
  have hw : w ≠ [] := by
    intro he
    have := hv.period_length
    simp only [he, List.length_nil] at this
    omega
  refine ⟨stripPeriodSuffix_bounded w B 18 hw hv.outer_bounded,
    stripPeriodCenter_bounded w H 18 hv.center_bounded,
    hv.period_bounded, hv.period_length,
    stripPeriodCenter_symmetric w H hv.center_symmetric,
    stripPeriodCenter_even w H hv.center_even, ?_⟩
  rw [stripPeriodSuffix_outside w B hw]
  exact hv.outside_positive

/-- The original Python valid(target) assertion, for its exact executable
quotient and every valid input, without a safety premise. -/
theorem quotient_valid (B H w : Word) (hv : ValidPeriodic B H w) :
    ValidPeriodic (quotientOuter B H w) (quotientCenter B H w) (rawPeriod B H w) :=
  strip_valid _ _ _ (raw_valid B H w hv)

/-- One exact transition produces a valid state and a positive exponent.
Positivity of that exponent is deliberately distinct from a new threshold3. -/
theorem valid_quotient_transition (B H w : Word) (k : Nat)
    (hv : ValidPeriodic B H w) (hk : 3 ≤ k) :
    ValidPeriodic (quotientOuter B H w) (quotientCenter B H w) (rawPeriod B H w) ∧
      1 ≤ (k-2)+outerPeriods B H w+centerPeriods B H w ∧
      stepWord (periodicWord B H w k) =
        periodicWord (quotientOuter B H w) (quotientCenter B H w)
          (rawPeriod B H w) ((k-2)+outerPeriods B H w+centerPeriods B H w) :=
  ⟨quotient_valid B H w hv, (quotient_exponent_accounting B H w k hk).1,
    quotient_step_bounded B H w k hv.outer_bounded hv.center_bounded
      hv.period_bounded hv.period_length hk⟩

end Agent1.Periodic

#print axioms Agent1.Periodic.raw_valid
#print axioms Agent1.Periodic.strip_valid
#print axioms Agent1.Periodic.quotient_valid
#print axioms Agent1.Periodic.valid_quotient_transition
