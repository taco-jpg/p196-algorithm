# Agent N12: 256 decimal central collisions emit two- or three-digit defects

**COMPUTED**, exact finite scope for the adjacent decimal seed pairs N_k=39++0^(31000+k)++43 and N_(k+1), every k=0..255. Ordinary reverse-add in base 10. No claim of a base-10 Lychrel number, no infinite-time theorem, no excluded family census.

## New mechanism
The master-orbit exact-padding transfer of reports/AgentN12MasterOrbitCollisionSweep.md supplies true integer states for every k until near centre collision, then the new code follows each seed by independent decimal digit-array additions. At every t it compares the two canonical integers after inserting *one zero at the exact central split* of the shorter state (least-significant-first index ceil(n/2)). Let D_k be their first aligned mismatch time, and C_k,C_(k+1) the first time each symmetric pairword zero corridor has length zero.

All 256 pairs are identical under this padding through t=D_k-1; no length gap changes before their first disagreement. The first nonzero Hamming defect at D_k has **two or three decimal digits**, with maximum distance from the central split <=2. Exactly 242 pairs have two changed positions and 14 have three; 243 have radius 1 and 13 radius 2. The emission delay D_k-min(C_k,C_(k+1)) is always between 1 and 5, with exact counts for delays 1..5 of 110, 97, 33, 12, 4. The outermost 16 symmetric pair coefficients agree for both integers at all 256 birth events.

The initial gap length is NOT a monotone collision clock: for k=3, the shorter-gap seed has collision at step 51470 while the longer-gap seed collides at 51468; nevertheless their first difference at step 51469 is precisely two central positions at offsets [-1,0]. A different mechanism occurs for k=12: the first difference is three central positions [0,1,2] at step 51483, after the earlier collision t51482. Both are exact local changes in real decimal integers. The 256 cases therefore support a **small birth-kernel** view: a macroscopic zero corridor may disappear and inject a bounded local defect while distant exterior coefficients are still synchronized. They do not prove an eventual stationary glider or stable finite-state propagation: the N12 postcollision wave from k0/1 previously expanded to radius 3239 by t60000.

## Exact reproduction and independent controls
From repo root, run `bash calculation/new_structures/agent-N12/run_pair_emission.sh`. It compiles the master transfer and the new `master_pair_emission.cpp`, generates all 257 master collision rows and 256 pair-birth rows, and independently checks counts, cross-table collision equality, all peripheral equality flags, and SHA256 `8e9e43633153ca7993bcd486e258acbcc8b4fee2e0a7109706f5fdceee28004a`. Expected output: `PAIR_EMISSION_ALL_256_PASS birth2=242 birth3=14 lag1to5`.

Independent real-integer controls do NOT use digit-array carry arithmetic. They start with the *literal original 52k-digit seeds*, execute each actual reverse+add step using arithmetic on base-10^9 integer limbs, assert every state nonpalindromic, and output the requested exact integers. To regenerate the two birth cases:

```sh
cd calculation/new_structures/agent-N12
g++ -std=c++17 -O3 birth_integer_oracle.cpp -o /tmp/n12_birth_oracle
/tmp/n12_birth_oracle 31003 51469 > /tmp/n12_31003_51469.txt
/tmp/n12_birth_oracle 31004 51469 > /tmp/n12_31004_51469.txt
/tmp/n12_birth_oracle 31012 51483 > /tmp/n12_31012_51483.txt
/tmp/n12_birth_oracle 31013 51483 > /tmp/n12_31013_51483.txt
python3 verify_birth_snapshots.py /tmp/n12_31003_51469.txt /tmp/n12_31004_51469.txt /tmp/n12_31012_51483.txt /tmp/n12_31013_51483.txt
```

Expected output ends with `BIRTH_INTEGER_CONTROLS_PASS`. The snapshot verifier checks four separately known SHA256 hashes, the exact LSB-centred changed positions, number lengths, two palindrome mismatches, and all outer 16 pair coefficients. Four full original-seed runs and all 256 pair-birth table checks passed locally. No bit-level oracle is imported from the primary engine.

## Soundness and limitations
Finite-family correctness is conditional only on the central-zero padding lemma's standard carry argument (the earlier report proves the induction) and the literal finite replay after each safe activation. The master-to-shorter unpadding is justified only while the short source has z>=4; every activation checks that bound, and after that there is no padding assumption. No general two-or-three-cell bound is claimed for arbitrary decimal centres, arbitrary k beyond 255, or later times. A new certificate would have to show regeneration, containment, or recurrent control of these emitted defects indefinitely. This report supplies a positive testable target for such a renormalisation rule, not its infinite closure.
