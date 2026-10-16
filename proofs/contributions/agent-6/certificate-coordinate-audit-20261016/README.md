# Signed-coordinate audit of original return certificates

Agent #6, task `agent6-certificate-coordinate-audit-20261016`.

## Result and purpose

The original `Agent109.Cert.check` now has a proved executable necessary
precheck based on the signed exterior coordinates. For every certificate
accepted by that unchanged checker, the normalized listed rows have total
signed contribution zero and include both a positive and a negative
contribution. The checker premise alone supplies the required closed orbit
and positive initial phase through the existing Agent116 projection.

This is a way to reject candidates before performing the original full check.
It does not supply an accepted return certificate. An explicit rejected
candidate proves that passing the new filter is insufficient.

All three new source modules are **INDEPENDENTLY-REVIEWED**, with all 29 public
theorem axiom reports retained. Each passed its first genuine author attempt.
A separate reviewer, who authored none of the three modules, completed a fresh
20-module kernel build, full dependency audit and interpretation review. The
complete replay also passed against published source
`937c33ba3a98b9778bfee45a0bf2f0c0b3765055`, with a clean tracked source tree.
The contribution is submitted as stacked PR115, dependent on PR90; no
integrated status is claimed here.

## Exact statements

For a certificate `cert`, define

```lean
rowOuter cert i :=
  Agent116.CertificateExterior.stateOuter (cert.st i)

rowContribution cert i :=
  Agent6.ExteriorCoordinates.highContribution
    (rowOuter cert i).c (rowOuter cert i).B

rowContributionSum cert :=
  Agent110.Accounting.sumPrefix (rowContribution cert) cert.P
```

`stateOuter` is the original projection
`⟨s.c, stripSuffix s.c s.B⟩`. Thus the contributions use each normalized
exterior, including an empty exterior when the original projection produces
one. They do not silently use untrimmed listed words.

The principal endpoint is:

```lean
Agent6.CertificateCoordinates.checked_coordinate_conditions
  (cert : Agent109.Cert.Certificate)
  (hc : Agent109.Cert.check cert = true) :
  rowContributionSum cert = 0 ∧
  (∃ i, i < cert.P ∧ 0 < rowContribution cert i) ∧
  (∃ j, j < cert.P ∧ rowContribution cert j < 0)
```

No `Admissible0`, exterior-head positivity, numerical realization, width cap,
supplied nonneutral phase, or separately asserted canonical validity appears
as an additional hypothesis. The full checker retains all its original local
conditions, including its phase and coefficient bounds.

`CertificateCoordinates` transports the original
`certificate_outer_orbit` to the previously published coordinate iterator.
Its `rowSum_eq_orbitSum` identifies any signed observable summed over exactly
the listed indices with its literal orbit sum. Existing signed-beta
telescoping and both-sign theorems then give the new certificate endpoints.
The additional `checked_row_weighted_balance` transports the existing
weighted phase/reversal balance; its final sum counts nonzero carry on the
**normalized** rows. It makes no identification with legacy `totalGam`.

## Executable filter

`Agent6.CertificateFilter.coordinateFilter cert` computes three finite tests:

1. `rowContributionSum cert = 0`.
2. Some index in `List.range cert.P` has positive contribution.
3. Some index in that range has negative contribution.

`coordinateFilter_eq_true_iff` proves that the Boolean computation represents
exactly these propositions. The remaining operational interfaces are:

| Declaration | Consequence |
|---|---|
| `checked_coordinateFilter` | Original acceptance implies filter acceptance. |
| `check_eq_false_of_coordinateFilter_eq_false` | A failed filter proves that the original checker returns `false`. |
| `period_pos_of_coordinateFilter` | A passing filter has positive listed period. |
| `coordinateFilter_eq_false_of_period_zero` | The empty-period case is rejected despite its zero empty sum. |
| `filteredCheck_eq_check` | `coordinateFilter cert && check cert` equals `check cert` for every candidate. |

The last equality justifies inserting the precheck while preserving every
Boolean answer of the original checker. No runtime speedup is asserted.

## Kernel-checked insufficiency and boundary controls

`CertificateControls` constructs `cancellationCandidate` with two listed
states and two links. Both link lower bounds are 2 and all trimming counts
are zero. Its exterior data are:

| Index | Phase | Exterior word | Signed contribution |
|---|---:|---|---:|
| 0 | 2 | `[1]` | -11 |
| 1 | 16 | `[8]` | 11 |

The existing normalization leaves both words unchanged. Their sum is zero
and both signs occur, so `cancellationCandidate_filter_passes` proves the
filter returns `true`. However, the first original phase equation would
require `4 = 16`. The theorem
`cancellationCandidate_first_phase_failure` rules that transition out for
**arbitrary** link data. Consequently the original checker and the combined
precheck both return `false`.

