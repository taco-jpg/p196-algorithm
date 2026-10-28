# All-modulus obstruction for scalar descending-carry corrections on decimal rec2

**PAPER PROOF.** This is an exact classification for a narrow bulk-weight ansatz across **every** modulus. It is neither a centre nonexistence theorem nor a certificate in base 10.

## Data and definitions

Take the published decimal period-8, spatial-period-48 rec2 lattice with overflow word `10101010` from `calculation/decimal_frontier/lattice_kinks/data/lat2.txt` (a copy is included in the calculation subdirectory of this result). Let `W_t[j]` be its 48 coefficient values at temporal phase t, j=0,...,47, and let `d_t[j]` be the unique cyclic descending carry satisfying `d_t[j-1] = [W_t[j]+d_t[j] >= 10]` (indices modulo 48).

Set the exact **integers**
`Q_t = sum_{j=0}^{47} 10^j W_t[j]` and
`D_t = sum_{j=0}^{47} 10^j d_t[j]`.
The candidate family for modulus M>=2 consists of single, time-independent scalars `alpha in Z/MZ` satisfying all eight equations `Q_t + alpha D_t = 0 (mod M)`.

## Theorem and proof

**Theorem.** Such an alpha exists if and only if M divides 99, and when it exists its unique value is 0 (mod M).

Suppose an alpha exists. Multiply the t=i equation by D_j, the t=j equation by D_i, and subtract. Every 2x2 minor `Delta_ij = Q_i D_j - Q_j D_i` must vanish modulo M. In particular `M | Delta_01` and `M | Delta_12`.

Exact arithmetic from the eight finite rows yields
`gcd(Delta_01,Delta_12)=99`, hence `M | 99`. The same rows give `gcd(Q_0,...,Q_7)=99`, so for every such M, choosing alpha=0 satisfies all eight equations. Finally, `gcd(D_0,D_2)=1`; when Q_t=0 modulo M the equations imply `alpha D_0=alpha D_2=0`, and Bézout forces `alpha=0` modulo M. This completes the classification for **all positive moduli M>=2**, without any state cap or statistical inference.

The independent checker reconstructs the descending carries by a separate reverse-cyclic method; it checks the carry recurrence, verifies the two determinant witnesses, and tests all M<=10,000 in a second modular linear-equation implementation (the latter is a regression only; the theorem is infinite).

## Scope and interpretation

For example, no single alpha gives simultaneous cancellation in all eight rec2 phases modulo 37, 101 or 9999. The only permitted moduli are 3, 9, 11, 33 and 99 (excluding trivial 1). This **does not** rule out a phase-dependent scalar, an array of spatial carry weights, an observable involving both carry streams, or a nonlinear invariant. It says nothing about real central carry correlations, periodic centres of any width, or 196.

The precise finite control runs, raw data and independent checker are described in `calculation/decimal_frontier/lattice_kinks/agent3_scalar_charge/README.md`. No Lean files are added.
