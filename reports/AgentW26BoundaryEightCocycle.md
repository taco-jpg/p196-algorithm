# W26 boundary cocycle: two decoupled polynomial coordinates

**COMPUTED**, exact finite scope: the explicitly constructed decimal family in `results/AgentW26FiveTermAffine1024.md`, all k>=111, state times t=0..1024. Each number has a five-term rational polynomial in X=10^(k-111), with exponent support E={0,20,68,116,136}; each polynomial itself is certified for every k by the previous exact canonical normalization and polynomial checker.

Write F_t(X)=a_{t,0}+a_{t,20}X^20+a_{t,68}X^68+a_{t,116}X^116+a_{t,136}X^136. The newly tested partial macro-return is:

    a_(t+8,0) = a_(t,0),
    a_(t+8,136) = 10^4 * a_(t,136),

for all t=0..1016. The checker compares exact Python Fraction values; it is not a fit from floating-point values or observations at finite X. There are 1,017 adjacent eight-step checks, each for both scalar identities, without failure. For each t congruent to r modulo 8 in the covered interval, these give a_(t,0)=a_(r,0) and a_(t,136)=10^(4*floor(t/8))*a_(r,136), by induction along the checked intervals.

The structural meaning is a solved two-coordinate exterior cocycle: one boundary coefficient repeats and the other scales with the four decimal length increases per eight steps. It is compatible with, but stronger in symbolic representation than, the observed 8-step digit-pair clock. The middle coefficients are the remaining interface variables; this is not a closure theorem for the full five-vector, and the equalities cannot be extrapolated beyond t=1024 without an induction hypothesis involving the migrating junction.

**Decisive redirection test.** Let v_j=(a_(8j,e))_(e in E). The 5x5 matrix with columns v_0..v_4 is full rank modulo the prime p=1,000,000,007 after mapping rational coefficients into F_p; the denominators are invertible modulo p. There is a unique matrix M over F_p taking these first five states to the next five (v_0->v_1 through v_4->v_5), but it fails v_5->v_6. Consequently no *fixed rational 5x5 matrix* can implement the complete eight-step update across these six transitions: any such matrix must reduce to the uniquely fitted matrix modulo p because its source matrix is invertible over the localization at p. This does NOT exclude nonlinear, affine-with-hidden-state, phase-dependent beyond modulo 8, or time-varying renormalization. The constructive search is now a two-boundary solved cocycle augmented by an explicit seam-state transducer governing a_{20},a_{68},a_{116}.

Reproduce after running `python3 calculation/new_structures/agent-W26/run_fast.py`: execute `python3 calculation/new_structures/agent-W26/boundary_cocycle.py`; the latter reads the three locally generated binary orbit files, recomputes all five exact rational polynomial coefficients, checks both scalar cocycles and tests the modular matrix. It writes only compact expected JSON. The binary files are scratch data and are intentionally not versioned.

Lean-first next lemma: with a certified affine-word edge and rational coefficient equality, a projection theorem `edge_project_boundary` states the two scalar equalities imply an eight-step projection return for every integer parameter. A finite guarded automaton for the other three coefficients (or a concrete wall-state register) would be required before any infinite palindrome-avoidance conclusion. No Lean compilation was available; no kernel proof is claimed.