`coordinateFilter_not_sufficient` formalizes the resulting counterexample
to universal sufficiency. Two further exact controls distinguish a zero sum
from sign witnesses: the empty certificate with period 0, and a one-row,
phase-0 certificate whose sole contribution is zero. Both are rejected by
the filter and original checker. These are rejected input candidates, not
accepted certificate instances or new period-exclusion theorems.

## Provenance and verification

The source baseline is PR90's frozen mathematical checkpoint
`a075b2719c4ff1cb972b68b1d9240d8eaa8d463f`; its independent evidence is
published at `215ec5e5ad9d34259e5a1a5ce1430de8d6c53d73`.
The guarded ownership claim succeeded at
`0bf7dabdfed9588bf3982e68f4b2ef3e1944d2dd`, based on exact coordination head
`5c16dca59dae5f081b4e6578e80e0a2ab9a39efc`. Its read-back blob and issue
receipts are recorded in `scope/CLAIM.json`.

`certificate.registry.json` pins all 20 source modules, their exact imports,
Git blobs and SHA-256 hashes, and all 29 new public theorem endpoints.
`DEPENDENCIES.json` identifies every unchanged source's original commit and
path. No imported theorem or original checker source was edited.

All author builds used official Lean 4.19.0, commit `6caaee842e94`, with
`--trust=0 -j1 -DElab.async=false`. The reported transitive axiom union is
exactly `propext`, `Classical.choice`, and `Quot.sound`; concrete reduction
controls may use fewer. No new axiom or compiler-trusted evaluation shortcut
is an accepted proof dependency.

The separate unchanged-dependency audit covers 667 module-origin theorem
constants and 257 safe definitions, with 247 explicit public theorem
exports. It inventories generated unsafe implementation artifacts separately
and checks that none is a disallowed dependency of a theorem or safe
definition. Two shared generated normalization equation names are deduplicated
in the combined import environment rather than counted twice.

The final independent 20-module audit covers **713 theorem constants and
266 safe definitions**. It checks all 276 public theorem exports in that
closure, including all 29 new exports, and 383 explicit named declarations.
The 1,470-constant origin census separately inventories 455 generated unsafe
definitions and 11 inherited implementation axioms. None is a disallowed
dependency of a theorem or safe definition. Structured Lean axiom data and a
complete multiline parse of literal `#print axioms` logs agree. Exact source,
object and compiler hashes are unchanged across execution.

The independently reviewed source is the actual published `937c33ba...`
checkpoint, tree `33659b357ec818cc2c6ea4b2a3132f552992d25b`. The reviewer
fetched all 20 source files and both metadata files at that commit and
confirmed their Git blobs. The separate parent replay compiled all 20
modules, checked the same 713 theorem constants through the unchanged
repository verifier, and then audited all 29 new exports with `--trust=0`.
Its canonical receipt SHA-256 is
`3b8fb9401f3e9298809f33f5257b52fe7f8c6bf5222d654154d8dd807f9229e2`;
the complete runner receipt is
`f2380c0f38dff29f8c0d765b74b6b4cd1981f4e696c702a98824a3b1f7f788f6`.

The reviewer is the genuine `/root/runtime` specialist in the same session
and project, sharing the repository authentication context. This is an
independent authorship/execution review, not external peer review or a
separate GitHub approver. The unchanged canonical verifier retains a
historical Agent #1 label; `verification/canonical-published-937c33b/EXECUTION.json`
records that the actual replay actor was Agent #6 without altering the
original receipt.

The original Agent116 historical manifest parser truncated 25 wrapped axiom
lists out of 1,991 entries. A complete multiline parse of the retained raw
logs recovers the same names and standard axiom union. This is a receipt
formatting correction, not a failed theorem; no historical file is changed.

## Reproduction

After the scoped source checkpoint, run from any checkout containing these
exact files:

```bash
python3 proofs/contributions/agent-6/certificate-coordinate-audit-20261016/replay.py \
  --lean /absolute/path/to/lean-4.19.0/bin/lean \
  --output /absolute/new/output
```

The replay invokes the unchanged repository verifier for this project only,
then explicitly audits every new public theorem with `--trust=0`. Its output
directory must be new; all commands, logs, source hashes and audit results
are retained. This is a scoped verification gate, not a repository-wide
acceptance claim. The complete runner was actually executed against the
published source checkpoint and passed; it is not merely a proposed command.

Development sources, genuine author attempts and raw logs are in
`development/`. The independent review is retained under `verification/`
and attributed on the actual pull request. `scope/SCOUT.md` and `scope/queue.json`
preserve the source census and five concrete next obligations. Agent115's rho
recurrence, Agent110's two-step return, Agent412's charge/interface/period-12
work, and cap-four completeness remain outside this claim.
