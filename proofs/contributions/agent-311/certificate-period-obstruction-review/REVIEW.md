# Agent #311 — Certificate period obstruction review

Status: WIP / source-audited.

On main commit 9de08d78db6526e2ce2dd66cedd5e63f600424bd, the strongest located period statements are:

- checked_period_at_least_forty_two: check cert = true plus Admissible0 cert H M gives 42 ≤ cert.P.
- checked_saturated_period_constraints: the same checker/admissibility hypotheses plus the additional saturation equality 2 * totalGam cert = (cert.P : Int) gives cert.P % 72 = 0 and 72 ≤ cert.P.
- The earlier small-period obstruction independently gives cert.P % 2 = 0 for checked certificates.

Logical audit:
1. The divisibility-by-72 result is conditional on saturation. It must not be stated as a consequence of check cert = true alone.
2. Once saturation is assumed, the bound 72 ≤ P already follows from P % 72 = 0 together with positivity, so the separate 42 lower bound adds no further numerical restriction.
3. The small-period parity theorem is strictly weaker than P % 72 = 0 and adds no new restriction in the saturated regime.
4. Therefore these currently published period constraints do not by themselves obstruct the existence of a concrete ReturnCertificate. They only force any saturated candidate into periods P = 72, 144, 216, ... .
5. Combining the period facts with the published total-overflow identity O = 2(Dg + Dh), with Dg,Dh divisible by 9 and O divisible by 18, does not create a contradiction: the divisibility conditions are compatible.

Research conclusion:
The period route has been pushed to a clean necessary-condition boundary, but no new impossibility follows from the currently published congruences alone. A productive next attack must add an independent width, exterior, phase, or state-count constraint that conflicts with P = 72m, or directly construct/search a complete P=72 certificate.

Verification boundary:
This is a source-level audit, not a fresh Lean execution. No theorem is upgraded to LEAN-CHECKED by this note.
