# Agent N13: decimal 22-step sheared moving front

Status: COMPUTED finite-horizon data only, **not** a base-10 Lychrel proof.

The source array in both C++ files is the t=0 first component of the first reachable p8/m20 SCC in the tracked repository file `calculation/decimal_frontier/lattice_formats/p8_scc.txt`; its 39-element path followed by its 20-element spatial cycle is copied inline, so no external files are needed. The central 100 coefficients are replaced in one of the two orbits. The input decimal seed (`seed.txt`) is provided explicitly to allow big-integer replay without relying on the generator.

Required: GNU-compatible C++17 compiler, Python 3.11+, `sha256sum`, bash. Run from any directory:

```sh
bash calculation/new_structures/agent-N13/run_all.sh
```

The script independently: compiles both C++ engines; makes and SHA-checks the 10,400-digit seed; runs the 20,000-step complete digit engine, checking a nonpalindrome at every step and its first eight pair coefficients; runs two integer orbits through 20,000 steps and compares *all* pair coefficients to locate their first difference; checks each equation `f(t+22)=f(t)-5` for t=18..19978 and `f(t+88)=f(t)-20` for t=18..19912; replays the exact seed using only Python's arbitrary-precision integer arithmetic for every t=0..20000; SHA-checks the complete final 20,400-digit integer; executes short-width and asymmetric digit-lift controls. Its last line must be `AGENT_N13_FULL_REPLAY_AND_FRONT_PASS`.

Primary outputs (COMPUTED, t<=20,000): no palindrome; length from 10400 to 20400; first eight pair coefficients exactly phase8; f(0)=5100, f(20000)=556, period22 translation exact after t=18. The two seed digit lifts are intentionally asymmetric; paired coefficients remain symmetric as required by arithmetic. The front approaches the exterior, so this demonstrates *a translating defect*, not a certified infinite orbit. Full mechanism and a proposed semilinear-spacetime certificate format in `reports/AgentN13DecimalShearedFront22.md`.
