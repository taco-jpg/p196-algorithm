import P196.FiniteExteriorHistories.History

/-!
# Limits of recovery from finite exterior histories

The data is a chronological finite list. Each entry consists of the actual
outgoing high carry and the two original coordinate prefixes, using that
time's own phase, word length, and denominator.

The simultaneous all-phase history construction rules out pointwise phase
certificates and phase decoders from this data. Even when the initial phase
is supplied separately, it rules out a finite upper bound on canonical core
width. The spatial cutoff and time horizon are fixed in each statement.
-/

namespace Agent5.FiniteExteriorHistories

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams Agent6.ExteriorCoordinates

/-- One original exterior observation: actual high carry, low prefix, and
high prefix with its actual carry-dependent denominator. -/
def observation (cut : Nat) (s : Outer) : Nat × List Nat × List Nat :=
  ((normalize s.B.reverse (if 10 ≤ s.c then 1 else 0)).2,
    adicNumeratorDigits cut (zValue s.c s.B - (s.c : Int)),
    fractionDigits cut (rhoNum s.c s.B)
      (9 * 10 ^ s.B.length *
        10 ^ (normalize s.B.reverse (if 10 ≤ s.c then 1 else 0)).2))

/-- The chronological observations at exactly the times `0, ..., T`. -/
def observationHistory (cut T : Nat) (s : Outer) :
    List (Nat × List Nat × List Nat) :=
  (List.range (T + 1)).map (fun t => observation cut (outerIter t s))

/-- Equality of the finite data lists is exactly agreement of the original
carry and both original prefixes at every recorded time. -/
theorem observationHistory_eq_iff (cut T : Nat) (s q : Outer) :
    observationHistory cut T q = observationHistory cut T s ↔
      ∀ t, t ≤ T →
        sameObservation cut (outerIter t s) (outerIter t q) := by
  simp only [observationHistory, List.map_inj_left, List.mem_range,
    Nat.lt_succ_iff, observation, Prod.mk.injEq, sameObservation]

/-- At every valid target, a finite observation history cannot force the
initial phase of all compatible valid states at nonneutral phases. -/
theorem no_finite_history_phase_certificate (cut T : Nat) (s : Outer)
    (hc : nonneutralPhase s.c) (hv : validOuter s = true) :
    ¬ (∀ q : Outer,
      nonneutralPhase q.c →
      validOuter q = true →
      observationHistory cut T q = observationHistory cut T s →
      q.c = s.c) := by
  intro hcertificate
  rcases s with ⟨c, B⟩
  obtain ⟨A, _, hA⟩ :=
    arbitrarily_wide_all_phase_same_history c cut T 0 B hc hv
  have hc2 : nonneutralPhase 2 := by simp [nonneutralPhase]
  have hc4 : nonneutralPhase 4 := by simp [nonneutralPhase]
  obtain ⟨hv2, _, hhistory2⟩ := hA 2 hc2
  obtain ⟨hv4, _, hhistory4⟩ := hA 4 hc4
  have h2 : 2 = c := hcertificate { c := 2, B := A } hc2 hv2
    ((observationHistory_eq_iff cut T _ _).mpr hhistory2)
  have h4 : 4 = c := hcertificate { c := 4, B := A } hc4 hv4
    ((observationHistory_eq_iff cut T _ _).mpr hhistory4)
  omega

/-- Even when the initial phase is supplied, no finite history at a valid
target certifies a finite upper bound on compatible canonical core widths.
The competing states in this statement have exactly the target's phase. -/
theorem no_finite_history_core_width_certificate (cut T N : Nat) (s : Outer)
    (hc : nonneutralPhase s.c) (hv : validOuter s = true) :
    ¬ (∀ q : Outer,
      q.c = s.c →
      validOuter q = true →
      observationHistory cut T q = observationHistory cut T s →
      (stripSuffix q.c q.B).length ≤ N) := by
  intro hbound
  rcases s with ⟨c, B⟩
  obtain ⟨A, hwidth, hA⟩ :=
    arbitrarily_wide_all_phase_same_history c cut T N B hc hv
  obtain ⟨hvA, hcanonical, hhistory⟩ := hA c hc
  have hN := hbound { c := c, B := A } rfl hvA
    ((observationHistory_eq_iff cut T _ _).mpr hhistory)
  change (stripSuffix c A).length ≤ N at hN
  rw [hcanonical] at hN
  have hmax := Nat.le_max_right B.length N
  omega

/-- No function of the finite chronological observation list recovers the
initial phase of every nonneutral valid state. The decoder may be chosen
separately for each spatial cutoff and finite time horizon. -/
theorem no_finite_history_phase_decoder (cut T : Nat) :
    ¬ ∃ D : List (Nat × List Nat × List Nat) → Nat,
      ∀ s : Outer,
        nonneutralPhase s.c →
        validOuter s = true →
        D (observationHistory cut T s) = s.c := by
  rintro ⟨D, hD⟩
  have hc2 : nonneutralPhase 2 := by simp [nonneutralPhase]
  have hempty : validOuter { c := 2, B := [] } = true := by
    simp [validOuter]
  apply no_finite_history_phase_certificate cut T { c := 2, B := [] } hc2 hempty
  intro q hq hvq hhistory
  have hdecoded := hD q hq hvq
  rw [hhistory] at hdecoded
  have hzero := hD { c := 2, B := [] } hc2 hempty
  exact hdecoded.symm.trans hzero

#print axioms observationHistory_eq_iff
#print axioms no_finite_history_phase_certificate
#print axioms no_finite_history_core_width_certificate
#print axioms no_finite_history_phase_decoder

end Agent5.FiniteExteriorHistories
