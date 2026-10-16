# Normalized carry and original certificate accounting

Agent #6, task `agent6-normalized-carry-accounting-20261016`.

## Purpose and current status

The existing certificate coordinate balance evaluates the maximally trimmed
exterior of each listed state. The original certificate accounting instead
uses `gam` on the raw exterior word. This contribution supplies the compatibility
needed to use those two results together.

The source baseline is the reviewed PR115 head
`dca30e76474569a276c2e58bbd6ee0b96c554ecc`. The exact-head task claim succeeded at
`1bd2354c2447febf38df9b69fb670e988abfc72a`, with parent
`47e808147f5f0a0dc5ec7340b062112018288c32` and readback blob
`6642f91e3a0a9898a150240b919d2b110d07a1b6`. Four earlier stale-head attempts are
retained in the scope receipt; none reserved ownership or started proof work.

**Author-checked source checkpoint.** All three mathematical sources are frozen.
Their sixteen public theorems have passed Lean 4.19.0 kernel compilation and
literal axiom audits, with only the standard three permitted axioms in their
combined dependencies. The structural module passed its first attempt; the
accounting module passed its third after two retained rewrite failures; the
controls passed both their initial and final-import builds. Full independent
execution and exact published-source review have not yet completed.

## Exact interfaces

`NormalizedCarry.lean` consumes Agent109's existing `normalize7_eq`,
`norm_band_tail`, `norm_append`, and `stripSuffix_spec`. Its raw `gam_eq_overflow`
is a correspondence consumer, not a new normalization theorem. It proves the
following carry-preservation interface with either of two independent premises:

```text
overflow c (stripSuffix c B) = overflow c B
```

One premise is `c ≤ 18`, allowing arbitrary natural coefficients in `B`. The
other is `Agent109.Bounded B`, allowing every natural phase `c`. The actual strip
definition is `P196.Agent7.Finite.stripSuffix`; Agent109's namespace provides its
existing decomposition theorem.

`CertificateCarryAccounting.lean` uses bounded raw `B` to identify

```text
overflowBit (Agent116.CertificateExterior.stateOuter s) = Agent109.Cert.gam s.
```

Neither the phase nor the interior words `A` and `C` need further restrictions.
For exactly the listed rows, their indicator sum then equals the unchanged
`Agent110.Accounting.totalGam`. The generic sum interface only requires the
listed raw exterior words to be bounded. The original checker supplies these
bounds and the prior coordinate balance, giving

```text
sumPrefix (weightedPhase ∘ rowOuter cert) cert.P
  = 9 * sumPrefix (weightedReverse ∘ rowOuter cert) cert.P
      + 9 * totalGam cert.
```

The checked gain version replaces the last term by
`18 * (totalG cert + totalH cert)`, by consuming Agent110's existing
`totalGam_eq_twice_gains`. This is an interface composition of existing balances,
not a second proof or discovery of the gain accounting.

## Boundary controls

`CarryControls.lean` evaluates original `State` values with empty interior words.
Its exact controls distinguish a numerical carry from its nonzero indicator.

| Phase and raw word | Trimmed word | Raw carry | Trimmed carry | Trimmed indicator |
| --- | --- | ---: | ---: | ---: |
| `19`, `[19]` | `[]` | 2 | 1 | 1 |
| `2`, `[20]` | `[20]` | 2 | 2 | 1 |
| `18`, `[18]` | `[]` | 1 | 1 | 1 |
| `9`, `[9]` | `[]` | 0 | 0 | 0 |
| `0`, `[0]` | `[]` | 0 | 0 | 0 |
| `19`, `[18]` | `[18]` | 1 | 1 | 1 |

The first row formally refutes unconditional numerical carry preservation. The
second formally refutes indicator-equals-carry without coefficient bounds,
including when the original permitted-phase predicate is kept. A completely
trimmed empty word retains its incoming carry; it need not have carry zero.

## Reproduction and attribution

The exact inherited closure has eighteen modules through
`CertificateCoordinates`; the final three new modules give twenty-one. It does
not import the earlier filter/control modules, Agent2's charge package, or the
experimental PR107 recurrence sources. `carry.registry.json` and
`DEPENDENCIES.json` pin every accepted source byte and declared import.

The replay command, after the source checkpoint is frozen, is:

```bash
python3 proofs/contributions/agent-6/normalized-carry-accounting-20261016/replay.py \
  --lean /absolute/path/to/lean-4.19.0-linux/bin/lean \
  --output /absolute/path/to/new-carry-replay
```

The pinned repository verifier remains unchanged. Its scoped fresh build is
followed by literal `#print axioms` checks with `--trust=0`; the separate
independent reviewer also performs a complete fresh trust-zero closure build
and module-origin theorem/safe-definition audit. Only `propext`,
`Classical.choice`, and `Quot.sound` are permitted in accepted proof dependencies.
Generated implementation constants are separately inventoried. No
`native_decide`, `sorryAx`, new axiom, or external proof oracle is accepted.

The genuine landscape specialist authors the structural module; the claims
specialist authors the controls; Agent #6's parent authors the accounting
consumer and is the sole Git writer. The runtime specialist authors none of
these modules and reviews them independently within the same session. Shared
authentication does not imply an external reviewer or separate account.

The upcoming evidence checkpoint retains the complete scope archives, source
and ownership census, independent review planning, and fresh execution results.
Author attempts already appear under `verification/author/`; every failed
attempt is separate from the accepted source and is excluded from the registry.

## Mathematical limits

The checker-facing statements retain `check cert = true`. They supply no
accepting certificate, converse criterion, positive overflow-existence result,
new recurrence, period bound, cap exclusion, ordinary-integer realization, or
infinite palindrome-avoiding orbit. The question for 196 remains unresolved by
this contribution. Other agents retain the recurrence, two-step boundary,
general arithmetic correspondence, and all-base carry scopes recorded in the
task claim.
