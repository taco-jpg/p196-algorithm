# Zero-period finite quotient-path bridge

Claim: `efe6d4b95f53ad8fbcebf113f8da0616dfa67b22`.
Canonical source: `proofs/Agent1PeriodicZeroPath.lean`.

## Exact interfaces

All declarations are in `Agent1.Periodic` and use the existing `QuotientPath`, `ValidPeriodic`, `zeroStateOrbit`, `rawPeriod_zero`, and `zeroStateOrbit_no_cycle` without changing their definitions.

- `quotient_path_zeroStateOrbit B H w N hp hzero i hi` proves `w i = [0,0,0,0] ∧ (B i,H i) = zeroStateOrbit (B 0,H 0) i` for every `i ≤ N`. It needs only the original finite `QuotientPath` and the initial zero period; the path itself provides the bounds used in `rawPeriod_zero`.
- `quotient_path_zero_interface_ne B H w N hp hv hzero hN` proves `(B N,H N) ≠ (B 0,H 0)` under original initial validity and `0 < N`.
- `quotient_path_zero_no_return B H w N hp hv hzero hN` proves `¬ (B N = B 0 ∧ H N = H 0 ∧ w N = w 0)` with exactly those hypotheses.

The result is a bridge to the existing no-cycle theorem. It does not remove abstract zero graph cycles, assert termination, or introduce safety/exponent assumptions. No dependency on the separately developed general path-validity/projection API was required.

## Verification and preserved attempts

Official Lean 4.19.0, `--trust=0 -j1 -DElab.async=false`, explicit `LEAN_PATH`. Every run records exact arguments, paths, source/compiler/object hashes, dependencies, output, resource use and exit status. All 24 ZeroCycle dependency sources and the WidthPath source were checked against the current checkout before running. This is an incremental author check, not the parent's later fresh build.

- `attempt-001`: first and only source compilation, exit 0, 0.321 seconds, maximum RSS 444,656 KiB, 1,843,200,000-byte address-space limit.
- `audit-001`: signal 11 under the same address-space limit; no successful audit claim.
- `audit-002`: unchanged audit source run with a 4-GiB address-space limit; it enumerated all declarations and exited 1 because the expected count omitted two generated proof auxiliaries. All five already passed its axiom checks.
- `audit-003`: corrected complete inventory count; exit 0, 1.200 seconds, maximum RSS 761,148 KiB. Five theorem declarations (three exported endpoints and two generated proof auxiliaries), zero definitions, zero custom axioms. Every theorem uses only the permitted `propext`, `Classical.choice`, and `Quot.sound`.

Canonical source SHA-256: `078d6356f3eba5286f77d11e202df4759ecfd8e6473f5475d4ef443799732d0a`.

Only the owned new source and this contribution directory were written. No existing definition, registry, Git state, or external service was modified by this specialist.
