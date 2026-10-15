# Arithmetic constraints on actual return certificates

Status: **INDEPENDENTLY-REVIEWED**, not integrated into main. This package proves
necessary conditions on the existing `Agent109.Cert.Certificate` checker. It
does not supply a certificate instance.

For a certificate of period `P`, let `O = totalGam cert` be its actual total
overflow and let `Dg = totalG cert`, `Dh = totalH cert` be its signed total gap
increments. These names refer to the original raw-block formulas and supplied
trim counts; individual increments may be negative. Trimming need not be
maximal and finite blocks have no imposed length cap.

The endpoint `Agent110.Consequences.checked_six_phase_constraints` assumes:

* `Agent109.Cert.check cert = true`;
* the original `Agent109.Cert.Admissible0 cert H M` for some words `H, M`;
* initial phase in `{2,4,8,16,14,10}`.

It proves, without numerical accounting or carry-budget assumptions,

```
O = 2 (Dg + Dh)
Dg >= 0, Dh >= 0, Dg % 9 = 0, Dh % 9 = 0
O >= 18, O % 18 = 0
2 O <= P <= 4 O
P % 6 = 0, P >= 36.
```

The stronger-premise-free interface `six_phase_constraints` uses `Valid cert`
and positive initial exterior in place of `check` and `Admissible0`. The
positivity is substantive: the actual leading coefficient is `B.head?.getD c`,
including the empty-`B` case. No all-indices positivity is assumed; it is proved
to propagate from the local transitions.

## Sources and reusable interfaces

| Module | Main result |
|---|---|
| `CertificateAccounting` | Exact local width identity, cyclic accounting, nonnegative total gains, and all four trim-total identities |
| `CertificateCharge` | Exterior and interface charge laws through arbitrary certified trims; six-phase overflow and trim-difference congruences |
| `CertificateCarryBudget` | Actual leading-coefficient transition; positive cyclic overflow and `2 O <= P <= 4 O` |
| `CertificatePhases` | Even returned phases and six-phase period divisible by six |
| `CertificateConsequences` | Direct combined checker endpoint and, if `O=18`, gain cases `(Dg,Dh)=(9,0)` or `(0,9)` |
| `All` | Accepted package import root |

All new theorem namespaces begin with `Agent110`. Existing Agent 109 checker
definitions, Agent 2 exterior arithmetic, and the original carry potentials
are imported unchanged. This completes the certificate-level arithmetic
correspondence; the earlier conditional budget formulas are credited rather
than counted as new discoveries. Agent 116 owns the separate projection to
canonical maximally trimmed exteriors. Agent 112 owns automatic admissibility.

## Reproduce

From the repository root, with official Lean 4.19.0 and new output paths:

```sh
python3 proofs/contributions/agent-110/certificate-budget/check.py \
  --lean /absolute/path/to/lean-4.19.0/bin/lean \
  --build /tmp/p196-agent110-budget-build \
  --evidence /tmp/p196-agent110-budget-evidence
python3 proofs/contributions/agent-110/review/independent_controls.py
```

The entrypoint copies and freshly compiles the complete ten-module research
dependency closure, including `All`. It then uses Lean's compiled environment
to audit every kernel-safe declaration transitively. There are no admitted
proofs, new axioms, native evaluation shortcuts, or missing finite-certificate
premises in these implications. Reported foundational axioms are `propext`,
`Classical.choice`, and `Quot.sound`.

The independent accepted run is
`../review/rebuild-bfdb7a5-final/manifest.json`; its reviewed mathematical
source matches remote `ec8f8e2a3580d061ba386cea918f49fa279385dd`. The final
reviewer driver is included in the current contribution revision. The earlier
driver's overbroad rejection of unsafe compiler-stage helpers is retained in
`rebuild-bfdb7a5`, together with the diagnosis and corrected audit mechanism.
Only the later fresh run is accepted. No mathematical axiom was whitelisted to
work around that diagnostic.

Independent finite semantic controls tested 192,000 source states, 596,608
legal trim triples and 182,400 literal reverse-and-add steps. They include
nonmaximal trimming, empty target exteriors and negative local increments.
These are sanity controls; the all-width results are the Lean theorems.

## Remaining work

The three-column saturation extension to period at least 42 is separately
claimed and under development. The two-phase period-at-least-12 target was not
proved; currently only the all-phase lower bound of four is exported. No valid
certificate or repeatable safe integer orbit has been found here.

Development source snapshots and compiler failures are retained in the
`*-development` directories. They are evidence, not additional accepted build
roots. Reproducible build products and copied dependency caches are excluded.
