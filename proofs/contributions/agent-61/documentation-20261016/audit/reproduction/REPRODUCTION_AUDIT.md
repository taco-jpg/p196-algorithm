# Agent #61 reproduction audit

Source pin: `10a173cb635fa8d03e357f454232816fc3e77609`.
Audit date: 2026-10-17 UTC. Specialist assignment: read-only reproduction inspection. The parent is the sole repository/Git writer. This report does not claim review acceptance, integration, a Lean rebuild, or completion of the mathematical project.

The complete role attachment, `AGENTS.md`, and `proofs/PUBLICATION_POLICY.md` were read. Ordinary coordination findings are supplied to the parent for attributed relay through issue #61. No issue or repository mutation was performed by this specialist.

## Recommended smallest coherent increment

Correct `proofs/CONSOLIDATION.md`'s description of the public wrapper commands, mark its historical publication metadata explicitly as historical, and repair its evidence links using the exact entries in `proofs/SOURCE_MAP.json`. This is a documentation change only: preserve the original source bytes, registry, theorem claims, toolchain pins, old verification reports, and historical generators. Coordinate the preservation-map transition with the current migration owner before altering any file selected as a frozen `current` replay input.

The currently claimed `proofs/REPRODUCE.md` and README files should receive the reproduction findings below through their owner. They should not be edited concurrently by this specialist or the parent without a handoff.

## Priority 1: Scope the release verifier to the reconstructed baseline

**Problem.** `proofs/CONSOLIDATION.md:14` says the second advertised command checks publication bytes and complete tracked-file coverage. At the current pin that description needs a baseline qualifier. Lines 97–99 describe regenerated metadata in the present tense. The public wrappers now reconstruct a historical layout before dispatching the original verifiers. This does not check every file of the migrated checkout or every subsequent addition.

**Pinned evidence.** `proofs/verify_release.py:1–5` imports the replay helper and dispatches the historical `proofs/verify_release.py`. `proofs/replay_original_layout.py:20–27` reads the mapping, initializes a temporary shared Git clone, and sets its HEAD and index to `mapping['base']`. The map's line 2 fixes that base at `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`. Lines 28–46 reconstruct all mapped paths; line 48 executes the requested command in that historical tree. The original implementation, now `proofs/verify_release__e7d6c74ed54123df.py:21–29`, uses the reconstructed Git index to define expected coverage. Its lines 73–76 print `complete_publication_coverage: true` and `mathematical_proof_check: false`; the first field is local to that reconstructed tree. `proofs/README.md:18` already explains this restriction correctly.

**Exact replacement for the prose at CONSOLIDATION line 14:**

> Run both commands from the repository root in a complete checkout with Git, Python 3.9 or newer, and enough temporary storage to reconstruct the mapped historical tree. Use official Lean 4.19.0, release commit `6caaee842e94`, and an absolute path to a new, nonexistent output directory for the project command. The public entry points reconstruct the original mainline layout pinned by `SOURCE_MAP.json` to `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`, verify each selected input's recorded SHA-256, and retain that temporary workspace. The project command freshly compiles the registered core and audits its exact theorem endpoints and transitive axiom dependencies. The release command checks publication bytes and tracked-file coverage within that reconstructed baseline. Its PASS does not verify the entire migrated checkout or establish mathematical truth. `--check-only` checks source identity and import closure without compiling project modules; it still requires the pinned Lean installation and is not proof verification.

Python 3.9 is a source-derived minimum for the two canonical verifier implementations because both use `Path.is_relative_to`. It is not asserted to be a minimum for every historical package; the inspected finite delay checker uses `sys.set_int_max_str_digits`, and Python 3.11 or newer is a safe common recommendation for those examples.

**Exact replacement for the non-link prose at CONSOLIDATION line 99:**

> At the recorded consolidation checkpoint, the original manifest omitted 478 tracked proof files, including 132 Lean files. The linked baseline-coverage record preserves those omissions separately from integration regressions. That checkpoint regenerated its byte metadata from the then-selected tracked publication files while retaining historical inventory rows, archived original bytes, and earlier aggregate statistics. These historical metadata and repair records remain evidence for their recorded snapshot; they are not a manifest of the later migrated checkout. Their byte-coverage scope does not complete the accepted-result census or establish mathematical truth.

**Validation status:** COMMAND_INSPECTED. No complete release replay was executed, because reconstruction would copy the entire mapping and exceeded this session's intended disk budget. Do not report a fresh release PASS.

## Priority 2: Explain preservation-map consequences before editing historical entry pages

