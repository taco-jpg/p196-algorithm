# Agent5P12NonErasingFrontJump

**PAPER PROOF.** For every k>=2, two distinct canonical positive
base-10 seeds of common length n=200+30k have symmetric input pairwords
whose first lower-half mismatch is exactly at index 59. After one
reverse-and-add step, their successor pairwords are NOT equal: they
differ only at indices 59+9k and n-1-(59+9k), by +2 at each.
Thus a nonvanishing successor defect has moved its first apparent
front forward EXACTLY 9k positions in one step, with no uniform bound.
Construction: one invisible seven-column bulk patch at index 59,
plus a far separated noninvisible single-column 4->5 change.
This refutes only an UNCONDITIONAL one-step front-speed cap for
possibly disconnected defects, not a connected-defect bound,
periodic-centre existence, or decimal Lychrel status.
Proof: `reports/Agent5P12NonErasingFrontJump.md`; reproduce: `python3 calculation/decimal_frontier/lattice_kinks/code/k2_delayed_front.py`.