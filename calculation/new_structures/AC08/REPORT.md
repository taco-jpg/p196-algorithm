# AC08 phase-0 centre-only census (2026-10-29)

**COMPUTED** finite centre exclusion, and **PAPER PROOF** specialisation of the previously known mod-11 parity gate. **NOT an all-time decimal Lychrel certificate.**

Rooted p12/m9 reference q=14,k=100, B34/W9 phase 0 from lattice_kinks/data/lat_p12m9.txt, fixed J=[5]. U group m=7 is (9,14,4), (14,4,9), (4,9,14). Enumerate all palindromic coefficient centres C of lengths 7 through 9, with 0..18 coefficients and an even midpoint for odd length. The exact predicate requires the 120-step *physical decimal reverse-and-add* orbit to equal the target U^(k+5) centre on radius 122+|C|+30 about the midpoint, with identical J, W9 exponent and centre. No strict intermediate-W9 rule is imposed.

| U | length 7 (simulated) | length 8 (simulated) | length 9 (mod-11 pruned) | length 9 (simulated) | endpoint matches |
|---|---:|---:|---:|---:|---:|
| (9,14,4) | 68,590 | 130,321 | 1,184,729 | 118,481 | 0 |
| (14,4,9) | 68,590 | 130,321 | 1,184,730 | 118,480 | 0 |
| (4,9,14) | 68,590 | 130,321 | 1,184,729 | 118,481 | 0 |

**Exact completed cardinality: 4,506,363 centres** (3 x (68,590 + 130,321 + 1,303,210)). Of these, **3,554,188** were excluded by the sound congruence and **952,175** underwent 120 full physical-digit iterations. No simulated case had an incorrect 30-overflow clock or growth count; no central endpoint fixed point was found.

## Sound endpoint-only mod-11 lemma

Let A(X)=sum_i (-1)^i X_i for LSD-first coefficient words. For any n-digit N, rev(N) is congruent to (-1)^(n-1)N mod 11. Therefore reverse-and-add of an even-length number is divisible by 11; once divisible, all subsequent numbers remain divisible. The canonical phase-0 source has outermost pair coefficient B[0]=10, which forces the first step to overflow. If |C| is odd, that step makes the source's odd digit count even, hence N_2 is divisible by 11. If |C| is even, N_1 is divisible by 11. Thus EVERY genuine N_120 is divisible by 11, regardless of any later carry/clock changes.

For an odd palindromic C, at q=14,J=[5],k+5=105 the returned pairword satisfies A(P_target)=10-2A(U)+A(C) mod 11. Divisibility of N_120 implies divisibility of its pairword value N_120+rev(N_120), so **A(C)=2A(U)-10 mod 11 is NECESSARY** for an endpoint return. Pruning by this condition is sound even when W9 is temporarily damaged and later repaired. Even palindromic C has A(P_target)=0 identically and is never pruned.

For TWO consecutive identical-J/C returns, k moves 100→105→110: the second target has even k, requiring A(C)=10 mod 11. Hence 2A(U)-10=10 mod 11, so A(U)=10 mod 11. The three U alternating sums are -1,19,9. Consequently **odd palindromic C of ANY length cannot give two identical-C consecutive returns for U=(14,4,9) or U=(4,9,14)** in this fixed-J rooted phase-0 family. This is an application of the existing general parity gate, not a novel global obstruction. Even C remains open.

## Independent checks / exact limits

The C++ enumerator performs true LSD-first decimal digit addition with separate input/output buffers; the Python verifier uses unbounded integers and string digit reversal independently. 24 centre/rotation examples at each of q/k=(14,100),(20,80),(40,160),(80,320),(160,640) agreed on central mismatches and the 1000 repeated 30 times overflow clock. 168 additional centre examples were pointwise compared with the original C++ enumerator; 2,700 algebraic substitutions agreed with direct target alternating sums. These are sample controls, not an independent exhaustive repeat of 4.5 million tests.

Lengths **7,8,9 are EXHAUSTED-NONE** for this *specific necessary centre-window predicate*, conditional on the canonical source and fixed J=[5]. Lengths **10,11,12,13,14 remain PARTIAL/UNDECIDED**, with per-U full cardinalities 2,476,099; 24,760,990; 47,045,881; 470,458,810; 893,871,739. Neither a width-independent T12 lifting proof nor a non-palindrome/all-time certificate follows from these finite tests. Do not conflate this with the entire U-group for arbitrary J and centre lengths.
