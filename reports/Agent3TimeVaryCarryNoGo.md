# All-modulus obstruction to eight-phase time-varying vector carry corrections on rec2

**PAPER PROOF.** A complete characterization for a 384-coefficient, time-dependent additive correction family on the decimal period-8, spatial-period-48 rec2 **cyclic bulk**. This does not establish anything about the existence of a real periodic centre or a decimal Lychrel orbit.

## Set-up

Let the rec2 rows W_t (t modulo 8) and overflow schedule g=10101010 be those in the copied `lat2.txt`. For any cyclic length-48 coefficient row P with entries 0..18 and unique cyclic carries, define ascending a_j and descending d_j by `a_(j+1)=[P_j+a_j>=10]`, `d_(j-1)=[P_j+d_j>=10]`, spatial subscripts modulo 48. The exact cyclic pair-word row maps are

`F_0(P)_j=2P_j+a_j+d_j-10(a_(j+1)+d_(j-1))`;

`F_1(P)_j=P_j+P_(j-1)+a_j+d_(j-1)-10(a_(j+1)+d_(j-2))`.

On the eight rec2 rows, `F_(g_t)(W_t)=W_(t+1)`; these and the three perturbed rows below have unique physical cyclic carry solutions.

For arbitrary modulus M>=2 and **independent coefficients** `alpha_(t,j) in Z/MZ` for t modulo 8 and j modulo 48, set

`C_t(P)=sum_{j=0}^{47}10^j(P_j+alpha_(t,j)d_j(P)) (mod M)`.

Require `C_(t+1)(F_(g_t)(P))=A_t C_t(P)`, where A_t=11 for g_t=1 and 2 for g_t=0, on *every* W_t and all admissible one-site W_t±e_j. The same alpha_(t,j) must be used across these tests, but may depend arbitrarily on phase and spatial position.

## Three exact short witnesses (necessary condition)

Let `E_t(P)=C_(t+1)(F_(g_t)(P))-A_t C_t(P)`. For a one-site perturbation at position j, denote `Delta_(t,j)=E_t(W_t+e_j)-E_t(W_t)`. Computing the exact integer coefficients of all 384 alpha symbols from the cyclic row maps gives:

- `Delta_(0,47) = 1 - 10^48`, with **no correction coefficients**.
- `Delta_(2,5) = 10^4 alpha_(3,4)`, with zero constant.
- `Delta_(3,5) = -99*10^4 - 2*10^4 alpha_(3,4)`.

The latter two give `2 Delta_(2,5)+Delta_(3,5)=-99*10^4`, with every correction coefficient cancelled even though it is allowed to vary with temporal phase. These arithmetic identities are exact over the integers and are independently checked by the two committed implementations, one of which computes the successor by digit normalization rather than by the displayed algebraic formula.

The required covariance at both reference and perturbed rows forces every Delta to vanish modulo M. Hence `M | (10^48-1)` and `M | 99*10^4`. Because `gcd(10^48-1,99*10^4)=99`, necessarily `M|99`.

## Sufficiency and scope

For every M dividing 99 choose `alpha_(t,j)=0` for all 384 entries. Then `C_t(P)=sum 10^j P_j` is time independent. Multiplying the exact row formulas by 10^j and summing cancels ascending carries, and the descending carry coefficient is a multiple of `1-10^2=-99`; the spatial wrap uses `10^48=1 mod 99`. Thus `C_(t+1)(F_0(P))=2C_t(P)` and `C_(t+1)(F_1(P))=11C_t(P)` for every admissible cyclic row. This proves the *if and only if* statement for all moduli, not merely 37 or 101.

A fixed multiplier `10^j` on P, a cyclic spatial bulk and universal local one-site covariance are essential assumptions. Time-dependent weights on P, nonlinear or nonlocal corrections, finite-centre boundary flux, and actual full-template reachability are **not** excluded. No finite-width centre census, decimal certificate or Lean proof is claimed.

Reproduction (standard Python 3 only): run both scripts in `calculation/decimal_frontier/lattice_kinks/agent3_timevary_carry/` as documented in README. Controls include all eight rec2 phase transitions, exact witness coefficient vectors, and 2,400 random cyclic row steps across M=3,9,11,33,99. The 1.95 KB lattice data snapshot is in the same commit.
