# Agent #105 / session 9df76b: complete numerical inverse decoder

Task `agent105-9df76b-numeric-decoder-20261016` was successfully claimed and read back on `p196/coordination` at `2873e4a2fa49854d8c6b4b77d972f15ff1253527`. The isolated branch is `research/agent-105/numeric-decoder-9df76b-20261016`, based on the preceding inverse-boundary source checkpoint `5923015f86eb1ef898becd77ce2ee328ff338b69`.

The mathematical source is the previously retained `persist_inverse_notes.txt`, section 6, Git blob `ecd101823b261fdac15d185fea963d9c9f16c601`. This is a formalization of that written numerical decoder. Existing folded trace, actual carry, canonical realization, and fixed-width profile uniqueness theorems are reused. The target is the complete ordinary integer output of `Lychrel196.step`; it is different from the existing inverse relations for `nextColumns` prefixes.

## Incremental checked interfaces

`Agent105DecoderLocal9df76b` supplies an executable solver for the two physical equations `q+a=u+10*aNext` and `q+bNext=v+10*b`, with coefficient at most 18 and next carries at most 1. It proves local uniqueness, full `some` soundness/completeness, and exact `none` rejection. The corresponding odd-center solver checks an even coefficient at most 18 and its full carry equation. These specifications hold for arbitrary natural inputs; any truncated subtraction is followed by the complete arithmetic equality checks.

`Agent105DecoderTarget9df76b` supplies the actual-number connection. `PayloadSpec` uses the unchanged `Admissible`, `output`, and `carry`. `WidthChoice` handles either source width equal to target width and carry 0, or a one-digit larger target with leading digit 1 and carry 1. `positive_predecessor_iff_finite_payload` proves exact existence equivalence between a finite accepted physical payload and a positive canonical ordinary integer predecessor at the specified source width. In particular, the overflow payload may have zero as its most significant remaining digit, as in `5 -> 10`.

All twelve current public theorem endpoints have actually compiled under official Lean 4.19.0, release `6caaee842e94`, with explicit `--trust=0`. Literal axiom reports use only the standard three logical axioms. The pinned eight-module closure is `proofs/Agent105NumericDecoder9df76b.registry.json`, project `agent105-decoder-checkpoint-9df76b`. The first local-solver attempt and first target-interface attempt failed for proof/API issues; their exact source and logs remain retained and are excluded from the registry. The later attempts passed.

The complete scanner and executable numerical acceptance iff are still WIP at this checkpoint. Its eventual scanner specification requires that input payload digits are at most 9; the canonical numerical wrapper supplies this premise. No whole-decoder theorem, independent full-closure replay, or integrated result is claimed yet. The finite scanner, final wrapper, concrete controls, and independent audit are the next obligations.

## Coverage

All substantive development snapshots, failed and successful compiler logs, and receipts published at each checkpoint are retained under this contribution. Reproducible `.olean` objects and duplicate build caches are excluded. The file inventory records the published bytes; full source pins for imported modules are in the registry. The original dependency authorship and preceding branch history are preserved.

This contribution makes no assertion about an infinite reverse-add orbit or the status of 196.
