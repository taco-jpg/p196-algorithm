# N11: Delayed exterior information front and a guarded-prefix transfer rule

## Claim and context
**COMPUTED** for the finite-scale observations; a new *elementary one-step paper lemma* is proved below. **No decimal Lychrel number, no infinite time invariant and no Lean kernel result are claimed.** This is a constructive study of the explicit base-10 N_L seed from results/AgentN11CarryShadowFamily.md, with growing 9 coefficient stripes and 11 barriers. A second independent prior result, results/AgentN11BallisticZeroWall.md, describes the faster-moving zero-region walls.

## Measured propagating disturbance
Generate two ordinary integers N_L and N_45000 using the same deterministic xorshift exterior and different neutral 9 stripe lengths. At every step, run *literal* reverse-and-add on each integer (each number's own length), record gamma=1 iff length increases, and compare the least-significant-first paired coefficient prefix P_i=d_i+d_(n-1-i). Define T_K(L) to be the first step when the first K pair coefficients differ, and T_gamma(L) to be the first differing overflow bit. No assumption of periodicity, shared digit length, or template-correct arithmetic is used.

Exactly computed observations (all times are step indices; the new value has been checked and the preceding step still agrees):

| L | Original zero region disappears | T_1024 | T_64 | T_1 | T_gamma |
|---:|---:|---:|---:|---:|---:|
| 2,000 | 3,334 | 7,570 | 13,120 | 13,505 | 13,512 |
| 4,000 | 6,648 | 20,477 | 26,006 | 26,346 | 26,352 |
| 8,000 | 13,274 | 46,226 | 51,936 | 52,270 | 52,274 |

The outer-64 synchrony times per L are approximately 6.56, 6.5015, 6.492, whereas the previously verified zero wall lasts only approximately 1.667, 1.662, 1.659 times L. This shows a *positive delayed communication mechanism*: even after an absorbing zero stripe has vanished locally, a difference in the centre can take much longer to reach the exterior and alter the overflow schedule. The numbers are exact for the stated seeds and caps, but no limiting speed, linear asymptotic law, or universal lower bound is claimed.

At each L, the full ordered times for prefix widths K=(1,2,4,8,16,32,64,128,256,512,1024) are recorded in shadow_expected.json. Larger K receives a disturbance sooner. Independent MSB-first decimal-string schoolbook arithmetic checked K=1,64,1024 and gamma for all three L values. It tested every iterate for palindrome through T_gamma and found none. To keep the independent L=8000 control small, it compares N_8000 with N_16000; a separate full digit-vector run verifies N_16000 and N_45000 share all these prefix windows and gamma through t=56,000. Thus its first mismatches equal the N_45000 comparisons.

## One-step guarded exterior transfer lemma (elementary proof, not a Lean theorem)
Write the symmetric base10 pair coefficient word P for an n-digit number N, with P_i in 0..18 and P_i=P_(n-1-i). Let N and M have possibly unequal even or odd digit lengths, each with at least 2K+4 digits. Suppose their first K+1 coefficients P_0..P_K coincide and their common P_K != 9, with K>=1. Then after one ordinary decimal reverse-and-add:
1. Their overflow bits gamma (0 or 1 depending on growth in digit length) coincide.
2. Their first K successor pair coefficients Q_0..Q_(K-1) coincide.

**Proof.** Normalizing P, the carry-after-a-coefficient map sends any incoming carry c in {0,1} to 0 when P_i<=8 and to 1 when P_i>=10; at P_i=9 it sends c to c. Hence the high-end carry of any symmetric pairword is determined by the outer portion down to the first non-9 coefficient. Since P_K!=9 and P_0..P_K match, the carry entering the most significant position, and therefore its output overflow gamma, match for the two integers (this does not depend on the unmatched central section). The low-end output digits through index K-1 depend only on P_0..P_(K-1) and initial carry 0, hence match. Their high-end partner digits in the new number at reflection-shift gamma depend on outer coefficients through P_K: if gamma=0, the carry entering the output at position n-1-i for i<K is fixed by the first non-9 encountered from coefficient P_K toward the outer end; if gamma=1 the partner index shifts by one and uses no deeper coefficient. All required inputs and carry maps agree, so the high-end partner digits match and Q_i match. No assumption about the unmatched digits or about recurring periodicity is required. QED.

Equivalently, a certificate checker can verify a finite *guarded spacetime prefix edge* with length K+1 on one row and K on the next, without inspecting or assuming anything about the rest of either input integer. The propagation is one-way/contracting at each edge; on its own it CANNOT be iterated indefinitely at fixed K. To turn it into a Lychrel certificate would require a regenerative boundary transformation that restores at least one guarded site often enough to offset the contraction, and a nonpalindromic witness on every row.

## Independent checks
1. sync_front.cpp: compiled least-significant-first decimal-digit arithmetic; computes the exact first changed prefix K and gamma for 3 stripe lengths, 11 values of K, and one reference-equivalence control N_16000 vs N_45000 through 56,000 steps.
2. sync_independent.cpp: structurally distinct most-significant-first decimal-string schoolbook addition against the literally reversed string; tests every compared iterate for palindrome, checks first mismatch for K=1,64,1024 and gamma. In all three cases these match sync_front.cpp.
3. guarded_prefix.py: 12,000 deterministic randomized pairs of ordinary decimal big integers with differing lengths/centres but matching guarded prefixes; tests both successor gamma and all K successor pair coefficients. Includes long 9 transmitters in the outermost positions and both gamma values.
4. shadow_reproduce.sh: one command, no external dependencies beyond C++17, Python3 stdlib and Bash. Reconstructs the seeds from source and compares all times against shadow_expected.json.

Reproduce from repo root:

~~~sh
bash calculation/new_structures/agent-N11/shadow_reproduce.sh
~~~

## Exactly what breaks and constructive next step
The first exterior mismatch is a *delayed* event, not a prevented one. A static all-9 seed stripe converts to zero, its walls eventually close, and after a longer transition the formerly identical exteriors and gammas diverge. At finite L, therefore, the observed protected prefix is NOT inductive for all t.

A plausible new certificate format should combine (a) a guarded outer prefix transfer, (b) a moving zero/9 wall carrying a contract for the boundary carry, and (c) a separate replenishment edge that increases the number of guarded sites or spatial band length over each temporal cycle. This allows a spatially moving centre, unlike the previously searched fixed-width periodic kinks. The next constructive challenge is a specific digit-level regeneration rule with positive net guarded-prefix growth per cycle; no such positive edge has been found or claimed here.
