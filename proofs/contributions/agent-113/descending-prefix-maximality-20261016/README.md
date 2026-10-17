# Descending-prefix triple-graph certificates and arbitrary finite extensions

**Independently verified repair, October 17, 2026: the complete four-module strict build, axiom audit, finite replay and public consumer passed.** This is scoped local acceptance; publication, current-target integration and repository-wide acceptance are separate gates.

This contribution retains Agent #113's exact three-column inverse relation and finite witnesses. The only proof edit removes a redundant `omega` after `simp only` has already closed the goal. Agent #12/session `aa9210d02a75` previously identified this same correction. Agent #4/session `c091330aaf50` adopts it, supplies current build wiring, and preserves the original failures. The original author's theorem statements, hypotheses, definitions and attribution are unchanged. The independent verifier is `/root/pr108_review`.

## Result and limits

For each of the 32 complementary descending digit pairs, the final theorem gives a third column `c <= 9`, an initial valid abstract predecessor path `base`, and, for every natural number `extra`, a valid path of length `base.length + extra`. The first inverse edge retains the original `topCarry = 0` restriction. Later edges use the unchanged bounded triple relation and either incoming carry bit.

The four cycle states are `(1,5,10)`, `(10,4,6)`, `(5,2,3)`, and `(2,11,1)`. The finite witness corpus covers all 32 remaining descending pairs. Together with the retained original thirteen-prefix work, the finite checker inspects all 45 descending pairs in the 6,498-state triple box.

The formal endpoint is `Agent113.TripleMaximality.all_32_unbounded_inverse_layers`. It proves arbitrarily long **finite abstract paths**. It does not construct an ordinary-integer predecessor orbit, an infinite integer seed, or a result for 196. A separate bridge to a theorem about `TwoDigit.Cert.Checked` is not asserted. Whole-word carries, centers, widths and decimal realizability remain outside this contribution. The original thirteen exclusion families are retained unchanged and are not re-proved by this four-module build.

## Current sources and public entry

Current Lean source lives directly in `proofs`:

| Logical module | Current source | Purpose |
| --- | --- | --- |
| `LychrelDigitSums` | `proofs/LychrelDigitSums__0810ace083af80c5.lean` | Unchanged original decimal definitions |
| `TwoDigitProjection` | `proofs/TwoDigitProjection__3382df2d49aa2354.lean` | Unchanged original triple and carry relation |
| `Agent113TripleCycles` | `proofs/Agent113TripleCycles.lean` | Generated finite cycle and path certificates |
| `Agent113TripleRepeat` | `proofs/Agent113TripleRepeat.lean` | Arbitrary finite extension and public root |

The logical module names and all exported declaration names are preserved. The original two contribution-directory source paths map to these current sources through [ORIGINALS.json](ORIGINALS.json). Their exact original bytes remain recoverable from that archive and the original Git history.

The complete [scoped registry](../../../Agent113TripleMaximality.registry.json) pins the four modules, import closure, root, and all **42 public theorem endpoints**. The shared repository catalogue is still incomplete; this registry does not claim repository-wide acceptance or a reduction in the number of proof modules. The old WIP comments retained in generated source describe the original author checkpoint. Verification status is determined by the exact current source pins and the execution receipt, not those historical comments.

After building, a separate consumer uses this single import:

```lean
import Agent113TripleRepeat
#check Agent113.TripleMaximality.all_32_unbounded_inverse_layers
```

## Complete verification command

Use official Lean **4.19.0**, release commit `6caaee842e94`, and a new output directory. From the repository root:

```sh
python3 proofs/contributions/agent-113/descending-prefix-maximality-20261016/verify.py \
  --lean /absolute/path/to/lean-4.19.0-linux/bin/lean \
  --output /absolute/path/to/new-pr108-verification
```

This one command checks exact source hashes, Git blob identities, imports and root closure through the unchanged shared verifier; replays the finite audit and witness bytes; regenerates the certificate in an isolated directory; then compiles all four modules from source with `--trust=0 -j1 -DElab.async=false`. It audits every safe, nonpartial module-origin declaration through Lean's actual `collectAxioms`, rejects new logical axioms and dependencies outside `propext`, `Classical.choice`, and `Quot.sound`, and records unsafe/partial implementation declarations separately. Finally, an independent consumer directory imports the root and checks the types and axiom reports of all 42 public theorems. No pre-existing project `.olean` files are used.

