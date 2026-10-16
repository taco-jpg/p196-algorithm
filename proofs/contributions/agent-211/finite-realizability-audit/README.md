# Agent #211 — Finite-seed realizability audit

## Scope

Task M99-B211 asked whether the concrete return-certificate route still assumes an unproved finite-seed, canonical-realizability, or positive-head premise.

This audit compares the exact current Lean endpoints rather than relying on theorem names or prose summaries.

## Finding

No such premise remains at the certificate-to-seed endpoint.

For an arbitrary cert : Agent109.Cert.Certificate with check cert = true, the current source provides the following kernel-checked chain:

1. Agent112.Admissibility.automatic_admissibility cert hc derives ∃ H M, Admissible0 cert H M.
2. Its internal proof obtains Valid cert from check_sound cert hc, proves valid_headPos for every cyclic state, and then calls admissible_of_valid_head. The center symmetry/even-middle condition is reconstructed from the predecessor's raw center via raw_center_mirr, mirr_trim, and mirr_split; it is not supplied as an external certificate hypothesis.
3. Agent112.Admissibility.certificate_existence_of_check cert hc then derives ∃ m, ∀ k, ¬ Palindrome (orbit m k) directly from the accepted certificate.
4. Agent112.Admissibility.checked_positive_decimal_seed cert hc packages the same result as ∃ m, 0 < m ∧ Lychrel196.IsLychrel m. The positivity proof explicitly rules out m = 0 from the all-time non-palindrome property.

The exact source is proofs/AdmissibleCenters__24186301c272e538.lean, proofs/AdmissibleHeads__ed9fdb294df85110.lean, and proofs/AdmissibleCompat__f7177d4d859e88d5.lean on the audited main snapshot.

## Important boundary

This does not prove that an accepting certificate exists.

The remaining logical shape is:

(∃ cert, check cert = true) -> (∃ m, 0 < m ∧ Lychrel196.IsLychrel m).

The missing premise is therefore an actual accepted ReturnCertificate, not finite-seed realizability.

Agent #11's M99-A01 branch independently records the same distinction and searches finite transition domains, but those searches found no internal cycles in their stated bounded domains only. They do not establish global certificate nonexistence.

## Dependency / trust audit

The retained Agent112 AuditAll evidence reports that automatic_admissibility, certificate_existence_of_check, and checked_positive_decimal_seed depend only on propext, Classical.choice, and Quot.sound in the recorded audit; no sorry, admit, or newly introduced theorem axiom is reported there.

The repository publication policy still treats the certificate route as conditional until an actual check cert = true instance is supplied.

## Consequence for M99-B211

The finite-seed hypothesis should not be reintroduced into future certificate searches. A candidate certificate should be tested with the original Agent109.Cert.check; once check cert = true is established, the existing Agent112 endpoint supplies the positive ordinary decimal Lychrel seed without an additional canonical-realizability assumption.

This task therefore closes the proposed finite-realizability gap as a source-audited already-proved bridge, while leaving the substantive certificate-existence bottleneck open.

Verification status: SOURCE_AUDITED. No new Lean execution was performed in this ChatGPT tool environment.