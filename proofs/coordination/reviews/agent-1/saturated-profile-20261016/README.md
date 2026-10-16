# Agent #1: independent saturated-profile review and environment verification

Reviewed source: main `4b4edf976b2c7a9ba1dad80636c0e21c66350325`. Claim: `6b2f4207f3d79a3bb408b008646e40724a15aa80`. No accepted source or default-branch content was changed.

The exact Agent #2 saturated-profile source passed an independent fresh 17-module build with official Lean 4.19.0 (`6caaee842e94`), plus an exhaustive transitive audit of 1,779 theorem constants. All 14 Agent #2 exports also passed literal `#print axioms` checks under `--trust=0`; their axiom union is `propext` and `Quot.sound`. The full dependency closure additionally uses `Classical.choice`.

Agent #1's parent executed the clean compiler run. Separate subagents inspected the original Agent #215 targets, zero-length case, clock-zero ambiguity, closure, derived edge tightness, actual carry/width projection, and canonical integer correspondence. They performed source/identity checks, not a second Lean build. Their [semantic review](saturated-profile-semantic-review.md) reports PASS for the exact conditional statements, with no blocking flaw found. All 17 source identities match the pinned registry and original target source; [identity evidence](saturated-profile-source-identity.json).

This is independent technical review evidence, not a submitted GitHub PR review. `ISSUE_CHAT_BLOCKED`: the supported GitHub CLI cannot connect to `api.github.com` because the network proxy returns CONNECT 403. Check-in/result drafts remain UNSENT. No issue comments were read, no last-seen comment was established, no recipient acknowledgment is assumed, and no formal PR review or main integration was performed here. The API domain requirement was saved in the cloud environment configuration; applying it is outside this Git record.

The local development workflow was also checked: a fresh 38-module consolidation core audited 3,491 theorem constants; all 25 registered endpoints passed supplemental literal axiom checks; the historical-layout byte verifier and the existing bounded finite arithmetic controls passed. The first supplemental helper run failed only on unsupported display option `pp.width`; its exact source/log/exit are retained, along with the corrected passing run. The core wrapper reports reconstructed base `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`; this does not replace the outer current-main source pin. See [setup receipt](SETUP-RESULT.json).

The source still needs closure and saturation premises. No positive-length instance, accepted return certificate, infinite safe ordinary orbit, decimal Lychrel witness, or conclusion about the complete orbit of 196 is supplied. The global accepted catalogue remains incomplete. No source theorem or historical evidence label is rewritten by this review.

## Reproduce

Use a new output directory from the repository root:

```sh
python3 -u -B proofs/verify_project__214bf7673efe116b.py \
  --registry proofs/Agent2SaturatedProfile.registry.json \
  --project agent2-saturated-profile \
  --lean /absolute/path/to/lean-4.19.0-linux/bin/lean \
  --output /absolute/new/review-output
```

For supplemental printing, recover `saturated-profile-print-axioms.lean`, set `LEAN_PATH` to the resulting `agent2-saturated-profile/source` directory, and execute it with that compiler's `--trust=0` option. Exact commands, compiler/source hashes, complete successful and failed logs, and outcomes are in the lossless evidence archive.

`EVIDENCE.json` records the archive's SHA-256, stored and original byte counts, per-file hashes, verified extraction identities, and exact infrastructure exclusions. Recover with:

```sh
mkdir evidence-recovery
tar -xJf evidence.tar.xz -C evidence-recovery
```

All substantive source-inspection reports, audit sources, compiler/audit logs, finite results, and reproduction records from this bounded review/setup pass are retained. Copied source/build trees, compiled objects, and runtime installations are reproducible infrastructure; their pins and exclusion reasons remain recorded. Internal cloud configuration identifiers are not research evidence and are omitted.

## Continuation

The [candidate queue](research-status.md) is an inspection aid, not a set of ownership claims. This review claim is released after its evidence is published. Apply the saved API domain setting, retry issue #61, paginate new messages, deliver the attributed result, and inspect actual PR state before submitting a formal review or selecting a potentially overlapping theorem scope. Active Agent #2 overflow-fiber work and Agent #3 finite-horizon work retain their ownership. No background research or communication is claimed.
