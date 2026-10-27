# Agent 110 — Period-12 centers through width 14, every repetition

## Status 和 precise scope

**PAPER PROOF + COMPUTED.** For the documented decimal driver

```text
e = 101010010101
g = 100010001000
```

there is no A120 center cycle at **any repetition count k** whose every
center has width at most 14. The statement also covers the three documented
carry-stream rotations, because they differ by joint four-step rotations
that preserve `g`. Arbitrary natural center trims are included.

This strengthens Agent 6's prior uniform-width-10 exclusion in
[issue296](https://github.com/taco-jpg/p196-algorithm/issues/296).
It leaves unrestricted center widths open. It does 不 exclude other decimal
drivers, establish a decimal Lychrel number, or provide a new Lean theorem.

The width-preserving balanced theorem is Agent 110's
[PR338](https://github.com/taco-jpg/p196-algorithm/pull/338), built on
Agent 7's neutral-padding covariance 和 Agent 107's schedule transport.
The specialized argument needed here is repeated below, so the computation
has no executable dependency on PR338 or another review branch.

## 1. Why one finite graph covers all repetitions

Write `P_a(C)=9^a ++ C ++ 9^a`, 和 let `F_t(C)` be raw `nextC`
for the fixed entering carry `e_t` 和 overflow `g_t`.
A legal center edge satisfies

\[
\operatorname{carry}(C_t,e_t)=1-e_t,
\quad F_t(C_t)=P_{v_t}(C_{t+1}),
\quad m_{t+1}=m_t+g_t-2v_t.
\]

Centers are nonempty. In a cycle they are symmetric, with coefficients
in `0..18`, since every raw center image is a reflected digit sum.
Closed length accounting gives `2 sum(v)=sum(g)=3k`, so **k is even**.

Let `S_t=sum(g_j,j<t)`, `r_t=S_t mod2`, 和 define

\[
w_t^-=\lfloor S_{t+1}/2\rfloor-\lfloor S_t/2\rfloor,
\qquad
w_t^+=\lceil S_{t+1}/2\rceil-\lceil S_t/2\rceil.
\]

For any uniform cap `W>=2`, the two target width profiles are
`L_t^-=W-1+r_t` 和 `L_t^+=W-r_t`.
Choose the profile matching the original initial width parity. At every
phase, `L_t` is the largest integer at most `W` of the original width parity;
therefore `a_t=(L_t-m_t)/2` is a nonnegative integer. The length equations give
`a_(t+1)=a_t+v_t-w_t`.

Under the carry flip, neutral padding preserves the entering/exiting carries
和 obeys `F_t(P_a(C))=P_a(F_t(C))`. Thus

\[
F_t(P_{a_t}(C_t))
=P_{a_t+v_t}(C_{t+1})
=P_{w_t}(P_{a_{t+1}}(C_{t+1})).
\]

This constructs the chosen balanced profile without increasing the cap.
It covers original width-one phases as well: the padded widths are positive.
Conversely, a balanced cycle is already a legal cycle under the cap.

For this driver, each 12-step block has three overflows. Hence
`r_(t+12)=1-r_t`, while `e,g` are unchanged. A 12-step time shift swaps
the two profiles 和 their trim schedules. It suffices to use the floor
profile, whose trims in a doubled 24-step block occur at zero-based phases
**4,12,20**. Any even-k cycle becomes a cycle of its 24-step return map.

Anchor that return map at original phase 4. Its source width is `W` 和
its edge has `e=g=v=1`. More generally, for any overflow edge with a positive
neutral trim, source head `a` satisfies

\[
((a+e)\bmod10)+9e=9,\qquad 0\le a\le18.
\]

For either bit `e`, this forces `a=9`. Source symmetry forces both endpoints,
so the source is exactly `C=[9] ++ D ++ [9]`, with symmetric `D`.
At this anchor the rotated trim positions are **0,8,16**.

Enumerate every such width-W source, follow exactly 24 forced carry/trim
steps, 和 retain an edge only if the result again has width W 和 endpoints9.
All intermediate widths are checked against the prescribed `W,W-1` profile.
This is a partial function. A temporal cycle gives a directed cycle in this
finite graph; every directed cycle conversely supplies a center cycle for
the same repeated driver. This equivalence concerns centers, independently
of whether a matching exterior is supplied.

## 2. Exact finite domain 和 completed counts

State IDs use the independent half-word of `D`, least significant first:

\[
\mathrm{id}=\sum_{j=0}^{\lfloor(W-1)/2\rfloor-1}D_j19^j,
\qquad N=19^{\lfloor(W-1)/2\rfloor}.
\]

Every coefficient choice is enumerated. There is **no** residue, odd-middle,
or maximally-stripped-state filter. Extra states that cannot occur in a
cycle are harmless; omitting cycle states would not be harmless.

| W | Enumerated states N | Initial carry flip | Complete 24 steps | Retained return edges | Cycles | Max return path |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | 1 | 0 | 0 | 0 | 0 | 0 |
| 3,4 each | 19 | 9 | 0 | 0 | 0 | 0 |
| 5,6 each | 361 | 180 | 0 | 0 | 0 | 0 |
| 7,8 each | 6,859 | 3,429 | 0 | 0 | 0 | 0 |
| 9,10 each | 130,321 | 65,160 | 0 | 0 | 0 | 0 |
| 11 | 2,476,099 | 1,238,049 | 32 | 32 | 0 | 1 |
| 12 | 2,476,099 | 1,238,049 | 0 | 0 | 0 | 0 |
| 13 | 47,045,881 | 23,522,940 | 335 | 327 | 0 | 1 |
| 14 | 47,045,881 | 23,522,940 | 163 | 148 | 0 | 1 |

All rows have `evaluated_states=finished_states=N`, `cycle_scan_complete=true`,
和 terminal `NO_CENTER_CYCLE`, exit0. Completed 24-step images that lack
the next anchor's required endpoints are excluded from the return graph:
eight at W13 和 fifteen at W14. Every initial-flip count equals `(N-1)/2`.
Indeed, coefficient complementation `d -> 18-d` pairs opposite exiting
carries: the most significant non9 coefficient fixes the carry, 和 later9s
transmit it. The sole fixed point is all9, which transmits entering carry1
和 fails the required exit0. This includes empty D at W2.

Final C++ runtimes for W11..14 were respectively 0.210285,0.256378,4.76556,
5.11328 seconds. Peak child RSS was415232KiB. A successful partial return
is **not** a cycle: e.g. W11 source421084 maps to1854137, whose next return
fails; source702607 maps to1944526, which also fails.

## 3. Reproduction 和 independent controls

Run from the repository root:

```bash
g++ -O3 -std=c++17 -Wall -Wextra -pedantic \
  calculation/agent-110/p12_balanced_graph.cpp -o /tmp/p12_graph
/tmp/p12_graph 11
/tmp/p12_graph 12
/tmp/p12_graph 13
/tmp/p12_graph 14
python3 calculation/agent-110/p12_balanced_reference.py 2 3 4 5 6 7 8 9 10
python3 calculation/agent-110/p12_balanced_reference.py 11 12 \
  --max-states 2500000 --seconds 90
python3 calculation/agent-110/p12_balanced_reference.py 11 14 \
  --max-states 50000000 --seconds 900
python3 calculation/agent-110/p12_balanced_controls.py --binary /tmp/p12_graph
python3 tools/verify.py --changed
```

The primary implementation uses ordinary carry propagation 和 an exact
functional-graph traversal. It supports widths2..14, uses uint32 state IDs,
checks an explicit allocation bound below1GB, 和 defaults to a1500-second
wall cap. A forced `14 --seconds 1` run returns `UNDECIDED`/exit2.
Invalid input, allocation failure, or internal errors cannot yield a negative.
`--map W` consumes IDs on stdin 和 emits `ID NEXT`, with `NEXT=-1` for failure.

The separately authored Python reference imports none of the repository
mirror, C++ implementation, or other Agent110 checker. It evaluates each
whole positional integer, recovers digits with `divmod`, stores only successful
return edges, 和 uses Kahn indegree peeling. Vertices outside the retained
edge endpoint set are isolated 和 counted as removed without allocating N
entries. It still enumerates **every** source. Its state/time limits produce
`UNDECIDED`, 和 optimized Python is explicitly rejected.

Independent complete W2..12 和 W14 runs reproduce every corresponding count
above. W11/W12 took16.75/19.02 seconds before the sparse-storage adjustment;
the final sparse W11 regression took15.913464 seconds 和 again retained32
edges, with every state removed. The final **complete W14** reference run
took420.415748 seconds, exit0, with this exact terminal output:

```json
{"completed_returns":163,"cycle_nodes":0,"domain_states":47045881,"edges":148,"initial_flip_valid":23522940,"period":24,"removed":47045881,"seconds":420.415748,"start_phase":4,"status":"NONE","width":14}
```

The independent reference's controls pass four base26 positive center edges,
14479 state-code roundtrips, 和48 floor/ceiling profile-shift checks.
The third checker uses the baseline Python mirror 和 independently verifies:

- 7686 forced-endpoint equations across bases2..62.
- 10000 random padded sources of widths2..30,19222 eligible covariance edges.
- All56 center edges from the eight existing source certificates.
- 24497 C++ return-map comparisons, zero mismatches: every14479 source at
  W2..8;10000 seeded sources at W9..14;16 independently successful W11 return
  sources; 和 their two terminal targets.
- 24467 prescribed p12 step attempts in those controls, including failures.

## 4. Verification status 和 remaining question

Literal `python3 tools/verify.py --changed` returned:

```text
[rules] 5217 Lean files, 301 projects, OK
[changed] against origin/main: 0 new/changed Lean file(s); building 0 module(s); auditing 0 project(s)
[build] up to 1 Lean file(s) at a time
[build] OK
[axioms] 0 endpoints checked
ALL CHECKS PASSED (changed files only, against origin/main)
```

This validates the repository gate for a code/report-only change. It does
不 turn the padding argument or exhaustive computation into a
kernel-checked theorem. No Lean file or registry entry is changed.

The remaining T3 question is whether this driver has a center cycle at
some larger width 和 even repetition. Finite-cap exhaustion does 不 resolve
that question or establish that the neutral-band route cannot work.
