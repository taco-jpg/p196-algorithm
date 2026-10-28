# Time-variable pair multipliers and carry vectors cannot escape modulus 99 on rec2 cyclic bulk

**PAPER PROOF.** Complete all-modulus theorem for a specified local cyclic-bulk covariance ansatz. It is not a nonexistence theorem for periodic decimal centres or a base-10 Lychrel certificate.

## 1. Model and claim

For each 48-cell coefficient word P with digits 0..18, let a_j(P) and d_j(P) be unique cyclic upward and downward carries satisfying
`a_(j+1)=[P_j+a_j>=10]`, `d_(j-1)=[P_j+d_j>=10]` (indices modulo 48). The row update is

`F_0(P)_j=2P_j+a_j+d_j-10(a_(j+1)+d_(j-1))`,
`F_1(P)_j=P_j+P_(j-1)+a_j+d_(j-1)-10(a_(j+1)+d_(j-2))`.

Use eight rec2 rows W_t in the committed `lat2.txt`, `g_t=10101010`, and `F_(g_t)(W_t)=W_(t+1)`. Require exact covariance on every W_t and every one-site W_t±e_j remaining in 0..18, using actual cyclic carries.

For any M>=2 permit beta_0=1, seven arbitrary beta_1,...,beta_7 modulo M, and **384 independent** alpha_(t,j) modulo M:

`C_t(P)=sum_(j=0..47)10^j(beta_t P_j+alpha_(t,j)d_j(P)) (mod M)`.

Demand `C_(t+1)(F_(g_t)(P))=(11 if g_t=1 else 2)C_t(P)`. Such coefficients exist **if and only if M divides 99**.

## 2. Seven exact perturbation equations

Subtract covariance at the reference row W_t from that at W_t+s e_j. The two independently implemented checkers both obtain these exact integer coefficient equations:

- For t=0,1,2,3 at j=0, s=-1, descending carry inputs/outputs do not change, so
  `11(beta_1-beta_0)=0`, `2(beta_2-beta_1)=0`,
  `11(beta_3-beta_2)=0`, `2(beta_4-beta_3)=0`.
- t=0, j=47, s=+1:
  `(10^47+1)beta_1-11*10^47 beta_0=0`, with no alpha terms.
- t=2, j=5, s=+1:
  `11*10^5(beta_3-beta_2)+10^4 alpha_(3,4)=0`.
- t=3, j=5, s=+1:
  `-79*10^4 beta_4-2*10^5 beta_3-2*10^4 alpha_(3,4)=0`.

The arithmetic identities are exact over the integers before reduction modulo M. Only these seven equations are needed.

## 3. All-modulus elimination

The t0 equation `11(beta_1-1)=0` and t0 j47 equation imply

`0=(1-10^48)beta_1+11*10^47(beta_1-1)`,

hence `(10^48-1)beta_1=0`. Since `11|(10^48-1)`, also `(10^48-1)(beta_1-1)=0`. Subtracting yields `10^48-1=0 (mod M)`. Therefore M is odd and coprime to 10.

Cancel the factor 2 in the t1 and t3 equations to obtain `beta_2=beta_1` and `beta_4=beta_3`. Twice the t2 j5 equation plus t3 j5 eliminates alpha_(3,4):

`0=10^4(200beta_3-220beta_2-79beta_4)=10^4(121beta_3-220beta_2)`.

But `11(beta_3-beta_2)=0`, so the last expression reduces to `-99*10^4 beta_2=0`. Because `beta_2=beta_1` and `11(beta_1-1)=0`, we obtain `99*10^4=0`. Cancel 10^4 to conclude `M|99`.

Conversely if M|99, set all beta_t=1 and all alpha_(t,j)=0. The cyclic weighted coefficient sum `sum 10^j P_j` obeys F0 multiplier 2 and F1 multiplier 11 modulo 99, since ascending carries telescope, descending carry coefficients carry factor `1-10^2=-99`, and cyclic wrap uses `10^48=1 mod 99`. This holds for every admissible row, hence satisfies all stated tests. Thus existence is **equivalent** to M|99.

## 4. Scope and reproduction

This result includes the exact rec2 snapshot, a primary checker of all seven integer equations, a separate digit-normalization checker, positive controls on every rec2 phase and admissible one-site perturbation for M=3,9,11,33,99, and 2,400 independent random cyclic updates. Commands and expected output in `calculation/decimal_frontier/lattice_kinks/agent3_phase_beta/README.md`. The exploratory 9,592-prime scan through p=100,000 is not the proof; these seven equations prove the result for **all M** with no cap.

Not claimed: spatially variable P weights, nonlinear/nonlocal charges, finite-centre boundary dynamics, any centre-width nonexistence, a decimal Lychrel certificate, or Lean verification.