**Problem.** A normal prose correction can break both public wrappers before they reach a checker. `proofs/SOURCE_MAP.json:354–360` selects the current `proofs/CONSOLIDATION.md` with SHA-256 `ea78a7918cafde6f74dadf9c7c29b174da9fe288648b8d1e38d5d3e5f4359385`. Lines 434–440 similarly select current `proofs/REPRODUCE.md`. The helper does not silently fall back to `preserved` when `current` has changed: lines 32–40 select `current` first and reject a hash mismatch.

**Observed preservation.** Read-only `git ls-tree` against the pin confirmed the original CONSOLIDATION at `proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/CONSOLIDATION.md`, blob `eeb1641cc215c3ee68f9705423ebc47deddd2033`, identical to the map's original blob. The original REPRODUCE is likewise retained at the corresponding archive path, blob `88a4e1d927be6960aa95cebe22112f5c09d6ebdb`.

**Required implication.** Preserve the original records and use the established migration process to keep historical replay selecting exact original bytes while permitting a current corrected reading page. Do not replace the historical `sha256` or `oid` with the new prose hash merely to satisfy the wrapper: doing so would invalidate the original baseline release manifest. No suitable current migration regeneration command was established by this specialist, so that step must remain owned and verified by the migration/integration owner. New edits to `proofs/README.md` do not cause this specific issue because its original record selects `current: null`; the existing root README also selects `current: null`.

**Generator provenance.** `proofs/CONSOLIDATION.md` was generated by the preserved `reconcile_consolidation.py`, now flattened as `proofs/reconcile_consolidation__6958180ab0d167c0.py`. Its line 172 writes the whole document; lines 223–229 write inventory/file-list/manifest outputs. The generator expects original directory depth (`parents[4]`, line 13), historical commits, and explicit metadata captures (lines 42–44); it is not a portable current-tree regeneration command. Preserve it unchanged as historical source. A current correction should be visibly identified as a later navigation/reproduction correction so running a historical generator is not represented as the current publication process.

## Priority 3: Replace stale working-directory instructions with original-layout dispatch

**Problem.** `proofs/REPRODUCE.md:9` says `research/` files retain their original relative locations, and lines 34–41 tell readers to execute commands from `proofs/research/`. Read-only `git ls-tree` at the source pin confirms `proofs/research` is absent. Its source is flattened or archived. The requirements and toolchain paths at lines 24–25 are likewise absent as current tree paths and are preserved through the map.

**Exact original-layout replacement for the delay replay, from repository root:**

```sh
python3 -B proofs/replay_original_layout.py -- sh -c \
  'cd proofs/research && python3 -B main_existence_attempt/ancestry_direct_pass/delay/check_delay.py'
```

This is the general compatibility route, but it reconstructs all 9,161 mapped files before running the lightweight checker. The wrapper command above is COMMAND_INSPECTED, not COMMAND_EXECUTED. It requires a complete mapped checkout, the original base Git object, Git, writable external temporary storage, and sufficient disk space. A shallow export without `.git`, or a sparse checkout missing preserved inputs, is not sufficient for this wrapper.

**Actually executed lightweight alternative for this self-contained checker:** copy only `proofs/check_delay__1a5c84a2538cd825.py` into a fresh disposable directory as `check_delay.py`, verify its source SHA-256 `7a991ed67595339db7bd4f07c3e702f4a352b01541ea8e6f84e38bd46be6925a`, and execute `python3 -B check_delay.py` there. This method is valid for this inspected checker because it imports only the standard library, embeds its finite seed, and writes its two result files next to its own source. Do not generalize it to checkers that require adjacent certificates or local imports.

**Observed result:** exit 0. `check_delay.json` SHA-256 `69890621b0b67fe20d83951f3f92163b4ba867d9e5d3e284960ec7f49f58eb24` and `delay_289_trajectory.json` SHA-256 `1d2eed56dd064058ba47f821cc5bdff2c5bfd2caa50c4e99b2759f9e24244564` exactly match their recorded original map entries. Level: EXPECTED_OUTPUT_CONFIRMED for these two finite outputs only. Receipt and complete stdout/stderr are retained in `delay-replay/`. No additional mathematical conclusion is inferred.

## Priority 4: Specify the actual preflight requirements and outputs

**Problem.** A reader may reasonably interpret `--check-only` as requiring only Python or assume the default verifier performs a quick global status query. Neither is true.

