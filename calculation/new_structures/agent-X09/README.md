# X09: binary-indexed spacetime certificate format, and grammar diagnostics

Status: **PAPER PROOF** for conditional soundness of the automatic-spacetime format; **COMPUTED** for controls and genuine 196 orbit diagnostics. Neither a base-10 certificate nor a 196 Lychrel proof.

The report is `reports/AgentX09AutomaticSpacetime.md`; short note is `results/AgentX09AutomaticSpacetime.md`.

## Reproduction in a repository checkout

```sh
cd calculation/new_structures/agent-X09
python3 automatic_spacetime.py --steps 2000 --independent 16
mkdir -p scratch
g++ -O3 -std=c++17 orbit.cpp -o orbit
./orbit 100000 scratch
python3 grammar_probe.py scratch > regenerated_summary.json
python3 -m json.tool regenerated_summary.json >/dev/null
```

`automatic_spacetime.py` requires the existing base-9 control file `calculation/decimal_frontier/lattice_formats/cert_b9_rec0.json` and checks its phase/affine-periodic digit formula against two completely different next-state algorithms, with 16 Python integer/divmod controls. Its 65,536 binary-index parity controls test that a two-state DFAO can describe a nonperiodic two-dimensional pattern. **It is not an implementation of the all-quantifier automatic model checker.**

`orbit.cpp` starts with decimal digits 196 and performs genuine grade-school reverse-and-add for 100,000 steps, detecting any palindrome at each step. Snapshots are local, do not commit them. `grammar_probe.py` verifies 2,000 steps independently with Python arbitrary-precision `int`, computes LZ78/gzip/substring entropies on five true palindromic pairword halfstrings, and compares each against a fixed-seed frequency-preserving shuffle. The original compact machine-readable metrics are in `summary.json`.

The full 100,000-step decimal string SHA256 is `c1855622b791d153520ff5bd39e539fd3d04832e21258d59c46f399acbfd2511`. This checksum is a replay control, not evidence of infinite avoidance.