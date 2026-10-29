# W12: a universal finite-horizon four-digit decimal pump

**Status:** COMPUTED (the 20,000-edge finite witness); PAPER PROOF (a two-sample soundness lemma). Neither LEAN-VERIFIED nor an infinite decimal Lychrel certificate.

## Explicit three-step motif
For every integer q>=2, let N0(q)=12(0297)^q34 in conventional MSB-first notation. Its first three decimal reverse-add states are
N1(q)=55(8217)^q55,
N2(q)=111(5346)^q10,
N3(q)=127(9702)^(q-1)969721.
The period-4 spatial interior at t=3 is a rotation of the starting 0297 word. Each identity is a rational-polynomial identity in X=10^(4q); the independent digit and base-10000 ordinary-integer engines check q=2,3 (two distinct X values, enough to prove an affine identity), and q=9,45,1000 as controls. At t=47, this nonconstant period-4 interior becomes a uniform zero band, so the three-step *bulk* return is not temporal closure of the whole integer.

## All-q soundness lemma (PAPER PROOF)
Fix a decimal digit word S=A B with nonzero first digit, and a fixed four-digit word U (possibly containing zeros). Define S(k)=A U^k B for k>=0. Its numerical value is an affine rational polynomial in X=10^(4k), because val(U^k)=val(U)(10^(4k)-1)/(10^4-1). The value of the reversed digit word reverse(B) reverse(U)^k reverse(A) is likewise affine in X. Consequently, for any three such template families S,T and a proposed reverse-add edge S(k)+rev(S(k))=T(k), the difference of the two sides is affine in X. **Equality at k=0 and k=1 implies equality for every integer k>=0**, since X=1 and X=10000 are distinct. Leading zeros in a reversed word are harmless since its integer value is unchanged. This is a direct exact arithmetic lemma, not finite-sample extrapolation.
If S(0) has a left-vs-reflected-right digit mismatch strictly outside the A|B insertion cut, that same mismatch persists for every k, proving S(k) nonpalindromic independently of the inserted word.

## New decimal finite-horizon certificate
Set q0=6000. Ordinary-digit reverse-add generates 20001 actual words S_t(0) at q0 and S_t(1) at q0+1 for t=0..20000. At each t put c_t=floor(len(S_t(0))/2). The checker establishes EXACT string equality
S_t(1)=S_t(0)[:c_t] ++ U_t ++ S_t(0)[c_t:]
with len(U_t)=4, independently at all 20001 phases. Thus define A_t,B_t by splitting S_t(0) at c_t and use the soundness lemma to prove, by induction over t, that the symbolic word S_t(k)=A_t U_t^k B_t is the genuine reverse-add orbit for **all k>=0**, i.e. all q>=6000. At each phase a nonpalindromic digit mismatch occurs outside the split; maximum matching outer prefix is just 16 digits. The checker also checks the 128-digit window around the centre has primitive digit and mirror-pair coefficient periods in {1,4} at every phase. The pairword is computed from the actual decimal digits, not postulated from lattice coefficients.

Control results for q0=6000: 20000 steps; final length 32307 decimal digits; gamma0=11697, gamma1=8303; final FNV64 of the full MSB-first word = 407e87dc3b767c04; digit-centre period 4 at 47 phases, 1 at 19954; pair-centre period 4 at 46, 1 at 19955. For each transition the primary engine adds decimal digits with carries from least significant to most; the independent engine separately reverses the decimal string and adds base-10000 limbs at every q0 step and at q0+1 checkpoints.

## Motif search and obstruction
scan.cpp exhaustively examines 100 + 1000 + 10000 + 100000 + 1000000 literal input words of lengths 2..6 in fixed 12 w^45 34 seeds. It detects every primitive period<=6 of a 40-digit central interval after steps 0 and 3, returns only equal cyclic motifs with all four whole numbers nonpalindromic, and prints six nonconstant cyclic classes: 0297, 0495 (length 4); 142857, 153846, 172656, 273438 (length 6). This is a *local three-step bulk discovery*, NOT a classification of all decimal lattice cycles or an infinite certificate. The actual overflow trajectory after step 3 is not period-three; the 0297 seed's primitive nonconstant interior reaches a uniform zero band at step 47. With q=80, the 128-digit central period witness fails at step 318, illustrating eventual inward boundary contamination for a shorter reservoir; that is NOT a palindrome claim. For q>=6000, the proven finite horizon is 20000 steps. Missing: an indefinitely renewable four-digit reservoir and closed time-phase boundary language.

## Reproduce
From repo root:
g++ -O3 -std=c++17 calculation/new_structures/agent-W12/check.cpp -o /tmp/w12
/tmp/w12 6000 20000
g++ -O3 -std=c++17 calculation/new_structures/agent-W12/scan.cpp -o /tmp/w12scan
/tmp/w12scan

Independent consistency checks are built into /tmp/w12. See checkpoints.txt for compact final signatures. No network, external package, Lean, or uncommitted data needed. The entire repository verify.py --changed was not run because the sandbox cannot resolve github.com for a checkout; only the standalone computations were run. No claim is made about the repository-wide verifier.
