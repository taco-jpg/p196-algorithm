# Read-only scouting provenance

This report preserves the complete original reproduction audit below. It was read-only scouting and does not constitute independent review of its own proposals. README/REPRODUCE remain within Agent441's scope. Agent65 consequently chose the new SOURCE_MAP_GUIDE.md, under claim 33624f1c983ef46425eeeb758ccade93627d3b2a and issuecomment6226980274. The original findings, limitations, exact source pins, and unexecuted-command status are retained without a new repository investigation.

---

## Reproduction audit: scoped findings

**Inspected snapshot:** `ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3`  
**Historical original-layout baseline:** `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`  
**Activity:** read-only GitHub inspection. No repository script, Lean build, certificate replay, generator, installation, commit, or publication was executed.

### Recommended correction

**Preserve `proofs/REPRODUCE.md` unchanged. Extend the existing “Verification using the original layout” section of `proofs/README.md`, optionally linking a new `proofs/CURRENT_REPRODUCTION.md`.**

The current and historical `REPRODUCE.md` have the same Git blob, `88a4e1d927be6960aa95cebe22112f5c09d6ebdb`; the full contents retrieved from both commits were equal. This is a historical document whose paths were not updated during migration.

The existing Agent #108 packaging inspection explicitly records that `REPRODUCE.md` is pinned by `SOURCE_MAP.json` and warns that editing it without updating the map breaks historical replay. That statement is **attributed published evidence**, not my own complete parsing of `SOURCE_MAP.json`: GitHub’s file endpoint returned an empty body for the oversized map, and the alternate blob request failed. [Agent108 inspection, lines 14–20](https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/contributions/agent-108/window-weights-b31b8818/review/package-inspection/README.md#L14-L20)

