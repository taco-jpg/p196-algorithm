# Independent strict source replay

**Status: PASS_INDEPENDENT_STRICT_REPLAY.** Agent #5's independent semantic reviewer executed a fresh serialized replay of all seven modules and the exhaustive module-origin axiom audit. This reviewer authored none of the reviewed Lean theorems. The replay used the frozen source hashes in `Agent5ExactDigitStreams.registry.json`, with explicit flags `--trust=0 -j1 -DElab.async=false`.

All **eight compilation/audit commands returned zero**. The exhaustive audit covered **133 theorem declarations** originating in the seven selected modules and checked all **25 fixed exported endpoints**. Their complete transitive axiom union is exactly `{Classical.choice, Quot.sound, propext}`. No custom mathematical axiom, `sorryAx`, or disallowed theorem dependency was accepted.

## Exact evidence

The retained output is `strict-replay-01/`, containing all seven source modules, the generated audit source, the exact registry, raw command logs, compiler preflight logs, and a structured exit/hash receipt. The original parent's generated audit source was copied byte for byte; this independent replay did not regenerate or weaken it.

| Evidence | SHA-256 |
|---|---|
| Registry | `66c54b0cb53225fe3b5dd0112e339aa67cdcf441e895c6d1526dfe7d301a58df` |
| Independent `verification.json` | `b5c97cde66635b2901809b05846390283511925900e2d297557dbeb7a5d7cd9c` |
| Unchanged `ProjectAudit.lean` | `3a08cba84e767c065d1a2fd9caee521d9e8537c3d786435233521619f34be6d8` |
| Independent `ProjectAudit.log` | `14574a495cb06533f17934a34cad172ec84b5552a3013ab41d0167f8e7ed7792` |

Every retained file listed in `strict-replay-01/FILES.json` was checked again against its byte count and SHA-256 after the replay finished. The final four contribution-source hashes match `semantic-source-inventory.json` and the exact identities in `SEMANTIC_REVIEW.md`. All live source hashes remained unchanged throughout the replay.

| Command | Exit code |
|---|---:|
| `OuterFinite` | 0 |
| `TARGET` | 0 |
| `ExteriorFactorizationProof` | 0 |
| `DigitDefinitions` | 0 |
| `AdicDigits` | 0 |
| `FractionDigits` | 0 |
| `CoordinateStreams` | 0 |
| `ProjectAudit` | 0 |

The compiler was official Lean 4.19.0, release commit `6caaee842e94`, with binary SHA-256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. The receipt also pins its shared runtime libraries. Each project module was freshly compiled into a new temporary import directory; no prebuilt project `.olean` was reused. Those reproducible compiled objects were removed after the replay, while the source and execution evidence were retained.

Two compiler-generated unsafe implementation declarations were inventoried separately by the unchanged audit: the `TARGET` module's specialized `List.foldl` implementation for `highValue`, and the `OuterFinite` module's generated representation helper. Neither occurs in any audited mathematical theorem's transitive axiom list. The distinction between these implementation declarations and mathematical proof dependencies is preserved in the receipt.

## Execution and publication provenance

The actual executor was `Agent #5 /root/semantic_review`. The independent driver is `strict_replay.py`; it leaves the existing canonical verifier and every Lean source unchanged. The parent had already executed a separate successful canonical replay. This is the independent execution following that run, with a new output and import directory and an explicit trust-level flag.

The ordinary sandbox initially returned `error: failed to locate application` for compiler version/help preflights. No proof compilation occurred in those failed preflights. `PREFLIGHT_ENVIRONMENT_FAILURE.json` records the observations and their classification. The authorized replay then used the supported `require_escalated` execution mode, after the parent confirmed that this same mode was required for its successful compiler runs. No automatic approval rejection occurred, and no proof, source, or verifier was changed to address the environment failure.

The repository HEAD recorded at source snapshot time was the earlier baseline `4b4edf976b2c7a9ba1dad80636c0e21c66350325`. This metadata is not a claim that all newly reviewed files were tracked in that baseline commit. The exact registry pins and copied source bytes identify the checked source; a later publication replay can additionally bind them to a published commit. This review does not claim a clean published-source checkout or a repository-wide pass.

The combined semantic and compiler verdict is positive for the two explicit finite stream equalities, their digit bounds and prefix consistency, and reconstruction of the unchanged abstract exterior successor for every cutoff at least `B.length+1`. The actual outgoing carry remains an input to the high denominator. Adjacent coordinate-only threshold selection, all-time integer realization, palindrome avoidance, and the 196 question remain outside this contribution's proved scope.
