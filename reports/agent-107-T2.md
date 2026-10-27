# Agent 107 — T2.bauto-completion-audit

**Classification: COMPUTED tooling audit.** The new driver reports exterior
automaton exhaustion explicitly, preserves accepted witnesses, 和 labels depth,
state, or packing limits `UNDECIDED`. 这 result supplies neither a new
mathematical B-cycle exclusion nor a decimal Lychrel certificate.

Coordination: [claim](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6432772615).
Baseline: `eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`.

## Finding

The existing `calculation/neutral_band/structure/bauto.cpp` runs

```cpp
while(!fr.empty()&&depth<400)
```

和 subsequently prints a period-level `done`, whether the frontier emptied
or the depth limit stopped expansion. The latter path emits neither a depth-cap
diagnostic nor a distinct exit status. A key requiring more than 127 bits is
skipped with a diagnostic, followed by the same period-level `done`.
The state limit is checked only after expanding an entire layer.

`structure/pipeline.py` retains only subprocess stdout. A caller using an empty
ACCEPT list or the period-level `done` as evidence of exhaustive absence can
therefore overstate what was searched.

The regression test makes the distinction observable with a controlled copy of
the old source: change only the depth constant from 400 to 1, then use the known
positive p11 stream. The old program exits 0, prints `p=11 done`, 和 reports
zero acceptances. The guarded program reports `UNDECIDED/depth_cap`.
This demonstrates the completion-reporting defect; it does **不** show that a
published negative actually encountered the original depth-400 limit.

## Implementation

`calculation/agent-107/bauto_guarded.py` reads the existing source through its
unique `main` boundary 和 appends `bauto_driver.cpp.inc` in a temporary build.
The mathematical packing, transition, 和 accepting functions are reused.
The source 和 driver SHA-256 values appear in the output.

The replacement driver validates arguments, guards shifts/packed-key capacity,
handles a fixed g directly, 和 reports one JSON `STREAM` record per selected g.
It checks the state limit before inserting a new state, preventing whole-layer
overshoot. Acceptance at the reached depth limit is retained even though
enumeration is incomplete.

The driver 也 harvests the already discovered partial next layer when the state
cap interrupts expansion. Those witnesses remain valid while completion stays
`UNDECIDED`. `STREAM.depth` records the layer being expanded; a witness in the
partial next layer can therefore 有 a depth 1 larger.

| Status / reason | Exact meaning |
| --- | --- |
| `EXHAUSTED / frontier_empty` | Reachable frontier processed completely; inspect `accepted` separately. |
| `UNDECIDED / depth_cap` | A reached frontier remains unexpanded. |
| `UNDECIDED / state_cap` | A new distinct state would exceed the configured cap. |
| `UNDECIDED / unsupported_key` | The selected g exceeds the reused core's 127-bit supported key capacity. |
| `ERROR` | Invalid input, build failure, or runtime exception. |

Exit 0 means the **selected** streams exhausted, exit 3 means a selected stream
remains undecided, 和 exit 2 means an error. `EXHAUSTED` alone is **不** a
negative: an exhausted stream can contain accepted B witnesses. A negative
requires `EXHAUSTED` **和** an empty `accepted` array. A partition with zero
selected streams does 不 establish a negative. An externally killed process
without a complete terminal record remains undecided.

## Reproduce

From repository root:

```bash
python3 calculation/agent-107/bauto_guarded.py --build /tmp/agent107-bauto
/tmp/agent107-bauto 10 11 11 -g 11100010000 -depth 1
/tmp/agent107-bauto 10 16 16 -g 1000100010001000
python3 calculation/agent-107/test_bauto_guarded.py
python3 tools/verify.py --changed
```

The depth-1 command exits 3 with `UNDECIDED`, `reason=depth_cap`.
The p16 control returns:

```json
{"type":"STREAM","base":10,"period":16,"g":"1000100010001000","status":"EXHAUSTED","reason":"frontier_empty","states":13170,"depth":13,"accepted":[]}
```

The p16 negative was already reported by Agent 2; 这 audit uses it as a regression
control 和 does 不 claim new authorship for that mathematical scope.

## Validation

The independently authored `test_bauto_guarded.py` passes 10 tests. It compiles
the 两个 programs, compares their positive outputs, 和 replays returned B words
using separate elementary carry arithmetic.

| Control | Result |
| --- | --- |
| Old-source depth-1 fixture | Exit 0 + `done` + zero ACCEPT despite a known positive stream |
| New depth 0/1 limits | `UNDECIDED/depth_cap` |
| New state cap 1 | `UNDECIDED/state_cap` |
| p22 g consisting of 22 ones | `UNDECIDED/unsupported_key` |
| 17 malformed argument sets | Rejected before searching |
| p11 `11100010000` | 18,061 states; original e=`10100110011`, depth29, exact B witness preserved |
| p12 `100010001000` | 136,653 states; original 3 carry streams 和 depth53 witnesses preserved |
| p11 depth29 limit | Witness retained; completion still `UNDECIDED` |
| p11 state cap 10,736 | Depth29 witness retained from the partial next layer; `UNDECIDED/state_cap` at expansion depth28 |
| p16 four-overflow control | 13,170 states, exhausted, zero accepts |
| p1–5 split into 2 partitions | Same 23 necklaces/results as the unsplit run; disjoint partitions |

The original 9-test regression suite completed in 5.593 seconds. The 10-test
revision adds the partial-next-layer state-cap regression. Controls
fit comfortably inside the per-run sandbox budget. The implementation changes
completion/reporting behavior; it does **不** formally verify the underlying
position automaton. No Lean source or registry entry is changed.

## Verification status 和 limits

`python3 tools/verify.py --changed` passes for the delivered computation/report
files. Since the change contains zero Lean modules, this is repository-rule
verification, **不** `LEAN-VERIFIED` mathematics. The gate checks 5,217 existing
Lean sources / 301 registered projects 和 builds zero changed Lean modules.

The audit does **不** invalidate any earlier exclusion whose author actually
established frontier exhaustion. It supplies explicit evidence for future
exhaustion claims 和 preserves scoped positive controls. Full B/C compatibility,
arbitrary-period impossibility, 和 decimal Lychrel existence remain unresolved.
