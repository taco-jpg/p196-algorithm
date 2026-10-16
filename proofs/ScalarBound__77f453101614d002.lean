import ScalarHierarchy
import RootBridge

/-! Final finite-certificate application. Acceptance of this module requires
successful compilation of the complete numerical hierarchy and its audit. -/

namespace ScalarBound

open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory ScalarOrbit

theorem root_vertex_certificate : ScalarPeriods.RootVertexCertificate :=
  RootBridge.certificate_of_finite_root_bound ScalarHierarchy.finite_root_bound

/-- Every rotation of the prescribed scalar clock has at most 94 complete
periods when its actual starting width is at least 14. -/
theorem wide_periods_le_94 (q : Nat → Nat) (L a s R : Nat)
    (ha : Admissible L q) (hwidth : 14 ≤ widthAt q L a)
    (hc : ClockSegment q L a s (7 * R)) : R ≤ 94 :=
  ScalarPeriods.wide_periods_le_94_of_root_certificate root_vertex_certificate
    q L a s R ha hwidth hc

theorem initial_width_dependent_bound (q : Nat → Nat) (L s R : Nat)
    (ha : Admissible L q) (hc : ClockSegment q L 0 s (7 * R)) :
    R ≤ 94 + warmup L :=
  ScalarPeriods.width_dependent_bound_of_root_certificate root_vertex_certificate q L s R ha hc

/-- Uniform actual-word bound, including width one and all starting phases. -/
theorem periods_le_98 (q : Nat → Nat) (L a s R : Nat)
    (ha : Admissible L q) (hc : ClockSegment q L a s (7 * R)) : R ≤ 98 :=
  ScalarPeriods.shifted_periods_le_98_of_root_certificate root_vertex_certificate q L a s R ha hc

theorem canonical_periods_le_98 (n : Nat) (d q : Nat → Nat) (L a s R : Nat)
    (hc : Canonical n d L) (hrep : ∀ i, i < L → columnSum d L i = q i)
    (hclock : ClockSegment q L a s (7 * R)) : R ≤ 98 :=
  ScalarPeriods.canonical_periods_le_98_of_root_certificate root_vertex_certificate
    n d q L a s R hc hrep hclock

theorem no_99_period_clock (q : Nat → Nat) (L a s : Nat) (ha : Admissible L q) :
    ¬ ClockSegment q L a s (7 * 99) := by
  intro hc
  have hb := periods_le_98 q L a s 99 ha hc
  omega

theorem wide_no_95_period_clock (q : Nat → Nat) (L a s : Nat)
    (ha : Admissible L q) (hwidth : 14 ≤ widthAt q L a) :
    ¬ ClockSegment q L a s (7 * 95) := by
  intro hc
  have hb := wide_periods_le_94 q L a s 95 ha hwidth hc
  omega

end ScalarBound
