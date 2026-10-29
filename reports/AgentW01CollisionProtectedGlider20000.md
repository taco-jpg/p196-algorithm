# Agent W01: two-pulse decimal scattering with a surviving 88-step outbound glider

**COMPUTED**, exact finite scope: four explicit 24,000-digit decimal seeds, full independent literal radix-10 and GMP reverse-and-add for 20,000 steps, 20,001 states each. **Not** a base-10 Lychrel number, infinite certificate, Lean proof, or claim about 196.

## Construction and difference channels

Use the already rooted N13 p8/m20 coefficient path `ROOT[39]` and spatial word `BULK[20]` embedded in `w01_collision.cpp` and independently duplicated in `w01_independent.cpp`. Put `H=12000` and `P_j=ROOT[j]` for `j<39` and `P_j=BULK[(j-39)%20]` for `39<=j<H`, mirror the pair coefficients. Lift each coefficient `q` to two decimal digits `(min(q,9),q-min(q,9))` on its low and high paired sides. Four seeds A/B/C/D respectively activate neither, the first, the second, or both disjoint initial perturbations:

* pulse X at paired indices `6000..6049`, setting `P_j=(7j+11)%19`;
* pulse Y at paired indices `8000..8049`, setting `P_j=(3j+7)%19`.

Both inputs remain genuine canonical positive base-10 integers. Let `S_B(t),S_C(t),S_D(t)` be the paired coefficient positions differing from clean A. Let `f_B,f_D` denote their first positions. `overlap` counts `S_B ∩ S_C`, and `unexpected` counts positions where both singles equal A but D differs; `nonlinear` additionally includes positions outside overlap where D is not the unique single-pulse result. These definitions are exact, not approximated by a front velocity model.

## New finite positive interaction

The two single-pulse supports **first intersect at time 2154**. A genuine nonlinear daughter site outside their union first appears at **time 2161**, only seven additions later (contrast N13's earlier 10400-digit / 4000-step collision at different injection sites). This is a new interaction geometry with *both* pulses surviving into a 20,000-step protected-outbound-glider regime.

For every integer `t=1000..20000`, the four-state direct decimal computation verifies `f_B(t)=f_B(t-88)-20`, `f_D(t)=f_D(t-88)-20`, and the common decimal digit length grows by exactly 44 over each 88 steps. For each t and each of 81 paired offsets `r=-40..40`, the **actual low and high digits** of A, B, and D, at their moving paired coordinates, exactly equal their t-88 predecessors: **9,234,486 exact digit equalities**, zero failures. These digit equalities are stronger than a paired-coefficient strip statement; they include the upper side which moves +64 in absolute least-significant-first position while the lower moves -20.

For every time `0..20000`, all four actual decimal pairwords begin with the same rooted 39-coefficient phase followed by complete repeats of the appropriate phase's spatial-period-20 word, at least up to `min(f_B,f_C)`. There are **298,285,792** direct four-orbit pair-coefficient comparisons against the eight-phase 39+20 tile, zero failures. The smallest intact-prefix length is **1456 paired positions**, at the last step, leaving at least 70 complete copies of the spatial word after the rooted 39 columns (`39+70*20=1439`). The 39-column exterior at each phase has an odd coefficient, hence each of the 20,001 states of each orbit is nonpalindromic (odd sum of mirrored digits rules out equal digits). The final decimal length is 34,000.

At t=20000: `f_B=f_D=1456`, `f_C=3459`, `right_B=right_C=16999`, `overlap=12086`, `nonlinear=1326`, and `unexpected=56`. Thus a strongly nonlinear interior can coexist for many iterations with an undisturbed, phase-locked outbound digit/carry channel; nevertheless the interior itself is **not** shown to return to a periodic centre or regenerate the consumed exterior.

## Independent arithmetic and adversarial control

`w01_collision.cpp` computes exact decimal integers as least-significant-first digit vectors with explicit carry, independently constructs four seeds, and checks each of their paired coefficients and the moving physical digits. A 64-bit FNV digest over full most-significant-first D-digit strings and a per-step interaction digest are recorded to detect accidental changes.

`w01_independent.cpp` instead constructs genuine GMP multiprecision integers **from a separately implemented decimal seed generator**, iterates `n += mpz_class(reverse(n.get_str()))`, obtains each full ordinary decimal string independently, tests the first **1456** paired coefficients and odd-witness for **every one of 20,001 states of each of four orbits** (29,121,456 comparisons per orbit), and reports the complete-number FNV64 digest at several keyframes. At t20000 the four independent GMP FNV64 digests, ordered A/B/C/D, are:

`1250752879650488018`, `5226968435340452601`, `16313672923089106462`, `15507195321027655971`.

The six selected full-string digests for D agree *exactly* between implementations, including at the first overlap and first daughter birth. As a negative control, the independent checker deliberately advances the tile phase by one: it rejects at `t=8, j=0`, rather than accepting a merely digit-periodic but wrong clock. `verify_results.py` compares all expected outputs and controls.

Reproduce from repository root:

```sh
bash calculation/new_structures/agent-W01/run.sh
```

Dependencies: `g++` C++17, GNU GMP C++ development libraries, Python 3.11+. No third-party downloaded data, binary, or solver. The wrapper builds both engines, replays **all four** 20,000-step GMP orbits, executes the wrong-phase negative control, checks every expected summary, and prints `AGENT_W01_TWO_PULSE_20K_PASS` only on success. The compact text `expected.txt` contains the control digests and primary measured event counts.

## Towards an infinite collision certificate (UNDECIDED)

The observed scattering has an *outbound protected port* (the 88-phase low/high digit tile and corresponding carry boundary contract) and an *active nonlinear interior port*. A prospective new certificate would require a **finite return or renormalisation map of the interior port**, whose outgoing low/high carry gates equal the next incoming 88-phase tile while the exposed lattice length is nondecreasing after a macrocycle. The glider alone moves **outward** by 20 positions per 88 additions and exhausts any fixed initial buffer: none of the four orbits supplies a proved replacement source. The measured `unexpected` count and the growing nonlinear region are not an interior return map. This explicitly separates a real positive scattering mechanism from the missing regeneration condition. No step beyond 20,000 is established.
