# Agent5P12InvisibleDefect

**PAPER PROOF.** For the decimal period-12, spatial-period-9 exterior
`g=100010001000`, the first mismatch with the prescribed lower-half
lattice can advance an arbitrarily large number of positions in ONE
reverse-and-add pair-word step, without changing the next pair word at all.
For each `k>=0`, take length `n=400+18k`, the exact `B0/W0` reflected
pair word, and change its symmetric coefficients at position `j=35`
from 18 to 9. The first mismatch is then 35, whereas after one step
it is `h=200+9k`, so the jump is `165+9k`. In fact 8 of 9 bulk
spatial residues admit such an invisible symmetric ±9 change.
This refutes only an **unconditional** constant one-step front-speed
bound; persistent-defect bounds, periodic centres, decimal certificates,
and the orbit of 196 remain UNDECIDED. Proof: `reports/Agent5P12InvisibleDefect.md`.
Reproduce: `python3 calculation/decimal_frontier/lattice_kinks/code/reproduce_wall_jump.py`.