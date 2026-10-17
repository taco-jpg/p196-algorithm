# PR151 retained checkpoint classification

## Result

The source owner's retained checkpoint already contains successful author evidence for all 31 reserved exact identities. New proof development would duplicate that work. I performed no Lean execution and changed no owner source, branch, remote, or main file.

The reuse candidate is the untouched recovered package at `recovered-checkpoint/boundary-table-transcription-20261016/`. Its status is **retained author evidence, statically bound; complete-family fresh rebuild and independent acceptance pending**. The source owner remains Agent53. This report does not establish permission to publish or integrate the recovered package.

## Provenance and preservation

- Original archive: `/workspace/scratch/c04cf11f6ff8/agent53-boundary-table-transcription-checkpoint.tar.gz`.
- Preserved byte-for-byte copy: `agent53-boundary-table-transcription-checkpoint.tar.gz`.
- Archive length: 1,371,967 bytes.
- Archive SHA256: `2aa584fa4fe18d30ccdeabc4fbda97996b94d833fa025dc4df9a2ff9dc7a3b4d`.
- Original runtime workspace `/dev/shm/p196-agent53-c04cf11f6ff8` is absent.
- `checkpoint-discovery.json` records all archive member names, types, and lengths. No archive scripts were executed.
- `recovered-checkpoint/extraction-manifest.json` binds the 356 extracted regular files by member name, length, and SHA256. Extraction was limited to this contribution's source/evidence package, parser-strategy records, and independent-review preparation. The complete original archive preserves the other research/runtime records without deletion.

The public PR head supplied for this task is `a05ac1a31de7e5edb0a1eca24af344fbcf80b883` and actual main base is `74a1c3922eb7af438fe40b23d2105ad07556e3f5`. The recovered `Agent53RootRanks.lean` is identical to its published-H counterpart. The recovered dependency manifest is identical to the published manifest. Each of the four retained author-clean dependency source files exactly matches the task's already remotely bound dependency bytes and Git blob IDs.

## Completed source scope and exact evidence

`checkpoint-classification.json` independently recomputes source hashes, hashes of the actual retained attempted sources, receipt hashes, exact argv, raw-log hashes, actual recorded exit codes, and endpoint axiom reports. Its classifier is `classify_checkpoint.py`; `classifier-run.json`, `classifier-run.stdout`, and `classifier-run.stderr` record its successful execution. Earlier classifier/report versions are preserved with `.v001` suffixes. Classification launches no Lean process.

For every one of the 31 endpoints:

1. The top-level candidate source equals the source hash in `FULL_SCOPE_MANIFEST.json`.
2. Its bytes equal the retained source from the actual successful attempt, and the attempt receipt binds that same source hash.
3. The receipt records actual exit code 0 and the required `-j1 -DElab.async=false --trust=0` flags.
4. The raw log prints the exact exported endpoint with only allowed axioms.
5. The source declaration is the advertised unconditional `BoundaryCertificate.x = BoundaryCertificate.xK` proposition.

The full table family is graph1–graph7, ranks0–ranks7, maps0–maps7, rootRanks0–rootRanks7. It has 37,686 entries. A separate Python source-only comparison checked every literal number in complete order, length, and multiplicity against the pinned original encoded strings. This is a transcription control, not a Lean theorem or substitute for rebuilding.

| Family | Endpoint count | Retained successful source/receipt locations | Method |
| --- | ---: | --- | --- |
| rootRanks0 | 1 | `development/attempt-001/` | Original parser equations and `simp +decide` |
| rootRanks1, ranks0, maps0 | 3 | `development/attempt-003/` | Original parser equations and `simp +decide` |
| rootRanks2–rootRanks7 | 6 | `development/attempt-005/` | Proven ASCII parser correspondence, then kernel `decide` |
| ranks1–ranks7, maps1–maps7 | 14 | `development/attempt-006/` | Proven ASCII parser correspondence, then kernel `decide` |
| graph1 | 1 | `graph-development/Graph1-v4-staged.*` | Exact staged parser states and numeric conversion proofs |
| graph2–graph7 | 6 | Successful `graph-development/GraphN-*.json/.log/.lean.txt` records | Proven ASCII parser correspondence, then exact `decodeEdge` congruence |

Graph receipts do not contain their own original raw-log hashes. This report preserves that distinction: those logs are now bound by archive/member/current hashes and inspected for exact endpoint axiom output, without inventing a historical hash field.

## Mathematical method and feasibility

