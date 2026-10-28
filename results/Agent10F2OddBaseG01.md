# Agent10F2OddBaseG01
**PAPER PROOF.** For every odd integer base b>=3 and cyclic overflow word g=01
(period 2), the exact position automaton has no neutral-band accepting
cut state reachable from its canonical root at ANY exterior width.
Proof: reports/Agent10F2OddBaseG01.md (one-carry invariant plus isolated
accepting self-loops). This is not Lean-verified.
Independent finite controls: code/agent10_g01_odd_check.py under
calculation/decimal_frontier/lattice_formats/ (run with python3).
It checks b=3,5,...,301, and the positive b26 g=01 width-8 control;
mandatory b9/b13 full-SCC controls were reproduced before the census.
Scope: ONLY this neutral exterior overflow necklace in odd bases;
no claim about other words, absorbing bands, any decimal Lychrel
certificate, or the orbit of 196.