# Agent3VectorCarryCovariance: complete independent reproduction

All required inputs are included in this one commit. Python 3 standard library only, no external packages, no hidden sandbox scripts, no state cap.

From the repository root:

```sh
python3 calculation/decimal_frontier/lattice_kinks/agent3_vector_covariance/witness.py
python3 calculation/decimal_frontier/lattice_kinks/agent3_vector_covariance/independent_check.py
```

Expected main output:

```text
PASS: 8/8 physical cyclic rec2 bulk steps, 384 row cells and both carry streams
Witness A: phase0 cell47+1 gives zero vector coefficient and bare=-(10^48-1)
Witness B: phase0 cell2+1 (bare=0, coeff[1]=10); phase1 cell2+1 (bare=-990, coeff[1]=-30)
gcd(10^48-1,990)=99; allowed moduli are divisors of 99
```

Expected independent output:

```text
INDEPENDENT PASS: modulo-normalized row-map witness, gcd 99, 2400 random cyclic control steps in M=3,9,11,33,99
```

The primary checker uses exact integer carry recurrences; the independent one uses modular digit normalisation and reconstructs both periodic carry streams without importing any source from the primary. The 1.95 KB `lat2.txt` is a self-contained exact snapshot of the existing rec2 input. The theorem is about a specified cyclic **bulk** correction family, not a finite-width centre census or a decimal Lychrel certificate.