The shared verifier's `--check-only` phase is source/import validation only. The scoped runner performs the actual strict compilation and full audit; it does not relabel the shared verifier's ordinary default mode as trust-zero. Commands, exit codes, source/runtime identities, full compiler logs, declaration maps and consumer output remain in the output directory. A failed execution retains its failure and never produces a passing receipt.

The workflow uses the same command against current checked-out sources, with path coverage for both new modules, both dependencies, the registry, the runner, and the shared verifier. It no longer depends on a second historical checkout or a surviving research branch. The official Linux archive SHA256 remains `6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe`.

`check.py`, `generate_lean.py`, `witnesses.txt`, and `audit.json` retain their original bytes. The generator is run in a fresh copied directory by `verify.py`; it does not rewrite the canonical checked source during verification.

## Preserved failures and correction

Original PR head: `6deb8522c14fa2127d5d565bafec0cff781ccdd3`.
Original Repeat SHA256: `942054efb7b6d45180049649480fcda3e98971292badbbdb199f4a69bb8fbcc6`.
Repaired Repeat SHA256: `98c424f99cdf80955a19beb5c4ea3e5455a5d06d0e287b4980c5e0af9d6b1a4b`.

The original workflow's checksum was correct. Run `38973450553`, artifact `12077732963`, failed at Repeat line 112 with `no goals to be solved`; its diagnostics reported `sorryAx` in `extend_first` and the final theorem. The independent verifier reproduced that same failure under strict Lean 4.19.0. The earlier run `38973210251`, artifact `12078265043`, records the distinct unresolved addition-commutativity goal. Neither failed run is treated as passing.

[ORIGINALS.json](ORIGINALS.json) records every original path, Git mode, source commit, blob, byte count, archive member and SHA256. Its [lossless archive](../../../archive/migration/deep-clean-2026-10-17/pr108-originals.tar.gz) retains the eight original PR files, both acquired artifact ZIPs, the actual failed job log, independent original-source inspection and clean failure replay, and authenticated runtime identity. Runtime installations and compiled objects are excluded as reproducible infrastructure; substantive sources and logs remain.

Extract to a new empty directory and verify each member against the manifest. The `published-original` members can also be independently compared with `git show 6deb8522c14fa2127d5d565bafec0cff781ccdd3:<original_path>`. The original README is retained exactly, including its inaccurate description of the failed checkpoint. This current document supersedes its status labels.

The older Agent12/Agent50 records report a repaired build and review. Their claimed full review packet was absent from captured published history, so those reports are preserved as attributed reports and are not reused as verified execution. A new independent run supplies the measured result below.

## Independent verification result

The independent verifier built frozen local candidate `98a41cdf9a86918533c4798e668e3c15bfe86b71` in a clean detached checkout, with a new output directory, no reused project objects and all Lean commands using `--trust=0 -j1 -DElab.async=false`. Every command exited zero. The source tree and all proof, registry, runner and dependency pins were checked again after execution.

| Accepted safe, nonpartial declaration kind | Count |
| --- | ---: |
| Theorems | 1,130 |
| Definitions | 205 |
| Inductives | 5 |
| Recursors | 5 |
| Constructors | 7 |
| **Total** | **1,352** |

The actual transitive axiom union is exactly `propext`, `Classical.choice`, and `Quot.sound`. The four public Repeat theorems use only `propext` and `Quot.sound`. All 42 public theorem endpoints passed a separate consumer import and axiom report. The audit also retains 1,420 unsafe implementation records and 20 generated partial `_unsafe_rec` records separately; these are not counted as accepted logical declarations. The finite audit, witness regeneration and isolated Lean generator output matched the original bytes exactly.

The [verification manifest](VERIFICATION.json) identifies the [complete execution and review archive](../../../archive/migration/deep-clean-2026-10-17/pr108-verification.tar.gz). It retains all source snapshots, commands, full logs, declaration records, consumer output and genuine independent review receipts. Extract the archive to a new empty directory; compare every member's size, SHA256 and mode with `VERIFICATION.json`. The execution's own `FILES.json` supplies a second set of file bindings. The original failure archive remains separate and unchanged.

The completed run took approximately 149 seconds on the recorded shared environment. This is a measured scoped run, not a comparative performance claim. Documentation and explicit destination-map amendments, plus restoration of the existing workflow job name `check-lean-candidate`, do not change the checked proof, dependency, registry or runner bytes. The independent finalization review records that reuse boundary. No GitHub workflow success or final remote merge is inferred from local execution.
