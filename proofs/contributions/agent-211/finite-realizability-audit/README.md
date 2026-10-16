# Agent #211 — Finite-seed realizability audit

## Scope

M99-B211 asked whether the concrete return-certificate route still assumes an unproved finite-seed, canonical-realizability, or positive-head premise.

## Finding

No such premise remains at the certificate-to-seed endpoint.

For cert : Agent109.Cert.Certificate with check cert = true, the current Lean source gives this chain:

1. Agent112.Admissibility.automatic_admissibility derives ∃ H M, Admissible0 cert H M from check_sound.
2. valid_headPos proves every cyclic state has a positive exterior head; it is derived from the finite-width growth contradiction, not assumed.
3. The center symmetry/even-middle condition is reconstructed from raw_center_mirr, mirr_trim, and mirr_split, rather than supplied as a certificate hypothesis.
4. Agent112.Admissibility.certificate_existence_of_check derives an ordinary orbit with no palindromic iterate.
5. Agent112.Admissibility.checked_positive_decimal_seed strengthens that endpoint to ∃ m, 0 < m ∧ Lychrel196.IsLychrel m; the m = 0 case is explicitly excluded.

Thus the return-certificate route has the logical form:

(∃ cert, check cert = true) -> (∃ m, 0 < m ∧ Lychrel196.IsLychrel m).

## What remains open

The missing premise is an actual accepting ReturnCertificate instance. Finite-seed realizability is not the remaining gap.

Agent #11's M99-A01 search is consistent with this boundary: its bounded transition scans found no internal cycles in their stated finite domains, but this is computational WIP evidence and cannot establish global certificate nonexistence.

## Trust boundary

The retained Agent112 AuditAll record reports propext, Classical.choice, and Quot.sound for the key endpoint theorems, with no sorry/admit/new theorem axiom in the reported dependency list. This contribution is a source audit, not a fresh Lean execution.

## Research consequence

Future certificate searches should not add a new canonical-realizability or finite-seed hypothesis. A candidate must first satisfy the original Agent109.Cert.check; after that, the existing Agent112 endpoint supplies the positive ordinary decimal seed.

Verification status: SOURCE_AUDITED.