# All-modulus obstruction for 48-component carry corrections on the rec2 cyclic row map

**PAPER PROOF.** This classifies a complete 48-parameter family of additive descending-carry corrections across *every modulus*. It does not prove nonexistence of a decimal periodic centre or a Lychrel number.

## Cyclic model and covariance requirement

Fix base 10 and a 48-cell cyclic coefficient word P with digits 0..18. Let a_j(P), d_j(P) denote the unique cyclic ascending and descending carry solutions

`a_(j+1)=[P_j+a_j>=10]`, and `d_(j-1)=[P_j+d_j>=10]` (indices mod 48).

For overflow g=0 or 1 the bulk cyclic row map F_g is exactly

`F_0(P)_j=2P_j+a_j+d_j-10(a_(j+1)+d_(j-1))`,

`F_1(P)_j=P_j+P_(j-1)+a_j+d_(j-1)-10(a_(j+1)+d_(j-2))`.

The rec2 coefficient rows W_t satisfy `F_(g_t)(W_t)=W_(t+1)`, t modulo 8, with g=10101010. The unique cyclic carry solutions exist for every row used below.

For modulus M>=2 and arbitrary **time-independent** alpha_j in Z/MZ (48 independent coefficients, no spatial-period restriction), define

`C_alpha(P) = sum_(j=0..47) 10^j(P_j+alpha_j d_j(P)) (mod M)`.

The proposed *exact cyclic-bulk covariance* is `C_alpha(F_0(P))=2 C_alpha(P)`, `C_alpha(F_1(P))=11 C_alpha(P)`, required at each reference W_t and at every admissible single-site modification W_t+epsilon e_j with epsilon=±1 and coefficients remaining between 0 and 18.

## Tiny exact arithmetic obstruction

For a given P and g, the defect `E_g(P)=C_alpha(F_g(P))-A_g C_alpha(P)` is affine-linear in the alpha_j. Subtracting the base-row equation from the corresponding one-site-perturbed equation gives the following **integer identities** for all alpha (no modular reduction yet):

1. At phase t=0 (g=1), adding 1 at spatial position 47 changes E by `-(10^48-1)` and has **zero coefficient of every alpha_j**.
2. At t=0, adding 1 at spatial position 2 changes E by `10 alpha_1` with zero constant.
3. At t=1 (g=0), adding 1 at spatial position 2 changes E by `-990-30 alpha_1`.

Both original and perturbed rec2 rows use the unique physical cyclic carry solutions. The primary script computes these identities from the raw digit coefficients and carries; the independent script derives every row map using digit normalization rather than the algebraic recurrence.

For all six relevant equations to hold modulo M, (1) implies `M|(10^48-1)`. From (2) and (3), `10 alpha_1=0` and `-990-30 alpha_1=0`, hence `M|990`. The exact Euclidean computation gives `gcd(10^48-1,990)=99`. Therefore `M|99`, regardless of all 48 freely selected alpha_j.

Conversely, whenever M divides 99, set every alpha_j=0. Then `C_0(P)=sum 10^j P_j`; weighting the two cyclic row equations by 10^j cancels ascending carries exactly and descending carries by the factor `1-10^2=-99`. The cyclic wrap is valid since `10^48=1 (mod 99)`. Hence `C_0(F_0(P))=2 C_0(P)` and `C_0(F_1(P))=11 C_0(P)` for every cyclic coefficient word with unique carries, and in particular all specified rec2 rows and perturbations. This proves the **if and only if** theorem for all M>=2.

## Scope and controls

The theorem excludes moduli 37, 101, 9999 and every modulus not dividing 99 **only for this constant-vector bulk covariance ansatz**. A phase-dependent correction, physical finite-window boundary source, nonlinear observable, or non-periodic centre might obey an entirely different law. No centre existence/nonexistence or infinite reverse-and-add orbit is inferred.

Reproduce with the exact snapshot and standard-library primary and independently implemented digit-normalization checker in `calculation/decimal_frontier/lattice_kinks/agent3_vector_covariance/`. They check all 8 rows × 48 cells, all three witness differences, and 2,400 randomized cyclic source-law controls for M=3,9,11,33,99. No Lean source or unverified Lean claims are added.
