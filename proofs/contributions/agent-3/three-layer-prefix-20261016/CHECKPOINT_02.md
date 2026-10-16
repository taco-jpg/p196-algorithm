# Complete mathematical source checkpoint

The four new modules are complete and frozen. All 52 explicit declarations
passed author compilation and literal axiom reports under Lean 4.19.0,
commit `6caaee842e94`, with `--trust=0`. The full dependency closure is
reused from reviewed source `89287c9d3eb7dd801c2b1a59eff03140d47d24ec`.

| Module | Explicit declarations | SHA-256 |
|---|---:|---|
| DeadPrefix | 15 | `09c01111e2eb2f57637fe7d3a04e45aca4ca3d20c0248dc349e956c6ffc1fc64` |
| ActualDepth | 14 | `dcc9655c0fe9f60419fc60b821e225f705f3ce713792419586d623125ca9d0e2` |
| SharpHistoryFamily | 16 | `6e3b02999b118ed00133d7bebdbf553a6f19d6bfaec4f6abbf982ab7ee2fb002` |
| SharpHistoryTheorem | 7 | `d6afdf3e252b1b223ad30548ba6f72a3ba17604dfba43563ea28a5a9435a2f29` |

The main entry point is
`P196.Agent3.ThreeLayer.finite_horizon_exact_two_history_family`.
For every `m : Nat` and `k > 0`, it gives two duplicate-free coefficient-word
lists of length `2^m`, each at width `2*(m+k+10)`. The actual two-step image
of the initial enumeration equals the protected enumeration. Every protected
word has two original `ActualFiber` layers and has no three such layers.
The relation retains bounded coefficients, equal half widths, zero computed
carry, and the unchanged full-word step equality.

Every initial coefficient word has a positive canonical ordinary realization.
For every such realization, the actual integer orbit avoids palindromes at
all times from zero through `k+3`, inclusive, and its time-four value is
`digitValue (target (m+9) k)`. A bounded mirrored candidate of the same width
and with zero computed final carry cannot be an additional predecessor of
the initial word. `sharp_initial_canonical_chain` separately exposes the
canonical three-word chain, equal widths, and successive carries `0,0,1`.

The generic `no_three_paths_dead_prefix` and `no_three_actual_fibers` retain
an arbitrary suffix after `[14,14,14,5]`. The specialized ancestry statements
also hold at `k=0`; positive `k` is required for the separate safety and
overflow-target conclusions.

All 52 explicit declaration reports contain only subsets of `propext`,
`Classical.choice`, and `Quot.sound`; the dead-prefix contradiction itself
uses only `propext`. Failed author attempts are retained alongside the
successful exact sources and commands. Historical source identities and
original bytes are preserved under `source-preservation/`; its generator
was not rerun.

At this checkpoint, independent semantic review and one separate fresh
27-module rebuild, plus the canonical 27-module portable verification,
are being completed. This source checkpoint is author LEAN-CHECKED and
does not claim those subsequent executions have finished. The README's
earlier first-checkpoint wording is superseded by this complete source
record while the final verification documentation is being prepared.

The result concerns the specified finite, all-zero-carry ancestry relation
and a horizon-dependent family. It does not exclude mixed-overflow histories
or establish an infinite ordinary orbit. Agent #3 holds no main-write slot.
