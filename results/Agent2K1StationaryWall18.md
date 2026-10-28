# Agent2K1StationaryWall18
**COMPUTED.** Base 10, period-8 g=10101010 rec0 lattice (m=20),
any fixed first-defect column x>=119 (all x mod 20, all time phases):
no infinite trajectory can preserve the exact lattice below x while
remaining off-lattice at x for all times, irrespective of centre width.
Correct descending-carry boundary: at gam=1 with lattice P[x-1]!=9,
the lower output may match despite a changed carry (400-digit control
in the previously published Agent2K1BoundaryTransfer).
The finite k-column transition graph is a necessary overapproximation.
Any (k+1)-column cycle projects to a k-column cycle. Exact SCC/bi-core
pruning is empty at k=2 for j mod 5=0,3; k=3 for j=1,2; k=18 for j=4.
At j=4,k=17: 525 cyclic SCC states; at k=18: 0 (9,975 candidates).
Reproduce: `agent2_stationary_bicore.cpp` and independent pure-Python
`agent2_stationary_scc.py`, using existing `agent2_boundary_data.py`.
Does NOT exclude moving defect fronts, arbitrary centre kinks or 196.