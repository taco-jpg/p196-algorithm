# Agent 106 — T2.forward-prefix-completeness

Status: **PAPER PROOF + COMPUTED**. No new Lean theorem is claimed.
Coordination: issue #289, claim comment #6433016484.
Baseline: `eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`.

## Result 和 exact scope

The decimal saturated exterior-prefix relation admits a compatible
temporal period-eight cycle at **every finite spatial depth**. One fixed
infinite coefficient/carry array witnesses all depths simultaneously.
Its first 39 columns form a preperiod, followed by a repeating block of
20 columns. These lengths are 不 asserted minimal.

Consequently, increasing the number of exterior coefficients alone cannot
prove acyclicity in this relation while its inward boundary carries remain
free. The construction supplies neither a finite neutral exterior cycle
nor a matching center. It does 不 decide the complete A120 route.

Each individual prefix edge also lifts to an actual finite A120 source.
Those phase-wise sources need 不 join into one whole-integer orbit.

This PR is standalone on the stated main baseline. It uses the existing
three-column profile 和 A120 Python mirror; it imports no code from PR #351.
Agent 109's backward neutral-tail work retains the terminal conditions
which are absent here, so these results are compatible.

## Exact spatial transfer

All coefficients are least significant first. Temporal phase `t` is read
modulo eight, 和 `g_t = t mod 2`. At spatial cut `j`, retain

\[
S_j=(L_{\bullet,j},H_{\bullet,j},Y_{\bullet,j}).
\]

`L` 和 `H` each contain eight carry bits. `Y` contains the previous
reverse-normalized digit at phases 1, 3, 5, 7. A transition emits one column
`x_t` in `0..18`, chooses inward carry bits `h_t`, 和 obeys

\[
d_t=x_t+L_{t,j}-10L_{t,j+1},\qquad
r_t=x_t+h_t-10H_{t,j},\qquad 0\le d_t,r_t\le9,
\]
\[
H_{t,j+1}=h_t,\qquad
x_{t+1}=d_t+
\begin{cases}r_t&g_t=0,\\Y_{t,j}&g_t=1,\end{cases}
\qquad Y_{t,j+1}=r_t\quad(g_t=1).
\]

The physical outer boundary is `L=0`, `H=g`, 和 `Y=1` at overflow
phases; the first coefficient at every phase is positive. The `Y` slots
record exactly the one-column reverse-digit shift caused by overflow.
The equation at `t=7` includes the temporal return to phase zero.

## Fixed positive witness

The first three coefficients at the eight phases are the existing
`cycleState` profile in
`lean/P196/Agent2SaturatedProfile/Saturated8CycleProfile.lean`:

```text
(8,12,9), (17,5,0), (8,13,5), (17,6,11),
(8,14,8), (17,8,17), (8,16,16), (17,13,14).
```

This profile admits 16 cut-3 states. The fixed witness starts at

```text
L = (1,0,0,1,0,1,1,1)
H = (1,0,0,0,0,1,1,0)
Y = (0,1,8,4).
```

`FIXED_ROWS` in `calculation/agent-106/infinite_prefix.py` gives all
56 emitted columns 和 inward carry rows as transparent integer data.
The first 36 edges reach cut 39. The remaining 20 edges return to the
identical complete cut state:

```text
L = (0,1,0,1,1,0,0,1)
H = (0,1,1,1,1,0,0,1)
Y = (8,8,5,5).
```

Thus cut 59 equals cut 39. The default command checks fixed data;
rediscovery is optional. Canonical witness-core SHA256:

```text
b7e2590318d74ddf06c75e2cbda593977fb3adc83649ee06e17a275e9b4151e6
```

The hash covers root, lengths, states, columns, 和 next-high rows, encoded
as sorted-key compact JSON; timing metadata 和 the source profile are excluded.

## PAPER PROOF: all finite depths survive

Repeat both the complete cut states 和 the emitted transition labels
around the 20-edge spatial loop. Exact equality of the endpoint states
ensures that low carries, reverse carries, 和 delayed reverse digits agree
across every repeated seam. The preceding stem already connects this
loop to the physical first-three-column profile.

This defines one infinite array `x[t,j]` with a temporal return after
eight steps. Fix any finite width `n >= 1` 和 set

\[
P_t^{(n)}=(x_{t,0},\ldots,x_{t,n-1}).
\]

Normalize this word from its low end with incoming carry zero; normalize
it in reverse with incoming carry `H[t,n]`. Induction through the columns
identifies the digits with `d` 和 `r` in the transfer equations. With no
overflow, corresponding digits add. With overflow, the leading one pairs
with the lowest digit, 和 subsequent positions use the stored previous
reverse digit. Hence

\[
\operatorname{prefixAdvance}(P_t^{(n)},H_{t,n})
   =(P_{t+1}^{(n)},g_t).
\]

