# AgentX13QuadrantAffinePumping
**PAPER PROOF (format):** a sound guarded affine-counter pairword certificate criterion, with an exact orthant-uniform finite-run carry/zip checker and a counter-cone closure obligation. No sample-to-infinity extrapolation.
**PAPER PROOF (positive decimal mechanism):** N19's synchronized six-edge decimal clock extends to every **independent** pair `k,l>=6`; phase-6 bulk `(8,16)` has differential lengths `(k-5,l-2)`, all six steps universally checked.
**COMPUTED (controls):** the same checker reproduces the published base-9 ten-edge (+1) and base-50 four-edge (+1) certificate cycles, 2,554 and 653 symbolic comparisons respectively.
**COMPUTED (independent replays):** five asymmetric ordinary-decimal-integer six-step controls, 125 randomized period-run controls, mutation and fail-closed quadrant tests all pass.
Reproduce: `python3 calculation/new_structures/agent-X13/test_oracle.py`.
Code/data: `calculation/new_structures/agent-X13/{affine_two_counter.py,periodic_affine.py,controls.py,test_oracle.py,data.json}`.
Details/proofs/Lean sketch: `reports/AgentX13QuadrantAffinePumping.md`.
**UNDECIDED:** no compensating `H6->H0` return edge, no decimal infinite certificate, no assertion about 196, and no Lean verification; the full repo verifier was unavailable locally.
