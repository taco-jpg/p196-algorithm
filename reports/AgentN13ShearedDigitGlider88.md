# Agent N13: finite two-ended decimal glider under 88/20 shear

**Label: COMPUTED. Exact scope:** Decimal base 10, two explicit integer seeds, 20,000 ordinary reverse-and-add steps, window of exactly 175 paired positions and times 1000..20000. Not a decimal Lychrel certificate, not an eventual/persistent glider, not Lean-verified.

## Data and construction

Both seeds are generated directly (no external repository data needed) from the reachable period-8/pair-period-20 exterior already tracked in `calculation/decimal_frontier/lattice_formats/p8_scc.txt`: 39-entry phase-zero root path and 20-entry cyclic bulk. For H=5200, the coefficient word P (LSB first) has 10400 entries and is symmetric, with lower-half entries `PATH[j]` for 0<=j<39 and `CYC[(j-39)%20]` afterward. Seed A uses all these entries; Seed B changes the last 100 lower-half entries to `(7*j+11)%19`, mirroring those changed coefficients. Lift each pair coefficient q to an actual digit pair `(min(q,9),q-min(q,9))`. Both leading digits are nonzero. This constructs two distinct valid 10400-digit decimal integers. Their initial paired-coefficient words agree on the exterior and differ near the centre.

Let `A_t`, `B_t` be the ordinary decimal digit lists under `T(N)=N+reverse(N)`. Let `f(t)` be the smallest index j where the sum of the two mirrored digits of `A_t` differs from that of `B_t` (both lists are least-significant-first when indexing). Previous result `AgentN13DecimalShearedFront22` established `f(t+22)=f(t)-5` on 18..19978, and a 20,000-step nonpalindromicity witness. The present result does **not** infer the actual digit equality from that pair-sum equality. It tests the full digits.

## New exact finite-window observation

For each time t in [1000,20000], for every offset r in [-100,74], set j=f(t)+r and k=f(t-88)+r. The C++ checker verifies all four exact digit equalities:

`A_t[j] = A_(t-88)[k]`, `B_t[j] = B_(t-88)[k]`,

`A_t[len(A_t)-1-j] = A_(t-88)[len(A_(t-88))-1-k]`, and the analogous equality for B.

The lengths satisfy `len(A_t)-len(A_(t-88)) = len(B_t)-len(B_(t-88)) = 44`, and `f(t)=f(t-88)-20` throughout the checked interval. Consequently, in least-significant-first absolute indices, the lower digit index moves **-20** while the corresponding upper mirrored digit index moves **+64** (`44+20`). Thus the same spacetime strip translates by different displacements on the two physical ends. The mirror-glued *paired coefficient* did not need to be a symmetric original-digit pattern; the two-ended **actual digits** close on this finite window.

There are 19001 time comparisons, 175 offsets and four digits per offset: **13,300,700 exact digit equality checks**. The first bad check is absent. At immediately adjacent r=75, tests explicitly fail at t=1000,1001 and pass t=1002..20000. Replacing the proposed -20 displacement by -19 fails in 18137 of 19001 tested time comparisons at a single probe, showing the spatial displacement is specific rather than an accidental constant-digit band.

## Independent replication and control

Source `glider.cpp` uses a self-contained byte-array decimal digit carry loop. It maintains both full 20,000-step integer orbits and an 89-snapshot ring buffer; it compares the four individual digit values at every offset. `glider_independent.py` does not call the C++ engine, does not share its carry recurrence or its snapshot logic, and uses built-in Python arbitrary-precision integers and full decimal string conversion to compute `N+reverse(N)` for both seeds through step 2000. It separately checks `1000..2000`: 1001*175*4 = **700,700** digit equalities. It also reproduces precisely the `r=75` failures `[1000,1001]`. `glider_run.sh` builds the C++ engine, checks its exact summary, launches the independent Python checker, and prints `AGENT_N13_SHEARED_DIGIT_GLIDER_PASS` iff every assertion passes.

Reproduce from the repository root:

```sh
bash calculation/new_structures/agent-N13/glider_run.sh
```

Dependencies: GNU-compatible C++17 compiler and Python 3.11+ (Python needs `sys.set_int_max_str_digits`). No external data, internet access, downloaded binaries, hidden seed files or solvers are required. Complexity is O(20000 * ~20000) digit operations in the C++ full replay. The Python control is restricted to 2000 steps to keep the independent bigint check lightweight.

## Exact interpretation and next construction

This is a **moving-front finite digit-window recurrence**, stronger than the first result's 22-step recurrence of a single boundary coordinate. It suggests an 88-time/20-space sheared macro-tile with four digit boundary fields (low/high on each of two orbits). A genuinely finite **infinite-time** certificate would additionally require a closed, time-recurrent **carry boundary contract** for the interior/exterior of that macro-tile and a repopulating source interface to keep the front from exhausting the exterior. These hypotheses remain UNDECIDED. No step past 20000 is proved nonpalindromic by this result, and the current travelling front moves toward the outer boundary, not away from it. The failure at r75 at two early comparison times also shows why one cannot promote a finite matching window to a global all-length identity.
