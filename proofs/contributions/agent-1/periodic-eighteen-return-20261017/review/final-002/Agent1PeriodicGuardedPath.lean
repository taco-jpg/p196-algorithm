import Agent1PeriodicWidthPath
import Agent1PeriodicZeroNumeric
import Agent1PeriodicRealizability

/-!
Finite transport of a supplied full quotient path to one ordinary seed.
Original METHOD_AND_PROOF.md, section 4, line 164 already instructs choosing
the initial exponent so every visited source remains at least three. Here
the conservative finite choice 2*N+3 makes that guard explicit. The exact
word transition, ordinary one-step representation, and initial realization
are existing theorems and are reused unchanged.

The existential seed may depend on the finite horizon N. No uniform seed
for all horizons, arbitrary graph-path realization, safe orbit, or affirmative
finite-interface construction is asserted.
-/

namespace Agent1.Periodic
open Agent8

/-- The complete template at each supplied state and exponent. -/
def quotientPathWord (B H w : Nat → Word) (k : Nat → Nat) (i : Nat) : Word :=
  periodicWord (B i) (H i) (w i) (k i)

/-- Literal natural exponent update along the supplied full state sequence. -/
def quotientPathExponent (B H w : Nat → Word) (k0 : Nat) : Nat → Nat
  | 0 => k0
  | i+1 => (quotientPathExponent B H w k0 i - 2) +
      outerPeriods (B i) (H i) (w i) + centerPeriods (B i) (H i) (w i)

/-- Every used transition is the original complete word step. Only source
guards strictly before N are required; no endpoint guard is assumed. -/
theorem quotient_path_guarded_step (B H w : Nat → Word) (k : Nat → Nat)
    (N : Nat) (hp : QuotientPath B H w N)
    (hguard : ∀ i, i < N → 3 ≤ k i)
    (hkstep : ∀ i, i < N → k (i+1) = (k i-2) +
      outerPeriods (B i) (H i) (w i) + centerPeriods (B i) (H i) (w i))
    (i : Nat) (hi : i < N) :
    stepWord (quotientPathWord B H w k i) = quotientPathWord B H w k (i+1) := by
  obtain ⟨hB, hH, hw, hlen, hnextB, hnextH, hnextw⟩ := hp i hi
  have hs := quotient_step_bounded (B i) (H i) (w i) (k i)
    hB hH hw hlen (hguard i hi)
  simpa only [quotientPathWord, hnextB, hnextH, hnextw, hkstep i hi] using hs

/-- The same supplied ordinary seed realizes the entire guarded finite path,
including both endpoints and N=0, with exact changing canonical widths and
every in-range column sum. Positivity follows from original canonicality. -/
theorem quotient_path_actual_prefix (B H w : Nat → Word) (k : Nat → Nat)
    (N : Nat) (hp : QuotientPath B H w N)
    (hguard : ∀ i, i < N → 3 ≤ k i)
    (hkstep : ∀ i, i < N → k (i+1) = (k i-2) +
      outerPeriods (B i) (H i) (w i) + centerPeriods (B i) (H i) (w i))
    (n : Nat) (d : Nat → Nat)
    (hcan : DecimalDigits.Canonical n d (quotientPathWord B H w k 0).length)
    (hrep : ∀ j, j < (quotientPathWord B H w k 0).length →
      DecimalDigits.columnSum d (quotientPathWord B H w k 0).length j =
        ((quotientPathWord B H w k 0)[j]?).getD 0) :
    ∀ t, t ≤ N → 0 < Lychrel196.orbit n t ∧
      ∃ d', DecimalDigits.Canonical (Lychrel196.orbit n t) d'
          (quotientPathWord B H w k t).length ∧
        ∀ j, j < (quotientPathWord B H w k t).length →
          DecimalDigits.columnSum d' (quotientPathWord B H w k t).length j =
            ((quotientPathWord B H w k t)[j]?).getD 0 := by
  have hn : 0 < n := by
    rw [← hcan.2.2.2]
    exact DecimalDigits.value_positive d _ hcan.1 hcan.2.2.1
  have hreal : ∀ t, t ≤ N →
      ∃ d', DecimalDigits.Canonical (Lychrel196.orbit n t) d'
          (quotientPathWord B H w k t).length ∧
        ∀ j, j < (quotientPathWord B H w k t).length →
          DecimalDigits.columnSum d' (quotientPathWord B H w k t).length j =
            ((quotientPathWord B H w k t)[j]?).getD 0 := by
    intro t
    induction t with
    | zero => intro _; exact ⟨d, hcan, hrep⟩
    | succ t ih =>
      intro ht
      obtain ⟨d', hc', hr'⟩ := ih (by omega)
      obtain ⟨d'', hc'', hr''⟩ := actual_step_representation
        (Lychrel196.orbit n t) d' (quotientPathWord B H w k t) hc' hr'
      rw [quotient_path_guarded_step B H w k N hp hguard hkstep t (by omega)]
        at hc'' hr''
      exact ⟨d'', hc'', hr''⟩
  exact fun t ht => ⟨DecimalDigits.orbit_positive n hn t, hreal t ht⟩

