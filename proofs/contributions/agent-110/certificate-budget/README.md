# Arithmetic constraints on actual return certificates

Status: accounting and saturation endpoints **INDEPENDENTLY-REVIEWED**, not
integrated into main. The final check-only consumers are LEAN-CHECKED, with a
nineteen-module independent rebuild pending. This package proves necessary
conditions on the existing `Agent109.Cert.Certificate` checker. It does not
supply a certificate instance.

For a certificate of period `P`, let `O = totalGam cert` be its actual total
overflow and let `Dg = totalG cert`, `Dh = totalH cert` be its signed total gap
increments. These names refer to the original raw-block formulas and supplied
trim counts; individual increments may be negative. Trimming need not be
maximal and finite blocks have no imposed length cap.

The final endpoint `Agent110.Checked.six_phase_constraints` assumes:

* `Agent109.Cert.check cert = true`;
* initial phase in `{2,4,8,16,14,10}`.

It proves, without numerical accounting or carry-budget assumptions,

```
O = 2 (Dg + Dh)
Dg >= 0, Dh >= 0, Dg % 9 = 0, Dh % 9 = 0
O >= 18, O % 18 = 0
2 O <= P <= 4 O
P % 6 = 0, P >= 42.
```

The separate endpoint `Agent110.Checked.saturated_period_constraints` retains
the explicit equality `2 O = P`; it gives `P % 72 = 0` and `P >= 72`.
`Agent110.Checked.period_at_least_four` applies to every phase class from
`check cert = true` alone.

Agent 112's `automatic_admissibility` supplies the original `Admissible0` split
witness. The source is used unchanged, not reproved or attributed to Agent 110.
Earlier reusable layers still expose `Valid cert` and positive initial
exterior as their precise hypotheses. The leading coefficient is
`B.head?.getD c`, including the empty-`B` case. Positivity is derived and
propagated; no all-indices positivity is silently assumed.

## Sources and reusable interfaces

| Module | Main result |
|---|---|
| `CertificateAccounting` | Exact local width identity, cyclic accounting, nonnegative total gains, and all four trim-total identities |
| `CertificateCharge` | Exterior and interface charge laws through arbitrary certified trims; six-phase overflow and trim-difference congruences |
| `CertificateCarryBudget` | Actual leading-coefficient transition; positive cyclic overflow and `2 O <= P <= 4 O` |
| `CertificatePhases` | Even returned phases and six-phase period divisible by six |
| `CertificateConsequences` | Direct combined checker endpoint and, if `O=18`, gain cases `(Dg,Dh)=(9,0)` or `(0,9)` |
| `CertificatePrefix` | Exact phase-padded three-column transition through arbitrary trims |
| `CertificateSaturation` | Reuse Agent 4's finite saturation proof to derive `P>=42`, and saturated `72` divisibility |
| `CertificateChecked` | Consume Agent 112's automatic admissibility to remove the separate realization/positivity premise |
| `All` | Accepted package import root |

All new theorem namespaces begin with `Agent110`. Existing Agent 109 checker
definitions, Agent 2 exterior arithmetic, and the original carry potentials
are imported unchanged. This completes the certificate-level arithmetic
correspondence; the earlier conditional budget formulas are credited rather
than counted as new discoveries. Agent 116 owns the separate projection to
canonical maximally trimmed exteriors. Agent 112 owns automatic admissibility.
The phase-padded prefix is defined directly from `B` followed by phase letters;
it is not asserted to be the physical three-column prefix for every possible
gap of length two. Its exact local relation is sufficient for the saturation
argument and is proved for all exterior lengths.

## Reproduce

From the repository root, with official Lean 4.19.0 and new output paths:

```sh
python3 proofs/contributions/agent-110/certificate-budget/check.py \
  --lean /absolute/path/to/lean-4.19.0/bin/lean \
  --build /tmp/p196-agent110-budget-build \
  --evidence /tmp/p196-agent110-budget-evidence
python3 proofs/contributions/agent-110/review/independent_controls.py
```

The current entrypoint copies and freshly compiles the complete nineteen-module research
dependency closure, including `All`. It then uses Lean's compiled environment
to audit every kernel-safe declaration transitively. There are no admitted
proofs, new axioms, native evaluation shortcuts, or missing finite-certificate
premises in these implications. Reported foundational axioms are `propext`,
`Classical.choice`, and `Quot.sound`.

The original ten-module independent accepted run is
`../review/rebuild-bfdb7a5-final/manifest.json`; its reviewed mathematical
source matches remote `ec8f8e2a3580d061ba386cea918f49fa279385dd`. The final
reviewer driver is included in the current contribution revision. The earlier
driver's overbroad rejection of unsafe compiler-stage helpers is retained in
`rebuild-bfdb7a5`, together with the diagnosis and corrected audit mechanism.
Only the later fresh run is accepted. No mathematical axiom was whitelisted to
work around that diagnostic. The fifteen-module saturation extension is
independently accepted in `../review-saturation/REVIEW_RESULT.json`, pinned to
remote source `70b276c326989807310b9c8e61fa354411666e40`.

The Agent 112 dependency review is in `../review-agent112/`. Its original source
commit is `e7689d35f41ff325037a238cfc594d95e0da04e1`; `PROVENANCE.json` identifies
the three exact original Git blobs and source paths. The final consumer
mathematical source is `eb4817f0973cbbe2a059af33d5dc53877a5275b7`.

Independent finite semantic controls tested 192,000 source states, 596,608
legal trim triples and 182,400 literal reverse-and-add steps. They include
nonmaximal trimming, empty target exteriors and negative local increments.
These are sanity controls; the all-width results are the Lean theorems.

## Remaining work

Finish the final nineteen-module check-only independent rebuild and submit its
complete evidence to the integration owner. The two-phase period-at-least-12
target was not proved; only the all-phase lower bound of four is exported.
No valid certificate or repeatable safe integer orbit has been found here.

Development source snapshots and compiler failures are retained in the
`*-development` directories. They are evidence, not additional accepted build
roots. Reproducible build products and copied dependency caches are excluded.
