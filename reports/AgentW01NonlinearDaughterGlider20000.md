# Agent W01: a phase-locked nonlinear daughter glider survives two-pulse scattering

**COMPUTED**, finite decimal reverse-and-add statement only. A new **interaction-only** moving defect is extracted from four exact 24,000-digit seeds (A clean, B patch X, C patch Y, D both) and checked for steps 0..20,000. This is *not* a decimal Lychrel certificate, proof about 196, or infinite scattering law. Initial numbers and the two disjoint 50-pair changes at j=6000 and j=8000 are completely specified in `AgentW01CollisionProtectedGlider20000`.

Let `q_K(t,j)` be the paired coefficient (sum of two mirrored ordinary decimal digits) of orbit K. Define the **signed interaction residual**, rather than a set union of affected positions,

`R(t,j) = q_D(t,j) - q_B(t,j) - q_C(t,j) + q_A(t,j)`.

For physical low and high digits define *separately* `L(t,j)=d_D^low-d_B^low-d_C^low+d_A^low` and `U(t,j)=d_D^high-d_B^high-d_C^high+d_A^high`, so `R=L+U`. The index j is paired position from the low end, so the physical upper absolute position changes when total digit length grows. The residual is a genuine four-orbit nonlinear correction; it vanishes identically when the two pulse effects add linearly, even if their supports overlap.

The first nonzero R occurs at **t=2154**, at precisely two paired sites j=7514..7515 (`R` signed sum 9, L1 norm 11). From **every t=2242..20000**, the first nonzero position `g(t)` obeys the exact spatial macrotranslation `g(t)=g(t-88)-20` (17,759 successful front comparisons, zero failures). This nonlinear boundary therefore propagates at the same outward speed as the original N13 glider, even after the collision.

More strongly, let the **two-ended signed residual tile** be the 61 positions `j=g(t)+r`, `r=-20..40`, and store both L and U, not just R. There is an explicit transient: the 88-step translated tile fails at some times through **t=2835**, and then, for **all 17,165 consecutive times t=2836..20000**, satisfies *both* physical-digit residual equalities

`L(t,g(t)+r) = L(t-88,g(t-88)+r)` and `U(t,g(t)+r) = U(t-88,g(t-88)+r)`

for every `r=-20..40`. Consequently the R tile also translates identically. This is **2,094,130** exact low/high residual-value equalities (`17165*61*2`), in addition to 17,759 front comparisons. The tile moves -20 actual low-digit positions but, given +44 decimal length per 88 steps, the mirrored high-side position moves +64. The tile is thus a nonlinear **two-ended daughter glider** with a stable finite observed phase-88 carry-coupled footprint, not merely a pair-sum illusion.

At t=20,000, `g=3459`, rightmost residual index 16999, 13,018 nonzero residual coefficients, signed sum -198, L1 norm 112,648. The nonlinear interaction region has grown enormous, yet its **outermost local daughter interface** continues to translate identically. This suggests a new possible centre-junction FORMAT: an independently pumpable exterior, a nonlinear interaction region of unbounded width, and a finite **signed-scattering port** whose two physical digit differences and carry gates repeat after a macrocycle. To become an infinite certificate, the interaction region must regenerate all incoming port conditions and ensure nonnegative net buffer change. Here that global closure remains **UNDECIDED**; the verified front moves outward and will exhaust a fixed buffer.

## Independent arithmetic and controls

`w01_residual_onset.cpp` evolves all four ordinary decimal digit vectors through 20,000 reverse-and-add operations. It constructs the full signed residual at every step, tests front propagation for all t=2242..20,000, and stores an 89-timestep ring buffer of **both** physical-digit residual windows. It computes the exact last failure t=2835 rather than selecting an arbitrary stable start.

`w01_scatter_gmp.cpp` reconstructs all four independently as GMP multiprecision integers, iterating `N += reverse(N)` using decimal strings. It independently recomputes both low/high signed residual windows at every step through 6,000, checks the same sharp onset t=2835, and verifies all **3,165** 88-step residual comparisons t=2836..6000. This checker does not import the digit-vector step or its residual arrays. A negative control changes the predicted spatial displacement to -19, which immediately fails at t=2836 (actual front 7359 versus predecessor 7379).

One-command reproduction, C++17/GMP/Python3, no network and no external data:

```sh
bash calculation/new_structures/agent-W01/residual_run.sh
```

The script compiles the two independent engines, runs the full 20,000-step residual profile and the 6,000-step independent GMP control, tests the wrong-shift mutation, validates the exact counts using `residual_verify.py`, then prints `AGENT_W01_NONLINEAR_DAUGHTER_20K_PASS`.
