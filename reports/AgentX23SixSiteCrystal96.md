# Agent X23: synchronized spatial-six / temporal-96 decimal kink crystal

**Label: COMPUTED; scope is finite-horizon arithmetic and a bounded, exact bulk census, NOT existence of a decimal Lychrel number.**

## Exact six-site bulk census

Represent the least-significant-first pair coefficient row as (a,b,c,c,b,a), with a,b,c in 0..18 and not all 9. There are 19^3-1 = 6,858 starts. For each phase of the alternating overflow schedule gamma=(10)^infinity, apply the exact cyclic forward/backward carry map F_gamma described in `reports/AgentX23DistributedKinkCrystal18.md`, generalized to spatial period six. The complete finite enumeration is `ring6.cpp`; reproduce with `g++ -O3 -std=c++17 ring6.cpp -o ring6 && ./ring6`.

Every one of the 6,858 starts is followed for at most 2,000 transitions (phase and all six coefficients included in the seen-state key). Exactly 6,854 enter a periodic functional orbit without entering the neutral all-9 row; the other FOUR enter this row, where a cyclic carry is not uniquely determined by the periodic bulk and this checker deliberately stops without asserting a unique orbit. For the 6,854 uniquely defined trajectories, minimal eventual periods and counts are 2:18, 6:1636, 12:222, 18:3000, 24:10, 36:1572, 96:396. All numbers count initial reflection-symmetric triples, not distinct cycles or reachable rooted exteriors. They sum to 6,854. The four neutral arrivals remain outside this classification.

## Positive period-96 crystal and 20,000-step replay

Choose the nonuniform six-site row R0=(18,12,6,6,12,18). Its *bulk* trajectory closes with minimal temporal period 96 **without transient** under gamma=101010..., and there are 48 overflow steps per period. This jointly synchronizes with the existing eight-phase, spatial-20 exterior. Define P0=B ++ W^400 ++ R0^2500 ++ reverse(R0^2500) ++ reverse(W^400) ++ reverse(B), where B and W are the 39 and 20 coefficients in `crystal96.cpp`. It has 46,078 decimal positions, with thousands of spatially distributed interior kink cells.

Realize N0 as a positive integer from P0 by setting the i-th most significant digit to min(9,P0_i) and the opposing digit to P0_i-min(9,P0_i) for i below the midpoint. Reproduce the genuine integer trajectory:

`g++ -O3 -std=c++17 crystal96.cpp -lgmpxx -lgmp -o crystal96 && ./crystal96 400 2500 20000`.

At each t=0..20,000, independently calculate the full next pairword by coefficient normalization and the full actual N_t by GMP decimal-integer reverse-plus-add; require exact pairword agreement at **every position**; reject any palindrome; enforce gamma alternating, the B exterior eight-phase recurrence, the W20 bulk prefix, and an R6 centre suffix against the independent cyclic-carry prediction. All assertions pass. At t=20,000 there are 56,078 decimal digits, with W prefix 3,465 and six-site crystal suffix 7,498; their minima across the entire run equal these terminal lengths. `crystal96_checkpoints.csv` gives intermediate checkpoints.

## Obstruction and next target

The interfacial span between the last proven W20 coefficient and the first proven R6 centre-suffix coefficient is 0 initially and 17,037 at t=20,000 (28,039 - 7,498 - (39+3,465)). Thus simultaneous temporal synchronization does **not** imply a closed microscopic seam. The missing piece is a finite 96-step transducer that either reabsorbs the growing interface into one of the two bulk species, or carries a translating bounded-width interface with certified outer/inner wall alignment. No such transducer is exhibited. The four neutral bulk arrivals also remain separate from the unique-carry census.

This work does not verify every decimal seed, prove survival past t=20,000, or prove an infinite base-10 orbit. No Lean files are introduced; the full repository verifier could not run without a network-accessible checkout, although both standalone programs compiled and completed all stated checks.
