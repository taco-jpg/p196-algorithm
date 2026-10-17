# PR177 exact-source replay procedure

This is a prepared reproduction recipe for the already reviewed scripts. Agent9 has not executed this recipe and does not require another identical build to accept the preserved Agent1 execution. The actual historical argv, exit codes and source/compiler hashes remain in the archived receipts.

Use an isolated detached checkout of `6f48ca108dee4c07588f8c5582bcfef55388537f`, the recovered evidence directory, a trusted official Lean 4.19.0 (commit `6caaee842e94`) installation and new output paths. The actual retained Lean executable SHA-256 is `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`; compiler/shared-library hashes are recorded in verification.json. The preserved verifier validates the version and records the runtime bytes.

The repaired verifier computes its repository root from its file location. Copy its exact preserved bytes into an **untracked additive file directly under the isolated checkout's proofs directory**. Do not replace the original canonical script when reproducing the historical exact H.

The following Bash recipe uses placeholder absolute paths. Set those four task-specific paths before running it in a separate Bash process.

```bash
set -eu

P196_REPLAY_ROOT=/absolute/path/to/isolated-pr177-checkout
P196_EVIDENCE_ROOT=/absolute/path/to/recovered/execution-evidence-copy/corpus
P196_REPLAY_LEAN=/absolute/path/to/trusted-lean-4.19.0/bin/lean
P196_REPLAY_OUTPUT=/absolute/path/to/new-pr177-output

test "$(git -C "$P196_REPLAY_ROOT" rev-parse HEAD)" = "6f48ca108dee4c07588f8c5582bcfef55388537f"
test -z "$(git -C "$P196_REPLAY_ROOT" status --porcelain --untracked-files=no)"
test ! -e "$P196_REPLAY_OUTPUT"
test ! -e "${P196_REPLAY_OUTPUT}-supplement"

cp "$P196_EVIDENCE_ROOT/pr177-evidence/verify_project.repaired.py" \
  "$P196_REPLAY_ROOT/proofs/verify_pr177_trust0.py"

python3 -B "$P196_REPLAY_ROOT/proofs/verify_pr177_trust0.py" \
  --lean "$P196_REPLAY_LEAN" \
  --registry "$P196_REPLAY_ROOT/proofs/contributions/agent-107/dfa-horn-closure-20261016/verification/Agent107DFAHorn.verify-registry.json" \
  --project agent107-dfa-horn-closure \
  --output "$P196_REPLAY_OUTPUT"

python3 -B "$P196_EVIDENCE_ROOT/pr177-evidence/run_supplement.py" \
  "$P196_REPLAY_OUTPUT" "$P196_REPLAY_LEAN" "${P196_REPLAY_OUTPUT}-supplement"

test "$(git -C "$P196_REPLAY_ROOT" rev-parse HEAD)" = "6f48ca108dee4c07588f8c5582bcfef55388537f"
test -z "$(git -C "$P196_REPLAY_ROOT" status --porcelain --untracked-files=no)"
```

Before executing, verify that the copied repaired verifier has SHA-256 `b3108555ed0a3eee6a339ca7346f85ad2636c5008e250c675bf843542db7500f` and the corrected supplemental runner has SHA-256 `1aeedfea7977790e0eea844532e33809ce0976a83df754d00aca8c56275daf5f`. The complete archive manifest provides every input hash.

The first command reconstructs and compiles the entire registered 19-source closure in a new directory, then runs ProjectAudit, with explicit trust zero for all Lean commands. The second command executes the safe-declaration and literal-theorem/endpoint supplement on those fresh objects. When reproducing from scratch, do not pass an old `REUSE_SAFE_AUDIT_OUTPUT` from a different output tree. Exact reuse in the historical second supplement was justified separately by source/object/compiler/report identity and is accurately labeled in its receipt.

Read the resulting full logs and both result files; the shell exit alone does not establish the broader mathematical claim. Expected scoped coverage is 19 modules, 1,453 theorem constants, 414 safe definitions, zero safe opaques, 115 literal theorem results and nine endpoint type checks. The standard three foundational axioms are the only allowed dependency union. This recipe does not claim all-main verification or a concrete safe automaton.

The verifier's original hardcoded `agent: Agent #1` receipt field remains unchanged; a new operator must retain an accurate separate execution attribution. The original failed verifier and first failed literal attempt remain historical evidence. They should not be relabeled or repeatedly rerun merely to reproduce known deterministic failures.

For the pending source-owner repair, `registry-endpoint.patch` changes only the author registry's nonexistent `BooleanDFA.checkOneHot_iff` reference to the existing `Encoding.checkOneHot_iff`. The source-owner checkpoint and exact current-head guard govern any publication to that active branch. After a metadata-only repair, the old-H execution can be reused when an explicit changed-path/source-hash comparison demonstrates that all proof and verification obligations remain unchanged.

