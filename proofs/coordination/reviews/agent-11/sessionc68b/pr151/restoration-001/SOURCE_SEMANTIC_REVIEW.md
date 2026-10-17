# PR151 recovered candidate: independent semantic source review

## Decision and precise status

**PASS for the semantics of the recovered candidate source, with strict execution and publication still pending.** I found no mathematical or proposition-level defect in the 31 endpoint proofs or their shared parser correspondence. This review does not certify that all 31 sources have been freshly compiled together, does not upgrade the published PR head, and does not establish readiness or integration.

The reviewed candidate is the original Agent #53 source recovered under:

`/workspace/scratch/c68be3818c4b/pr151/proof-development/recovered-checkpoint/boundary-table-transcription-20261016/`

The published PR head supplied for this review is `a05ac1a31de7e5edb0a1eca24af344fbcf80b883`; its independently reconciled contents contain only the `rootRanks0` endpoint. The actual main supplied for this review is `74a1c3922eb7af438fe40b23d2105ad07556e3f5`. The recovered 31-source candidate is not that published head. Publication or later changes require an explicit binding to the reviewed hashes below.

Reviewer: independent semantic-review subagent `/root/pr151_full_semantic_review`, acting for Agent #11/session `c68be3818c4b`. I authored no mathematical proof, modified no mathematical source, ran no Lean process, executed no retained author script, and performed no source-branch, main-branch, GitHub, or external messaging write. I read the repository preservation and sole-writer policy in `pr140/AGENTS.md`. Agent #53 remains the source author; this review neither transfers that ownership nor grants integration authority.

## Scope and evidence separation

I inspected the complete parser source, all seven graph proof files, all eight root-rank proof files, all eight rank proof files, and all eight map proof files. I also inspected the relevant original definitions and the four-source local dependency closure, the formalization contract, full-scope manifest, claims, and retained audit source. I checked the parser against the local Lean 4.19.0 reference definitions of `String` and `Char`; their exact file hashes are retained in the supporting JSON.

The independently completed initial source reconciliation is reused for the unchanged original/K data pairs and published checkpoint provenance. Its input is `pr151/initial-review/static-reconciliation.json`, hashed in this review's static result. I did not rerun that retained script or duplicate the original 13-file evidence reconciliation. The archive/author-receipt reconciliation belongs to the separate checkpoint reviewer.

I extended the existing data reconciliation where the recovered proof introduces copied strings or numeric literals: every graph helper string is byte-for-byte the original graph's string, and every helper numeric list is byte-for-byte the corresponding K literal list. All array proofs unfold the actual original/K constants directly and introduce no replacement data.

The reviewer-authored `inspect_semantics.py` performed 397 successful static checks in its first and only run. `static-run-001.json` retains every check and the complete source inventory; `static-run-001.stderr` is empty. It checks source hashes, exact endpoint statements, imports, namespaces, proof-body structure, forbidden proof shortcuts, graph helper bindings, all graph1 character transitions, all 40 token-composition accumulators, and all 40 numeral proofs. These checks support this human semantic reading. **Neither the static computation nor its JSON is a Lean proof or a substitute for the parent's strict source build.**

## Exact propositions and absence of weakening

Every endpoint has the exact form

```lean
Agent53BoundaryTables.x_eq_xK :
  BoundaryCertificate.x = BoundaryCertificate.xK
```

for `graph1` through `graph7`, and `ranks`, `maps`, and `rootRanks` at indices 0 through 7. All 31 are closed, unconditional propositions. There are no explicit binders, inherited section variables, fake premises, positivity assumptions, carry-validity assumptions, seed assumptions, or assumed transcription equalities. Unqualified names in the array statements resolve through `open BoundaryCertificate`; no candidate declaration, instance, notation, or namespace shadows the targets. The final statements in the graph files are fully qualified.

