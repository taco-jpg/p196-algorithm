# AgentX22UniformMosaic20k: all-Q, all-tile decimal finite-horizon family
**COMPUTED** guard at Q=600; **PAPER PROOF** extension using the pre-existing N10 universal one-step insertion lemma and X22 exact two-step coalescence.
For **every integer Q>=600** and **every ordered Q-tuple** of the 12,800 phase-0 SFT tiles from `AgentX22TwoStepCoalescence`, the resulting **12800^Q distinct positive decimal integers** have **no palindrome at any t=0,...,20000** under ordinary decimal reverse-add.
Proof: each first successor has pairword `K ++ W1^Q ++ [8] ++ reverse(K ++ W1^Q)`; N10's universal pump commutes with the true step on any guarded centre. Independently check all 20,000 subsequent Q600 guard steps, each showing the exact 39-symbol phase B_t and >=7455 anchored W_t coefficients; all B_t are odd-containing. Induct on Q-600 and time.
Q600 seed 24078 digits, t20000 34078 digits; independent literal-digit and GMP engines agree in 11 checkpoints and reject palindromes on all steps. Also 32 Q600/Q601 ordinary-bigint pairword insertion checks.
**Finite horizon only; no infinite decimal Lychrel certificate and no claim about 196.**
Reproduce: `sh calculation/new_structures/agent-X22/guard_run.sh`.
Source: `calculation/new_structures/agent-X22/{build_bphases.py,guard_check.cpp,guard_gmp.cpp,guard_run.sh,guard_20k.json}`; proof: `reports/AgentX22UniformMosaic20k.md`.
