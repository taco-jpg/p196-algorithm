import P196.SparseProfileGrowth.FiniteNeighborhoods
import P196.SparseProfileGrowth.Propagation
import P196.Agent9DigitSumWindows.DecimalEmbedding

set_option autoImplicit false

/-!
# Linear growth from finite propagation of positive coefficients

The existing nonsymmetric profile iterator keeps every positive coefficient
within distance `t` of a positive initial coefficient after `t` steps. The
finite neighborhood mass estimate therefore bounds each later profile mass
by a linear function of time and the initial mass.

The exact padded representation transfers this estimate to ordinary decimal
reverse-and-add digit sums, including seed zero. No initial width parameter
is required. The coefficient is a sufficient bound; no optimality, exact
support equality, or palindrome-avoidance conclusion is asserted.
-/

namespace SparseProfileGrowth

open DecimalProfile DecimalDigits DecimalMass Lychrel196

/-- Valid profile mass has a linear upper bound depending only on initial mass. -/
theorem mass_iter_le_linear (s : DecimalProfile.State) (t : Nat)
    (hv : DecimalProfile.Valid s.1 s.2) :
    DecimalProfile.mass (DecimalProfile.iter s t) ≤
      18 * (2 * t + 1) * DecimalProfile.mass s := by
  have hvalid := DecimalProfile.iter_valid s t hv
  exact mass_le_of_positive_origin s.2 (DecimalProfile.iter s t).2
    s.1 (DecimalProfile.iter s t).1 t 18
    (fun i _ => hvalid.2.2.1 i)
    (fun i _ hi => iter_positive_origin s t i hv hi)

/-- Every ordinary decimal orbit satisfies a linear digit-sum upper bound
in its initial digit sum, with no width or positivity hypothesis. -/
theorem digitSum_orbit_le_linear (n t : Nat) :
    DecimalMass.digitSum (Lychrel196.orbit n t) ≤
      18 * (2 * t + 1) * DecimalMass.digitSum n := by
  by_cases hz : n = 0
  · subst n
    have hzero : Lychrel196.orbit 0 t = 0 := by
      induction t with
      | zero => rfl
      | succ t ih =>
        change Lychrel196.step (Lychrel196.orbit 0 t) = 0
        rw [ih]
        rfl
    simp only [hzero, digitSum_zero, Nat.mul_zero, Nat.le_refl]
  · obtain ⟨d, L, hc⟩ := canonical_exists n (by omega)
    have ha := NormalizationBridge.canonical_admissible n d L hc
    have hv := DecimalProfile.NumericBridge.pad_valid (columnSum d L) L ha
    have hbound := mass_iter_le_linear
      (DecimalProfile.NumericBridge.embed (L, columnSum d L)) t hv
    have hstart :
        DecimalProfile.mass (DecimalProfile.NumericBridge.embed (L, columnSum d L)) =
          2 * digitSum n := by
      simpa only [DecimalProfile.iter, Lychrel196.orbit] using
        DecimalProfile.NumericBridge.mass_numeric_iter n d L 0 hc
    rw [DecimalProfile.NumericBridge.mass_numeric_iter n d L t hc, hstart] at hbound
    have hfactor : 18 * (2 * t + 1) * (2 * digitSum n) =
        2 * (18 * (2 * t + 1) * digitSum n) := by ac_rfl
    rw [hfactor] at hbound
    omega

#print axioms mass_iter_le_linear
#print axioms digitSum_orbit_le_linear

end SparseProfileGrowth
