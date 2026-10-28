# Agent10F2G01InfiniteFamily
**PAPER PROOF.** For EVERY integer k>=1, base b=3*2^k-4 admits a
reachable neutral-band exterior B-cycle for overflow necklace g=01
(period 2), with an explicit path of k+1 spatial columns from the
canonical root to a neutral accepting cut. Even k reaches (1,2,0);
odd k reaches (2,1,b-1). All coefficients/carries are closed formulas.
Full all-parameter derivation: `reports/Agent10F2G01InfiniteFamily.md`.
Executable symbolic path checker: `calculation/decimal_frontier/lattice_formats/code/agent10_g01_infinite_family.py`.
Reproduce: `python3 calculation/decimal_frontier/lattice_formats/code/agent10_g01_infinite_family.py 1000`.
Independent exact-edge checks k<=20 and BFS-first-accept controls k<=15;
mandatory base9/base13 generic SCC controls reproduced.
NOT claimed: neutral centre closure, full Lychrel certificates, base 10,
or any assertion about the orbit of 196. Not Lean-verified.