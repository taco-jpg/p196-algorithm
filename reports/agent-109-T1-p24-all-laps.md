# Agent 109 — bounded exteriors for every lap count of the priority center

## Result 和 exact scope

**PAPER PROOF + COMPUTED:** the prescribed decimal center driver below
has no compatible exterior cycle, for **any positive number of center
laps**, if every canonical exterior width is at most **16**.
An exact fixed-width calculation gives

$$|S_0|=273260286537746369382,\quad |S_1|=410578,\quad S_2=\varnothing.$$

Here $S_n$ is the complete set of padded exterior words that can follow
$n$ consecutive prescribed 24-step laps. Thus even a 48-step trajectory
within this width bound is impossible. There is no inference about wider
exteriors, different drivers, or unrestricted decimal Lychrel existence.
This is not a new Lean theorem.

Agent101 discovered the actual center cycle in [PR381](https://github.com/taco-jpg/p196-algorithm/pull/381).
The pinned data, with coefficients least significant first, are:

```text
e  = 010100110100101011001011
g  = 110001001000110001001000
v  = 100001000000100001000000
C0 = [9,14,13,18,13,14,9]
```

Agent117's primary one-lap/all-width completion 和 Agent108's independent
engine now report a negative even for every $e$ at this single-lap $g$.
Those results exclude one-lap closure without asserting anything about
other lap counts. The present bounded-width/all-laps calculation addresses that separate
question. Agent115's two-lap target, Agent106/116's all-width regular
languages, 和 Agent101's bounded SAT work retain their scopes/attribution.

## 1. Verified center 和 exterior padding

The independent center control reconstructs all 24 phases from the data
above. At each phase it checks the incoming $e_t$, complementary terminal
carry $1-e_t$, coefficient update, exact neutral trim $v_t$, 和 symmetry.
It separately checks positional-integer identities 和 the unchanged
`neutral_band_search.py` mirror with an exterior realizing that $e_t,g_t$.
The center returns exactly to $C_0$, has widths 6 or 7, 和 satisfies
$\sum g_t=8$, $\sum v_t=4$.

For completeness, if the normalized center digit word has value $D$,
fixed-width reversed value $R$, 和 width $m$, its raw successor value is

$$Z_{\rm raw}=\begin{cases}
D+R,&g=0,\\
D+bR+(b-1)e(b^m+1),&g=1.
\end{cases}$$

Writing $M=m+g$, the trim identity checked independently is

$$Z_{\rm raw}=(b^v-1)(1+b^{M-v})+b^v\operatorname{val}(C').$$

The common exterior-width reduction is the credited Agent7 padding
argument, used in [PR390](https://github.com/taco-jpg/p196-algorithm/pull/390)
和 now formalized separately by Agent114 in
[PR400](https://github.com/taco-jpg/p196-algorithm/pull/400).
Every bounded canonical exterior cycle can be represented with all
exterior words of length $W$, without changing $C,e,g,v$, 和 with exact
exterior trim $u_t=g_t$. This covers arbitrary original natural trims.
The all-neutral padded word represents the empty canonical exterior.

## 2. A finite map whose cycles cover all center repetitions

Let $U_W$ be all length-$W$ coefficient words in $\{0,\ldots,18\}$ with
positive lowest coefficient; for $W=0$ use the singleton empty word.
For each phase $t$, let $T_t$ be the partial exterior map with exactly
the prescribed $e_t,g_t$, target in $U_W$, 和 neutral suffix trim $g_t$.

The parent engine's exact one-column transducer is unchanged. Its cut
state is $(g,L,H,Y)$. The new phase preimage uses only the outside state
$(g_t,0,g_t,g_t)$ 和 requires the terminal conditions

$$L_W=e_t,\qquad H_W=1-e_t,\qquad
g_t=0\ \text{or}\ Y_W=9e_t.$$

These are precisely the low/high carries 和 the omitted neutral digit of
the padded phase map. The memoization key includes $(\text{target},s,e)$;
$g$ is already part of $s$. Thus results for different incoming carries
cannot be confused when the same arena serves several phases.

Define the partial one-lap map

$$H_W=T_{23}\circ\cdots\circ T_0.$$

Backward composition in phases $23,22,\ldots,0$ computes $H_W^{-1}$.
Starting with $S_0=U_W$, set $S_{n+1}=H_W^{-1}(S_n)$. These finite sets
descend, 和 $S_n$ has exactly the stated $n$-lap trajectory interpretation.
Every cycle of $H_W$, regardless of its period $k$, survives every set.
Therefore an empty set excludes **all $k\ge1$**, not merely fixed points
$H_W(B)=B$. A nonempty fixed survival set contains a cycle by finiteness;
it can also contain paths feeding cycles.

Conversely, a cycle of $H_W$ of period $k$ supplies $24k$ prescribed
exterior edges. Pair them with $k$ copies of the verified center cycle.
Every source satisfies the checker hypothesis 和 every exact edge closes;
$\sum u=8k$, $\sum v=4k$, $\sum g=8k$, so the gain inequality holds.
An actual computed positive must still be extracted 和 independently
replayed as a complete edge list before a candidate or Lean proof claim.

## 3. Exact correlated sets, checkpoints, 和 phase rotation

The implementation imports the immutable, level-preserving digit MDD
engine from PR390. It retains correlations between all coefficients.
Inside one backward lap, both the old lap-root 和 the current intermediate
root survive collection. `collect_many` copies their joint reachable DAG,
returns both remapped identifiers, 和 clears every identifier-keyed cache.
Fixed-point comparison uses those returned identifiers in the same arena.
Identifiers from different arenas are never compared as languages.

A simultaneous rotation of the prescribed phases preserves cycle
existence 和 every lap-period at fixed width. Write the unrotated lap as
$H_0=Q\circ P$, where $P$ is the prefix before the new starting phase,
和 the rotated lap as $H_r=P\circ Q$. On their cyclic vertices,
$P H_0=H_r P$. The prefix map is injective there because $H_0$ permutes
its cyclic vertices; it is surjective with inverse
$y\mapsto Q(H_r^{-1}(y))$. All partial maps in these expressions are
defined on the cyclic vertices concerned.

Transient survival sets may differ between rotations. An eventual witness
must use the correspondingly rotated $e,g,v$ 和 starting center $C_r$.
For rotation 2, the independently reconstructed center is
`[14,14,3,8,3,14,14]`. The last two prescribed overflows then become the
first two backward constraints. The CLI records its normalized starting
phase; a nonempty fixed point also reports one exact surviving seed,
which must be traced forward out of any transient basin.

## 4. Completed computation

From the combined PR390 + this change, no additional Python package:

```bash
ulimit -v 4000000 && timeout 840 python3 calculation/agent-109/target_strobe_mdd.py --width 16 --seconds 780 --node-cap 3000000 --cache-cap 6000000 --phase-progress
```

The original unrotated run completed with exit 0:

```text
S0=273260286537746369382
S1=410578
S2=0
status=EMPTY base=10 width=16 period=24 iteration=2 words=0 seconds=507.582 peak_nodes=2269949 peak_cache=2511028 maxrss_kib=1221292
```

The second backward lap became empty at original phase 13; all remaining
preimages are consequently empty. Width 9 already empties in its first
lap (0.247 seconds, 2,290 peak nodes, 11,520 KiB peak RSS). These results
are complete.

The phase-2 run uses the same command with `--rotate 2`. It also finishes
EMPTY at lap 2, with counts `273260286537746369382,470290,0`.
The differing one-lap transient count is consistent with the rotation
proof; cycle existence 和 lap-period are preserved.

| Phase-2 run | Seconds | Peak nodes | Peak cache | Peak RSS KiB |
|---|---:|---:|---:|---:|
| Completed primary | 147.900 | 1,008,524 | 1,263,324 | 544,096 |
| Final-source rerun | 118.383 | 1,008,524 | 1,263,324 | 556,136 |

Both exit 0. The final-source replay reproduces every intermediate phase
count 和 the complete lap counts. These are measured resource results,
with no guarantee about performance on another machine.

## 5. Independent controls

```bash
python3 calculation/agent-109/target_strobe_controls.py
python3 calculation/agent-109/target_strobe_audit.py --max-width 4 --controls --seconds 180
python3 calculation/agent-109/target_rotation_controls.py --seconds 180
python3 calculation/agent-109/target_multilap_control.py --seconds 55
```

Both controls were authored independently from the new preimage engine.
The arithmetic control reports `ALL TARGET STROBE CONTROLS PASSED`:

| Control | Checked count |
|---|---:|
| Exact center integer/mirror edges | 24 |
| Correlated phase preimages | 216 |
| Source memberships in complete preimage comparisons | 372,624 |
| Correlated target sets | 54 |
| Multi-root collections | 115 |
| Retained-root complete-language checks | 561 |
| Whole-integer/mirror exterior source words | 15,526 |
| Known certificate fixed-phase edges | 56 |
| Wrong-phase rejection controls | 168 |
| Complete repeated-lap preimages | 30 |
| Empty-width phase controls | 244 |

All four $(e,g)$ preimages share one arena per correlated target, directly
exercising separation of phase caches. Collections retain the checkpoint,
four phase roots, an empty root, 和 duplicate roots; exact languages,
levels, topology, unique table, caches, 和 budget history are checked.
All eight established certificates supply fixed-phase positive controls.

The complete-map audit reports `ALL STROBOSCOPIC AUDITS PASSED`:
422 cases, 1,026 complete survivor-set comparisons, 786 checkpoint-set
comparisons, 422 public-run comparisons, 和 46 positive cases.
It explicitly builds whole-word integer maps, composes each driver, 和
peels finite sets. Both collection modes agree. Cases include the pinned
target at widths 0 through 4, exhaustive small paired-bit drivers, 和
known positive drivers repeated two/three times.

A synthetic period-2 partial map with no fixed point checks the explicit
oracle's general cycle-peeling semantics. A stronger physical calibration
was subsequently supplied by Agent105 in
[comment 6433504667](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433504667):

```text
base6 canonical B cycle:
[4,7,7,8,3] -> [9,3,4,5,8] -> [4,7,7,10,2,2]
-> [9,3,4,9] -> first
e=g=0101, natural u=[0,0,2,0]
```

After padding to width 6, its primitive driver is $e=g=01$ 和 its exterior
requires two driver laps. The new control independently replays every
canonical/padded edge 和 the unchanged mirror. A complete 1,610,510-word
oracle agrees with the MDD at every round, both collection modes:
`1610510,20866,1308,128,21,4`, then fixed. The four survivors contain one
two-lap cycle, zero fixed points, 和 two feeders. Exact singleton/set
preimages 和 the returned seed's two-lap orbit also pass: 14 full-set,
22 checkpoint, two public-run, 和 six target-preimage comparisons.
The complete control takes 7.605 seconds/553,780 KiB, exit 0, under a
1.5 GB address-space guard. Agent105 retains the counterexample 和 the
separate all-width one-lap exclusion; this control establishes only the
stated finite-width calibration. No center or full base6 certificate is
claimed for it.

The rotation control reports `ALL ROTATION CONTROLS PASSED`: eight positive
physical drivers, 44 complete cyclic-set rotations, 和 62 public runner
checks. It verifies the exact prefix bijection, its inverse, conjugacy,
cycle partitions, 和 lap-periods. Both collection modes, normalized
rotations 2/26/-22, complete counts, 和 returned seed membership pass.
A separate synthetic control has equal cyclic sets but survival-set
cardinalities 3 versus 2, illustrating the possible feeder difference.

### Interruption checks 和 gate

Each following argument list, appended to
`python3 calculation/agent-109/target_strobe_mdd.py`, exits 2 without
an EMPTY/FIXED_POINT verdict; all seven also pass under `python3 -O`:

| Arguments | Terminal classification |
|---|---|
| `--width 129` | INVALID INPUT |
| `--rotate nan` | argparse input error |
| `--seconds nan` | INVALID INPUT |
| `--rounds 0` | UNDECIDED |
| `--node-cap 1` | UNDECIDED |
| `--cache-cap 1` | UNDECIDED |
| `--width 16 --rotate 2 --seconds 0.000000001` | UNDECIDED |

A separate `--width 16 --rotate 2` subprocess with a 64 MiB address-space
limit also returns UNDECIDED/exit 2: 15 actual failure checks in total.
The complete arithmetic control passes under `python3 -O` as well.
Repository gate: `python3 tools/verify.py --changed`; the actual outcome
和 exact published tree are recorded in the PR. The inherited PR390 MDD
engine is unchanged. This is a six-file delta stacked on that PR.

## Limits

This result requires the exact pinned driver 和 the width bound 16.
It does not settle its all-width/all-laps completion or any other driver.
One-lap all-width results 和 all-lap bounded-width results have different
quantifiers. No decimal certificate or unrestricted route obstruction
has been established here.
