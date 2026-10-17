# PR151 full-family verifier: independent repair review

## Decision

**PASS for the concrete verifier repair; ready for the parent-owned full clean execution. No blocking verifier defect was found.** This decision is bound to the hashes below. It is not a successful full Lean build, a publication decision, a source-owner acknowledgment, or main integration. The reviewer executed no Lean command, did not run the candidate preparation script, and did not change the candidate or recovered source files.

The inspected repair addresses the earlier partial verifier: the runner fixes the target family at all 31 exact identities; the registry contains the parser and all 31 endpoint modules; the diagnostic audit checks the actual endpoint expression structure and covers the 36 mathematical modules. Together with that audit, the planned run compiles 37 source modules, preceded by two compiler-identity commands.

This review is independent of implementation. I read the complete 292-line `check.py`, 556-line `BUILD_REGISTRY.json`, 191-line `Agent53Audit.lean`, and 189-line `prepare_full_candidate.py`. I also read `DEPENDENCIES.json`, the retained five-endpoint registry and audit, and the repository rules in `pr140/AGENTS.md`. The separate accepted mathematical review is reused as source-semantic evidence; its proof checker and proofs were not rerun here.

## Exact inspected identity

The candidate package is `/workspace/scratch/c68be3818c4b/pr151/candidate/proofs/contributions/agent-53/boundary-table-transcription-20261016/`.

| File | SHA-256 |
|---|---|
| `check.py` | `5f2388e5adcd274a3ccfe3389eebcf98f3c3b0fb6a1079907b7f47d48af3a75b` |
| `BUILD_REGISTRY.json` | `5ca1c89cdafed746d76a7cba18d84e048146a491ae8ae63bb33e647f7c77bc29` |
| `Agent53Audit.lean` | `1c181f7b58541c11d5418bda94892c28b53f6024d2dd128bdccdd118097b29e9` |
| `DEPENDENCIES.json` | `a13bbde623b66b4eec661a47a93b9fb9da7b1b2f8f8ac2826bca351fb02ffb68` |
| `pr151/prepare_full_candidate.py` | `7d9297610d3b5bd2357a891a6fb224bf550017e0606c8074e519580a32d3a61f` |

All five hashes were unchanged after the review's two negative executions. The complete independent inventory, including the SHA-256 of every one of the 37 candidate Lean source files, is in `inventory-and-negative-paths.json` under `source_inventory`.

The compiler was read and hashed without execution: `/tmp/p196-agent5-lean/lean-4.19.0-linux/bin/lean`, SHA-256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. This matches the runner's fixed expected compiler bytes. Its version and git hash remain commands for the full run; this review does not claim to have newly observed those command outputs.

## Assessment of the acceptance logic

### Fixed coverage and dependency identity

The target family is fixed in the Python runner: `rootRanks0..7`, `ranks0..7`, `maps0..7`, and `graph1..7`. The registry must mark the family complete, have the 31-claim count, and match the fixed ordered declaration list, axiom-print list, and original/literal constant pairs. Its proof-module set must be exactly the parser plus the 31 appropriate endpoint modules, including the special `Agent53RootRanks` filename for `rootRanks0`.

The runner independently fixes the following dependency blob identities and checks both each blob and its registry SHA-256 against source bytes:

| Module | Required Git blob |
|---|---|
| `ReverseClosure` | `6e49b1675bb713b7efd594f0f784fae3a4da60a5` |
| `SoficProof` | `7ba0129c374957c684324d8166fcef8488701605` |
| `BoundaryData` | `8c00e1ba6b10b13700eabd21ba6a27f076e8839e` |
| `BoundaryDataK` | `ea5554eb5662a5f23690532d27576a0dc96148be` |

The independent inventory verified these four candidate blobs, all source hashes, and the exact registered import sequence for all 37 source files. Their order is topological: dependencies precede the parser and endpoints, and all mathematical modules precede the audit. `PACKAGE.parents[3]` resolves to the intended candidate repository for this package layout. Each registered source path is resolved and required to stay inside the selected repository.

### Fresh compilation and trust configuration

The runner rejects an existing output directory, creates a new build directory, and copies only validated `.lean` source bytes into it. It does not copy project `.olean` files from the recovered package. Before compiling it checks that no project objects exist in the build directory. The isolated `LEAN_PATH` points to that directory; the subprocess environment is constructed from an allowlist rather than inheriting preload, sysroot, or credential variables.

The compiler bytes are checked before any compiler command. The planned identity commands require Lean 4.19.0 and git-hash prefix `6caaee842e94`. Each source command uses `-j1 -DElab.async=false --trust=0 -s65536`, emits its own `.olean`, records complete stdout/stderr in one log, and must exit successfully. The stack setting is consistent with the retained successful graph executions. Timeout and observed-RSS termination fail the run and retain the command record and log; the RSS field describes sampled process RSS, not a hard process-group resource guarantee.

The token check rejects the listed proof shortcuts after removing comments and ordinary strings. For this concrete source set, the separate semantic review also established the absence of user-defined unsafe proof oracles, new axioms, custom elaborators, or execution commands in the 36 mathematical modules. The token filter is not treated as a universal Lean parser or as mathematical evidence by itself.

### Actual unconditional endpoint types

The repaired audit obtains each endpoint's actual `ConstantInfo` from the imported environment. It requires a theorem with no universe parameters, then requires the complete type to be a three-argument application of the actual `Eq` constant. It checks that arguments 1 and 2 are bare constants with the exact original and literal target names. A proposition with an outer premise or quantifier fails the direct `Eq` shape check. An application, wrapper, substituted expression, or different constant fails the bare-constant check. There is no normalization step that could silently weaken this check.