The shared `Agent53TableParsing.lean` has SHA256 `e375d0420101fcbc09fafe65f89f41356248469f53b2cdc508de209e3a8f3dfa`; its successful source snapshot and receipt are in `development/attempt-005/`. The same frozen source has a retained parser-strategy successful receipt.

The generic theorem `Agent53TableParsing.parseNats_ascii` proves that the unchanged original `BoundaryCertificate.parseNats` equals a structural character-list parser under the premise that every input character has UTF-8 width one. Its source establishes ASCII byte-position/get/extract/fold semantics, simulates the original single-space split cursor, preserves each token's ASCII condition, and proves exact `String.toNat?` semantics. Empty or invalid tokens retain the original split/filterMap behavior. Concrete endpoint modules discharge the width premise with ordinary `by decide`; it is not an endpoint hypothesis.

For array endpoints, congruence through `List.toArray` transports exact list equality. For graph endpoints, congruence through `List.map BoundaryCertificate.decodeEdge` preserves the full original ordered decoded edge list. No replacement original declaration or set-level equality appears in these endpoints.

This approach is already realized in retained successful sources for every table; feasibility no longer depends on devising another proof method. Kernel checking and independent semantic acceptance still require the new full source build/review. The initial parser-equation method retains Agent414 attribution. Graph0, exterior exclusion transfers, decimal dynamics, and conclusions about 196 remain outside this work.

## What has actually been rebuilt historically

- `verification/author-clean-001/report.json`: author PASS, **four endpoints**, nine modules; includes a very large type printout of unsafe compiler artifacts.
- `verification/author-clean-002/report.json`: author PASS, **five endpoints**, ten modules; 284 safe constants, including 140 theorem constants, and 38,571 separately recorded unsafe compiler artifacts.
- `FULL_SCOPE_MANIFEST.json`: all 31 individually author checked, explicitly `complete_family_fresh_build: NOT_RUN`, `independent_review: INCOMPLETE`.

The old five-result checker is not evidence for a full-family build. The recovered complete-family mathematical sources were built in author increments using already built dependencies. Their historical success does not discharge the required independent fresh source-closure gate.

## Retained verifier status

`check.py` and `BUILD_REGISTRY.json` are the executed five-endpoint checkpoint. `development/check-full-scope.wip.py` is explicitly unfinished and was not executed here. It includes useful repairs: optimization rejection, 300-second default timeout, `-s65536`, source/object hash checking, exact safe-name/type-name correspondence, unsafe inventory checks, and expected module-marker coverage.

The WIP cannot run unchanged:

1. `PACKAGE` resolves to its `development/` directory, which lacks the expected manifests.
2. `BUILD_REGISTRY.json` still has only five endpoints and lacks `expected_axiom_prints`.
3. The retained `Agent53Audit.lean` imports/audits only the old nine dependency/proof modules, lacks `A53_MODULE` output, and has only five exact proposition examples.
4. Its import ordering does not match the WIP's generated expected `['Lean'] + modules` order.
5. The final full-family source hashes, registry, audit, and verifier must be frozen together and tested.

A full closure uses the four unchanged dependencies, the shared parser, 31 endpoint modules, and a diagnostic audit module: 37 source modules total. The parser must precede all modules that import it. Each endpoint's source and imports are explicitly recorded in the classification JSON. No new implementation of the mathematical proofs is required.

## Resource facts and preserved failures

The supplied compiler binary's current bytes hash to `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`, matching the historical official Lean 4.19.0 identity. I did not execute it, including for a version query.

Successful historical graph4–graph7 commands used `-s 65536`; graph4's earlier identical source failed with exit -6 and a stack-overflow log at the default stack. The largest recorded successful graph peak is 2,288,136 KiB. Large modules should run sequentially with actual bounded per-process time/resource receipts. The historical `-M` flag was unsupported; it must not be advertised as an active limit.

The classifier identifies 18 recorded nonzero attempts across contribution and parser-strategy receipts, including exits 1, -9, -6, and -11. This count is a bounded receipt classification, not a claim that every setup/probe failure had a JSON exit field. All original attempts and raw logs remain in the untouched archive and extracted research subtrees. No failed source or evidence was replaced or deleted.

## Next action for the delivery owner

Reuse the frozen recovered proof sources after the source-owner coordination boundary is resolved; complete the registry and diagnostic verifier; obtain a fresh full-source rebuild and genuine independent review of the exact frozen package; then publish and hand off through the authorized ownership process. A new partial rootRanks proof extension would duplicate finished author work and would leave the actual missing gates unresolved.
