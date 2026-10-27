# Agent 106 — T2.charge-completed-prefix

**PAPER PROOF + COMPUTED. No new Lean theorem.**
Coordination: issue #289, claim #6433213217, progress #6433296031.
This three-file result is stacked on PR #384, commit
`b37cb6a607fd880b01554e6ca5f2f3049db4d0fe`.

## Result 和 attribution

For an exact free-prefix exterior transition at a fixed positive width,
the strong alternating residue at both endpoints forces the precise
finite neutral terminal boundary. Thus a closed prefix itinerary with
the strong residue at every phase is an actual autonomous B return.
A matching C cycle is still required for a certificate.

This is a converse to a necessary condition, conditional on exact prefix
dynamics. It does 不 assert that a charge-qualified word alone constructs
a cycle. The terminal criterion is equivalent to the existing exact B
automaton's accepting condition, 不 an additional pruning theorem for
arbitrary intermediate prefixes.

Credits: Agent107 [PR #363](https://github.com/taco-jpg/p196-algorithm/pull/363)
supplies the all-base strong residue necessity; Agent108
[PR #360](https://github.com/taco-jpg/p196-algorithm/pull/360) supplies its
decimal A120 Lean bridge. Both credit the earlier alternating-charge
normalization algebra. Agent7's neutral-padding mathematics 和 subsequent
Agent114 exterior formalization supply common-width transport. The new
contribution here is the free-prefix endpoint converse 和 its application
to the specific infinite spatial lasso in
[PR #384](https://github.com/taco-jpg/p196-algorithm/pull/384).

## Definitions

Fix base `b>=2`, modulus `m=b+1`, a coefficient word `B` of length
`n>=1`, coefficients in `0..2b-2`, 和 a freely chosen bit `h`.
For actual exterior sources assume `B[0]>0`. Put

\[
A(W)=\sum_j(-1)^jW_j,\qquad s=(-1)^n,\qquad R(W)=A(W)-(-1)^{|W|}\pmod m.
\]

Normalize `B` from carry zero to obtain `(D,e)`. Normalize `reverse B`
from carry `h` to obtain `(Rrev,g)`, 和 put `H=reverse Rrev`. The carries
`e,g` are bits. Write `d=H[n-1]=(B[n-1]+h) mod b`.

The exact width-`n` free-prefix successor `B'` is

\[
B'_j=\begin{cases}
D_j+H_j,&g=0,\\
D_0+1,&g=1,\ j=0,\\
D_j+H_{j-1},&g=1,\ j>0.
\end{cases}
\]

Define `F(B)` to be the actual autonomous A120 raw exterior update,
using its required complementary reverse-entry carry `1-e`. There is
no center assumption in the free-prefix construction; `h` starts free.

## PAPER PROOF: exact endpoint converse

The standard normalization identity evaluated at `-1 mod(b+1)` gives

\[
A(D)\equiv A(B)-se,\qquad A(H)\equiv A(B)-sh+g\pmod m.
\]

Consequently, for the exact prefix successor,

\[
A(B')\equiv
\begin{cases}
2A(B)-s(e+h),&g=0,\\
s(h-e-d),&g=1
\end{cases}\pmod m. \tag{1}
\]

For the overflow identity, the high-side prefix contribution is
`1 - A(H) - s*d`; adding `A(D)` gives (1).

Suppose `R(B)=R(B')=0`. If `g=0`, equation (1) implies
`e+h-1=0 mod m`. This integer lies in `[-1,1]`, while `m>=3`, so
`h=1-e` exactly. The free-prefix edge is already the full raw B edge.

If `g=1`, the target residue alone implies
`h-e-d=1 mod m`. Its range is `[-b,1]`, leaving precisely:

| Integer value | h | e | d |
|---:|---:|---:|---:|
| 1 | 1 | 0 | 0 |
| -b | 0 | 1 | b-1 |

Thus `h=1-e` 和 `d=(b-1)e`. In either case the coefficient bound
`0<=B[n-1]<=2b-2` forces `B[n-1]=b-1`. The omitted raw coefficient is

\[
(b-1)(1-e)+d=b-1.
\]

Therefore

\[
\boxed{F(B)=B'\mathbin{+\!+}(b-1)^g.} \tag{2}
\]

Conversely, the terminal conditions inserted in (1) preserve zero residue
from a zero-residue source. On that source domain the exact equivalence is

\[
R(B')=0\quad\Longleftrightarrow\quad
h=1-e\ \land\bigl(g=0\ \lor\ d=(b-1)e\bigr). \tag{3}
\]

For overflow, (3) does 不 need the source-residue premise. No division by
two occurs; every base `b>=2`, including odd bases 和 base 2, is covered.

## PAPER PROOF: cyclic characterization

For a nonempty listed temporal period, the following are equivalent:

1. A finite autonomous B return with arbitrary widths 和 natural neutral
   suffix trims.
2. Some positive common width `N`, positive-headed bounded coefficient
   words `W_t`, free bits `h_t`, exact cyclic prefix transitions, 和
   `alt(W_t)=(-1)^N mod(b+1)` at every phase.

`2=>1` follows edge by edge from (2), with exterior trims `u_t=g_t`.
For `1=>2`, choose `N>=1,max |B_t|` 和 append neutral coefficients:
`W_t=B_t ++ (b-1)^(N-|B_t|)`. Credited suffix covariance 和 the raw length
identity imply `F(W_t)=W_(t+1) ++ (b-1)^g_t`. The credited all-base cycle
charge theorem supplies the residue, which neutral padding preserves.

A closed positive-head itinerary cannot have only `g=0`: its first
coefficient would at least double every step. Empty original B emits
overflow immediately; the existing charge law then excludes empty 和
all-neutral phases on any actual closed return. Thus there is no hidden
zero-overflow or empty-word exception. The empty temporal itinerary is
excluded explicitly.

At a proposed finite cut, (3) restores precisely the old terminal test
`L+H=1` 和 `Y=(b-1)L` at overflow phases. A proper prefix of a larger
valid B need 不 have zero charge. **Do 不 discard intermediate spatial
prefixes merely because their own charge is nonzero.**

## COMPUTED application: every common-width lasso cut fails

The #384 lasso has 39 initial columns 和 a 20-column spatial loop.
Across cuts 39 to 59 its eight alternating sums change by exactly

```text
(11,44,11,44,11,44,11,44).
```

The complete carry state, spatial parity, 和 charge vector therefore
repeat every 20 columns modulo 11. It suffices to classify widths 1..38
和 one representative of each later class, widths 39..58.

Bit `t` of the following failure masks means phase `t` has nonzero
strong residue. Every displayed mask is nonzero:

```text
cuts 1..38:
255,253,255,255,255,51,255,255,255,243,255,255,255,247,255,119,
255,63,243,255,207,255,255,63,92,241,255,255,247,67,255,63,124,
255,255,255,63,255

cuts 39..58, repeating with period20:
125,255,223,252,255,245,255,127,243,255,
215,255,253,207,255,95,255,247,63,255
```

The eventual residue-vector period is exactly 20: none of its proper
divisors 1,2,4,5,10 is a period. This minimality is supplementary;
periodicity alone proves finite coverage of all widths.

| Phases satisfying the residue | Cuts 1..38 | Periodic cut classes |
|---:|---:|---:|
| 0 | 22 | 8 |
| 1 | 3 | 4 |
| 2 | 8 | 8 |
| 3 | 2 | 0 |
| 4 | 2 | 0 |
| 5 | 1 | 0 |
| 6,7,8 | 0 | 0 |

Hence **no common-width truncation of this particular lasso is a finite
B return**. This does 不 classify independently chosen phase widths,
other spatial paths, or all possible B words. Padding a hypothetical
variable-width construction could leave this particular lasso family.
The existing broader period-eight exclusion is prior work, 不 a new claim.

## Odd-base distinction 和 negative controls

The weaker doubled charge `Q=2alt(B)+(b-1)(-1)^n` cannot replace the
strong residue. In base 3, `B=[4,1]`, `h=0` gives the exact free-prefix
successor `B'=[2,3]`. Both weak Q residues vanish modulo 4, but `e=0`,
so the complementary entry must be 1. Indeed `F(B)=[2,3,4]`, which is
unequal to `B'++[2]`. Both strong residues are 2, correctly failing (3).

Additional base-two width-one controls show why source charge alone is
insufficient (`B=[2],h=1`) 和 why target charge alone is insufficient
without overflow (`B=[1],h=0`).

## Reproduction 和 independent validation

From the repository root of this stack:

```bash
python3 calculation/agent-106/charge_prefix.py
python3 -O calculation/agent-106/charge_prefix.py
python3 calculation/agent-106/charge_prefix.py --lasso-only --lasso-json
python3 calculation/agent-106/charge_prefix_audit.py
python3 -O calculation/agent-106/charge_prefix_audit.py
python3 tools/verify.py --changed
```

Normal 和 optimized Python complete with `CHARGE_PREFIX_CHECK PASSED`
和 `CHARGE_PREFIX_INDEPENDENT_AUDIT PASSED` respectively.

| Check | Exact completed scope |
|---|---|
| Core exhaustive algebra | 136,525 bounded words, widths1..3, bases2..16, both high bits:273,050 edges; includes zero heads for the algebraic identity |
| Core accepted-boundary checks | 20,044 charged-source edges;12,921 charged-target edges;71,125 terminal-closed edges;136,525 overflow edges |
| Existing positive fixtures | 8 original nondecimal certificates,56 padded B edges, all exact cycle equations; original mirror cycleOK controls pass |
| Independent integer exhaustive | 119,444 positive-head edges: bases2..7,widths1..4, plus decimal widths1..3;54,081 nonoverflow/65,363 overflow |
| Independent seeded integer | 10,000 edges,5,000 words,widths1..128,bases2,3,4,5,7,8,10,11,16,20,26,32;seed106202;4,442 nonoverflow/5,558 overflow |
| Independent lasso interpretation | 20,792 phase residues at every cut1..2599;76 coefficient/carry cutoff API checks; exact58-class table agreement |
| Necessary-premise controls | Three counterexamples above, including the odd-base weak-charge failure |

The independent reference constructs ordinary integers with coefficient
word `B ++ [(2b-2)h] ++ reverse(B)`, converts them to base-b digits, 和
adds paired digits. This uses no carry-loop routine to obtain its expected
prefix. The unchanged main A120 mirror separately checks the restored
raw transition using an actual Hyp-satisfying one-coefficient center.
Explicit exceptions remain active under Python optimization.

The all-base theorem follows from the displayed algebra; the all-width
lasso classification follows from its exact finite loop 和 residue sums.
Neither conclusion extrapolates from finite random samples.

The literal repository gate passes:5,217 Lean files/301 projects,
zero changed Lean modules 和 zero new endpoints. This is 不 Lean
verification of the new theorem. Core arithmetic needs no unmerged
charge implementation; only the lasso application uses parent #384 data.
No C cycle, cycleOK10 input, or decimal Lychrel proof is supplied.
