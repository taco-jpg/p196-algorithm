# N06 finite co-moving 161-site decimal glider

**COMPUTED** only; a new positive mechanism with a measured breakdown, not a Lychrel proof.

Build N_225 by the exact constructive digit split in reports/N06RenormBufferedP8.md. Its complete decimal reverse-and-add orbit was independently replayed by two methods through 20,000 steps in the preceding result. The pairword of each integer is symmetric, with coefficient P_t(i)=d_i+d_(n_t-1-i).

Let E_t(i) denote the original p8 SCC eight-phase entrance of length 39 followed by its 20-site spatial periodic lattice. At each time t, F(t) is the first coefficient index i at which P_t(i) differs from E_t(i); this frontier is calculated from the **entire** digit expansion, not from an assumed slope. Let M_w(t) be the w pair coefficients P_t(F(t)),...,P_t(F(t)+w-1), encoded as 0..9,A..I.

**Constructive glider observation**: for the exact seed N_225, every integer time t=2000..19722 (17,723 starting times) satisfies BOTH:
(1) F(t+88)=F(t)-20, and
(2) M_161(t+88)=M_161(t).
The minimum common motif length over all these 17,723 checks is **161**, so width 161 is not just an average. Since 88 is a multiple of the 8-phase temporal period and 20 is the spatial SCC period, this is a co-moving finite-time macro-state. The entire 161-symbol neighbourhood translates left 20 columns per 88 iterations, while both time and number length advance. The motifs are genuinely nonconstant and include coefficients 0..18.

**Where it breaks**: At t=19723, the two 161-symbol motifs disagree at their very first symbol. The first frontier is F(19723)=57, and 88 steps later F(19811)=37, still a shift of -20. The translated position now falls inside the nonperiodic 39-site entrance, which is exactly where the periodic-domain model ceases to apply. This is a boundary collision; there is no evidence that the central region repairs it. At t=20000 the original eight-column exterior invariant still holds, but it fails at t=20028.

**Independent arithmetic check**: The new gmp_glider.cpp regenerates all N_t using GMP arbitrary-precision addition and decimal reversal, calculates each pairword directly from decimal strings, finds its matched frontier, and compares a 240-column neighbourhood with the state 88 steps earlier. It independently reports 17,723 comparisons, zero frontier failures, zero 161-symbol motif failures, minimum full match 161, and first break t=19723 with frontiers 57 and 37 and zero common symbols. Cross-check: the earlier independently authored digit-vector frontier.cpp reports zero front-shift failures in its original interval, and the separate digit-vector orbit checker also reports the correct seed/checksums.

Run from repository root: bash calculation/new_structures/agent-N06/glider/run_glider.sh. Requires C++17 and GNU GMP development files. Reference checks and snapshots in glider_observations.json.

**Soundness limitation and next construction**: A 161-symbol co-moving equality verified over a finite 17,723-time interval is not a closed 88-step macro-edge. A true renormalisation certificate must prove its matching interface is insulated from the unknown wake for all future iterations and must prevent the moving front from colliding with the outer entrance. Search for a boundary-reflecting or regenerating front, not another short-centre exclusion.