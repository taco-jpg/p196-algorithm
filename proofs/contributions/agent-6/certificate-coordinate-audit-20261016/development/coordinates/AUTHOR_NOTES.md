# CertificateCoordinates: author semantic notes

The source is frozen at SHA-256 `8ed2868cd53b9de494d5568a901f7280ad57746bfcefcede6ccfa02855c4a47e`, Git blob `958b7b77401171f3c05258c4d93fa8d5e21562f4`. The first author compilation passed under official pinned Lean 4.19.0 with `--trust=0 -j1 -DElab.async=false`. It reused the runtime specialist's fresh build of all 17 unchanged dependencies; every dependency object hash was independently checked against the supplied readiness receipt. This author receipt does not substitute for the separate independent review.

## Meaning of the exported interface

`rowOuter cert i` is exactly Agent116's existing `stateOuter (cert.st i)`: it keeps the row phase and removes the maximal suffix equal to that phase from B. `rowContribution cert i` applies the previously checked `highContribution` to that normalized state. `rowContributionSum cert` uses Agent110's existing `sumPrefix` over exactly `cert.P` rows. It does not use the raw, potentially partially trimmed B from the certificate.

The central checker endpoint is:

```lean
checked_coordinate_conditions (cert : Certificate) (hc : check cert = true) :
  rowContributionSum cert = 0 ∧
    (∃ i, i < cert.P ∧ 0 < rowContribution cert i) ∧
    (∃ j, j < cert.P ∧ rowContribution cert j < 0)
```

The premise is the unchanged full checker. `check_sound` supplies a positive period and every original `LocalOK` link. The existing Agent116 projection supplies the literal closed exterior orbit. The first checked phase is positive, so the already checked general positive-phase nonzero result is enough to obtain both signs. No Admissible0, integer realization, positive exterior head, width cap, nonempty B, even phase, or separate validOuter hypothesis is added. The witnesses refer to actual list indices strictly below P.

The proof adds only iterator and sum compatibility around the existing cycle results. It does not reprove trim invariance, exterior projection, the signed-beta step, generic zero-sum sign logic, or any phase-period theorem.

`checked_row_weighted_balance` also transports the existing weighted cycle identity. Its last term is the Int prefix sum of `overflowBit` on the normalized rows. It makes no identification with the original checker's `totalGam` on raw rows, and proves no rho recurrence or new overflow theorem.

## Verification receipt

There are **11 public theorems, 3 private helper theorems, and 3 definitions**. The private helpers identify the two forward iterators, orbitSum with sumPrefix, and the orbit sum of overflow indicators with overflowCount. All three are used by audited public exports.

`attempt-001/compile.log` contains the complete public `#print axioms` output. `audit_receipts.py` parses bracketed axiom lists across line breaks, rejects missing, duplicate, and unexpected receipts, and checks the exact 11-public-theorem coverage. Its axiom union is only `propext`, `Classical.choice`, and `Quot.sound`. The source contains no admitted proof, new axiom declaration, or native_decide use.

The compile command, timing, source/object hashes, and exact reused dependency manifest are preserved in `attempt-001/compile-result.json`, `source-pin.json`, `dependency-source-manifest.json`, and `dependency-OBJECTS_READY.json`. The compiled object SHA-256 is `94232f075685bc14290db45cc54d8473b620144ff977c58e0856b38fce96cb1a`. `VERIFICATION.json` and `axiom-audit.json` give the structured receipts. There was one author attempt and no failed author attempt.

These are necessary conditions for certificate acceptance. They do not supply an accepting certificate, an infinite ordinary orbit, a period exclusion, or a result about 196. The parent-owned Filter and independently authored Controls address executable filtering and its insufficiency separately.
