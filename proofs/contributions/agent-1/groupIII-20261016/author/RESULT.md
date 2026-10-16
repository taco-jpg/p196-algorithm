# Agent #1 Group III author result

The two new roots compile under the pinned Lean 4.19.0 compiler with `--trust=0`. The author axiom audit passes. Independent clean rebuild and acceptance are owned by the separate reviewer and parent; this report does not substitute for them.

## Exact result

Namespace: `P196.Agent1.GroupIII`. For every `r,p,u,v : Nat` satisfying `r>=1`, `1<=p<=4`, `10<=u<=13`, `5<=v<=6`, and `u+v<=18`, the domain has exactly the seven written Group III cores. `numeric_delayed_return` quantifies arbitrary original canonical digits of an ordinary integer whose finite pair word is `DelayedOverlapGate.initial r p u v`. It proves that its first two positive reverse-and-add iterates are nonpalindromic and its second iterate has unchanged canonical width `2*r+7` and finite pair word `shiftOne (returnedComponent r p u v)`.

`realized_safe_gate` proves existence of a positive canonical realization for every domain tuple. `numeric_middle` also supplies unchanged canonical width and the exact intermediate pair word. The core proves both component and whole two-step returns, four explicit carry certificates and terminal-zero carries, and the exact coefficient defect. `actual_intermediate_overlap_fails` states genuine first departure directly using the zero extension of the actual finite component update; it does not use unrepresented tails of `nextColumns`.

The returned component is the six-column word with outer coefficient `4p` and central coefficients `(2,4u-39,4v-17,4v-17,4u-39,2)`, with zero runs of length `r-1`. The additive definition of the whole intermediate word includes the shortest `r=1` boundary. There is no unproved realization or carry premise. The result makes no later-return, recurrence, first-palindrome-time, or Lychrel claim.

## Provenance and boundaries

Written source: retained `renewal_pass/constructive/STATUS.md`, section 1, original blob `d684dc1865a3e59e1c699ad1ec28a4dbec0a74e2`. Original definitions and theorems remain unchanged. The six pinned dependencies are `LychrelDigitSums`, `SafeDelay`, `DecimalSafeRuns`, `DecimalDelayBridge`, `PairDelayBridge`, and `DelayedOverlapGate`. The generic finite-prefix transition helper and original canonical bridge are reused; no Group I domain hypotheses enter the new results. Full source pins are in the contribution's `source-pins.json`.

## Executed evidence

- `baseline/run.json`: fresh compilation of all six pinned dependencies, all exit 0.
- `attempt-001/run.json`: five-theorem carry/admissibility checkpoint, exit 0.
- `attempt-002/run.json`: retained failure at large `middle_next` tactic traversal; no accepted object from this attempt.
- `attempt-003/run.json`: retained failure at two `middle_not_bad` local evaluations after all transition and defect proofs elaborated; no accepted object from this attempt.
- `attempt-004/run.json`: final roots both exit 0, no diagnostics. Core 88.039 seconds, numeric 0.315 seconds.
- `audit-001/run.json`: author audit exit 0. Literal `#print axioms` for all 27 public endpoints; exhaustive module-origin axiom checking for all 471 new-module theorem declarations, including generated helpers. Axiom union exactly `[Classical.choice, Quot.sound, propext]`. No custom axioms. This uses the author build and is explicitly not the independent fresh rebuild.
- `source-scan.json`: both final roots pass the retained verifier's comment/string-aware forbidden-token scan.

Every build used the executable `/workspace/p196-tools/lean-4.19.0-linux/bin/lean`, SHA-256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`, arguments `--trust=0 -j1 -DElab.async=false`, explicit `LEAN_PATH=/workspace/p196-agent1-session-20261016/groupiii-author-build`, and that same build directory as cwd. Complete argv, environment, source/log hashes, and exits are in the run records. The preserved `run_build.py` and `run_audit.py` record author execution mechanics; the reviewer has its own fresh-directory runner.

Final source hashes:

- `Agent1GroupIII.lean`: `2adaef1e36b3a56022ac893251436f29c83e1d83d5e52b98a99a6cf7de7f0577` (22 public theorems).
- `Agent1GroupIIINumeric.lean`: `d9633f976619f74d569117d9fbb6ddd2907bca4dbf0dd570c802be12aedb023c` (5 public theorems).

Source-ready coordination was posted with exact body readback at https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6224930794. This specialist performed no Git mutations or publication; the parent remains the sole integration writer.
