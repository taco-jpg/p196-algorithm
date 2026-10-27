# Agent 107 — T3.trim-schedule-equivalence

**Classification: PAPER PROOF + COMPUTED.** For fixed periodic carry/overflow
streams, center-cycle existence over unrestricted widths is independent of the
nonnegative trim schedule, provided its total is unchanged. One prescribed
binary schedule therefore suffices for an all-length decision.

Coordination: [claim](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6432786581),
[progress 和 scope split](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6432836759).
Baseline: `eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`.

**Attribution.** Agent 7 established neutral-padding covariance 和 canonical
normalization in [#301](https://github.com/taco-jpg/p196-algorithm/issues/301),
[#315](https://github.com/taco-jpg/p196-algorithm/pull/315), 和
[#326](https://github.com/taco-jpg/p196-algorithm/pull/326). 这 report derives the
prescribed-schedule transport, its minimal nonnegative offsets, its quantitative
width allowance, 和 its consequence for exhaustive center searches. Agent 110
owns the separate balanced-width corollary 和 one-schedule solver runner;
Agents 111/113/118 own compiled long-period center decisions.

## 1. Definitions

Fix a base \(b\ge2\), a period \(P\ge1\), 和 cyclic binary streams
\(e_t,g_t\), indexed modulo \(P\). Put \(h=b-1\) 和
\(P_a(C)=h^a\mathbin{++}C\mathbin{++}h^a\).

A valid center word 有 coefficients in \([0,2h]\) 和 normalization
\(\operatorname{norm}_b(C,e_t)=(D,1-e_t)\). The raw update is

\[
F_t(C)=\begin{cases}
\operatorname{pair}(D),&g_t=0,\\
\operatorname{pair}(D\mathbin{++}[he_t]),&g_t=1,
\end{cases}
\]

where \(\operatorname{pair}(W)=W+\operatorname{reverse}(W)\) coordinatewise.
A center cycle with trims \(v_t\in\mathbb N\) satisfies

\[
F_t(C_t)=P_{v_t}(C_{t+1}). \tag{1}
\]

The carry flip excludes empty or entirely neutral centers. A closed cycle 有
symmetric centers 因为 the raw update 和 symmetric stripping preserve
symmetry. Lengths in (1) give

\[
2\sum_t v_t=\sum_t g_t=:G,
\qquad K:=\sum_t v_t=G/2. \tag{2}
\]

## 2. Padding covariance, with the carry conditions explicit

Let \(x=h(1-e_t)\), \(y=he_t\). Neutral digits transmit either carry, so

\[
\operatorname{norm}_b(P_a(C),e_t)
=(x^a\mathbin{++}D\mathbin{++}y^a,1-e_t).
\]

For \(g_t=0\), pairing these digits places \(x+y=h\) at the 两个 ends.
For \(g_t=1\), append \(y\) first 和 regroup as
\(x^a\mathbin{++}(D\mathbin{++}[y])\mathbin{++}y^a\).
The same pairing argument gives

\[
F_t(P_a(C))=P_a(F_t(C)). \tag{3}
\]

This is Agent 7's padding identity specialized to the forced center map.
Padding preserves bounds, symmetry, nonemptiness, 和 the exit carry.
For a full B/C certificate, B stays fixed; therefore e1, e2, DR, g, 和 raw nextB
也 stay fixed.

## 3. Prescribed schedule theorem

**Theorem.** Let a center cycle satisfy (1). For any nonnegative integers
\(w_0,\ldots,w_{P-1}\) with \(\sum w_t=K\), there is a center cycle with the
same driver streams 和 trims exactly \(w_t\).

**Proof.** Define

\[
d_0=0,\qquad d_t=\sum_{j<t}(v_j-w_j),\qquad
a_t=d_t-\min_{0\le j<P}d_j.
\]

Equal totals give \(d_P=d_0\). Thus the offsets are cyclic nonnegative integers
和 satisfy

\[
a_t+v_t=a_{t+1}+w_t.
\]

Set \(C'_t=P_{a_t}(C_t)\). Applying (3) 和 then (1),

\[
F_t(C'_t)=P_{a_t+v_t}(C_{t+1})
=P_{w_t}(C'_{t+1}).
\]

Every validity condition survives padding, so these are the required edges.
Exchanging the source 和 target schedules proves equivalence of existence.
For a full certificate, keep B, B2, 和 u on each edge, replace C/C2 by the padded
words 和 v by w. The e/g streams, linked closure, 和 total gain remain unchanged;
the complete `cycleOK` equations therefore hold. ∎

## 4. Minimal offsets 和 width allowance

Every solution of the cyclic difference equation differs by a common constant.
The displayed solution satisfies \(\min a_t=0\), so it is componentwise minimal among
nonnegative solutions.

Follow the directed cyclic interval from an index minimizing d to one maximizing
d. The increase is a sum of \(v_t-w_t\), bounded above by the total source mass
K. Consequently

\[
0\le a_t\le K,\qquad |C'_t|\le |C_t|+2K=|C_t|+G. \tag{4}
\]

Thus equal finite-width caps do **不** transfer between schedules. A cycle
bounded by M for one schedule maps to a cycle bounded by M+G for a prescribed
schedule. This additive allowance is explicit; it is **不** an unrestricted
conclusion from a finite-width computation.

The additive allowance can be attained. Starting from the doubled existing
base26 certificate, first concentrate its K=2 trims at the last phase, then
transport to a target concentrated at phase0. Minimal offsets are
\((K,0,\ldots,0)\), so phase0 gains exactly 2K coefficients. The independent
regression test constructs 和 verifies these full certificates.

## 5. Search consequence 和 limits

Since g is binary, \(K\le P/2\). Choose any binary vector w with K ones.
The theorem proves that its all-length center decision covers arbitrary
nonnegative trim schedules, including original schedules with entries above1.

| Driver case | P | G | Binary schedules previously enumerated | Sufficient completed schedules |
| --- | ---: | ---: | ---: | ---: |
| p11, k1 | 11 | 4 | 55 | 1 |
| p11, k2 | 22 | 8 | 7,315 | 1 |
| p12, k2 | 24 | 6 | 2,024 | 1 |
| p11, k3 | 33 | 12 | 1,107,568 | 1 |
| p12, k4 | 48 | 12 | 12,271,512 | 1 |

These are schedule counts, **不** measured runtime speedups. A selected schedule
can still return `CAPPED`, `NOPERIOD`, or time out. Such a result remains
`UNDECIDED`; the theorem does 不 establish exhaustion for an incomplete run.
The period/segment/packing limits of the concrete solver remain binding.

For example, \(C=[4,4,10,4,4]\), \(e=1\), \(g=0\) gives raw
\([9,9,0,9,9]\), permitting v=2. Binary schedule completeness follows from
transport, **不** from an incorrect assumption that an edge can trim at most1.

## 6. Reproduction 和 validation

```bash
python3 calculation/agent-107/trim_schedule.py selftest
python3 -O calculation/agent-107/trim_schedule.py selftest
python3 -O calculation/agent-107/test_trim_schedule.py
python3 calculation/agent-107/trim_schedule.py schedule 111000100001110001000011100010000
python3 calculation/agent-107/trim_schedule.py retime cycle.json --target 1,0,0,0
python3 tools/verify.py --changed
```

The `retime` command accepts JSON `{"base":b,"edges":[[B,C,B2,C2,u,v],...]}`
和 emits the complete transformed edge list, offsets, streams, 和 target trims.
Invalid source cycles, negative trims, or mismatched totals are rejected with
explicit conditionals; acceptance does 不 depend on Python assertions.

| Test | Completed count |
| --- | ---: |
| Existing fixture bases | 8: 2,4,8,11,16,17,26,32 |
| Binary schedules on original 和 doubled fixtures | 896 |
| Nonbinary targets on doubled 和 tripled fixtures | 280 |
| Transformed complete certificates accepted by the existing mirror | 1,176 |
| Replayed transformed edges | 21,440 |
| Neutral-padding covariance checks | 19,694 |
| Arbitrary schedule-offset checks | 5,000 |
| Independent ordinary-integer reverse-add cycle replays | 112 cycles / 1,792 edges |
| Independent exhaustive local covariance checks, including nonsymmetric words | 12,240 |

Normal 和 optimized Python print identical passing counts. Direct positional
integer arithmetic checks the normalization used in the finite covariance
tests. The new implementation is independent of the repository mirror; the
mirror is imported only for a second replay of the transformed complete
certificates. Existing positive fixtures are prior results, **不** new
certificates attributed to Agent 107.

The separate `test_trim_schedule.py` passes 4 tests under optimized Python,
using ordinary integer template values 和 canonical integer reversal, independent
of the coefficient mirror. It verifies every edge of the 112 transformed
cycles, their nonpalindromic phases, the sharp width example, 和 malformed-input
rejections. These finite controls check implementation; the universal theorem
comes from sections2–4.

## 7. Scope 和 verification

The general theorem is **PAPER PROOF**; its implementation/controls are
**COMPUTED**. `python3 tools/verify.py --changed` passes for these code/report
changes, with zero changed Lean modules; this does **不** make the theorem
`LEAN-VERIFIED`. No Lean or registry file is changed.

This result changes the search reduction. It does **不** exclude p11 k3, p12 k4,
arbitrary k, or arbitrary base-10 one-band cycles. A decimal Lychrel witness
remains absent; those center decisions remain separate tasks.
