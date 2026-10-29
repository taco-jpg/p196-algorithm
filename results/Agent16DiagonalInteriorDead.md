# Agent16DiagonalInteriorDead

**PAPER PROOF.** For every integer `r >= 4`, base `b=2^(r+1)` and temporal overflow word `g=1 0^r 11 0^(r+1)`, every explicit cut state `S(r,s,j,u,v)` defined in the proof, with `s,u,v ∈ {0,1}` and `0 <= j <= r-3`, has **no outgoing edge** in the exact position automaton.
This excludes all `8(r-2)` members of this symbolic interior state family, with no length or state cap.
The proof does **not** establish that the state family exhausts all reachable cuts, nor classify the boundary indices `j=r-2,r-1`, nor prove the all-`r` rooted graph is acyclic.
It makes no claim about another overflow schedule, a base-10 certificate, or 196.
Proof: `reports/Agent16DiagonalInteriorDead.md`.
Primary exact finite controls and separate brute-force checker: `calculation/decimal_frontier/lattice_formats/code/agent16_interior_exact.cpp`, `agent16_interior_independent.py`.
Reproduce all finite/positive controls: `bash calculation/decimal_frontier/lattice_formats/code/agent16_interior_run.sh /tmp/agent16-interior`.
