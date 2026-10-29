# SAT-synthesized coalescing and rebounding decimal packet (agent-N05)

**COMPUTED** in base 10. A finite positive construction showing a non-injective defect evolution combined with reversible-looking *spatial* packet compression/re-expansion, not a true infinite reversible recurrence. No Lychrel certificate.

## Exact construction and claims
The underlying spatial lattice is the period-12 overflow schedule gamma 100010001000, period-9 absorbing bulk W_t, temporal phase t=7, and source position x=1008. The seed construction is independent of SAT: take B0 width34, append 3000 bulk coefficients, cap symmetrically with [0,0], then reverse, realize as ordinary decimal integer, take seven reverse-and-add steps, and replace symmetric pairword coefficients at x..x+3 by either:
- source A [17,8,0,2] (only first three coefficients differ from the lattice),
- source B [17,3,10,6] (four differ).
Realize each as a different positive decimal 6072-digit integer.

An independent local carry transfer computes these changed-site supports, with offsets relative to x:
```
time   A occupancy   A changed support       B changed support
 0         3             [0,2]                   [0,3]
 1         3             [0,2]                   [0,3]
 2         4             [0,3]                   [0,3]   same coefficients
 3         5             [0,4]                   [0,4]
 4         5             [0,4]                   [0,4]
 5         5             [0,4]                   [0,4]
 6         3             [3,5]                   [3,5]
 7         3             [3,5]                   [3,5]
 8         4             [1,4]                   [1,4]
 9         4             [1,4]                   [1,4]   values [2,17,13,16]
10         5             [1,5]                   [1,5]
```
The three-cell packet at steps6..7 has sharply repaired its previous five-cell wake, and then returns to four cells shifted +1 at steps8..9. Not shape-periodic; no permanent glider.

A stronger direct integer fact: despite different positive seeds N_A != N_B, their full pairwords (not merely the bulk window) are **exactly identical at step 2**, so `N_A(3)=N_B(3)` as ordinary decimal integers. Two full independent big-int evolutions confirm N_A(0..2) != N_B(0..2). Coalesced step-3 decimal length is 6073 digits; SHA256(decimal representation) `bbab72318986afcd3547b2070214e20861e947e18a38bc3561cd12d36c921ea4`.

## SAT and independent verification
For source A, impose the 9-step exact two-sided carry QF_LIA update from `sat_glider.py` over x=990..1037 with the 12-phase lattice entering carry. Pin only p(0,1008)=17 and p(0,1009)=8; allow remaining two source coefficients freely in [0,18]. Constrain the time-9 defect to translate +1 and occupy a width4 interval, with a genuinely changed target left endpoint. Z3 produces A=[17,8,0,2]. `sat_h9_rebound.py` independently replays all nine local transitions, asserts two-step coalescence with B and the exact support trajectory, and compares the terminal pairword against the decoded SMT model.

The independent ordinary decimal arithmetic script `integer_collision.py` proves equality of complete pairwords at step2 and equality of numbers at step3, with zero palindromes for the shared next 997 steps. Each source also separately passes `phase_packet.py` over 1000 full-integer steps: 250 overflows, all prescribed gamma bits, zero palindromes, exact local pairwords. This is a concrete finite-time mechanism, not proof of infinite avoidance.

## Exact reproduction
```sh
python3 calculation/new_structures/agent-N05/sat_h9_rebound.py
python3 calculation/new_structures/agent-N05/integer_collision.py
python3 calculation/new_structures/agent-N05/phase_packet.py --steps 1000 --band 3000 --x 1008 --phase 7 --patch 17,8,0,2
python3 calculation/new_structures/agent-N05/phase_packet.py --steps 1000 --band 3000 --x 1008 --phase 7 --patch 17,3,10,6
```
Only the SAT script needs `libz3.so.4`; the others need Python 3. A candidate for next research is to couple this non-injective two-to-one junction with its own temporal/spatial phase copies to obtain return paths, rather than search only for same-width deterministic packets.
