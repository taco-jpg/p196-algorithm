# Completed independent acceptance: Agent 4 whole-word bridge

**PASS.** The exact five-module local source closure at `4ffba5a60b6089075f6e3e4ab5952eb6bc46a4d7` has been rebuilt from source in a fresh outside-repository directory, and every local theorem constant has passed a complete transitive axiom audit. The frozen concrete scope-witness module published at `c8fb8bca4160f3dfdb577b17405d2845bf6dbb12` has also compiled and passed its exhaustive audit without alteration.

This completes the execution gates left pending in `../semantic/SEMANTIC_REVIEW.md`. That semantic report, the original preparation checkpoint, the original proof sources, and the witness source remain unchanged. The semantic review found no statement mismatch or missing condition in the six exports. This acceptance is an independent internal replication and scope review; it claims no new theorem ownership, novelty, human peer review, or P196 result.

## Exact formal coverage

| Freshly compiled module | Explicit source theorem declarations | Compiled theorem constants audited |
|---|---:|---:|
| LychrelDigitSums | 297 | 986 |
| PrefixModel | 0 | 7 |
| SaturationCertificate | 18 | 36 |
| SaturationTheorem | 10 | 35 |
| WholeWordBridge | 6 | 28 |
| **Original local closure** | **330** | **1,092** |
| ReviewScopeWitnesses | 9 | 24 |

The compiled counts include private/generated theorem constants and are audit metadata, not counts of independent mathematical results. All original closure axioms are contained in `{propext, Classical.choice, Quot.sound}`. Each of the six named `WholeWordBridge` exports depends on exactly `{propext, Quot.sound}`. Every scope theorem uses either no axioms or exactly `{propext, Quot.sound}`; the two concrete orbit equalities use no axioms.

The official checked-kernel-environment axiom collector traverses definitions, theorem proof terms, opaque values, and referenced types. Its result contains no `sorryAx`, custom axiom, `Lean.ofReduceBool`, or other excluded axiom for any accepted theorem. Source inspection found no sorry/admit, native evaluation, alternate implementation, unsafe metaprogram, or kernel-check bypass in the local theorem sources. Thirteen compiler-generated unsafe implementation axiom declarations in `LychrelDigitSums` are enumerated in the report; none occurs transitively in any of the 1,092 accepted theorem constants. No such declarations occur in the scope module. The allowed-axiom gate was not weakened.

The accepted result is precisely the reviewed conditional bridge: an actual returned three-column sum prefix at saturated width growth implies divisibility of the return time by eight. The numeric endpoint remains the theorem's canonical existential endpoint. No prefix-return or saturation premises for 196 are supplied, no arbitrary positive return is excluded, and no all-time nonpalindromicity argument is added.

## Toolchain and reproduction

Execution used `Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)` with compiler SHA-256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. The runner checked the inspected wrapper/shim and shared-library pins and rehashed **1,303 imported official objects** against the inherited published official release manifest. The official archive provenance is inherited; no new independent download is claimed. The documented shim only redirects the current process's executable readlink query to `/proc/self/exe`.

The original closure used one active compiler process at a time, `-j1 -DElab.async=false`, and no memory or time cap. No pre-existing local `.olean` was supplied. All five local `.olean` files came from the pinned source snapshots in this execution. The scope check then reused exactly those newly built and audited objects, verified their hashes, and independently compiled its own source. Every source, object and compiler pin checked unchanged at completion.

Original build durations were 68.979 s, 3.788 s, 59.738 s, 2.139 s and 1.198 s respectively; the exhaustive original audit took 20.464 s. Scope compilation took 0.606 s, and its exhaustive audit took 2.183 s. Every subprocess exited zero. There were **zero failed compiler or audit attempts**. Peak resource records and complete unabridged compiler/audit output are retained.

The actual commands, directories, exits, timings and hashes are in `attempt01/verification.json` and `scope-attempt01/verification.json`. `rebuild.py` reproduces the fixed original closure in a new build/evidence directory; `verify_scope.py` then checks the fixed published witness against that accepted closure. The original `README.md` remains a historical preparation note. A new replay must use new directories because the runner refuses pre-existing local objects or an overwritten attempt.

## Scope illustrations and evidence retention

The two formerly diagnostic instances are now kernel-checked exactly as stated in `ReviewScopeWitnesses.lean`: `89870` reaches `179745797` in eight ordinary steps, with canonical widths five to nine, returned column-sum prefix `(8,16,16)`, and saturated growth; `770` reaches `176176` in seven steps, with canonical widths three to six and returned prefix `(7,14,7)`, but fails saturation. The latter demonstrates why the saturation condition cannot simply be dropped. These checks make no additional claim about infinite trajectories or novelty.

The independent bounded Python diagnostics remain separately labeled diagnostics. Their 198,882 admitted words and 250,560 trajectory steps do not replace or enlarge the universal theorem statement. The additional palindrome observation in the semantic report is not part of the witness Lean assertions.

`execution-review.json` records the completed build/audit result. `acceptance.json` binds that result to the exact preserved semantic report, diagnostic evidence, witness source, and preflight manifest. `finalize_evidence.py` separately reparsed the complete audit logs and verified each compiler-log hash and zero exit status against the reports.

All new substantive sources and logs are retained. `execution-exclusions.tsv` inventories every one of the 14 clean-build infrastructure files: six duplicate theorem-source snapshots, two duplicate generated audit sources, and six compiled objects, each with exact path, size, SHA-256 and retained source reference. No substantive failed attempt or output is omitted. `execution-file-list.txt` gives the exact retained file set, and `final-manifest.sha256` freezes it except for the manifest itself.
