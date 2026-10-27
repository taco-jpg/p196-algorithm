# Agent 119 — T3: exact common center-unpadding

## Result 和 dependencies

**LEAN-VERIFIED:** symmetric neutral center padding preserves **and reflects**
the unchanged A120 source hypotheses 和 checked edges. Applying one common
padding depth to every source/target center preserves **and reflects** the
complete original `chainOK` 和 `cycleOK` predicates.

This supplies a formal cancellation foundation for Agent7's paper normalization
([#315](https://github.com/taco-jpg/p196-algorithm/pull/315)) 和 Agent117's
common-padding reduction
([discussion](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433125752)).
The paper mathematics remains credited to those authors.

This is a **stacked** contribution depending on Agent119's local forward API in
[#374](https://github.com/taco-jpg/p196-algorithm/pull/374), parent commit
`f182aa81cdb4040f6237401bced19fbb863adf4f`. It does 不 depend on PR339.
Coordination [claim](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433187397).

## Exact equivalences

Write `P_a(C)=(b-1)^a ++ C ++ (b-1)^a`. The registered inverse endpoints prove

\[
\operatorname{Hyp}(b,B,P_a(C))\iff\operatorname{Hyp}(b,B,C).
\]

For an arbitrary edge `E=(B,C,B2,C2,u,v)`, natural padding depths `a,a'`, 和
natural replacement trim `w`, assume the exact balance `a+v=w+a'`. Then

\[
\operatorname{edgeOK}(b,(B,P_a(C),B_2,P_{a'}(C_2),u,w))=\mathrm{true}
\iff \operatorname{edgeOK}(b,E)=\mathrm{true}.
\]

The theorem reflects the **entire** checker, including both coefficient bounds,
base admissibility, nonzero exterior-head condition, carry flip, 和 both exact
successor equalities. It does 不 merely cancel the final word equation.

Define `padEdges b a es` by replacing every edge with
`transportEdge b a a E.v E`. Both trims 和 every exterior word are retained.
The main registered endpoint is:

```lean
theorem cycleOK_padEdges_iff (b a : Nat) (es : List Edge) (B C : List Nat) :
    cycleOK b (padEdges b a es) B (padC b a C) = true ↔
      cycleOK b es B C = true
```

The analogous `chainOK_padEdges_iff` includes empty/nonclosed chains. The cycle
statement includes nonemptiness, every initial/internal seam, both final
interface closures, 和 the overflow/gain inequality. Padding injectivity means
an invalid seam cannot become valid through this transformation.

The results allow arbitrary widths, zero padding, empty exteriors, nonsymmetric
centers, 和 nonmaximal trims. They quantify over natural bases; invalid bases
remain rejected by the original checker. `not_Hyp_neutral_center` separately
proves that an all-neutral center of **any** length cannot flip the carry;
`Hyp_center_ne_nil` includes the empty-center case.

## Why the converse is sound

The forward covariance theorem assumes `Hyp` of the unpadded source. That
assumption cannot be reused to prove its own converse. `Inverse.lean` first
proves the normalization formula using only `b>=2` 和 coefficient bounds:

\[
\operatorname{norm}(P_a C,e_1)
 =(x^a\mathbin{++}D_C\mathbin{++}y^a,e_2).
\]

Both carries remain in `{0,1}` by the existing `norm_carry_le_one`. Therefore
outgoing-carry invariance holds before the flip condition has been established.
Bounds on the padded word imply bounds on its middle subword, allowing the
original `Hyp` to be reconstructed without circular reasoning.

For an accepted transported edge, the restored source `Hyp` permits use of
forward covariance. The center equality becomes

\[
P_a(F(C))=P_{w+a'}(C_2)=P_{a+v}(C_2)=P_a(P_v(C_2)).
\]

Cancelling the identical prefix 和 suffix yields the original edge equation.
The original exterior equation follows from exterior invariance.

`Main.lean` inducts over the edge list. It preserves length, final exterior,
final padded center, 和 `sumGain` structurally. `sumGam` is preserved under the
restored checked-chain hypothesis. The reverse cycle proof restores that chain
**before** using overflow invariance; it then checks every original acceptance
clause. No checker definition is modified.

## Validation

```bash
LEAN_NUM_THREADS=1 python3 tools/verify.py --changed
python3 calculation/agent-119/center_unpadding_controls.py
python3 -O calculation/agent-119/center_unpadding_controls.py
```

The combined stack against main contains 5,222 Lean files / 303 projects.
The required gate builds 和 kernel-replays five changed modules (three from
#374, two new here) 和 audits 36 endpoints, including the 18 new endpoints.
Publication requires the actual `ALL CHECKS PASSED` terminal result. New
endpoints use only `propext` 和 `Quot.sound`.

Direct stock Lean4.19 per-file checks, one thread, 8 GiB address-space ceiling
和 1,200-second timeout:

| New module | Wall seconds | Peak RSS, KiB |
|---|---:|---:|
| Inverse | 0.515 | 444936 |
| Main | 0.518 | 447960 |

**COMPUTED finite controls:** both normal 和 optimized Python pass identical
counts. The unchanged mirror checks Hyp, edges, 和 complete cycles. A local
chain adapter follows the original A120 seam/edge recursion; it is labelled an
adapter, 不 a separately proved checker.

| Comparison pairs | Total | Accepted originals | Rejected originals |
|---|---:|---:|---:|
| Hyp | 22796 | 4580 | 18216 |
| Balanced local edges | 333664 | 2504 | 331160 |
| Common-padding chains | 2560 | 2248 | 312 |
| Common-padding cycles | 2560 | 256 | 2304 |

The edge controls include 315,612 independently selected source/target pairs
(14 accepts), rather than only constructed successors. The eight existing
certificate bases provide 56 original edges. Eight malformed-seam controls
retain individually valid edges; 32 accepted padded-cycle pairs have a center
trim greater than one. Explicit failure guards remain active under `python -O`.
Independent source review of the chain/cycle proof passed.

## Boundary

This proves removal of a **common specified padding depth**, preserving every
trim. It does 不 select a maximal strip for each phase, prove a canonical
deterministic quotient, or implement Agent117's automaton subtraction. Agent104
retains phase-dependent equal-total center-schedule transport; Agent114 retains
exterior transport. 没有 new decimal certificate, center nonexistence result,
or unrestricted decimal impossibility theorem is claimed.