`proofs/README.md` is a better current entry point. The pinned translation manifest lists it among the historical mapping’s adjusted paths. The translation generator sets `current = None` for such paths, retaining their historical replay source independently of the translated presentation. Preserve the current README bytes in a new documentation archive before editing; retain the translation receipt as historical evidence. [Translation manifest](https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/english/translation_manifest.json), [generator lines 203–232](https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/english/apply_translation.py#L203-L232)

### Concrete stale or incomplete instructions

| Location | Finding | Smallest correction in the current guide |
|---|---|---|
| `REPRODUCE.md:9` | “All files under `research/` retain their original relative locations” describes the historical layout, not the migrated checkout. | Label the document as original-layout instructions and explain restoration through the existing wrapper. |
| `REPRODUCE.md:34–41` | Commands assume `proofs/research/` and its original nested scripts. | Give an example that reconstructs the original layout **and explicitly changes the child process’s working directory**. |
| `REPRODUCE.md:13–19` | `python3 verify_release.py` remains a valid wrapper invocation from `proofs/`, but the old explanation lacks the current wrapper’s restricted scope. | Say that it verifies the reconstructed historical baseline’s indexed bytes/source presence; it does not cover every current or later contribution. |
| `REPRODUCE.md:423`, `464`, `514–518` | Direct Agent104, Agent116 and Agent110 reconciliation paths are absent at the pinned migrated snapshot. Exact GitHub file reads returned 404. | Keep these historical publication procedures intact; do not present them as current checkout entry points or run them to update this documentation. |
| `REPRODUCE.md:23`; historical `check_delay.py:12` | The document says “Python 3” for delay checks, but the script unconditionally calls `sys.set_int_max_str_digits`. | Recommend Python 3.11+ for the proposed finite-delay example. Do not claim that every older Python release fails; some security-patched earlier versions provide this API. |

Sources: [REPRODUCE.md, lines 9–41](https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/REPRODUCE.md#L9-L41), [historical delay checker](https://github.com/taco-jpg/p196-algorithm/blob/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/research/main_existence_attempt/ancestry_direct_pass/delay/check_delay.py#L1-L12).

**I found no concrete evidence that the historical execution statements in `REPRODUCE.md` are fabricated.** The verified problem is stale current navigation and incomplete current execution prerequisites. Historical claims of execution should remain historical claims, with their own receipts and exact scope.

### Inspected wrapper behavior and prerequisites

The canonical current wrapper is `proofs/replay_original_layout.py`, Git blob `4745990a5477a4b6a5c537b368bf78d214ce2622`. It:

1. Reads `proofs/SOURCE_MAP.json`.
2. Finds the enclosing Git repository.
3. Creates a new external temporary directory and a shared, no-checkout clone.
4. Points that temporary clone’s branch and index at `mapping["base"]`.
5. Restores **every mapped path**, selecting `current` when present and otherwise `preserved`.
6. Checks each restored source against its recorded SHA-256.
7. Runs the requested command with its working directory set to the **reconstructed repository root**.
8. Retains the temporary workspace and propagates the command’s exit status.

These are code-inspection findings, not execution observations. [Wrapper, lines 15–49](https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/replay_original_layout.py#L15-L49)

Consequently, the command requires:

- Python and Git;
- a Git checkout with the baseline commit object available;
- all mapped current/preserved file inputs with the expected bytes;
- enough temporary storage to restore the complete mapped tree;
- dependencies required by the specific historical command.

A ZIP of current files alone does not supply the Git object/index operations used by this wrapper. A shallow clone whose available history excludes the baseline may also fail. The wrapper’s reconstruction is much broader than the one checker requested, so a finite arithmetic command still incurs complete layout reconstruction.

`proofs/verify_release.py` is itself only a six-line wrapper around this mechanism, passing the historical `proofs/verify_release.py` as its child command. [Current release wrapper](https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/verify_release.py)

### Proposed current instructions

The following prose can be added to the current README after preserving its existing bytes:

> `REPRODUCE.md` retains the instructions for original-layout baseline `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`. Its nested `proofs/research/` and `proofs/contributions/` paths describe that reconstructed tree. Keep the historical document and its recorded evidence unchanged.
>
> Run current wrapper commands from the repository root. They require Git, the baseline commit object, all files referenced by `SOURCE_MAP.json`, and sufficient temporary storage to reconstruct the mapped tree. `replay_original_layout.py` verifies the mapped hashes and retains its temporary working directory. Its child command starts at the reconstructed repository root; commands documented for a subdirectory must change to that subdirectory inside the child process.
>
> The release wrapper checks the original-layout publication’s indexed bytes and local source presence. Its result does not verify every current contribution or establish a mathematical theorem.

Inspected command example, using Python 3.11+:

```sh
python3 -B proofs/replay_original_layout.py -- sh -c \
  'cd proofs/research && python3 -B main_existence_attempt/ancestry_direct_pass/delay/check_delay.py'
```

**Status: `COMMAND_INSPECTED`.** It has not been executed in this audit; no `EXPECTED_OUTPUT_CONFIRMED` claim is available.

The inspected child checker has no external input-file dependency: it contains its seed and recomputes ordinary integer reversals, column additions and bounded controls. It writes `delay_289_trajectory.json` and `check_delay.json` alongside its restored source. The assertions verify the specified 289-step first positive palindrome hit and finite-depth statements; they do not prove unbounded delays, decimal Lychrel existence, or a result for the orbit of 196. [Full historical checker](https://github.com/taco-jpg/p196-algorithm/blob/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/research/main_existence_attempt/ancestry_direct_pass/delay/check_delay.py)

### Canonical generators and scope boundary

The historical Agent110 `integration/reconcile.py` explicitly generates its Agent110 block in `REPRODUCE.md` through `docs()`. Its reconciliation mode also requires frozen review evidence, specific historical Git objects, staged publication contents and the recorded integration state. It is **not a generic current documentation generator**. The current task should not hand-edit its generated block or rerun it to update unrelated current instructions. [Historical canonical generator](https://github.com/taco-jpg/p196-algorithm/blob/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/contributions/agent-110/integration/reconcile.py)

No evidence status changes follow from this correction: source publication, Lean checking, independent review and integration remain separate. This scouting report is not independent review of its own proposed wording.
