# Kernel certificate for the three-column high-return graph

`HighReturnRank.lean` passed Lean 4.19.0 with five theorem declarations.
It imports only `Std`. The finite evaluation theorem has no axioms; the
other four theorems use only `propext` and `Quot.sound`. No `sorry`,
custom axiom, or `native_decide` is used in the accepted source.

The graph has 900 vertices, encoding `(A,B,C)` with A in 10..18 and
B,C in 9..18 as `100*(A-10)+10*(B-9)+(C-9)`. Each vertex has two possible
deep-carry controls. The exact digit formulas retain 258 transitions.
The checked ranks have counts 760, 123, 14, and 3 at ranks 0 through 3.
Every retained edge stays in range and strictly decreases rank.
`no_four_edges` consequently excludes four consecutive graph edges.

The Lean kernel checks all 1,800 controls. Python only proposes the rank
function and emits source; an incorrect proposal would fail the checked
inequalities. The balanced lookup includes all 900 ranks. The graph's
transition definition is arithmetic, not a trusted precomputed edge list.
`finite_data.json.gz` retains the independent generated rows, including
rejected controls, and ranks. Recover it with
`gzip -dc finite_data.json.gz > finite_data.json`.

The intended actual-orbit reduction and the small-width cases are in the
separate `../2026-10-15-full-high-return/` written proof. **This module
does not formalize that reduction.** Its machine-checked conclusion is
the finite graph exclusion, not a standalone formal theorem about
reverse-and-add, safe consecutive returns, or the orbit of 196.

The root independently derived the digit-mod formulas and generated the
same edge and rank counts as the other research branch. Complete row
comparison and independent review are recorded separately when available.

Reproduce with Python 3 and Lean 4.19.0:

```
python generate.py
lean -j1 HighReturnRank.lean
```

`verification.json` and `compile.log` retain the successful compiler
result, exact source hash, and every axiom report. The initial unsuccessful
source is retained under `failed_attempts/`: it used an incorrect Boolean
lemma name in two proof steps. Its finite check succeeded, but its
incomplete downstream declarations were not valid verification evidence.
The accepted source fixes the lemma name and all five declarations pass.
