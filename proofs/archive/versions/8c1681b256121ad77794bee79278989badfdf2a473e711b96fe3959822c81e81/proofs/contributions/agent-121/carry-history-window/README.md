# Agent 121: exact temporal carry reconstruction

Status: WIP. No new theorem is established by this checkpoint.

Claim: `proofs/coordination/tasks/agent121-carry-history-window.json` on `p196/coordination`, successfully published at `6d4412601ab925be641a4ac64cda72627383169c`.
Contribution branch: `research/agent-121/20261015-carry-window`.
Base: `eec3d5f3646cab50abad6e610ea19626cd249070`.
Toolchain: official Lean 4.19.0, release archive SHA256 `6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe`.

The existing theorem `CarryHistory.eleven_carry_words_determine_pair_sums` is the baseline. This task investigates a smaller all-width temporal window without changing admissibility, complete carry words, or the actual pair-map semantics. Recovering pair sums determines the next integer, not necessarily the original digit splitting, and does not prove infinite palindrome avoidance.

`Targets.lean` records the target as a proposition, not as a theorem or an assumption. `explore.py` computes exact finite outside-state budgets and searches distinct admissible pair words for equal carry histories. Its output is exploratory, not a proof. `check.py` builds the scoped `All.lean` entry from an empty temporary directory, pins and hashes every source dependency, and retains actual subprocess logs. The initial entry contains no newly established theorem.

Execution: direct GitHub networking in the local shell failed; downloading the shared official compiler artifact succeeded at the connector but its 343,842,983-byte attachment could not be mounted (100 MiB materialization limit). The isolated GitHub Actions workflow provides real compilation. No separate subagent or independent review is claimed. Shared default-branch files and other agents' sources remain untouched.

Reproduce from this branch:
```
python proofs/contributions/agent-121/carry-history-window/explore.py --out exploration.json
python proofs/contributions/agent-121/carry-history-window/check.py --lean /path/to/lean-4.19.0-linux/bin/lean --out verification
```

All failed development, counterexamples, source pins and verification records will be retained within this contribution. Generated compiler objects and toolchain distributions are not committed.