**Pinned evidence.** `proofs/verify_project__214bf7673efe116b.py:63–70` requires `--lean` and `--output` and creates a nonexistent output directory. Lines 93–99 execute the compiler's `--version` and `--print-prefix` and hash compiler/runtime files before reaching check-only mode. Source/import checks read official `.olean` files. Lines 164–165 skip project compilation and set `SOURCE_AND_IMPORT_CHECK_ONLY`. Lines 208–212 distinguish scoped success, incomplete global catalogue, and the returned exit status. Omitting `--project` does not short-circuit the build; in normal mode it can build selected registered projects and only then return 2 for `BLOCKED_INCOMPLETE_ACCEPTED_CATALOGUE`.

**Exact scoped command to document as inspected:**

```sh
python3 -B proofs/verify_project.py \
  --lean "$LEAN_BIN" --project consolidation-core \
  --output "$P196_SOURCE_CHECK_OUTPUT" --check-only
```

Both variables must be explicit absolute paths. `P196_SOURCE_CHECK_OUTPUT` must not exist. Expected successful preflight: exit 0, output `verification.json` with `status: SOURCE_AND_IMPORT_CHECK_ONLY`, `mathematical_proof_check: false`, and `repository_wide_pass: false`, plus `FILES.json` and copied source records. This expectation is source-inspected; no source-only wrapper replay or Lean process was executed here. The complete wrapper also retains an independently named historical-layout workspace.

**Executed supporting check:** `python3 -B proofs/verify_project__214bf7673efe116b.py --help` returned exit 0 with the documented argument names. This direct flattened invocation was used only for argparse help, not presented as a working build command. Running `--help` through the public wrapper would still reconstruct the full mapping before displaying help.

## Priority 5: Use deterministic evidence navigation and separate metadata generation

**Problem.** The historical paths linked from CONSOLIDATION are absent from their advertised original locations in the migrated tree. A basename search risks choosing a duplicate from another branch or an unrelated result. `ACCEPTED_BUILD.json` paths intentionally remain original-layout paths and should not be rewritten to flattened paths merely to fix navigation.

**Navigation rule.** Resolve each legacy path as an exact key in `proofs/SOURCE_MAP.json`. For exact evidence select `current` when non-null, otherwise `preserved`, then verify the selected blob/hash against that row. For a reading-only English rendering, `english_current` can be offered separately and must not replace the original evidence identity. At the source pin, the eight migrated evidence targets in CONSOLIDATION all select `preserved`; the registry and REPRODUCE links remain current. Exact link replacements are retained in `CONSOLIDATION_LINK_MAP.json`. For immutable evidence links, prepend `https://github.com/taco-jpg/p196-algorithm/blob/10a173cb635fa8d03e357f454232816fc3e77609/` to the selected repository path.

**Registry generator.** `proofs/make_accepted_registry__fede06cbdb1651bd.py:14–16` assumes the original directory depth and imports `code_only` from the original verifier. Its line 46 rejects a changed reviewed map and line 100 writes `ACCEPTED_BUILD.json`. It generates the exact fixed 38-module registry and five claim groups; it is not a way to extend acceptance to new packages. It was inspected, not executed. The current public wrapper `proofs/verify_project.py` exports no `code_only`, which is another reason not to run this flattened generator directly.

Historical reconciliation commands printed in REPRODUCE at lines 423, 464, and 514 perform file writes, not just verification. They should be clearly labeled historical publication-generation procedures, executed only with their exact captured inputs and appropriate ownership, outside the shared current checkout. No metadata generator or mutation-based coverage test was executed by this audit.

## Execution ledger and limitations

| Operation | Honest status | Result |
|---|---|---|
| Initial shell read | Attempt failed before command execution | Sandbox setup reported ENOSPC; parent recovered its incomplete clone artifacts. |
| GitHub pinned source reads | Completed | No mutation; files/map retrieved at the exact source pin. |
| Local instructions, source, map, and `git ls-tree` reads | COMMAND_EXECUTED | Current HEAD matched source pin; old research path absent; preserved original doc blobs present. |
| Legacy project implementation `--help` | COMMAND_EXECUTED | Exit 0, argument names confirmed. |
| Isolated finite-delay checker | EXPECTED_OUTPUT_CONFIRMED | Exit 0; both generated file hashes match published map records. |
| Public release/project wrappers | COMMAND_INSPECTED | Full reconstruction not run. |
| Lean build or `--check-only` compiler probe | Not executed | No toolchain installation or download; no mathematical re-verification claimed. |
| Registry, metadata, or coverage mutation generators | COMMAND_INSPECTED | Not executed. |

The session used Python 3.12.14 and Git 2.51.1 for the actual lightweight checks. No full current-tree inventory validation, complete historical-layout replay, GPU/production job, discovery search, remote write, or metadata regeneration was performed. The retained finite replay is a representative arithmetic reproduction check only.
