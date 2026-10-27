# Agent 119 — T3 signed center trims and weighted chains

Claim: T3.lean-center-trim-numeric-chain, issue #289, comment6433651344.

## Result and scope

**LEAN-VERIFIED + COMPUTED.**

This result extends Agent112's verified **raw** numerical center update
through the actual accepted neutral trim, then through a complete checked
chain. Every accepted center-closed chain satisfies an exact integer
identity and its divisibility consequence. The original `edgeOK`, `chainOK`
and `cycleOK` are unchanged.

The result is a necessary arithmetic condition on actual coefficient data.
It gives no scalar-to-literal converse, no numerical-cycle realization,
no driver-only obstruction, no new search exclusion, and no decimal
certificate or unrestricted impossibility theorem. Symmetry, maximal trims,
positive center width and target `Hyp` are not added as premises.

## Attribution and exact dependencies

- Agent112's paper numerical model #349 already contains the signed
  neutral-padding scaling law and integer successor. The broader numerical
  cycle realization theorem is paper work in #368, not reproved here.
- Agent112's verified raw formula is imported from #398, pinned head
  `cc1ffbce28372cc93ecd460402290a75157570cf`.
- Agent7's paper neutral padding is formalized by the imported Agent119
  padding API #374, pinned head `f182aa81cdb4040f6237401bced19fbb863adf4f`.
- The existing A120 normalizer, value function, fixed-width digit extraction,
  `signedValue`, list algebra and checker equations are all reused.

The integration base has both exact dependency commits as parents. Its tree
is `f824a7f6eeb4397229ba52701134ba6929255a73`; the registry is the exact
union of unchanged entries, and no dependency source is edited.

The new delta is two registered Lean modules, an independent control script,
this report and an additive registry entry. It does not depend on the joint
canonicalizer #418 or change other agents' claimed work.

## Exact arithmetic

Use the existing signed center value

\[
Z(C)=\operatorname{val}_b(C)+1-b^{|C|}\in\mathbb Z.
\]

For arbitrary coefficient lists and every base b>=1,

\[
\boxed{Z(\operatorname{padC}_b(v,C))=b^v Z(C).}
\]

A private single-pair calculation uses `val_cons` and `val_append`, followed
by induction through the existing `padC_add`. No new normalizer or stripper
is implemented. Base one is included; base zero is excluded from this
unrestricted padding identity.

For an accepted edge, write m=|C|, N=val(C), e=e1(b,B), g=gam(b,B,C),
and let R_m(N+e) be the value of the **reversed fixed-width digit list**,
retaining leading zero padding and discarding carry above width m. Define

\[
\Delta(B,C)=b^g\bigl(R_m(N+e)+e(b^m+1)-b^m\bigr).
\]

All subtraction is integer subtraction. Agent112's raw formula, the actual
checker equation `nextC=padC b v C2`, and the scaling lemma give

\[
\boxed{b^v Z(C_2)=Z(C)+\Delta(B,C).}
\]

The less restrictive endpoint `trimmed_signed_update` requires source
`Hyp` and only the literal center equation. `edge_signed_update` obtains
both premises directly from `edgeOK_sound`.

## Chain telescope and cycle constraint

Let V=sum_i v_i, P_i=sum_{j<i} v_j, and

\[
W=\sum_i b^{P_i}\Delta(B_i,C_i).
\]

The executable recursion is `W(E::es)=Delta(E)+b^E.v*W(es)`.
`trimTotal` uses the standard list sum, not a duplicate trim-counter
implementation. Concatenation laws are proved for both totals and weights.
For every chain accepted from (B,C),

\[
\boxed{b^V Z(C_{\rm final})=Z(C)+W.}
\]

Only literal center closure is needed to obtain

\[
\boxed{(b^V-1)Z(C)=W,\qquad (b^V-1)\mid W.}
\]

Exterior closure, positive gain and nonemptiness are not needed for these
center-closed-chain endpoints. The cycle corollaries retain the full
original `cycleOK` premise. Conversely, failed divisibility proves that
original `cycleOK` returns false; successful divisibility proves no acceptance.

Empty chains work at every natural base. At V=0, the closed identity forces
W=0, and divisibility means 0 divides 0. No division or hidden positive-V
assumption is used. The source-dependent reversal term is retained, so
fixing only the e/g/v streams does not determine W.

## Lean endpoints

Namespace: `Agent119.NeutralCenterNumericChain`.

| Module | Endpoints | Main contracts |
|---|---:|---|
| `Trim` | 5 | Integer scales, signed padding, source-Hyp/literal-trim and accepted-edge updates |
| `Chain` | 9 | Concatenation, open/closed weighted identities, zero-trim case, divisibility and checker rejection |

The root is `P196.Agent119NeutralCenterNumericChain.Chain`.
Fourteen new endpoints are registered. The only arithmetic coordinate is
Agent112's existing `signedValue`; the permitted inherited axioms include
`propext`, `Classical.choice` and `Quot.sound`.

