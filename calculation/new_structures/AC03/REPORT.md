# AC03 centre-only U group m=2
Label: COMPUTED for lengths 7,8; UNDECIDED for lengths 9..14. NOT a decimal Lychrel certificate.

PREDICATE: phase-0 rooted P=H C reverse(H) in LSD-first pair coefficients, H=B34 ++ W9^14 ++ J ++ U^100, J=[5], U=(9,4,14)/(4,14,9)/(14,9,4). C is a palindrome over digits 0..18 of length 7..14; its midpoint is even when length is odd. Physical reverse-and-add runs exactly 120 steps. Required target H' C reverse(H') with H' identical except U^105. The necessary centre window is [400, n120-400). No outer-W9 endpoint comparison or strict-phase W9 pruning enters the census.

SOUND PORT REDUCTION: Run python3 abstract.py. The overapproximating coefficient masks include EVERY centre of the specified length (no mirror correlations needed) and propagate every possible incoming carry and decimal digit residue under each ordinary normalized reverse-and-add. By induction, every physical orbit is included. All 24 U/length combinations yield a SINGLETON carry at the moving left cut s_t=280+t and singleton overflow at t=0..119, specifically the overflow clock (1000)^30. These are universal forced values, not sample observations. Thus centre.cpp's shrinking-window recurrence (trim one coefficient on both sides per step, then account for actual overflow length) exactly computes the entire remaining centre window for each C without assuming persistence of W9 at intermediate phases.

EXACT EXHAUSTIVE CENSUS:
- len7, each U: 10*19^3=68,590 centres, zero central-window returns. Three U: 205,770.
- len8, each U: 19^4=130,321 centres, zero central-window returns. Three U: 390,963.
Combined 596,733 distinct (U,C) candidates, zero central-window returns. Full mismatch histograms in certified_census.txt relative to the final left cut index 400; no strict-phase pruning. Exact status EXHAUSTED-NONE is ONLY for phase0 J=[5], q14/k100 and this necessary centre-window predicate at lengths 7,8.

UNDECIDED sizes for each U: len9=1,303,210; len10=2,476,099; len11=24,760,990; len12=47,045,881; len13=470,458,810; len14=893,871,739. Singleton port/clock does not prove a failed centre return; these are NOT EXHAUSTED.

REPRODUCTION: from calculation/new_structures/AC03 run python3 abstract.py, compile g++ -O3 -std=c++17 centre.cpp -o centre, and for l in 7 and 8 and u in 0 1 2 run ./centre scan l u. Run python3 oracle.py separately. The Python oracle uses genuine arbitrary-precision n += reverse(n) rather than pairword normalization, checks five width pairs (q,k)=(14,100),(20,80),(40,160),(80,320),(160,640), and checks real overflow/palindrome/whole-return/centre first mismatch. Seventy-two independent controlled full pairword trajectories at q14/k100 additionally checked local port and local state at every one of 120 steps. No candidate is promoted to an all-width or all-time return.

EXACT MISSING LEMMA SUPPLIED: a sound all-centres centre-port reduction for all lengths7..14 of this U group, and an exhaustive centre-window non-return decision for the first two lengths. The infinite growing-band return and all-time nonpalindrome guard remain unproved.
