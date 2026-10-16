# Prefix inverse transducer: kernel verification

`../PrefixInverse.lean` uses Lean 4.19.0 and `Std` only. The module supplies the
complete executable `SevenColumn.prefixPredecessors`, exact local relations
`NoOverflow`, `OverflowTail`, and `LongCompatible`, and the kernel theorem

```
mem_prefixPredecessors_iff :
  s ∈ prefixPredecessors p ↔ LongCompatible p s
```

Consequently `longCompatible_mem_prefixPredecessors` covers every actual
long source once the separate `ActualPrefix` bridge proves `LongCompatible`.
This file alone does not claim full-word realizability for arbitrary local
paths, nor a theorem about all trajectories of 196.

Additional kernel theorems preserve the source/target prefix length, restrict
all source sums to 0..18, and require a positive source exterior. Both
no-overflow and overflow branches are present; the overflow terminal carry
is checked even for width one. A zero-width prefix has no admissible source.

## Correction at invalid target exterior zero

The reference Python routine is used only on target states with positive
exterior. Outside that domain, its overflow initial expression maps target
`(0,)` to source `(9,)`; this is not a forward-compatible edge (the source
instead yields exterior 10 in its overflow case). The Lean implementation
therefore guards the overflow case by `0 < v ∧ v ≤ 10`. This agrees with
Python on every intended certificate target and makes the equivalence
above valid for all finite lists, without an implicit positive-target
hypothesis. Checkpoint 01 retains the initial completeness-only version
before this strengthening. Checkpoint 02 is the strengthened exact version.

## Retained evidence and replay

- `checkpoint-01/`: first compiling module and axiom audit (completeness only).
- `checkpoint-02/`: exact inverse iff, boundary bounds, compiling audit.
- `compile-initial.log`, `compile-exact-01.log`: original compiler output.

Replay from any directory with the Lean 4.19.0 toolchain:

```
lean PrefixInverse.lean
```

The accepted theorem audits contain only `propext`, `Classical.choice`, and
`Quot.sound`. There is no `sorry`, `admit`, `native_decide`, `Lean.ofReduceBool`,
or new axiom in the accepted source.

## Four-choice optimized inverse

`../FastInverse.lean` imports the stable `PrefixInverse` module. At each column
it enumerates only the next low/high carry pair, so there are four candidate
branches. The source sum is recovered from the equations and every candidate
is checked against the original equations. Exact recovery is kernel proved
by `noCandidate_eq` and `overflowCandidate_eq`; no finite table is trusted.

The accepted statements are:

```
longCompatible_mem_fastPrefixPredecessors :
  LongCompatible p s → s ∈ fastPrefixPredecessors p
mem_fastPrefixPredecessors_iff :
  s ∈ fastPrefixPredecessors p ↔ LongCompatible p s
fastPrefixPredecessors_mem_iff :
  s ∈ fastPrefixPredecessors p ↔ s ∈ prefixPredecessors p
```

The failed first optimization draft and its compiler log are retained as
`failed-fast-01.lean` and `compile-fast-01.log`. Its two incomplete simp
branches are historical failed evidence, not accepted declarations; the
`sorryAx` reported there is Lean's placeholder for those failed branches.
Both branches were fixed in `FastInverse.lean` by applying the candidate
identity before simplification. `compile-fast-02.log` and `fast-axioms.log`
record the successful version without `sorryAx`.

## Runtime comparison, separate from kernel proof

`runtime_crosscheck.py` derives all 58,500 seven-column nodes from the retained
739 certificate, runs either Lean executable, and compares each full result
with the original Python inverse. Both implementations produce 68,152 unique
long inverse edges and no duplicate entries. Their serialized output is
byte-for-byte identical. These are implementation/performance diagnostics;
the formal theorem does not rely on Python, JSON, or runtime checks.

| Executable | Elapsed seconds | Result |
|---|---:|---|
| Original 38-choice | 23.43 | PASS |
| Optimized 4-choice | 4.96 | PASS |

The runtime summaries contain the toolchain version, input certificate hash,
raw and compressed output hashes and byte counts, and lossless recovery
commands. Both full outputs are retained as `.txt.gz`. Runtime is indicative
of this shared environment and is not a performance guarantee.

Example replay after compiling `PrefixInverse.olean` and `FastInverse.olean`
into a clean directory `BUILD`:

```
python inverse/runtime_crosscheck.py /path/to/lean BUILD original
python inverse/runtime_crosscheck.py /path/to/lean BUILD fast
```

## Stable final source hashes

- `PrefixInverse.lean`: `0a93622752fa22cf6c8de2efc8500dc313498d59831bb0e5381b3b351e0ab03e`
- `FastInverse.lean`: `585cb4d197479714edbdbe147c2c1c489742fa0f8eb978571abdc602eada4eee`

`inverse/controls-snapshot.lean` is the stable original inverse immediately
before optimization; the main module has the same bytes. The accepted
`prefix_196_has_no_predecessors` theorem uses ordinary kernel `decide` and
has no axioms. It refers to the three source-sum entries `(1,9,6)`, not the
integer 196, whose raw symmetric-sum word is `(7,18,7)`.
