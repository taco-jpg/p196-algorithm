# Carry boundary controls: author verification

The seven public controls pass the pinned Lean 4.19.0 kernel at trust level zero.
The final source imports `CertificateCarryAccounting`, bringing the structural
carry and certificate accounting modules into the registry root. Only this
import changed after the first successful control build; the theorem bodies
are byte-identical to that earlier attempt.

## Exact mathematical content

All examples use `controlState c B = { c := c, B := B, A := [], C := [] }`.
These are original row values, with no assertion of an accepted certificate.

| Phase | Raw B | Stripped B | Raw gam | Stripped carry | Stripped indicator | Purpose |
| --- | --- | --- | ---: | ---: | ---: | --- |
| 19 | [19] | [] | 2 | 1 | 1 | Unrestricted carry invariance fails; the raw indicator is also 1. |
| 2 | [20] | [20] | 2 | 2 | 1 | Permitted phase and unchanged stripping do not remove the coefficient-bound requirement. |
| 18 | [18] | [] | 1 | 1 | 1 | The empty word retains incoming carry one. |
| 9 | [9] | [] | 0 | 0 | 0 | Neutral phase is a meaningful zero-carry boundary. |
| 0 | [0] | [] | 0 | 0 | 0 | Zero phase and zero coefficient are included. |
| 19 | [18] | [18] | 1 | 1 | 1 | A bounded exterior works above phase eighteen. |

The first two controls explicitly prove raw carry 2. The latter four use
coefficients within the existing bound of eighteen. Their exact conjunctions
are in the frozen source; auxiliary zero-carry table entries are definitional
reductions of the same empty words and incoming phase carry.

The negative theorem `unrestricted_strip_carry_invariance_false` proves:

```text
not (forall c B, overflow c (stripSuffix c B) = overflow c B).
```

The combined theorem `indicator_eq_gam_without_bounded_false` proves both:

```text
not (forall s, overflowBit (stateOuter s) = gam s),
not (forall s, Phase s.c -> overflowBit (stateOuter s) = gam s).
```

These are failures of unrestricted identities. They do not contradict the
bounded-state interface, establish a cycle, or produce an accepted certificate.

## Source and trust evidence

- Source: `/workspace/scratch/f8aedc6d7adf/agent6-carry/proofs/contributions/agent-6/normalized-carry-accounting-20261016/CarryControls.lean`
- Source SHA256: `abac509aeef647003b9cc5d78ceecd5a9536b907285449d6dea9aa408ed333fb`
- Git blob SHA1: `9a7e155e0a53494067b15da77ff0d1da47c5eec0`
- Source bytes: 4446
- Claim coordination: `1bd2354c2447febf38df9b69fb670e988abfc72a`
- Claim blob: `6642f91e3a0a9898a150240b919d2b110d07a1b6`
- Public theorem declarations and literal `#print axioms` receipts: 7 each
- Explicit private theorem declarations: 0
- Full module-origin theorem constants: 18
- Full module-origin safe definitions: 1
- Separately recorded compiler unsafe implementations: 2
- Axiom union for all safe audited declarations: `Quot.sound, propext`
- Retained actual attempts: 3; failed attempts: 0

The compiler binary SHA256 is `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.
Every invocation uses `--trust=0 -j1 -DElab.async=false`. The initial pass uses
the inherited eighteen objects that runtime matched to its existing successful
review; unchanged baseline modules were not recompiled here. The final pass
adds the freshly built structural and accounting objects. Exact paths, object
hashes, commands, source snapshots, and elapsed times are retained in each
`verification.json`. Raw compiler logs are unchanged.

The source-level receipt checks all seven literal exports. `CarryControlsAudit`
selects every theorem and definition by its actual imported module origin,
includes generated theorem constants, rejects nonstandard axioms in safe
declarations, and records compiler unsafe implementations separately. This is
an author audit; runtime's independent combined review is a distinct gate.

`check_controls.py` records each actual execution in a fresh attempt directory.
`finalize_review.py` only summarizes existing receipts and hashes; it does not
invoke Lean. Compiled objects are retained locally for dependency use but
excluded from the portable evidence manifest.
