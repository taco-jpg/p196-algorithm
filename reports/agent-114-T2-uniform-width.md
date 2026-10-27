# Agent 114 — T2: exact uniform exterior width

## Status and scope

**LEAN-VERIFIED.** For the unchanged `Agent120.Neutral.cycleOK`, every accepted
cycle whose exterior interfaces have width at most `M` has an accepted
representative with every exterior interface of width exactly `M` and exterior
trim equal to its actual overflow. The construction preserves the center words,
center trims, complete carry/overflow stream, listed edge count, and total gain.
An existence equivalence also holds when only the maximally stripped exterior
widths are bounded. There is no restriction on the original natural trim counts.

This formalizes a known reduction used by bounded exterior searches. It does
not run a new search, validate a particular search implementation, find a
decimal certificate, or prove that the unrestricted decimal route fails.

Claim: issue #289, comment
[6433307811](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433307811).
Agent7's padding/normalization arguments and Agent109/107's common-width PAPER
reductions retain their attribution. Agent119's checked length theorem is
imported unchanged. Agents101/117/4/108/110/115/109 retain their respective
priority-P24 and repeated-lap search scopes; Agent107 retains the independent
width-eight graph review.

## Exact construction

For an accepted edge `E`, write `l=|E.B|`, `l'=|E.B2|`, and
`g=gam b E.B E.C`. Agent119's `edge_lengths` proves

```text
l' + E.u = l + g.
```

If `l,l' <= M`, put `a=M-l` and `a'=M-l'`. Natural subtraction is used only
under these bounds. The length equation gives the exact padding balance

```text
a + E.u = g + a'.
```

The existing local padding theorem therefore accepts

```text
Bnew  = E.B  ++ (b-1)^a
B2new = E.B2 ++ (b-1)^a'
unew  = g
Cnew  = E.C, C2new = E.C2, vnew = E.v.
```

Padding preserves `gam`, so `unew` is the overflow computed from the NEW source,
not merely a stored label from the old edge. Both exterior widths equal `M`.
Conversely, every accepted edge with equal exterior widths already satisfies
`u=gam`, directly from Agent119's equation.

For a linked chain the phase deficits form an existing `PadChain` witness.
The final deficit equals the initial deficit on a cycle. Existing exact chain
transport supplies acceptance, endpoint closure, stream preservation, and the
telescoping gain equality. Empty exterior words, empty chains, and `M=0` require
no separate theorem assumption; a cycle still has to satisfy the original
checker, including its nonemptiness and gain conditions.

## Registered Lean interface

Namespace: `Agent114.NeutralUniformExterior`.

| Module | Main content | Registered endpoints |
| --- | --- | ---: |
| `UniformEdge` | Width padding, local balance/acceptance, actual overflow trim | 6 |
| `UniformChain` | Complete linked-chain/cycle transport and preserved data | 9 |
| `Main` | Bounded-existence equivalences, including canonical widths | 4 |

Definitions `WidthBound M es B` and `UniformWidth M es B` include the separately
supplied starting exterior `B` and BOTH exterior endpoints of EVERY edge.

Principal endpoints:

```text
uniformEdge_balance
uniformEdge_ok
uniformEdge_trim_eq_gam
equal_width_trim
uniform_chain_plan
uniform_chainOK
uniform_chain_streams
uniform_cycleOK
uniform_cycle_gain
uniform_widths
uniformEdges_trims
bounded_cycle_exists_iff_uniform
canonical_bounded_cycle_exists_iff_uniform
```

The first existence equivalence is exactly

```text
(exists es B C, cycleOK b es B C = true AND WidthBound M es B)
IFF
(exists es B C, cycleOK b es B C = true AND UniformWidth M es B
               AND every e in es has e.u = gam b e.B e.C).
```

The second replaces the left-hand width condition by
`WidthBound M (canonicalEdges b es) (canonB b B)`. Its forward direction first
uses our accepted-cycle canonicalizer, then uniform padding. Its reverse
direction observes that canonicalization cannot increase any exterior width.
Original padded representatives on this left-hand side may be arbitrarily long.

## Fixed width and maximal stripping are different representations

The uniform representative can retain a neutral suffix. Its trim `u=gam`
need not be the maximal neutral suffix of the raw successor. For the known
base-two edge

```text
B=[2], C=[0,0], B2=[1,0], C2=[2,0,2], u=0, v=0,
```

the width-three representative is

```text
B=[2,1,1], raw nextB=[1,0,1,1], B2=[1,0,1], u=gam=1.
```

The raw suffix depth is two. Full canonicalization of the same edge has `u=0`.
Both are accepted, but they serve different state representations. The control
script checks this example against independent integer arithmetic and the mirror.

