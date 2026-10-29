# W02: p12/m9 decimal ballistic frontier and finite collision-delay renormalization

## Physical seeds and two independent engines
**COMPUTED, base 10 only.** Let P be the palindromic least-significant-first pairword with exterior B2=(2,11,1,6,8,1,7,15,9,3,9,4,7,9,10,16,9,11,4,10,8,8,9,11,11,7,4,3,9,12,1,1,9,11) and interior period W2=(1,10,8,5,9,16,0,9,11), total length 20,000. Realize a physical decimal integer by assigning d_low=P-min(P,9) and d_high=min(P,9) at mirrored sites. Replace the 11 symmetric pair coefficients anchored at x=2100 by A=(6,1,0,1,11,14,10,6,11,16,1) or B=(16,0,9,11,1,10,8,5,14,18,0). These symbols were used in N21's earlier first-collision study; the new result concerns their frontier time laws.

The first engine evolves differences against the period-12 bulk using explicit two-direction carry arrays and gamma schedule. The completely separate checker starts all three ordinary decimal digit vectors (background, A, B) from scratch, adds each number to its decimal reversal, and verifies all 5001 state lengths, both entire halfword-difference FNV64 hashes, both support endpoints and rightmost actual coefficients. It checks every one of the 15,003 numbers for palindromicity. All checks passed. The generated 5002-line trace SHA256 is 79691eb68dd08543c3627b68e5b46bde3de5b7aa86fb7ee9419b3e14e23e0ab8, checked on reproduction; no opaque trace needs to be downloaded.

## Frontier symmetry, finite scope
Let R_X(t) be the largest lower-half position at which the pairword of packet X differs from the unmodified integer orbit. Exact computations show:

    R_A(t+76)-R_A(t)=33  for all integer 337 <= t <= 4924
    R_B(t+76)-R_B(t)=33  for all integer 155 <= t <= 4924.

For every phase and every lattice position, the background arrays obey W_(t+76)(x+33)=W_t(x), C_(t+76)(x+33)=C_t(x), and gamma_(t+76)=gamma_t. This is an exact 108-entry table check from 76 mod 12=4 and 33 mod 9=6, explicitly asserted by the generator. It explains phase compatibility but NOT infinite persistence.

Crucially, a frontier position is not a full soliton state. The coefficient one site behind the rightmost defect has a (76,33) translation mismatch as late as t=4592 for A and 4644 for B, and the nonperiodic wake keeps growing. One cannot infer a whole-packet return, a bounded-width centre, or a permanent palindrome-avoidance invariant from this boundary equation.

## Ordered packet collision clock and exact failure
At a separate anchor x=1200, form the background, A-only, B-only and AB orbits, with B initially 1200+g. The first nonlinear time T(g) is the least t with nonzero lower-half residual P_AB(t)-P_A(t)-P_B(t)+P_bg(t). The independent local carry engine examines 161 distances g=180,189,...,1620. All 41 distances g=189,198,...,549 have the finite affine renormalization

    T(g+378) = T(g)+608.

This is not an all-distance rule: at g=180 the difference is 605 and at g=558 it is 607. Five independent ordinary base-10 digit-vector simulations verify first nonlinear time and first residual position: g=189 -> (339,1341), g=504 -> (840,1561), g=558 -> (931,1600), g=882 -> (1448,1825), g=936 -> (1538,1863). Each of these four-orbit simulations is nonpalindromic through its collision. The generated 161-row clock has SHA256 d349e2c7df422e114574a1fda56b2f5c94c9ba134622efe8d516e32f403f27f4.

## Certificate interpretation and reproduction
The new constructive mechanism is a phase-locked **front coordinate** in a nonperiodic, expanding packet wake, plus a bounded window of affine scattering delays with countercontrols. A plausible replacement for a whole-packet fixed point is a collision transducer whose finite state includes both the leading-front phase and a regular-language invariant for the full wake, plus the two carry boundaries. A return equation on the frontier alone is insufficient. No such closed infinite decimal transducer is constructed here.

Reproduce the exact trace generation, complete 5001-step ordinary decimal replays, 161 collision events, five independent collision replays, expected SHA256 controls and an intentionally corrupted-trace rejection from the repository root:

    sh calculation/new_structures/agent-W02/run.sh

**Not claimed:** SAT periodic soliton, 20,000-step candidate, all-gaps collision law, infinite decimal Lychrel number, Lean proof, or anything specific about 196. All reported recurrence ranges are *finite*, and hashes are checksum comparisons rather than kernel proofs.
