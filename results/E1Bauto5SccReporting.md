# E1 bauto5 SCC reporting audit

**COMPUTED (bug fix, not a new decimal census).**
Original `bauto5.cpp` printed `edges=0` for every nontrivial SCC graph.
The exact number of distinct directed edges is now counted from its adjacency lists.
The small base-4 control `g=101100` has 957 reachable states, 1,012 edges, and four
nontrivial SCCs (all of size one), established independently in `scc_oracle_b4.py`.
`SCCMIN_NONE` means exhaustive shortest-cycle search up to S in that SCC.
`SCCMIN_CAPPED` and `SCCMIN_SCOPE` identify size-capped and omitted SCC searches;
`-scccap N` defaults to 6000 and permits deterministic coverage regressions.
Reproduce: `sh calculation/decimal_frontier/lattice_formats/code/test_bauto5_scc.sh`.
No p25..28 census, decimal lattice exclusion, palindrome avoidance, or Lean claim.
