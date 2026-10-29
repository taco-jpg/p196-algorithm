# W01: decimal collision daughter has a nine-geometry 88/60 spacetime covariance

**COMPUTED**, nine explicit finite base-10 collision geometries, each consisting of four distinct ordinary decimal integer reverse-and-add orbits, all replayed through **20,000** steps; **no infinite Lychrel certificate**.

Take the N13 reachable p8/m20 rooted folded-pair lattice (39-coefficient root path, period-20 bulk) and length 24,000. The input coefficient at position `j` is `ROOT[j]` for `j<39`, otherwise `BULK[(j-39)%20]`. Lift each coefficient `q ∈ 0..18` to true decimal digits `low=min(q,9)`, `high=q-low` at symmetric paired positions; this gives a leading nonzero digit. For each second-pulse start `y=8000+80k`, `k=-3,-2,-1,0,1,2,3,4,5`, construct four seeds A (unmodified), B (replace paired coefficients `j=6000..6049` by `(7j+11)%19`), C (replace `j=y..y+49` by `(3(j-y)+10)%19`), and D (both replacements). The coordinate formula makes the *local second pulse* the same at all nine starts.

For step `t`, at mirrored pair offset `j` define the signed *interaction-only residual* of the actual **low** and **high decimal digits** separately, `L_y(t,j)=digitLow(D)-digitLow(C)-digitLow(B)+digitLow(A)` and `H_y(t,j)=digitHigh(D)-digitHigh(C)-digitHigh(B)+digitHigh(A)`. This is a four-orbit nonlinear superposition residual: `R=L+H` is the corresponding folded pair coefficient interaction. Define `f_y(t)` as the **first** index with `R_y(t,j) != 0`, or `-1` when there is no interaction. The tested 61-cell emission tile is `L_y(t,f_y+r), H_y(t,f_y+r)` for every `r=-20..40`. All coordinates are measured against the current exact digit strings (whose length changes on carries).

## Positive finite spacetime-scattering law

For **every** tested `k ≠ 0` and **every integer** reference time

    3020 ≤ t ≤ min(20000, 20000-88k),

all three statements hold in actual decimal arithmetic:

    f_(8000+80k)(t+88k) = f_8000(t) + 60k
    L_(8000+80k)(t+88k, f_(8000+80k)+r) = L_8000(t, f_8000+r)
    H_(8000+80k)(t+88k, f_(8000+80k)+r) = H_8000(t, f_8000+r)

for every `r=-20..40`. There are **134,528 complete aligned time rows**, **134,528 exact front equalities**, and **16,412,416 exact signed-digit equalities**, zero exceptions; these data come from 36 separately evolved actual decimal digit-vector orbits. At every step for each seed, the first 39 paired positions contain at least one odd coefficient, providing an explicit non-palindrome witness; the four orbit lengths agree for each `y` at every step. All initial decimal numbers have 24,000 digits; the `y=8000` family independently checked with GMP in the prior W01 result has 34,000 digits at step 20,000. No statement about different seed lengths is needed for the covariance.

The nonlinear interaction first appears at `(t,f)=(2154+88k,7514+60k)` for **each** of the nine `k`. The final mismatching reference times, when testing covariance from reference time 2300 onward, are `k=-3:2747, -2:2831, -1:2761, +1:2747, +2:3019, +3:2747, +4:2747, +5:2747`. Thus `t=3020` is an inclusive, explicitly tested common stabilization threshold (sharp because `k=2` still mismatches at `t=3019`). For all eight `k`, changing the expected spatial displacement by **+1** fails, as does shifting the phase by **-1** time step, at the reference control `t=3100`.

The spatial-temporal covariance is **not** the N13 single-glider identity `f(t+88)=f(t)-20`. It is a different, *inter-geometry scattering* law `Δy=80k → (Δt, Δf)=(88k,60k)` for an entirely nonlinear daughter signal, after collision; both actual digit tracks follow the same law. It is a promising blueprint for a finite, phase-coded collision port, because the emitted local daughter tile is insensitive to eight independent, finite changes in incoming pulse separation after matching the geometrical delay. The signed interaction residual **does not** claim that the whole four-orbit state, or the growing interaction interior, is identical, or that the centre is re-emitted forever.

## Independent ordinary-integer replay and reproducibility

`w01_scatter_phase.cpp`: generates nine groups of four true 24,000-digit integers, evolves each by literal array-carry reverse-and-add for 20,000 operations, checks matching lengths and an odd-pair nonpalindromicity witness on every step, and emits all 61+61 signed daughter digits plus first interaction front for each time 1750..20000. The compact `phase_verify.py` checks **all** 134,528 aligned source and target time rows; it recomputes every assertion from the generated CSVs rather than relying on a stored trace and checks the explicit wrong-time and wrong-position controls.

`w01_phase_gmp.cpp` is a separate implementation using `mpz_class` in base 10, `get_str`, independent seed assembly, and whole-integer addition with a separately parsed reversed string: it reconstructs both `y=8000` and `y=8080` groups (eight actual decimal orbits), verifies the first collision events `(2154,7514)` and `(2242,7574)`, the last mismatching shifted time `2835` (reference `2747`), and 1,393 exact two-ended shifted tile rows at current times `3108..4500`, rejecting the wrong spatial shift `59` on 2,171 rows. This integer checker **does not use** the C++ digit-vector step, the CSVs, or the CSV checker.

From repository root: `bash calculation/new_structures/agent-W01/phase_run.sh` (GNU C++17, Python 3, GMP). Code and compact controls: `calculation/new_structures/agent-W01/{w01_scatter_phase.cpp,w01_phase_gmp.cpp,phase_verify.py,phase_run.sh}`. The already published companion controls `w01_collision.cpp` and `w01_residual_onset.cpp` independently verify the baseline 20,000-step orbit and the daughter’s within-geometry 88/-20 translation. No bulk trace file is needed or committed.

**UNDECIDED beyond exact finite scope:** whether the eight shifts extend to *arbitrary* `k`, whether local equality holds after step 20,000, whether boundary carry inputs automatically regenerate, and whether a finite centre/gate cycle can be assembled to emit a fresh daughter after every incoming collision. In particular, the front still propagates toward the exterior wall; this is not an infinite-time closure, a Lean proof, a 196 result, or an existence proof for a base-10 Lychrel number.
