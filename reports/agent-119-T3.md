# Agent 119 — T3: Lean center-padding covariance

## Result 和 attribution

**LEAN-VERIFIED local foundation:** symmetric neutral padding preserves the
unchanged Agent120 source hypotheses, exterior transition, carry, 和 overflow.
The raw center successor commutes with padding. A checked edge transports to
new source/target padding depths whenever the exact additive trim balance holds.

The underlying paper covariance is Agent7's result in
[#315](https://github.com/taco-jpg/p196-algorithm/pull/315).
The global prescribed-schedule argument belongs to Agent107
([#336](https://github.com/taco-jpg/p196-algorithm/pull/336)); balanced profiles
belong to Agent110 ([#338](https://github.com/taco-jpg/p196-algorithm/pull/338)).
This contribution supplies registered Lean proofs at the existing A120
definitions. It does 不 claim their paper mathematics as a new discovery.

Coordination [claim](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6432941782).
Baseline `eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`.
This PR is independent of Agent119's length-accounting PR339.

## Exact theorem scope

For `h=b-1`, define

\[
P_a(C)=h^a\mathbin{++}C\mathbin{++}h^a.
\]

Under the unchanged `Hyp b B C`, for any natural `a`:

- `Hyp b B (P_a C)` holds;
- `e2`, `DR`, `yd`, 和 `gam` are unchanged;
- `nextB b B (P_a C) = nextB b B C`;
- `nextC b B (P_a C) = P_a (nextC b B C)`.

The incoming carry `e1` 和 `DB` depend only on `B`, which is unchanged.
The statements permit every admitted base `b>=2`, arbitrary widths, empty
exteriors, zero padding, nonsymmetric centers, 和 nonmaximal trims.

For an original checked edge `E=(B,C,B2,C2,u,v)`, let

\[
E'=(B,P_a(C),B_2,P_{a'}(C_2),u,w).
\]

The central registered endpoint is:

```lean
theorem edgeOK_transport {b : Nat} {E : Edge}
    (he : edgeOK b E = true)
    (a a' w : Nat) (balance : a + E.v = w + a') :
    edgeOK b (transportEdge b a a' w E) = true
```

The sign is fixed by the exact output equation:

\[
F(P_a C)=P_a(F(C))=P_{a+v}(C_2)
 =P_{w+a'}(C_2)=P_w(P_{a'}C_2).
\]

`transportEdge_gam` proves that the transported edge retains its original
overflow bit. Exterior blocks 和 exterior trim `u` are unchanged by definition.

**Boundary:** these modules prove local checked-edge transport. They do 不
construct cyclic padding offsets, prove transported chain closure, or prove
the full arbitrary equal-total schedule-existence theorem. Maximal-strip
normalization is also outside the formalized scope. 没有 decimal certificate,
center nonexistence result, or universal decimal obstruction is supplied.

## Lean proof structure

`Padding.lean` uses the existing `norm_append` 和
`norm_replicate_neutral` lemmas. Its exact normalized center is
`x^a ++ DC ++ y^a`, with the original outgoing carry, where `x=xd`, `y=yd`.
The carry bounds follow from `Hyp`, 和 `Hyp.xy` gives `x+y=b-1`.

`WordAlgebra.lean` proves, for arbitrary natural lists 和 symbols:

\[
\operatorname{pairs}(x^a D y^a)
 =(x+y)^a\operatorname{pairs}(D)(x+y)^a.
\]

It also moves the extra overflow symbol `y` across the identical right run.
These identities cover the overflow 和 nonoverflow branches without assuming
symmetry of `D`.

`Main.lean` composes those facts into `nextC_padC`, proves the converse direction
of the existing `edgeOK_sound` specification, 和 validates `transportEdge`
through the complete unchanged Boolean checker.

The 3 modules 和 their 18 theorem endpoints are registered under
`Agent119NeutralCenterPadding`. No earlier proof source or checker is edited.

## Validation

```bash
LEAN_NUM_THREADS=1 python3 tools/verify.py --changed
python3 calculation/agent-119/center_padding_controls.py
```

The repository gate checks 5,220 Lean files / 302 projects, builds 和 replays
the 3 changed modules with `lean4checker`, 和 audits 18 registered endpoints.
The required terminal result is `ALL CHECKS PASSED`; publication requires this
actual result on the submitted code. Endpoint dependencies use only `propext`
和 `Quot.sound`.

Stock Lean 4.19.0 direct per-file measurements, one thread, 8 GiB address-space
ceiling 和 1,200-second timeout:

| Module | Wall seconds | Peak RSS, KiB |
|---|---:|---:|
| Padding | 0.929 | 444832 |
| WordAlgebra | 0.669 | 411784 |
| Main | 0.886 | 432872 |

Python `resource.getrusage` measured child RSS because `/usr/bin/time` was
unavailable. No compiler/runtime modification or trust bypass was used.

**COMPUTED positive calibration:** the existing eight Lean-source certificate
bases supply 56 edges. Every locally balanced transport with source padding
0..4 和 nonnegative resulting trim passes `edgeOK`; uniform padding also
preserves the original complete positive cycles. Exact output:

```text
PADDING CALIBRATION PASS bases=8 original_edges=56 local_transports=880 uniform_cycles=40
```

These are existing positive controls, 不 new certificates. An independent
source review checked source-Hyp preservation, empty exteriors, nonsymmetric
centers, the trim-balance sign, 和 the stated local/global scope boundary.
