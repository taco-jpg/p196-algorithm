# A charge-balanced phase-6 emitter and five-step physical repair in decimal rec2

**PAPER PROOF (all symbolic widths and all future times after merger).** This closes the two-phase physical ingress gap for one explicit repair packet on the period-8, spatial-period-48 rec2 lattice. It does not close a positive-growth centre return, certify an infinite palindrome-free orbit, or prove anything about the literal number 196.

## Exact family

All pairword coefficients are least-significant-first and lie in [0,18]. Let W0 be the pinned 48-symbol rec2 phase-0 lattice and B6=(17,13,14,5,14,4,3,6,10,12,17) its rooted phase-6 prefix. Derive W6 by six cyclic physical bulk transitions with overflow clock 101010; the independent checker derives W6 from six ordinary decimal additions starting at rooted B0/W0. Define V6 by changing ONLY these ten zero-based positions of W6:

    index: 13 14 15 16 18 20 22 23 24 25
    value: 17  8 12 15 15  2  3  0  9  6

For any q>=3, any finite coefficient word C (including empty), and any subset E of {1,...,q-2}, let H_E be B6 followed by q blocks, using V6 at copies in E and W6 otherwise, followed by C. Define the even-length symmetric pairword P_E=H_E ++ reverse(H_E). It is realized by a genuine canonical decimal integer N_E: for every halfword coefficient p use low digit max(p-9,0), reflected high digit min(p,9). Its leading digit is nonzero because B6[0]=17. The 2^(q-2) N_E are distinct.

**Theorem.** For every q,C,E above, all five true overflow bits are 10101; the entire pairword of R^5(N_E) is independent of E; hence the ordinary decimal integer R^6(N_E) is independent of E, and all these orbits coincide for EVERY t>=6. The rooted B6,B7,B0,B1,B2,B3 prefixes contain odd pair coefficients at each t=0..5, so no N_E reaches a palindrome before merger. This says nothing about palindromes after merger.

## Finite carry-port proof for all q

For physical coefficient p, c_out=floor((p+c_in)/10) with c_in in {0,1}. Coefficients <=8 reset carry to 0, >=10 reset to 1, and coefficient 9 passes the entering carry. For overflow gamma the exact two-ended local output is

    Pnext[j] = ((P[j]+a[j]) mod 10) + ((P[j-gamma]+d[j-gamma]) mod 10).

The C++17 primary reconstructs all eight unmodified W phases and five modified phase transitions. Its exact modified-vs-original supports are:

    phase6: 13,14,15,16,18,20,22,23,24,25
    phase7: 20,21,22,23,24,25,26
    phase0: 20,21,22,23,24,26
    phase1: 20,21,22,23,24,25
    phase2: 20,22,23,25
    phase3: empty

At every phase, W and V have identical first and last coefficients and identical ascending/descending carry bits at both block boundaries. Every block resets carries in BOTH directions independently of its entering bit. The maximal cyclic run of coefficient 9 in any of the six original or modified phases is <=2. The primary checker enumerates all eight choices of three adjacent block types and all four external carry-bit assignments at each of the five transitions (160 cases), verifying the ENTIRE central 48-cell output. These are finite transfer identities, not extrapolation from sample q values.

The matching carry ports allow arbitrary concatenations of W/V blocks: each selected block has the checked local output independently of adjacent selected blocks. The first and last unmodified W copies guard the rooted prefix and arbitrary centre C. A disturbance outside the protected interior cannot cross a 48-cell guard within five steps: runs of 9 have length <=2, giving a conservative support expansion <=4 cells per step, hence <20 cells total. The rooted prefix determines gamma=10101 independently of C. Thus every packet is repaired by phase3, simultaneously for every q,C,E. At t=5 the entire symmetric pairword is equal, and one more ordinary reverse-add step depends only on that pairword. Determinism gives equality for all t>=6.

## Why this differs from the existing isolated W23 eraser

At phase0 the new packet contains the known W23 (13,9)-to-(8,14) eraser at indices 20,21, PLUS a four-site shoulder at 22,23,24,26. The complete six-site perturbation has signed alternating sum zero modulo 11, while the isolated W23 eraser has nonzero alternating sum modulo 11 and cannot alone be the image of the preceding g1-to-g0 physical two-step map. The explicit ten-site phase6 source supplies a positive, charge-balanced, physically rooted predecessor. It is non-gauge: differences persist through phases7,0,1,2 before disappearing at phase3. It is NOT an autonomous source, and the packet is consumed rather than regenerated.

## Reproduce and independent controls

From repository root:

    sh calculation/decimal_frontier/lattice_kinks/agent3_phase6_shoulder_eraser/run_checks.sh

The same commit includes primary.cpp, independent_check.py, controls.txt and run_checks.sh. The independent checker does NOT import the primary cyclic carry engine: it derives W6/B6 by six literal ordinary-digit reverse-additions, checks 750 complete six-step trajectories (all interior masks through q=10, randomized C and q=11/12 samples), four separate Python-bigint controls, and a wrong-shoulder negative control. All local checks passed. No Lean or repository-wide verify.py --changed success is claimed because local GitHub shell checkout is unavailable.

**Missing all-time Lychrel lemma:** a 192-step rooted centre interface must re-emit this phase6 packet (or a charge-balanced equivalent), grow a protected band, and restore all carry ports for every independent symbolic length. Without that renewable source this theorem is not a decimal certificate.
