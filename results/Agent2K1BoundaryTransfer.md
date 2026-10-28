# Agent2K1BoundaryTransfer
**COMPUTED.** Decimal p=8, g=10101010, rec0 spatial m=20, fixed first-defect
position x=119+j: exact 3-column necessary graph has no indefinitely
persistent off-lattice path for j mod 5 = 0,1,2,3 (all 8 phases).
Its longest paths have respectively 14,32,26,18 transitions, from exhaustive
8*18*19^2=51,984 states per j, reproduced for all j=0..19.
For j mod 5=4, the 3-column graph retains 2,189 indegree-core states;
the 10-column scan visits 169,030,175 candidates, 292,306,336 edges,
and leaves 29,717,052 indegree-core states; beyond width 10 **UNDECIDED**.
A concrete 400-digit integer step disproves requiring the unperturbed
lattice descending carry on every overflow: actual/nominal carries 0/1.
Run `python3 calculation/decimal_frontier/lattice_kinks/code/agent2_boundary_check.py`;
compile/run `agent2_boundary_transfer.cpp` with data from `agent2_boundary_data.py`.
No actual periodic centre, unrestricted wall bound, base-10 certificate, or claim about 196.