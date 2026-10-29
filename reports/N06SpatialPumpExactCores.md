# N06 exact finite-time spatial pumping of the complete evolving core

**COMPUTED**, finite-time renormalisation identity. No all-width theorem or decimal infinite-time certificate is claimed.

Use the explicit decimal seed family N_L defined in reports/N06RenormBufferedP8.md: a 39-column entrance, then L copies of a 20-site p8 spatial block, with the coefficient word mirrored and paired digits split into a positive decimal number. Let P^L_t be the *complete* pairword of its exact integer reverse-and-add orbit at time t. At each step find F_L(t), the first pair-coefficient position that disagrees with the original p8 SCC eight-phase entrance + periodic lattice. This is determined by scanning the actual entire digit expansion; it is not stipulated in advance.

Define the active central halfword C_L(t) = P^L_t[F_L(t) : floor(length(P^L_t)/2)]. The comparison is made in the same physical least-significant-first coordinate system.

**Cross-scale renormalisation identity, observed by exhaustive complete-step replay**: For each of the explicitly tested L in {1,2,10,100,224}, and every integer 0<=t<=10+88L, both
  F_(L+1)(t) = F_L(t)+20,
  C_(L+1)(t) = C_L(t)
hold, with no truncation or masking of the growing central halfword. The two exact integers have digit lengths differing by 40 throughout this interval. At L=224 and t=19,000, the common central halfword comprises **9,068 coefficients**; the full equality at that step is not simply a 161-symbol near-front coincidence.

For each tested L, the first broken full-core equality is exactly t=11+88L; the front-shift equality itself first fails at t=12+88L. Checks: L=1 (99,100), L=2 (187,188), L=10 (891,892), L=100 (8811,8812), L=224 (19723,19724), where each pair denotes the two first failure times. This matches the spatial buffering expectation: one extra 20-site period in the initial seed supplies **88 additional exact evolution steps** with an identical evolving core in the translated coordinate system. The formulas for untested widths remain UNDECIDED.

**Why the translated identity fails:** In the largest test, at t=19,723 the frontiers are F_224=37 and F_225=57. The latter is in the spatially periodic bulk, but the former has crossed into the nonperiodic 39-position entrance. Their central pairwords first disagree precisely at this boundary collision, while the frontier offsets still differ by 20 for that one step. The front offset itself fails next, at t=19,724.

**Independent reproduction:** pump_pairs.cpp implements both orbits in ordinary least-significant-first decimal digit arrays and compares entire central pairword slices at every time. gmp_pump.cpp instead independently steps two GNU GMP arbitrary-precision integers using decimal string reversal, computes the entire coefficients, and compares the same full central slices. Both are run for all listed L by run_pump.sh. The negative control mutates a central decimal digit in N_3, and full-core equality fails immediately at t=0. Exact commands from repository root: bash calculation/new_structures/agent-N06/pump/run_pump.sh. Requires C++17 and GMP; compact observations in pump_observations.json.

**Implication and limitation:** This is a practical finite renormalisation pump: the *whole turbulent core* is invariant under a spatial scale increment of 20 columns, not merely the periodic exterior. It motivates an exact 88-step macro-transducer for the junction of lattice and core, potentially certifiable by a finite set of boundary-carry states. But finite buffer consumption remains; without a new boundary-regeneration rule, this cannot rule out future palindromes for any single finite decimal seed.