# S37 cyclic-seam pumping lemma

**PAPER PROOF** (conditional all-width lemma; no decimal Lychrel certificate).

For a rooted `B W^q J_(k mod d) U^k C_(k mod d)` pairword family with equal-length cyclic junctions/centres, the exact finite window `q=Q`, `k=K,...,K+d-1` suffices for all independent `q>=Q,k>=K` if every 120-step edge returns exactly to `k+5`, has the rooted overflow clock and odd-coefficient guards, and the two-cut carry/overflow-one lag conditions pump `W` and `U^d` back to themselves.

The proof and exact scope are in `reports/AgentS37CyclicSeamPumping.md`; the executable candidate checker and randomized local regression are in `calculation/new_structures/S37/`.

No physical decimal seam passes the endpoint-return obligation yet; existence remains **UNDECIDED**.
