# W09: a delayed six-phase decimal bulk refill over 60 steps

COMPUTED: An explicit base-10 reverse-and-add seed with a 60-coefficient cap achieves a positive +6 homogeneous-centre width gain after 60 steps, despite losses during intermediate steps. Two independent arithmetic engines check 20000 actual integer operations; every state is nonpalindromic and its central pairword contains a nonempty exact six-phase uniform block. This is NOT an infinite decimal Lychrel certificate or a Lean result.

## Exact seed
The initial least-significant-first pairword is L ++ 8^(2k) ++ reverse(L) with L the sixty entries in calculation/new_structures/agent-W09/renew60/cap.csv. Realize p as low digit floor(p/2), upper digit ceil(p/2). In most-significant-first ordinary decimal notation:
N_k = 116306872642729707615958232967841904794691524521087889888578 ++ 4^(2k) ++ 864887887780025415096487409047668232759515706816235167603511.
For k=22000, the initial decimal length is 44120.

## Universal 60-step template family
For every k>=80, and t=0..60, the entire pairword has exact shape A_t ++ x_t^(2k+beta_t) ++ reverse(A_t), with x_t cycling 8,16,14,10,2,4. The entire finite cap A_t is independent of k, and every A_t contains an odd coefficient. This finite-horizon parameter statement follows from the centre-insertion carry lemma in reports/AgentW09TransientCoreReplenishment.md and the exact finite reference computations: an interior homogeneous even coefficient stabilizes its carry, symmetric central insertion commutes with normalization/pairing, and the k=80 reference retains more than six homogeneous central cells in all 61 stages. Independent genuine Python integer replays at k=80,81,100,150 confirm the complete cap equalities, safety guards and 60 step offsets.

| t | width offset beta_t | outer cap length |
|---:|---:|---:|
| 0 | 0 | 60 |
| 6 | -4 | 63 |
| 12 | -2 | 63 |
| 18 | -3 | 65 |
| 24 | -3 | 66 |
| 30 | -2 | 67 |
| 36 | +4 | 65 |
| 42 | 0 | 68 |
| 48 | -3 | 71 |
| 54 | -7 | 74 |
| 60 | +6 | 69 |

The payoff is delayed and non-monotone. The number of decimal digits increases by 24 after 60 operations, exactly accounting for +6 core plus two times +9 cap cells. Since A_60 != A_0, this is a transient positive refill, not a period-60 certificate. The missing recurrence condition is full cap state return, not merely a positive width budget.

## Independent long replay
The already committed W09 direct byte-digit engine and separate base-1000 big-integer engine now accept an optional CSV cap argument. Defaults are unchanged, preserving their prior control. The first engine directly adds low-first base-10 digits; the second repeatedly renders a canonical base-1000 integer to decimal, reverses its decimal representation, parses that into new limbs, and adds by base-1000 carries. Neither infers its next integer from the asserted pairword format. Both check every stage for palindrome and the prescribed central uniform letter, and the reproducer compares checkpoint lines and independent FNV64 hashes exactly.

For k=22000: t60 homogeneous width 44006; t1000 43406; t5000 40760; t10000 37445; t20000 30891. Final 52329 digits, 8209 overflows, zero palindromes, no core-shape failure, LSD-first FNV64 262683335058ed77. The complete checkpoints and source are shipped.

## Reproduce
From repository root:
sh calculation/new_structures/agent-W09/renew60/reproduce.sh

This compiles both independent C++ integer engines, checks ordinary Python integers for k=80,81,100,150 through t60, and compares the two full 20000-step outputs to the committed checkpoint file. The heuristic provenance source is search60.cpp, with seeded RNG and optional argument 160000; it is not part of the proof and the witness is checked without trusting the optimizer. The finite-state universal core insertion theorem and conditional nonnegative-prefix resource-cycle criterion were established in the preceding W09 report; no such closed cap cycle has been found.

No repository-wide tools/verify.py --changed or Lean verification was available in this sandbox; only the stated local arithmetic checks are claimed.
