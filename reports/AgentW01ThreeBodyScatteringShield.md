# W01: a third decimal pulse screens an outgoing two-pulse daughter and creates an antipodal displaced glider

**COMPUTED**, 8 explicit ordinary base-10 reverse-and-add orbits, all 20,000 steps; 8 independently replayed with GNU GMP through 6,000 steps. Not a decimal Lychrel certificate, an all-time particle theorem or a Lean result.

## Three-packet input and three-body residual

Use exactly the already published N13/W01 reachable p8/m20 exterior: the length-39 `ROOT` and length-20 `BULK` coefficient arrays included in `w01_screened_corridor.cpp`. With half-length `H=12,000`, take the palindromic 24,000-entry *pair coefficient* word formed by the root and repeated bulk. The physical decimal digit at each lower index is `min(q,9)`, and the opposite digit `q-min(q,9)`; the leading decimal digit is nonzero. Independently replace pair coefficients in any subset of three disjoint 50-cell pulses:

- `X`: positions `6000..6049`, replacement `(7j+11)%19`;
- `Y`: positions `8000..8049`, replacement `(3(j-8000)+10)%19`;
- `Z`: positions `10000..10049`, replacement `(5(j-10000)+3)%19`.

The eight masks `000..111` yield eight distinct 24,000-digit decimal integers. Evolve each by the **literal** base-10 operation `n <- n + reverse(n)`. All eight lengths agree at every checked step; every actual state `t=0..20,000` has an odd paired coefficient in its first 39 positions, so none is a palindrome. All outputs and claims here refer to the **actual individual decimal digits**, not only to abstract pairword dynamics.

At any step, digit side (`low` or `high`), and mirrored-pair index `j`, define the signed two-body YZ interaction without X:

    U_YZ = d_110 - d_100 - d_010 + d_000,

and with X present:

    U_YZ|X = d_111 - d_101 - d_011 + d_001.

The three-body Möbius residual is `R3=U_YZ|X - U_YZ`. The equality is a **PAPER PROOF** of inclusion-exclusion for *any* values of the eight digits. Define `f3(t)` as the first `j` where the **sum of the low and high** values of `R3` is nonzero. Define `s(t)` as the first `j` where **either low or high** of `U_YZ|X` is nonzero. In particular, `s` uses the stricter *physical* digit test and is not allowed to hide cancellation between the two ends.

## Exact positive finite event

The first genuine three-body interaction occurs at **t=4354, j=9014** (two adjacent nonzero pair indices). After a transient, for **every integer** `5098<=t<=20000`:

    s(t) - f3(t) >= 41

Therefore **both individual low/high physical digits of `U_YZ|X` vanish** at every paired position `f3(t)+r` for **all 61 offsets -20<=r<=40**. Equivalently `R3(t,f3+r) = -U_YZ(t,f3+r)` on both ends. This is a complete two-ended, 61-cell outgoing YZ-packet **screen**, not just a paired-digit-sum coincidence. Exactly **14,903 complete 61-cell time rows** satisfy this screened identity with no exceptions; the last failing 61-cell tile is at **t=5097**, where `s-f3=40`. At t=5098, the first unshielded physical index is at `f3+41`; by t=20,000 it lies at `f3+1011` (`f3=5459`, `s=6470`). Individual gap values fluctuate, so no per-step monotonicity is asserted. However, the minima over each successive consecutive 176-step time block starting at t5098 are **strictly increasing** across all 85 tested blocks, with smallest block-to-block increase 4 and minima from 41 to 1004. This is a measured expanding leading **screened corridor** behind a moving outgoing three-body defect.

The three-body leading front also obeys **`f3(t+88)=f3(t)-20` for every integer `4370<=t<=19912`** (15,543 exact front equalities). Its actual signed low/high 61-cell tile (`r=-20..40`) obeys the identical 88-step moving-window law for **every `5098<=t<=19912`** (14,815 rows, **1,807,430** exact signed-digit equalities). The only early front-law failures with comparison starts `t=4354..4369` are **t=4365,4368,4369**. Thus the screening pattern is embedded in a robust sheared outgoing glider, not a stationary region.

There is also a second positive correspondence with the originally isolated X–Y daughter from the two-body W01 result. For **every 4370<=t<=20000**, `f3(t)=f_XY(t)+2000`. For **every 5098<=t<=20000**, at all `r=-20..35`, its **two signed actual digit tracks** are precisely the *negative* of the X–Y daughter tracks at their respective fronts (`14,903 * 56 * 2 = 1,669,136` equalities). In each of those 14,903 rows the additional 5-cell tail `r=36..40` has at least one nonzero discrepancy (89,415 actual digit discrepancies in total). Hence the third-order daughter is an **antipodal spatially translated copy with a tightly localized five-cell seam**, not a trivial globally identical residual.

## Reproduction and independent arithmetic

From repository root:

    bash calculation/new_structures/agent-W01/triple_run.sh

This compiles and runs the self-contained `w01_screened_corridor.cpp` to step20k, regenerates the X–Y baseline from the previously committed independent source `w01_scatter_phase.cpp`, and runs `triple_verify.py` across both full generated traces. A compact 12-row fixture `triple_expected.csv` checks exact first events and later keyframes; the full 20,000-step traces are **regenerated**, not bundled. Python independently checks every front, every signed low/high 88-step tile, every full two-ended YZ screening interval, the anti-copy plus five-cell seam, and 85 block minima; off-by-one spatial shift and early transient controls are rejected.

Finally, `w01_triple_gmp.cpp` reconstructs **all eight original integers independently** using decimal string assembly and `mpz_class`, then computes each 6,000-step literal integer orbit with `n += mpz_class(reverse(n))`. It independently checks first three-body onset, last failed shield tile, all **903** complete physical YZ cancellation tiles `t5098..6000` (110,166 equalities), and the 56-cell antipodal X–Y relation over those same 903 rows (101,136 equalities). It does **not** use the C++ digit-array step, the Python checker or the generated CSV. Required dependencies: C++17, GMP development libraries and Python3. Compact report inputs, no downloads or hidden data.

## Limit of the claim and next certificate problem

This is a constructive **three-body macro-scattering shield** for the p8/m20 decimal lattice. It supplies a candidate *emission/eraser interface* with a sharply bounded, identifiable five-cell seam and a moving protected corridor. It does **not** supply a finite inductive gate contract proving the 88-step dynamics persist indefinitely, a junction that produces another initial X/Y/Z packet, an arbitrary-packet-spacing theorem, a return-map fixed point, an infinite palindrome-free orbit, or anything specific about starting number 196. Those remain **UNDECIDED**. A promising next proof target is a finite carry-gate transducer for the five-cell seam, treating the growing shield as a pumpable distance between two glider ports; a closed gate cycle would convert the present finite mechanism into the desired certificate.
