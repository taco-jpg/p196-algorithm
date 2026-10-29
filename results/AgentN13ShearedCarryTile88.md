# Agent N13: an 88-phase decimal two-ended carry-boundary tile
**COMPUTED**, finite witness only; **PAPER PROOF** conditional local-block carry lemma in the report, but no unconditional infinite decimal certificate.
For the two 10400-digit seeds of AgentN13DecimalShearedFront22, with front `f(t)` and strip `j=f(t)+[-100,74]`, all **eight** low/high start/end carry bits (two orbits) satisfy `g(t+88)=g(t)` for all tested `1000<=t<=20000`.
This is **152,008** exact comparisons (19001 times * 8 gates), zero failures. The high incoming gates of the two orbits differ in **49/88** phases, so the tile is not a constant or globally identical carry block.
An independent ordinary Python big-integer reverse-and-add computation checks 8,008 boundary bits at `t=1000..2000` and independently produces an **identical** eight-bit, 88-phase table. The entire table is stored in `calculation/new_structures/agent-N13/carry88.csv`.
Run: `bash calculation/new_structures/agent-N13/carry_tile_run.sh`; sources: `carry_tile.cpp`, `carry_tile_independent.py`, `carry_tile_run.sh` in the same directory.
The report `reports/AgentN13ShearedCarryTile88.md` states the conditional one-step two-ended carry-cut soundness lemma and its limitation: the 88-phase gate inputs have NOT been proven self-generated forever.
This result is a finite nontrivial candidate macro-boundary contract, not a base-10 Lychrel proof, not Lean-verified, and not a claim beyond 20000 steps.
