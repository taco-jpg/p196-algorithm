import P196.CrossWidthCollisionPaths.Recovery
import P196.CrossWidthCollisionPaths.Actual

/-!
# Exact realization of finite collision traces

The reflected closed paths with the two center conditions are precisely
the finite traces of ordinary collisions at the specified adjacent widths.
Their common output determines the path on its active interval. Values of
the path function outside that interval, and the digit splits realizing
the two coefficient words, are not asserted to be unique.
-/

set_option autoImplicit false

namespace CrossWidthCollisionPaths

open DecimalDigits FoldedDecimal Lychrel196 CrossWidthCollisionStates

/-- The common positional value specified by the shorter reconstructed word. -/
def pathValue (L : Nat) (f : Nat → State) : Nat := value (shortWord f) L

private theorem stateAt_congr
    {q r q' r' : Nat → Nat} {L i : Nat}
    (hq : ∀ j, j < L → q j = q' j)
    (hr : ∀ j, j < L + 1 → r j = r' j)
    (hi : 1 ≤ i) (hiL : i ≤ L) :
    stateAt q r L i = stateAt q' r' L i := by
  have hx := hq (i - 1) (by omega)
  have hqu := carry_congr_upto q q' L hq i hiL
  have hru := carry_congr_upto r r' (L + 1) hr i (by omega)
  have hqv := carry_congr_upto q q' L hq (L - i + 1) (by omega)
  have hrv := carry_congr_upto r r' (L + 1) hr (L - i + 1) (by omega)
  simp only [stateAt, hx, hqu, hru, hqv, hrv]

private theorem realized_of_valid {L : Nat} {f : Nat → State}
    (h : Valid L f) :
    ∃ (n m : Nat) (d e : Nat → Nat),
      Canonical n d L ∧ Canonical m e (L + 1) ∧
      step n = step m ∧
      ∀ i, 1 ≤ i → i ≤ L →
        stateAt (columnSum d L) (columnSum e (L + 1)) L i = f i := by
  obtain ⟨hq, hr⟩ := valid_words h
  obtain ⟨n, d, _, hn, hqn⟩ := valid_word_realizable (shortWord f) L
    hq.1 hq.2.1 hq.2.2.1 hq.2.2.2.1 hq.2.2.2.2
  obtain ⟨m, e, _, hm, hrm⟩ := valid_word_realizable (longWord L f) (L + 1)
    hr.1 hr.2.1 hr.2.2.1 hr.2.2.2.1 hr.2.2.2.2
  have hnvalue := step_eq_word_value n d (shortWord f) L hn hqn
  have hmvalue := step_eq_word_value m e (longWord L f) (L + 1) hm hrm
  have hstep : step n = step m :=
    hnvalue.trans ((closed_values_equal h.toClosed).trans hmvalue.symm)
  refine ⟨n, m, d, e, hn, hm, hstep, ?_⟩
  intro i hi hiL
  exact (stateAt_congr hqn hrm hi hiL).trans
    (closed_trace_recovered h.toClosed i hi hiL)

/-- Exactly the center-admissible reflected closed paths arise from
canonical ordinary sources at the specified adjacent widths. Equality
with the supplied path is required only on its full finite trace. -/
theorem valid_iff_realized (L : Nat) (f : Nat → State) :
    Valid L f ↔
      ∃ (n m : Nat) (d e : Nat → Nat),
        Canonical n d L ∧ Canonical m e (L + 1) ∧
        step n = step m ∧
        ∀ i, 1 ≤ i → i ≤ L →
          stateAt (columnSum d L) (columnSum e (L + 1)) L i = f i := by
  constructor
  · exact realized_of_valid
  · rintro ⟨n, m, d, e, hn, hm, hstep, hf⟩
    exact actual_trace_valid hn hm hstep hf

/-- The reconstructed positional value is the actual common ordinary
output whenever the finite trace is supplied by canonical sources. -/
theorem pathValue_eq_step
    {n m L : Nat} {d e : Nat → Nat} {f : Nat → State}
    (hn : Canonical n d L) (hm : Canonical m e (L + 1))
    (hstep : step n = step m)
    (hf : ∀ i, 1 ≤ i → i ≤ L →
      stateAt (columnSum d L) (columnSum e (L + 1)) L i = f i) :
    pathValue L f = step n := by
  change value (shortWord f) L = step n
  exact (step_eq_word_value n d (shortWord f) L hn
    (actual_trace_words hn hm hstep hf).1).symm

/-- At a fixed source width, equal common outputs are equivalent to
equality of the entire finite trace. The path functions may differ
outside their active interval, and source digit splits may differ. -/
theorem pathValue_eq_iff
    {L : Nat} {f g : Nat → State}
    (hf : Valid L f) (hg : Valid L g) :
    pathValue L f = pathValue L g ↔
      ∀ i, 1 ≤ i → i ≤ L → f i = g i := by
  constructor
  · intro heq
    obtain ⟨hqf, hrf⟩ := valid_words hf
    obtain ⟨hqg, hrg⟩ := valid_words hg
    have hqvalue : value (shortWord f) L = value (shortWord g) L := heq
    have hq := ReverseAddInverse.symmetric_value_injective
      (shortWord f) (shortWord g) L hqf.2.2.1 hqg.2.2.1
      hqf.2.2.2.1 hqg.2.2.2.1 hqvalue
    have hrvalue : value (longWord L f) (L + 1) =
        value (longWord L g) (L + 1) :=
      (closed_values_equal hf.toClosed).symm.trans
        (hqvalue.trans (closed_values_equal hg.toClosed))
    have hr := ReverseAddInverse.symmetric_value_injective
      (longWord L f) (longWord L g) (L + 1) hrf.2.2.1 hrg.2.2.1
      hrf.2.2.2.1 hrg.2.2.2.1 hrvalue
    intro i hi hiL
    exact (closed_trace_recovered hf.toClosed i hi hiL).symm.trans
      ((stateAt_congr hq hr hi hiL).trans
        (closed_trace_recovered hg.toClosed i hi hiL))
  · intro hfg
    apply value_congr
    intro i hi
    exact congrArg State.x (hfg (i + 1) (by omega) (by omega))

end CrossWidthCollisionPaths

#print axioms CrossWidthCollisionPaths.pathValue
#print axioms CrossWidthCollisionPaths.valid_iff_realized
#print axioms CrossWidthCollisionPaths.pathValue_eq_step
#print axioms CrossWidthCollisionPaths.pathValue_eq_iff
