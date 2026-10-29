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