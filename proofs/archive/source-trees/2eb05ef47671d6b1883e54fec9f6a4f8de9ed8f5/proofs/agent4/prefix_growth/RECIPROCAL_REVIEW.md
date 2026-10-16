# Agent #4 reciprocal verification record

Agent #4 independently reviewed and rebuilt three pinned collaborator modules. The checks below establish compilation of their exact source bytes and the stated formal dependency boundaries. They do not establish external originality, independent human review, or a solution of P196.

## Exact sources and actual checks

| Module | Source commit | SHA-256 | Audited theorem declarations |
|---|---|---|---:|
| Agent #5 `proofs/agent5/ExteriorClock.lean` | `db65db3646694d95fe6a8e7a0f836d66d8e6a4c8` | `7158c8c7d07fab80c4212ba4c6c4b0a318ca22faee988c8d22eca45edfd439c5` | 30 |
| Agent #8 `proofs/contributions/2026-10-15-agent8-complementary-bulk/PeriodObstructions.lean` | `8902b2b8d5cf495d7ee407e905817e1737aae770` | `83102a949036799a929ba72d74ce9d76bc2a11cb3adf61e0bc06b6013b22991a` | 24 |
| Agent #9 `proofs/contributions/2026-10-15-agent9-complementary-bulk/ExteriorErasure.lean` | `9a8c30c0e097f3ef0cfc5c614be957f153e4b827` | `1de006bcb67eefc0feba31332ed7790813b291aa31de2c8f45de70caf6a970a2` | 28 |

All **82 declarations** passed a fresh compile and per-theorem dependency audit in Agent #4's GitHub Actions run **38686134384**, then passed another native local rebuild from that run's exact downloaded source snapshot. Both used official Lean 4.19.0, release commit `6caaee842e94`, without mathlib. Every audit was either empty or a subset of `propext`, `Classical.choice`, and `Quot.sound`. No `sorryAx`, custom axiom, or native-evaluation dependency appeared in these roots.

The checked source/audit snapshot is artifact **11950266417**, ZIP SHA-256 `9d42a9435b9ea31ecdc7c633e320cb2888e8d558d37efd185f0b102cf52668a0`. The workflow pins the source URLs and expected hashes. `verify_lean.py` records source hashes, compiler exits, every theorem audit, and log hashes; it rejects a missing audit or an axiom outside the allowlist. The artifact is temporary infrastructure; the immutable source commits, workflow, and this record retain the reproduction information.

## Mathematical review: exterior clock

Agent #5 formalizes recursive carry normalization, reversal and coordinatewise-addition sums, trim-invariant exterior mass, the phase-dependent modulo-nine clock, and its telescoping over an arbitrary exterior path. The bounded-coefficient hypothesis guarantees the final exterior carry is a bit. The unit-phase restriction is essential when inverting the phase modulo nine. It cannot be extended to phases 6 or 12 by cancelling a nonunit.

The proof of the full-cycle lower bound retains positivity, closed exterior/potential/clock paths, and even total overflow as hypotheses. Evenness comes from a full two-gap width return, not an arbitrary exterior return. Agent #2's complementary written argument also obtains individual gain divisibility by nine. Agent #4's new saturation result uses these credited restrictions to eliminate the remaining period-36 possibility.

## Mathematical review: mass and period restrictions

Agent #8 formalizes normalization modulo nine and the actual doubled mass of a mirrored digit word. It then proves the six-multiple iteration and template mass congruence. The outer potential bounds cancel only when the exterior returns; dropping their endpoint terms on an arbitrary path would be invalid.

Its nonnegative-gain short-period exclusion correctly distinguishes a returned interface from an infinitely repeatable template. Negative total gain in either gap eventually defeats repeated application even if a finite interface walk closes. The module's exterior-evolution and width-identity premises are documented rather than silently asserted as facts about every symbolic state.

## Mathematical review: exact erasure

Agent #9 proves the two different erasure mechanisms. With overflow, the erased suffix is exactly the maximal suffix over the two-letter alphabet {t,t+9}; no alternating-tail assumption is justified or needed. Without overflow, the one-column erasure bound requires a trimmed source exterior. The untrimmed source c=1, B=(1,1) is an explicit counterexample to dropping that hypothesis.

The complete binary-collapse identity leaves a singleton exterior rather than an empty one. The resulting nonempty-exterior and cycle-budget consequences are useful necessary constraints, but they do not establish that every exterior escapes or that no large cycle exists. Agent #4 retained this distinction when interpreting the accepted formal statements.

## Remaining integration boundary

All three modules formalize their explicitly defined operations and prove their declared propositions. A single theorem simultaneously linking the complementary quotient, its changing gap parameters, the actual ordinary-integer orbit, the exterior clock, and the new three-column certificate is not supplied by these three files alone. Agent #4 is separately formalizing the exact whole-word prefix projection against the repository's established canonical numeral and numeric-orbit definitions. The independent compilation reported here is complete; that broader integration is a separate research result and must not be inferred merely from successful builds.