`Sofic.Graph` is the abbreviation `List LEdge`, where `LEdge` has `src`, `dst`, and `lab` fields of type `Nat`. Graph equality is therefore actual ordered-list equality, not set equality, membership equivalence, a graph isomorphism, or language equivalence. The rank and map targets are actual `Array Nat` equalities. Thus the endpoints preserve every value, its position, duplicate multiplicity, and length. Subsequent array operations, including operations with out-of-bounds behavior, receive the same argument by ordinary equality congruence; the proofs do not impose a new indexing convention.

The complete finite family has 37,686 entries: 7,430 graph entries, 14,158 rank entries, 14,158 map entries, and 1,940 root-rank entries. This is precisely the contracted family of concrete representation identities. It is not a restriction of a universal dynamics claim to a finite experiment.

## Original parser and decoder remain the targets

The original `BoundaryData` definitions are:

```lean
def parseNats (s : String) : List Nat :=
  (s.splitOn " ").filterMap String.toNat?

def decodeEdge (n : Nat) : LEdge :=
  {src := n / 16777216, dst := n / 4096 % 4096, lab := n % 4096}

def parseGraph (s : String) : Graph :=
  (parseNats s).map decodeEdge
```

Each original graph is `parseGraph` of its original string. Each K graph is the corresponding literal `List Nat` mapped through the same imported `decodeEdge`. The graph proofs establish the natural-number-list equality first and apply `congrArg (List.map BoundaryCertificate.decodeEdge)`. They do not introduce a second decoder, reinterpret its fields, coerce numbers to bounded machine words, reduce the source field modulo 4096, or require the decoder to be injective. The exact decoded-list equality follows even without any encoding-range premise.

The original arrays are parsed lists followed by `.toArray`; the K arrays are literal lists followed by `.toArray`. Their proofs apply `congrArg List.toArray` to an exact list equality. The dependency sources are unchanged and are bound to the initial independent reconciliation and to fresh hashes in this review.

## Shared parser theorem: substantive assessment

The theorem `Agent53TableParsing.parseNats_ascii` states equality between the unchanged original `parseNats` and the structural character-list parser `parseChars`, under the explicit condition that every input character has UTF-8 size 1. It does not claim correctness for arbitrary Unicode strings. Every concrete use discharges this condition with ordinary `by decide` on the actual constant string. The condition does not remain as a hypothesis in any exported endpoint.

### Character access, positions, and extraction

The primitive lemmas relate byte positions to character-list positions under the one-byte condition. `utf8GetAux_ascii` and `get_ascii` match the reference recursion for `String.get`; `next_ascii` advances exactly one byte; `utf8ByteSize_ascii` identifies byte size with list length. The fallback character in the logical reference definition is also one byte, so the helper statements that cover arbitrary positions do not secretly assume a valid in-range position. The split simulation itself uses in-range scanning positions and proves its end test.

The two extraction lemmas separately handle advancing to the starting position and collecting the requested span. `extract_ascii` explicitly splits the `b ≥ e` case, where the substring and the list take are both empty. In the other case it uses `e = b + (e-b)` and proves the ordinary drop/take description. Source exhaustion gives truncation in both implementations. There is no omitted end-of-string or reversed-interval premise.

### Decimal parsing

`foldlAux_ascii` and `anyAux_ascii` use the invariant `s.data = pre ++ rest`. Their recursive steps move one character from `rest` into `pre`, preserving both the traversal position and accumulator. `anyAux_ascii` retains short-circuit Boolean behavior; `all_ascii` derives the universal check from the same negated-existential definition used by `String.all`. `isEmpty_ascii` identifies the string and list emptiness tests.

`listToNat?` requires a nonempty list and `Char.isDigit` for every character before performing the decimal fold. The inspected `Char.isDigit` reference definition accepts exactly code points 48 through 57. `toNat?_ascii` unfolds the original `String.toNat?` and `String.isNat` and rewrites the proved traversal facts. It preserves the original decimal recurrence `10*n + (c.toNat - '0'.toNat)`, using arbitrary-precision naturals. It does not replace a failed parse with zero or accept only a valid numeric prefix of an invalid token.

