# All cubic local parity/carry covariance observables vanish on decimal rec2 bulk

**PAPER PROOF**, with two independent standard-library checkers. This is a complete negative classification of a narrowly defined GF(2) function class, **not** an all-width centre nonexistence result.

## 1. Function class and exact finite constraints

The decimal period-8, spatial-period-48 rec2 cyclic bulk has overflow word `10101010` and eight coefficient rows `W_t`. For a cyclic 48-cell pair-coefficient word `P_j in 0..18`, excluding the all-9 neutral word so carries are unique, let `a_j` and `d_j` be actual cyclic ascending and descending carry bits satisfying `a_(j+1)=[P_j+a_j>=10]` and `d_(j-1)=[P_j+d_j>=10]`. The exact cyclic pair-word update is `F_g`, as independently implemented by both checkers.

At spatial position j form the six bits `(P_j mod 2, P_(j+1) mod 2, a_j, d_j, a_(j+1), d_(j+1))`. Take the XOR over all 48 positions of each of the **42 square-free monomials of total degree ≤3** in these six bits: constant 1, 6 variables, 15 quadratic products and 20 cubic products. A phase-t observable `C_t` is an arbitrary GF(2) linear combination of those 42 translation-invariant feature sums. The eight phases have independent coefficients, so 336 unknown bits.

Require `C_(t+1)(F_(g_t)(P))=(11 if g_t=1 else 2)C_t(P)` modulo 2 on each reference row `W_t`, all admissible one-site perturbations `W_t ± e_j` and adjacent-pair perturbations `W_t ± e_j ± e_(j+1)`. There are precisely **2252** such tests (same set as the completed degree≤2 result, but a strictly larger feature space). The theorem: **every solution defines the zero function on every eligible cyclic word**, at each phase.

## 2. Universal identities from a 76-state carry graph

The graph's 76 vertices are triples `(P_j,a_j,d_j)` with `P_j in 0..18` and carry bits `a_j,d_j in {0,1}`. An edge from `(p,a,d)` to `(q,A,D)` is valid exactly when `A=[p+a>=10]` and `d=[q+D>=10]`. There are **1444 valid directed edges**. The six-bit local feature vector is determined by the edge, and every genuine cyclic coefficient word with its physical cyclic carries traces a directed 48-edge closed walk.

The committed deterministic generator finds **13 linearly independent feature masks** `m_k` and for each constructs a 76-vertex Boolean potential `phi_k` plus one constant `c_k` satisfying the **finite exact identity on every one of the 1444 graph edges**
`<m_k, feature(edge)> = phi_k(source) + phi_k(target) + c_k (mod 2)`.
Summing over any closed 48-edge walk makes both potential sums telescope and the constant term vanish (48 is even). Thus **all 13 feature masks define identically zero charges for every eligible cyclic word**, independent of random sampling and centre width. They have GF(2) rank 13; placing them separately in each of eight time phases gives 104 linearly independent, universally zero coefficient vectors.

The masks are discovered deterministically from 250 seeded random cyclic words, but the randomness is not trusted in the proof: the generator explicitly verifies all 13 graph identities on *every* edge and checks their independence. A separate program uses a different digit-level algorithm and validates all 1444×13 equations again.

## 3. Finite rank upper bound

The primary checker reads the 2252 rec2 test tags in deterministic order and greedily collects **232 independent 336-bit covariance row vectors**. It emits their concrete tags in the generated compact `certificate.json`. The independent checker independently reconstructs all 232 rows from schoolbook cyclic digit normalization, uses a different pivot convention, and obtains rank **232**.

Therefore any coefficients satisfying the covariance tests lie in a kernel of dimension at most `336-232=104`. But the 104 universal zero-function coefficient vectors from the graph are linearly independent and each satisfies every covariance equation. Consequently the kernel has dimension **exactly 104**, and contains only identically zero observables. No nontrivial degree≤3 local invariant in this precise ansatz exists.

## 4. Reproduction and limitations

Under `calculation/decimal_frontier/lattice_kinks/agent3_cubic_parity/` the commit includes the raw rec2 1952-byte data snapshot, source-code feature/row generator, rank-and-graph certificate generator, and independent digit-normalization checker. Both programs pass; the primary also checks 10,000 random cyclic rows, and the independent program 2,000 words ×8 phases, solely as controls. Exact commands and expected output in README. No external solver, hidden data or state cap; small generated certificate (<5 KB) is reproducible from the committed input.

**Not claimed:** higher-degree, larger-neighbourhood, spatially nonuniform or nonlocal observables; a no-go for a genuine finite-width centre of any size; a base-10 Lychrel certificate; or Lean verification.
