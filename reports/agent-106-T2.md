# Agent 106 — neutral exterior cycles 和 saturated prefix constraints

Task: **T2.alternating-neutral-strip**, forward-prefix scope after the split
with Agent 109 in [coordination #289](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6432846116).
Baseline: `eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`.

## Result 和 attribution

**PAPER PROOF.** Every nonempty closed base-10 neutral exterior cycle, with
arbitrary finite exterior widths 和 arbitrary legal neutral-suffix trims,
projects to the existing exact three-column prefix model. Consequently,
writing \(P\) for its period 和 \(G=\sum_t g_t\) for its overflow total,

\[
2G\le P,\qquad 2G=P\Longrightarrow 8\mid P.
\]

In the equality case its padded first three coefficients follow exactly the
existing eight-phase skeleton below, up to a cyclic phase shift. The result
includes empty or short exterior representatives.

The prefix inequalities, clock theorem 和 eight-state skeleton are **prior
results**, in `P196.Agent4.Saturation` 和 `Agent2.SaturatedProfile`. The new
contribution here is the explicit neutral-A120 exterior padding/projection
bridge. Agent 7's general neutral-padding work, [PR #315](https://github.com/taco-jpg/p196-algorithm/pull/315),
is credited. The main branch's `CertificatePrefix` bridge concerns the
different Agent109 nonneutral-phase checker; its phase excludes 9.

**COMPUTED.** Independent local arithmetic audits verify the bridge on
6,859 exterior words of widths 0–3, 5,000 longer deterministic samples 和
35,577 padded instances. A separate 36-edge first-coordinate certificate
checks the density bound; a second-column audit eliminates its spurious
\(9\leftrightarrow18\) equality component.
An independent ordinary-integer implementation checks another 20,000
instances. Exact prefix graphs through width 8 retain 8-step returns.

**Scope.** These are necessary conditions. Alternating overflow at \(P=16\)
remains undecided here. 没有 new center cycle, decimal certificate or universal
one-band impossibility follows. The new bridge is **不 LEAN-VERIFIED**;
existing Lean theorems are used as mathematical source statements.

## 1. Autonomous exterior 和 common padding

For a finite coefficient word \(B\), let

\[
e(B)=\operatorname{carry}(\operatorname{norm}_{10}(B,0)).
\]

Define \(F(B)\) by the exact A120 `nextB` formulas, supplying reverse-entry
carry \(1-e(B)\). This is the actual exterior successor on every `Hyp`-valid
B/C state, 因为 `Hyp` forces the complementary center output carry.
Write \(g(B)\) for the reverse-normalization terminal carry.

Since normalizing a coefficient 9 preserves an incoming carry bit,
right padding obeys, for every \(a\ge0\),

\[
e(B9^a)=e(B),\quad g(B9^a)=g(B),\quad F(B9^a)=F(B)9^a. \tag{1}
\]

For the last identity, the added low digits equal \(9(1-e)\), while the
added reversed high digits equal \(9e\). Their sum is 9. At an overflow the
single shifted boundary contribution reproduces the original final entry
of \(F(B)\); the remaining added entries are 9. Also,
\(|F(B)|=|B|+g(B)\).

Suppose a cyclic exterior list satisfies

\[
F(B_t)=B_{t+1}9^{u_t},\qquad B_P=B_0.
\]

Choose \(N\ge\max(3,|B_0|,\ldots,|B_{P-1}|)\) 和 put
\(\widetilde B_t=B_t9^{N-|B_t|}\). The length equation gives
\(u_t=|B_t|+g_t-|B_{t+1}|\). Substituting in (1) yields

\[
F(\widetilde B_t)=\widetilde B_{t+1}9^{g_t}. \tag{2}
\]

Thus the first three positions evolve exactly 和 close after \(P\) steps,
regardless of the original trim schedule. An empty original B becomes a
positive padded word with first coefficient 9, so the prefix positivity
hypothesis remains valid.

## 2. Exact bridge to the prior prefix theorem

Let \(s_t\) be the first three coefficients of \(\widetilde B_t\), 和 let
\(h_t\in\{0,1\}\) be the carry obtained by normalizing the reversed suffix
\(\widetilde B_t[3:]\), starting from \(1-e(B_t)\).

The low normalization starts at carry 0. High normalization crosses the
three prefix coefficients in reverse order, starting at \(h_t\). Therefore
the definition in [PrefixModel.lean](../lean/P196/Agent2SaturatedProfile/PrefixModel.lean)
gives exactly

\[
\operatorname{advance}(s_t,h_t)=(s_{t+1},g_t). \tag{3}
\]

All coefficients lie in \([0,18]\), the first is positive, the inward carry
is a bit, 和 \(s_P=s_0\). Thus every hypothesis of the prior
`closed_prefix_overflow_bounds` holds. If \(2G=P\), every hypothesis of
`saturated_closed_prefix_period` 和 `saturated_overflow_profile` holds too.
These exact source endpoints are in
[SaturationTheorem.lean](../lean/P196/Agent2SaturatedProfile/SaturationTheorem.lean)
和 [Agent2SaturatedProfile.lean](../lean/P196/Agent2SaturatedProfile/Agent2SaturatedProfile.lean).

The existing saturated skeleton is:

| Phase | First three coefficients | \(g\) | Inward carry at cut 3 |
|---:|---|---:|---|
| 0 | (8,12,9) | 0 | 1 |
| 1 | (17,5,0) | 1 | arbitrary bit |
| 2 | (8,13,5) | 0 | 0 |
| 3 | (17,6,11) | 1 | arbitrary bit |
| 4 | (8,14,8) | 0 | 0 |
| 5 | (17,8,17) | 1 | arbitrary bit |
| 6 | (8,16,16) | 0 | 1 |
| 7 | (17,13,14) | 1 | arbitrary bit |

The table is read directly from the existing `cycleState` definition by
`prefix_bridge.py`; the table is 不 a newly discovered cycle or a B witness.

## 3. Compact independent density audit

The first coefficient \(x\in\{1,\ldots,18\}\), with inward carry
\(h\in\{0,1\}\), satisfies

\[
g=\lfloor(x+h)/10\rfloor,\qquad
x'=\begin{cases}2x+h,&g=0,\\x\bmod10+1,&g=1.\end{cases}
\]

The potential on \(x=1,\ldots,18\),
\[
R=(3,2,2,1,1,1,1,1,1,2,0,0,0,0,0,0,0,0),
\]
satisfies \(R(x')-R(x)\ge2g-1\) on every edge. Summation proves \(2G\le P\).
Its tight subgraph 有 only the cyclic components \(\{8,17\}\) 和
\(\{9,18\}\), each alternating overflow/nonoverflow.

The second component cannot lift to a second spatial column. At a
nonoverflow phase let its second coefficient be \(q\). The head 9 forces
the inward head carry to be 0, hence \(q+a\le9\) 和 \(r=2q+a\) for an
inward bit \(a\). At the following overflow phase the head is 18, so

\[
q'=(r+1)\bmod10+(18+b)\bmod10,
\qquad \lfloor(r+c)/10\rfloor=b,
\]
for bits \(b,c\), 和 the next nonoverflow phase again requires \(q'\le9\).
The exact permitted relation is only
\(0\to9,4\to8,4\to9\); its source 和 target sets are disjoint. Hence it
没有 closed temporal walk. Padding to \(N\ge3\) covers short originals.

## 4. Longer forward prefixes: exact computation 和 its limit

Fix the prior eight-phase first-three-coefficient skeleton. Append arbitrary
coefficients in \([0,18]\), permit either inward high carry, 和 retain every
edge that advances the skeleton correctly. Every finite neutral B cycle
projects into 这 graph after sufficient common padding.

A cyclic prefix of width \(k+1\) projects to a cyclic prefix of width \(k\).
Therefore extending only the cyclic vertices retained at the preceding
width preserves every possible cycle. The resulting exhaustive hierarchy
有 the following counts; candidate counts concern the filtered domain.

| Width | Candidates | Edges | Cyclic vertices | Cyclic SCC sizes | SCC period gcds |
|---:|---:|---:|---:|---|---|
| 4 | 152 | 156 | 65 | 65 | 8 |
| 5 | 1,235 | 1,521 | 388 | 388 | 8 |
| 6 | 7,372 | 9,395 | 2,191 | 2,191 | 8 |
| 7 | 41,629 | 54,294 | 7,556 | 8; 656; 6,892 | 8; 8; 8 |
| 8 | 143,564 | 187,833 | 36,479 | 140; 426; 35,913 | 16; 16; 8 |

Full cyclic vertex sets agree with unrestricted suffix enumeration at
widths 4–7. A second implementation uses direct integer digit pairing,
Tarjan SCCs 和 explicit closed-walk lengths to independently check every
edge, SCC 和 period gcd at widths 4–5.

At width 8 an actual prefix return 有 the following states:

```text
(8,12,9,10,6,2,2,9)   (17,5,0,1,13,4,4,18)
(8,13,5,1,5,8,8,13)  (17,6,11,2,10,16,17,6)
(8,14,8,4,3,8,15,14) (17,8,17,8,6,17,11,10)
(8,16,16,16,14,14,10,3) (17,13,14,14,10,10,1,8)
inward high carries: 0,0,0,0,1,0,1,0
```

These eight edges replay exactly. Hence 这 width-8 projection cannot
imply \(16\mid P\) or exclude alternating overflow altogether. Free inward
carries 还 require completion by a real finite B suffix; 这 is 不 a
B witness. Width 9 needs 693,101 candidates, exceeding the chosen 500,000
cap; its status in 这 result is **UNDECIDED**.

## 5. Independent backward-method audit shared with Agent 109

This is a limitation of one proof strategy, 不 a full exterior obstruction.
For the exact `Agent9.AlternatingScalarBoundary.Tile`, neutral cuts are
\(S(a,b)=(a,b,1-a,10b-1)\). The equations for an inner neutral cut force

\[
r=9,\quad e=1-b,\quad X.a=a,\quad X.b=b,
\quad q=4+5(a+X.c),\quad X.z=q_+-10(1-b).
\]

Thus nonneutral predecessors with \(q=4\) or \(14\) remain possible. Put
\(S=(0,1,1,9)\). The following spatial loop consists entirely of traces
constant in paired time:

\[
S\to(1,0,0,0)\to(0,1,1,6)\to(1,0,1,5)\to(1,0,1,8)
\to(1,0,0,3)\to(0,1,0,1)\to(0,1,0,4)\to S.
\]

For its eight edges, respectively,
\[
q=q_+=(10,7,12,13,11,5,7,4),\quad
r=(0,16,5,8,3,11,14,9),\quad e=(0,1,0,0,0,1,1,0).
\]

Every exact Tile field holds. Repeating the loop gives arbitrarily many
predecessor cuts before the same permanently nonneutral immediate
predecessor of S. Temporal shifts do 不 change constant traces. Therefore
没有 fixed finite predecessor depth proves unanchored neutral-tail erasure
in 这 relation. 这 differs from the scalar 6/12 erasure theorem in
[REPORT_218](REPORT_218.md). The loop does 不 connect to the physical
outside or establish a B cycle. Agent 109 retains the broader backward
transfer task after the coordination split.

## 6. Reproduction 和 verification

From the repository root:

```bash
python3 calculation/agent-106/head_density.py
python3 calculation/agent-106/head9_second_column.py
python3 calculation/agent-106/prefix_bridge.py
python3 calculation/agent-106/neutral_tail.py
python3 calculation/agent-106/prefix_integer_audit.py
python3 calculation/agent-106/prefix_extension.py --max-width 7 --witness
python3 calculation/agent-106/prefix_hierarchy.py --witness
python3 calculation/neutral_band_search.py selftest
python3 tools/verify.py --changed
```

Observed arithmetic output:

```text
HEAD_DENSITY_CHECK PASSED
vertices=18 labeled_edges=36 tight_edges=29
slack_histogram={0: 29, 1: 6, 2: 1}
tight_cyclic_components=[(8, 17), (9, 18)]
HEAD9_SECOND_COLUMN_CHECK PASSED
input_assignments=80 surviving_assignments=4
paired_relation=[(0, 9), (4, 8), (4, 9)]
composable_paired_edges=0
PREFIX_BRIDGE_CHECK PASSED
exhaustive_words=6859 random_words=5000 padded_checks=35577
neutral_fibers: tested=254144 accepted=80 PASS
bounded_tiles=1640 constant_time_tiles=88
constant_spatial_loop: edges=8 PASS
alphabet_only_predecessor_counts=[4, 16, 80, 88]; full_88_slot_fixed_point
DIRECT_INTEGER_PREFIX_AUDIT PASSED
samples=20000 overflow_counts=[9203, 10797] empty_B=306 B_width_lt_3=907
CAPPED width=9 candidate_vertices=693101 cap=500000 status=UNDECIDED
SELFTEST PASSED
```

The required repository verification returned exit 0 和 literal
`ALL CHECKS PASSED (changed files only, against origin/main)`.
It checked 5,217 Lean files / 301 registered projects, with zero changed
Lean modules 和 zero endpoint audits. Since 这 result changes no Lean
files or registry entries, 那 PASS does 不 constitute Lean verification
of the new bridge. No repository theorem or trust rule was changed.
