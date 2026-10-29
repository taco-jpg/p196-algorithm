# AgentN15DyadicFifteenStepNeutralRun
**PAPER PROOF.** A dyadic Thue–Morse decimal pairword hierarchy has **15 exact consecutive ordinary reverse-and-add transitions at every substitution height h>=2**, with no palindrome among the initial N_0,...,N_15 (finite-time claim only).
The earlier h-uniform seven-edge locality breaks when coefficient 9 enters the bulk. A new two-sided, bounded-neutral carry transducer handles 9-runs of length at most 1; the local rule has radius at most 2 and handles overflow-induced partner shifts exactly.
All-height proof: 240 length-77 Thue–Morse factors of sigma^7(UV) (U,V in {14,16}) cover every bulk dependency cone for t=3..15. None produces a consecutive pair of neutral 9s before step 15; exterior/centre windows are resolved by the two suffix-parity classes h=10,11 plus finite heights h=2..9.
Overflow word for steps 0..14: `011000010101001`. Each of N_1..N_15 has a concrete opposing unequal digit pair recorded in the evidence file (N_0 has leading/trailing 4/0).
Independent ordinary C++ decimal digit-list replay verifies levels h=2..18, 15 steps, 6,290,677 interior local-arithmetic cells and 192 mutation rejections.
Scope: the first 15 steps for every h, not infinite Lychrel, not Lean-verified, no certificate cycle, nothing about the 196 orbit.
Proof: `reports/AgentN15DyadicFifteenStepNeutralRun.md`; source/data under `calculation/new_structures/agent-N15/`.
Reproduce: `sh calculation/new_structures/agent-N15/run_bounded.sh`.
