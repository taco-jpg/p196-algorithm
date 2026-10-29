# W02 base-10 nested pulse clock: three exact episodes in 40,000 actual decimal additions

## Scope and new positive mechanism
**COMPUTED.** This result continues the phase-locked p12/m9 packet frontier discovered in `AgentW02P12BallisticFront` and the 20k nonpalindromic family in `AgentW02P12PulseTrain20k`. Here the new phenomenon is **three** repeated exceptional six-cluster patterns whose interarrival gaps grow by an exact multiple of the front period on the observed horizon. This is strictly stronger data than the earlier two-episode 20k report; no all-time periodicity is presumed.

Construct three 100,000-digit ordinary integers with the least-significant-first palindromic pair coefficient word defined by B2=(2,11,1,6,8,1,7,15,9,3,9,4,7,9,10,16,9,11,4,10,8,8,9,11,11,7,4,3,9,12,1,1,9,11) followed by the 9-site p12/m9 phase-2 period W2=(1,10,8,5,9,16,0,9,11) to half-width 50,000 and reflected. The two packet integers replace the 11 pair-coefficient sites anchored at x=13998 and their mirror with A=(6,1,0,1,11,14,10,6,11,16,1) or B=(16,0,9,11,1,10,8,5,14,18,0). Split each pair coefficient P into low digit P-min(9,P) and reflected high digit min(9,P), so all three are actual canonical decimal integers. The anchor is spatially congruent to the earlier 5997 anchor modulo 9, so the physical perturbations have the same local lattice phase but much longer safety buffers.

An independent C++ ordinary decimal-digit vector engine computes N+reverse(N) for all three starting integers at every t=0..40000, checks all **120,003** states nonpalindromic, and checks full lower-half defect-word FNV64 hashes against a separate local pairword carry engine at every state (80,002 full hash comparisons), plus each pair of support endpoints and the two rightmost coefficients. All checks passed. Final length is 110,000 digits. The generated 40,002-line trace has SHA256 `3942215a5ebadbbc45f1712aa263ef7f24f84411330cd343d8b613ceb25ee3e7` and its corruption is rejected by the independent checker.

## Exact finite-horizon moving-edge and timing grammar
Let R_X(t) be the last lower-half pair coefficient differing from the unperturbed reference, and Q_X(t) the actual pair coefficient at R_X(t)-1. For every t=337..39924, R_A(t+76)=R_A(t)+33; for every t=155..39924, R_B(t+76)=R_B(t)+33. These are checked on ordinary integer trajectories; the bulk's (76,33) diagonal covariance is an independent finite 12x9 table identity.

Define a second-cell glitch at t if `Q_X(t+76)!=Q_X(t)`, only for 500<=t<=39924. The exact set of glitch times splits into consecutive clusters.

- A has **38** clusters, each exactly length 3, all starts congruent 30 mod 76, arranged in **19** adjacent twin clusters separated by exactly 76 steps.
- B has **70** clusters: 64 length3 and six length4. Excluding 18 clusters in its three exceptional six-cluster episodes, the other 52 clusters are exactly **26** twins of length3, starts congruent 6 mod76.
- Three exceptional episodes begin at steps **941, 18573, 39093**. In each, the six cluster-start offsets relative to the episode origin are exactly **(0, 5, 53, 76, 81, 129)**, with consecutive-cluster lengths **(3,4,3,3,4,3)**. The episode-start spacings are 17632=232*76 and 20520=270*76, whose difference is **2888=38*76**.

One can extrapolate a quadratic formula from three data points, but that is NOT a mathematical consequence and the fourth episode remains UNDECIDED. The 40k evidence supports a **phase-labelled recurrent event shape plus a nonconstant clock**, not a global fixed point, not a full-packet return, and not a long-term finite automaton proof. The sparse exceptional events are a more precise obstruction to collapsing the wake to its rightmost one or two coefficients.

## Reproduction and limitations
From the repository root, run `sh calculation/new_structures/agent-W02/run_40k.sh`. It compiles and runs `front_trace_40k.cpp` and the independently written `independent_decimal_40k.cpp`, validates the SHA256 of the regenerated 40,002-row trace, checks the complete ordinary-number trajectories and every full halfword-difference hash, runs `pulse_check_40k.py` to assert the exact 70/38 clusters, all phases, twin-spacing and three six-cluster episodes, and mutates one trace datum to ensure the checker rejects it. Expected results in `pulse_expected_40k.json`. No external fixture, untracked source or third-party Python package is required; the C++ compiler and Python3 suffice.

**Not claimed:** an infinite decimal orbit, finite certificate, periodic full wake, proof that pulse clock spacings continue, Lean verification, or any conclusion about 196. The proof obligation for a true certificate is closure of *all* coefficients and two-sided carry boundary states, not merely the scalar frontier or three timing episodes.
