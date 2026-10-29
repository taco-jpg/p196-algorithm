# Agent N23: independent 20,000-step decimal protected-pairband candidates

**COMPUTED**, finite-length replay of explicitly supplied decimal seeds; no Lean, no infinite certificate, no result on the number 196.

## Candidate and predicted shape

For Q in {7000,7001,8000}, seed N_0(Q) is the genuine base-10 integer whose most-significant-first decimal digit string is

    12 ++ "99" repeated Q times ++ 34.

Initially the full least-significant-first *pair-coefficient* word P_i=d_i+d_(n-1-i) is [5,5] ++ [18]^(2Q) ++ [5,5]. The claim at EVERY step t=0,1,...,20000 is that the real base-10 number is not a palindrome and P_t has a symmetric central run [18]^L with L>=1970,1972,3970 respectively. The exteriors A_t are not asserted to be periodic or bounded width; the accurate family template is P_t=A_t ++ [18]^L_t ++ reverse(A_t). No infinite orbit or template cycle is asserted. In decimal digits, a central coefficient 18 means BOTH paired digits equal 9, making the shape independently checkable without claiming that the exact A_t repeats.

## Independent algorithms and computed outcomes

Program protected_20k.cpp represents a potentially unbounded integer as base-10 digit bytes, computes reverse-and-add by digit carries, checks a full-digit palindrome comparison and inspects the entire central pair band each step. Its independently written second oracle protected_bigint.cpp represents the number in base 1,000,000,000 limbs, renders and reverses an ordinary decimal string, parses the reversal into limbs and adds using 64-bit carry arithmetic. The independent oracle also tests the full string for being a palindrome and measures the central all-9 run. Neither imports any template generator, external bigint library, or the other oracle. The complete final integer is hashed MSD-first with the deterministic recurrence H=(131 H + decimal-digit ASCII) mod 1000000007. Same final checksum and length in both algorithms is a strong cross-engine comparison; no hash is presented as a mathematical proof of integer equality (both code paths are supplied for inspection).

| Q | steps | initial digits | final digits | initial central 18 | final/min central 18 | final checksum |
|---|---:|---:|---:|---:|---:|---:|
| 7000 | 20000 | 14004 | 22266 | 14000 | 1970 | 914048026 |
| 7001 | 20000 | 14006 | 22268 | 14002 | 1972 | 480308761 |
| 8000 | 20000 | 16004 | 24266 | 16000 | 3970 | 721346226 |

The Q=7000 engine additionally observed sum of central run lengths over t=0..20000 = 159,850,050. These runs shrink dramatically but do not disappear in the tested window; no asymptotic statement is justified.

## Reproduction, contribution, next mechanism

Run from a clean checkout:

    bash calculation/new_structures/agent-N23/reproduce_20k.sh

It compiles both self-contained C++17 implementations, executes six independent full 20,000-step runs, compares exact final-length/checksum metadata and asserts saved small-data witnesses in seed20k.tsv. The earlier N23 result proves a 174-step algebraic corridor for a shorter version of the same decimal family for all padding parameters; this is a separate substantially longer numerical probe, not an extrapolated theorem. The next constructive task is to turn the observed central protected region into a finite speed bound with verified two-sided carry states and, crucially, an absorbing or replenishing mechanism when its two boundaries eventually meet. Full tools/verify.py --changed was unavailable without a GitHub shell checkout, and no Lean source is added.
