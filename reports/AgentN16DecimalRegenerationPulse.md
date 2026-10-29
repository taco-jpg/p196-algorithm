# Agent N16: transient outward-pumping decimal centres
**COMPUTED.** Every number, digit and pairword is genuinely decimal. This report identifies a positive, finite centre repair mechanism, **not** a decimal Lychrel proof.

## Construction
Use the known p8/m20 rec0 phase rows B_t (39 entries) and W_t (20 entries), coefficients 0..18, encoded base19 by 0..9,A..I, in `rows.txt`. For any q≥1 and any finite centre HALF-WORD C (coefficients 0..18), form symmetric pairword
`P_q(C)=B_0 ++ W_0^q ++ C ++ reverse(C) ++ reverse(W_0)^q ++ reverse(B_0)`.
Realise it as a valid positive decimal integer by setting each lower-half digit `a_i=max(0,P_i-9)` and its mirrored upper digit `a_(L-1-i)=min(9,P_i)`. This produces an even-digit seed with the stated pairword.

Let M_q(t) denote the longest prefix of the ACTUAL evolved pairword matching the known infinite eight-phase exterior `B_(t%8) W_(t%8)^infinity`; set `D_q(t)=39+20q-M_q(t)`. Negative D means the periodic exterior has grown beyond the original nominal boundary. For C empty, the separately committed N16 front clock gives D(264)=60 and D(20000)=4545 at q300.

## Two positive centre emissions
The short 16-coefficient core `87FEBC813IFI5D46` first matches only the original 39+20q outer coefficients at t=0 but, at t=22, **matches six more**: D(22)=-6 (q=5, q=20 and q=300 replay). It is a genuine outward 22-step pulse, not an infinite centre solution. By t=66 its D is 0 again, by t=264 it is 45.

The 28-coefficient core `HEBBBCI8D2545G2HFAHE39AH9IF2` achieves much better *longer* repair. It has D(0)=-1, D(22)=-1, D(88)=0, **D(264)=2**, D(528)=61, D(792)=121, D(1000)=170, D(5000)=1078, D(10000)=2215, D(20000)=4487 at q=300. The q301 values of D at step 20000 are the same. Comparing with the empty-centre D(264)=60 shows a 58-coefficient gain in one macrocycle, but D(528)=61 confirms failure of renewal. The q300 seed has 12,134 digits; after exactly 20,000 steps it has 22,134 digits and still at least 1,552 matching coefficients.

## Fully reproducible search and checks
`sh calculation/new_structures/agent-N16/regeneration_pulse/run.sh`
compiles three independent C++17 programs:
- `search.cpp` uses fixed MT19937_64 seed 20261028 to sample exactly 600,000 random half-centres of lengths 1..30 at q5, screens their 22-step gain, and retests promising ones at 264 steps. Its deterministic 264-step winner is `HEBBBCI8D2645G2HFAHE3CG5IG8F2`, score M264−(39+20q) = -20.
- `evolve.cpp` starts from that winner, runs 30,000 deterministic local mutations, and produces the final 28-character centre with score -2. The random search is a *discovery tool*, not exhaustive evidence of optimality.
- `replay.cpp` independently calculates both the literal GMP integer N+reverse(N) and a separate LSB-first digit-vector carry sum, comparing the entire integers on every step. It checks the eight-phase pairword prefix, nonpalindromicity, and alternating digit overflow at all 20,001 timestamps for q300 and q301; separately controls the six-cell 22-step pulse at q5. No mere template prediction replaces true integer replay.

## Why this redirects the construction
The *known* absorbing outer lattice is compatible with a centre producing new periodic coefficients. The successful 22-step six-cell excursion and 264-step 58-cell retention mean that a glider generator is not obviously obstructed by congruences alone. Yet the improvement is a **single pulse**: after that, the front returns to its usual speed about 60 cells inward per 264 steps. The next certificate format should track a **train or substitution hierarchy of centre pulse packets** whose output over every 264-step CRT-aligned macrocycle replenishes at least 60 bulk coefficients. The 12-lane CRT clock (orders 2/4/6 for 99/101/1001) aligns at 264 steps with the period-8 temporal and period-20 spatial clocks. No finite sustainable packet cycle was found or claimed.
