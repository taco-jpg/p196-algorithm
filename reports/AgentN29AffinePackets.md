# Agent N29: a 20,000-step decimal moving-zero-gap family

**COMPUTED** for the finite orbit and every checked word; **PAPER PROOF** for the following algebraic identity and its uniform-in-gap consequence. No claim of an infinite base-10 Lychrel number.

## New constructive mechanism
Let `q` be a free natural parameter and set `N_0(q)=88 0^q 75` as a decimal word. Write `N_t(q)=A_t 10^(q+s_t)+B_t` with `(A_0,B_0,s_0)=(8800,75,0)`. For a positive integer `a`, let `len(a)` be its decimal digit count and `rev(a)` be its decimal reversal (leading zeros dropped).

If `E=q+s_t >= len(B_t)`, then the actual word is `digits(A_t) ++ 0^(E-len(B_t)) ++ digits(B_t)`. Reversing its **entire** decimal word gives the exact identity

`rev(N_t)=rev(B_t)*10^(E+len(A_t)-len(B_t)) + rev(A_t).`

This holds even if either packet ends in zeros. Therefore with `d=len(A_t)-len(B_t)`:

* `B_(t+1)=B_t+rev(A_t)`.
* For `d>=0`: `A_(t+1)=A_t+10^d rev(B_t)`, `s_(t+1)=s_t`.
* For `d<0`: `A_(t+1)=10^(-d) A_t+rev(B_t)`, `s_(t+1)=s_t+d`.

For `q` large enough to keep the packet gap nonnegative, this is an **exact** digit-free polynomial-in-`10^q` description of the real reverse-add orbit. Nothing about a short or periodic central block is assumed.

## Sound finite-time lemma
Fix an integer `T` and calculate the above state recurrence for `0<=t<=T`. If `q >= Q_sep=max_t(len(B_t)-s_t)`, then the identities for every step `0..T-1` follow by induction, provided each next state is also separated; in particular one can include state `T` in the maximum to cover the final addition.

If `g>=max(len(A),len(B))`, the predicate `digits(A) ++ 0^g ++ digits(B)` *is a palindrome* is independent of `g`: the two packet comparisons at the opposite ends do not interact across the central zeros. Consequently define

`Q_uni=max_(0<=t<=T) (len(B_t)+max(len(A_t),len(B_t))-s_t).`

If every canonical word `digits(A_t) ++ 0^max(len(A_t),len(B_t)) ++ digits(B_t)` is nonpalindromic, **all** initial integers `N_0(q)` with `q>=Q_uni` avoid a palindrome at each state `0..T`. This finite-time lemma is a general two-packet format with moving shift and unfixed end widths. It does not imply a single fixed `q` survives forever.

## Reproducible decimal instance
`T=20000`, `Q_sep=11985` (over states 0..20000), and `Q_uni=22107`. All 20,001 canonical-word palindrome tests passed. For the *smaller, explicit* `q=14000`, the separate Python calculation checked all 20,001 actual words directly, with minimum zero gap 2,015. A C++ program starts from the literal integer `88 0^14000 75`, then performs 20,000 actual full-integer GMP reverse-and-add steps. At each of the 20,001 states it checks full decimal-string equality to the independently updated two-packet prediction and checks nonpalindromicity. 22 full-number SHA-256 snapshots (t=0,1000,...,20000 and t=19999) match bit-for-bit; final iterate is 22,258 digits. This is stronger than checking a pairword projection alone.

From the repository root: `python3 calculation/new_structures/agent-N29/run_all.py`. Dependencies: Python >=3.11, g++ with libgmpxx/libgmp, OpenSSL libcrypto. The runner writes only to a temporary directory and tests the forced-palindrome negative control `1 0^20 1` (must be rejected). Data `checkpoints.txt` is the full compact list of snapshots. No local untracked replay files are needed.

## What breaks / next constructive search
The separation requirement rises to 11,985 by step 20,000; the endpoint packets themselves grow to 10,121 digits each and the shift reaches -1,863. Thus the currently verified invariant consumes a finite zero reservoir. A single finite initial gap has **not** been shown to persist for all time. To turn this into an infinite decimal certificate, the next idea is to couple the two endpoint packet laws to an absorbing periodic interior that replenishes the buffer, or to replace `q+s_t` by a renormalized geometric-series band with positive gain per macrocycle. This is a constructive direction, **not** a no-go or a census of dead families.
