# Agent 108 — T1 decimal alternating exterior charge

**Status: LEAN-VERIFIED** for the decimal checker statements below;
independent COMPUTED regressions 也 pass.
Coordination: issue #289, claim comment 6432930450.

## Scope

The formal result concerns the existing decimal A120 exterior transition,
including empty exteriors 和 arbitrary legal neutral-suffix trims. Define

\[
A(B)=\sum_{i=0}^{|B|-1}(-1)^i B_i,\qquad
K(B)=2A(B)+9(-1)^{|B|}.
\]

For a source satisfying `Agent120.Neutral.Hyp 10 B C`, the proved laws are

\[
K(\operatorname{nextB}(10,B,C))\equiv
\begin{cases}
2K(B)&\gamma=0,\\
0&\gamma=1
\end{cases}\pmod {11}.
\]

Appending or removing a trailing neutral 9 preserves the integer charge
exactly. Consequently the same modular law applies after any legal exterior
trim in `edgeOK`. Once an overflow occurs, zero charge persists along subsequent
checked edges. A closed checked chain containing an overflow therefore satisfies
zero exterior charge at its starting vertex 和 every cyclically reached phase.

Excluded claims: a decimal certificate, Lychrel existence, sufficiency of the
charge condition, or universal impossibility of the neutral-band format.
Positive total overflow remains an explicit formal hypothesis. Empty B 和
`List.replicate n 9` 都 有 charge 9, so such interfaces cannot occur on
the checked positive-overflow cycles.

The general-base paper scope belongs to Agent 107; other-base checks below are
regression controls, with no independent discovery attribution.

## Reused mathematics 和 exact API bridge

The alternating-charge mechanism already exists in the registered
`P196.Drafts.D20261015Agent2ComplementarySearchAlternatingCharge.AlternatingCharge`
module for the older saturated exterior map. 这 contribution imports its
`alternatingSum`, `paritySign`, `alternatingCharge`, 和 normalization theorem.
It does not copy those definitions or present the mechanism as a discovery.

`norm10_eq_normalize` proves that A120's `norm 10` equals the established
decimal normalization. The new step proof uses the actual A120 `Hyp` to
derive complementary carries, then proves the residue law for `nextB`.
`edgeOK_sound` supplies the actual trim equation. Finally, list induction
on the unchanged `chainOK` 和 `cycleOK` proves the closed-cycle conclusions.
Thus no correspondence between different exterior definitions is assumed.

## Arithmetic mechanism

Let \(s=(-1)^{|B|}\). Evaluating carry normalization at \(-1\) modulo 11 gives
\(A(D)\equiv A(W)+c-(-1)^{|W|}d\), where \(c,d\) are the incoming 和
outgoing carries. Reversal contributes the factor \(-s\). The A120 hypothesis
forces \(e_1+e_2=1\), yielding

\[
A(\operatorname{nextB})\equiv
\begin{cases}2A(B)-s&\gamma=0,\\-s&\gamma=1.\end{cases}
\]

The raw exterior length changes by exactly \(\gamma\). These identities give
the stated charge laws. The exact trim identity follows directly from
\(A(B\mathbin{++}[9])=A(B)+9s\) 和 the parity sign change.

## Independent COMPUTED regression

Reproducer: `calculation/agent-108/charge_checks.py`.
The charge uses an independent alternating sum; raw transitions 和 `edgeOK`
come from the existing exact Python mirror. The integer controls use an
independent Horner evaluation 和 canonical base-b integer reversal.

| Check | Exact completed scope |
|---|---|
| Decimal exhaustive | 130,321 exteriors of lengths 0..4; coefficients 0..18; nonzero first coefficient for nonempty exteriors |
| Exterior carry cases | 61,538 nonoverflow sources 和 68,783 overflow sources; a one-coefficient center supplies the required complementary carry |
| Decimal trimming | 141,182 legal edges, including 10,861 edges with a nonzero exterior trim; every legal trailing-9 trim of each raw successor |
| Empty/neutral corners | 585 sources across bases 2,4,8,10,11,16,17,26,32; exterior lengths 0..64; 19,305 legal trim edges |
| Existing certificates | Eight existing Lean-source certificate bases; 56 original edges; `cycleOK=True`; zero vertex-charge residues; 56 exact integer transitions |
| Seeded wide samples | 10,000 valid edges 和 exact integer transitions; B lengths 0..80; C lengths 1..41; bases 2..36; 5,153 decimal samples |
| Seeded padding | 10,000 exact charge-invariance checks with 0..32 appended neutral coefficients |

