# Agent 109 — exact digit-MDD exterior width decision

## Status 和 scope

**PAPER PROOF + COMPUTED:** every decimal neutral-band certificate must
have some canonical exterior phase of width at least **9**.
The exact width-8 map is acyclic; its longest legal path has 36 edges.
No new Lean theorem or decimal certificate is asserted.
The calculation allows every temporal period, carry stream, overflow stream,
和 natural exterior trim schedule. It bounds the exterior block only.
The center block is absent from this necessary-condition calculation.

This is an independent compressed method for the uniform exterior-width
question. Agent9 retains primary ownership of the earlier explicit census.
Agent7's neutral suffix covariance, Agent107's trim transport, 和 Agent114's
formal local exterior-padding bridge are credited existing foundations.
Agent118's correlated center MDD motivated related compression; this report
uses a digit-wise preimage of the autonomous exterior map, rather than that
fixed-driver center image construction. No alternating-charge restriction
or restriction to a selected overflow itinerary is used.

## 1. Exact fixed-width reduction

Fix a base $b\ge2$, put $h=b-1$, 和 write coefficient words least significant
first. Every coefficient belongs to $\{0,\ldots,2h\}$.
For a legal exterior word $B$, let $e$ be the final carry of `norm b B 0`.
The complementary inward carry of the reversed exterior is $1-e$; its
outward carry is $g\in\{0,1\}$. These are exactly the autonomous exterior
quantities obtained from the unchanged A120 checker under its carry-flip
hypothesis. A nonempty legal source has positive lowest coefficient.

Let $F(B)$ denote the untrimmed next exterior. Appending $a$ neutral
coefficients leaves $e,g$ unchanged 和 gives

$$F(Bh^a)=F(B)h^a.$$

Suppose a closed exterior itinerary has every width at most $W\ge1$.
Pad each phase to $P_t=B_t h^{W-|B_t|}$. The exact length identity is
$|B_t|+g_t=|B_{t+1}|+u_t$. Therefore

$$F(P_t)=P_{t+1}h^{g_t}.$$

Thus all natural-trim cycles within width $W$ map to cycles of one partial
function $T_W$: normalize a positive-head length-$W$ word, compute $F$,
和 remove exactly $g$ terminal neutral coefficients. The map is undefined
if that suffix condition fails or its length-$W$ target has zero head.
Conversely every cycle of $T_W$ is an exterior cycle with $u_t=g_t$.
It still needs a compatible center cycle to produce a certificate.

Neutral suffix canonicalization identifies the domain with all canonical
exteriors of width at most $W$. The all-neutral length-$W$ word represents
the empty canonical exterior. There are exactly
$2h(2b-1)^{W-1}$ domain words for $W\ge1$.
For $W=0$, the only word is empty 和 $F([])=[b]\ne[h]$, so no edge exists.

## 2. Exact one-column transducer

At a cut before coefficient $x_i$, store $s=(g,L,H,Y)$.
$L$ is the carry arriving from the low end; $H$ is the carry leaving this
coefficient toward the outside. When $g=1$, $Y$ is the already computed
high-normalized digit one position farther outside; when $g=0$, set $Y=0$.
The outside state is $(0,0,0,0)$ or $(1,0,1,1)$ according to $g$.

Choose the next inward high carry $H'\in\{0,1\}$. A column exists exactly
when the following equations hold:

$$H=\lfloor(x+H')/b\rfloor,\quad
L'=\lfloor(x+L)/b\rfloor,\quad r=(x+H')\bmod b.$$

The next cut is $(g,L',H',r)$ for $g=1$, 和 $(g,L',H',0)$ for $g=0$.
The target coefficient is

$$y=(x+L)\bmod b+\begin{cases}r&g=0,\\Y&g=1.\end{cases}$$

Require $x_0>0$ 和, after exactly $W$ columns,

$$L+H=1,\qquad g=0\ \text{or}\ Y=hL.$$

The first terminal condition identifies $e=L_W$ 和 the complementary
inward high carry $H_W=1-e$. For $g=1$ the only omitted raw coefficient is
$h(1-e)+Y_W=h$, exactly the required neutral suffix. For $g=0$ there is no
omitted coefficient. Hence an accepted strip is equivalent to one edge of
$T_W$. Despite the guessed high carries, the accepted target of each
source is unique: ordinary carry normalization determines both carry
chains 和 $g$. Coefficients as large as $2b-2$ still give one-bit carries.

## 3. Correlated decision diagrams 和 sink peeling

An ordered, level-preserving MDD stores a finite set of length-$W$ words.
Node zero denotes the empty set; node one denotes the terminal singleton.
Every other node is an immutable pair consisting of its digit level 和
the ordered vector of $2b-1$ children. Equal pairs share one identifier.
Levels are retained even when every child is equal. Union recursively
unions corresponding children 和 interns the resulting pair.
Consequently root identity within the current arena means equality of
complete correlated word sets; no independent-coordinate product
approximation is taken.

For a target node $A$ 和 cut state $s$, `pre(A,s)` constructs exactly the
source suffixes whose output suffix follows $A$. At each source digit
$x$, enumerate the compatible $H'$, compute $y$, follow child $A[y]$,
和 recurse at the next cut. Union those choices under source child $x$.
At the terminal node use precisely the terminal carry conditions above.
Union the two outside starting states. Induction on the remaining digit
positions proves that this is the exact preimage $T_W^{-1}(A)$.

