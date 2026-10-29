# Agent X30 phase-dislocated carry-crystal shadows

**COMPUTED**: reproducible exact finite-horizon decimal trajectories. **PAPER PROOF**: the carry-reset interface lemma below. No Lean verification and no infinite base-10 certificate.

## Distinct mechanism

The W10 control is an unmodified period-four seed ("5346")^Q. X30 introduces an *interior phase-dislocation*, not a simple local gauge eraser: X0=("5346")^12000 and Y0=("5346")^4000 ++ "3465" ++ ("5346")^7999, with all strings written MSB first. Both are genuine decimal integers.

For every t=0..20000, two independent engines verify that X_t and Y_t have the same length and overflow bit, but Y_t is NOT X_t. Their initial and final Hamming disagreement are 4 and 21586; maximum over the run is 21744; no t coalesces. Both have 8323 total leading overflows. The pair-coefficient word P_i=d_i+d_(n-1-i), indexed LSB first, contains a consecutive period-four run of length >=3941 in Y_t at EVERY state, with exact minimum at t=20000. The first mismatching mirrored digit of Y_t occurs at index <=18 and lies in a common exterior shared with X_t: the two exterior guards each have >=14129 digits at all times. Initial/final length is 48000/56323. Final FNV-1a 64-bit checksum on MSB-first decimal ASCII bytes is d4ed11ed5dc47a65 (initial offset 1469598103934665603).

The separate radix-10^9 arbitrary-precision engine and decimal schoolbook carry engine agree at all 20,001 complete integers, and independently verify palindrome avoidance and pair-periodicity. Further samples (kind1 span80, kind2 span1/80, kind3 span1) maintain a common external witness and the same overflow clock for 20k steps. Q=10000, a=3333, one phase slip also passes with minimum period-four run 1273 and final length 48323. This is not a claim for all possible patches.

## Carry-reset interface lemma (PAPER PROOF, any base >=2)

Write s_i(x)=x_i+x_(n-1-i) for an n-digit input, LSB first; c_0=0, c_(i+1)=floor((s_i+c_i)/b). All carries are 0 or 1. If s_i(x)=s_i(y) for i<ell, output digits agree at positions <ell by induction from c_0=0. If s_i(x)=s_i(y) for i>=r and the common s_r differs from b-1, then c_(r+1)(x)=c_(r+1)(y) regardless of incoming carry (for s_r<=b-2 the next carry is always 0, for s_r>=b it is always 1). Hence output digits agree for all positions >r and both final overflow bits agree. This is exact even if the interiors and their pairword coefficients differ.

A possible *relational reset-shadow certificate format* is a finite graph of phases with two simultaneously normalized, length-parametric pairword templates (reference and mutant), identical outer ports, bounded reset barriers around unrestricted defect pockets, and a common outer palindrome-mismatch witness. Each edge must check universally over all pumped lengths: true reverse-and-add, interface reset at both ends, next guarded port states, and guard inequalities. A directed cycle whose guards never shrink below their stated bounds and whose witness stays in an equal exterior proves nonpalindromicity of the mutant orbit by induction, even with noncoalescing and expanding interiors. No such graph closes in these experiments: this statement specifies the soundness conditions, not a discovered certificate.

## Failure mode and next structure

The periodic run shrinks from 15997 to 3941, while disagreement grows beyond 21000 positions. The experiment therefore lacks a regenerative guard. A naive interval abstraction treating 320 central digits as independent arbitrary 0..9 digits lost all known-digit exterior witnesses by t=58; it erases essential phase and carry correlations. The promising replacement is a correlated automaton tracking four-digit phase and paired boundary carries, rather than independent wildcard intervals.

## Reproduce

Compile phase_shadow.cpp and independent_limb.cpp using C++17 -O3. Run each with arguments "12000 4000 1 1 20000". For extra checks run phase_shadow with "12000 4000 80 1 20000", "12000 4000 1 2 20000", "12000 4000 80 2 20000", "12000 4000 1 3 20000". Run independent_limb with "10000 3333 1 1 20000". Compact stage checkpoints including independent FNV64 hashes: calculation/new_structures/agent-X30/checkpoints.csv. No Lean files or shared sources were modified.
