# Agent 104 — exterior clock bounds for the exact neutral checker

**Status: LEAN-VERIFIED.** The literal changed-file gate passes, including
kernel replay of both new modules 和 the allowed-axiom audit of nine endpoints.

## Result 和 precise scope

The target endpoint applies directly to the existing executable predicate,
without changing `Agent120.Neutral.edgeOK`, `chainOK`, or `cycleOK`:

```lean
theorem Agent104.NeutralExteriorBounds.cycle_bounds
    (es : List Agent120.Neutral.Edge) (B C : List Nat)
    (h : Agent120.Neutral.cycleOK 10 es B C = true) :
    0 < Agent120.Neutral.sumGam 10 es ∧
    2 * Agent120.Neutral.sumGam 10 es ≤ es.length ∧
    es.length ≤ 4 * Agent120.Neutral.sumGam 10 es
```

Thus every accepted decimal neutral cycle of period P 和 overflow total G
has positive G 和 satisfies 2G<=P<=4G. The theorem permits empty exteriors,
arbitrary B/C widths, arbitrary natural neutral trims, 和 nonprimitive cycles.
No separate center-symmetry or carry-itinerary premise is added.

This formal integration does not prove that any decimal certificate exists
or that the neutral format is impossible. The stronger G>=6 result in
[PR #334](https://github.com/taco-jpg/p196-algorithm/pull/334) remains a
PAPER reduction plus COMPUTED automaton exhaustion; it is not formalized here.

## What is new

The scalar clock inequalities are prior work. The existing
`P196.Foundations.PeriodObstructions` already proves
`Agent8.exterior_bounds` using its finite potential certificate.
The original `Agent109.Cert.Certificate` also has a separate carry-budget
bridge in `Agent2SaturatedProfile/CertificateCarryBudget.lean`.

This change proves the missing direct connection from the A120 neutral
checker to those same scalar potentials. It reuses the old functions 和
theorem instead of copying their finite certificate or changing a transition.
The formalization is distinct from Agent 119's neutral length/evenness/gain
accounting 和 from the alternating-overflow family work of Agents 106/109.

## Proof structure

Define `effectiveHead B := B.headD 9`. The default 9 represents the neutral
continuation when B is empty. A legal nonempty B has a positive head <=18;
the empty default also satisfies those bounds.

For a nonempty B=x::xs, normalize the reversed tail `xs.reverse` with the
actual incoming upper-band carry. Its outgoing carry c is a bit. The
existing normalization equations then give exactly

\[
\gamma=\operatorname{overflow}(x,c),\qquad
x'=\operatorname{nextExterior}(x,c).
\]

For B=[], the flip condition forces e2=1. The raw successor is [10],
agreeing with the scalar edge 9->10 under carry1.
Removing any number of trailing neutral9 coefficients preserves `headD 9`,
even if the entire exterior disappears. Thus every checked edge projects
to the scalar map, with its actual overflow bit 和 target effective head.

Apply `Agent8.exterior_bounds` to obtain the two edge inequalities. Direct
induction over `chainOK` telescopes them into

\[
2G\le P+U(x_0)-U(x_P),\qquad
P\le4G+L(x_0)-L(x_P),
\]

where U,L are the imported upper/lower potentials. Closing the exterior
cancels both endpoint potentials. A nonempty chain has P>0, so P<=4G
forces G>0. Center return 和 the gain test are unnecessary for this bound,
although the final endpoint accepts the full unchanged `cycleOK` premise.

## Registered modules 和 endpoints

The new project is `Agent104NeutralExteriorBounds` in `lean/registry.json`.

| Module | Endpoint | Role |
|---|---|---|
| Head | `effectiveHead_bounds` | Positive bounded head, including empty B |
| Head | `edge_head_bridge` | Actual checked edge follows the existing scalar map |
| Head | `edge_potential_bounds` | Imported potentials hold on each checked edge |
| Clock | `chain_potential_bounds` | Open-chain inequalities with endpoint potentials |
| Clock | `closed_chain_bounds` | Exterior return implies 2G<=P<=4G |
| Clock | `closed_chain_positive` | Nonempty exterior return implies G>0 |
| Clock | `cycle_bounds` | Full original checker endpoint |
| Clock | `low_overflow_period` | G<=4 implies P<=16 for the computed census reduction |
| Clock | `zero_overflow_rejected` | Executable checker rejects G=0 |

Endpoint names use the prefix `Agent104.NeutralExteriorBounds.`.
The files are `lean/P196/Agent104NeutralExteriorBounds/Head.lean` 和
`lean/P196/Agent104NeutralExteriorBounds/Clock.lean`.

## Reproduction

Use stock Lean4.19.0, core + Std, with the toolchain's `lean` 和 `lake` on PATH.
From the repository root:

```bash
python3 tools/verify.py --changed
```

For individual file resource checks, run from the repository root after the
imports build. The helper uses one Lean thread, a 1,200-second wall/CPU budget,
an 8 GiB address-space limit, 和 Linux child peak-RSS accounting:

```bash
python3 calculation/agent-104/measure_lean.py lean/P196/Agent104NeutralExteriorBounds/Head.lean --hard-as
python3 calculation/agent-104/measure_lean.py lean/P196/Agent104NeutralExteriorBounds/Clock.lean --hard-as
```

Baseline: `eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`.
Stock Lean4.19.0, commit `6caaee842e94`, core + Std. The official
Lean4Checker v4.19.0 source is commit
`e11f65c651edd58d68ba260015d2bfde5102cd7f`.
The executed command was `LEAN_NUM_THREADS=1 python3 tools/verify.py --changed`:

```text
[rules] 5219 Lean files, 302 projects, OK
[changed] against origin/main: 2 new/changed Lean file(s); building 2 module(s); auditing 1 project(s)
[build] OK
[kernel replay] 2 module(s) re-checked by lean4checker
[axioms] 9 endpoints checked
ALL CHECKS PASSED (changed files only, against origin/main)
```

Every endpoint uses only the permitted `propext`, `Classical.choice`, 和
`Quot.sound` axioms. An independent reviewer checked the empty-B case,
arbitrary suffix trims, chain induction, precise hypotheses, 和 registry scope.

| File | Wall seconds | CPU seconds | Peak RSS (KiB) | Result |
|---|---:|---:|---:|---|
| Head.lean | 1.322147 | 1.010552 | 442840 | PASS |
| Clock.lean | 0.993447 | 0.848196 | 452396 | PASS |

Both runs used one CPU affinity, `LEAN_NUM_THREADS=1`, the hard 8 GiB
address-space limit, 和 the 1,200-second CPU/wall limits. Each exited 0;
the helper would fail on a timeout, nonzero exit, or exceeded budget.
