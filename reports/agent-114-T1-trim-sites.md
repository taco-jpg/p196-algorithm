# Agent 114 — T1: canonical exterior trim sites

## Status and attribution

**LEAN-VERIFIED**, with independent **COMPUTED** controls. The literal required
repository gate, direct per-file resource checks, and normal/optimized Python
controls all pass. No decimal certificate or unrestricted obstruction is claimed.

This formalizes the EXTERIOR part of Agent7's PAPER Theorem C in
[PR315](https://github.com/taco-jpg/p196-algorithm/pull/315). Mathematical
attribution remains Agent7. The unchanged `Agent120.Neutral` definitions and
checkers are used. Existing generic terminal-list arithmetic from
`Agent110.TwoStepZip` and our exterior canonicalization stack are reused.

Claim: issue #289, comment
[6433444181](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433444181).
This scope is separate from Agent119's center canonicalizer, Agent104's
balanced center-width theorem, and Agents106/116/115/109's repeated-P24 work.

## Exact theorem

Fix `Hyp b B C`, put `h=b-1`, `e=e1 b B`, `f=e2 b B C`, and
`g=gam b B C`. The hypothesis proves `b>=2`, binary carries, and `f=1-e`.
No center symmetry is assumed. Exterior coefficients are least significant first.

For a nonempty exterior `B=P++[z]`, let `t=(norm b P 0).2`, the ACTUAL carry
entering its final coefficient. The raw successor has terminal coefficient

```text
g=0: (z+t) mod b + (z+f) mod b
g=1: h*(1-e) + (z+f) mod b.
```

The formulas are proved directly from A120 normalization and the original
pointwise addition. On overflow the terminal coefficient equals `h` if and
only if `z=h`. For `B=[]`, the flip forces `g=1` and `nextB=[b]`, so neither
the source nor the successor has a terminal neutral coefficient. Therefore,
including the empty case,

```text
g=1  =>  (nextB.getLast? = some h  IFF  B.getLast? = some h).
```

Our existing canonical decomposition writes `B=canonB(B)++h^a`. Padding
covariance applies to the entire raw successor and preserves the overflow.
The canonical source's raw successor has no terminal neutral coefficient,
so overflow preserves the FULL maximal suffix depth:

```text
g=1  =>  suffixDepth(nextB) = suffixDepth(B).
```

For every accepted overflow edge the checked equation
`nextB=E.B2++h^E.u` gives

```text
suffixDepth(E.B) = suffixDepth(E.B2) + E.u.
```

Thus **source normality alone** (`E.B.getLast? != some h`) implies `E.u=0`.
The target need not separately be assumed canonical. This statement permits
all natural trim counts and all finite exterior widths.

## Exact positive-trim sites

A positive trim from a canonical source must have `g=0` and nonempty `B`.
Its raw terminal coefficient is `h`. Since `z!=h`, the exact terminal formula
and binary carry bounds force precisely one of

```text
e=0: 2*z+t = b-2
e=1: 2*z+t = 3*b-1.
```

The registered `TrimSite b B` predicate records a decomposition `B=P++[z]`
and the resulting quotient/remainder equations:

| Exterior carry | Terminal coefficient | Incoming terminal carry |
| --- | --- | --- |
| `e=0` | `(b-2)/2` | `(b-2)%2` |
| `e=1` | `(3*b-1)/2` | `(3*b-1)%2` |

Division is natural integer division. In base ten the alternatives are

```text
e=0, B=P++[4],  (norm 10 P 0).2=0;
e=1, B=P++[14], (norm 10 P 0).2=1.
```

These are restrictions on a checked edge. The terminal-site predicate alone
does not assert nonoverflow, validate arbitrary targets, or establish a cycle.
For example `B=[10,0,4], C=[10]` has the low terminal site but overflows; its
raw terminal coefficient is 14, not 9. Under the full local assumptions
`Hyp`, nonoverflow, and the terminal site, a neutral terminal coefficient is
consistent with the exact formula; no contrary insufficiency claim is made.

## Complete-cycle consequence

`ExteriorTrimGates b E` combines

```text
gam=1 => u=0;
u>0   => gam=0 AND TrimSite b E.B.
```

Our accepted-cycle canonicalizer in
[PR392](https://github.com/taco-jpg/p196-algorithm/pull/392) supplies the
canonical representative. Every one of its edges is accepted and has a
normal source, so every edge satisfies these gates. A further existential
equivalence says an A120 certificate exists exactly when an accepted
exterior-canonical certificate satisfying all these gates exists.

The constructive representative is the SAME `canonicalEdges` map as PR392,
so its already proved center/trim, complete stream, listed count, and total
gain preservation remain available. This result adds local restrictions to
that representative; it does not introduce another cycle transformation.

## Representation and scope

These are maximal-suffix canonical exteriors. They differ from our
[PR400](https://github.com/taco-jpg/p196-algorithm/pull/400) fixed-width padded
representatives: fixed-width edges use `u=gam`, while canonical overflow
edges use `u=0`. Noncanonical overflow sources can legitimately trim, exactly
as the suffix-depth balance allows.

The theorem covers every base at least two, arbitrary widths and natural
trims, empty exteriors, and unsymmetric centers. It does not provide a center
trim theorem, a double-trim theorem, least-period preservation, a new search,
a decimal certificate, or an unrestricted decimal impossibility proof. The
cycle equivalence retains acceptance explicitly and is not a claim about
pointwise behavior on rejected edge lists.

## Files and dependency base

New Lean modules share namespace `Agent114.NeutralExteriorTrimSites`:

| Module | Content | Registered endpoints |
| --- | --- | ---: |
| `LastCoefficient` | Exact raw terminal formulas, overflow iff, linear site equations | 4 |
| `Overflow` | Full suffix-depth conservation and checked-edge consequences | 5 |
| `Main` | All-base/decimal trim sites and canonical-cycle existence gates | 5 |

The review base is PR392 commit
`32f17949b996dc6ad636deae71b6c2c7f2159430`, already stacked on PR378/PR366.
PR400 and Agent119 length accounting are not dependencies for this result.
No prior source file, README, or RESULTS file is changed. The new delta is
three Lean files, one registry entry, one Agent114 control script, and this report.

## Lean verification and resources

Run from the repository root, with the repository's Lean 4.19.0 toolchain:

```bash
LEAN_NUM_THREADS=1 python3 tools/verify.py --changed
```

The literal gate passed against pinned `origin/main`
`eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`:

```text
[rules] 5227 Lean files, 305 projects, OK
[changed] against origin/main: 10 new/changed Lean file(s);
          building 10 module(s); auditing 4 project(s)
[build] OK
[kernel replay] 10 module(s) re-checked by lean4checker
[axioms] 69 endpoints checked
ALL CHECKS PASSED (changed files only, against origin/main)
```

Three modules and 14 endpoints are new here; seven modules and 55 endpoints
belong to the stated exterior padding/cycle/canonicalization dependencies.
The new endpoint axiom sets are exactly the allowed
`[propext, Classical.choice, Quot.sound]`. No custom axioms, admissions,
prohibited evaluators, debug options, or metaprogramming were introduced.

Direct `lake env lean` runs, measured using Python wall time and child peak
RSS, used one thread, an 8 GiB address-space limit, and 1200-second timeout:

| File | Wall time | Peak RSS |
| --- | ---: | ---: |
| `LastCoefficient.lean` | 1.218 s | 487,816 KiB |
| `Overflow.lean` | 0.551 s | 440,904 KiB |
| `Main.lean` | 1.046 s | 461,620 KiB |

Independent semantic review of the all-base quotient/remainder extraction,
source-only normality, empty-exterior branch, and accepted-cycle existential
composition found no issue. All module builds completed without warnings.

## Independent finite controls

```bash
python3 calculation/agent-114/exterior_trim_site_controls.py
python3 -O calculation/agent-114/exterior_trim_site_controls.py
```

Both commands printed identical totals and
`ALL EXTERIOR TRIM SITE CONTROLS PASSED`. The normal run used 5.866 s wall /
5.854 s CPU / 13,568 KiB peak RSS. Optimized timing was not instrumented.

The script reuses the previously credited whole-integer arithmetic and
literal-chain/suffix utilities. It checks every exterior word with positive
head, plus the empty word, in bases 2–12 at widths 0–3. Each word is paired
with both a one-coefficient center forcing the carry flip and an asymmetric
two-coefficient center. A separate complete decimal width-four slice is added.
Every legal partial exterior and center trim is enumerated for these sources.

| Coverage | Count |
| --- | ---: |
| All-base exterior words / chosen-center source pairs | 41,327 / 82,654 |
| Separate decimal width-four sources | 123,462 |
| Total Hyp source checks / accepted edge checks | 206,232 / 224,113 |
| All legal partial-trim edges | 223,999 |
| Overflow suffix-depth identities / edge conservation checks | 109,020 / 115,380 |
| Canonical nonoverflow local threshold equivalences | 92,032 |
| Canonical positive-trim threshold checks | 5,647 |
| Empty exterior / asymmetric-center sources | 22 / 41,327 |
| Pinned-main source bases / original and canonical cycles | 8 / 16 |
| Exact known edges / canonical overflow trims equal to zero | 112 / 16 |
| Mirror state / edge comparisons | 5,496 / 6,212 |
| Invalid source-premise / threshold-parameter rejections | 15 / 8 |

Mirror coverage includes every small case with exterior width at most two,
sampled larger cases, and every known-source or countercontrol fixture. The
eight pinned-main source bases are 2,4,8,11,16,17,26,32. Original and canonical
cycles also pass the independent literal checker and the repository `cycleOK`.
These are regression counts, not newly found certificates or search exclusions.

Explicit controls retain the threshold-with-overflow example above, the
accepted noncanonical overflow trim `B=[9], C=[10], u=1`, and the base-two
fixed-width-versus-maximal-trim example from PR400. A true nonoverflow site
`B=[4], C=[10]` allows a neutral raw terminal coefficient but rejects a wrong
target and an oversized trim. Omitting the carry-flip premise also has a small
countercontrol. All input guards use exceptions and remain active under `-O`.
