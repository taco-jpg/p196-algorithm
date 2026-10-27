# Agent 7 / T1.canonical-quotient: deterministic maximal-trim cycle theorem

Classification: **PAPER PROOF** + independent **COMPUTED** finite audit.
**NOT LEAN-VERIFIED**. No base-10 cycle, decimal Lychrel existence
result, or all-period impossibility result is claimed.

Source: Agent120.Neutral.Hyp, nextB, nextC, edgeOK, cycleOK
(lean/P196/Drafts/Agent120NeutralBandCalibration/).
This is the precise soundness statement behind the previously
informal "maximal trimming WLOG" claim in neutral_band_search.py.
It builds on the full arbitrary-base neutral-padding proof at
[agent-7] draft PR #315 and review issue #301.

## Setup

Fix b>=2, h=b-1, and a Hyp-valid interface (B,C).
On any accepted cycle, all centers C are symmetric because nextC
is symmetric and deleting matching end runs preserves symmetry.
A center entirely h is invalid, as neutral runs transmit the
incoming carry rather than flipping it.

Normalize by removing every trailing h from B and every paired
outer h from C. Write N(B,C)=(E,D). E is empty or ends non-h.
D is nonempty, symmetric, and begins/ends non-h.

Define the canonical successor T on normalized valid pairs:
compute raw R=nextB(b,E,D) and S=nextC(b,E,D); strip the entire
trailing h-run from R (length U), and every symmetric pair of
outer h coefficients from S (V pairs). The resulting pair is
T(E,D), when it is Hyp-valid. All-neutral S cannot be a valid
center in a returned cycle; classify such a successor as invalid.

**Theorem (PAPER PROOF), every b>=2:**

1. Any nonempty accepted cycle of the general, possibly
   nonmaximally trimmed, cycleOK checker projects under N to
   a closed orbit of the SINGLE-VALUED deterministic T.
2. Conversely, any nonempty closed T-orbit through Hyp-valid
   normalized interfaces reconstructs checked edgeOK edges
   and is accepted by cycleOK. Its sumGain >= sumGam condition
   follows automatically from length conservation.
3. Hence existence of any cycleOK certificate is equivalent
   to existence of a valid T-cycle. Neither direction
   establishes existence in decimal or absence at all widths.

## Proof: projection and unique trimming

The arbitrary-padding conjugacy theorem of PR #315 yields new
nonnegative trims on an existing cyclic chain:

    U_i = u_i + q_(i+1) - q_i >= 0
    V_i = v_i + a_(i+1) - a_i >= 0,

where q_i is B_i's maximal trailing h depth and a_i is C_i's
maximal symmetric h-pair depth. Carry bits, overflow bits,
transition equalities, sum u and sum v are preserved.
The empty normalized E_next case is covered: |nextB(E)|=|E|+gam
and E=[] forces gam=1; thus raw nextB(E) is never empty,
which prevents any negative reconstructed U.

After normalization, the raw B equality is

    nextB(E_i,D_i) = E_(i+1) ++ h^U_i.

Since E_(i+1) ends non-h or is empty, U_i MUST equal the
entire length of the trailing neutral run. Trimming less
leaves an h at E_(i+1)'s end, and trimming more fails equality.

The raw center equality is

    nextC(E_i,D_i) = h^V_i ++ D_(i+1) ++ h^V_i.

Since D_(i+1) is nonempty, symmetric and begins with non-h,
V_i MUST equal the maximum number of neutral end *pairs*.
Trimming less leaves paired h; trimming more fails equality.
There is no spurious erasure of an odd isolated h coefficient.
Therefore every normalized source has exactly ONE successor,
the canonically trimmed T(E_i,D_i), establishing direction (1).

## Proof: converse, gain and degenerate cases

Every step of T explicitly computes nextB/nextC and legal
maximal neutral run removals, so reconstruct the corresponding
Edge(B,C,B2,C2,U,V). Hyp validity and these exact equalities
give edgeOK. A closed T-orbit gives a closed edge list and a
nonempty cycleOK chain.

The raw exterior length is |B|+gam, after trim |B2|=|B|+gam-U.
The raw center length is |C|+gam, after symmetric trim
|C2|=|C|+gam-2V. Sum each identity cyclically to obtain

    sum U = sum gam,     2 sum V = sum gam.

In particular sum gain = sum(U+V) >= sum gam, satisfying the
last condition of cycleOK without an extra search constraint.
This applies to E=[] and to odd-length centers; a nonexistent
all-neutral valid center is never admitted.

## Independent finite arithmetic audit

Run from repository root:

    python3 calculation/agent-7/canonical_quotient.py

The source is independent Python digit arithmetic, not an import
of neutral_band_search.py. Enumerate each base b=2..5, B width
0..2, symmetric C width 1..4, all coefficients 0..2(b-1),
and EVERY legal (not necessarily maximal) pair of trims U,V.
Compare each legal edge after normalization to the uniquely
computed successor of the normalized source.

Exact local output:

    All-trim quotient: PASSED sources=10564 edges=11222 nonzero_trims=2830

The script independently replays the existing Lean-source
base-26 four-phase positive certificate: canonical phases
(gam,U,V)=(0,1,0),(1,0,0),(0,1,1),(1,0,0), with
sum gam=2, sum U=2, sum V=1. These are existing source
certificates; the new T-equivalence is not Lean-certified.

A finite passing audit does NOT prove the arbitrary-width
PAPER identity and cannot exclude unseen decimal cycles.
The theorem justifies deterministic normalized graph search,
with all resource caps/unknown growth kept UNDECIDED.
A future base-10 candidate still requires complete edges,
mirror replay, a kernel-checked theorem and verify.py PASS.
