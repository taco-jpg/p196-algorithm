# Exact periodic safety Boolean: author checkpoint

Agent #1 genuine specialist `/root/verification_plan`, task `agent1-periodic-safety-20261016`, published claim `53448de233d15fdddcc992e4440961f4e3a80f55`.

Frozen mathematical source `proofs/Agent1PeriodicSafety.lean`, SHA256 `d779d12e1ab558bd9135840cbe562ef8a778938e7260a70c3ec1032158b2b979`.

The axiom-free executable definition `safePeriodic` checks precisely the two original Python rejection patterns over `B ++ H ++ w`, with outside coefficient `(B ++ w).headD 0`. It does not expand a repeated word or modify `FoldedDecimal.BadWord`.

Three public theorems:

- `safePeriodic_iff_not_bad B H w k hk hw`: for every positive k and nonempty w, the Boolean is true iff the literal `periodicWord B H w k` is outside the original indexed BadWord language. No bounds, symmetry or realization assumption is inserted.
- `safePeriodic_strip B H w hw`: the exact maximal outer/center stripping algorithms preserve this Boolean, including empty residuals.
- `safePeriodic_quotient_eq_raw B H w hv`: the stripped quotient Boolean equals the raw image Boolean. It is not equated with the predecessor Boolean.

Alphabet/head facts are imported from the separately authored `Agent1PeriodicSafetyAlphabet`. No generic arithmetic palindrome criterion or ordinary-integer bridge is reproved here. Root owns the numeric corollary and fixed counterexamples. This module proves no safety-transition closure, repeated guard condition, infinite orbit, or P196 statement.

## Executed compilation and audit

Official Lean4.19.0 commit6caaee842e94, executable SHA256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.

Attempt004 exit0, 0.259s:

```text
cwd=/workspace/p196-agent1-session-20261016/periodic-safety-author-build
LEAN_PATH=/workspace/p196-agent1-session-20261016/periodic-safety-author-build
/workspace/p196-tools/lean-4.19.0-linux/bin/lean --trust=0 -j1 -DElab.async=false -o Agent1PeriodicSafety.olean Agent1PeriodicSafety.lean
```

The source prints literal axioms for all three exports. Criterion and strip use only `[propext, Quot.sound]`; the quotient corollary uses the standard three foundations. Object SHA256 `966af21c93d98034ba2a07a47ccdf267195b4b203fe0c3bb73e2418d74aee118`.

`audit-002` exit0, 1.487s, uses the same compiler/trust/path settings and `SafetyAudit.lean`. It prints all four public types and literal axiom reports, then audits every theorem constant originating in the new module, including private/generated declarations, and every safe definition. Result: **9 theorem constants, 1 safe definition, standard-three theorem axiom union; safePeriodic itself axiom-free**. Custom axioms, disallowed theorem/definition axioms, and noncompiler unsafe definitions are rejected.

Six compiler implementation definitions ending in `_cstage1`/`_cstage2` are separately inventoried in the audit log and receipt. They are not accepted as logical proofs or used to justify the Boolean specification. All nine theorem dependency audits pass the ordinary axiom whitelist, and the logical `safePeriodic` definition is safe and axiom-free. `audit-001` intentionally rejected the first generated unsafe compiler stage before this distinction was implemented; its exact audit source, driver, log and failed receipt are preserved. The mathematical source was unchanged between both audits.

## Preserved attempts and dependency provenance

- Attempt001 failed because unrestricted `simp` distributed Boolean/list predicates differently, and the generic indexed/membership rewrite needed explicit predicate arguments.
- Attempt002 repaired the indexed proof but selected the logical-negation rather than Boolean-negation simplifier lemma.
- Attempt003 used the correct Boolean-negation lemma but needed an explicit `not_congr` step before rewriting the inner Boolean expression.
- Attempt004 passes with exact endpoints unchanged. All prior immutable source snapshots, logs and command receipts are retained. Failed logs containing auto-generated `sorryAx` are not accepted proof evidence; the final source has no placeholders.

This is an **incremental author verification**, not an independent fresh rebuild. The runner verifies and copies the17 frozen source/object pairs from `/workspace/p196-agent1-session-20261016/periodic-validity-review-clean-001`, whose independent receipt is PASS under trust0. It then copies the separately compiled Alphabet source/object, verifies equality to the live frozen source, and records all18 source/object hashes in each attempt's `dependencies.json`. No original dependency was rebuilt or edited. The parent's independent combined closure review remains separate.

`run.py` requires a fresh attempt directory; `audit.py` requires a fresh audit directory. Root remains sole Git writer. This frozen source and evidence are ready for parent publication/composition.
