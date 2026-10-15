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
