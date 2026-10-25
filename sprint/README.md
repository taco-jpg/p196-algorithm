# Sprint agent folders

Each `sprint/agent-NN/` folder holds the report (`REPORT.md`), scripts and small data of one Claude sprint agent
(pull requests #261–#265, #267, #287, merged on 2026-10-24). Their Lean files are registered results under
`lean/P196/Sprint/AgentNN/` and are listed in [RESULTS.md](../RESULTS.md) ("Sprint agent results").

| Folder | Topic | Lean result |
| --- | --- | --- |
| `agent-01` | forward abstraction from the orbit of 196; the width-8 core is one strongly connected component | `Sprint01ForwardWalk` |
| `agent-02` | forward invariant census up to width 9; width-8 exclusions of 2342, 9149, 6676 | `SprintAgent02` |
| `agent-03` | enriching the forward state gains nothing; 196's prefix state lies on a cycle | `SprintAgent03` |
| `agent-04` | anatomy of the cycles of the prefix abstraction | `SprintAgent04` |
| `agent-05` | delay witnesses: lower bounds for every prefix certificate | `Sprint.Agent05` |
| `agent-19` | review of eleven earlier results (prose corrections) | `SprintAgent19` |
| `agent-20` | red team of the prefix-exclusion chain and CertificateToLychrel | `SprintAgent20` |

For the status of every four-digit prefix use [`calculation/prefix4_status.csv`](../calculation/prefix4_status.csv),
which supersedes the per-agent prefix tables here.

Run logs, `RUNS.md`, `analysis_output.txt`, `run_summaries.txt`, `graph_out.txt` and the red-team reproducer
`agent-20/repro/SkipKernelTC.lean` were removed on 2026-10-25 (repository rule 5: no logs or probe files); the
reports still mention them, and they are in the git history before that date. The kernel-bypass trick the
reproducer showed is now rejected by `tools/verify.py` (source rule plus lean4checker).
