# Agent X10: Four-sheet two-parameter decimal arithmetic, 20,000-step universal chamber

**Status: COMPUTED** (finite exact symbolic enumeration and independent full-integer replay), not a base-10 Lychrel proof. This report supplies a mathematical soundness argument for the format; no Lean formalization is claimed.

## Construction and arithmetic model

For independent positive integers `q,r`, define

`N_0(q,r) = 88*10^(3q+r) + 37*10^q + 75`.

This is a genuinely two-gap family: the interior distance `q` and mirror-interior distance `q+r` can vary independently. Represent a decimal integer as a sum of four *digit sheets* `P_k`: for `v_0=(0,0)`, `v_1=(1,0)`, `v_2=(2,1)`, `v_3=(3,1)`, each packet consists of digits `d_{k,c} in {0,...,9}` at exponents `v_k.(q,r)+c`, where `c` is an integer offset bounded separately from the parameters. Leading and trailing zero offsets are trimmed. The packet supports are disjoint whenever q and r satisfy the computed gap guard. Initially the four packet offsets are `P0=[5,7]`, `P1=[7,3]`, `P2=[]`, `P3=[8,8]`, in least-significant-first order.

Let the leading nonzero exponent be `E_t=3q+r+h_t`, where `h_t` is the highest offset of `P3`. Reversal sends an offset `c` in sheet `k` to offset `h_t-c` in sheet `3-k`. This works because `v_k+v_(3-k)=(3,1)` for all four k. Raw next coefficients in sheet k are thus:

`R_(k,c)=d_(k,c) + d_(3-k,h_t-c)`.

Normalize each finite raw packet independently by ordinary schoolbook carries to the next offset. Keep the resulting four packets. The crucial fact is that *the slope set never grows*: reflection permutes the four slopes, and addition/carries change only integer offsets. This also covers leading overflow, since a local top carry extends P3 by one offset. The bottom digit of the number may be zero, without affecting the reversal formula.

## Finite and exactly checkable soundness condition

At each time t, define `lo_k,hi_k` as the first/last nonzero offsets of packet k (ignore empty packets). Require (1) each sheet's absolute exponents are nonnegative, (2) all occupied sheets are in ascending slope order with strictly separated absolute ranges, and (3) P3 is nonempty and highest. For adjacent sheets, sufficient guards are

`q + lo_1 - hi_0 >= 1`,

`q+r + lo_2 - hi_1 >= 1`,

`q + lo_3 - hi_2 >= 1`,

when the involved sheets are nonempty. More distant sheet pairs then follow transitively. Other sufficient guards are `q+lo_1>=0`, `2q+r+lo_2>=0`, `3q+r+lo_3>=0`, and `lo_0>=0`. Define G_t as the least positive integer ensuring every one of these inequalities for **all** q,r>=G_t. A corrected implementation must check each inequality at both parameter lower endpoints, or equivalently use the coefficients shown above; no random sampling or floating-point rounding is permitted.

Assume the state at time t represents the true digits and has those guards. Reversal is `sum d_i*10^(E_t-i)` exactly. Thus its raw decimal coefficient multiset is precisely the four `R_(k,c)` above. Within each packet, normalization uses the real base-10 carry rule. If the resulting packets satisfy the separation guards, no carry can interact across packets: independent normalization gives the actual integer `N_t+rev(N_t)` in all positions. This proves the one-step soundness lemma by elementary base-10 positional arithmetic. Induction yields all sheets at all checked times for every q,r above the maximum reported G. A palindrome check is purely a comparison of the four sheets against their mirrored counterparts (each k versus 3-k, with offset reversal about h_t). If any digit differs, it cannot be a palindrome for any admissible q,r, regardless of their magnitudes.

**Conditional infinite-cycle format:** any finite cycle of such packet states (with possible affine parameter update `(q,r)->A(q,r)+d`) proves an infinite orbit if each edge satisfies the exact local carry recurrence and separation inequalities for a polyhedral region P; each state has a nonpalindromic mirror mismatch; `A P+d` is contained in P; and the terminal packet state equals the initial packet state with the updated parameter. This is proved by induction on repeated cycles. No such cycle was found here. The format is broader than a one-variable repeated geometric-word identity because it includes independently drifting nonparallel exponent slopes and explicit polyhedral separation guards.

