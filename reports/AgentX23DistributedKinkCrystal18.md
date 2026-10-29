# Agent-X23: a distributed decimal period-3 kink crystal inside the period-8 exterior

**Status: COMPUTED (20,000 actual decimal steps, no infinity claim).**

## Construction

Digits and coefficient words are least significant first. Let the 39-cell B and 20-cell W be the literal constants in `crystal18.cpp` (taken from the earlier validated period-eight exterior, not claimed as new). Let R=(8,6,8), q=400, r=5000. Define the symmetric pair-coefficient word

`P = B ++ W^q ++ R^r ++ reverse(R^r) ++ reverse(W^q) ++ reverse(B)`.

It has 46,078 coefficients. To obtain an explicit positive integer N0, for each 0<=i<|P|/2 put its i-th **most significant** decimal digit equal to min(9,P_i), and its (|P|-1-i)-th most significant digit equal to P_i-min(9,P_i). This digit split has no leading zero and produces pairword P. The source implements this definition exactly, so no long seed literal is needed.

## Reproduction and independent arithmetic

`cd calculation/new_structures/agent-X23`
`g++ -O3 -std=c++17 crystal18.cpp -lgmpxx -lgmp -o crystal18`
`./crystal18 400 5000 20000`

Two independent evolution methods run for all t=0,...,20,000: direct coefficient normalization followed by pair formation, and arbitrary-precision GMP integer reversal plus addition using actual decimal strings. All coefficients of both full words are compared at **every** step, and GMP's decimal string is tested against its own reversal at every step. Every comparison passes; there are no palindromes, and gamma_t=1 for even t and 0 for odd t. The literal B clock of period 8 and spatial-W 20-cell prefix are checked on each word. Separate three-cell cyclic-carry computation predicts the central R region.

Selected measurements (full 1,000-step checkpoint table: `crystal18_checkpoints.csv`):

| t | digits | W matching prefix | R matching centre suffix |
|---:|---:|---:|---:|
| 0 | 46078 | 8000 | 15000 |
| 10000 | 51078 | 5729 | 11743 |
| 20000 | 56078 | 3457 | 8551 |

These W/R lengths are contiguous *verified* runs, not guesses about the unseen portion. Minimum over all t: 3457 and 8551 respectively. At t=20000, the gap between those verified runs is 15,992 coefficients (initially 0): the interface **expands**, and does not return to a bounded shape. This rules out calling the present finite simulation a cycle certificate.

## Exact bulk map and general finite-propagation fact

For any nonneutral m-periodic coefficient word r (some r_i !=9), compute unique cyclic incoming carries c_i^+ along increasing indices and c_i^- along decreasing indices, with c_{i+1}^+ = floor((r_i+c_i^+)/10) and c_{i-1}^- = floor((r_i+c_i^-)/10). Write d_i^+=(r_i+c_i^+) mod 10 and d_i^-=(r_i+c_i^-) mod 10. For an overflow g in {0,1}, the bulk successor is

`F_g(r)_i = d_i^+ + d_{(i-g) mod m}^-`.

**Finite-propagation argument (paper derivation, not Lean):** a coefficient <=8 forces its output carry to zero, and one >=10 forces it to one; only coefficient 9 transmits an incoming carry unchanged. Therefore, in any repeated nonneutral period-m word, a left-to-right or right-to-left carry forgets the outside boundary within at most m cells. The pairing index shifts by at most one under overflow. Hence an interior site at distance >m+1 from both ends of a periodic run has exactly F_g(r) as its successor coefficient. Induction yields conservative shrinking protected intervals for arbitrarily many finite steps; it does not produce an infinite orbit without a stable interface invariant.

For R=(8,6,8) and the alternating g=1010..., the cyclic ring has an 11-step transient, then **minimal temporal period 18** (9 overflow ones per 18 steps); `cycle18.csv` tabulates the full cycle. The outer B/W clock has period 8, so the clocks re-align every lcm(18,8)=72 steps, with 36 total overflows. This is a concrete distributed-kink clock compatibility not requiring a single bounded centre; the unbounded **inter-species interface** remains the obstruction.

## What is not proved

No base-10 Lychrel number, no all-length root certificate, no all-q/all-r survival theorem, and no bounded interface cycle is claimed. A sound next search target is a 72-step translating or self-replicating *interface tile* between W20 and R3, with direct finite-edge checks and a nonpalindromic root witness; the measured positive interface expansion must be arrested or replaced by a regenerative rule.
