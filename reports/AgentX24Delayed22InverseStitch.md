# Agent X24: delayed 22-step inverse stitch, base 10

**Label: COMPUTED** for exact finite inverse checks and 20,000-step double-engine ordinary-decimal replay. This is neither a Lean proof nor an infinite Lychrel certificate.

## Seeds and exact scope

Use the rooted p8/m20 pair-coefficient exterior B0,W0 from the existing X24 packet_replay.cpp. For any integer r define two symmetric pairwords with the same outer blocks B0 ++ W0^r and their reversals but distinct palindrome centres:

A_r centre [17,6,5,2,11,11,2,5,6,17].
B_r centre [8,15,18,13,5,5,13,18,15,8].

Realize each coefficient p by the LSB/MSB digit pair floor(p/2), p-floor(p/2). All digits are valid; each has a nonzero most significant digit.

Direct Python arbitrary-precision integer calculations checked the first equality R^22(A_r)=R^22(B_r), with strict inequality for every 0<=t<22, for r in {1,2,3,4,10,50,234}. This is a set of **seven tested band counts**, not a claim for every r. In the r234 long replay, two independent implementations check the full 22-step merger anew, and none of the pre-merger states is palindromic.

## Discovery scope

The code depth_sweep.cpp uses an exact pair-coefficient normalization and folding update. Its exhaustive width-4 test covers all 19^4=130321 centre halfwords for 30 updates, finding first numerical merger depths 2,3,4,5,6,7,8,10,11,12,14. Its deterministic width-5 sample covers 200000 of 19^5=2476099 halfwords for 80 updates (stride 104729, offset 1234567 modulo the candidate count), finding depths 2,3,4,5,6,7,8,9,10,11,12,14,15,16,18,20,22. The width-5 sample is **not exhaustive**, and neither set excludes later mergers.

## Independent 20,000-step test

For r=234 both seeds have exactly 9448 decimal digits. Compile delayed_replay.cpp, which reuses the first X24 C++ implementation via a source include. It compares GMP mpz_add against separately implemented positional decimal addition at each of the 20000 transitions from seed A, and separately checks both seeds for the 22 initial transitions. Each of the 20001 states on the A trajectory was checked for palindromicity and against the prescribed period-eight B cap plus the W band. Zero palindromes; at least six whole period-20 bands were intact at *every* step, with the last length 19448 digits. The second seed shares the entire orbit after t=22. Checkpoint values and hashes are in calculation/new_structures/agent-X24/delayed22_20k.log.

Reproduce:

    cd calculation/new_structures/agent-X24
    g++ -O3 -std=c++17 delayed_replay.cpp -lgmp -o delayed_replay
    ./delayed_replay 234 20000
    g++ -O3 -std=c++17 depth_sweep.cpp -o depth_sweep
    ./depth_sweep 4 2 30
    ./depth_sweep 5 2 80 200000

## Remaining gap

This is **finite delayed synchronization**. Once the states merge at t=22, the inverse choices have no effect on the future. The surviving external lattice still erodes. No infinite nonpalindromic orbit or self-renewing centre is inferred.
