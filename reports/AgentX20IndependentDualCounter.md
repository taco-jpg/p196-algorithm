# Agent X20: independent 20/48 counters and the 272-step resonance

**Status:** PAPER PROOF for the finite-state lifting lemma and the Diophantine length identity; COMPUTED for the 480 exact edge checks, literal-digit controls, and two 20,000-step independent-integer experiments. Not Lean-verified. No base-10 Lychrel number is claimed.

## New scope relative to existing work

N01's published 480-step result only asserted synchronized counts `m=n=k`. Here **m and n are separately arbitrary integers >=40**. This strict two-parameter strengthening is not inferred from sampled asymmetric lengths: a complete four-corner finite-state test is performed for each of the 480 edges, along with the two independent band-matrix idempotence assertions. In contrast with N20's general affine-sheet soundness language, the new computed instance retains the nontrivial interacting decimal period-20 and period-48 bulks and has an exact, specialized 80-state two-ended arithmetic checker.

The initial palindromic *coefficient* word is `P0(m,n)=H++[9]++reverse(H)` (least significant coefficient first) with `H=B++W^m++[9]++V^n`. The literal arrays `B` of length 39, `W` of length 20 and `V` of length 48 are in `two_counter.cpp`, transcribed from the independently published N01 witness. Here coefficients may exceed 9: the genuine initial integer is `val_10(P0)` after carrying. **The coefficient word itself is not asserted to be an ordinary base-10 digit string.**

For each phase `t=0..480`, the entire lower folded pairword factorization is

`A_t ++ W_t^(m-40) ++ J_t ++ V_t^(n-40) ++ C_t`, plus the even/odd central coefficient and reflection.

The exact zero-based halfword cut indices are

`0, 199, 20m-601, 20m+616, 20m+48n-1304, floor(|P_t(m,n)|/2)`.

Thus `|A_t|=199`, `|J_t|=1217`, and both repeated blocks have distinct, independently variable exponents. Their updating periods are 20 and 48, and their bulk values are uniquely obtained from the constant cyclic carry on each band and the actual overflow `gamma_t`.

## Universal two-counter finite-state lemma (PAPER PROOF)

For one edge let `M_A, M_W, M_J, M_V, M_C` be the 80x80 Boolean relation matrices of the exact two-ended base-10 carrying machine, with the centred acceptor enforcing output geometry and nonpalindromicity. For arbitrary integers `r=m-40` and `s=n-40` the complete relation is

`M_A M_W^r M_J M_V^s M_C`.

At every one of the 480 edges the code computes `M_W^2=M_W` and `M_V^2=M_V`. Therefore each exponent can be replaced by `min(exponent,1)` **independently**. All four `(r,s) in {(0,0),(1,0),(0,1),(1,1)}` accepted: no diagonal-only conclusion is used. The endpoint conditions are the exact integer-carry constraints, so relation acceptance is equivalent to correctness of the proposed next pairword for an actual reverse-add transition. The mismatch bit certifies an unequal opposing digit pair, hence a nonpalindrome; the ordinary digit-array controls also verify leading digit and the full overflow schedule.

Induct on the 480 certified edges, starting from `N0=val_10(P0)`. Each step preserves the indicated two-parameter template for all m,n>=40. This is a **finite 480-step theorem**, not an infinite certificate: the literals `J_t,C_t` do not return.

The checker computes each one-symbol transition by taking incoming low carry `a`, outgoing high carry `h`, previous high digit `z`, and mismatch flag `e`. A candidate inward high carry `r` is legal iff `floor((x+r)/10)=h`; then low/high digit remainders and the `gamma`-dependent upper partner determine the proposed next pair coefficient. Centre terminal conditions enforce the low/high carry meeting. This is the same actual decimal arithmetic as the N01 80-state transducer but recomputed in X20's standalone source; the four-corner lift is new.

## Diophantine macroperiod target (PAPER PROOF and COMPUTED diagnostic)

