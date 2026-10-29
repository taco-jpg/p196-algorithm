# AC04 centre census and sound outer-centre-prefix pruning

**Labels:** COMPUTED (exhaustive C7/C8; bounded C9..C14 prefix gate), PAPER PROOF (soundness of carry-set overapproximation), UNDECIDED (remaining C9..C14 and the all-time certificate).

**Missing-lemma contribution:** The exact 120-step centre-side fixed-point predicate has a sound necessary condition on the outer centre letters, valid for ALL inner completions; six concrete short-centre slices of that predicate are exhausted.

## Exhaustive short-centre cells

Rooted phase-0 B34/W9, junction J=[5], q=14,k=100; U in {(9,6,12),(6,12,9),(12,9,6)}. Palindromic C has coefficients 0..18; odd midpoint even. Demand 120 genuine decimal reverse-and-add steps with the prescribed actual overflow clock, followed by the identical C and at least 150 coefficients of U on BOTH sides, with U exponent k+5. No strict intermediate W9 condition or odd-centre mod-11 gate is enforced.

| U | C length 7 (odd) | C length 8 (even) |
|---|---|---|
| (9,6,12) | 68,590 / 68,590 tested; zero returns | 130,321 / 130,321; zero |
| (6,12,9) | 68,590 / 68,590; zero | 130,321 / 130,321; zero |
| (12,9,6) | 68,590 / 68,590; zero | 130,321 / 130,321; zero |

**596,733 exact tested candidates, zero endpoint centre-collar returns.** All physical controls have the correct 30/120 overflow clock. First collar mismatches relative to the new centre occur at -46..-39 (U0), -44..-40 (U1), -45..-39 (U2). This excludes only the stated physical reference-width cells. A statement for arbitrary J requires separately checking every hypothesis of the published T12 centre-cone separation. There is NO base-10 Lychrel certificate or general no-go here.

## Sound C7..C14 prefix gate

The overapproximation starts with exact singleton coefficient-value masks on B,W,J,U and mirror flanks, and possible-value masks {0,..,18} on unknown C (odd midpoint restricted to evens). Fix r outer mirrored C positions, allow ALL inner values. At each genuine decimal coefficient step, for every possible current coefficient p and incoming carry c, include normalized digit (p+c) mod 10 and outgoing carry floor((p+c)/10). At the next pairword column include EVERY sum of the possible two reflected digits, deliberately dropping correlations. Induction proves that the resulting masks contain all concrete trajectories. If carry-out or digit length is ambiguous, the engine fails open. A required endpoint collar or fixed-centre coefficient absent from the final set proves that NONE of the palindromic completions of the fixed outer prefix can return. Only the endpoint is tested; temporary W9 damage is permitted.

For EACH length 7,8,9,10,11,12,13,14, with two outer C coefficients fixed and 19^2=361 prefix classes per U, the sound exclusion counts were identical by length:

| U | excluded prefixes | unresolved prefixes |
|---|---:|---:|
| (9,6,12) | 228 / 361 | 133 |
| (6,12,9) | 25 / 361 | 336 |
| (12,9,6) | 82 / 361 | 279 |

All abstract runs had unambiguous expected overflow clocks. For EVEN C length 14 with THREE fixed outer pairs (19^3=6,859 classes), exclusions were respectively 5,237, 1,638, and 2,633, leaving 1,622, 5,221, and 4,226 unresolved. This DOES NOT justify EXHAUSTED-NONE for any C length 9..14.

## Reproduction and independent check

In this directory compile:

    g++ -std=c++17 -O3 -o centre_scan centre_scan.cpp
    g++ -std=c++17 -O3 -o abstract_pruner abstract_pruner.cpp

Then, for each u=0,1,2 and l=7,8, run:

    ./centre_scan u l 999999999 0 14 100 central

To reproduce the abstract gate, for each u and each length 7..14 run:

    ./abstract_pruner u l 2

And for the length-14, three-fixed-letter gate, run:

    ./abstract_pruner u 14 3

The exact scan enumerates 10*19^3=68,590 C7 centres and 19^4=130,321 C8 centres per U; offsets permit disjoint chunks. An independent Python arbitrary-precision integer engine checked EVERY one of 120 steps against schoolbook coefficient normalization on 120 seeded controls: five widths (14,100),(20,80),(40,160),(80,320),(160,640), three U rotations, and all lengths 7..14 = **14,400 individual matching decimal transitions**, with the correct clock. The two scripts are test_crosscheck.py and independent.py.

