# Agent 104 — bounded neutral centers have balanced representatives

**Status: LEAN-VERIFIED + COMPUTED.** The unchanged checker, full kernel/axiom
gate, independent executable controls, 和 read-only proof reviews pass.

## Result 和 attribution

This formalizes Agent110's established width-preserving center reduction from
[PR338](https://github.com/taco-jpg/p196-algorithm/pull/338), using Agent7's
neutral padding mechanism 和 Agent119's local padding/length theorems. It is
distinct from Agent104's unrestricted-width arbitrary schedule transport in
[PR391](https://github.com/taco-jpg/p196-algorithm/pull/391).

Theorem: in any base, any accepted A120 certificate whose center
phases all have width at most W has a checked representative with centers
of widths W-1/W 和 center trims0/1, for W>=2. The construction keeps the
entire exterior sequence, exterior trims, lower carry/overflow streams,
listed number of edges, 和 total gain. It preserves the cap W.

At fixed initial exterior, all exterior edge triples (B,B2,u), 和 all
lower-carry/overflow pairs, existence with arbitrary center widths<=W is
equivalent to existence in this balanced class. Center words 和 center-trim
schedules are existential on both sides; the original schedule is not fixed.

The contribution is the registered Lean proof. It proves no new finite search
negative, decimal certificate, unrestricted impossibility, or least-period
preservation. It does not combine balancing with maximal neutral stripping.

## Width-preserving construction

For a center C with m=|C|<=W, use the actual phase-dependent reserve

\[
a(C)=\left\lfloor\frac{W-m}{2}\right\rfloor,
\qquad
\widehat C=(b-1)^{a(C)}\;C\;(b-1)^{a(C)}.
\]

Then

\[
|\widehat C|=W-((W-m)\bmod2)\in\{W-1,W\}.
\]

This construction uses the largest permitted width of the original parity.
The generic prefix/suffix reserves from PR391 are not used here: those may
exceed the width ceiling.

For an accepted edge, write m,m' for the old center widths, v for its trim,
g for its actual overflow, 和 a,a' for the two reserves. Imported exact
accounting gives

\[
m'+2v=m+g,\qquad g\in\{0,1\}.
\]

Set the new trim to w=v+a-a'. The proof first establishes a'<=v+a, so natural
subtraction loses nothing. If M,M' are the padded widths, then

\[
M'+2w=M+g.
\]

Both M,M' lie in the adjacent pair W-1/W; the equation forces w<=1 和 the
exact rule

\[
w=1\quad\Longleftrightarrow\quad g=1\text{ 和 }M=W.
\]

The local transition table follows:

| Source width | Overflow | Target width | Center trim |
|---:|---:|---:|---:|
| W-1 | 0 | W-1 | 0 |
| W | 0 | W | 0 |
| W-1 | 1 | W | 0 |
| W | 1 | W-1 | 1 |

Thus the initial low/high width choice determines the profile from the
overflow word. This explains the credited two-profile reduction; it does not
assert that either syntactic profile has a realizable center.

## Checked chains 和 complete cycles

Local transport needs bounds on both edge endpoints. The global input uses
only source-phase bounds. `cycle_interface_cap` derives every target bound
from the original `chainOK` seams 和 center closure, including the final seam.
No target-Hyp assumption or center symmetry is added.

Map `balanceEdge` over the list. Since every occurrence of a given center is
mapped by the same function, adjacent endpoints still agree. The final B is
unchanged; final C is the balanced image of the old final C. Each transformed
edge passes the original `edgeOK` via Agent119's local transport theorem.

Agent119's `cycleOK_iff_closed_chain` then supplies acceptance from the
nonempty checked closed chain, without duplicating its automatic-gain proof.
Actual overflow is preserved at every edge. Applying the existing identity
2*sumGain=3*sumGam to the old 和 new accepted cycles proves exact gain equality.

The existential endpoint `bounded_iff_balanced` fixes the base, width ceiling,
initial exterior, full exterior edge data, 和 lower-carry/overflow stream.
Its forward direction uses the construction. Its reverse direction uses the
balanced widths' inclusion in the original cap. It is not an equivalence
between arbitrary rejected edge lists before 和 after transformation.

## Lean modules

All names use namespace `Agent104.NeutralBalancedWidth`.

| Module | Main roles |
|---|---|
| Step | Reserve, exact padded lengths, natural trim balance, checked edge, binary/exact trim rule |
| Chain | Source-to-target cap coverage, seams/endpoints, fields/streams, cycle acceptance, gain |
| Main | Positive balanced-phase predicate 和 fixed-data bounded existence equivalence |

The original A120 checker is imported unchanged. There is no new stripping,
normalization, or carry implementation in the proof.

## Executable controls

From the repository root, both commands pass with matching counters:

```sh
python3 calculation/agent-104/balanced_width.py
python3 -O calculation/agent-104/balanced_width.py
```

The same per-state reserve construction is checked against the exact mirror
和 an independently structured whole-integer normalizer. The latter evaluates
a complete positional sum, divides once by the base power, then extracts the
remainder digits. It checks complete source/output edge equations rather than
simulating an ordinary reverse-add orbit.

Controls use the eight baseline certificate bases2,4,8,11,16,17,26,32, every
distinct rotation, original/doubled lists, selected concentrated/separated
natural schedules, 和 four ceilings: source maximum plus0,1,2,5. There are
four/five source variants per rotation, not necessarily distinct schedules;
this is not exhaustive weak-composition coverage. The source variants include
trim2 edges. Each local call checks both source 和 destination width bounds.

```text
BALANCED_WIDTH_PASS
bases=8 source_edges=56 source_variants=504
nonbinary_source_variants=112 balanced_cycles=2016
transformed_edge_replays=25088 independent_integer_edge_replays=50176
zero_output_trims=21952 one_output_trims=3136
length_arithmetic_cases=624 malformed_inputs_rejected=20
max_source_trim=2 max_source_width=51 max_balanced_width=56
```

All guards use explicit exceptions 和 remain active under optimized Python.
The20 negative controls include each local cap separately, invalid natural
values/types, malformed certificates, broken closure, 和 invalid bases.
Independent read-only review reconciled every counter from fixture periods
和 independently reran the624 arithmetic/20 guard controls under `-O`.
No later-added certificate or new decimal search is counted here.

## Dependencies 和 verification

The source tree contains exact published parents:

- Agent104 arbitrary schedule transport #391,
  commit `5e24416320d0a8a55a2e0a8ff1aa1f45a983aba2`; its script supplies valid
  nonbinary source schedules for the independent tests.
- Agent119 local center padding #374,
  commit `f182aa81cdb4040f6237401bced19fbb863adf4f`, already inherited by #391.
- Agent119 length accounting #339,
  commit `67b353c211a36cc45945a42f484c3ab7bd027428`.

Their proof source is unchanged. The dependency registry conflict was resolved
by retaining both complete original project entries. The new project registers
three modules 和22 endpoints. All printed dependencies belong to the allowed
set: `propext`, `Classical.choice`, `Quot.sound`.

Separate source measurements use stock Lean4.19.0, one CPU, one Lean thread,
a hard8GiB address limit 和1200-second CPU/wall limits:

```sh
python3 calculation/agent-104/measure_lean.py lean/P196/Agent104NeutralBalancedWidth/Step.lean --hard-as
python3 calculation/agent-104/measure_lean.py lean/P196/Agent104NeutralBalancedWidth/Chain.lean --hard-as
python3 calculation/agent-104/measure_lean.py lean/P196/Agent104NeutralBalancedWidth/Main.lean --hard-as
```

| Module | Wall seconds | CPU seconds | Peak RSS KiB |
|---|---:|---:|---:|
| Step | 1.756406 | 1.340402 | 486944 |
| Chain | 0.990536 | 0.871561 | 452884 |
| Main | 0.562734 | 0.481444 | 449932 |

The required literal gate passed in the isolated integration worktree:

```sh
python3 tools/verify.py --changed
```

```text
[rules] 5229 Lean files, 305 projects, OK
[changed] against origin/main: 12 new/changed Lean file(s)
[kernel replay] 12 module(s) re-checked by lean4checker
[axioms] 73 endpoints checked
ALL CHECKS PASSED (changed files only, against origin/main)
```

The stack contributes12 modules/73 audited endpoints; this task contributes
three/22. The reference main is `eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`.
The checker is the official lean4checker v4.19.0 revision
`e11f65c651edd58d68ba260015d2bfde5102cd7f`. Publication compares the complete
Git tree with this checked local tree; its receipt belongs in the PR/issue,
not as a self-referential hash inside this report. No forbidden placeholder,
custom axiom, or metaprogramming is used.
