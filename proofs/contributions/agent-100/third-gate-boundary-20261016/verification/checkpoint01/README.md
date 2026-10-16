# Third-gate checkpoint01 independent verification

Executor: Agent #100 `runtime_setup` child, separate from the source authors. Three new modules contain 28 named theorem exports: Boundary 8, Numeric 12, Controls 8. The exact import closure contains twelve modules. The full audit also checks 45 inherited named endpoints and every theorem constant, including generated auxiliaries, in the twelve selected modules.

Read `result.json` for the completed execution outcome. `statement-review.md` records the precise semantic scope, and `statement-inventory.json` pins all 28 new signatures. `registry.json` fixes every dependency path, SHA256, Git blob and import list. `source_baseline` is the actual Git worktree base, not a claim that the new sources were already committed there.

## Replay from any matching Git checkout

Set `REPO_ROOT` to a checkout containing these exact sources and retained verifier/harness files, `LEAN_BIN` to the Lean 4.19.0 executable, and `FRESH_OUTPUT` to a nonexistent writable directory. No original scratch path is needed.

```bash
python3 "$REPO_ROOT/proofs/contributions/agent-100/third-gate-boundary-20261016/verification/checkpoint01/replay.py" \
  --lean "$LEAN_BIN" \
  --output "$FRESH_OUTPUT"
```

The launcher discovers the checkout root using `git -C` relative to its own resolved location. It verifies registry and shared-wrapper hashes. The shared wrapper preserves all six historical source pins and calls the unchanged `verify_project__214bf7673efe116b.py`. That verifier validates every source hash/import, requires the exact root closure, copies source into the new output, compiles with direct Lean, checks all 73 named endpoints, and audits all selected theorem constants against `propext`, `Classical.choice`, and `Quot.sound`. Unsafe implementation axioms remain separately inventoried.

The original verifier retains its historical `Agent #1` report label. This run's supplemental invocation receipt records the actual `Agent #100 runtime_setup` executor. That label is fixed in the shared historical wrapper; third-party replays must separately record their own actual execution identity rather than treating the fixed label as proof of who ran them.

The build uses the official precompiled Lean standard library; it does not require a native Lake rebuild. The recorded compiler version and binary/library hashes are in the original verification report. Output directories must be fresh, and no cached project `.olean` is used.

## Evidence and historical exclusions

`evidence.tar.xz` contains the twelve exact staged source files, ProjectAudit source, all compilation/audit logs, unchanged original report and FILES manifest, actual invocation receipt, review/harness files, and byte-preserved development history. `evidence-manifest.json` lists each archive member's hash and byte length. `result.json` and the archive manifest remain outside the archive to avoid circular hashes. All archived members are reread and compared byte for byte after packaging.

Files under `history-excluded/` are development attempts, including failures and author self-checks. None substitutes for this independent clean build. Binary `.olean` files are omitted because the source-pinned replay regenerates them.

`prepare.py` was used before compilation to assemble this registry after all three hashes were frozen. Normal verification replay uses `replay.py`; rerunning preparation is unnecessary and would record a different preparation base if the checkout HEAD changes. `finalize.py` only packages a completed build and never invokes Lean.

## Mathematical scope

For the actual initial `(1,1,6)` family and every spacer `r≥1`, component and whole at time six have respective widths `2r+7` and `2r+8`, but outer pair coefficients 14 and 15. Thus the specified third two-step `shiftOne` overlap repair fails within the valid first column. The result transfers to every ordinary integer realization with the stated initial pair sums. It does not assert nonpalindromicity at times five or six, exclude every possible re-encoding or later return, establish infinite renewal, or settle a Lychrel/196 statement. The global accepted catalogue is unchanged.
