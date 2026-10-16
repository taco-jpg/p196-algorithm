# Agent #105 / session 9df76b: numerical inverse boundaries

This contribution formalizes the ordinary decimal reverse-add statements in `persist_inverse_notes.txt`, sections 1–3, retained at Git blob `ecd101823b261fdac15d185fea963d9c9f16c601`. Those written results predate this formalization. The two concrete integers below are this session's canonical realizations of the profiles in the old note.

## Independently reviewed source and full replay

The four flat Lean modules and the 9-module registry `proofs/Agent105InverseBoundaries9df76b.registry.json` are frozen. Each new module has compiled with the official Lean 4.19.0, release commit `6caaee842e94`, at trust level 0. All 38 public theorem endpoints have literal `#print axioms` reports. Reported theorem dependencies are subsets of `propext`, `Classical.choice`, and `Quot.sound`.

The exact published source checkpoint `5923015f86eb1ef898becd77ce2ee328ff338b69` is INDEPENDENTLY-REVIEWED. Separate semantic reviews cover every new module: runtime105 reviewed the three modules it did not author, and scope105 reviewed runtime105's WidthSupport. Scope105 then independently rebuilt the complete nine-module closure in two empty directories. The unchanged canonical verifier passed all ten commands and audited all 1,042 module-origin theorem constants. Because official Lean's help reports a default trust level of `max`, a separate complete replay explicitly used `--trust=0` for every module and the unchanged generated audit. It also passed all ten proof/audit commands; the extra help command passed as well.

Both exhaustive theorem audits report only `propext`, `Classical.choice`, and `Quot.sound`. The canonical audit separately records 22 pre-existing unsafe implementation axioms in imported infrastructure; none is a theorem dependency and none originates in these four new modules. These are reported transparently, not silently removed. No proof, registry, verifier, or audit source was changed between the two successful replays. This is same-session independent specialist review, not external peer review or a separate GitHub account. Integration into the shared accepted catalogue remains the integration owner's task.

The unmodified canonical receipt SHA-256 is `a309168ed0cb803c2c9b20156faab1c9bf4c564da62559d969e39127a9dbdddd`; the explicit trust-zero receipt SHA-256 is `f5c279db93de777711d6c3ae15756e70633015551e9f9754f7f5e647ff6f7320`. Readable copies are `canonical-verification.json` and `strict-verification.json`. The complete semantic and execution assessment is `controls/scope105-final-review.md`.

## Mathematical interfaces

| Module | Precise result |
| --- | --- |
| `Agent105WidthSupport9df76b` | Canonical width and in-range digits are unique; actual output width is source width plus the terminal carry. Different source widths with equal numerical `step` output differ by one, with short-source carry 1 and long-source carry 0. |
| `Agent105CrossWidth9df76b` | Such a collision has short outer column sum 11, long outer column sum 1, short width at least 2, common output first and last digits 1, and output divisible by 11. Any three canonical finite source digit lists with equal numerical output contain two with identical finite `digitPairSums` profiles. |
| `Agent105CrossWidthWitness9df76b` | Fully canonical controls prove `step 200799 = step 1098900 = 1197801` and that this target is not a palindrome. The old note's two finite profiles are recovered exactly. The separate boundary control is `step 29 = step 110 = 121`. |
| `Agent105PalindromeImage9df76b` | For every positive canonical palindrome target of width W, a positive numerical predecessor exists exactly when W is even or its central digit is even. A same-width predecessor with all carries zero is constructed. For W at least 2, one can choose it nonpalindromic, so the first palindrome occurs at time 1. |

The profile bound does not bound the number of integer predecessors by two; Agent101's digit-splitting multiplicity remains relevant. The collision conditions are necessary conditions, without a sufficiency or complete arbitrary-target decoder claim. The palindrome-image iff covers one-digit targets; the first-hit-one result deliberately requires at least two digits. Numeric reversal admits source trailing zeros and removes their leading zeros in the reversed number. No theorem here assumes that infinite digit-function tails are part of a finite canonical representation.

## Dependencies and provenance

The base `Lychrel196Research` source is unchanged, SHA-256 `f8950d138fa4231b536059e2334d36b6496de3d25a806f4cf3925941aa05144c`, blob `c6c1f5441c54a36f2d82b3ef78dff1ccdbc5a506`. Agent101's four digit-splitting modules and all accompanying source/evidence were imported by a genuine merge of exact published commit `326645944168ad2b035a1e653b61527d79684156`; their bytes and authorship are retained. The dependency merge is `43259106e755d501ca88819f373e0a6c1bff3f05`, based on main `ae8bbdfd2a18e8910eebc25fd2a81661c01abc16`.

User-directed task claims were published on `p196/coordination` at `c9ef8561d8ac236117102ddeccc758a541591543`. The isolated contribution branch is `research/agent-105/cross-width-palindrome-9df76b-20261016`. This session is distinct from Agent #105 / session `8f1107db019a`, which owns affine-dynamics work.

## Reproduce

From the repository root, with the unmodified official Lean 4.19.0 executable and a fresh output directory:

```sh
python3 proofs/verify_project__214bf7673efe116b.py \
  --registry proofs/Agent105InverseBoundaries9df76b.registry.json \
  --project agent105-inverse-boundaries-9df76b \
  --lean /absolute/path/to/lean-4.19.0-linux/bin/lean \
  --output /absolute/path/to/new-empty-output
```

The unchanged verifier SHA-256 is `c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a`. This is a scoped project invocation, not a repository-wide accepted-build pass. Its legacy metadata field identifying the verifier's author is not the identity of this session's executor.

## Research evidence coverage

All substantive new source snapshots, failed and successful compiler logs, commands, receipts, scope scouting, and semantic reviews are retained under this directory. Failed attempts are historical WIP and are outside the registry; any failure-time `sorryAx` report is not an accepted result. The two failed proof attempts were repaired in later snapshots without changing the intended statements.

Compiled `.olean` files, duplicate runtime/build caches, the installed toolchain, and operational publication helpers are reproducible infrastructure and are excluded from publication under `PUBLICATION_POLICY.md`. The 46 full verification sources, logs, receipts and file inventories are retained losslessly in `verification-evidence.tar.gz`: 819,489 original bytes, with each member checked again after compression. `VERIFICATION_ARCHIVE.json` gives the exact original path, byte count and hash, archive member, compressed hash, and recovery command. The `FILES.json` inventory records every directly published file in this contribution except itself; archived originals have the separate member inventory. Source identities for all nine actual build modules are recorded in the registry.

The status of 196 and decimal Lychrel existence remains unresolved. These are finite one-step structural results, without an infinite-time claim.
