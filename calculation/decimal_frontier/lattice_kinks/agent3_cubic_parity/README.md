# Agent3CubicParityNoGo: exact finite-rank/graph reproduction

All required data and checkers are committed together. Requires Python 3 standard library only. From the repo root:

```sh
python3 calculation/decimal_frontier/lattice_kinks/agent3_cubic_parity/verify.py /tmp/agent3_cubic_certificate.json
python3 calculation/decimal_frontier/lattice_kinks/agent3_cubic_parity/independent_check.py /tmp/agent3_cubic_certificate.json
```

The first command regenerates **all certificate data** from the included 1952-byte `lat2.txt`, writes a compact JSON proof file (approximately 5 KB) to `/tmp/agent3_cubic_certificate.json`, and checks 2252 rec2 test rows, 232 independent rank witnesses, all 1444 physical carry graph edges against 13 independent coboundaries, and 10,000 randomly generated cyclic rows. The second command uses a **separate digit-normalization and different GF(2) pivot implementation** to recheck the actual 232 certificate rows and every one of the 1444×13 edge equations, then checks 2000 random words in 8 phases.

Expected primary output:

```text
PASS: 2252 rec2 tests; 232 independent rows among 336 phase coefficients
PASS: 76 cyclic carry states, 1444 valid edges, 13 independent telescoping feature identities
PASS: 104-dimensional universal zero-function kernel exhausts covariance constraints
CONTROLS: 10000 independent physical-carry cyclic rows
PAPER PROOF: no nonzero degree<=3 local GF(2) cyclic-bulk covariance observable
```

Expected independent output:
```text
INDEPENDENT PASS: 232 witness rows using digit-normalized successor and different GF(2) eliminator
INDEPENDENT PASS: all 13 universal coboundary certificates across 1444 physical carry-graph edges
CONTROLS: 2000 arbitrary 48-cell words x 8 phase checks; cubic kernel=zero-function space
```

The seeded random words only propose candidate identities; exhaustive graph-edge verification is the **actual universal proof**. No external solver, missing data, capped search or decimal Lychrel certificate is involved.
