# W13: a charged dipole and pumpable inverse corridor in decimal reverse-and-add

**PAPER PROOF** (exact all-k macro identity, arbitrary multiplicity under explicit separation assumptions). **COMPUTED** (independent ordinary-integer controls through 20,000/100,000 steps). **UNDECIDED** (all-time Lychrel property). This is a nonlocal *constructive* mechanism, building on the already known period-three four-step packet eraser from Agent N28; the new contribution is its explicit arbitrarily long, charge-balanced, one-step inverse and a sound interval pump, not a re-verification of the four-step particle.

## 1. Words, physical arithmetic, and exact parametric seeds

A pairword P of the nonzero decimal integer N is the least-significant-first list P_i=d_i+d_(n-1-i), symmetric and in {0,...,18}. Define F(P)=pairs(normalize10(P)), where normalize10 performs genuine one-directional decimal carries and appends a final carry when present. Then for every ordinary positive decimal N with pairword P, pairword(N+reverse(N))=F(P); moreover N+reverse(N)=val10(P) independently of the digit split.

For any half-length h and i=0,...,h-1, define H_h[0]=17, and H_h[i]=4 if i≡1 (mod 3), else 1 for i>=1. Set P_h = H_h ++ reverse(H_h), a realizable symmetric pairword of length 2h with P_h[0]=17 and an 8 as the leading digit of its deterministic decimal lift (low digit 9, high digit 8). Fix an integer k>=1, an index a>=30 with a≡2 mod3, and put b=a+6k+3. Require b+20<=h. In the LOWER half replace the length-(6k+6) interval a,...,b+2 by

    [3,4,3] ++ [2,0,5,0,2,3]^k ++ [4,3,4]

and make the mirror replacement. In the baseline the same interval is

    [1,1,4] ++ [1,1,4,1,1,4]^k ++ [1,1,4].

All replacements lie in 0,...,5, have the same length as the original, preserve P_0=17 and produce valid positive decimal integers. The perturbation contains an **arbitrarily long nontrivial alternating residue corridor**; it is not bounded support as k increases.

## 2. Exact one-step inverse: signed checkerboard-charge cancellation

On a source word with no 9 in the interior and overflow gamma=1, the low/high interior paired-digit map is F(P)_i=r_i+r_(i-1), where r_i=P_i-9*[P_i>=10] (the two-ended carry-gauge quotient). The exterior P_0=17 forces overflow 1; all P_i for 1<=i<h and their mirrors are <=5, so after the initial reset the interior actually has zero carries, and **r_i=P_i** there. The outer two columns are unchanged, hence both original and perturbed words have the same overflow and first two output columns.

Let δ_i be the change we want in the output. We ask for exactly two defects at positions a and b, each changing the consecutive period-three target triple [5,2,5] to [7,7,7]: δ_a..a+2=(2,5,2), δ_b..b+2=(2,5,2), and δ=0 otherwise. The source correction ε_i is uniquely obtained by

    ε_(a-1)=0;   ε_i=δ_i-ε_(i-1).

The first three values are 2,3,-1. Between packets, ε alternates +1,-1. Because b-a=6k+3 is **odd**, ε at b-1 equals -1; the last three values at b,b+1,b+2 are 3,2,0, so ε terminates exactly. The source coefficients P_i+ε_i are the displayed block [3,4,3] ++ [2,0,5,0,2,3]^k ++ [4,3,4] (check the six-phase residues directly). Every one stays in 0,...,5 and keeps the incoming/outgoing decimal carry zero. Thus the source has **no changed pair coefficients outside that whole interval**, while its first successor differs at **exactly six positions** a..a+2 and b..b+2. Its one-step image is exactly two separated known period-three defects. This is an exact all-k identity, not an interpolation from the sampled lengths.

The alternating moment of the three-site output defect is (2-5+2)=-1. Two copies shifted by an odd distance carry opposite signed checkerboard flux and cancel; the recurrent alternating inverse is precisely the balanced dipole corridor. A single isolated defect cannot have such a compactly terminating inverse under the same no-9 gamma=1 local quotient. This identifies the **required source format**: a pair of charged packets connected by a parity-controlled alternating corridor, rather than a bounded centre.

## 3. Four-step local sink with exact guards and all-M independent corridors

The baseline first successor has, at every index a≡2 mod3 sufficiently far from its ends, a [5,2,5] triple, and the altered successor has [7,7,7] at a and b. From that instant the rooted overflow clock for four steps is 0,1,0,1. Direct exact two-ended carry tables show the support of each isolated packet, relative to its start, is:

| time from first successor | support |
|---|---|
| 0 | 0,1,2 |
| 1 | 0,1,2 |
| 2 | 0,1,2,3 |
| 3 | 0,1,2,3 |
| 4 | none |

