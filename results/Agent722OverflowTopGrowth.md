# Agent722OverflowTopGrowth

**PAPER PROOF** (every integer base b >= 2). Let B be a nonempty canonical neutral-band exterior block of length n, with coefficients in [0,2b-2], B[0] != 0, B[-1] != b-1. Its forward carry is e in {0,1}. Let gamma be the final carry from normalizing reverse(B) with incoming carry 1-e. If gamma=1, then canonical nextB has **exactly n+1 coefficients** and its forward carry is **1-e**.

Proof: The untrimmed nextB at gamma=1 is zipAdd(DB ++ [(b-1)(1-e)], [1] ++ reverse(DR)), so its last coefficient is z=(b-1)(1-e)+((B[-1]+1-e) mod b). If e=0, the last B coefficient lies in [0,b-2], hence z lies in [b,2b-2]. If e=1, its non-neutral last coefficient has residue modulo b in [0,b-2], hence z lies in [0,b-2]. Thus z != b-1 in either case, so no trailing neutral coefficient can be removed; moreover normalizing nextB from zero has final carry 1-e, regardless of its incoming carry at the last position.

If gamma=0 the untrimmed nextB has length n, hence the canonical nextB has length at most n. Consequently **an overflow cannot occur at any maximum-width phase of a periodic canonical B-cycle**. Writing u_t for the number of stripped trailing neutral coefficients gives |B_(t+1)|-|B_t|=gamma_t-u_t, gamma_t*u_t=0, and sum_t u_t=sum_t gamma_t over every period.

Scope: the canonical Agent120 neutral-band B-system with e2=1-e1; no conclusion about absorbing/lattice exteriors, centres, existence of a base-10 Lychrel number, or an actual orbit of 196.

Independent checks: python3 calculation/decimal_frontier/exterior_census/py/agent722_top_overflow.py (482,648 exhaustively enumerated canonical words, bases 2..11, widths 1..4; 15,000 independent ordinary-integer reverse-and-add checks). No Lean file is added.
