# Agent15F2CappedFollowup
**COMPUTED** (exact finite-state searches, stated caps): complete follow-up of all 17 F2 primitive position-zero-feasible overflow streams previously CAPPED at 3,000,000 states, bases 7,19,22,25 and periods 17..24.
Nine exhaust their reachable automaton with **no repeated edge**, hence no reachable SCC; eight remain **CAPPED/UNDECIDED** (10,000,000-state cap). One base-25 p19 stream exhausted at 18,296,615 states under a 20,000,000-state cap.
**COMPUTED** (exhaustive all-width single-lap lattice obstruction): base 7, p21, g=`101001010110001011000`, S=9 has no root-reachable self-mirror absorbing lattice returning after exactly 21 time steps with spatial period m|9. Periods m=3,9 have no genuine returning mirror row; both m=1 targets (uniform 0,12) have only their own state as predecessor, unreachable from root.
Scope excludes other overflow words, other bases, superperiodic temporal returns, other lattice formats, a base-10 certificate and any claim about 196.
Data and exact commands: `calculation/decimal_frontier/lattice_formats/agent15_followup17/agent15_f2_17.tsv`, `run_agent15.sh`.
Code, controls and independent arithmetic checkers: the other source files in that same directory.
All reported caps are per overflow word; the full 17-row table is a single result, not 17 separate partial commits.
