# W24: 20,000 exact moving-cut pumping steps with an aperiodic spatial band

Label: COMPUTED, not an infinite Lychrel certificate. Builds on AgentW24ComplementDualTwoFront, the source p8/m20 lattice, and the known cut-relocation lemma of AgentN28SlidingCuts. Not a new proof of that cut lemma.

## Pairword relation

Let P_t(q) be the symmetric coefficient word of the *actual decimal integer* after t ordinary reverse-and-add steps from the 9-complement family H_q= (18-B) ++ (18-W)^q, then mirror(H_q), with physical initial digits defined in dual_front.cpp. The first p8/m20 SCC gives |B|=39, |W|=20. q=900 and 901 correspond to 36078- and 36118-digit actual starting integers.

For a symmetric coefficient word P of even/odd length, let I_c(P) insert the lower-side 20-digit coefficient block P[c:c+20] at lower-side position c, and insert its reverse at the reflected upper-side position. (The central pairword between the cuts is left untouched and translated.) This produces a symmetric word of length |P|+40, and the inserted 20-block depends on the actual state P, not on a prespecified eight-phase lattice.

At every t=0..20000 we locate the LONGEST interval [L_t,R_t) in the lower half satisfying P_t(900)[i]=P_t(900)[i+20] for all i there, with i+20 in the lower half. Choose c_t=floor((L_t+R_t)/2). The computation checks the **entire identity**

    P_t(901) = I_{c_t}(P_t(900)).

The checker compares every original lower-half coefficient before c_t, verifies every one of the 20 INSERTED coefficients agrees with P_t(900)[c_t:c_t+20], and compares every original lower-half coefficient after c_t against the longer word translated by 20 positions. Palindromicity of the coefficient words makes these checks sufficient for the full upper mirrored halves, which the insertion operator explicitly preserves. The actual integers are evolved independently on both tracks via schoolbook digit-vector additions AND separately via GMP mpz_class with string decimal reversal, and full integer equality is checked at every step on each track.

## Numerical scope and positive structural mechanism

The q=900/901 pair passed all 20,001 pairword identities and all 40,000 independent track/step arithmetic checks. Both initial and all subsequent 20,000 states had no palindrome. Integer lengths: t=0 36078/36118; t=10000 40229/40269; t=20000 44400/44440. Their length difference stays 40 for every verified time.

The longest period-20 run had minimum size 2732; midpoint cut was always at least 1366 coefficient positions from either edge. At t=0, [L,R)=[35,18019), c=9027; t=5000: [3006,17144), c=10075; t=10000: [5930,16294), c=11112; t=15000: [8873,15410), c=12141; t=20000: [11844,14576), c=13210.

We additionally encode the 20 consecutive *folded pair coefficients* beginning at L_t+30 (always inside the long period-20 run), then take the lexicographically minimal one of its 20 cyclic rotations. Across t=0..20000, all **20001 necklaces are distinct**. Thus this is neither the fixed phase-t%8 lattice insertion from N10 nor a temporal-periodic bulk. It is a FULL-WORD pump with a moving insertion cut inside a temporally nonrepeating period-20 source. This does NOT prove mathematical aperiodicity for all future t, since the computation is finite.

The same method for q=100/101 independently passed all t=0..2500 (2501 states) with a minimum 47-site period-20 run. A further pure digit-vector pilot detects first failure of the midpoint-cut identity at t=2558 when the band collapses; no all-time conclusion follows. The important constructive redirection is to build a finite-state **replenishment rule for a temporally nonperiodic moving insertion domain** rather than insist on an eight-phase stationary bulk or short fixed centre.

## Reproduction

    g++ -O3 -std=c++17 calculation/new_structures/agent-W24/sliding_pump_gmp.cpp -lgmpxx -lgmp -o /tmp/w24pump
    /tmp/w24pump 100 2500
    /tmp/w24pump 900 20000 > /tmp/w24pump20k.json

The C++ file includes the previously committed dual_front.cpp in the same directory for the canonical B/W coefficients, two arithmetic engines, 20-run scanner and FNV hash. Checkpoints are in sliding_pump_20k.json, with 64-bit hashes recorded as integer literals (not floating-point numbers). This is one explicit two-seed finite observation, not a theorem for arbitrary q, not a universal symbolic commutation law, not a claimed palindrome-free infinite decimal orbit, and not a result about the fate of 196. The full checkout verifier was unavailable because GitHub DNS is inaccessible in the computation sandbox; no Lean code is added.