The actual overflow schedule is `1,0,1,0,...`, four overflows every eight coefficient steps. Any macrocycle of 8r transitions has `4r` additional *full-word* coefficients. To return to fixed literal exterior/junction/centre while inserting `a` extra copies of the 20-word and `b` extra copies of the 48-word in **each** of the two mirrored halves, the growth is exactly `2(20a+48b)=40a+96b`. Thus necessarily

`4r = 40a+96b`, i.e. `r=10a+24b`.

Smallest `r` with both a,b>=1 is 34, attained uniquely by a=b=1; the first possible simultaneous positive return is therefore `8*34=272` steps. This equation alone is only a *necessary* counting constraint; it does not imply an arithmetic transition or a closed template cycle.

At t=8,88,272,480, the actual `(A,W,V)` phase-0 bulk words all return, consistent with the 8-clock. At t=272 the suffix centre has length 1412 versus 1344 initially, exactly +68 lower-half coefficients, matching the proposed insertion of one 20-copy and one 48-copy. Despite that ideal count, the actual full pairword at t=272 differs from `P0(41,41)` in **3,993** of 5,657 coefficient locations (longest identical low-first prefix 778, last mismatch index 4878). The fixed 1217-coefficient bridge differs at 215 locations. At t=480 it differs in 391 locations; the centre has grown from 1344 to 1464. The obstruction is thus an *unrepaired bridge/centre*, not an incompatible growth rate.

**Constructive redirection:** search for a finite-state regenerating bridge whose 272-step update has exactly the required +20/+48 symmetric insertion, possibly using a moving junction interface or an extra independent centre counter. The Diophantine equality gives a discrete lattice of all candidate insertion vectors, not an exhaustive rejection of centres.

## Reproducible computation and exact bounds

From the repository root (all sources are C++17 standard library except Python 3 for the optional independent short check):

```sh
g++ -O3 -std=c++17 calculation/new_structures/agent-X20/two_counter.cpp -o /tmp/x20
/tmp/x20 480
g++ -O3 -std=c++17 calculation/new_structures/agent-X20/resonance.cpp -o /tmp/x20_res
/tmp/x20_res
python3 calculation/new_structures/agent-X20/spotcheck.py
g++ -O3 -std=c++17 calculation/new_structures/agent-X20/asymmetric20k.cpp -o /tmp/x20_big
/tmp/x20_big 427 509 20000
/tmp/x20_big 509 427 20000
```

The 480-edge runner checks five distinct `(m,n)=(40,40),(41,40),(40,41),(41,41),(52,67)` coefficient *and* direct decimal-digit trajectories at **all 481 states**, separately verifies each band-matrix idempotence and the four corner relations on every edge, and prints suffix length 1464 and 391 bridge changes. The Python `int` checker independently reconstructs the initial integer and adds its ordinary decimal reversal for 128 operations on four asymmetric seeds, with no transducer calls.

For the two long checks, an independent **base-10^9 arbitrary-precision limb engine** reverses canonical decimal digits and adds with *nine-digit carries*, while the first engine independently performs digit-by-digit decimal addition; each state is compared as a full integer and verified nonpalindromic. The coefficient engine also checks exact carrying back to the ordinary digit word, the alternating clock and fixed disjoint **50 copies of W plus 20 copies of V** on each of the 20,001 states. The final least-significant-first decimal FNV-1a 64-bit hashes:

| (m,n) | t | final digits | hash |
|---|---:|---:|---|
| (427,509) | 20,000 | 76,026 | `fd9b296c175cbcce` |
| (509,427) | 20,000 | 71,434 | `29d9fb65743a3d46` |

The long replays do **not** establish a closed template after 480 steps, nor an infinite invariant; only two fixed windows, and not the full two-band factorization, are asserted beyond the finite 480-step theorem. This distinction is essential. No result about 196, uniqueness or completeness of such templates, or Lean verification is claimed. Repository-wide `tools/verify.py --changed` was not runnable because a full local checkout could not be fetched; the standalone files were compiled, run, and independently cross-checked as stated.