## Results, controls, and scope

The optimized C++ packet engine separately normalizes 20,000 genuine base-10 carry rounds and reports the running **maximum** threshold G=11,984 over all t=0..20,000. All four slope classes persist and all 20,001 state templates are nonpalindromic by literal digit comparison. At t=20,000, P0/P1/P2/P3 stored offset spans are respectively 10,122 / 12,003 / 12,002 / 10,121 positions (zero entries included), with `h_t=8255`. The 20,000-step sweep took about 1.72s on one test environment (not a reproducibility guarantee).

For explicit q=r=11,985, the independent `decimal_replay.cpp` computes `N+reverse(N)` as two complete decimal digit arrays using one schoolbook carry across the **entire** 47,942-to-56,196-digit integer. It constructs the predicted full decimal numeral from sheet locations and compares every character at each time. There were exactly 20,001/20,001 full-word matches, no palindrome in those 20,001 states, and no gap guard failure (5.75s in the same environment). This is not a modular hash check or a comparison of only a frontier. An additional Python implementation makes real arbitrary-precision integer updates with `int(str(N)[::-1])` and checks all 265 symbols at three small q,r controls; the max G for those slices is only 162.

For q=r=200, the chamber threshold first exceeds 200 at t=329, and the independent integer path first disagrees with the four-sheet no-cross-gap template at exactly t=329. The integer path remains nonpalindromic for t=0..1,000, but that statement alone is only a finite observation. This countercontrol demonstrates why finite q,r do not imply infinite four-sheet preservation.

Reproduce from the repository root via `bash calculation/new_structures/agent-X10/reproduce.sh`. Outputs under that directory are compact checkpoints, not whole-number data dumps. `four_sheet.py` is written independently of `four_sheet_fast.cpp` and provides another transition realization for 264 steps. `decimal_replay.cpp` uses ordinary full-decimal digit arithmetic, not the four-sheet arithmetic, to advance the actual integer.

**What is not proved:** Nothing shows that any fixed q,r can keep its gap guards satisfied forever; G_t grows roughly linearly in the tested range. This is no decimal Lychrel certificate and says nothing about 196. The next constructive target is a resetting or replenishing packet rule that makes the boundary offsets recur while maintaining nonnegative q,r parameter drift.

## Strengthening: exact polyhedral two-gap region, negative r allowed

The original reproducibility run restricted both q and r to be at least 11,984; this is a sufficient but unnecessarily strong orthant. A *separate C++ boundary checker* computes the exact maximum guard terms from all 20,001 four-packet states, without evaluating huge decimal numbers:

- `q >= Q = 11984` from exterior-to-near-centre and far-centre-to-exterior separations, and nonnegative P1 exponents;
- `q+r >= D = 12024` from central two-sheet separation;
- `2q+r = q+(q+r) >= U = 1884` for nonnegative P2 exponents;
- `3q+r = 2q+(q+r) >= V = 1865` for nonnegative P3 exponents.

With `q>=11984` and `q+r>=12024`, the latter two conditions hold automatically. Since every guard is linear in q and r, this proves that the **whole closed lattice polyhedral wedge**, including negative values of r, satisfies the same 20,000-step symbolic trace. It is not an extrapolation from a finite grid of integer parameter samples. `poly_guard.cpp` records the monotone maxima and their exact values, and `decimal_replay.cpp` now checks these actual per-instance guards rather than incorrectly imposing an independent lower bound on r.

Three independent full-word 20,000-step controls now pass with zero palindrome and 20,001/20,001 exact digit-template matches:

- boundary `q=11984,r=40`: seed length 35,994, final length 44,248;
- interior `q=11985,r=11985`: seed length 47,942, final length 56,196;
- skewed negative-r `q=20000,r=-7976`: seed length 52,026, final length 60,280.

This is a **strictly stronger finite result** than the first uniform statement. The 35,994-digit seed is the smallest seed by length *within this proven wedge*, not claimed smallest among all decimal seeds surviving 20,000 iterations. Every case is still finite-horizon and no infinite recurrence is proved.