The Lean acceptance theorems start from accepted inputs and explicit bounds.
They do not assert a pointwise checker equivalence for arbitrary rejected or
undersized input data. Listed edge count is preserved; least period is not claimed.
No center-width cap, solver completeness theorem, or new decimal obstruction is
part of this result.

## Dependency integration and review scope

The review base is an exact integration of two existing branches:

1. Our exterior canonicalization PR [#392](https://github.com/taco-jpg/p196-algorithm/pull/392),
   commit `32f17949b996dc6ad636deae71b6c2c7f2159430`, already stacked on
   [#378](https://github.com/taco-jpg/p196-algorithm/pull/378) and
   [#366](https://github.com/taco-jpg/p196-algorithm/pull/366).
2. Agent119's length-accounting PR
   [#339](https://github.com/taco-jpg/p196-algorithm/pull/339),
   commit `67b353c211a36cc45945a42f484c3ab7bd027428`.

The integration tree is `3a69497dda585c2284dba69d37c64860b253ff66`.
The four Agent119 source/report files match the pinned commit byte-for-byte;
the registry is the union of the existing project entries. No dependency proof
was rewritten. The new review delta is only the three Agent114 Lean modules,
one registry entry, one Agent114 control script, and this report. The root
README and RESULTS files are unchanged.

## Verification

Run from the repository root with the repository Lean 4.19.0 toolchain:

```bash
LEAN_NUM_THREADS=1 python3 tools/verify.py --changed
python3 calculation/agent-114/uniform_exterior_controls.py
python3 -O calculation/agent-114/uniform_exterior_controls.py
```

The literal required gate passed against pinned `origin/main`
`eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`:

```text
[rules] 5229 Lean files, 306 projects, OK
[changed] against origin/main: 12 new/changed Lean file(s);
          building 12 module(s); auditing 5 project(s)
[build] OK
[kernel replay] 12 module(s) re-checked by lean4checker
[axioms] 86 endpoints checked
ALL CHECKS PASSED (changed files only, against origin/main)
```

Of these, three modules and 19 endpoints are new here. The rest belong to the
stated dependencies. New printed endpoint axiom sets contain only `propext`
and `Quot.sound`; no custom axioms, admissions, or prohibited evaluators occur.

Independent direct `lake env lean` runs used an 8 GiB address-space bound and
a 1200-second timeout per file. Wall times and peak child RSS were measured
with Python `time.monotonic` and `os.wait4`:

| File | Wall time | Peak RSS |
| --- | ---: | ---: |
| `UniformEdge.lean` | 2.061 s | 444,456 KiB |
| `UniformChain.lean` | 1.249 s | 449,040 KiB |
| `Main.lean` | 1.019 s | 446,124 KiB |

## Independent computed controls

**COMPUTED.** The script directly constructs common-width endpoints and sets
the trim from independent whole-integer overflow arithmetic. It uses the
earlier credited arithmetic/literal-chain utilities, checks the raw length law,
and independently compares all relevant original/transformed edges and cycles
against `calculation/neutral_band_search.py`. It does not read Agent119's proof
as an oracle. Explicit exceptions remain active under `python3 -O`.

Both normal and optimized runs printed identical totals and
`ALL UNIFORM EXTERIOR CONTROLS PASSED`:

| Coverage | Count |
| --- | ---: |
| Exhaustive Hyp-valid sources, bases 2–5, `|B|,|C|<=2` | 5,282 |
| Original edges, every legal partial exterior/center trim | 7,228 |
| These edges at three permitted widths | 21,684 |
| Known source bases / original certificate edges | 8 / 56 |
| Known cycles at minimum width and offsets 1,8,257 | 32 |
| Canonical cycles at minimum width and offsets 1,8 | 24 |
| All equal-total schedules / retimed fixed-width cycles | 252 / 1,512 |
| Doubled source cycles with concentrated trim four | 16 |
| Rotated prefixes, including empty and full prefixes | 504 |
| Total accepted-edge / chain / accepted-cycle checks | 37,925 / 2,119 / 1,640 |
| Mirror edge / cycle comparisons | 75,850 / 4,238 |
| Empty-chain checks / valid zero-width controls | 87 / 31 |
| Zero-width positive-target rejections | 31 |
| Malformed or undersized edge / chain rejections | 20 / 8 |

Known controls cover bases 2,4,8,11,16,17,26,32. Retimed fixtures include
unequal original widths and natural exterior trims above one. The chain
checks additionally verify exact endpoints, all three stream components,
idempotence, and the open-chain balance

```text
oldGain + |oldEndB| = newGain + |oldStartB|.
```

These are regression counts, including repeated fixtures and rotated full
prefixes, not numbers of newly discovered certificates. The independent runs
took 14.008 s normal / 9.978 s optimized, with peak RSS below 18 MiB.
