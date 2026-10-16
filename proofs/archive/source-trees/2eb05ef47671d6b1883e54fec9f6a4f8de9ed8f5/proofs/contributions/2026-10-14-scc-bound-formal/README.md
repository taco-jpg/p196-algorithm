# Weighted component bounds for finite paths

`CondensationBound.lean` proves the generic composition theorem used by the
broader-return graph hierarchy. It imports only Lean 4.19.0's `Std`.
All 15 public theorems pass a fresh source rebuild and transitive axiom audit.

For a path with **n vertices**, let `component i` label its vertex at time
`i`, let `weight C` bound one constant-component interval, and let `rank C`
be a weighted sink rank. The exact certificate premises are:

1. Every interval `[a,b]` contained in the path whose component is constant
   has `b + 1 - a ≤ weight (component b)`.
2. Every visited component satisfies `weight C ≤ rank C`.
3. Every path edge crossing from component `C` to a different component
   `D` satisfies `weight C + rank D ≤ rank C`.

`path_vertices_le_rank` concludes

```text
n ≤ rank (component 0).
```

These are precisely the inequalities produced by a weighted longest-path
calculation on the condensation DAG. The proof does not need to trust an
SCC discovery algorithm or an algorithm that computes candidate ranks.
An application must establish the three premises for its own path.

## Why the path bound follows

`blockAge component t` counts vertices in the current constant-component
suffix, starting at one. The file proves that this suffix is constant and
that its age is at most its component's weight. The main inductive invariant
is written without truncated subtraction:

```text
t + rank (component t) + 1
  ≤ rank (component 0) + blockAge component t.
```

Inside a component the age increases by one. At a component change, the
age resets to one while the rank drops by at least the previous weight.
At the final vertex, the weight is at most the current rank, yielding the
claimed vertex count. Both endpoints are counted, including a one-vertex
path; the empty path is also handled.

## Component intervals and cyclic weights

`component_interval` proves that a path cannot leave a component and later
return to it when every visited weight is positive: between any two equal
endpoint components, every intermediate component is the same. It derives
this from the same local rank inequalities rather than assuming contiguity.

`interval_bound_of_cyclic` assigns weight `B` to cyclic components and
weight one to acyclic components. Its premises are:

- every constant interval in a cyclic component has at most `B` vertices;
- there is no path edge inside an acyclic component.

The second premise holds for a loop-free singleton SCC. The first is the
place where a spatial lift to a deeper graph supplies its bound.
`cyclic_path_vertices_le_rank` combines these premises with the weighted
rank certificate. `graph_path_vertices_le_rank` gives the same theorem
directly for a path in an arbitrary directed graph with a component map.

## Relation to the broader-return calculation

The neighboring `2026-10-14-broader-return/finite_bound.py` uses cyclic
weights equal to the next graph's maximum path vertex bound and acyclic
weights equal to one. Its candidate phase-zero bound is 1600 vertices.
`seven_returns_le_228` checks only the arithmetic implication:

```text
n ≤ 1600 ∧ 7 * returns + 1 ≤ n  →  returns ≤ 228.
```

This package does **not** certify the numerical graph tables, their SCC
assignments, the spatial-lift map, or the actual-orbit interval premises.
It supplies the reusable theorem for combining those separately verified
facts. It makes no claim of an all-time palindrome-avoidance result or a
proof of the 196 conjecture.

## Reproduction

```sh
python check.py /path/to/lean-4.19.0/bin/lean
```

The checker copies the exact source into a new temporary directory,
compiles it, and prints the transitive axioms for every public theorem.
It rejects proof placeholders, explicitly declared axioms, and
`native_decide`, permits only Lean's standard logical axioms, and records
source SHA256 and Git blob hashes in `verification.json`.
`compile.log` preserves the complete compiler and axiom-audit output.

During development, the first complete generic theorem compiled immediately.
The contiguity and cyclic-weight additions also compiled; two unused-binder
warnings were removed. Moving `omit` ahead of a declaration's documentation
comment resolved one syntax error. The saved final rebuild is clean.