### Space-delimited splitting and output order

`step_digit`, `step_space`, and `step_end` unfold the original `String.splitOnAux` at delimiter `" "` and delimiter cursor 0. The non-space step advances the source cursor. The space step emits the preceding substring, starts the next token at the next source position, and resets the delimiter cursor. Its subtraction by the delimiter width is justified by the fact that the matched character is a one-byte space. The end step emits the final substring and reverses the accumulated token list.

`splitList` mirrors that process structurally. A non-space appends to the current token; a space pushes the entire current token, including an empty one, and clears it; exhaustion pushes the last token and reverses the accumulator. `split_simulation` tracks the exact source as `pre ++ token ++ rest`, the beginning position as `pre.length`, and the scanning position as `pre.length + token.length`. The space branch extends `pre` through the delimiter and empties the token. The other branch extends the token by one character. This preserves every character exactly once and keeps the reversed accumulator in the order required by the original function.

`splitOn_eq_splitList` initializes this invariant with empty prefix, token, and accumulator. The separator is fixed to nonempty `" "`; it makes no claim about arbitrary separators, overlapping matches, or the empty-separator special case. `splitList_ascii` proves that all produced tokens satisfy the character-width condition. `filterMap_toNat?_ascii` then transports the proved decimal conversion through the whole list, in order. `parseNats_ascii` composes these facts without assuming the desired parser result.

### Edge conditions

The following are consequences of the inspected definitions and proof structure; they were not run as Lean tests in this review:

| Input | Original/parser-bridge result | Reason |
|---|---|---|
| `""` | `[]` | Splitting emits one empty field; `toNat?` rejects it. |
| `" "` | `[]` | Both empty fields are rejected. |
| `" 0  0 "` | `[0, 0]` | Empty fields are rejected while both `some 0` fields remain. |
| `"01 1 001"` | `[1, 1, 1]` | Leading zeroes are permitted; multiplicity and order remain. |
| `"12x 3"` | `[3]` | The invalid whole field is rejected. |
| `"-1 +2 3"` | `[3]` | Signs are not digits in this natural-number parser. |
| `"1\t2 3"` | `[3]` | A tab is not the delimiter; the first whole field is invalid. |
| `"1\n2 3"` | `[3]` | A newline is not the delimiter; the first whole field is invalid. |

ASCII control characters also have size 1 and are handled by the general correspondence. Multibyte Unicode inputs lie outside this auxiliary theorem's premise; this causes no gap for the actual target tables, whose strings contain ASCII decimal digits and spaces.

## Endpoint proof paths

### Four direct proofs

`rootRanks0`, `rootRanks1`, `ranks0`, and `maps0` unfold both imported targets and the original parser, apply array congruence, and simplify the original split and decimal-fold equations with `simp +decide`. They do not use a newly asserted parser equation or compiled result. The reviewed `rootRanks0` source matches the published checkpoint's already reconciled source hash.

### Twenty array proofs using the general correspondence

`rootRanks2..7`, `ranks1..7`, and `maps1..7` unfold the actual targets and apply array congruence. The first equality in their transitivity chain is `parseNats_ascii` with a concrete ASCII proof. The second is the closed equality between the structural list computation and the complete literal list, supplied by ordinary `by decide`. There are no externally generated Boolean certificates, unchecked equality casts, or separate data constants inserted into these proof bodies.

### Graph1's staged original-parser proof

Graph1 does not depend on the shared parser theorem. It uses the original split-state equations directly. The input contains 40 numeric tokens in 382 bytes, comprising 343 digit positions and 39 literal spaces. The independent static inspection checked every advance from each digit position to the next, every delimiter boundary, every stated token substring, and the final end position at byte 382. All these concrete premises are discharged with ordinary `by decide` in the source.

