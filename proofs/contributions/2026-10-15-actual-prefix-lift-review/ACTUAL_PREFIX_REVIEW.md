# Independent review of actual prefix lifting

**Actual-orbit statements: PASS. Bounded-label adapter and actual hierarchy
composition: PASS.** Finite bit-graph implementations must use the adapter,
not the unrestricted source graph. This review read both original new
sources, the imported one-column extension interface, and the supplied
fresh verification record. It does not duplicate the full dependency
build.

## Valid actual-orbit content

`ActualPath` counts vertices; its edges are required only when both
endpoints lie inside the interval. Each vertex records the actual phase,
last known coefficient, and low carry. Each edge label is the actual
carry entering the high prefix. `actual_path_lifts` constructs the next
coefficient and its deeper carry from the same whole-word orbit. It
uses the exact actual extension theorem and actual scalar overflow,
without choosing independent carry controls or requiring disjoint
boundary windows.

The assumptions (1\le k<L), together with nondecreasing actual width,
are sufficient at every represented time. Restriction shifts both time
and clock phase and keeps the same inclusive endpoint convention.
`actual_component_interval_lifts` then selects the constant-component
interval and constructs a same-length path in the induced abstract lift.
It does not assume the existence of the path it constructs.

`ScalarRoot` proves the exact ten-edge root table by kernel evaluation
of all (7\cdot7\cdot2=98) triples. Actual scalar-clock windows map into
that root using their actual carry labels. Its first lift uses
`Fin 7 × Fin 19`, and the integer encoding lies in 0 through 132 with
the stated phase and coefficient recovery formulas.

These statements are mathematically sound. No claim of a numerical
94/98 bound follows before the remaining finite graph data, retained
membership, encoding, and hierarchy obligations are supplied.

## Concrete interface limitation found by review

The frozen `lift G` uses a `Nat` edge label called `deeper`, and its edge
definition does not require `deeper ≤ 1`. Its `Realization.edges`
condition, however, asks for forward encoding of **every** such edge.
This is stronger than needed for actual paths, whose labels are carry
bits, and prevents direct encoding into the saved bit-labeled graphs.

The concrete example in `lift root` is:

- source: phase 0, new coefficient 0;
- target: phase 1, new coefficient 9;
- deeper label: 9;
- parent edge label: 0.

The parent edge ((0,1,0)) exists. The extension equations read

\[
 0=\lfloor(0+9)/10\rfloor,\qquad
 9=(0+0)\bmod10+(0+9)\bmod10,\qquad
 0=\lfloor(0+0)/10\rfloor.
\]

Thus both endpoints are valid and this abstract label-9 edge exists.
`LabelNineCounterexample.lean` proves these facts and the stronger
statement that no unrestricted `Realization` from this frozen lift can
exist into any graph whose edge labels are all at most 1.

This is an applicability issue in the abstraction, not a contradiction
of any actual orbit theorem. A sufficient repair is to restrict graph
edges to labels at most 1, prove the actual labels satisfy that bound,
and apply the original encoding theorem to the restricted graph. The
author implemented this in a separate package so the frozen source
and its existing verification remain intact. This review does not
silently treat the unrestricted lift as the finite bit graph.

## Evidence and checkpoints

The original package's observed report records a successful fresh Lean
4.19.0 build and an audit of 52 declarations, including 15 new theorems
and 37 prerequisites. Only `propext`, `Classical.choice`, and `Quot.sound`
occur in that audit.

The three counterexample declarations compiled successfully against the
verified development dependency objects. Their final axiom audit uses
only `propext` and `Quot.sound`; see `counterexample_compile.log`.
That initial incremental check has now also been included in the adapter's
successful fresh build described below. `initial_elaboration_failure.log` preserves the first unsuccessful
attempt: Lean could not infer a decision procedure through the graph
projections until those goals were explicitly unfolded. That failed
attempt is not verification evidence; the final source contains no
unproved declaration.

| File | SHA-256 |
| --- | --- |
| Original `ActualPrefixLift.lean` | `48fbaf35996292ee97d4a10c14c598567d07b0f4bacd120138cb7cc7dcb4eea6` |
| Original `ScalarRoot.lean` | `f4dc3aeccafaa9b9ffcc5ba572708f9745cf599de8268e5f3c6e610194e336ec` |
| Original `verification.json` | `607a1022f0b947ac479b4ced45316c3827a2966363794bd2c09748e6484a0dd7` |
| `LabelNineCounterexample.lean` | `4753eb3bca19bc03711124396f469557f92623bf722c8361da2f4f06ca1a99a9` |

## Bounded adapter and hierarchy composition review

The separate package `../2026-10-15-bounded-prefix-lift-formal/` resolves
the limitation without changing the original proof sources.
`BoundedPrefixLift.bounded` restricts labels to at most 1.
`actual_label_bound` proves that restriction for every actual carry label,
including labels at overlapping boundaries. The actual path and
component-interval constructions therefore remain valid in the bounded
graph. Finite-ID transport now needs forward completeness only for
the two admissible carry labels.

`ActualJobFamily.family` supplies a concrete job-dependent family of
actual orbit windows. Its restriction law is proved with both the time
and phase shifted. `constructive_child_lift` constructs the actual child
path before applying its finite-ID encoding; it does not assume the
desired path lift. The component restriction and vertex count are
preserved. `actual_path_vertices_le` correctly supplies the earlier
generic hierarchy theorem with these constructed lifts, the acyclic
edge condition, and the weighted rank certificate.

The remaining premises are explicit local finite-data obligations:
child height and width, the bounded child encoding, vertex/rank bounds,
and rank decrease across bit-labeled component-changing edges. They
must still be checked for the concrete saved tables. The package does
not assert that those numerical tables are instantiated or that the
94/98 bound has been kernel verified.

The adapter's observed fresh Lean 4.19.0 audit reports **82 declarations**:
8 new adapter/hierarchy theorems, the 3 review counterexample theorems,
and 71 prerequisites. All source hashes and the checker hash were
recomputed from the report and agree. The 82 audit entries use only
`propext`, `Classical.choice`, and `Quot.sound`. This review inspected
the source, checker, and supplied fresh report; it did not repeat that
compiler run.

| Adapter evidence | SHA-256 |
| --- | --- |
| `BoundedPrefixLift.lean` | `57cbe8689aa6dc63a90445fcc48388edd3c2ce28653d45f178e849133bed2995` |
| `ActualJobFamily.lean` | `d98fb979c67def5649bb11d8076424b19812d10a8c0ae275f899439d20a94a94` |
| Adapter `verification.json` | `04d0ba46f6e5f9f5121f8b904f0bdf8e692e10c803afb25dd3b7ea11c06cc3cb` |

No further mathematical correction is requested for these statements.
