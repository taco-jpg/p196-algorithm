# W23: An arbitrary-multiplicity coalescence code on the decimal p8/m48 bulk

**PAPER PROOF (finite-time arithmetic identity), with independent COMPUTED controls.** This is a constructive parametric family, not a proof that a decimal reverse-and-add orbit avoids palindromes forever.

## Statement
Use coefficient words low-first, `B=(17,5,0,2,1,9,15,18,14,9,3)`, and the explicit 48-coefficient word `W` from `AgentW23P48ThreeStepErasers`. For any integer M>=1 put q=M+4 and `H=B ++ W^q ++ [10,14,1,10]`. For every mask E subset of {0,...,M-1}, replace the adjacent `(13,9)` at positions `s_j=11+48*(2+j)+20` and `s_j+1` of H, for j in E, with `(8,5)`. Reflect the resulting halfword to the odd-length palindrome of pair coefficients `P=H_E ++ reverse(H_E[:-1])`. Lift P to a genuine canonical decimal integer N_E by assigning digit max(p-9,0) on the low side, min(p,9) on the high side, and centre 5.

**Finite coalescence theorem:** the 2^M numbers N_E are distinct; none is a palindrome at times 0,1,2,3; all their complete symmetric pairwords are EXACTLY identical at t=3; their actual ordinary decimal reverse-and-add iterates are equal at t=4. In particular the q100/M96 family contains 2^96 distinct 9,629-digit numbers with one shared iterate after four additions. Combining this exact finite identity with the independently verified q100 20,000-step base orbit gives a 20,000-step nonpalindrome horizon for all of those 2^96 seeds, not an infinite-horizon certificate.

## Why all M can be proved without a width search
The normalization map of a symmetric pairword is ordinary grade-school base-10 addition. An ascending/descending carry at coefficient p changes its outgoing bit with the incoming bit **only when p=9**. For p different from 9, outgoing carry is fixed by p, independent of the entering carry (0/1). Thus if two source words differ in a bounded interval, differences in the two emitted digit streams terminate at the first non-9 coefficient outside the interval in their respective directions. The mirror pairing with length-overflow gamma in {0,1} shifts partners by at most one. Consequently, if all input sites in a protected region have runs of 9 of length at most r, the output's difference support is contained in the old support widened by at most r+2 positions on each side; this follows directly by induction over the carries (both orientations). The global overflow also agrees if the changed sites have a non-9 guard before the most-significant end.

For the rooted p8/m48 initial word and its first three temporal bulk phases, the longest run of coefficient 9 is respectively **2,1,1** (finite inspection of one spatial period, the 11-cell rooted B phases and the reflected centre). Patching (13,9)->(8,5) introduces no longer 9-run. The phase-1 and phase-2 local patch rows (listed and exactly checked in `AgentW23P48ThreeStepErasers`) also introduce no longer run. Therefore a conservative support cone expands at most 4 sites per step; through t=3 its maximum radius is 12. Packet starts are exactly 48 sites apart, so even the conservative cones (initial two-site intervals widened by 12 on either side) remain disjoint. The first packet is 127 coefficients from the low endpoint, and the last packet leaves at least two whole 48-cell W periods before the centre. Root and centre carry guards remain outside all three-step cones. The same applies to the reflected high-half packets.

The isolated packet's **exact verified local tile** in the actual p8/m48 phase-0 bulk is:
t0: (13,9) -> (8,5), difference sites {0,1};
t1: difference sites {0,1,2};
t2: difference sites {0,2};
t3: no difference, with BOTH carry ports synchronized to the unmodified lattice.
The complete local rows and the two-sided carry-normalization code are in `AgentW23P48ThreeStepErasers`. Because the disjoint cones carry exactly the same background boundary states as isolated packets, a standard local induction (one packet at a time, one step at a time) proves that a simultaneous collection is just the disjoint union of isolated transient differences at t=0,1,2 and empty at t=3. Hence all masked pairwords agree at t3. Reverse-and-add depends only on the pairword, so their next integers at t4 agree.

The first eight rooted coefficient columns follow the exact p8 exterior phases for all t=0..3 by the same guard reasoning. They contain odd entries at each relevant phase (for example p0=17 at t0/t2; p1=13 at t1; p5=9 at t3); any decimal palindrome has only even symmetric pair coefficients. Thus all N_E at these four times are nonpalindromic. Injectivity of the initial digit splitting and the visibly different packet coefficients yields exactly 2^M distinct initial integers.

This is a PAPER PROOF of a **finite four-step identity**, not of any closed indefinitely resetting template. Lean checking was not attempted.

## Independent computation and exact scope
- Python arbitrary-precision integers, digit conversion/reversal with no pairword transition engine: all 1,024 masks at M=10, q=14, initial 1,373 digits, t3 identical full pairwords, t4 identical 1,375-digit integer.
- M=128, q=132: 20 independently selected masks including all-zero/all-one, initial 12,701 digits, common t4 length 12,703; PRNG seed 20261028.
- M=96, q=100: unmodified, all 96 patches and alternating 48 patches, initial 9,629 digits, common t4 length 9,631. Independent ordinary decimal C++ digit-vector engine confirms these three and checks palindromes at t0..3.
- Prior independent 20,000-step digit-vector AND GMP runs for the common q100 baseline give no palindrome, exterior clock 1010..., final 19,629 digits, FNV-1a low-first 971e60282dc35bc9. Because all 2^96 q100 seeds merge into that same orbit at t4, the finite horizon applies to all of them.

## Reproduction
```sh
python3 calculation/new_structures/agent-W23/packed_glue.py
g++ -O3 -std=c++17 calculation/new_structures/agent-W23/packed_digit.cpp -o /tmp/w23_packed && /tmp/w23_packed
```
For the independent 20,000-step baseline checks, run the `digit_replay.cpp` and `gmp_replay.cpp` commands documented in `AgentW23P48ThreeStepErasers`. Exact expected data in `packed_expected.json`.

## What remains
This is a dense **eraser reservoir**, not a regenerative reservoir. Initial packets all disappear and do not automatically reappear. To turn the phase-3↔7 reset alphabet from `AgentW23ClockedP48RepairAlphabet` into a decimal certificate, one must construct a time-periodic physical *emitter* whose generated repairs are absorbed before reaching the rooted nonpalindrome witness while net protected-band width is nondecreasing. No such emitter, stationary infinite defect front, or base-10 Lychrel number has been established here.
