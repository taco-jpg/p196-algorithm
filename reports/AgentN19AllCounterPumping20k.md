# Agent N19: Universal two-band counter pumping through 20,000 decimal steps

**PAPER PROOF (conditional on complete finite trace), COMPUTED checks.** Not a Lean proof or an infinite Lychrel certificate.

## Parametric finite-horizon theorem
For every integer k>=15000, take the canonical decimal seed consisting of the digit blocks

    N_k = 9 8^k 59 9^k 80 7^k 20 0^k 1.

For every t=0,...,20000 the iterate of decimal reverse/add is nonpalindromic. Its LSD-first symmetric pairword P_i=d_i+d_(n-1-i) has folded halfword

    H_t(k) = L_t ++ x_t^(a_t+k-15000) ++ J_t ++ y_t^(b_t+k-15000) ++ R_t

where L_t, J_t and R_t are independent of k and are exactly the words in the independently GMP-validated k=15000 reference trace. The bulk clocks repeat every six steps: x=(8,16,14,10,2,4) and y=(16,14,10,2,4,8). The minimum original a_t,b_t are 1820,1786. At t=20000 the invariant junction J_t has length 13183. At t=0, H_0(k)=[10]++8^k++[5,11]++16^k++[8]. These are infinitely many distinct seeds with a fixed **finite** horizon, not one infinite-time certificate.

## Exact soundness lemma (PAPER PROOF)
Decimal reverse/add of symmetric pair coefficients P is computed by carries c_(i+1)=floor((P_i+c_i)/10) and normalized digits o_i=(P_i+c_i) mod10, plus final overflow gamma=c_n. The next pairword is P'_i=o_i+o_(n+gamma-1-i). This arithmetic is deterministic.

The two-ended folded carry transducer from the earlier N19 results (source fold_check.py and unary_allk.py) has 40 states (low carry, high carry, preceding high-side digit). It accepts exactly the folded input/output pairword edges, with parity-specific centre constraints and prescribed gamma. An accepted edge is the exact ordinary decimal reverse/add transition, not an approximate relation.

Suppose a true folded edge contains two disjoint **aligned** paired-column runs (x,x') and (y,y') with Boolean matrices Mx,My; both of positive length. If Mx^2=Mx and My^2=My, inserting q>=0 extra copies of both paired columns preserves the accepted matrix product because M^(a+q)=M^a for every a>=1. Both source and output lengths increase by four q due to mirrored halves, preserving gamma, parity, initial carries and terminal conditions. Therefore the pumped source maps to precisely the pumped target, with no periodicity restriction on intervening junction J. The source and target runs need only overlap at the same column indices; their starts may differ.

In the exact k=15000 reference trace, allq_matrix.py checks for all six phases and both gamma values that both column transition matrices are idempotent (12 temporal/carry cases, two matrices each). For each of the 20000 edges it checks that the source and target left/right bulk intervals overlap in order and away from the centre. Minimum overlaps: 1820 and 1786. Induction on these 20000 sound edges proves the parametric halfword identity and arithmetic orbit for every integer q=k-15000>=0.

All bulk coefficient values are EVEN. The independent digit checker bulk20k_pump_q.cpp verifies that the baseline folded pairword has at least two ODD coefficients at each of the 20001 states (minimum 2). Pumping the even bulk coefficients does not remove these odd witnesses. A palindrome would require each symmetric coefficient to be 2*d_i, hence even. Thus the whole parametric family avoids palindromes throughout the 20000-step horizon.

## Complete reproducibility
Run from repo root:

    bash calculation/new_structures/agent-N19/run_allq.sh

The runner compiles the direct digit-vector base engine, generates all 20001 reference trace rows, checks all 12 matrix/carry identities and 20000 aligned overlaps, then literally evolves the seeds k=15000 and k=15001 through all 20001 states, deleting one extra coefficient from each bulk and comparing the ENTIRE folded pairword; it checks minimum odd count 2. It also runs an independent q=2 finite arithmetic control. Local q=2 and q=7 complete 20000-step arithmetic checks passed. The previous run_bulk20k.sh independently verifies the reference with GMP arbitrary precision, with trace SHA256 0ac6f1d97ed2da30430bd1d8f393918691de847abcf4b678738b27187b297851.

**Limitation:** No replenishment exists in the construction yet; bulk lengths erode. Nothing is asserted for t>20000, for 196, or for an actual infinite decimal Lychrel number.
