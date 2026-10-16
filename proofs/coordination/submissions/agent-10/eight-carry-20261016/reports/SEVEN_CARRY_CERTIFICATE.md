# Agent 10: seven complete carry observations are insufficient

`Agent10SevenCarryCounterexample.lean` is a new, frozen, independently
checkable source importing only `ActualCarryObservability`. It compiled
successfully on its first attempt with Lean 4.19.0, `--trust=0`, one worker,
and asynchronous elaboration disabled.

The source SHA-256 is
`7cdc32bd5d0eff4174d1d35314ef544a7cf80532868ba38fe664cd063edb67f9`.
The successful log SHA-256 is
`e2497ea6b4f9539e885c04815c2efef8707153ee5a395a7a11fe2b3105f66739`.

## Exact counterexample

The initial ordinary integers are

```text
n = 900000058163209
m = 900000082716109.
```

Lean proves both inputs canonical at width fifteen. Their complete carry
words agree at all observation times `t < 7`, including every terminal
carry and every index `i ≤ current width`.

Their initial pair coefficients at active index two differ:

```text
leftColumns 2 = 2
rightColumns 2 = 1.
```

Their exact next integers also differ:

```text
Lychrel196.step n = 1802361908163218
Lychrel196.step m = 1801617362716118.
```

The first carry disagreement occurs at time seven. At that time, both
widths are nineteen and carry index four is in range:

```text
carry (iterPairs leftColumns 15 7).2 4 = 1
carry (iterPairs rightColumns 15 7).2 4 = 0.
```

The conclusion is that seven complete observations cannot universally
reconstruct the active initial pair vector or the next integer. The
example has no eight-word agreement, so it does not disprove reconstruction
from eight observations. No optimal universal bound is claimed.

## Proof structure and provenance

The initial digit functions are explicit fifteen-element lists, checked
against the displayed ordinary integers. The source records both complete
pair trajectories at times zero through seven, with widths

```text
[15,16,16,17,18,19,19,19].
```

Each of the fourteen adjacent-row transitions is checked by
`decide +kernel` against the unchanged `nextWidth` and `nextColumns`
definitions. The finite carry certificate checks every index through
nineteen, conditional on that index being within the current complete
carry word. `next_state_congr_upto` and `carry_congr_upto` then transport
the bounded certificates to the unchanged `iterPairs` recursion.

This bounded-row transport pattern is reused from the preserved
`agent10-count/Agent10SixCarryCounterexample.lean`, SHA-256
`b4277ca76c6ad874db41933735ae7b677990e120e0bc5be01f9c0579c882f869`.
That source and all previously frozen three-column sources remain unchanged.

`numeric_orbit_representations` connects the iterated pair representation
to canonical digit representations of the actual ordinary-integer orbits.
Thus the certificate concerns the existing decimal arithmetic semantics,
not only the explicit row lists.

The example was found by the exact width-fifteen lift scan retained in
`twice-padded-width15-001`. Its four-prefix filter remains computational
evidence with no Lean inclusion theorem. The direct counterexample proof
does not import, assume, or depend on that filter. The earlier scan receipt
and its original computational classification are preserved unchanged;
this new Lean receipt supplements them.

## Public endpoints

All names below are in namespace `Agent10SevenCarryCounterexample`.

| Endpoint | Checked conclusion |
|---|---|
| `left_canonical` | The displayed left digit function is canonical for `n` at width 15. |
| `right_canonical` | The displayed right digit function is canonical for `m` at width 15. |
| `left_widths` | The actual left width equals the recorded width through time 7. |
| `right_widths` | The actual right width equals the recorded width through time 7. |
| `widths_agree` | Both actual widths agree through time 7. |
| `seven_complete_carries` | Every complete carry word agrees at `t < 7`. |
| `initial_pair_sums_differ` | Initial pair values at index 2 are respectively 2 and 1. |
| `next_integer_values` | Both exact next-integer values. |
| `next_integers_differ` | The next ordinary integers are unequal. |
| `numeric_orbit_representations` | Canonical ordinary-orbit semantics for the pair iteration. |
| `eighth_carry_differs` | Carries at time 7, index 4 are respectively 1 and 0. |
| `initial_pair_difference_active` | Index 2 lies below width 15 and its pair values differ. |
| `first_separation_at_seven` | All preceding complete words agree, followed by an in-range mismatch. |
| `seven_carry_counterexample` | Canonical inputs, seven complete agreements, different initial pair values and next integers. |

## Verification

All five finite certificate lemmas, both canonical-input lemmas, the initial
pair statements, and the exact next-integer statements are axiom-free.
The actual-trajectory transport, numeric representation, seven complete
carry agreements, and first separation use only `propext` and `Quot.sound`.
The source has no `sorry`, `admit`, `native_decide`, custom axiom declaration,
or `unsafe` declaration.

The successful local command, executed from `agent10-semantic`, was:

```bash
LEAN_PATH=/workspace/scratch/4b20b8469eb3/agent10-semantic:/workspace/scratch/4b20b8469eb3/agent10-eight/development /tmp/p196-agent5-lean/lean-4.19.0-linux/bin/lean --trust=0 -j1 -DElab.async=false -o Agent10SevenCarryCounterexample.olean Agent10SevenCarryCounterexample.lean
```

`seven_carry_proof_receipt.json` records the exact source, log, compiler,
import closure pins, endpoint declarations, and discovery-artifact hashes.
The integration writer's canonical closure replay and the runtime
specialist's independent source/trace review are separate checks.
