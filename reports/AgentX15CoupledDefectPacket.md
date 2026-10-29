# Agent X15: compensated inner-band packet and finite-horizon pumping

**COMPUTED** (independent ordinary-decimal and pairword replays through 20,000 steps), plus a **PAPER PROOF** finite-horizon all-q reduction conditional on N10's published universal one-step lattice insertion lemma. Not Lean-verified. NOT an infinite base-10 Lychrel certificate.

## Explicit new decimal construction

Coefficients are least-significant first, encoded 0..9,A..I for 0..18. Adopt N16/N18's rooted p8/m20 lattice with B0=H501D4EC98FGHDH9144B8G09EB9B6DI947HF97D (length 39), W0=H31DHBE3I12073ECF97D (length 20), gamma_t=1 for even t and 0 for odd t. Use U of forty 1s with U[13]=7,U[20]=7,U[30]=4,U[33]=3,U[34]=4,U[38]=8,U[39]=3, and C=[8,0,0]++U++[16]++reverse(U)++[0,0,8], an 87-coefficient palindromic centre. The known N18 control instead has U[13]=7,U[20]=7,U[30]=6, all other entries 1.

For any integer q>=6 construct the symmetric pairword P_q=B0++W0^q++C++reverse(W0)^q++reverse(B0). At lower-half indices 129,132,135,145 +20(q-6), replace the coefficients and their mirror partners by 9,18,0,1, respectively. This is a four-site defect packet within the inner two periodic bands. Every coefficient stays 0..18, midpoint 16, and each pair is split as digits low=min(9,p), high=p-low (midpoint p/2), yielding a valid positive decimal seed N_q. The source implements this literal rule.

## New computed mechanism and failure point

The stand-alone C++ checker compares at EVERY iteration (i) genuine GMP decimal reverse/add, (ii) independent ordinary grade-school decimal digit-list reverse/add and (iii) full pairword carry normalization; palindrome, unexpected overflow, and integer/digit/pairword divergence cause failure. It also checks phase-B_t exterior prefixes.

At q=6 and t=352 the fourth-return W-target at site 139 has 17/20 mismatches for the original N18 centre, 14/20 for X15's centre-only edit, and 13/20 for that centre with the four-site packet. The centre-only pairword prefix agrees through two W sites; the packet has zero matching sites at that specific inner target, even though total mismatches are fewer. The packet does NOT give a fourth renewal.

The four-site packet moves leftward through the protected lattice: q=6 phase-correct matching-prefix lengths at t=88,176,264,352 are 109,89,69,49, a deficit of precisely 20 per 88-step block. q=7 gives 129,109,89,69. N18 already reported an 88-step -20 glider; we claim only the new *coupled four-site packet / adjusted centre* and its quantitative fourth-return effect, NOT discovery of that velocity.

At q=245, 20,001 consecutive genuine integers t=0..20000 are all nonpalindromes; digit length 9,965 -> 19,965, first phase-B failure NONE, minimum entire matching B_t+period-W_t prefix =364 pair-coefficients (at least 16 whole 20-cell bands beyond B), and FNV64 over (matching prefix, decimal digit length, phase) = cca7f290777fdfd9. Fourth-return site 4919: 13 mismatches. Independently q=246 gives 10,005 -> 20,005 digits, 20,000 steps, minPrefix384, FNV64 7c692254ff423566. This is a positive finite family with a nonperiodic centre/packet; it is NOT a self-reproducing infinite certificate.

## Sound finite-horizon pumping (PAPER PROOF conditional on N10)

Let F be exact coefficient-pair reverse/add. For each phase t, let I_t insert W_t at position 39 after B_t and insert its reversal symmetrically at the right. Suppose a checked finite trajectory P_0,...,P_H satisfies P_{t+1}=F(P_t), has the B_t+W_t prefix (and mirror) for every 0<=t<H, and contains an odd B_t coefficient. N10's universal one-step lemma says F(I_t(P_t))=I_(t+1)(F(P_t)) for any core whenever this rooted guard is present. An induction on t, then k, yields F^t(I_0^k(P_0))=I_t^k(P_t) for all k>=0 and 0<=t<=H. An odd B_t coefficient remains, so none of these finite trajectories contains a palindrome.

The exact q245 computation supplies every finite hypothesis with H=20000 and prefix>=364>59. Thus **for every q>=245**, this particular explicit decimal construction has at least 20,000 nonpalindromic reverse-add steps, with matching phase prefix >=364+20(q-245), assuming N10's separately published paper lemma. This is finite-time pumping only; no induction in unbounded time t is claimed. The q7 finite replay similarly supplies the all-q>=7 statement for H=352.

## Reproduction and search provenance

g++ -std=c++17 -O3 calculation/new_structures/agent-X15/packet_replay.cpp -lgmpxx -lgmp -o /tmp/x15_packet
/tmp/x15_packet 6 352 0
/tmp/x15_packet 6 352 2
/tmp/x15_packet 6 352 1
/tmp/x15_packet 7 352 1
/tmp/x15_packet 245 20000 1
/tmp/x15_packet 246 20000 1

Variants: 0 is the unmodified N18 reference, 2 is the centre-only X15 edit, 1 is centre+packet. Exact outputs in observations.json. The modifications were obtained by a bounded, nonexhaustive soft-residual coordinate search, not by ILP/CP-SAT, and do NOT prove optimality or exclude longer centres. A 49,920 two-site scan and 59,000 three-neighbor tests preserving three prior renewals found no fourth return; those exploratory negative scans are not standalone results. Known carry-gauge degeneracies were discarded (N28). The required full repository verify.py --changed was unavailable in this tool container (GitHub DNS/Lean checkout absent); the C++ source itself compiled and passed independent tests. No Lean source is added.

Credits: N16/N18 for the rooted exterior and three-renewal centre, N18 for -20 glider motion, W05 for a distinct all-q 264-step mechanism and q230 20,000-step decimal control, N10 for the insertion commutation lemma, N28 for gauge equivalences. The new X15 contribution is a specified *coupled four-site inner-band pulse* with alternate centre, 13-versus-17 residual, and the independent q245/q246 20,000-step actual-integer family. A true certificate would still require a regenerative packet or growing shield rule rather than adding a finite passive guard.