The corresponding untouched left/right guard coefficients (at start-1 and start+4) at the four input steps are (5,2), (10,4), (5,5), (10,10). All differ from 9, so each resets the carry even with nonlocal decimal reflection. No packet can communicate across a gap of at least five untouched columns in these four steps. Since b-a=6k+3>=9, both sink packets are independent. Therefore F^5(P_h)=F^5(P_h with this arbitrarily long corridor), **for every k>=1 and every eligible finite h**. One further ordinary addition gives equality of integer values at N_6, regardless of the initial realizable digit split.

For M corridors with respective (a_j,k_j), choose disjoint intervals [a_j,b_j+2] with their neighbouring four-cell interaction windows disjoint, e.g. the next a at least previous b+20, and satisfy the same global h bound. Every subset of M corridors is an exact predecessor of its own two-packet phase and all 2^M pairwords coincide at step 5. These 2^M distinct positive integers therefore have identical sixth reverse-and-add iterates. The rooted first six steps have an odd pair-coefficient in positions 0,2,0,4,0,3, so every variant avoids palindromes at t0..t5 without relying on a late numerical trace.

## 4. Independent computation, controls and finite horizons

The standalone `charge_dipole.py` checks the full six-state pairword traces, the exact two-triple one-step support, separate ordinary digit-list and Python arbitrary-precision integer calculations, and equality of integers after six additions for corridor lengths 12,18,24,30,36,66,126,306,606,1806,6006,12006 (k=1,2,3,4,5,10,20,50,100,300,1000,2000). For M=4 with independent corridors, all 16 subsets are exhausted in the coefficient model; 16 sampled subsets are independently checked with two ordinary decimal arithmetic implementations. The data contains an explicit 160-digit q80,a32,k1 baseline/dipole pair.

For h=6000 and twenty independent k=1 corridors at a=200+198j, j=0,...,19, there are exactly 2^20 distinct 12,000-digit ordinary decimal initial seeds. The C++ independent checker `replay20k_dipole.cpp` verifies the altered and baseline integer joining at step 6, then replays the baseline independently using (i) least-significant-first byte-vector add-with-reflection carries and (ii) GMP `mpz_class` arithmetic on the separately reversed base-10 string at *every* t=0,...,20,000. The full integers agree at all steps; every state is nonpalindromic. Every one of the 20,001 states contains an odd pair coefficient within the first 32 positions. Baseline output: 20,330 decimal digits, 8,330 overflows, low-first digit FNV64 bd9eb7ba3cf147d3. (The initial 1,0 alternating overflow clock first deviates at t=22; it is not silently assumed for the whole replay.)

For compact h=80,a=32,k=1, two different explicitly listed 160-digit decimal seeds merge at integer step6. The independent `replay_string100k.cpp` computes the baseline through t=100,000 using two *separately implemented* ordinary decimal adders: a low-first byte-vector adder, and a conventional most-significant-first decimal text adder that explicitly constructs reverse(s) and adds right-to-left. Their entire decimal numerals agree at every state, and every one of the 100,001 states is nonpalindromic with an odd pair coefficient among the first 32 positions. Final length 41,582, overflows 41,422, low-first FNV64 8eeb5483f7c87950. Its first 32-coefficient states at t0..t99999 are **all distinct**, and no period <=4096 appears over the final 10,001 states; the computation therefore does not supply a bounded recurrence invariant. C++/GMP is used separately for 20,000-step full-integer replay of the twenty-corridor family, and both Python true-integer and digit-list arithmetic cover the finite mergers.

Run from repository root: `sh calculation/new_structures/agent-W13/run_dipole.sh` (Python3, C++17 compiler, GMP headers and libraries). Data: `calculation/new_structures/agent-W13/dipole_observations.json`. Controls: the script asserts exact counts, observed fingerprints, the 12,006-coefficient largest perturbation and the compact seed lengths.

## 5. Scope and next certificate direction

This is a **new length-parametric positive mechanism**: a pumpable nonlocal corridor stores an alternating carry charge that collapses into just two localized packets on the very next integer step, and those two packets vanish completely four steps later. Unlike a stationary finite centre, the construction tolerates arbitrary distances between two disturbance sources. It is **not** an infinite base-10 Lychrel proof: the source never regenerates the corridor after annihilation, and no finite all-time invariance of the 32-column odd exterior has been established. The search should now target a *renewing dipole source* with a signed-flux/phase state and a finite carry-reset boundary transducer, rather than uncharged bounded short centres. A sound certificate must verify all transition cases indefinitely, not merely 100,000 numerical additions.