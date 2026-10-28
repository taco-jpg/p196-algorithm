# Agent3QuadraticParityNoGo: exact reproducible finite-rank proof

Python 3 standard library only; all data and code in this commit. From repository root:

```sh
python3 calculation/decimal_frontier/lattice_kinks/agent3_quadratic_parity/verify.py
python3 calculation/decimal_frontier/lattice_kinks/agent3_quadratic_parity/independent_check.py
```

`lat2.txt` is the exact 1.95 KB decimal rec2 coefficient/carry snapshot. `rank_witness.json` lists **104 concrete rec2 row tags** (t,j,s,u) with independent 176-bit covariance vectors. These two compact data files prove finite rank 104 alongside nine explicit universal identity masks in `model.py` and their hand proofs in `reports/Agent3QuadraticParityNoGo.md`. No external packages, SAT solver, hidden data, or cap.

Expected primary output:

```text
PASS: 104 independent finite rec2 test rows; full 2252-row GF(2) rank=104
PASS: 9 independent cyclic identities per phase; 72-dimensional kernel exhausts all 176 coefficients
CONTROL: 10,000 random cyclic words satisfy 9 identities; 8,000 random covariance equations respect 72 trivial identities
PAPER PROOF: every local quadratic parity/carry covariance observable in this basis is identically zero
```

Expected independent:

```text
INDEPENDENT PASS: digit-normalized rec2 covariance rank=104 on 104 witnesses and all 2252 tests
INDEPENDENT PASS: 9 independent identity masks, 72-dimensional zero-function kernel
CONTROLS: 10,000 cyclic rows satisfy even-site carry equality and exact ascending/descending carry-run counts
```

The PAPER PROOF applies to this finite 22-feature basis on all cyclic coefficient rows with unique carries. No physical finite-centre impossibility or decimal Lychrel certificate is inferred.
