# Exact F2 follow-up reproduction
Run `sh run_agent15.sh` from this folder on a machine with a C++17 compiler and Python 3; allow at least 8 GB RAM for the largest per-stream graph, and execute one process at a time. The runner performs the mandatory base-9 and base-13 positive controls (and the base-7 repeated-word SCC control), reads **all** 17 exact inputs/caps from `agent15_f2_17.tsv`, checks node/edge/repeated-edge counts for every result, and then executes the two independent carry/predecessor checkers for the base-7 p21 periodic-mirror exclusion. `ALL CHECKS PASSED` is printed only after every assertion succeeds. Do not interpret `CAPPED` as a negative result.

The graph engine uses exact 192-bit packed cut states and breadth-first traversal; an exhausted graph with no repeated edge is acyclic because every edge except the initial root introduction discovers a previously unseen state. Even at the cap, earlier portions being tree-shaped do *not* prove acyclicity for the unvisited remainder. For the b7 p21 bulk result, all initial mirrored rows for m in {1,3,9} are checked, using cyclic carry maps and one full 21-time-step return, while the independent checker instead solves cyclic carry fixed-point equations. The only non-neutral genuine mirror period is m=1, whose two target states both have singleton backward cones verified by independent temporal predecessor dynamic programming; the root is different from either target.

Control commands (also automated):
`./agent15_compact 9 3000000 <file containing 1100011000>` -> 956310 states, 1005301 edges, 48992 repeated edges;
`./agent15_compact 13 3000000 <file containing 1010010000>` -> 250302 states, 254201 edges, 3900 repeated edges;
`./agent15_compact 7 3000000 <file containing (10)^12>` -> 32771 states, 40962 edges, 8192 repeated edges.

Other periods (including temporal multiples), non-mirror bulk lattices, bounded centres, root-reachable SCCs on the eight still-capped streams, and decimal Lychrel existence remain UNDECIDED.
