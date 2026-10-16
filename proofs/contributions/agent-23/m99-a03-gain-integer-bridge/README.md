# Agent #23 — M99-A03 gain/integer bridge

Status: SOURCE-PUBLISHED / VERIFICATION-PENDING

Manager #99 dispatch: support M99-A03 with exact accumulated gain and certificate-to-integer interfaces; coordinate with Agent #13. Agent #13's existing WIP gain audit remains its own work. This contribution is deliberately complementary: it composes the existing exact gain theorems with the existing automatic-admissibility integer endpoint.

## Exact contract

For a finite return certificate cert, the accepted checker premise is exactly check cert = true.

The exported interface establishes, without adding hypotheses:

* 0 <= totalG cert;
* 0 <= totalH cert;
* ∃ m, 0 < m ∧ Lychrel196.IsLychrel m.

The first two conjuncts are the existing Agent #110 accounting results. The third is the existing Agent #112 certificate-to-integer bridge, which itself uses Agent #109's ordinary decimal realization and Lychrel compatibility.

This is conditional on a checked certificate. It does NOT provide a certificate instance, does NOT assert that 196 is Lychrel, and does NOT turn a finite search into an infinite existence result without the checked certificate premise.

## Source pins

Research main at dispatch: afbb3282be77f63711aca4fb165814104a365806.
Current repository base used for this contribution: main commit 02224f03a0fe24bf270e1c8feb6c71d128fdd9ba.

Relevant source declarations:
* Agent110.Accounting.totalG_nonneg
* Agent110.Accounting.totalH_nonneg
* Agent112.Admissibility.checked_positive_decimal_seed
* Agent109.Cert.check_sound
* Agent109.CertCompat.certificate_existence_lychrel

Agent #13 branch observed at dispatch: research/agent-13/m99-a03-20261015, with its own m99-a03-gap-gain-audit/Audit.lean. No files owned by Agent #13 were modified.

## Verification

The source was published on isolated branch formalize/agent-23/m99-a03-20261015, commit 62fb48fe190a736b577c7ebb1aae8e8c8e5165d0.

The connected repository interface does not expose a local Lean compiler shell, so this session has not independently compiled this new wrapper. Existing repository evidence reports the imported endpoint chain as Lean 4.19.0 kernel-checked with only the project's permitted logical foundations. The new wrapper therefore remains VERIFICATION-PENDING until a clean build compiles this exact source and its transitive dependency closure.

No sorry, admit, native_decide, or new mathematical axiom is introduced by the source text.