The unknown C9..C14 classes remain UNDECIDED. Repairing the loss of correlations in the sound abstraction with a relational two-ended carry automaton is the next route. Finite endpoint obstructions are not a proof that any decimal number is Lychrel.

## NEW: all-length symbolic prefix-pumping lemma (PAPER PROOF + COMPUTED)

**Theorem (sound necessary constraint, no upper bound on centre length).**
For the reference rooted phase-0 B34/W9, q=14,k=100,J=[5], and ANY physically realizable palindromic C of ANY length L>=7, let a,b be its first two least-significant-side centre coefficients. The following exact 120-step fixed-C return is impossible for:
- U=(9,6,12): 228 of 361 ordered (a,b) pairs (the sound masked first-mismatch index is new centre-46 for 46 pairs and centre-45 for 182 pairs);
- U=(6,12,9): 25 of 361 pairs (index centre-43);
- U=(12,9,6): 82 of 361 pairs (index centre-44).

Each exclusion holds for EVERY admissible choice of C's remaining coefficients and for BOTH centre parities, independently of centre length. The other 133,336,279 outer pairs are UNDECIDED; this is NOT a no-go for all C and NOT an all-time Lychrel certificate. No W9 strict-phase constraint or fixed overflow assumption has been imposed: the 120-bit clock is derived from the carry masks and certified unique for every case.

**Abstract pumping proof (all L, not tested extrapolation).**
Let A be the set of possible pair coefficients {0,..,18}, D the digits {0,..,9}, and F={0,1} the carry set. For every nonempty carry input subset of F, normalizing A yields exactly digit-mask D and outgoing carry-mask F. Thus the set-valued pairword P=X A^K reverse(X), K>=1, normalizes to dL D^K dR (possibly followed by overflow digit 1); dL is computed from X with incoming carry {0}, and dR from reverse(X) with incoming carry F, BOTH independent of K. Pairing digits across the two ends gives exactly X' A^K reverse(X') on zero overflow and X' A^(K-1) reverse(X') on one overflow, with X' computed from the finite dL,dR and gamma only. If X' ends in a full mask A, move that symmetric trailing pair into the central run to increment K by 2. This canonicalization is equality of masked words and never discards possibilities. Hence the finite sequence X_t is independent of the initial K, and K_t=K_0+delta_t, as long as K_t>=1. The concrete admissible C has initial coefficient word INCLUDED in X_0 A^(L-4) reverse(X_0), where X_0 contains the physical rooted H and fixed a,b; even midpoint of odd C is safely relaxed to A. All admissible L>=7 have K_0=L-4>=3.

**Finite checked part.**
The new code symbolic_all_lengths.py executes this exact symbolic mask recurrence for all 3*19^2=1,083 ordered U/prefix cases through all 120 phases with baseline K_0=3. Every case has min_t K_t>=2 (indeed all have min exactly 2), no ambiguous overflow, and precisely gamma=(1000)^30. A final target left-collar coefficient is ABSENT in 228+25+82=335 prefix cases at the positions above. Because larger K_0 simply adds an unchanged number of A symbols at EVERY phase, the terminal left-side masks and their absent target values are identical for ALL L>=7. This proves an infinite-length necessary gate, not a finite-horizon extrapolation. The code also checks the final collar lies wholly before the right boundary of the symbolic A run.

**Independent physical checks.**
test_symbolic_replay.py chose 20 concrete rejected-prefix completions per U across centre lengths 7..46 (60 cases total). The independent arbitrary-precision ordinary decimal implementation executed 120 steps each and found the predicted specific missing coefficient in the target left U collar in EVERY case. Existing test_crosscheck.py separately checked 14,400 physical decimal steps against the schoolbook normalizer at five (q,k) widths. Run:
    python3 symbolic_all_lengths.py
    python3 test_symbolic_replay.py
The symbolic checker is deliberately a sound overapproximation: a nonrejected prefix does not imply a physical returning centre, and an infinite-length candidate would still need an identical regenerative seam and all-width proof.