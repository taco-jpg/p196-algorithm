# AgentX05AffineTwoCorridor
**COMPUTED.** Exact affine-RLE symbolic normalization/paired-digit zipper gives 2,000 nonpalindromic decimal reverse-add transitions for every independently chosen A,B>=10000.
Seed pair coefficients (LSB first): `9^(A+1) 18^2 9^B 0^2 9^B 18^2 9^(A+1)`; starting number is `val_10` of this word.
Each symbolic length comparison is certified over the whole 2-dimensional orthant; unknown order causes rejection, not extrapolation.
At step 2000, symbolic pairword has 5,231 run terms, and for A=B=10000 its length is 40,837 coefficients.
Independent base-10 Python big-integer replay: A=10000,B=10017, 1,200 steps, every canonical decimal digit string agrees with expanded pairword and no palindrome.
Arithmetic controls: 1,080 random one-step checks in bases 3,7,9,10,13,16 and an existing base-9 certificate seed replayed 300 steps.
General all-length affine-RLE step-soundness and potential cycle criterion (PAPER PROOF argument): `reports/AgentX05AffineTwoCorridor.md`.
Reproduce: `bash calculation/new_structures/agent-X05/reproduce.sh`.
Code/data: `calculation/new_structures/agent-X05/{affine_rle.py,controls.py,independent.py,expected.json,reproduce.sh}`.
No closed temporal cycle, Lean verification, 20,000-step decimal replay, infinite Lychrel number, or result about 196 is claimed.