The 40 token lemmas are chained from the original initial state. Before token `i`, the accumulated list is exactly the preceding `i` tokens in reverse order. The last token lemma applies `step_end`; the final reversal restores the original token order. Each of the 40 decimal numeral lemmas unfolds the original `String.toNat?` semantics. `parseResult` rewrites the full split result and all 40 numeral lemmas through `List.filterMap`, then the public endpoint applies the original decoder by congruence. The graph helper input and numeric result are bound to the imported original/K declarations, so this is not merely a proof about an unrelated copied table.

### Graph2 through graph7

Each final recovered source proves one closed full-list parse equality using `parseNats_ascii`, then applies the original decoder map. **There is no chunk decomposition or chunk-stitching proof in these final recovered files.** Historical chunk strategies or failed attempts therefore must not be described as the current proof mechanism. Their full helper strings and lists agree exactly with their target definitions. No boundary, suffix, append, or chunk omission can be hidden in their final proof composition.

## Trust, axioms, and circularity

The reviewed mathematical source closure contains no source use of `sorry`, `admit`, `sorryAx`, `native_decide`, `Lean.ofReduceBool`, new axiom declarations, `unsafe`, `partial`, external proof primitives, custom elaborators/macros, or execution commands. Its candidate proofs use ordinary induction, equations, rewriting, simplification, equality transitivity, congruence, and `decide`. The diagnostic audit is separate from this mathematical closure and does not supply an equality proof.

The shared parser module imports only `BoundaryData`. The endpoint modules import `BoundaryDataK` and, where needed, the shared parser module. The local dependency direction is `ReverseClosure`/`Std` → `SoficProof` → `BoundaryData` → `BoundaryDataK`. The parser neither imports the endpoints nor defines the target constants. The extra `parseChars` function is connected to the original function by an independently structured theorem, and the desired target equality is never assumed to prove that correspondence. There is no circular target definition or proof dependency visible in the source.

The allowed transitive logical axioms are exactly `propext`, `Classical.choice`, and `Quot.sound`. Static absence of forbidden tokens is not a complete axiom audit. I do not assert a freshly observed transitive axiom set for any elaborated constant. That requires the pending clean build and complete environment audit. Standard compiler-generated unsafe implementation artifacts must be distinguished from safe theorem/definition bodies; no such artifact may be used as an unsafe proof oracle. The audit should report them separately and enforce the allowed axiom set for every selected safe constant, not merely for the 31 final theorem names.

## Concrete remaining blockers and sound completion steps

No mathematical source correction is requested. The following verification and delivery obligations remain:

1. **Complete strict source build.** Compile the entire four-dependency + shared-parser + 31-endpoint source closure in a fresh isolated directory with the pinned official Lean 4.19.0 compiler, `--trust=0 -j1 -DElab.async=false`. Record compiler identity/hash, source hashes, exact arguments/environment overrides, complete logs, exit codes, and resource settings. Reuse of prebuilt project modules or an import-only audit does not replace this source compilation.
2. **Replace the stale audit's scope in a separate delivery artifact.** The retained top-level `Agent53Audit.lean` imports/checks only five endpoints and selects nine local modules. It does not import the shared parser or 26 other endpoint modules. A complete audit must select all 36 mathematical modules, check the exact 31 endpoint types, report all selected safe declarations and transitive axioms, enforce the allowlist, and verify module origins. Preserve the original stale audit and historical failures rather than rewriting their evidentiary status.
3. **Keep claim levels precise.** `FULL_SCOPE_MANIFEST.json` says the endpoints were individually checked by the author, the complete-family fresh build was not run, independent review was incomplete, and integration was not done. This report closes the independent semantic-source-review part only. Archive/receipt authentication and strict execution are separate evidence components.
4. **Publish the reviewed candidate and completed evidence under the actual source owner's coordination.** The published head still supplies only one endpoint. A new candidate commit must include the missing sources and evidence and be checked against the hashes reviewed here. Review findings cannot be transferred to an unrelated or modified head merely because it has the same PR number.
5. **Respect integration ownership.** The source author remains Agent #53/session `c04cf11f6ff8`; Agent #31/session `02893e4f368d` remains the sole main writer. This review performs no acknowledgment, main write, merge, or readiness transition. A later delivery decision must bind the final PR and then-current main state and retain all original research and failure records.

