# Agent 114 — T3: A120 center symmetry and canonical trim sites

## Status and attribution

**LEAN-VERIFIED**, with independent **COMPUTED** controls. The literal complete
gate, direct file-resource checks, and normal/optimized arithmetic controls pass.

This formalizes the CENTER portion of Agent7's PAPER Theorem C in
[PR315](https://github.com/taco-jpg/p196-algorithm/pull/315), including the exact
symmetry bridge needed to apply it to the unchanged A120 cycle checker.
Agent7 retains mathematical attribution. Agent119's center canonicalizer is
imported unchanged; this work adds no stripping algorithm or joint quotient.

Claim: issue #289, comment
[6433567813](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433567813).
Agent119 retains joint canonicalization/uniqueness, Agent104 finite width
decision, Agent112 numerical injectivity, and the existing teams retain all
priority-driver searches and regular-language scopes.

## The symmetry bridge

For ALL natural bases and arbitrary input lists, each branch of `nextC` is
the pointwise sum of a word and its reverse. The existing A120 reflection
lemma therefore proves

```text
(nextC b B C).reverse = nextC b B C.
```

If an edge is accepted, its center equation removes equal neutral runs from
the two ends of this symmetric raw successor. Exact list cancellation proves
that the TARGET center is symmetric. The source of an arbitrary accepted
edge need not be symmetric.

Every nonempty accepted chain has a symmetric final center. For an accepted
cycle, closure identifies that final center with the starting center. Symmetry
then propagates along every listed edge. Thus original A120 acceptance itself
implies symmetry of the specified start and every source/target center; no
additional cycle hypothesis has been assumed.

## Why source symmetry must be explicit locally

The accepted decimal edge

```text
B=[], C=[9,10], B2=[10], C2=[0], u=0, v=1
```

has `e1=0`, `e2=gam=1`, raw `nextB=[10]`, and raw `nextC=[9,0,9]`.
Its source has paired neutral stripping depth zero, yet its center trim is
positive on overflow. The source is asymmetric and starts with 9.

Consequently, zero paired stripping depth ALONE is not a local overflow
restriction. The correct direct local premise is a nonneutral source head.
For a symmetric valid source, pair-core normality implies that premise:
symmetry supplies the matching terminal coefficient, irreducibility excludes
a removable neutral pair, and `Hyp` excludes the remaining singleton-neutral
case. The latter exclusion reuses Agent119's existing theorem.

## Exact head formulas and trim gates

Fix `Hyp b B C`; put `h=b-1`, `e=e1 b B`, `f=e2 b B C=1-e`, and
`g=gam b B C`. For a nonempty center with first coefficient `c`, overflow gives

```text
nextC.head = (c+e) mod b + h*e.
```

Under these hypotheses the raw head equals `h` exactly when `c=h`. This
equivalence does not require source symmetry. A positive center trim forces
a neutral raw head; hence a nonneutral source head implies `v=0` on overflow.

Without overflow, write `C=P++[c]` and explicitly require `C.head= c`.
Let `t=(norm b P e).2`, the actual carry entering the LAST center coefficient.
The exact raw head is

```text
(c+e) mod b + (c+t) mod b.
```

The formula needs only matching first/last coefficients, not full symmetry.
Full symmetry supplies this premise in the cycle application. For `c!=h`, a
neutral raw head and the carry bounds force

```text
e=0: 2*c+t = 3*b-1
e=1: 2*c+t = b-2.
```

Since `t` is a bit, the exact coefficient/carry sites are:

| Exterior entering carry | Center head and last coefficient | Carry entering last coefficient |
| --- | --- | --- |
| `e=0` | `(3*b-1)/2` | `(3*b-1)%2` |
| `e=1` | `(b-2)/2` | `(b-2)%2` |

Natural integer division is used. In base ten this is `(e,c,t)=(0,14,1)` or
`(1,4,0)`, the reverse carry pairing from the exterior trim-site theorem.

A raw-head site does not itself guarantee that a PAIR can be removed. In
base three, `B=[1,0,3], C=[0]` has `e=1`, `g=0`, and the low site, but its
raw center is the singleton `[2]`. It allows no positive center trim.
The formal result is positive-trim necessity, not the converse implication.

The local source-head overflow gate requires no target normality and no
source symmetry. The packaged positive-trim theorem explicitly requires
source symmetry and a nonneutral head. The canonical-edge consequence derives
the head premise from source symmetry, `Hyp`, and zero paired depth.

## Complete-cycle consequence

`CenterTrimGates b E` records source-center symmetry, a nonneutral source head,
`gam=1 => v=0`, and `v>0 => gam=0` with the exact `CenterTrimSite` predicate.

Agent119's existing `normalizeEdges` map takes every accepted cycle to an
accepted cycle with zero paired center depth at every interface. Applying the
new cycle-symmetry theorem to THAT accepted cycle supplies the missing local
symmetry premise. Every resulting edge therefore satisfies the center gates.

The existential certificate problem is equivalent to adding these restrictions
and center canonicality. Both sides retain full `cycleOK=true`; the reverse
implication simply forgets the additional properties. The result does not
assert that gates alone establish acceptance or that normalization preserves
rejection of arbitrary malformed lists.

The constructive representative is exactly Agent119's existing map. Its
already proved unchanged exterior words/trims, complete carry/overflow stream,
listed edge count, and total gain remain available. No new transformation,
least-period claim, search result, decimal witness, or unrestricted obstruction
is introduced. No full suffix-depth conservation theorem is claimed for
arbitrary asymmetric centers.

## New files and dependency base

Namespace: `Agent114.NeutralCenterTrimSites`.

| Module | Content | New endpoints |
| --- | --- | ---: |
| `CenterSymmetry` | Raw/target/chain/cycle symmetry | 5 |
| `HeadCoefficient` | Exact head formulas and all-base linear thresholds | 4 |
| `CenterGates` | Correct local hypotheses, quotient/parity sites, decimal specialization | 5 |
| `Main` | Existing normalized cycle inherits gates; existential restriction | 3 |

The exact base is Agent119 PR
[#402](https://github.com/taco-jpg/p196-algorithm/pull/402), commit
`ffa92174a3ce66726660cad1961440788deed896`, tree
`d73f14bffb8fe8c409f256a387a547e3e5a68943`, already stacked on
[#389](https://github.com/taco-jpg/p196-algorithm/pull/389) and
[#374](https://github.com/taco-jpg/p196-algorithm/pull/374).
No Agent119 source is edited. Our exterior canonicalization/trim-site PRs and
Agent112's numerical modules are not dependencies. The new delta is four Lean
files, one registry entry, one self-contained Agent114 control script, and this
report. README and RESULTS are unchanged.

## Lean verification and resource bounds

Run from the repository root with the repository Lean 4.19.0 toolchain:

```bash
LEAN_NUM_THREADS=1 python3 tools/verify.py --changed
```

The literal required gate passed against pinned `origin/main`
`eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`:

```text
[rules] 5229 Lean files, 305 projects, OK
[changed] against origin/main: 12 new/changed Lean file(s);
          building 12 module(s); auditing 4 project(s)
[build] OK
[kernel replay] 12 module(s) re-checked by lean4checker
[axioms] 85 endpoints checked
ALL CHECKS PASSED (changed files only, against origin/main)
```

Four modules and 17 endpoints are new; eight modules and 68 endpoints belong
to the pinned Agent119 dependencies. Every new endpoint uses only a subset
of the permitted `propext`, `Classical.choice`, and `Quot.sound` axioms.
There are no custom axioms, admissions, prohibited evaluators or debug options.
New files compile without warnings; an unchanged legacy dependency retains
its pre-existing unused-variable warning.

Direct `lake env lean` checks used one thread, an 8 GiB address-space bound,
and a 1200-second timeout per file. Python measured wall time and child peak RSS:

| File | Wall time | Peak RSS |
| --- | ---: | ---: |
| `CenterSymmetry.lean` | 0.557 s | 423,228 KiB |
| `HeadCoefficient.lean` | 3.081 s | 467,296 KiB |
| `CenterGates.lean` | 0.827 s | 457,140 KiB |
| `Main.lean` | 0.411 s | 445,964 KiB |

Independent semantic review confirms the singleton-neutral exclusion,
source symmetry versus head normality, actual last incoming carry orientation,
and the accepted-cycle existential composition.

## Independent finite arithmetic controls

```bash
python3 calculation/agent-114/center_trim_site_controls.py
python3 -O calculation/agent-114/center_trim_site_controls.py
```

Both runs printed identical totals and `ALL CENTER TRIM SITE CONTROLS PASSED`.
The normal run used 7.521 s wall / 7.102 s CPU / 14,080 KiB peak RSS; optimized
used 7.178 s / 6.944 s / 14,080 KiB.

The script is self-contained, using whole positional integers for normalization
instead of the mirror's coefficient-by-coefficient carry loop. It imports no
Agent114/119 helper. The mirror supplies pinned source fixtures and differential
checks. Pair stripping is independently compared with all literal decompositions.

In bases 2–10, arbitrary centers of widths 0–3 and symmetric centers of widths
4–5 are exhausted. The four exterior fixtures `[]`, `[1,0]`, `[b]`, `[1,0,b]`
cover respectively `(e,g)=(0,1),(0,0),(1,1),(1,0)` whenever the flip holds.
Every legal partial exterior/center trim of each Hyp-valid source is checked.

| Coverage | Count |
| --- | ---: |
| Small arbitrary-center / wider symmetric-center source inputs | 85,344 / 84,912 |
| Hyp-valid sources / asymmetric Hyp-valid sources | 85,303 / 39,601 |
| Raw symmetry checks / raw inputs outside Hyp | 170,539 / 85,236 |
| Total accepted edges / all legal partial-trim edges | 98,444 / 96,152 |
| Head-normal overflow edges with `v=0` | 40,073 |
| Canonical local head-site equivalences / positive trim sites | 21,292 / 1,730 |
| Repeated neutral-pair padding controls | 2,010 |
| Original / center-normalized / padded source cycles | 8 / 8 / 24 |
| Exact known edges / normalized overflow edges with `v=0` | 280 / 16 |
| Mirror state / edge / cycle comparisons | 6,673 / 7,917 / 40 |
| Empty source-center inputs / empty target-center edges | 36 / 375 |
| All-neutral center Hyp exclusions | 180 |
| Malformed checker / operation rejections | 15 / 14 |

All eight pinned-main source bases (2,4,8,11,16,17,26,32) and all 40 cycle
variants pass independent and mirror acceptance. Additional checks cover the
asymmetric decimal counterexample, the odd-base singleton-site boundary, a
wrong target, a nonclosing singleton edge list, empty cycles, and arbitrary
large natural coefficients for the unconditional raw symmetry statement.
All guards remain active under optimized Python.

The script also corroborates symmetric-source overflow pair-depth identities
on its finite domain. That computation is not promoted to a new general Lean
depth theorem. These counts are regressions, not newly discovered certificates,
period-completion results, or a decimal no-go argument.
