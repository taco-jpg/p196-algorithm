# Agent N11 decimal real-orbit and zero-shield construction

The finite result is COMPUTED, not an infinite Lychrel proof. The main
constructive experiment uses an explicit 90,260-digit base-10 seed N_45000,
two independent 20,000-step ordinary integer replays, and a pair-coefficient
zero shield of length at least 45,000 - 2t for steps 1 <= t <= 20,000.

Everything reproduces from repository source without network access:

~~~sh
bash calculation/new_structures/agent-N11/reproduce.sh --quick
bash calculation/new_structures/agent-N11/reproduce.sh
~~~

The quick mode runs the 20k constructive candidate, independent checker,
100k carry-shadow census on the real 196 orbit, literal 196 vs Python bigint
control for 5k steps, the sampled 9-stripe switch census, and a 21-step
defect trace. The full mode also executes the 1,000,000-step real 196 replay
(about 414,302 final digits; elapsed time depends on hardware).

Individual commands after compiling with g++ -O3 -std=c++17:
- bubble_family 45000 20000 1000
- bubble_independent 45000 20000 1000
- adaptive_rule 100000 100
- neutral_switch 100000 100 (writes temporary events TSV)
- trace_defect 96400 10 10
- orbit_mine 1000000 1000 128 10 /tmp/n11million
- python3 independent_check.py --steps 5000 --sample-file /tmp/n11million_samples.tsv

The runner generates temporary raw time series only, checks compact
expected.json, then removes the temporary files. No large logs or external
data are required. See reports/AgentN11CarryShadowFamily.md for the exact
local arithmetic proof, observations, qualifications and next construction.
