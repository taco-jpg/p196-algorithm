# N28: a four-step erasing decimal particle with independent multi-packet superposition

**PAPER PROOF** (exact four-step local update and arbitrary-multiplicity gluing). **COMPUTED** (128 physical decimal seed variants, additional 40-packet controls, independent arithmetic and 20,000-step replay). No infinite base-10 Lychrel orbit is claimed.

## Local structure

In the least-significant-first symmetric coefficient word P (pair sums of ordinary radix-10 digits), consider an interior periodic bulk w=(5,5,2), and the overflow itinerary gamma=(0,1,0,1) for four steps. Replace a three-position occurrence of (5,2,5) by (7,7,7), with a reflected identical replacement in the right half to retain palindromic P. The residue profiles modulo 9 differ, so this is **NOT** a trivial +/-9 carry-gauge erasure.

The background temporal phases under this gamma itinerary are:
- t=0: (5,5,2);
- t=1: (10,10,4);
- t=2: (5,2,5);
- t=3: (10,4,10);
- t=4: (2,5,5);
- t=5: (4,10,10);
- t=6: (5,5,2).

At defect insertion cut s (s mod3 matched to (5,2,5)), the exact four-step local source/defect windows are:
| t | background, beginning at s | altered, beginning at s | changed positions relative to s |
|---|---|---|---|
| 0 | 5,2,5 | 7,7,7 | 0,1,2 |
| 1 | 10,4,10 | 14,14,14 | 0,1,2 |
| 2 | 2,5,5,2 | 6,10,10,6 | 0,1,2,3 |
| 3 | 4,10,10,4 | 13,1,1,13 | 0,1,2,3 |
| 4 | 5,5,2,5 | 5,5,2,5 | none anywhere |

**Soundness (PAPER PROOF):** Apply the carry-gauge lemma of reports/AgentN28CarryGaugeFunnel.md. At a non-neutral coefficient P_i=x_i+9 z_i with 1<=x_i<=8, the carry out is z_i, independent of the entering carry. Hence inside these bulk windows the exact pairword map is a radius-one cellular update: for gamma=1, Q_i=x_i+x_{i-1}; for gamma=0, Q_i=2x_i+z_{i-1}+z_{i+1}-2z_i. The four steps above involve only coefficients from {1..8,10..17}, so there are no neutral 9 cells or exceptional 0/18 cells in the causal cones. Direct substitution into these two explicit formulas verifies the four table rows. Outside the radius-four causal cone, the two physical pairwords agree, and after t=4 they agree everywhere. This proves the local eraser for any sufficiently separated packets under the stated four-overflow itinerary, independently of the bulk length.

## Rooted, real base-10 seed family

Let B=(8,16^79), W=(5,5,2) and, for integer k>=10M+10, let

    P_k = B ++ W^k ++ [8] ++ reverse(B ++ W^k).

The initial ordinary number splits each symmetric coefficient a into floor(a/2) on its low side and ceil(a/2) on its high side, and places digit 4 at the centre. This is a legitimate nonpalindromic decimal integer of length 161+6k. The exterior B guarantees the **actual** first four overflow bits 0101: the initial leading coefficient is 8 (no length increase); the next is 17 (overflow); the next is 8 (no overflow); the fourth is 17 (overflow). These values are controlled by the first few B digits and absorbing high-side carries, far from the packet sites.

For j=0,...,M-1, select any subset of positions s_j=80+3*(12+10j)+1 in the left W region and make the symmetric replacements (5,2,5)->(7,7,7) there. The positions are 30 apart and at least 20 coefficients away from the edges of W. Their radius-four causal cones are disjoint for all four steps. Therefore every one of the 2^M *distinct initial decimal integers* has the **same entire pairword at t=4**, hence the **same ordinary decimal integer at t=5** (because the next reverse-and-add number is determined solely by the pairword). The four-step local eraser thus gives a genuine arbitrarily extensible **delayed collision mechanism**, not merely a short numerical coincidence. It is not a glider that propagates forever: the perturbations annihilate.

COMPUTED: for k=80,M=7, the 128 variants (packet positions 117,147,177,207,237,267,297) were all replayed through five steps by three mutually checked paths: local coefficient normalization, independent ordinary digit-list reverse-and-add, and independent Python arbitrary-precision integer addition. All 128 share the same entire P_4 and N_5 and are nonpalindromic during these steps. The negative control replacement (7,7,6) does not heal. For k=420,M=40, 30 random choices also matched exactly.

Two extreme seeds (no packets and all seven packets, each 641 decimal digits) were additionally independently replayed for 20,000 steps by replay_int.cpp, an ordinary digit-list-only C++ program. Neither encountered a palindrome; both ended with identical 8,914-digit numbers and FNV-1a low-to-high digit digest 4126939692961530337, with 8,273 length increases. Since all 128 variants coalesced at t=5 and were nonpalindromic before t=5, **all 128 share that finite 20,000-step no-palindrome observation**. No uniform 20,000-step claim for arbitrary M is made.

## Reproduce (self-contained repo)

    python3 calculation/new_structures/agent-N28/particle_eraser.py --emit-dir /tmp
    g++ -O3 -std=c++17 calculation/new_structures/agent-N28/replay_int.cpp -o /tmp/n28_ordinary
    /tmp/n28_ordinary /tmp/n28_eraser_base.seed 20000
    /tmp/n28_ordinary /tmp/n28_eraser_seven.seed 20000

Source and full local table checks: calculation/new_structures/agent-N28/particle_eraser.py. Compact expected controls: calculation/new_structures/agent-N28/particle_eraser_observations.json. No third-party packages.

## Next constructive direction

Seek a **source-and-eraser pair**: a finite carry interface that periodically emits the (7,7,7) packets into the (5,5,2) bulk, followed by the four-step annihilator. This can renew a finite moving joint without indefinitely increasing a static reservoir, which is the missing ingredient for a true decimal certificate.
