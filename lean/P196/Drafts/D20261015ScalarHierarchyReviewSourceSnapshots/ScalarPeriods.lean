import P196.Drafts.D20261015ScalarHierarchyReviewSourceSnapshots.ScalarRoot
import P196.Drafts.D20261015ScalarHierarchyReviewSourceSnapshots.WidthOne

/-! Final scalar-period arithmetic, conditional on the concrete root graph
certificate. This module does not assert that certificate has been checked.
Every starting clock phase and every actual starting time are explicit. -/

namespace ScalarPeriods

open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory
open ScalarOrbit ActualPrefixLift

/-- Exact endpoint expected from the finite hierarchy instance. This is a
named proposition, not an axiom or a theorem supplied by this module. -/
def RootVertexCertificate : Prop :=
  ∀ (q : Nat → Nat) (L a s n : Nat) (path : Nat → Fin 7),
    Admissible L q → 14 ≤ L → ActualPath ScalarRoot.root q L 1 a s path n → n ≤ 659

theorem iterPairs_restart (q : Nat → Nat) (L a t : Nat) :
    iterPairs (iterPairs q L a).2 (iterPairs q L a).1 t = iterPairs q L (a + t) := by
  induction t with
  | zero => simp only [iterPairs, Nat.add_zero]
  | succ t ih =>
    simp only [iterPairs, Nat.add_succ, ih]
    rfl

theorem clock_restart (q : Nat → Nat) (L a s n : Nat) :
    ClockSegment q L a s n ↔
      ClockSegment (iterPairs q L a).2 (iterPairs q L a).1 0 s n := by
  simp only [ClockSegment, outerAt, Nat.zero_add, iterPairs_restart]

/-- A period has seven edges and the clock window includes both endpoints,
so R periods give 7R+1 graph vertices. The bound holds in every rotation. -/
theorem wide_periods_le_94_of_root_certificate (hcert : RootVertexCertificate)
    (q : Nat → Nat) (L a s R : Nat) (ha : Admissible L q)
    (hwidth : 14 ≤ widthAt q L a) (hc : ClockSegment q L a s (7 * R)) : R ≤ 94 := by
  have had := iterPairs_admissible q L a ha
  have hclock := (clock_restart q L a s (7 * R)).mp hc
  have hp := ScalarRoot.actual_root_path (iterPairs q L a).2 (iterPairs q L a).1
    0 s (7 * R + 1) had (by
      intro i hi
      exact hclock i (by omega))
  have hb := hcert (iterPairs q L a).2 (iterPairs q L a).1 0 s (7 * R + 1)
    (ScalarRoot.phasePath s) had hwidth hp
  omega

theorem width_dependent_bound_of_root_certificate (hcert : RootVertexCertificate)
    (q : Nat → Nat) (L s R : Nat) (ha : Admissible L q)
    (hc : ClockSegment q L 0 s (7 * R)) : R ≤ 94 + warmup L := by
  apply period_bound_after_warmup q L s R 94 ha hc
  intro a phase periods hwidth hclock
  exact wide_periods_le_94_of_root_certificate hcert q L a phase periods ha hwidth hclock

theorem periods_le_98_of_width_ge_two (hcert : RootVertexCertificate)
    (q : Nat → Nat) (L s R : Nat) (ha : Admissible L q) (hL : 2 ≤ L)
    (hc : ClockSegment q L 0 s (7 * R)) : R ≤ 98 := by
  have hb := width_dependent_bound_of_root_certificate hcert q L s R ha hc
  have hk := warmup_at_most_four L hL
  omega

/-- Width one cannot complete any period; all larger widths use warmup. -/
theorem periods_le_98_of_root_certificate (hcert : RootVertexCertificate)
    (q : Nat → Nat) (L s R : Nat) (ha : Admissible L q)
    (hc : ClockSegment q L 0 s (7 * R)) : R ≤ 98 := by
  by_cases hL : L = 1
  · subst L
    have hz := WidthOne.zero_complete_periods q s R ha hc
    omega
  · have hpos := ha.1
    exact periods_le_98_of_width_ge_two hcert q L s R ha (by omega) hc

/-- The uniform bound also applies to a clock beginning later in the orbit. -/
theorem shifted_periods_le_98_of_root_certificate (hcert : RootVertexCertificate)
    (q : Nat → Nat) (L a s R : Nat) (ha : Admissible L q)
    (hc : ClockSegment q L a s (7 * R)) : R ≤ 98 :=
  periods_le_98_of_root_certificate hcert (iterPairs q L a).2 (iterPairs q L a).1 s R
    (iterPairs_admissible q L a ha) ((clock_restart q L a s (7 * R)).mp hc)

/-- Canonical decimal digits discharge admissibility for the actual word. -/
theorem canonical_periods_le_98_of_root_certificate (hcert : RootVertexCertificate)
    (n : Nat) (d q : Nat → Nat) (L a s R : Nat)
    (hc : Canonical n d L) (hrep : ∀ i, i < L → columnSum d L i = q i)
    (hclock : ClockSegment q L a s (7 * R)) : R ≤ 98 := by
  have ha : Admissible L q := NormalizationBridge.admissible_congr _ _ _
    (NormalizationBridge.canonical_admissible n d L hc) hrep
  exact shifted_periods_le_98_of_root_certificate hcert q L a s R ha hclock

end ScalarPeriods
