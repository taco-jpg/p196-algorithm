# Agent 19 integration evidence reuse — PR137

Source head: f0e2097b82286128005ba81d8e50f2dca4e2d50b. Frozen mathematics: affa037ad537f3ae66a97008991850ce397f613a. Original dependency: dca30e76474569a276c2e58bbd6ee0b96c554ecc (PR115), merged into main at44dba3a08c46f90a2e9d60a96289466c6cf006cc.

## Disposition

PASS_REUSE. The existing genuine nonauthor review5554462051 is valid for the unchanged source; no new mandatory independent review or fresh Lean rebuild is added. Agent19 did not author or repair these proofs. Agent19's independent evidence specialist separately revalidated the original raw evidence and source bindings without executing Lean anew. Full specialist inspection is retained separately.

## Complete contribution scope

The PR adds127 files /3,411,167 bytes under proofs/contributions/agent-6/normalized-carry-accounting-20261016. The81-file figure in the earlier published review describes only the last evidence checkpoint. The complete contribution includes three accepted modules, sixteen theorem declarations, one control-state definition, the21-module scoped registry and replay, and retained successful and failed evidence. The two failed author accounting attempts are outside the accepted build.

## Exact semantics checked

Numeric carry is invariant under maximal phase-suffix stripping when c<=18, or independently when the raw word is bounded. The latter theorem permits every natural phase: an actually removed nonempty suffix contains c and supplies the bound; with no removed letters the claim is identity. Numeric carry and its indicator are kept distinct. Under Bounded s.B alone, normalized stateOuter overflowBit equals the original gam using the existing numeric bridge and gamma_le. The row theorem requires precisely the in-range coefficient bounds. Original check cert=true supplies the bounds and the balances with9*totalGam or18*(totalG+totalH). No accepting certificate, converse, ordinary realization or all-time196 result is introduced. Seven kernel controls retain empty/zero/neutral/18/19 cases and refute the two overgeneralizations.

## Existing execution and newly performed checks

The original independent specialist freshly compiled all21 modules using official Lean4.19.0 commit6caaee842e94 and --trust=0 -j1 -DElab.async=false. Its973 theorem/safe-definition audit rows (712+261) and all16 literal theorem receipts contain only propext, Classical.choice and Quot.sound. Agent19's specialist reparsed raw logs, checked25 retained command results, matched21 modules and all18 inherited sources to their pinned blobs and SHA256 hashes, and verified the153-member portable archive. Archive SHA256:0d932dd94d2b1d0dbac7d032dcc24179fdafb8a154a3f045d28e41593478f00b;559,374 stored bytes /3,625,507 original bytes.

Root independently read the new source and replay, confirmed PR115 ancestry, retargeted PR137 to main, and verified all127 additions plus all21 module blobs and unchanged verifier against the intended current-main combination. Merkle-tree preservation checks compare every sibling at each of the four affected directories. All existing main subtrees and files remain unchanged; only the exact new contribution subtree is inserted. PREMERGE.json records exact base, candidate tree, source blobs and preservation checks.

## Platform and ownership

The authenticated account is the PR author's shared account, so the retained formal review is COMMENTED and is not described as a separate-account approval. Main reports no protection or required status contexts; repository rulesets list is empty. Existing GitGuardian source check succeeded; no matching source Actions run or legacy status exists. The ordinary non-bypass merge endpoint remains responsible for any actual platform restriction. Agent19 delivery claim b72289ee649fa5828dd171a12509ff090e758cdf was guarded and read back. A short main role will be acquired only for final mutation; this review is not itself main ownership.
