# Agent 114 — exterior canonicalization of accepted A120 certificates

## Result and dependencies

**LEAN-VERIFIED:** every accepted A120 cycle has an accepted representative
whose exterior words are empty or end in a coefficient different from `b-1`.
The exterior trim at each normalized edge is the uniquely forced maximal
neutral suffix depth of its actual raw successor. Its natural shift formula
is proved nonnegative. Centers and center trims, listed edge count, complete
carry/overflow streams, and total gain are preserved.

This formalizes the exterior portion of Agent 7's PAPER normalization and
canonical quotient in [PR 315](https://github.com/taco-jpg/p196-algorithm/pull/315)
and [PR 326](https://github.com/taco-jpg/p196-algorithm/pull/326).
The mathematical reduction is credited; no new normalization discovery is
claimed. Agent 107's retiming arguments and controls remain credited in the
supporting regression code.

This review stacks on [PR 378](https://github.com/taco-jpg/p196-algorithm/pull/378),
commit `01fa5029d7e0186a9368c1195e92e09e913052a2`, which depends on
[PR 366](https://github.com/taco-jpg/p196-algorithm/pull/366).
Main baseline: `eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`.
The original A120 checker and other agents' source files are unchanged.

## Reused suffix machinery

The new code uses the existing `P196.Agent7.Finite.stripSuffix`; it introduces
no second stripping implementation in Lean. Generic decomposition,
idempotence, length, and terminal-symbol facts are imported from
`Agent6CertificateCoordinateAudit.OuterBridge` and `ExteriorNormalization`.
Only their generic list statements are used, not their older decimal-phase
transition theorems.

For neutral coefficient `h=b-1`, define

```text
K(B) = stripSuffix h B
q(B) = |B| - |K(B)|.
```

The registered facade proves exact decomposition, including empty and
all-neutral words:

```text
K(B) ++ h^q(B) = B
K(B ++ h^a) = K(B)
q(B ++ h^a) = q(B) + a
K(K(B)) = K(B)
q(K(B)) = 0
K(B) = B <-> B.getLast? != some h
Hyp b (K(B)) C <-> Hyp b B C.
```

The generic list statements permit arbitrary natural `b`; acceptance of a
nonempty A120 chain supplies `b>=2` through the unchanged `Hyp`.
No center-symmetry assumption is added.

## One-edge normalization and forced trim

For an accepted original edge `E`, let

```text
R = nextB b (K(E.B)) E.C
U = q(R).
```

`canonicalEdge` replaces `B` and `B2` by their `K` values and `u` by `U`,
leaving `C`, `C2`, and `v` unchanged. Suffix covariance gives

```text
R ++ h^q(E.B) = E.B2 ++ h^E.u.
```

Applying `K` and `q` separately proves

```text
K(R) = K(E.B2)
q(E.B) + U = E.u + q(E.B2)
q(E.B) <= E.u + q(E.B2)
U = E.u + q(E.B2) - q(E.B).
```

Thus the subtraction has no negative case. The original edge is exactly
`padEdge` applied to its canonical edge, so the established checked-edge
equivalence proves canonical acceptance. Also

```text
R = K(E.B2) ++ h^U.
```

Every other natural `w` satisfying this same normalized-target decomposition
equals `U`. This is the required uniqueness, not merely a chosen trim bound.

## Complete chains and cycles

`canonicalEdges` maps the edge normalization without changing order.
For an accepted chain starting at `(B,C)`, the proof constructs

```text
PadChain b (q(B)) (q(endB es B)) (canonicalEdges b es) es.
```

The canonical list is the unpadded side; the original list is its padded side.
The reverse direction of the verified `chainOK` equivalence therefore proves
acceptance of the canonical chain. Closed original endpoints make the two
offsets equal, so the reverse `cycleOK` equivalence gives the complete cycle.

Registered endpoints additionally prove unchanged center data, list length,
the exact `(e1,e2,gam)` sequence, overflow total, and closed-cycle gain. The
existential endpoint `cycle_exists_iff_exterior_normal` states that an
accepted cycle exists exactly when an exterior-normalized accepted cycle
exists. It imposes no finite width or period cap.

## Why acceptance is a necessary premise

**COMPUTED counterexample:** in base 2, the following four local edges all
pass `edgeOK`, but the first target exterior differs from the second source:

| Edge | B | C | B2 | C2 | u | v |
| --- | --- | --- | --- | --- | ---: | ---: |
| 0 | `[2]` | `[0,0]` | `[1,0]` | `[2,0,2]` | 0 | 0 |
| 1 | `[1,0,1]` | `[2,0,2]` | `[2]` | `[0,2,0]` | 2 | 0 |
| 2 | `[2]` | `[0,2,0]` | `[1,0]` | `[2,1,1,2]` | 0 | 0 |
| 3 | `[1,0]` | `[2,1,1,2]` | `[2]` | `[0,0]` | 1 | 1 |

Starting at `B=[2], C=[0,0]`, both the chain and cycle checks reject this list.
Canonicalization erases the extra terminal 1 on edge 1, changes its trim to
1, and restores the known accepted four-edge base-2 cycle. Total gain changes
from 4 to 3. Independent arithmetic and the original mirror agree.

Accordingly, no unconditional pointwise checker equivalence or gain
preservation is asserted for arbitrary rejected lists. The proven statements
use accepted chains/cycles, and the existence equivalence is existential.

## Lean verification

Project `Agent114NeutralExteriorCanonical` registers three modules and 27
endpoints in `lean/registry.json`:

```text
P196.Agent114NeutralExteriorCanonical.SuffixNormalization
P196.Agent114NeutralExteriorCanonical.CanonicalEdge
P196.Agent114NeutralExteriorCanonical.CanonicalCycle
```

Commands, from the repository root with Lean 4.19.0 on `PATH`:

```bash
export LEAN_NUM_THREADS=1
ulimit -v 8388608
cd lean
timeout 1200 lake build P196.Agent114NeutralExteriorCanonical.CanonicalCycle
cd ..
timeout 1200 python3 tools/verify.py --changed
```

Actual combined gate, including unmerged parents 366 and 378:

```text
[rules] 5224 Lean files, 304 projects, OK
[changed] against origin/main: 7 new/changed Lean file(s); building 7 module(s); auditing 3 project(s)
[build] OK
[kernel replay] 7 module(s) re-checked by lean4checker
[axioms] 55 endpoints checked
ALL CHECKS PASSED (changed files only, against origin/main)
```

The new contribution supplies 3 of those modules and 27 of the endpoints;
the parents supply 4 modules and 28 endpoints. Every endpoint satisfies the
allowed-axiom policy. The printed new endpoints depend only on
`[propext, Quot.sound]`; no forbidden mechanism is used.

Separate one-thread `lake env lean` checks, each under the 8 GiB address-space
limit and 1,200-second timeout:

| File | Exit | Wall seconds | Peak RSS KiB |
| --- | ---: | ---: | ---: |
| `SuffixNormalization.lean` | 0 | 0.530 | 455248 |
| `CanonicalEdge.lean` | 0 | 0.713 | 453548 |
| `CanonicalCycle.lean` | 0 | 0.616 | 446192 |

Measurements use `time.monotonic` and per-child `os.wait4` because
`/usr/bin/time` is unavailable. All files meet the required budgets.

## Independent arithmetic regression — COMPUTED

```bash
python3 calculation/agent-114/exterior_canonical_controls.py
python3 -O calculation/agent-114/exterior_canonical_controls.py
```

Both final runs print identical counters and
`ALL EXTERIOR CANONICAL CONTROLS PASSED`.
The script reuses the prior independent whole-integer edge arithmetic and
literal chain verifier; maximal suffix removal and all literal suffix splits
are independently implemented and compared.

| Coverage | Exact count |
| --- | ---: |
| Exhaustive Hyp sources, bases 2–5, B<=2, C<=3 | 44812 |
| Accepted edges covering every legal partial u/v trim in that domain | 62492 |
| Accepted edge controls overall / mirror edge comparisons | 69416 / 138832 |
| Edges with nonmaximal original exterior trim | 14723 |
| Empty original / canonical source exterior cases | 810 / 4860 |
| Empty canonical target cases | 1230 |
| Nonsymmetric center edge cases | 54568 |
| Existing source bases / source edges | 8 / 56 |
| Equal-total schedules / retimed cycles | 252 / 504 |
| Additional constant-padding cycles, depths 1,8,257 | 24 |
| Accepted-cycle checks / chain checks / empty chains | 592 / 1040 / 56 |
| Mirror cycle comparisons | 2082 |
| Malformed edge / list / suffix guards | 18 / 3 / 9 |

The 592 cycle checks include full-length rotated prefixes; they are not 592
distinct new certificates. Every tested accepted edge also passes exact
restoration, maximal-trim uniqueness, idempotence, and carry/overflow checks.
The counterexample above and the empty-cycle rejection are retained. All
acceptance and failure guards remain active under optimized Python.

## Limits

This is exterior-only canonicalization. It does not normalize center ends,
identify the least temporal period, prove overflow-site trim restrictions,
or supply a new certificate or search exclusion. No decimal Lychrel
existence or unrestricted one-band impossibility result is claimed.
