# N23: an exact two-ended decimal 9-band transducer and uniform 20k-step family

**COMPUTED** path, with a **PAPER PROOF** of its sound local digit rule; neither a Lean theorem nor an infinite decimal Lychrel certificate. This is a new constructive parametric finite-horizon mechanism, not a census/exclusion.

## The exact two-sided carry rule

Represent decimal digit words least-significant first. Let N(U,V,L)=U ++ 9^L ++ V, where |U|=|V|=a, L>=2, every entry is a decimal digit and V's final high digit is nonzero. Reverse-and-add N+reverse_10(N) is performed by the ordinary base-10 carry recurrence. Its lower exterior consists of normalized sums of U_i+V_(a-1-i) with initial carry 0, resulting in a digit block lo and an outgoing carry c in {0,1}. The first interior pair 9+9 yields digit z=8+c and ALWAYS outgoing carry 1. Every subsequent 9+9 interior pair yields digit 9 with outgoing carry 1. The upper exterior normalized with incoming carry 1 produces block hi and final overflow gamma in {0,1}. The EXACT successor word is

    lo ++ [8+c] ++ 9^(L-1) ++ hi ++ ([1] if gamma=1 else []).

To restore symmetric central 9-band form, set U'=lo++[8+c]. If gamma=0, set V'=[9]++hi, preliminary L'=L-2. If gamma=1, set V'=hi++[1], preliminary L'=L-1. The resulting full digit word equals N+reverse(N), and |U'|=|V'|=a+1. Now repeatedly trim a 9 from the END of U' and the BEGINNING of V', adding 2 to L' per paired trim. This is a digit-for-digit identity; it neither changes the integer nor depends on the initial L, provided the interior has L>=2 throughout. The number is a decimal palindrome iff U'=reverse(V') because the interior is all 9s.

## Finite-horizon pumping statement

Start from N0(Q)=12 (99)^Q 34, represented LSD-first by U0=[4,3], V0=[2,1], L0(Q)=2Q. The formulas just proved evolve U_t,V_t,c_t,gamma_t and the number of trims independent of Q. Thus, for a tested baseline Q0, if L_t(Q0)>=2 and U_t!=reverse(V_t) for EVERY t=0..T, the same is rigorously true for ALL Q>=Q0, with L_t(Q)=L_t(Q0)+2(Q-Q0). This is a finite-horizon *parametric pumping certificate*, not a periodic cycle or an inference from a handful of sampled lengths.

For T=20,000, the exact C++17 integer-carry state computation with baseline Q0=6016 confirms L_t>=2 for all 20,001 time slices, with minimum/final L=2, and checks nonpalindromicity of the exterior at every step. Over the path: gamma=0 occurs 11,738 times, gamma=1 occurs 8,262 times, symmetric wall trimming occurs 9,854 times. The final exterior widths equal 10,148 each; final decimal digits = 20,298; the final full-number rolling checksum mod 1,000,000,007 is 788,241,103. Every base-10 pair coefficient in the central mirrored 9-run is 18.

## Independent arithmetic and threshold scope

The two previously committed independent programs protected_20k.cpp (decimal digit vector) and protected_bigint.cpp (base-10^9 arbitrary-precision limbs plus whole decimal-string reverse) reproduce a full genuine 20,000-step run at Q=6016 after lowering their configurable *test-only* central-band threshold from 1000 to 2. Both confirm all 20,001 nonpalindromic states, final length 20,298, min centre 2, and identical final full-number checksum 788,241,103. At Q=7000,7001,8000, the unmodified versions additionally confirm larger protected bands and checksums independently. A new Python ordinary-integer checker runs 10,000 randomized two-wall transitions, including both parity/overflow cases, against the exact transfer formula.

The result claims **all Q>=6016 for exactly 20,000 steps**. Q=6016 is the smallest baseline certified by THIS particular L>=2 run at this horizon; at Q=6015 the same abstraction reaches L=1 before 20,000, which does NOT establish a palindrome or exclude a different format. No asymptotic nonpalindromicity or never-palindrome number is asserted.

## Reproduce

    bash calculation/new_structures/agent-N23/reproduce_parametric.sh

This invokes the previously shipped independent two-engine 20k controls, the new 10k random edge tests, computes the parametric path for Q=6016/7000/7001/8000, checks tabulated hashes and replays the Q=6016 boundary with two independent arithmetic engines. Source, exact commands, and compact TSV data are under calculation/new_structures/agent-N23/. Full tools/verify.py --changed was not available without an HTTPS GitHub shell checkout, and no Lean files were added.
