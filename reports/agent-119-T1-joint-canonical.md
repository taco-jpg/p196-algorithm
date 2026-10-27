# Agent 119 — T1 joint canonical deterministic quotient

## Status and scope

**LEAN-VERIFIED + COMPUTED.**

Four new Lean modules formalize Agent7's prior joint normal-form and
maximal-successor argument at the unchanged `Agent120.Neutral` checker.
This composes Agent114's exterior canonicalizer (#392) and our center
canonicalizer (#402). No other agent's source is edited.

The result concerns every base accepted by the checker. Every accepted cycle
has a fully stripped accepted representative with the same **listed edge
count**, complete `(e1,e2,gam)` stream, overflow total and total gain. Every
source and target exterior/center width is pointwise no larger. Each new edge
is the unique maximal raw successor of its normalized source, including both
natural trim counts. Certificate existence at each fixed listed length is
therefore equivalent to existence in this deterministic normal form.

This is a formal bridge for existing mathematics, not a new decimal
certificate or a global obstruction. Least/primitive period, preservation of
individual trim counts, unconditional checker equivalence, and continued
validity after an arbitrary valid source are not claimed.

## Dependencies and attribution

- Agent7: paper simultaneous stripping and conservation, #315; deterministic
  maximal-trim quotient, #326. Mathematical attribution remains Agent7.
- Agent114: exterior padding #366, chain transport #378, canonicalization #392.
  Pinned exterior head: `32f17949b996dc6ad636deae71b6c2c7f2159430`.
- Agent119: center padding #374, inverse #389, canonicalization #402.
  Pinned center head: `ffa92174a3ce66726660cad1961440788deed896`.
- Existing generic strip algorithms and their proved laws are imported;
  neither stripper nor the A120 checker is reimplemented in Lean.

The integration parent contains exactly the two unchanged dependency trees
with their registry entries united. Its Git tree is
`147a39511c1000a8609edff39c4f4774a51f4c69`.
The new research delta contains only this report, one agent119 control script,
four new registered Lean files, and the additive registry entry.

## Definitions and proof

Write `canonB` for maximal neutral exterior-suffix removal, `coreC` for
maximal paired neutral center removal, and `suffixDepth`/`depthC` for their
actual removed depths. A normal pair satisfies
`canonB b B = B` and `coreC b C = C`.

`rawEdge b B C` retains its exact source `(B,C)`. Its targets are
`canonB b (nextB b B C)` and `coreC b (nextC b B C)`; its trims are the
corresponding actual raw depths. It is accepted **iff** the source satisfies
`Hyp b B C`. Its target is normal, but need not satisfy `Hyp`.

For any accepted edge with normal targets, `edgeOK_sound` provides

```
nextB = suffixPad b u B2
nextC = padC b v C2.
```

Apply the stripping maps to force the two targets. Apply the depth maps,
using target depth zero, to force `u` and `v`. Thus that edge equals
`rawEdge` at its source. This uniqueness needs neither source normality nor
target validity and uses no unchecked natural subtraction.

Define `jointEdge` by exterior normalization followed by center normalization.
Both imported acceptance theorems apply. Its source and target are normal by
construction, so uniqueness identifies it with the raw maximal edge of the
fully normalized source. Consequently equal normalized sources give equal
normalized accepted edges. The same uniqueness also proves accepted-input
retraction, idempotence, and commutation of the two canonicalizers.

Map this transformation over a chain. Equal original seams remain equal.
Both imported cycle theorems preserve complete Boolean acceptance. The two
closed-cycle depth corrections cancel, preserving gain. Label preservation
is pointwise; width bounds compare corresponding fields in an ordered zip,
and an equal-length theorem ensures the zip omits no edge. The final
existence equivalence retains the original `cycleOK` and listed length on
both sides; it does not replace cycle acceptance with an initial-state test.

## Registered endpoints

Namespace: `Agent119.NeutralJointCanonical`.

| Module | Endpoints | Main contracts |
|---|---:|---|
| `MaximalEdge` | 6 | Normal/raw definitions, raw acceptance iff, maximal-target uniqueness |
| `JointEdge` | 10 | Accepted composition, raw identification, source quotient, retraction, idempotence, commutation, widths, labels |
| `Main` | 13 | Chain/cycle acceptance, count, normality, ordered widths/labels, totals, deterministic edges, fixed-length existence equivalence |
| `Boundary` | 2 | Exact counterexamples to two overstrong extensions |

The registered root is `P196.Agent119NeutralJointCanonical.Boundary`.
There are 31 new endpoints. The boundary examples use ordinary `decide`;
all other proofs compose existing algebra or checker equations.

## Two exact Lean boundary examples

1. **Source validity need not continue.** In base 10, `B=[1], C=[10]`
   has `(e1,e2,gam)=(0,1,0)`. Its already canonical raw edge has targets
   `B2=[3], C2=[0]` and `u=v=0`. The edge is accepted, but the target has
   both carries zero and fails `Hyp`. `decimal_source_not_invariant`
   verifies this at the actual checker.
2. **Joint idempotence requires acceptance.** In base 2, take malformed
   source `B=[4], C=[1,0,1]`, target `B2=[], C2=[0]`, and zero trims.
   The first joint application has exterior trim 0 and the second has 2.
   `joint_not_idempotent_without_acceptance` reduces the actual Lean
   natural-number computation and proves the two resulting edges differ.

The second source is outside the coefficient bounds. Outside `Hyp`, the
Python mirror's signed subtraction can differ from Lean's natural
subtraction. The control script therefore labels its separate Nat-arithmetic
witness explicitly and claims mirror/formula agreement only on accepted
sources. No rejected-input semantics is used in the positive theorems.

## Independent finite controls — COMPUTED

Exact commands from the repository root:

```bash
python3 calculation/agent-119/joint_canonical_controls.py
python3 -O calculation/agent-119/joint_canonical_controls.py
```

Both outputs agree. The script compares both normalization orders, the
unchanged mirror's maximal `step`, and separately coded whole-word integer
division followed by independent strip formulas. Explicit `require` checks
remain active under `-O`. Relevant output:

```text
JOINT CANONICALIZATION FINITE CONTROLS PASS (not a mathematical proof)
known_bases=8 known_edges=56
strip_word_controls=1218
integer_raw_controls=1596
template_controls=3192
edge_controls=798 edge_empty_exterior=24
edge_fixed_retractions=147 edge_nonfixed_inputs=651
edge_nonmaximal_u=439 edge_nonmaximal_v=402
edge_nonsymmetric_center=182 edge_target_hyp_false=78
edge_u_changed=270 edge_v_changed=224
chain_controls=89 chain_empty_controls=8
cycle_controls=56 cycle_listed_edges=504
cycle_phase_dependent=24 cycle_strictly_narrowed=51
source_equivalence_pairs=953
source_equivalence_equal=65 source_equivalence_different=888
```

The eight source certificates are those in the pinned main mirror
(bases 2,4,8,11,16,17,26,32). This is not a claim to cover every subsequently
published certificate. Directed sources include nonsymmetric centers and
accepted edges with invalid targets; padding schedules change both depths.
Finite cycle controls also check total `u` and total `v` separately, a
computational check stronger than the combined-gain endpoint claimed here.

A malformed base-2 seam is repaired by normalization: all four local edges
pass before stripping, while the original chain/cycle fail and the normalized
chain/cycle pass. Wrong trim values can likewise be repaired. These examples
exclude any assertion of checker equality on arbitrary malformed input.
Changed nonneutral target coefficients remain rejected in the selected
negative controls. These controls are finite tests, not an exhaustive search.

## Resource and repository verification

The exact Lean version is the pinned 4.19.0. All builds use one thread,
an 8 GiB address-space cap, and a 1200-second timeout. No verifier/checker
source, axiom allow-list, or mathematical dependency is modified.

Exact mandatory command (runtime binary directory prepended to `PATH`):

```bash
LEAN_NUM_THREADS=1 python3 tools/verify.py --changed
```

The unmodified command returned `ALL CHECKS PASSED`: 5,236 Lean files and
308 projects pass repository rules; 19 changed/stacked modules were built
and kernel-replayed; 154 endpoints were audited across seven projects.
Wall time was 46.688 seconds, peak child RSS 456,696 KiB, exit code 0.
The 31 new endpoints use only permitted axioms (`propext`, `Quot.sound`),
or none. The current main baseline was freshly fetched and remained
`eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`.

Final direct `lake env lean` measurements (seconds): `MaximalEdge` 1.950,
`JointEdge` 1.276, `Main` 1.318, `Boundary` 0.958. Cumulative child peak
RSS across these four sequential runs was 465,008 KiB, an upper bound for
each file. All four exit codes were 0. The independent Python runs took
approximately 0.23–0.25 seconds each and had identical normal/`-O` output.

Independent source review checked maximal-target uniqueness, the complete
cycle conditions, fixed listed length, ordered width correspondence, and the
two boundary examples. No issue was found. The result leaves base-10
certificate existence and unrestricted impossibility open.
