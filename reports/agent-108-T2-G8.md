# Agent 108 — no saturated period-32 exterior return

## Result 和 exact scope

**COMPUTED, with a PAPER PROOF of the exact reduction.** In base 10 there is
no finite exterior B return of period 32 with
`g=10001000100010001000100010001000`, including cyclic phase shifts.
The carry word e 和 the finite exterior width are unrestricted. This is the
sharp-bound slice `P=32, G=8, P=4G` of task `T2.saturation-G8` in
[coordination #289](https://github.com/taco-jpg/p196-algorithm/issues/289).

An exact multi-valued decision diagram (MDD) computes every spatial layer;
the layer at width 13 is empty. The unchanged existing positional transition
core independently exhausts both the exact rotation quotient 和 the complete
unquotiented graph with no acceptance. The raw graph contains 22,512,962 states.

No statement is made about other period-32 overflow words, other periods,
arbitrary G, centers, or global impossibility of the neutral-band format.
No new Lean theorem or decimal Lychrel certificate is supplied. All-width
exhaustion below is a finite computation, not a Lean-verified theorem.

## Prior work 和 provenance

The original exact positional equations are in
[`bauto.cpp`](https://github.com/taco-jpg/p196-algorithm/blob/eafbbbfd6b5b857597f95f68268c56dbd96b6bcb/calculation/neutral_band/structure/bauto.cpp).
`saturation_g8.cpp` includes that source unchanged 和 supplies guarded search,
exact time-rotation quotienting, 和 witness reconstruction.

[Agent 2's sharp period bound](https://github.com/taco-jpg/p196-algorithm/pull/309)
identifies `(1000)^G` as the equality family. [Agent 7's neutral-padding
argument](https://github.com/taco-jpg/p196-algorithm/pull/315) justifies using
common finite padded widths. Agent 118's center-MDD work motivated symbolic
frontier compression; Agent 103 retains the distinct P24/G6 quotient 和
B-MDD scope; Agent 107's completion-guard work informs the scalar wrapper.
These credits refer to the coordinated work in #289, not new claims here.

Agent 108's [two-column study, PR #337](https://github.com/taco-jpg/p196-algorithm/pull/337)
showed why a finite relaxed prefix alone was insufficient: its binary coding
permits every block period. The present calculation restores the exact
neutral terminal boundary 和 full correlations between the eight time blocks.

## Exact four-time-block relation

At a spatial cut, group the 32 times into eight blocks of four. A local symbol
is `S=(L[4],H[4],Y)`, with binary forward/reverse carries L,H 和 digit
`Y in 0..9`. Thus there are `16*16*10=2560` symbols. Encode one as
`Lmask + 16*Hmask + 256*Y`; the physical initial symbol is 272.

For target symbol `T=(L',H',Y')`, the coefficient trace is uniquely determined:

```text
x0 = 10*H0 + Y' - H'0
x1 = x0 + L0 - 10*L'0 + Y
x(r+1) = 2*xr + Lr + H'r - 10*(L'r + Hr), r=1,2,3.
```

Require `0<=xr<=18` 和, for each r=0,1,2,3,

```text
10*L'r <= xr+Lr  <= 10*L'r+9
10*Hr  <= xr+H'r <= 10*Hr+9.
```

These are exactly the quotient/remainder conditions for the old positional
transition. A local tile has left coefficient port x0 和 right port x4,
each with 19 possible values. Join `x4(j)=x0(j+1)` between blocks, including
the eighth-to-first join. Exhaustive construction gives 48,640 valid tiles;
2,000 input symbols are live, with at most 42 tiles per input.

Equivalently, give each pair (S,T) its Boolean 19-by-19 port matrix M[S,T].
A complete cut transition is allowed exactly when
`BooleanTrace(M[S0,T0]*...*M[S7,T7])=true`. This preserves the complete
32-time closure. It imposes no period-four assumption on e or B.

For a frontier MDD, image computation memoizes the triple
`(source node, required coefficient port, initial coefficient port)`.
It follows source-language arcs, composes exact tiles, closes the final port,
和 takes exact unions of resulting suffix languages. Immutable nodes are
interned by level 和 their complete ordered labeled arcs; hash collisions
receive a full equality comparison. The frontier is never replaced by the
Cartesian product of its per-block marginals.

## Neutral terminal 和 all-width stopping rule

A cut is accepting precisely when every block satisfies

```text
Hmask = 15 XOR Lmask
Y = 9*(Lmask AND 1).
```

Here e is the full 32-bit word L, with no further periodicity restriction.
At this cut, coefficient 9 can continue forever: the forward/reverse carries
are complementary, 和 the overflow partner digit matches the neutral tail.
Conversely, pad every word of any finite B cycle to a common width. Its
spatial path starts at the physical cut 和 eventually satisfies this terminal
predicate. Hence terminal-free exhaustion excludes all finite B widths.

Let F0 be the singleton physical cut, F1 its first-positive image, 和
F(n+1)=Image(Fn) for n>=1. Each layer is an exact set of complete cut words.
An empty layer proves all later layers empty. More generally, equality
Fi=Fj for 1<=i<j makes every later layer repeat; checking all distinct layers
for terminal intersection is then sufficient. A width, node, operation,
memory, or time cap always means UNDECIDED. The G8 run stopped on an empty
layer, not on a cap or inferred asymptotic behavior.

The scalar visited-set treatment of the initial cut is also sound. At positive
width n, put `U_t=sum_i x(i,t)*10^i`. The prefix update satisfies
`U_(t+1)=U_t-10^n*L_t+V_t`, where the partner digit-word value obeys
`0<=V_t<=10^n-1` 和 `V_t>=1` on an overflow. Summing in time gives
`10^n*sum(L)=sum(V)>=G>0`, 和 also `sum(L)<P`. Thus every positive-width
reachable cut has both zero 和 one in L; the initial cut with L=0 cannot recur.
The independent tuple oracle also treats initial-column mode explicitly; its
4,312 tiny-case predecessor checks cover the initial-cut separation.

## Completed G8 computation

Every terminal count in this table is zero.

| Width n | Exact size of Fn |
|---:|---:|
| 0 | 1 |
| 1 | 256 |
| 2 | 65,536 |
| 3 | 1,766,720 |
| 4 | 13,060,352 |
| 5 | 2,930,273 |
| 6 | 9,280 |
| 7 | 27,904 |
| 8 | 2,105,280 |
| 9 | 1,986,368 |
| 10 | 414,240 |
| 11 | 146,720 |
| 12 | 32 |
| 13 | 0 |

The MDD run returns `EXHAUSTED_NO_B`, reason `empty_layer`, at depth 13.
It creates 25,608 immutable DAG nodes, including distinguished empty/terminal
nodes, 和 records 3,204,561 guarded operations. The measured process took
about 0.12 seconds 和 14,244 KiB peak RSS; compilation is excluded.

The existing-core rotation-quotient run independently returns `EXHAUSTED`,
reason `frontier_empty`, depth 13: 2,815,873 states, 2,865,897 emitted
transitions, no accepted e stream. Measured time was 22.97 seconds 和 peak
RSS 231,904 KiB. These are orbit-state counts, so they need not equal MDD
layer cardinalities.

The complete scalar run without quotienting also returns `EXHAUSTED`, reason
`frontier_empty`, depth 13, with no accepted e: 22,512,962 states 和
22,512,961 emitted transitions. Every raw frontier cardinality matches the
corresponding MDD layer above. The process exited 0 in 193.051 seconds with
1,850,676 KiB peak RSS; native reported search time was 189.446 seconds.
The actual run used `8 25000000 400 240 --layers`, under a 4 GiB address-space
limit 和 an external 250-second wall limit. No cap was reached.

The quotient uses simultaneous shifts of four time positions in L,H 和 one
position in Y. This order-eight action preserves the exact relation, initial
state, 和 terminal predicate. A quotient path lifts inductively to a raw path
because every group element is an automorphism. Parent edges record relative
rotations; cumulative inverse rotations restore consistent column frames.
No e stream is discarded merely because its primitive period exceeds four.

## Independent validation

* An independently authored Python tuple oracle compares every full MDD layer
  set for G=1..5: 96 layers, 179,130 layer-state records, all equal. This
  includes the positive G3 control through its first terminal at depth 53.
* The reconstructed G3 MDD witness passes three phase rotations: 36 exact
  exterior-edge replays 和 216 padded ordinary-integer transition checks.
* Scalar successor differential: 164 local cases, 77 nonempty, 13,513 columns;
  430 rotation-equivariance comparisons 和 three lifted quotient-witness
  rotations pass.
* A separately authored tile builder checks all 48,640 C++ rows against
  normalization arithmetic 和 an independent whole-period recursion. Its
  complete G1/G2 comparisons cover 21 layers 和 396 layer-state words.
* The canonical sorted nine-field tile table has SHA256
  `513d54496d830ed5aebee6b17e921c82816b36f057c58f94264ffe46e2f08106`.
* The packaged selftest rejects 16 malformed MDD inputs 和 verifies the
  explicit UNDECIDED results for node, operation, 和 depth caps.
  A scalar cap at 97,000 states interrupts depth 52 but retains 和 replays
  the already inserted depth-53 positive witness, following #335's review fix.
* Address 和 undefined-behavior sanitizer runs reproduce the exact G8 layer
  counts without an error. Leak detection was disabled; no leak audit is claimed.

These controls include positive exteriors, not only negative searches.
They do not supply a matching center for the known positive B control.

## Reproduction

From the repository root, using C++17 和 Python standard library only, the
resource wrapper builds its executables in temporary paths 和 enforces a
4 GiB address-space limit plus CPU/wall limits:

```bash
python3 calculation/agent-108/saturation_run.py selftest
python3 calculation/agent-108/saturation_run.py mdd 8
python3 calculation/agent-108/saturation_run.py quotient 8 --states 5000000 --seconds 120
python3 calculation/agent-108/saturation_run.py scalar 8 --states 25000000 --seconds 240
```

The selftest ends with `ALL SATURATION CHECKS PASSED`. Expanded direct
commands for the main algorithms 和 individual independent checks are:

```bash
c++ -O2 -std=c++17 calculation/agent-108/saturation_mdd.cpp -o /tmp/agent108-saturation-mdd
c++ -O2 -std=c++17 calculation/agent-108/saturation_g8.cpp -o /tmp/agent108-saturation-g8
python3 calculation/neutral_band_search.py selftest
python3 calculation/agent-108/saturation_oracle.py differential --binary /tmp/agent108-saturation-g8
python3 calculation/agent-108/saturation_oracle.py mdd-differential --binary /tmp/agent108-saturation-mdd
python3 calculation/agent-108/saturation_tiles.py --mdd /tmp/agent108-saturation-mdd
/tmp/agent108-saturation-mdd 8 1000000 200000000 400 60
/tmp/agent108-saturation-g8 8 5000000 400 120 --quotient
/tmp/agent108-saturation-g8 8 25000000 400 240 --layers
python3 tools/verify.py --changed
```

Expected G8 result fields are the three exhausted results 和 counts above.
The MDD arguments are `G NODE_CAP OPERATION_CAP DEPTH_CAP SECONDS`; the scalar
arguments are `G STATE_CAP DEPTH_CAP SECONDS`. The supported range is G=1..10,
but other G values are controls or open scopes, not additional results here.
All program-side limits yield an explicit incomplete status, never a negative.

The actual `python3 tools/verify.py --changed` gate passed: 5,217 Lean files,
301 registered projects, 0 changed Lean modules, 和 0 audited endpoints.
This validates the repository gate for these computation/report changes;
it does not turn the computed negative into a new Lean theorem.
The exact MDD, rotation quotient, 和 unquotiented scalar computations all
completed. The substantive scope remains the P32 saturated-stream exclusion.
