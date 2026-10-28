# Fixed period-10 schedule exclusion in bases 32--40

**COMPUTED.** For bases 32 through 40, the exact position automaton has no
reachable nontrivial SCC for either fixed period-10 overflow word `1100011000`
or `1010010000`, at a 3,000,000-state cap; every run completed below that cap.

Scope: the two stated words and bases only.  This neither proves a parametric
family nor excludes other periods, other schedules, or base-10 certificates.

Code and reproducible command: `calculation/decimal_frontier/lattice_formats/code/bauto3.cpp`.
Compact data and controls: `calculation/decimal_frontier/lattice_formats/f2_fixed_schedule_32_40.md`.
