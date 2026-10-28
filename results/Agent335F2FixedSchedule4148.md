# Agent335F2FixedSchedule4148

**COMPUTED.** The fixed period-10 schedules `1100011000` and `1010010000`
have no reachable nontrivial exterior SCC in bases 41 through 48.

Scope: the exact `bauto3` position automaton, one run for every listed
(base, schedule) pair, with the 3,000,000-state cap.  No run reached the cap:
`1100011000` has one state and zero edges in every base; `1010010000` has
169, 285, 133, 9, 9, 9, 9 and 9 states respectively, all with zero
nontrivial SCCs.  The same binary and cap reproduce the base-9 control
(`1100011000`, including the depth-61 period-4 SCC) and base-13 control
(`1010010000`, including the depth-55 uniform SCC).

Reproduce: `calculation/decimal_frontier/lattice_formats/code/f2_fixed_schedule_41_48.sh /tmp/agent335-f2`.
This excludes only these two fixed schedules in these eight bases; it makes no
claim about other schedules, other bases, decimal, 196, or an infinite orbit.
