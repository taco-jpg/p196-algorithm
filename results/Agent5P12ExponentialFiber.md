# Agent5P12ExponentialFiber

**PAPER PROOF.** For every integer k>=1, there are at least 2^k
DISTINCT canonical base-10 positive integers of common length
n=200+18k, all sharing the identical complete pair-coefficient word
after ONE ordinary reverse-and-add step. The same holds at length
n=201+18k. Starting at the decimal period-12/m=9 lattice phase t=1,
concatenate k independent mirrored seven-column bulk substitutions
at lower indices 59+9j (0<=j<k). Each returns both carry boundaries
to the baseline, so every subset produces the same successor pairword.
All 2^k subsets were independently replayed through k=12 (4096 seeds).
This is a quantified one-step collision-fibre theorem, not an orbit
return, a centre certificate, or proof that any seed is Lychrel.
Proof: `reports/Agent5P12ExponentialFiber.md`.
Reproduce: `python3 calculation/decimal_frontier/lattice_kinks/code/k2_multi_fiber.py`.