# Certificate coordinate filter: exact boundary controls

## Result

`CertificateControls.lean` passes the pinned Lean 4.19.0 kernel at trust 0.
The source is frozen at SHA256
`578424a22b753be50fb7a3a5ba93d9acd9f8740d4c29c3a446dbf6f17b26845f`
(5,043 bytes). The author compile and full module audit both passed on their
first attempt. All twelve public theorem endpoints have literal `#print axioms`
commands in the source and actual successful compiler receipts.

The complete module-origin audit checked twenty theorem constants, including
generated private proofs, and four safe definition constants. Its axiom union is
exactly `{propext, Classical.choice, Quot.sound}`. Twenty-two compiler-generated
unsafe implementation constants are recorded separately in the raw audit log;
none is presented as a theorem. No proof source was changed after the successful
compile.

## What the counterexample proves

`cancellationCandidate` is an actual `Agent109.Cert.Certificate` with two listed
states and two links. Each link uses `j = j1 = j2 = k = 0` and `lo = lo' = 2`.
The `A` and `C` words are empty. The exact shared projection is
`Agent116.CertificateExterior.stateOuter`, which trims the exterior suffix;
the row theorem verifies that these two particular words are unchanged.

| Row | Phase | Exterior word | Signed contribution |
| --- | ---: | --- | ---: |
| 0 | 2 | `[1]` | -11 |
| 1 | 16 | `[8]` | 11 |

The signed contribution sum is zero and both strict signs occur, so the finite
`coordinateFilter` returns `true`. However, the original `LocalOK` phase equation
for the first row requires `tOf 2 + tOf 2 = 16`, which reduces to `4 = 16`.
The theorem `cancellationCandidate_first_phase_failure` refutes this local step
for arbitrary link data, not only for the links chosen in the candidate.

The original `check` therefore returns `false`. The unchanged-answer theorem
from `CertificateFilter` also gives `filteredCheck = false`. The exported theorem
`coordinateFilter_not_sufficient` formally refutes the universal implication
from filter acceptance to original checker acceptance.

This is a rejected candidate with legal row phases and cancelling coordinates.
It does not produce an accepted certificate, an actual exterior cycle, a realized
ordinary trajectory, or a global period or acyclicity result. Other local
conditions may also fail; the phase contradiction already establishes rejection.

## Boundary controls

`emptyCandidate` has period zero and an empty signed sum of zero. Its coordinate
filter and original checker both return `false`. The zero sum alone does not
supply the required sign witnesses.

`zeroPhaseCandidate` has one listed row, phase zero, and an empty exterior word.
Its sole contribution and total sum are zero, while both Boolean tests return
`false`. This distinguishes positive listed length from positive phase: positive
length and a zero sum alone need not produce either strict sign.

## Exact verification inputs and retained evidence

The author used the fresh seventeen-module baseline at
`runtime-agent6/review-certificate/baseline/build/objects`, followed by the frozen
`CertificateCoordinates` source SHA256
`8ed2868cd53b9de494d5568a901f7280ad57746bfcefcede6ccfa02855c4a47e`
and frozen `CertificateFilter` source SHA256
`29c684a2f83335bd9fa69a4881f415990d9eb33cb1e52206131a4cc1b172e8ff`.
The exact object hashes and baseline source-manifest hash are recorded in each
attempt's `verification.json`.

The official Lean binary hash is
`92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.
Both compiler calls used `--trust=0 -j1 -DElab.async=false`. They produced separate
raw logs under `attempts/CertificateControls-001` and
`attempts/CertificateControlsAudit-001`; neither log has been edited.
`RESULT.json`, `exported-axioms.json`, and `full-module-axioms.json` summarize
those actual receipts. `MANIFEST.json` hashes the support files while excluding
compiled objects. `finalize_review.py` only parses retained evidence and does not
re-run any proof build.
