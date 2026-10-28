# Quadratic local parity/carry charges give no nonzero conserved observable on decimal rec2 bulk

**PAPER PROOF.** For a precisely defined 22-feature, degree≤2 translation-invariant cyclic bulk ansatz, every phase-dependent GF(2) charge satisfying rec2 local covariance is the zero *function*. This neither proves nonexistence of a decimal centre nor constructs a base-10 Lychrel orbit.

## Model and feature basis

Base 10, cyclic 48-cell coefficient word P_j∈{0,...,18} with at least one P_j≠9. The upward and downward carry bits are the unique cyclic solutions `a_(j+1)=[P_j+a_j>=10]`, `d_(j-1)=[P_j+d_j>=10]`. F_g is the exact cyclic bulk pair-word map in `calculation/decimal_frontier/lattice_kinks/agent3_quadratic_parity/model.py`.

At each position j define six Boolean variables `x=P_j mod 2, y=P_(j+1) mod 2, a=a_j, d=d_j, A=a_(j+1), D=d_(j+1)`. The 22 features are `1`, these six variables, and all 15 products of distinct pairs, **summed over 48 cells modulo 2**. This covers all square-free Boolean polynomials of local degree≤2 in this specific width-two variable set. At phase t mod8 choose independent coefficients for all 22 features, 176 coefficient bits total.

Require `C_(t+1)(F_(g_t)(P))=(11 if g_t=1 else 2) C_t(P)` modulo 2 with overflow word 10101010 at all eight rec2 reference rows W_t, every W_t±e_j, and every valid adjacent W_t±e_j±e_(j+1), totaling **2252 tests**. The theorem is that every such C_t is **identically zero** on every P with unique cyclic carries.

## Nine universal identities per phase

All sums below are over j modulo 48, and valued in GF(2). Each is exact for **every** eligible cyclic coefficient word, not only the rec2 rows.

1. `sum 1=0` since 48 is even.
2. `sum(x+y)=0`, `sum(a+A)=0`, `sum(d+D)=0`: cyclic shifts.
3. `sum(x*a+y*A)=0`, `sum(x*d+y*D)=0`, `sum(a*d+A*D)=0`: cyclic shifts of products.
4. `sum(a+d+x*A+y*d)=0`: for even P_j, the map f_j(c)=[P_j+c>=10] is constant, hence a_(j+1)=d_(j-1). Thus (1+x_j)(a_(j+1)+d_(j-1))=0 pointwise. Sum over j and shift the descending index.
5. `sum(a+d+a*A+d*D)=0`: the **carry-run identity**. At every nonneutral P_j≠9 the carry map f_j forces the same fixed bit s_j in both directions; intervals of P=9 propagate that bit unchanged. The ascending and descending cyclic carry sequences therefore follow the same circular ordered list of forced bits, merely placing the transitions at opposite ends of each neutral interval. Hence the number of 1→0 transitions while scanning a_j in increasing j equals **exactly** the number while scanning d_j in increasing j: `sum a_j(1-a_(j+1)) = sum d_j(1-d_(j+1))` as integers. Reduce modulo2 to get the identity.

The nine coefficient masks, in the documented 22-feature order, are `[1,6,40,80,16640,33280,2162688,9240,1179672]`, with GF(2) rank 9. They act independently in each of the eight phases, yielding **72 independent coefficient vectors** representing identically zero observables. Every such vector lies in the kernel of every covariance test.

## Independent 104-row finite rank certificate

The 176-column binary covariance matrix from all 2252 rec2 local tests has rank **104**. More importantly, the committed `rank_witness.json` lists just 104 concrete reference/perturbation tags whose 176-bit row vectors are linearly independent. The primary checker recomputes them using integer cyclic carry equations; an independent checker uses cyclic digit normalization. Both check rank104 on these witnesses and on all2252 tests.

Any charge satisfying those 104 constraints belongs to a kernel of dimension at most `176-104=72`. But the 72 universal zero-function coefficient vectors are independent and lie in that kernel. Therefore the entire kernel is *exactly* their span, and **every** allowed C_t vanishes on *every* eligible cyclic row. This is a sound finite-rank mathematical argument, not an extrapolation from random samples. The 10,000 random physical carry controls are auxiliary.

## Exact scope

No claim about degree≥3 features, nonuniform spatial weighting, neighbourhood beyond j,j+1, nonlocal/temporally nonlocal observables, finite-centre boundary flux, centre nonexistence, or a base-10 Lychrel certificate. This is not Lean-verified. Reproduction and controls: `calculation/decimal_frontier/lattice_kinks/agent3_quadratic_parity/README.md`.
