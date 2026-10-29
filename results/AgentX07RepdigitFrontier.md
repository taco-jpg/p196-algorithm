# AgentX07RepdigitFrontier

- **COMPUTED:** Explicit base-10 `10^12013-2` seed survives 20,000 reverse-and-add steps without any palindrome; GMP and independent schoolbook digit replay match at every step. Final length 20,286; 8,273 overflows; minimum central nine-run length 2.
- **PAPER PROOF:** Exact two-front repdigit transducer when a uniform inner block has length >=2; its 2u coefficient has an input-independent carry-out, and canonical trimming preserves the exact whole-digit and pairword structure.
- **COMPUTED:** At all 20,001 states, an odd pair coefficient lies within the first 18 positions. The symbolic check is independent of n and establishes the finite 20k-step statement for **every** initial `10^n-2` with `n>=12013` (maximal `2m_t-G_t` = 12011).
- **COMPUTED:** Additional `a*R_n+k` symbolic witnesses through 20k: `(a,k)=(1,3268)` for `n>=13180`, `(8,-9999)` for `n>=13249`; no big-int 20k replay claimed for these.
- Reproduce: `bash calculation/new_structures/agent-X07/run.sh`; evidence: `calculation/new_structures/agent-X07/measurements.json`; theorem/scope: `reports/AgentX07RepdigitFrontier.md`.
- **Not a base-10 Lychrel proof:** the boundaries grow, the central repdigit shrinks for every fixed seed, and all conclusions are finite-horizon. No Lean verification claimed.
