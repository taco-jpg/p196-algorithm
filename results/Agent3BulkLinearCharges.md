# Agent3BulkLinearCharges

**PAPER PROOF.** For any base b>=2, cyclic bulk period m>=1 and modulus M>=2, the additive linear charges whose coefficients cancel independently variable ascending/descending carries in both overflow cases are exactly q[i]=b^i z (mod M) with (b²-1)z=(b^m-1)z=0 (mod M).
Their number is gcd(M,b²-1) for even m, gcd(M,b-1) for odd m. Their update multipliers are 2 (overflow 0) and b+1 (overflow 1).
For base 10, rec2 spatial period 48 and overflow 10101010, this class contains only mod-9 ordinary-sum and mod-11 alternating-sum information; every rec2 bulk row has zero charge modulo 99.
Scope: *cyclic bulk and formally independent carry streams only*. Does not classify physical carry correlations, finite-centre boundary terms or nonlinear invariants, and does not exclude any centre width or establish a decimal certificate.
Proof: reports/Agent3BulkLinearCharges.md.
Executable checks: python3 calculation/decimal_frontier/lattice_kinks/code/agent3_charge_invariants.py.
