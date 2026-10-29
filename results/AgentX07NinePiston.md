# AgentX07NinePiston

- **COMPUTED:** `N_n=10^n-2908` has a frozen central nine block and paired frontiers with exact **piston relation** `m_t=G_t+4` for `t=1..60000`, where `G_t` is cumulative decimal overflow. For all `n>=24884`, the sound frontier engine guarantees no palindrome through 60,000 steps; an odd pair coefficient lies in the first 22 positions at every checked state.
- **PAPER PROOF:** In the two-front nine-core format, `m'=m+1-r`, `L'=L+gamma-2+2r`; complementary carries `alpha+gamma=1` and `r=1-gamma` imply `m'=m+gamma`, `L'=L-gamma`, conserving `m-G`. The post-initial two guards are checked for 59,999 finite transitions.
- **COMPUTED:** Exact exhaustive negative perturbation scan `k=-9999..-1` for `9R_n+k` finds 51 seeds with preserved piston offset and odd pair coefficient for `t=0..20000`: offset 4 (45 seeds), offset 3 (4), offset 2 (2). Full list in `piston_data.json`; every survivor has `9|k`.
- **COMPUTED:** Independently GMP + schoolbook replayed the **8,297-digit** seed `10^8297-2908` for 20,000 steps: no palindrome, exact whole-word frontier, 16,584 final digits, FNV64 `a5a5b7b3e4e9b7ca`.
- Code: `calculation/new_structures/agent-X07/{piston_scan.cpp,piston_probe.cpp,piston_run.sh,piston_data.json}`. Report: `reports/AgentX07NinePiston.md`. Reproduce with `bash calculation/new_structures/agent-X07/piston_run.sh`.
- **No infinite decimal Lychrel certificate:** `L` drains by each overflow, so an additional centre-renewal gadget is still needed. No Lean claim.
