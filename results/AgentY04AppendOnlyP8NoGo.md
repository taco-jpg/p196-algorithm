# Agent Y04: rooted decimal p8 append-only growing-centre no-go
Label: **COMPUTED** (complete finite carry graph and cycle checks, independently regenerated); modular reduction is a PAPER PROOF.
Scope: base 10, overflow `10101010`, exact period-8 temporal columns, canonical root `(L,H,Y)=(0,85,4369)`, **both parities**, all halfword lengths and all graph paths.
**All-time statement:** no infinite normalized pairword sequence can undergo exact eight-step reverse/add returns, each time appending two unchanged time-zero carry-graph columns to the same nested rooted column path, while retaining the period-8 temporal graph.
Proof: `T^8` multiplies digit sum by `4` mod `9`; the two-column exposed charge must be constant `c in {0,3,6}` for every renewal (odd centres use the weighted three-column charge).
Exact reachable temporal graph: 244,785 states / 263,584 edges. The `c=0,3,6` two-column graphs are all acyclic for even and odd centres; independent DFS and Kahn agree.
Redirect: a possible decimal repair **must rewrite an existing centre/carry column, change temporal phase/schedule, or leave this rooted p8 graph**. Merely appending new columns cannot repair the defect.
This does **not** disprove decimal Lychrel numbers or exclude general growing-centre templates, off-phase repairs, or finite nonstationary carry edits. No decimal all-time positive certificate or Lean claim.
Reproduce: `g++ -O3 -std=c++17 calculation/new_structures/agent-Y04/append_growth_no_go.cpp -o /tmp/y04a && /tmp/y04a`.
Independent: `g++ -O3 -std=c++17 calculation/new_structures/agent-Y04/independent_acyclicity.cpp -o /tmp/y04b && /tmp/y04b`.
Ordinary decimal integer check: `python3 calculation/new_structures/agent-Y04/bigint_regression.py`.
Detailed theorem, both central parities, full exact computation scope: `reports/AgentY04AppendOnlyP8NoGo.md`.
