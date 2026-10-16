# Independent review: Agent105ReturnTimeBound

Reviewer: Agent #105, session `agent105-8f1107db019a`, subagent
`/root/ownership_audit`. The reviewed mathematical source was authored by the
independent subagent `/root/lean_runtime`. The reviewer made no changes to that
source or its two dependencies. See `AUTHORSHIP_CORRECTION.md` for the correction
to an earlier attribution in checkpoint 33474b2b.

## Verdict

**PASS for the stated Agent8 list-dynamics conclusions.** The nine public
theorems retain the required initial canonicality, actual return equality,
head equality where potentials are cancelled, endpoint width information, and
positive-time assumptions. No theorem establishes a returning instance or a
palindrome-free segment. No unrestricted integer statement is inferred.

The reviewed source is `proofs/Agent105ReturnTimeBound.lean`, SHA-256
`93384ce0e3a2443ca37fbb2c510ce927f0f2334509b6430d7b91ff252d0d57f7`.
The source and dependencies were copied byte for byte into an empty external
directory and compiled in dependency order. All four invocations in attempt 001
exited 0, including the independent scope checker. There were no failed Lean
attempts in this review.

## Mathematical checks

1. `orbit_width_potential_bound` applies the lower-potential half of the original
   `Agent8.path_potential_bounds` to `actualExterior` and `actualInput`. Original
   `actual_path_valid`, `actual_path_evolves`, and `actual_width` discharge its
   path and overflow hypotheses. The resulting inequality retains both endpoint
   potentials and both actual list lengths.
2. `return_time_bounds_of_width_gain` cancels endpoint potentials only after
   using the explicit equal-head hypothesis. The original
   `actual_return_bounds` and exact width gain give both `2 * gain ≤ t` and
   `t ≤ 4 * gain`. The source never infers `0 < t` merely from a return equality.
3. The offset theorems retain source and target offset costs with the correct
   signs: `t + 4 * sourceOffset ≤ 4 * gain + 4 * targetOffset`. They do not use
   truncated natural-number subtraction to represent an arbitrary length
   difference.
4. `word_family_return_time_bound` keeps positive slope, shift, and time as
   assumptions and instantiates the exact width gain with `A * s`. The endpoint
   wrappers use only the two displayed length formulas. The natural intercept
   wrapper is not advertised as covering arbitrary negative intercepts; the
   exact-width-gain interface remains available for such tail applications.
5. The original `CanonicalPair` predicate contains nonemptiness, reversal
   symmetry, a symbol bound of 18, and a positive head. It does not require even
   central symbols in odd length. `ReviewScope.lean` kernel-checks both
   `CanonicalPair [1]` and `∀ w, pair w ≠ [1]`. This proves the interpretation
   boundary explicitly: the list predicate alone does not certify an ordinary
   integer's pair-word representation. The reviewed file states that boundary
   and identifies the separate existing Agent109 bridges.

## Verification and evidence

Runtime: official Lean 4.19.0, commit `6caaee842e94`, Release. Executable SHA-256:
`92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.
Every review compilation used `--trust=0 -j1 -DElab.async=false`.

`attempt-001/` preserves source snapshots, raw combined output logs, and the
execution receipt. The reviewed source emits literal axiom reports for all nine
public theorems. All reports use only `propext`, `Classical.choice`, and
`Quot.sound`. The companion six-module canonical audit in
`../../../verification/components/canonical-attempt-001/` additionally scans
every theorem by its defining module, including generated and private theorems.

Reproduction from the repository root, using a previously nonexistent output
directory:

```sh
python3 -B proofs/contributions/agent-105/8f1107db019a-affine-dynamics/review/time-bound/ownership-audit/replay_review.py --repo "$PWD" --lean /tmp/p196-agent105-toolchain/lean-4.19.0-linux/bin/lean --output /tmp/p196-agent105-return-bound-review-replay-NEW
```

The replay script refuses a source-pin mismatch or an existing output directory.
Compiled objects and the runtime are excluded from retained contribution files.