## Independent finite controls — COMPUTED

Exact commands from the repository root:

```bash
python3 calculation/agent-119/center_numeric_chain_controls.py
python3 -O calculation/agent-119/center_numeric_chain_controls.py
```

Both pass with identical output in approximately 0.11–0.14 seconds. Explicit
failure checks remain active under `-O`. Whole-integer quotients independently
calculate e/e2/g; fixed-width reversal is checked in two ways. Literal mirror
acceptance is checked before arithmetic. Forward prefix accumulation agrees
with a separately evaluated backward recursive weighted sum.

| Completed control | Count |
|---|---:|
| Known fixture bases / original edges | 9 / 64 |
| Positive-base padding cases / base-one subset | 148 / 20 |
| Accepted edges / nonmaximal trims | 682 / 409 |
| Empty exteriors / nonsymmetric source centers | 35 / 74 |
| Invalid-Hyp targets / zero signed-value targets | 50 / 22 |
| Accepted chains / empty chains | 105 / 21 |
| Zero-total-trim chains / nonempty open subset | 47 / 26 |
| Checked prefix identities | 700 |
| Closed identities / zero-factor cases | 75 / 21 |
| Accepted cycle variants / listed edges | 54 / 512 |
| Phase-dependent cycle variants | 27 |
| Rejected malformed edges / chains / cycles | 8 / 2 / 2 |

The original eight fixtures come from the unchanged mirror; the ninth is
Agent116's base20 certificate #356. Its literal source and pinned SHA-256
are read from the imported Agent112 fixture, then its eight transitions are
reconstructed with the mirror and digest-checked. No parent arithmetic code
is imported or executed by the new control script.

The supplied decimal P24 center is separately replayed with prescribed e/g/v:
24 steps, V=4, Z0=549450, weighted increment5493950550. Its closed identity is
`9999*549450=5493950550`. This is explicitly CENTER ONLY, with no B or full
cycle claim. Agent101 retains discovery attribution; the reported one-lap
exterior exclusion is not contradicted by this arithmetic positive control.

These are finite controls, not an exhaustive search or a numerical realization
proof. They deliberately retain source-valid edges whose targets are invalid.

## Limits demonstrated by concrete controls

1. At b=0, v=1, C=[], the padded signed value is1 whereas b^v Z(C)=0.
   This is why unrestricted padding explicitly requires b>=1.
2. The accepted decimal edge ([1],[10])->([3],[0]), with zero trims, has
   a target that fails `Hyp`. Its arithmetic identity still holds.
3. Decimal sources B=[1], C=[10] and C=[11] have the same width and
   e/g/v=(0,0,0), but increments -10 and -9. The law is not driver-only.
4. At b=10, source B=[1], C=[0,10,10,18] has genuine target
   B2=[3], C2=[1,1], u=0, v=1. Replacing C2 with [11,0] keeps width2,
   value11 and the scalar identity `10*(-88)=9101-9981=-880`, while
   failing the literal center equation and `edgeOK`.
5. A wrong v can pass the scalar identity when Z(target)=0. A malformed
   exterior seam can preserve a closed center arithmetic trace while the
   original chain and cycle both reject. Literal acceptance and consistent
   seams remain necessary.

Agent112's separate bounded symmetric trim-converse task addresses additional
hypotheses for a literal removal. No such converse is inferred here. The
Manager's frozen-itinerary linear/gcd certificates concern different data;
this work supplies no row compiler, elimination algorithm or certificate.

## Verification and resources

The unmodified mandatory command was run from a clean isolated checkout
containing the exact result sources and both unchanged dependency stacks:

```bash
LEAN_NUM_THREADS=1 python3 tools/verify.py --changed
```

It returned `ALL CHECKS PASSED`: 5,225 Lean files and304 projects satisfy
repository rules; eight modules were built and replayed by stock
`lean4checker`; 51 endpoints were audited across three projects. Wall time
45.805 seconds, peak child RSS414,860 KiB, exit0. All endpoint axioms are
permitted. No verifier, checker, dependency source or allow-list was changed.

Stock Lean4.19.0 was used with one thread, an8GiB address-space cap and a
1200-second timeout. Final direct compile times were1.153 seconds for Trim
and0.959 seconds for Chain; cumulative peak child RSS454,008 KiB bounds
both runs. Both exit codes were0. The final optimized Python controls also
pass in the isolated checkout, with the same output as normal execution.

Freshly fetched main remained
`eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`. The staged isolated tree and
publication tree are checked for exact equality before upload.

Independent read-only review found no issue in the direction of the scaled
update, prefix weighting, closure/divisibility implications, or empty/base-one/
zero-trim/invalid-target boundaries. Decimal certificate existence and the
unrestricted neutral-band route remain open.
