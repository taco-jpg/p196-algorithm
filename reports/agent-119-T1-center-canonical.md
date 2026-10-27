# Agent 119 — T1: Lean maximal center normalization

## Result 和 attribution

**LEAN-VERIFIED:** every cycle accepted by the unchanged A120 checker maps to
an accepted cycle with maximally stripped centers. The transformation retains
every exterior word, exterior trim, both carry labels, overflow bit, listed
edge count, 和 total gain. Center widths do 不 increase at any listed phase.

This formalizes the **center component** of Agent7's paper normal form
([#315](https://github.com/taco-jpg/p196-algorithm/pull/315)) 和 canonical quotient
([#326](https://github.com/taco-jpg/p196-algorithm/pull/326)). It does 不 claim new
normalization mathematics or the full jointly deterministic B/C quotient.
Agent114's exterior-only canonicalization is the complementary component;
Agent104 retains prescribed center-schedule transport.

The actual stripping algorithm is the existing
`Agent1.Periodic.stripPeriodCenter [b-1] C`. Its decomposition, maximality,
length, 和 wrapper lemmas are reused, along with
`Agent105.AffineNormalize.singleton_pow`. No new stripping loop is introduced
in Lean. The previous Agent1 returned-path integration concerns a different
decimal period-four quotient; this contribution supplies the missing A120
checker bridge.

The PR stacks on [#389](https://github.com/taco-jpg/p196-algorithm/pull/389),
parent `e68ba8e36eb474429bcb47f58e56edd8789b9c16`, including its #374 foundation.
It does 不 depend on PR339, Agent104's schedule implementation, or Agent114's
exterior implementation. Coordination
[claim](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433300439).

## Exact construction

Let `coreC b C` 和 `depthC b C` be the two outputs of the existing stripper.
Writing `P_a(C)=(b-1)^a ++ C ++ (b-1)^a`, the core API proves

\[
C=P_{d(C)}(\widehat C),\qquad
\widehat{P_a(C)}=\widehat C,\qquad d(P_a(C))=a+d(C).
\]

The core has no further complete neutral pair: there is no word `D` with
`coreC b C = P_1(D)`. This is the exact meaning of maximality; it does 不 assume
symmetry or assert that both endpoints of an arbitrary word are nonneutral.
`Hyp b B (coreC b C)` is equivalent to the original `Hyp b B C`.

For an original edge `E=(B,C,B2,C2,u,v)`, the new edge keeps `B,B2,u` 和 uses
the two cores. Its center trim is defined **from the actual raw successor**:

\[
\widehat v=d\bigl(\operatorname{nextC}(b,B,\widehat C)\bigr).
\]

The definition never uses an unchecked truncated natural subtraction. For an
accepted original edge, the formal bridge proves

\[
\widehat{\operatorname{nextC}(b,B,\widehat C)}=\widehat C_2,
\qquad d(C)+\widehat v=v+d(C_2).
\]

Thus the target is exactly the raw center's maximal stripped core, 和 the
new trim is its actual maximal strip count. `normalizeEdge_ok` proves acceptance
by the complete unchanged Boolean checker. The local theorem requires no
validity hypothesis on the target; it works for accepted nonclosed edges too.

## Complete-cycle theorem

`normalizeEdges b es` applies the transformation pointwise. Its main endpoint is

```lean
theorem cycleOK_normalize {b : Nat} {es : List Edge} {B C : List Nat}
    (h : cycleOK b es B C = true) :
    cycleOK b (normalizeEdges b es) B (coreC b C) = true
```

The list proof retains nonemptiness, every seam, both interface closures,
overflow total, 和 the original gain inequality. For an open checked chain,
the precise accounting identity is

\[
\operatorname{gain}(\widehat{es})+d(C_0)
=\operatorname{gain}(es)+d(C_P).
\]

Closing the center cancels the endpoint depths, so total gain is unchanged.
Both carries 和 overflow are preserved at every listed edge; exterior words
和 exterior trim are unchanged by construction. `core_length_le` together with
the ordered width-map identity proves pointwise nonincrease of center widths.

Normalization is idempotent. A checked list whose source 和 target centers
already have depth zero is fixed by the transformation. The preserved period
is the **listed edge count**; minimal or primitive period may become smaller.
The theorem covers arbitrary admitted bases, widths, periods, natural trims,
empty exteriors, 和 nonsymmetric centers, without any decimal specialization.

## Why acceptance is only claimed forward

Maximal stripping is many-to-one. A malformed seam can join centers with
different neutral depths but the same core, 和 normalization can repair it.
Therefore an arbitrary-input `cycleOK(normalize es) iff cycleOK(es)` would be
false, unlike the earlier **common fixed padding** equivalence in #389.

**COMPUTED explicit counterexample:** take the existing four-edge base-two
certificate 和 pad only its first edge's source 和 target centers by one pair.
Every local edge remains accepted. Its first bad seam is

```text
previous target center = [1, 2, 0, 2, 1]
next source center     = [2, 0, 2]
```

Both original `chainOK`/`cycleOK` reject; normalization returns exactly the
original base-two certificate 和 both accept. The script emits the full
before/after Boolean result. This is a counterexample to an overstrong API
claim, 不 a new nondecimal or decimal certificate.

## Proof structure 和 validation

`Core.lean` connects the existing generic stripper to neutral padding.
`Edge.lean` applies core/count covariance to the exact original output equation,
proves natural trim balance, 和 restores `edgeOK`.
`Main.lean` inducts over checked chains 和 telescopes the depth balance.
The three new modules register 32 public theorem endpoints.

```bash
LEAN_NUM_THREADS=1 python3 tools/verify.py --changed
python3 calculation/agent-119/center_canonical_controls.py
python3 -O calculation/agent-119/center_canonical_controls.py
```

The combined stack against main contains 5,225 Lean files / 304 projects.
The required gate builds 和 kernel-replays eight changed modules (five parents,
three new here) 和 audits 68 endpoints, including the 32 new endpoints.
Publication requires the actual terminal result `ALL CHECKS PASSED`.
New endpoints depend only on the permitted `propext` 和 `Quot.sound` axioms.

Stock Lean4.19, one thread, 8 GiB address-space ceiling 和 1,200-second timeout
were used. The first build of the existing generic dependency closure took
138.836 seconds, peak 2,323,248 KiB. This is unchanged dependency work, 不 a
new theorem's direct compilation time. New-module measurements:

| Module | Wall seconds | Peak RSS, KiB |
|---|---:|---:|
| Core, direct compile | 1.484 | 486036 |
| Edge, build including a Core rebuild | 1.993 | 476708 |
| Main, direct compile | 1.963 | 477080 |

**COMPUTED finite controls:** normal 和 optimized Python agree on:

| Scope | Exact controls |
|---|---|
| Independent stripping | 3,533 words; two-index loop, end-run formula, 和 mirror trim agree |
| Accepted edge normalization | 494 edges; 330 nonmaximal input trims; 104 changed trims |
| Boundary sources | 21 empty exteriors; 35 nonsymmetric centers; 20 trims greater than one |
| Accepted cycle normalization | 48 cycles / 448 listed edges; 24 phase-dependent padding cases |
| Strict width reduction | 43 cycles have smaller aggregate interface width |
| Existing certificates | Eight baseline bases / 56 original edges |
| Invalid-input scope control | One repaired-seam counterexample; four individually valid edges |

Every accepted control checks the actual raw-successor trim, exact depth
balance, original checker acceptance, maximality, idempotence, carry/overflow
labels, exterior data, listed length, 和 total `u/v/gain`. Explicit guards stay
active under `python -O`. These finite controls do 不 replace the general Lean
proof. Independent source review checks the gain sign 和 complete-cycle scope.

## Boundary

This is center-only maximal normalization of accepted A120 certificates. It
does 不 select exterior trims, prove that arbitrary normalized malformed input
reflects original acceptance, or settle any fixed driver. 没有 decimal cycle,
all-width center exclusion, or unrestricted one-band impossibility is claimed.
