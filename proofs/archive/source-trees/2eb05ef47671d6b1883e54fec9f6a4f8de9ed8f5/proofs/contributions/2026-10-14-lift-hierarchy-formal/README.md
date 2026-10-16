# Finite hierarchy composition

`LiftHierarchy.lean` proves the downward induction used when a cyclic
component interval lifts to a deeper spatial graph. It builds on the frozen
15-theorem `2026-10-14-scc-bound-formal/CondensationBound.lean` package.
There are three new public theorems. The checker freshly rebuilds both
modules and audits all 18 theorems.

## Exact path-family interface

A `PathFamily` provides a predicate

```text
valid level path numberOfVertices
```

and a proof of restriction closure: any interval of a valid path is itself
valid at the same level. An interval may start at any time or clock phase.
Restriction closure applies at every level, including the target of a lift.

This family may be smaller than the set of all paths in an overapproximating
graph. In particular, actual orbit projections can have carry correlations
that are not expressed by the graph's local edges. The theorem does **not**
assume that every abstract graph path admits a spatial lift.

`orbitPathFamily` is a concrete constructor. Given projections of one orbit
at each level and a level-dependent eligibility predicate, it contains all
eligible finite windows of those projections. The eligibility predicate can
record clock preservation and membership in the retained graph at that
level. Restriction closure is proved in the constructor, and
`orbit_interval_valid` proves membership for any eligible window.

## Hypotheses of the hierarchy theorem

`hierarchy_path_vertices_le` uses levels `0` through `depth`, component maps,
cyclic-component flags, candidate sink ranks, and candidate vertex bounds
`bound level`. Its application premises are:

1. At the terminal level, every component visited by a valid path is acyclic.
2. At any earlier level, every nonempty valid path contained in a single
   cyclic component lifts to a valid next-level path with the **same number
   of vertices**. This is required at every starting phase.
3. Inside a valid path, an acyclic component has no internal edge. For an SCC
   decomposition, an acyclic component is a loop-free singleton.
4. Every valid path satisfies the weighted rank certificate, using weight
   `bound (level + 1)` for cyclic components and weight one otherwise.
5. For a nonempty valid path, its initial component's rank is at most
   `bound level`.

The conclusion is that **every supplied valid path at every level through
the terminal level has at most that level's candidate number of vertices**.
Empty paths are handled without requiring a bound on their unused initial
vertex. The next-level bound appearing syntactically at the terminal level
is never needed for a cyclic interval, since premise 1 excludes one.

`cyclic_interval_lifts` is the bridge between premises 1–5 and the one-level
weighted theorem. It restricts a source path to any inclusive interval
`[a,b]`, applies the whole-block lift premise to that restricted path, and
produces a next-level valid path of length `b + 1 - a`.

The main proof then inducts down from the terminal level. Each deeper bound
supplies the cyclic interval weight at the preceding level, where
`CondensationBound.cyclic_path_vertices_le_rank` combines the intervals.

## Scope and reproduction

This package checks the induction argument. It does not assert a particular
graph's SCC assignments, numerical rank tables, spatial-lift map, terminal
acyclicity, or membership of an actual reverse-and-add orbit in the family.
Those remain explicit premises for an application. It does not prove the
196 conjecture or any all-time palindrome-avoidance claim.

```sh
python check.py /path/to/lean-4.19.0/bin/lean
```

`verification.json` records the exact source SHA256 and Git blob hashes,
fresh compilation results, and transitive axiom audit. `compile.log`
preserves the complete output. Only Lean's standard logical axioms are
permitted; proof placeholders, extra axioms, and `native_decide` are rejected.

Development record: the interval and downward-induction proofs compiled
on their first attempt. One unused typeclass warning was removed. The
concrete orbit-window constructor was then added; eligibility was made
level-dependent so it can express membership in successive retained graphs.
The final clean rebuild checks those exact sources.
