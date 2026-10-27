# Agent 119 — T1: Lean length accounting

## Status 和 scope

**LEAN-VERIFIED:** formalization of the established neutral-band length-counting
argument in `calculation/neutral_band/README.md`. The unchanged Agent120 checker
accepts precisely the nonempty closed checked chains; its separate gain clause
follows from exact length accounting.

The statements cover arbitrary bases, coefficient widths, periods, 和 legal
trim counts. They require neither symmetric centers nor maximal trimming.
没有 decimal certificate is supplied. Overflow positivity 和 universal decimal
impossibility are outside this result.

Baseline: `eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`.
Coordination: [#289, claim](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6432822466).
The paper identities predate this work; the contribution is their registered
Lean formalization, checker equivalence, 和 reusable conditional corollary.

## Exact statements

Write `G = sumGam b es`, `U = sumU es`, `V = sumV es`, 和
`S = sumGain es`. `U` counts exterior neutral coefficients; `V` counts removed
center pairs. The Lean namespace is `Agent119.NeutralLengthAccounting`.

For every `Hyp b B C`:

\[
|\operatorname{nextB}(B,C)|=|B|+\gamma,\qquad
|\operatorname{nextC}(B,C)|=|C|+\gamma.
\]

For every checked edge:

\[
|B_2|+u=|B|+\gamma,\qquad |C_2|+2v=|C|+\gamma.
\]

For a checked chain starting at `(B,C)`, including an empty or open chain:

\[
|\operatorname{endB}|+U=|B|+G,\qquad
|\operatorname{endC}|+2V=|C|+G.
\]

Closing the 两个 interfaces therefore gives:

\[
U=G,\quad 2V=G,\quad S=U+V,\quad 2S=3G,
\quad G\le S,\quad G\equiv0\pmod2.
\]

The exact next-lap band parameter is `g + S - G = g + V` for every natural `g`.
These counting identities alone permit `G=0`; positivity is 不 asserted.

The main acceptance equivalence retains the original definitions:

```lean
cycleOK b es B C = true ↔
  es ≠ [] ∧ chainOK b es B C = true ∧
  endB es B = B ∧ endC es C = C
```

`lychrel_of_closed_chain` applies the existing `lychrel_of_cycle` to those
hypotheses with the original bound `2 + G ≤ g`. It is conditional on supplying
an actual closed chain, 和 does 不 construct one in base 10.

## Proof structure 和 registered endpoints

`StepLengths.lean` imports the existing `A120Certificate` module.
`Hyp.gam_le` permits the 两个 overflow cases. Existing normalization-length
lemmas make the `zipWith` inputs equal in length, proving `nextB_length` 和
`nextC_length`. `edgeOK_sound` then gives `edge_lengths` directly from the
checked list equalities.

`Main.lean` proves the chain identities by induction, using additive equations
to avoid natural-subtraction side conditions. Endpoint cancellation yields the
closed totals. The gain clause follows arithmetically, so the original Boolean
checker itself needs no edit.

The 两个 modules 和 12 theorem endpoints are registered under
`Agent119NeutralLengthAccounting` in `lean/registry.json`:

- `nextB_length`, `nextC_length`, `edge_lengths`;
- `sumGain_eq`, `chain_length_balance`, `closed_chain_totals`;
- `closed_chain_gain`, `closed_chain_even`, `closed_chain_gap`;
- `cycleOK_iff_closed_chain`, `cycleOK_totals`, `lychrel_of_closed_chain`.

## Reproduction 和 verification

With the repository's pinned Lean 4.19.0 toolchain available:

```bash
LEAN_NUM_THREADS=1 python3 tools/verify.py --changed
python3 calculation/agent-119/certificate_totals.py
```

The actual repository gate passed against `origin/main` at the baseline above:
5,219 Lean files, 302 projects; 2 changed modules built 和 replayed by
`lean4checker`; 12 endpoints audited; terminal `ALL CHECKS PASSED`.
Only `propext`, `Classical.choice`, 和 `Quot.sound` occur in the audited axioms.
No trust escape or runtime modification was used.

Direct per-file Lean runs used one thread, an 8 GiB address-space ceiling, 和
a 1,200-second timeout. `StepLengths.lean`: 0.517 seconds, 437,112 KiB peak RSS.
`Main.lean`: 1.020 seconds, 476,612 KiB peak RSS. Python `resource.getrusage`
measured child RSS because `/usr/bin/time` was unavailable. The full initial
repository gate took 48.702 seconds, peak child RSS 575,556 KiB.

**COMPUTED calibration only:** the supporting script reads the existing
Lean-source certificates through the unchanged Python mirror. The eight bases
2, 4, 8, 16, 32, 26, 11, 17 都 pass; 56 existing edges 和 504 rotated chain
prefixes satisfy the formulas. Every control has `(G,U,V,S)=(2,2,1,3)`.
The final calibration line is:

```text
CALIBRATION PASS controls=8 edges=56 rotated_chain_prefixes=504
```

These positive controls are existing certificates, 不 new Lychrel discoveries.
The general proof is supplied by the Lean modules, independently of the
finite calibration cases. A separate agent reviewed the statements, empty
chain/exterior cases, nonsymmetric centers, induction, 和 registry coverage.
