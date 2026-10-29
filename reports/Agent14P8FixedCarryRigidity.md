# Fixed-carry rigidity of the three reachable decimal period-8 non-self-mirror bulk lattices

**PAPER PROOF.** Scope: the three stored periodic **bulk coefficient** schedules rec0, rec1 (spatial period 20) and rec2 (spatial period 48), each with overflow g=10101010. Among integer bases b>=2, base 10 alone supports an 8-phase cyclic bulk having the unchanged complete ascending and descending carry-in itineraries of that stored lattice. Coefficients may vary with b. Different carries, other exteriors, a centre or a decimal Lychrel certificate are not excluded.

Let W[t,j] be the coefficient at bulk spatial column j at time t, modulo m. Let A[t,j], D[t,j] be the ascending and mirrored-descending carries **into** that coefficient. Their cyclic laws are A[t,j+1]=floor((W[t,j]+A[t,j])/b) and D[t,j-1]=floor((W[t,j]+D[t,j])/b), with binary carries. Exact carry normalization and reflection give

    W[t+1,j] = W[t,j] + W[t,j-g[t]] + A[t,j] + D[t,j-g[t]]
               - b*(A[t,j+1]+D[t,j-g[t]-1]).                         (1)

All 704 coefficient edges of the base-10 cases (160+160+384) satisfy (1), with unique cyclic ascending and descending carry itineraries. For a *fixed* itinerary, (1) is affine in b over Q. Write Sx[j]=x[j-1]. Since g has four zeros and four ones, the homogeneous eight-step return map is F=(2I)^4(I+S)^4=16(I+S)^4. Thus H=I-F equals I modulo 2, so det H is odd and nonzero. The cyclic affine solution is **unique over Q** for every b and necessarily has form

    W_t(b) = W_t(10) + (b-10)*alpha_t.                                (2)

The complete initial alpha_0 vectors are stored as exact integer numerators with common positive denominators in agent14_p8_slopes.json. The denominators are 11547965 (rec0/rec1) and 383853808245439899739645498017 (rec2). The independently implemented checker verifies integer recurrences over all eight phases and exact return. The reduced first-coordinate slopes are

    rec0: 21544192/11547965
    rec1: 21490008/11547965
    rec2: 57765677212647727789248476516/127951269415146633246548499339.

Every displayed denominator exceeds 8. For any integer b=2..9, (b-10)*alpha_0[0] is nonintegral. Therefore NO integer coefficients can realize the specified itinerary below base 10.

For b>10, an exact *tight carry-zero* constraint obstructs the unique rational solution. For rec0, at (t=0,j=17), descending carry in=out=0 and W=9 in base 10, while the coefficient slope is 12187782/11547965>1. Consequently W(b)+D(t,j)-(b-1)=(b-10)*(slope-1)>0, contradicting carry out zero for every real b>10. Rec1 has the same translated witness at (t=2,j=12). Rec2 has an ascending witness at (t=0,j=11), carry in=out=0 and W=9, with slope 31062954481448612473362149455/29527216018879992287665038309>1. This excludes all real b>10. Base 10 satisfies all equations, proving the precise rigidity theorem. No state cap occurs.

Reproduce from repository root (standard Python 3 only):

    python3 calculation/decimal_frontier/lattice_formats/code/agent14_fixed_carry_lift.py
    python3 calculation/decimal_frontier/lattice_formats/code/agent14_fixed_carry_independent.py

Inputs: agent14_p8_rows.json (compact snapshot of all three cycles, checked against the existing p8_scc.txt), and agent14_p8_slopes.json (exact rational certificate), both in calculation/decimal_frontier/lattice_formats/. The primary code independently solves a 20x20 or 48x48 system over rational Fractions. The independent checker uses integer arithmetic to validate the supplied slope certificates; both replay every base-10 coefficient edge, not just the stated obstruction sites. The second program additionally reproduces independent existing **positive controls**: base 9 g=1100011000, m=4, |B|=61 and both base 13 g=1010010000 certificates, |B|=75 and 55, by direct 10-step pairword replay from stored certificate files. Those controls are not newly claimed. Neither a rooted base-10 B-cycle nor any periodic centre, actual Lychrel number, or 196 claim is asserted.
