# Agent #1: verified Lean status

## Accepted finite witness

`SafeHighWitness.lean` compiles with official Lean 4.19.0. All five printed
transitive axiom sets are empty. Source SHA-256:
`456a80a2e5397b7005028129b4f8b56914ac39e5ff53ab67ad5fad1e8ab14a9c`.

Both a local rebuild and CI run **38682618951** passed. CI source commit:
`ec5994cc1a334e14e545bd3c59a48f377565d28c`. The earlier failed source at
`13594a41c4a08ccbf3ac9bb12795b2914f997421` remains unaccepted and is retained
in Git history with its failure record. The repaired extractor uses
structural recursion, not native_decide or a fixed decimal-width limit.

## Accepted all-parameter family

`SafeHighFamily.lean` compiles locally against a freshly compiled
`SafeHighWitness.olean`, using only the exact supplied source and Std.
All **70 named supporting theorem declarations** were inspected using
`FamilyAudit.lean`. Each transitive axiom set is a subset of
`{propext, Quot.sound}`. There is no sorryAx, custom axiom, Classical.choice,
or Lean.ofReduceBool in the printed audits. Declaration counts are audit
metadata, not counts of independent major discoveries.

The accepted endpoints are `safe_three_returns_family` and
`seed_closed_form`. Together they certify three safe high-region returns
for every `81*10^(m+7)-1`, m>=0. The file includes the canonical digit,
normalization, reflection, and ordinary-natural-number semantic bridge.
No unproved realization or finite certificate is a hypothesis.

Source SHA-256:
`7207fd6f418f88f3eec6e16543aebb9a724e77a23c314efb8329930e125d8d05`.
Audit source SHA-256:
`69ebca4e25f628be89f4987b739d6f66de219bed9d4f92b69e3e2eea262ee7db`.
Audit output SHA-256:
`30f4fbacacff20a1dcc7a6ed3e084c0aa699796aeba14b2c8dc366e1d416e8d9`.

## Compiler and reproduction

Compiler output:
`Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)`.
The local runtime came from Agent #7's artifact 11948836175. Its ZIP hash
matched `d0f9da76ef720316407b6e905a28a8519dc725c0553408379a125dbe16ac523d`;
the contained official Lean release archive matched
`6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe`.
Runtime binaries and compiled objects are reproducible infrastructure and
are not part of the research-source contribution.

In a fresh directory containing the three supplied Lean files:

```sh
lean -j1 -o SafeHighWitness.olean SafeHighWitness.lean
LEAN_PATH=. lean -j1 -o SafeHighFamily.olean SafeHighFamily.lean
LEAN_PATH=. lean -j1 FamilyAudit.lean
```

The successful local witness and family axiom logs are retained alongside
the sources. The all-width family was not part of the earlier finite-only
CI run; no CI result is being attributed to an untested source revision.

The minimality exhaustion remains computationally checked, not Lean-certified.
The existing general three-return upper bound retains its separate written
bridge / finite-kernel-certificate distinction. No proof of P196 follows.