Start with all legal source words $S_0$ 和 iterate
$S_{n+1}=T_W^{-1}(S_n)$. These sets descend. A word belongs to $S_n$
exactly when its first $n$ steps remain defined within this domain.
If $S_n$ is empty, there is no cycle; the longest legal path has $n-1$
edges when $S_{n-1}$ is nonempty. If a nonempty root repeats immediately,
the surviving set is invariant 和 contains a cycle by finiteness.
It can also contain paths feeding cycles, so it is not merely the set of
cycle vertices. No conclusion is taken from a resource cap or a
nonempty frontier before equality. Python integers avoid count overflow;
node/cache/time/round limits return `UNDECIDED` with nonzero exit status.
Between rounds, collection retains exactly the current root's reachable
DAG, renumbers its nodes, 和 clears every identifier-keyed cache.
Fixed-point identity is tested before collection, never across arenas.

## 4. Computation 和 independent controls

From the repository root, with Python 3 和 no additional packages:

```bash
ulimit -v 2000000 && timeout 600 python3 calculation/agent-109/exterior_mdd.py --width 8 --seconds 540 --node-cap 1500000 --cache-cap 2500000
```

Completed primary run, exit 0:

```text
status=EMPTY base=10 width=8 iteration=37 words=0 seconds=136.221 peak_nodes=738552 peak_cache=1166537 maxrss_kib=530864
```

The largest retained diagram has 343,511 internal nodes at round 12.
The final-source rerun reproduces every count below 和 the same peak
node/cache totals: exit 0, 141.629 seconds, peak RSS 531,004 KiB.
Exact survivor counts $|S_0|,\ldots,|S_{37}|$:

```text
16089691302,8044845651,4194462916,2167657610,
1010339205,574674477,333193228,176470230,
101046189,57701839,34159026,20361171,
11818003,7187782,4471415,2826876,
1758103,1098948,718028,462014,
300401,193787,127980,83737,
53490,34871,22106,13801,
8275,5210,3200,1788,
943,470,131,48,14,0
```

An earlier run without collection reached its one-million historical-node
cap; that run was explicitly UNDECIDED. Its last completed set was $S_{11}$,
with 20,361,171 words. Collection enabled completion without changing
the represented sets. No unfinished run is counted as negative evidence.

### Independent controls within this task

The audit implementations were authored separately from the MDD engine.
They reuse the established normalization mirror or whole-integer arithmetic,
not the engine's column recurrence, to construct expected results.

```bash
python3 calculation/agent-109/exterior_mdd_audit.py --bases 10 --max-width 5 --positive-controls
python3 calculation/agent-109/exterior_mdd_audit.py --bases 2 4 11 --max-width 4
python3 calculation/agent-109/exterior_mdd_controls.py
python3 calculation/neutral_band_search.py selftest
```

All commands pass. The first two expand every accepted MDD path 和 compare
complete survivor sets at every round, then separately check counts:
185 set equalities over 21 distinct base/width cases. Decimal first-empty
rounds for widths 0,1,2,3,4,5 are 1,4,11,13,17,22 respectively.
The width-5 direct enumeration finishes in 9.391 seconds under a
1,500,000 KiB virtual-address cap. Base2 和 base4 width-2 fixed sets retain
their explicit known period-2 和 period-3 exterior cycles.

The arithmetic control's final output is
`ALL EXTERIOR MDD ARITHMETIC CONTROLS PASSED`, with:

| Control | Complete checked scope |
|---|---:|
| Local column inputs, all supported bases 2 through 62 | 1,317,112 |
| Valid local options | 658,556 |
| Empty-width cases | 61 |
| Singleton boundary fixtures | 366 |
| Deliberately correlated target sets | 63 |
| Source memberships in complete preimage comparisons | 108,682 |
| Complete-language collection checks | 126 |
| Known certificate exterior edges | 56 |

Correlated tests include diagonal, antidiagonal, congruence, parity, 和
sparse two-fibre languages. They compare complete preimages, then collect
the target/preimage DAGs 和 recompute first/second preimages. The collection
checks verify exact accepted sets, levels, topological IDs, unique table,
empty caches, 和 unchanged budget history. Boundary tests include maximal
coefficients, the $h+1$ carry threshold, zero-head rejection, 和 width zero.

All eight established nondecimal certificates supply positive controls,
including base11 at common canonical B width7, base26 at width8, 和 base17
at width29. Their known word sets remain contained in their own preimages;
these inclusion tests do not claim complete survivor classification there.
The unchanged Python mirror also passes its full eight-base selftest.

### Fail-closed limits 和 publication gate

Each following argument list, appended to
`python3 calculation/agent-109/exterior_mdd.py`, exits 2 without an EMPTY
or FIXED_POINT verdict. The same seven cases pass under `python3 -O`:

| Arguments | Terminal classification |
|---|---|
| `--base 1` | INVALID INPUT |
| `--width 129` | INVALID INPUT |
| `--seconds nan` | INVALID INPUT |
| `--rounds 0` | UNDECIDED |
| `--node-cap 1` | UNDECIDED |
| `--cache-cap 1` | UNDECIDED |
| `--width 8 --seconds 0.000000001` | UNDECIDED |

A separate width-8 subprocess with `RLIMIT_AS=64*1024*1024` also returns
UNDECIDED/exit 2: 15 input/interruption checks in total. The complete
arithmetic control command also passes under `python3 -O`.
Repository gate: `python3 tools/verify.py --changed`; its actual outcome
和 the exact published tree are recorded in the review PR.
External campaign review of the complete width-8 computation remains
requested. No rejected or capped experiment contributes to the exclusion.

## 5. Limits

Every exclusion is a finite exterior-width statement. It does not rule
out wider exteriors, prove center nonexistence, or settle decimal Lychrel
existence. A surviving exterior cycle would require separate exact
arithmetic extraction 和 a compatible center before any full-certificate
claim. The repository gate for a Python-only change is distinct from
kernel verification of a mathematical theorem.