I verified the relevant installed Lean 4.19.0 definitions read-only: `Expr.isAppOfArity`, `Expr.isConstOf`, and `ConstantInfo.levelParams`. The first checks the precise application spine and head name; the second checks the constant constructor/name; the third reads the declaration's own level parameters. The implicit type argument of `Eq` need not be independently compared here: the kernel must accept the fixed table constants at that argument's type, and the audit additionally compiles a closed `example` for every exact original proposition.

The Python postcondition requires exactly 31 unique `A53_ENDPOINT` records with exactly the fixed left/right pairs. Separate `#print axioms` records must cover exactly those 31 names without duplication or disallowed axioms.

### Complete mathematical-module census and axiom audit

The audit selects declarations by the environment's real imported-module index, rather than by declaration-name prefixes. Its 36-name module array includes all four dependencies, the parser, and every endpoint module. It checks the presence of all selected modules and emits a marker for each. `Environment.constants` and `getModuleIdxFor?` were checked against the installed Lean definitions; imported constants are selected from the kernel environment and import-origin map. The diagnostic audit module itself is outside this mathematical-module census.

Every selected declaration is reported. Unsafe declarations are listed separately; they cannot inflate the safe count. For every selected safe constant, the audit computes transitive axioms and enforces exactly the allowlist `{propext, Classical.choice, Quot.sound}`. Installed `collectAxioms` traverses checked declaration types and bodies, recursively including their used constants, and reports axiom declarations encountered. The reviewed mathematical sources contain no authored unsafe declarations, supporting the separate compiler-artifact classification used here.

Every safe constant's actual `ci.type` is printed between paired name markers, with full names, universes, explicit arguments, proof terms, and deep terms enabled. The Python consumer requires a unique name inventory, one type block per safe constant, matching begin/end name sequences, exact theorem and unsafe counts, coverage of every selected module, and no ellipsis marker. It also enforces the allowlist again for parsed safe records. Lean's installed message serializer confirms that information messages are emitted without location prefixes, so the anchored marker patterns match the actual CLI output format. The expression-printer option definitions confirm that the guarded omission glyph is the one used for proof/depth/step elision.

These are reviewed future execution conditions. Actual census counts, printed types, and observed axiom sets await the full run.

### Preservation and end-of-run stability

The preparation script first refuses to overwrite an existing candidate. It copies the recovered package, preserves the old runner/registry/audit under `development/recovered-five-endpoint-verifier/`, and writes the three repaired infrastructure files. It generates no mathematical proof source. Its summary compares every recovered parser/endpoint module byte-for-byte.

My independent inventory found all 32 recovered proof modules unchanged and verified preservation of all 275 original package files, using the preserved location for the three replaced infrastructure files. There were no preservation mismatches. Retained WIP files, individual author receipts, and historical failure files remain evidence in the preserved package; no historical failure was relabeled. The original recovery subtree and separate receipt-classification report were not modified.

During the planned full run, source bytes are checked before copying and checked again in both repository and build locations at the end. Every emitted object is hashed immediately after its own compilation; after the audit the complete object set and all those hashes must match. The compiler hash is checked again before PASS. Existing successful author receipts, prior objects, or old report contents cannot substitute for these new commands.

## Exactly two authorized negative-path checks

Both checks ran once. Their complete argument arrays, cwd, sanitized environment, timestamps, exit statuses, stdout/stderr hashes, and observations are preserved in `inventory-and-negative-paths.json`. The driver is `inspect_and_negative_paths.py` (SHA-256 `1a10735a77edfe01ef7f9144ac7fdef70031c9d105aaa571348473d055de7012`).

| Check | Observed result | Decision |
|---|---|---|
| Run the new candidate runner with Python `-O` | Exit 1; empty stdout; stderr says `Refusing optimized Python: proof acceptance checks require assertions enabled`; requested output directory does not exist | PASS: assertion removal is rejected before output/build creation |
| Pair a byte-identical new runner with the actual preserved five-endpoint registry in an isolated fixture | Exit 1; report `FAIL`, `AssertionError:`; zero recorded Lean commands; zero copied sources; empty build and log directories | PASS: old partial coverage cannot become an all-31 PASS |

The second fixture's registry hash is `86c81fd33737dfd8d2c414f2e9001535f2202042df050bda513abf7a8f92eff5`, identical to the retained historical registry. Its runner hash is the new candidate runner hash listed above. This is an authentic old-registry rejection, rather than a fabricated partial registry. The old-registry run creates its failure report and empty directories, which are retained; only the optimized-Python check was required to reject before creating output.

Raw evidence files are `python-O-rejection.stdout`, `python-O-rejection.stderr`, `five-endpoint-rejection.stdout`, `five-endpoint-rejection.stderr`, and `five-endpoint-rejection-output/report.json`. No Lean process was started by either check, and no other negative test or proof execution was performed.

## Scope of this decision

The reviewed repair is ready for the one parent-owned full clean source execution, with no requested source or verifier change. A subsequent full-build PASS must come from that execution and be bound to these reviewed bytes and its recorded compiler/source/object evidence. Publication and source-owner coordination remain with the parent; accepted-main mutation remains with its owner. This review does not change the published PR151 head or transfer the accepted source-semantic result to an unrelated future head.