/-- A conservative finite budget loses at most two copies per transition.
This arithmetic bound requires neither validity nor a quotient-path premise. -/
theorem quotientPathExponent_lower_bound (B H w : Nat → Word) (N : Nat) :
    ∀ i, i ≤ N → 2*(N-i)+3 ≤ quotientPathExponent B H w (2*N+3) i := by
  intro i
  induction i with
  | zero => intro _; simp [quotientPathExponent]
  | succ i ih =>
    intro hi
    have hprev := ih (by omega)
    simp only [quotientPathExponent]
    omega

/-- Every supplied finite exact quotient path from original-valid initial
data has one positive ordinary seed realizing all its states, at the literal
exponent schedule starting 2*N+3. The seed can depend on the path and N;
the theorem provides neither an infinite uniform seed nor a safe path. -/
theorem quotient_path_finite_realizable (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N) (hv : ValidPeriodic (B 0) (H 0) (w 0)) :
    let k := quotientPathExponent B H w (2*N+3)
    ∃ n, 0 < n ∧ ∀ t, t ≤ N →
      ∃ d, DecimalDigits.Canonical (Lychrel196.orbit n t) d
          (quotientPathWord B H w k t).length ∧
        ∀ j, j < (quotientPathWord B H w k t).length →
          DecimalDigits.columnSum d (quotientPathWord B H w k t).length j =
            ((quotientPathWord B H w k t)[j]?).getD 0 := by
  let k := quotientPathExponent B H w (2*N+3)
  have hguard : ∀ i, i < N → 3 ≤ k i := by
    intro i hi
    have h := quotientPathExponent_lower_bound B H w N i (by omega)
    change 3 ≤ quotientPathExponent B H w (2*N+3) i
    omega
  have hkstep : ∀ i, i < N → k (i+1) = (k i-2) +
      outerPeriods (B i) (H i) (w i) + centerPeriods (B i) (H i) (w i) := by
    intro i _
    rfl
  obtain ⟨n, d, hn, hc, hr⟩ := periodicWord_realizable (B 0) (H 0) (w 0)
    (2*N+3) hv (by omega)
  have hreal := quotient_path_actual_prefix B H w k N hp hguard hkstep n d hc hr
  exact ⟨n, hn, fun t ht => (hreal t ht).2⟩

end Agent1.Periodic

#print axioms Agent1.Periodic.quotientPathWord
#print axioms Agent1.Periodic.quotientPathExponent
#print axioms Agent1.Periodic.quotient_path_guarded_step
#print axioms Agent1.Periodic.quotient_path_actual_prefix
#print axioms Agent1.Periodic.quotientPathExponent_lower_bound
#print axioms Agent1.Periodic.quotient_path_finite_realizable
