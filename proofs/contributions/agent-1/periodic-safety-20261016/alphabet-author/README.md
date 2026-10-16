# Periodic safety alphabet author evidence

Frozen source `proofs/Agent1PeriodicSafetyAlphabet.lean`:
SHA256 `ec2632bcdfc630947844098f09f54161e2bd4ab3473f0e4a139ec6bc2d56912c`;
Git blob `e5c1480c24770054ff24b7c770e457a5162a7d26`.

This module exposes finite-list facts needed by the original periodic-state safety test. It imports the frozen `Agent1PeriodicValidity` closure. It defines neither `safePeriodic` nor a competing `BadWord` criterion, and it makes no safety-preservation or orbit assertion.

Checked public interfaces in namespace `Agent1.Periodic`:

- `mem_pow_iff (w : Word) (k x : Nat)`: `x ∈ pow w k ↔ x ∈ w ∧ 0 < k`. This includes empty blocks and zero powers.
- `mem_periodicWord_iff (B H w : Word) (k x : Nat) (hk : 0 < k)`: `x ∈ periodicWord B H w k ↔ x ∈ B ++ H ++ w`. There is no nonempty-block, bound, symmetry, or validity assumption.
- `periodicWord_head (B H w : Word) (k : Nat) (hk : 0 < k) (hw : w ≠ [])`: the whole word's `headD 0` is that of `B ++ w`. The elementary head argument already existed inside `periodicWord_canonical`; this is its exposed minimal-domain interface, not new normalization arithmetic.
- `mem_stripped_alphabet_iff (B H w : Word) (x : Nat)`: membership in `(stripPeriodSuffix w B).1 ++ (stripPeriodCenter w H).1 ++ w` is equivalent to membership in `B ++ H ++ w`. Empty w is handled explicitly, so no nonempty premise is needed. All discarded symbols belong to the period still stored in both alphabets; the existing decomposition theorems suffice, with no reproof of maximality or termination.

The intended interpretation comes from preserved Python `periodic_word_quotient.py`, blob `c7b87ad87287a7fafb6849c2e6cf9c4cd4ebe72a`, whose `safe(s)` computes the alphabet of B,H,w. This module supplies only its finite alphabet/head interfaces. The other author owns the executable safety Boolean and original BadWord correspondence.

Executed checks:

1. Seventeen prior checked dependency source/object pairs were reused from `/workspace/p196-agent1-session-20261016/validity-parent-clean-001/agent1-periodic-validity/source`. Sources matched the current pinned registry byte-for-byte and by SHA256. Every reused olean hash is recorded in `reused-dependencies.json`. No fresh dependency rebuild is claimed for this author task.
2. The actual Lean4.19.0 compiler executable/version/hash and source HEAD are recorded in `compiler.json`. All executed source/audit commands use `--trust=0 -j1 -DElab.async=false`.
3. `attempt-001/` preserves the genuine first failed source and diagnostics: simplification left a trivial propositional goal, and arithmetic automation did not resolve membership disjunctions. Its incomplete inferred declarations are rejected and not part of the accepted chain. `attempt-002/` replaces those steps with explicit disjunction proofs and passed. Both full snapshots, logs, commands, timings, and exit codes remain.
4. All four literal exported theorem axiom prints passed. `audit-001/AlphabetAudit.lean` then selected every declaration by actual module origin: all9 theorem/safe constants passed, zero unsafe implementations, no custom axiom, transitive union exactly `propext`, `Quot.sound`.
5. Final accepted-source forbidden-token scan passed; `frozen-receipt.json` records the results and freeze pins.

The frozen source is ready for parent publication and a separate combined fresh closure/review. This record claims executed incremental author verification only. For a full fresh reproduction, stage and compile `reused-dependencies.json` sources under their module names in registry dependency order in an empty directory; then execute the accepted source command from `attempt-002/result.json` and audit command from `audit-001/result.json`, with LEAN_PATH set to that directory. `run-attempt.py` is the exact source-preserving incremental driver used here.
