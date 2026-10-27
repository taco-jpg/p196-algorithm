# Agent 108 — positive-power lifting through labelled graph quotients

## Result and scope

The new generic Lean development formalizes the power-lifting argument
proposed by Agent106 and independently discussed by Agent113 for their
cyclic graph representations. Given pointwise edge lifting and a finite
cover of the relevant fiber, a quotient closed word has an original closed
lift after a positive number of repetitions. A specified original source
may first traverse a transient. The complete label word is preserved,
with repetition rather than cyclic rotation.

**LEAN-VERIFIED, plus independent COMPUTED finite controls.** The actual
repository build/kernel/axiom receipt and exact tested/published tree are
recorded in the companion PR. No external computation is a premise of the
Lean proof. The code imports only `Std` and its own three prerequisite modules.

This does not prove a concrete cyclic-graph generator or quotient checker
correct, establish P24 emptiness, produce an exterior/center cycle, or
prove decimal existence or unrestricted impossibility. Fixed-period
languages need not be equal, and the original supplied source need not
return. These limitations are themselves demonstrated by Lean examples.

Claim: [6433711477](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433711477).
Method/PAPER attribution remains Agent106
([6433654839](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433654839))
and the independent discussion by Agent113
([6433664421](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433664421)).
Agent111 retains computational invariant verification; Agent114 retains
the separate exact-period graph-pruning formalization. Agent105's actual
base6 exterior obstruction [#417](https://github.com/taco-jpg/p196-algorithm/pull/417)
is not replaced or reattributed by the abstract examples here.

## Exact hypotheses and conclusion

Let original and quotient edge relations be

```text
E : V -> A -> V -> Prop
F : Q -> A -> Q -> Prop
pi : V -> Q.
```

`Walk E x w y` means a path from x to y carrying exactly the finite label
list w. The empty walk requires x=y. No determinism is assumed.

The core lifting hypothesis is POINTWISE:

```text
for every original x, label a, and quotient q':
  F (pi x) a q' -> exists y, E x a y and pi y=q'.
```

It must hold from every individual member of a quotient fiber. Merely
having some original edge between two fibers is insufficient. The core
lifting direction does not require a homomorphism assumption; that
assumption is added explicitly for the reverse projection direction.

Suppose w closes at q0 in F, x0 lies over q0, and a supplied list `carrier`
contains every original vertex over q0. The principal theorem
`lift_closed_with_transient` gives natural r,m and a vertex y such that

```text
0 < m
r + m <= carrier.length
pi y = q0
Walk E x0 (wordPower w r) y
Walk E y  (wordPower w m) y.
```

Only the full-word endpoints need this finite cover. Intermediate vertices
while reading one copy of w may lie elsewhere. Duplicates or extra vertices
in the supplied cover weaken its bound but do not invalidate the theorem;
an exact duplicate-free fiber enumeration gives the fiber-cardinality bound.

`lift_nonempty_closed_power` additionally requires w nonempty and concludes
that the closed lift is nonempty, with 1<=m<=carrier.length. The existence
is over a suitable y in the fiber, not necessarily x0. The word-length
identity `(wordPower w m).length=m*w.length` is separately proved.

## Why the proof works

Pointwise edge lifting first lifts any finite quotient path from a specified
original source. Fix the closed word w. For every x in its basepoint fiber,
choose one such complete-word lift and call its endpoint `next x`.
The endpoint remains in the same fiber. Outside that fiber the proof's
auxiliary map is the identity; an invariant proves that this default case
is never used along the relevant orbit.

Among the first N+1 endpoints, where N is the cover length, two agree.
`FiniteReturn.lean` proves this directly from a finite-list injection bound,
using standard list-erasure lemmas; the cover need not be duplicate-free.
Writing the two indices as r and r+m gives m>0 and r+m<=N.

Concatenating the chosen complete-word paths supplies the transient w^r
and the closed suffix w^m. This explains both essential qualifications:
the repeated endpoint may occur after a transient, and m can exceed one.
All choice and equality reasoning is checked by ordinary Lean; the only
permitted axioms remain the repository's standard three.

## Accepted languages and repeated drivers

`PowerStable accept` means

```text
accept w and 0<m -> accept (wordPower w m).
```

`ClosedWith E accept` means existence of a nonempty E-closed word satisfying
that predicate. Add a surjective edge homomorphism pi, pointwise lifting,
and finite covers for all fibers. Then

```text
closedWith_iff_of_powerStable:
  ClosedWith E accept <-> ClosedWith F accept
```

and `no_closedWith_iff_of_powerStable` gives the corresponding absence
equivalence. Homomorphism projects an original closed walk without changing
its labels. The other direction lifts a quotient word and uses power
stability exactly where the repetition count can increase.

There is a concrete specialization to fixed-driver repetitions:

```text
PositivePowers driver word :=
  exists k, 0<k and word=wordPower driver k

positivePowers_closedWith_iff:
  ClosedWith E (PositivePowers driver)
    <-> ClosedWith F (PositivePowers driver).
```

The separate `wordPower_mul` identity proves this predicate power-stable.
The exponent is existential; this is not an equivalence for each fixed k.
Phase restrictions must be retained in the actual labels or supplied as
a predicate with the stated stability property. An arbitrary phase or
fixed-length predicate is not automatically stable.

Applying these endpoints to the current exterior algorithms still requires
checking their concrete projection, every-member edge lifting, fiber covers,
and acceptance interpretation. Graph pruning and exact column arithmetic
have their own obligations. The theorem does not silently discharge them.

## Formal boundary controls

`Examples.lean` uses only finite Bool/Unit/Empty graphs. Its seven endpoints
are structural proofs, including exclusions for every nonempty word:

| Endpoint | Boundary established |
|---|---|
| `toggle_quotient` | Two-state toggle has projection and pointwise lifting. |
| `toggle_requires_two_laps` | Quotient one-letter loop; no original one-lap return; two laps return. |
| `transient_quotient` | false -> true -> true satisfies both graph-map conditions. |
| `transient_returns_only_at_true` | No nonempty word returns false; true loops. |
| `homomorphism_without_lifting` | Merging an acyclic edge creates a loop but fails pointwise lifting. |
| `merged_acyclic_no_return` | That original graph has no nonempty closed word at any length. |
| `empty_fiber_boundary` | Vacuous lifting on an empty original graph cannot supply an original cycle. |

The toggle also shows why acceptance of words of length exactly one cannot
be transported by the power-stable theorem. The empty-word premise is
separately controlled in the computation: a zero-edge walk is not a
positive-length cycle merely because its repetition count is positive.

## Independent finite computation

`cyclic_quotient_checks.py` compares a local greedy lifting construction
with independent Boolean endpoint-relation composition and a breadth-first
simple-lasso search. It checks every returned edge, literal label, quotient
phase, cycle closure, and r+m bound. The exhaustive domains are exactly:

| Family | Graphs | Supplied-start cases |
|---|---:|---:|
| All pairs of total labelled maps on n=1..3, binary words of lengths1..3 | 746 | 31,080 |
| All one-label nonempty-outgoing graphs on n=1..3, word lengths1..4 | 353 | 4,192 |
| All total one-label maps on four vertices, word lengths1..4 | 256 | 4,096 |
| Two quotient vertices, fiber sizes1/2, all nonempty target subsets in each fiber from each source; source-phase labels; closed paths of lengths1..3 | 6,616 | 184,856 |
| Total | 7,971 | 224,224 |

These are not all arbitrary labelled graphs on four vertices. They cover
105,504 quotient closed-word instances, 316,835 endpoint pairs, and 448,448
explicit path certificates, two per supplied-start case. Six declared
power-stable predicates yield 1,622,976 checked implications. A four-state
cycle attains the bound r=0,m=4. Four corrupted certificates are rejected.

Both normal and optimized Python runs pass, in 11.09 s and 9.11 s in the
recorded executions. A genuine tiny time cap returns UNDECIDED/exit3; zero
budget is rejected. All validation remains active under Python `-O`.
This computation checks examples and specifications, not the unrestricted
mathematical theorem and not a concrete exterior representation.

## Modules, resources, and reproduction

The project registers four modules and 34 public theorem endpoints:
`FiniteReturn`, `WordWalk`, `QuotientLift`, and `Examples`. The only registry
change is its new entry; every previous entry remains unchanged.

Fresh final-source compilation with `lake env lean -j 1 <module>` enforced
one CPU core, 8 GiB address space, and 1,200 CPU seconds per module:

| Module | Wall seconds | Peak RSS KiB |
|---|---:|---:|
| FiniteReturn | 0.567590 | 443,068 |
| WordWalk | 0.385337 | 437,920 |
| QuotientLift | 0.328528 | 431,500 |
| Examples | 0.344704 | 429,732 |

All compile without warnings under the pinned stock Lean4.19.0 runtime.
The unmodified `python3 tools/verify.py --changed` gate passes: 5,221 Lean
files and 302 projects checked, four changed modules replayed by
lean4checker, and all 34 endpoints audited with permitted axioms only.
The exact staged-tree identity is in the PR. No proof escape hatch or custom
axiom is used, and no benchmark result is trusted as a theorem premise.

From the repository root, with the pinned toolchain on PATH:

```bash
python3 calculation/agent-108/cyclic_quotient_checks.py
python3 -O calculation/agent-108/cyclic_quotient_checks.py
python3 tools/verify.py --changed
```

Prior-work audit distinguished the existing `Sofic.projection_sound` rank
projection (original cyclic words map forward) from this finite-fiber
positive-power lifting direction. Agent104's A120 bounded-simple-cycle
extraction may change driver words and is not substituted for this theorem.
Neither development is copied or imported as an unneeded dependency.
