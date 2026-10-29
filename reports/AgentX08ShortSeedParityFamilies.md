# Agent X08: short-seed paired-parity witnesses (COMPUTED)

## Construction
For an integer N with n base-ten digits d_i indexed from the right, define the symmetric pairword P_i=d_i+d_(n-1-i), for 0<=i<floor(n/2). A palindrome has every P_i even; therefore an odd coefficient anywhere is a rigorous non-palindrome witness for that finite state.

Family A consists of four-digit words a b c d with a in 1..8, b in 4..9, c=13-b, d=8-a. Its full coefficient word is [8,13,13,8] (low first), and the ordinary integer sum N+reverse(N) is identically 9438. All 48 words are non-palindromic initially (odd coefficient at i=1).

Family B consists of five-digit words a b 9 d e, a in 1..9, b in 6..9, d=15-b, e=10-a. Its full coefficient word is [10,15,18,15,10], and N+reverse(N) is identically 116960. All 36 are initially non-palindromic (odd coefficient at i=1). Digitwise reversal padded with a leading zero gives the same numerical reverse for Family A members ending in zero. The one-step coalescence argument is exact arithmetic, so checking the two representatives checks all 84 seeds from t=1 onward.

## Concrete finite-window witness
For N_t, let k_t be the least i such that P_i is odd. The C++ positional engine checks every state t=0..100000 without missing k_t, obtaining max k_t = 22 for seed 1497 and 24 for 16999, and final lengths 41387 / 41255. Through t=20000 its maxima are 17 / 16. These are finite measured bounds, not invariants certified beyond the measured interval.

Two independently implemented complete decimal orbits (C++ little-endian schoolbook digits; Python arbitrary-precision integer and decimal-string reversal) agree at EVERY t=0..20000, checked by SHA-256 over each entire numeral followed by newline, not merely by samples. The expected SHA-256 are:
- 1497: 8ab0894c7daf435e5e5af2c4b1bbf2b5e62f4aea3558ff9fefba38753a49d325.
- 16999: 2cd0f8b0357fe7bab6d27c2186ed565530fb194a77dfd2b35a756d3b7c89e289.
The independent Python implementation also checks palindrome avoidance and k_t on every t in this interval.

## Discovery and interpretation
The first-pass exhaustive short-seed screen covered integers 1..99999, excluding initial palindromes and filtering for survival through 128 steps: 6020 survivors, partitioned into 261 distinct exact first-successor orbits. All 261 class representatives survive 1024 steps; 40 classes have an odd paired coefficient at every t=0..2048, and retain this property through 20000 with maximum first-odd index 26. These facts and 40 rows are produced by the optional --survey command. This is a discovery filter, NOT an exclusion theorem outside its exact scope.

Merely observing a first-odd index of order log(time) in a long trajectory may reflect ordinary parity statistics rather than a conserved physical interface. The genuinely exact structural statement is coalescence of two parametric, short-digit families into two independent measured orbits. A route toward infinity would have to prove one-step closure of a bounded-pair-parity language with additional carry-context constraints, perhaps using the existing AgentN04 / AgentN07 folded automata, rather than treating a finite maximum as a proof. No such closure has been established here.

## Reproduction
In a source checkout: sh calculation/new_structures/agent-X08/run.sh. Needs g++ C++17, Python 3, sha256sum; can be computationally expensive for the two full 20k bigint traces. The script builds and checks both parametric families, reruns the 1..99999 discovery screen, repeats the two 100k C++ traces, then compares complete-state SHA-256 for independent 20k Python/C++ traces. This is one non-Lean result; no Lean claim or 196 result is made. GitHub connectivity prevents a local checkout and tools/verify.py --changed was not run.
