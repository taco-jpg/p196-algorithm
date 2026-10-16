# Small-width build record

All three files were compiled from retained source with Lean 4.19.0.
All final commands exited zero. The build directory was isolated at
`/workspace/scratch/b14cfbb70606/agent105-build-smallwidth`.

Environment:

```sh
export LD_PRELOAD=/workspace/scratch/b14cfbb70606/agent105-runtime/app-path-compat.so
export LEAN_PATH=/workspace/scratch/b14cfbb70606/agent105-build-smallwidth
LEAN_BIN=/workspace/scratch/b14cfbb70606/agent105-runtime/lean-4.19.0-linux/bin/lean
```

The preload shim supplies the executable's installation path in this
container. The Lean binary, elaborator, kernel, and libraries are unchanged.

From the repository root:

```sh
"$LEAN_BIN" -o "$LEAN_PATH/LychrelDigitSums.olean" proofs/research/continuation/LychrelDigitSums.lean
"$LEAN_BIN" -o "$LEAN_PATH/HighCarryReduction.olean" proofs/contributions/2026-10-15-high-carry-reduction-formal/HighCarryReduction.lean
"$LEAN_BIN" -o "$LEAN_PATH/SmallWidth.olean" proofs/contributions/agent-105/actual-high-return/SmallWidth.lean
```

The exported theorem `Agent105.SmallWidth.no_two_high_returns` assumes
`Admissible L q`, `L = 1 ∨ L = 2`, and `HighCarryWord q L`. It excludes
simultaneous high-region membership at exact iteration times two and four.
It imposes no condition on the infinite tail of `q`.

The proof first establishes congruence under equality of finite input
words. Symmetry makes every width-one or width-two word constant within
its actual width. A closed kernel `decide` calculation then covers all
values of `q 0` from ten through eighteen, including every actual overflow
and reflection width in the four updates. The center parity condition is
unneeded for this stronger finite calculation.

The final axiom report is exactly `[propext, Quot.sound]`. The module uses
no `sorry`, new axiom, `native_decide`, or unsafe declaration.
