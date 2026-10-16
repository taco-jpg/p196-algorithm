# Structural certificate accounting development

**Evidence label:** formal necessary conditions on an `Agent109.Cert.Valid`
symbolic certificate; no certificate instance, integer realization, infinite
seed, or statement about 196 is supplied.

`CertificateAccounting.lean` derives the local physical width equation from the
exact returned block lengths and the supplied `LocalOK` trimming equalities.
Finite cyclic telescoping then proves
`totalGam = 2 * (totalG + totalH)`, both signed gap totals nonnegative, and an
explicit nonnegative integer half of `totalGam`. Arbitrary nonmaximal trims are
allowed because no maximality predicate occurs in the hypotheses or proofs.
Each block length also telescopes individually, giving `totalJ = P`,
`totalJ1 + totalJ2 = 2*P - totalGam`, and
`2*totalK = 2*P - totalGam`. The signed gap totals are related directly to
these trim counts by the definition-expansion theorems in the same module.

Development compiler: official Lean 4.19.0 release, commit
`6caaee842e94`, invoked through the parent task's recorded compatibility wrapper.
Imports are the existing Agent #109 `TemplateStep.lean` and
`ReturnCertificate.lean` plus their Core/Std dependencies. The shared dependency
build is recorded separately by the runtime agent. This developer's axiom
audit is not an independent semantic review.

`verify.py` records each current-source snapshot, command, compiler output,
source and dependency hashes, and every public theorem's `#print axioms` output.
The ordinary permitted logical axioms are `propext`, `Classical.choice`, and
`Quot.sound`. No admitted declaration, custom axiom, native Boolean reduction,
or hidden finite evaluation is introduced.

Replay, with freshly compiled dependencies and the recorded compiler wrapper:

```sh
python3 proofs/contributions/agent-110/certificate-budget/accounting-development/verify.py \
  --lean /path/to/lean-4.19.0-wrapper \
  --deps /path/to/fresh-agent109-dependencies \
  --build /path/to/empty-accounting-build
```

History retained in full:

- `attempt-001`: failed because two explicit lambda applications were not
  reduced before rewriting/arithmetic. It did not expose a mathematical gap.
- `attempt-002`: all 18 public theorems compiled; unused generic positivity
  argument generated one linter warning.
- `attempt-003`: removed that unnecessary argument; clean compilation and all
  18 public theorem axiom queries passed. Its JSON identifies exact source and
  dependency hashes.
- `attempt-004`: added individual block-length telescopes and trim-count
  formulas; clean compilation and all 30 public theorem axiom queries passed.
  This is the current formal-source checkpoint.

The numbered audit source files for attempts 003 and 004 were deterministically
regenerated from their retained source snapshots after the driver was changed
to preserve audit source under attempt-specific names. Their contents match
the exact `#print axioms` commands represented by the corresponding retained
logs. `AccountingAxiomAudit.lean` is the last pre-change generated audit source.

Compiled `.olean` products and duplicate dependency sources are reproducible
infrastructure and remain outside this evidence directory. Published sources,
failed attempts, logs, audit source, and execution manifests remain here.