This argument applies to cuts inside the repeating block, 不 only its
endpoints. Widths one 和 two follow by truncating the initial profile
with its induced carries. At widths at least three, the distinct phase
profiles also ensure least temporal period eight.

Therefore every finite-depth projection with these unrestricted cut
carries contains a closed eight-step path. A sound acyclicity proof
using only such a projection cannot exclude this case at any depth.
Additional information about termination, global invariants, or centers
can still exclude it.

## PAPER PROOF: each abstract edge has a finite source

Let `P` be a positive-head coefficient prefix 和 let `h` be its desired
inward reverse carry. Choose

\[
B=P\mathbin{+\!+}[18h],\qquad C=[18(1-h)].
\]

If `h=0`, the terminal zero of `B` forces `e1=0`, 和 `C=[18]` gives
`e2=1`. If `h=1`, the terminal 18 forces `e1=1`, 和 `C=[0]` gives
`e2=0`. Thus `Hyp` holds. Reverse normalization starts with `e2=1-h`;
its first coefficient, `18h`, emits carry `h` into `P`. The first `|P|`
coefficients of `nextB` 和 its overflow are therefore exactly the
prefix transition above. This also works in base `b>=2` with `2b-2`
in place of 18, assuming every coefficient of `P` lies in `0..2b-2`
和 `h` is a bit.

The appended coefficients depend on the phase 和 cut. This lemma gives
local source realizability, **不** temporal closure of those finite sources.

## COMPUTED validation

Commands from the repository root:

```bash
python3 calculation/agent-106/infinite_prefix.py
python3 -O calculation/agent-106/infinite_prefix.py
python3 calculation/agent-106/infinite_prefix.py --search
python3 calculation/agent-106/infinite_prefix.py --json
python3 calculation/agent-106/infinite_prefix_audit.py
python3 -O calculation/agent-106/infinite_prefix_audit.py
python3 tools/verify.py --changed
```

Default witness output:

```text
initial_cut3_states=16
SPATIAL_LASSO VERIFIED_LOCAL_EQUATIONS stem_after_cut3=36 spatial_preperiod=39 loop_columns=20
```

Rediscovery stops at a positive witness after 7,599 visited states 和
7,664 explored edges. These are **partial-search** counts, 不 exhaustive
graph sizes. Default limits are 500,000 states 和 55 seconds; exceeding
a limit reports `UNDECIDED`. Fixed-witness validation needs no search.

Both ordinary 和 optimized-Python independent audits exit zero:

```text
LOCAL_LASSO_AUDIT PASS stem=36 loop=20 tiles=56 sha256=b7e2590318d74ddf06c75e2cbda593977fb3adc83649ee06e17a275e9b4151e6
malformed_witnesses_rejected=5 explicit_validation=True
INTEGER_PREFIX_AUDIT repetitions=0 every_cut=1..39 phase_edges=312 PASS
INTEGER_PREFIX_AUDIT repetitions=1 every_cut=1..59 phase_edges=472 PASS
INTEGER_PREFIX_AUDIT repetitions=2 every_cut=1..79 phase_edges=632 PASS
INTEGER_PREFIX_AUDIT repetitions=5 every_cut=1..139 phase_edges=1112 PASS
INTEGER_PREFIX_AUDIT repetitions=16 every_cut=1..359 phase_edges=2872 PASS
INTEGER_PREFIX_AUDIT repetitions=64 every_cut=1..1319 phase_edges=10552 PASS
RANDOM_INTEGER_DEPTHS seed=106 depths=64 range=157..1000 phase_edges=512 PASS
A120_LOCAL_SOURCE_LIFTS samples=64 seed=106120 width_range=1..1000 high_carry_counts=[31, 33] PASS
INFINITE_PREFIX_AUDIT PASSED integer_phase_edges=16464 max_width=1319
```

The independent checker expands every local carry equation directly.
For its integer reference it forms the number represented by
`P ++ [18h] ++ reverse(P)`, obtains ordinary decimal digits with `str`,
和 adds paired digits. It imports no generator normalization/transition
routine to calculate the reference output. Supplementary checks compare
64 actual A120 sources against the unchanged main-branch mirror.
Both validators use explicit exceptions, including length checks before
iteration; optimization does 不 disable them.

The all-depth conclusion follows from the finite loop proof, 不 from
extrapolating the 16,464 finite arithmetic samples. The samples audit
the interpretation 和 implementation independently.

`verify.py --changed` passed on the final code/report snapshot: 5,217 Lean
files, 301 projects, zero changed Lean modules, zero new endpoints.
This is the required repository gate, 不 Lean verification of this result.

## Remaining scope

There is no finite neutral terminal condition in the exhibited lasso.
Avoiding acceptance along one infinite path does 不 prove acceptance
unreachable along every other branch. No full B-cycle, B+C cycle,
`cycleOK 10` certificate, or decimal Lychrel existence theorem is claimed.
The result establishes the exact limitation of free-boundary exterior
prefix exclusion while leaving stronger approaches open.
