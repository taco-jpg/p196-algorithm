# Nine-center registry preflight

Agent #1 specialist `/root/verification_plan` prepared this scoped registry; this role did not author either new mathematical module or run Lean for this preflight. The parent remains the sole Git writer.

The sole root is `Agent1PeriodicNinesCenter`, project key `agent1-periodic-nine-center`, in `proofs/Agent1PeriodicNinesCenter.registry.json`. The actual import DFS contains exactly 17 modules: 15 unchanged inherited modules and two new modules. Original aliases come from the published NinesCycle and Quotient registries at foundation `b8c17a5204ae56ad1fc99d8f9932ca9f57b6ac80`; all 14 overlapping prior pins agree. Every inherited source matches that published foundation in bytes, SHA-256, Git blob and imports. The accepted claim is `7fd992f8a842eb7e870cd047df0d1e995de77128`.

The four registered public theorems are:

- `Agent1.Periodic.stripPeriodCenter_wrap`: for any nonempty period, adding one period on the left and its reverse on the right preserves the maximal stripped residual and increases the strip count by one.
- `Agent1.Periodic.rawCenter_nines_mixed`: bounded outer/center inputs with actual mixed nine entries produce an exact nine wrapper around the paired fixed center digits with the actual overflow pad.
- `Agent1.Periodic.quotientCenter_nines_mixed`: the quotient center is precisely the maximal stripping of that paired residual.
- `Agent1.Periodic.centerPeriods_nines_mixed`: the removed count is precisely the residual count plus one, including further inner removals.

These statements retain the actual entry bits and clock; they assert neither center descent nor a no-return obstruction, a qualifying cycle, an unconditional decimal existence result, or a conclusion about 196. A separately proposed finite counterexample task contributes no source or endpoint to this registry.

Frozen new source pins:

| Module | SHA-256 | Author verification |
| --- | --- | --- |
| `Agent1PeriodicCenterWrap` | `dd0cba7b9f1fd97eb733d8815e1059440040a464508a3a3a265bf11084383523` | attempt-002: strict compile and whole-origin audit PASS; 6 theorem constants, no definitions/runtime entries; actual axiom union `propext`, `Quot.sound` |
| `Agent1PeriodicNinesCenter` | `7d6d27081c480345e796c6b8e950c08a5ce0d7207e4030d24e504db4abde695e` | attempt-004: strict compile and whole-origin audit PASS; 12 theorem constants, no definitions/runtime entries; actual axiom union `propext`, `Classical.choice`, `Quot.sound` |

The author commands use official Lean 4.19.0 with `--trust=0 -j1 -DElab.async=false`. They reuse 11 and 16 pinned dependency objects respectively. `confirm-authors.py` checks canonical sources against the immutable successful attempt sources, the frozen receipts, both successful command records, exact compiler identity, complete theorem audit rows and public literal `#print axioms` output, and the sealed author evidence file hashes. Those author increments are not fresh combined verification.

`run-000` preserves the inherited-only source check, `run-001` the provisional actual 17-module snapshot, and `run-002` the final author-confirmed snapshot. Each retains its exact preflight script. The nested-comment/string-aware source scan found no prohibited executable trust-bypass or unfinished-proof tokens in the actual closure. This source scan supplements execution evidence; it does not replace it.

An initial helper lookup failed because its predecessor path was absent in this working tree. `setup-failure-001.json` retains that non-Lean setup failure. The exact published predecessor was then read with `git show`; `helper-provenance.json` records that origin and the scope adaptations. No source was restored or edited outside the owned preflight and scoped registry paths.

Final registry status is `FROZEN_AUTHOR_CHECKED_FRESH_REVIEW_PENDING`. Parent and independent fresh combined builds are still pending at this freeze; subsequent results should be additive evidence, preserving this historical status text. No global accepted registry was changed. `FILES.json` seals this directory, excluding itself.

The parent canonical command, after publishing the frozen sources, is:

```sh
python3 proofs/verify_project__214bf7673efe116b.py --lean /workspace/p196-tools/lean-4.19.0-linux/bin/lean --output /workspace/p196-agent1-session-20261016/nine-center-parent-clean-001 --project agent1-periodic-nine-center --registry proofs/Agent1PeriodicNinesCenter.registry.json
```

Working directory: `/workspace/p196-agent1-nine-center-20261017`. This documented command has not been executed by the registry specialist; the canonical verifier's argv does not explicitly include `--trust=0`. The independent reviewer separately controls strict compiler arguments.