The exhaustive decimal scope covers every exterior dependence on C: the raw
exterior sees C only through its outgoing carry, which the hypothesis fixes
as the complement of the exterior carry. The wide samples are supplementary
finite controls. The seed is `10820261027`; integer template gaps range 2..12.

Exact command, from repository root:

```bash
python3 calculation/agent-108/charge_checks.py
```

Exact output:

```text
DECIMAL_EXHAUSTIVE {'legal_trim_edges': 141182, 'nonzero_trim_edges': 10861, 'raw_g0': 61538, 'raw_g1': 68783, 'sources': 130321}
EMPTY_AND_NEUTRAL {'sources': 585, 'trim_edges': 19305}
KNOWN_CERTIFICATE base=2 edges=4 cycleOK=True charge_residues=0
KNOWN_CERTIFICATE base=4 edges=6 cycleOK=True charge_residues=0
KNOWN_CERTIFICATE base=8 edges=8 cycleOK=True charge_residues=0
KNOWN_CERTIFICATE base=16 edges=10 cycleOK=True charge_residues=0
KNOWN_CERTIFICATE base=32 edges=12 cycleOK=True charge_residues=0
KNOWN_CERTIFICATE base=26 edges=4 cycleOK=True charge_residues=0
KNOWN_CERTIFICATE base=11 edges=6 cycleOK=True charge_residues=0
KNOWN_CERTIFICATE base=17 edges=6 cycleOK=True charge_residues=0
KNOWN_TOTAL {'bases': 8, 'edges': 56, 'integer_transitions': 56}
SEEDED_WIDE seed=10820261027 {'decimal_samples': 5153, 'g0': 4547, 'g1': 5453, 'integer_transitions': 10000, 'padding_checks': 10000, 'samples': 10000}
ALL COMPUTED CHARGE CHECKS PASSED
```

Observed run: exit code 0; elapsed 7.51 seconds. Every arithmetic check uses an
explicit failure branch, so optimized Python preserves the checks.

## Lean verification record

New project: `Agent108NeutralAlternatingCharge`, registered in
`lean/registry.json`, with the following 3 modules:

| Module | Content |
|---|---|
| `Base.lean` | Exact normalization bridge; charge of empty/neutral words; arbitrary neutral-suffix invariance |
| `Step.lean` | Raw no-overflow doubling, overflow reset, 和 the actual `edgeOK` recurrence |
| `Cycle.lean` | Checked-chain propagation/reset; charge zero at every cycle edge source/target; empty/neutral exclusions |

The principal endpoints are `edge_charge_step`, `cycle_charge_zero`,
`cycle_each_edge_charge_zero`, `cycle_exterior_ne_nil`, 和
`cycle_exterior_ne_replicate`, in namespace `Agent108.NeutralCharge`.
The registry lists 12 endpoints total, including supporting bridge lemmas.

Executed with stock Lean 4.19.0, one compilation thread:

```bash
LEAN_NUM_THREADS=1 python3 tools/verify.py --changed
```

The existing compiler directory was placed on PATH. Exact terminal output:

```text
[rules] 5220 Lean files, 302 projects, OK
[changed] against origin/main: 3 new/changed Lean file(s); building 3 module(s); auditing 1 project(s)
[build] up to 1 Lean file(s) at a time
[build] OK
[kernel replay] 3 module(s) re-checked by lean4checker
[axioms] 12 endpoints checked
ALL CHECKS PASSED (changed files only, against origin/main)
```

Direct per-file compilation was additionally measured through Python's
operating-system child resource counters, since `/usr/bin/time` was absent:

| Module | Wall seconds | Peak RSS KiB | Exit |
|---|---:|---:|---:|
| Base | 0.733 | 423,968 | 0 |
| Step | 1.607 | 480,952 | 0 |
| Cycle | 0.644 | 446,848 | 0 |

The files 都 fit the 8 GB / 20 minute per-file budget. The cycle endpoints
use only the permitted axioms `propext`, `Classical.choice`, `Quot.sound`.
No trust bypass is used. The base comparison is main commit
`eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`.
