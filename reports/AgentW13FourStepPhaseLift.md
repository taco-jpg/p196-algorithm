# Agent W13: four-step phase-lift of a non-gauge eraser

**PAPER PROOF** for the exact local carry-reset transport and all-M independent-packet amplification, **COMPUTED** for all finite ordinary-integer checks. This is a temporal backward-preimage of the independently committed three-step p8 eraser (`results/AgentW13ThreeStepP8Eraser.md`), *not* a second infinite certificate.

## Explicit family
Write the symmetric least-significant-first pair coefficient word of a canonical positive decimal integer as P_i=d_i+d_(n-1-i). Let B be the rooted length-39 decimal exterior and W the period-20 word listed verbatim in `calculation/new_structures/agent-W13/three_step_eraser.py` (first p8 SCC in `calculation/decimal_frontier/lattice_formats/p8_scc.txt`). Let T=F(B ++ W^q ++ [0] ++ reverse(W^q) ++ reverse(B)), where F is pair(normalize10(P)). T is the real temporal phase-1 full pairword and has even length 2(39+20q)+2. For every M>=1 and q>=30+10M, independently at each j_m=39+20(30+10m)+10, m=0..M-1, replace the triple T[j_m:j_m+3]=[3,2,7] and its reflected counterpart by [3,2,7], [5,16,0], or [1,6,5]. All 3^M symmetric pairwords are positive-decimal realizable and distinct. For q300 the initial length is 12080. For canonical realization, split pair sums into min(9,p) on the lower half and p-min(9,p) on the upper half, then when the uppermost digit would be zero (p_0=8), move one digit from the lower to the upper end. The exact pairword, arithmetic, length and nonpalindromicity claims do not depend on that choice of digit split.

## Four-step two-ended local contract
The exact digit normalization is c_0=0, c_(i+1)=floor((P_i+c_i)/10), emitting d_i=P_i+c_i-10c_(i+1), and appending c_n if nonzero; the next pairword pairs digits at reflected indices. A coefficient <9 resets carry to 0, >9 resets carry to 1, and 9 alone transmits it. The rooted overflow clock from temporal phase 1 across four steps is 0,1,0,1. For both nontrivial replacements, the exact lower-half difference supports relative to j_m are:

| step | lower-half differences |
|---|---|
| 0 | 0,1,2 |
| 1 | 0,1,2 |
| 2 | 0,1,2,3 |
| 3 | 0,1,2,3 |
| 4 | none |

The two coefficients immediately outside each support interval, j_m-1 and j_m+4, are unchanged and equal the baseline at each step. Their successive pairs are (10,8), (1,17), (6,8), (13,17). None equals 9, so each direction's carry resets before entering/exiting the local packet. This finite table and the exact interior transducer are independent of the remaining centre and of the number of 20-period copies. Since packet locations are 200 columns apart, their supports cannot overlap in these four steps. Applying the same local table simultaneously proves for **every q and M in the stated range** that the full pairwords coincide at step 4, without an assumption of a small centre or extrapolation from numerical lifetimes. The ordinary reverse-add successor at step 5 is uniquely determined by the shared pairword at step 4, so all 3^M integers meet there.

The first transition sends baseline [3,2,7] to [7,4,15]. Its two variants become [12,12,2] and [3,12,11], with identical residues (3,3,2) modulo 9. Both are phase-2 versions of the eight three-step erasers, but their source residues, respectively (5,7,0) and (1,6,5), differ from the original (3,2,7). The two altered pairwords themselves merge after two steps through the next overflow, while both rejoin the untouched exterior after four. The construction is a *two-tier finite preimage funnel*: the extra step is a real, non-gauge predecessor, not merely a time-shift of an identical source.

## Exact finite-scope controls
`four_step_precursor.py` checks both five-row local traces, every guard, and all 3^3=27 combinations at q=65,M=3. It independently creates ordinary canonical decimal strings for 36 deterministic patterns, comparing actual Python arbitrary-precision N+reverse(N) to a separate digit-vector carry implementation at each of five additions. All 36 converge to one integer at t5; all numbers at t0..t5 are nonpalindromic. The exterior has odd pair coefficients at lower indices 1,0,4,0,7 for t0..t4.

`replay20k_phase1.cpp` independently constructs a q=300,M=25 phase-1 source from its own rooted B/W data, checks a representative packet choice and the baseline join at pairword step4 and ordinary integer step5, then replays the common baseline through 20,000 **genuine** decimal reverse-and-add steps by two independent representations: base-10 digit vectors and GMP `mpz_class` operating on separately reversed decimal text. It checks their *entire integer string* at every state, no palindromes, the odd 39-column exterior, and 60 complete period-20 bulk copies repeated with temporal period8. Result: 12080 starting digits, 22080 final digits, exactly 10000 length overflows, final FNV-1a64 (low-first digits) `6268b4257ba99e6f`. Since all other 3^25 sources converge with the baseline at t5 by the exact local proof, the same finite t0..20000 palindrome avoidance holds for all of them.

Run from repository root: `sh calculation/new_structures/agent-W13/run_phase1.sh` (Python 3, g++ C++17 and GMP development libraries). All code/data and both independent implementations are committed alongside this report.

## Infinite-time gap and constructive next direction
This packet family disappears into the bulk, which still loses a finite exterior supply. It is **not** an infinite Lychrel construction. To turn the two-tier inverse funnel into an infinite certificate, a successor-generation interface would have to regenerate the charged precursor (or a phase-shifted copy) every renewal, with a compatible centre. A natural format is a finite-state two-ended inverse carry transducer with an alternating flux charge across a bounded gateway; the present result certifies a *sink* and a nontrivial predecessor, not the self-generating source.