Graph0 remains outside this contribution's endpoints and with Agent414. Exterior-exclusion transfer and existing certificate/dynamics work remain with their respective Agent414/Agent109 scope. These table equalities do not prove a new exterior exclusion, validate a new dynamical certificate, establish an ordinary decimal-orbit bridge, or prove any statement about 196.

## Endpoint coverage and source hashes

All hashes below are SHA-256 of the complete files actually inspected. For each row `x`, the exported declaration is `Agent53BoundaryTables.x_eq_xK` and its complete proposition is `BoundaryCertificate.x = BoundaryCertificate.xK`. Every row has semantic source status PASS and strict execution status not performed by this reviewer.

| Endpoint | Entries | Source file | SHA-256 |
|---|---:|---|---|
| `graph1` | 40 | `Agent53Graph1.lean` | `664b3798e77e7efd2a2c9d9e187189411306e96f9f5b796fa92e5ac074f698e4` |
| `graph2` | 178 | `Agent53Graph2.lean` | `4c622dfe7c3b7d946d5d08baf580893a8a72b975d883692b6223820cfb047e18` |
| `graph3` | 484 | `Agent53Graph3.lean` | `4bae6249c70859a39c9e44ee98100225d36462e3c5f2b487d5ef29d7306d0585` |
| `graph4` | 1,322 | `Agent53Graph4.lean` | `c79cc9e2b148f5519e13b324cf4cab8963851b874ce9d580ee0e5ceea51229b4` |
| `graph5` | 1,802 | `Agent53Graph5.lean` | `8eb762f5f62f57781e82f2d6b25abc2aa8492ebe4ff257aa89af4f893a3a21fe` |
| `graph6` | 1,802 | `Agent53Graph6.lean` | `f75c189bf16170c7f8f281247e4cbf3453abac0040729d35abbbc7de3ac5f886` |
| `graph7` | 1,802 | `Agent53Graph7.lean` | `4000df105de8db5391b2bf428a4e201f0448934eb35801272a9da15a00d70410` |
| `ranks0` | 24 | `Agent53Ranks0.lean` | `18d8a3d44a6dd90700a9e358c275ad1f5616078a79e96a2e5e03f1049a31d04e` |
| `ranks1` | 76 | `Agent53Ranks1.lean` | `a6329d04062bdfaafc3c6ec3b11f8661559b33a724cd6aca5717a780b2ee35e7` |
| `ranks2` | 324 | `Agent53Ranks2.lean` | `bd467f02b78c0e02b83ab8c9566548dddca3a16351e34133e3e9d97a5ccb013c` |
| `ranks3` | 910 | `Agent53Ranks3.lean` | `778376f04e8e9761a3478a55676a26f7269bb88809f35a5de25ca44bf2d6c99b` |
| `ranks4` | 2,522 | `Agent53Ranks4.lean` | `49ab3c6b0e86a9cfce78f7e7e9c1adab9a5331221763bcd25b8a6b7aed6b4b44` |
| `ranks5` | 3,434 | `Agent53Ranks5.lean` | `64373fe593429d384fc41334a7eb83d93c7312290440db597203273d4d5f6a24` |
| `ranks6` | 3,434 | `Agent53Ranks6.lean` | `cf9183861bb29e4896b678107f56e8ace1a27edc9183ba7c4aba22e4dc2e072c` |
| `ranks7` | 3,434 | `Agent53Ranks7.lean` | `3301066e0646b9c95c46bd87e6079138f551f8baacd40d5a0d63e7e5994811c0` |
| `maps0` | 24 | `Agent53Maps0.lean` | `5059fa7042999b20cca52e29ed8b0b9f027191d49842116dfe4894c56e7e3551` |
| `maps1` | 76 | `Agent53Maps1.lean` | `6cd21baf7b5d0c2ab3ce79103f2f5fbacac297e6e7d2feb4eaf36bdc731987d6` |
| `maps2` | 324 | `Agent53Maps2.lean` | `bed0657bf9ad678d6f275924ed1954beb307e98ec8fa65ba9079cd3305b8dc43` |
| `maps3` | 910 | `Agent53Maps3.lean` | `33d30aa317e57fd3f148bc546763cf155d47b05671f635d7825be0805654b10d` |
| `maps4` | 2,522 | `Agent53Maps4.lean` | `90122d8dd29da20a1538b9a816754683a857ee1b809f9f5a7901e6a1056fb490` |
| `maps5` | 3,434 | `Agent53Maps5.lean` | `d680b110caa68bfc9c34e76d771b945d14b9662d91bac431185602a848ef734f` |
| `maps6` | 3,434 | `Agent53Maps6.lean` | `61a388490fc63455010adf7c3c14d13921c13d8d9387b76f60ad9742a4873396` |
| `maps7` | 3,434 | `Agent53Maps7.lean` | `9a88d309fa1b76262088f325522a2864921fbeff5a1603dd3f1ebcac44431160` |
| `rootRanks0` | 12 | `Agent53RootRanks.lean` | `e68426cfebfc1868ecaa9d3ee2ca9ab645358a915359d92fcec96fb60de36062` |
| `rootRanks1` | 22 | `Agent53RootRanks1.lean` | `58482b33abad66c85787f6271d41f9ab59e50027aec582ea382c66dbef76d559` |
| `rootRanks2` | 60 | `Agent53RootRanks2.lean` | `4b44a07551ab3169ec5472f51ec1d7c38f4a73c14764d5dcdcf5d64214a69a8e` |
| `rootRanks3` | 136 | `Agent53RootRanks3.lean` | `062cbf8fe5145829df41db7241bcd7caa1dc2c7affb8d685a137123a6aa76eed` |
| `rootRanks4` | 342 | `Agent53RootRanks4.lean` | `5f8a5096a4deecea49a5e425ad2db845113827cbfaa3ee33938bbef2b173592a` |
| `rootRanks5` | 456 | `Agent53RootRanks5.lean` | `262db604137f1f7de22fa13fe7e073e7c9be726faba92eb5e413130cdfb7ad45` |
| `rootRanks6` | 456 | `Agent53RootRanks6.lean` | `d06f50c59fff3a8ec52ba18bd2efc617129d809c332d6709bdff014d11a1bd7c` |
| `rootRanks7` | 456 | `Agent53RootRanks7.lean` | `375c267c80a2218f31bfeb26e4e770476cf6f014fd51213b19a106e0db04c19f` |

### Shared parser and unchanged dependencies

| Module | SHA-256 |
|---|---|
| `Agent53TableParsing` | `e375d0420101fcbc09fafe65f89f41356248469f53b2cdc508de209e3a8f3dfa` |
| `ReverseClosure` | `4eff36855476726d54abc86393e841cf6aa744e1eed639c3f8786440cfd092ee` |
| `SoficProof` | `7e31c22897c4a334b4ea0a98e399f99f87a769d18b133d19ca5ead81b534b085` |
| `BoundaryData` | `37588ed783e26ba39ab014a6dde44f0473bf739ff281fbc204fbff2130185a42` |
| `BoundaryDataK` | `39e1383e23960734617bff1d66fb72faeb11bd9df951d63538e63c3072e1d76e` |

### Supporting evidence files

The complete per-check results, inspected source paths/imports/declarations, and hashes of the contract, claims, manifest, stale audit, policy, and local String/Char reference files are in `static-run-001.json`. `RESULT.json` records the semantic decision and remaining obligations in machine-readable form. The reviewer-authored static checker and its first-run stderr are retained alongside them. No static check failed, and no Lean execution was attempted by this reviewer.
