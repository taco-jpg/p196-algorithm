# PR 135: independent mathematical and source review

**Decision: PASS for the mathematical statements, certificate data, concrete source closure, and source preservation within this review's scope. No unresolved mathematical defect was found.** This is a nonauthor source review with bounded exact arithmetic diagnostics. It is not a claim of fresh Lean compilation, a standalone transitive axiom audit, or final integration approval.

Reviewer: Agent #22, task `/root/pr135_semantics`, using the parent-selected highest supported reasoning effort. Source authorship remains with Agent #104 and the credited upstream authors. The reviewer neither modified the mathematical sources nor authored the supplied certificate. The root delivery owner controls integration and remote writes.

## 1. Exact scope and decision binding

| Reference | Exact commit |
| --- | --- |
| Mathematical source freeze | `dc2123ae4a4513acfe75e0a6cd21c3b6a044bec4` |
| Source head reviewed in full scope | `786ea690d8221503ae93dc3f981b1b56749ff40f` |
| PR merge base used for the original diff | `ae8bbdfd2a18e8910eebc25fd2a81661c01abc16` |
| Initial target base independently checked for generic source identity | `cc3de9834bef628d1083ce637641f07ed3953b13` |
| Updated head to which this decision also applies | `32d2b92ec79becfbb4d2aa2cf9bd42f8bbd5597e` |
| Refreshed accepted base checked for all 13 generic dependencies | `a38b83ec83b74ad046207c5848ec05d39a878cfb` |

The original diff contains exactly **2,703 additions**, all regular files with mode `100644`, and no edits or removals. The complete path inventory was compared against the actual Git diff. It contains 1,556 Lean files, 1,073 logs, 54 JSON files, 11 Python files, six Markdown files and three text files. Every incoming Lean blob was read and its Git blob identity and SHA-256 recorded. The exact active endpoint closure is **510 concrete modules plus 13 existing generic modules**, with no extra project import and no missing module. All 510 concrete modules agree byte for byte with the mathematical freeze and the generation manifest. All 13 generic sources agree with the original merge base, the initial observed target base, and the refreshed accepted base. [E1–E4]

The updated head has the reviewed head as its immediate parent. Its only changes are the contribution README and two correction-record additions. The original README was preserved byte for byte. All 523 mathematical source files were read again at the updated head and match the reviewed source identities. The repair increases the cumulative incoming path count to 2,705 without altering the mathematical result. Exact review of the repair's revised wording is assigned separately to `/root/pr135_repair_review`; this report verifies its source isolation and original-byte preservation. [E5]

The controlling uploaded role and repository `AGENTS.md` were read. No branch, ref, index, source, lock, credential, remote comment or review was changed by this subtask. Work products were written only to the assigned isolated review directory.

## 2. Statement fidelity and the ordinary decimal meaning

The concrete public endpoint is [`proofs/Agent104Prefix620.lean`](https://github.com/taco-jpg/p196-algorithm/blob/32d2b92ec79becfbb4d2aa2cf9bd42f8bbd5597e/proofs/Agent104Prefix620.lean). Its source SHA-256 is `9c4af5ff576c4184c1beb7fded6e1c0a33a815bfb1130793029815e66ab3e653`.

`PalindromeStarts620 P` is exactly `PalStarts3 6 2 0 P`. The public theorem `palindromeStarts620_iff` is a definitional equivalence to the conjunction of the ordinary `Lychrel196.Palindrome P` and existence of canonical decimal digits of length at least three with leading digits 6, 2, 0. The digit indexing is from the units place, so the displayed leading digits are `e (W - 1)`, `e (W - 2)`, and `e (W - 3)`. The length condition prevents truncated natural subtraction from changing this interpretation. [S1, S2]

The underlying `Lychrel196` definitions remain unchanged: `reverse10` is decimal reversal, `Palindrome n` means `reverse10 n = n`, `step n = n + reverse10 n`, and `orbit n 0 = n` with each successor time applying `step`. The inspected canonical representation requires positive length, every digit at most 9, a nonzero most significant digit, and the exact positional value. Its uniqueness and reversal correspondence supply the bridge to the ordinary numeral interpretation. A fuel-bounded implementation of reversal is accompanied by the needed equality to the terminating decimal division recurrence; it is not an arbitrary alternate predicate. [S2]

The two substantive endpoint statements are:

```lean
∀ A P t, 0 < A → PalindromeStarts620 P →
  Lychrel196.orbit A t = P → t ≤ 12

∀ t, ¬ PalindromeStarts620 (Lychrel196.orbit 196 t)
```

The first quantifies over every positive seed, every target and every time. It does not assume that the target is the first palindrome, that the seed has a fixed number of digits, or that a certificate proposition is available as a user-supplied premise. The orbit definition keeps iterating after a palindrome. Time zero is handled explicitly. Excluding seed zero is an explicit original hypothesis, not a silently imposed restriction. [S1, S3]

The second theorem excludes **620-leading palindromes** on the 196 orbit. It does not prove that 196 never reaches any palindrome, and it does not assert the full P196 conjecture. The concrete endpoint supplies all three certificate facts to the generic theorem: `allRows`, `short`, and `initialBounded`, each for the same `R ranks`. The fixed arithmetic conditions are kernel decisions. There is no unproved certificate premise or circular use of either final theorem. [S1, S3, S4]

## 3. Generic mathematical chain and boundary cases

The twelve smaller generic modules were read in full, including the inverse checkers and their soundness proofs. For the 218,799-byte existing `LychrelDigitSums` module, the complete source was identified and read into the evidence store; the human mathematical inspection concentrated on the required decimal, carry, orbit, representation, finite-196 and endpoint dependency sections. This report does not claim a line-by-line review of its unrelated research results. The separate evidence reviewer covers compilation and the complete recorded axiom footprint of the module and endpoint closure. [S2–S4, E3]

### Decimal palindrome to initial pair word

The palindrome bridge uses the canonical target, its leading digit greater than one, the actual palindrome equality, and the symmetric column-sum equations. A leading overflow digit would be one and is excluded by canonical representation uniqueness. Crucially, the source does **not** infer that every carry vanishes merely from absence of final overflow. It uses the palindrome and symmetric pair equations with the zero outer carries to establish all the required zero carries. The actual pair-word projection preceding the final reverse-and-add step therefore belongs to the original `initialWordsK 7 6 2 0` enumeration. The high-order 620 prefix becomes the corresponding low-order entries using the actual palindrome relation. [S2, S3]

### Long predecessors

The actual-prefix lemma applies whenever the current width is at least seven. It does not assume disjoint first and last seven-digit blocks. Width seven, widths 8–13 where the blocks overlap, and larger widths are covered by the same proof. The inner carry is the actual carry at the cut. Enumerating both possible cut carries can add abstract possibilities; it cannot remove the actual predecessor. [S3]

The original inverse relation includes both no-overflow and overflow cases, positive outer pair sum, coefficients below 19, Boolean carries, and the terminal overflow condition. The fast inverse and concrete Boolean checker have proved implications from the original inverse. All local carry alternatives are covered. The uses of natural subtraction in candidate formulae are accompanied by bounds and exact equation checks, so truncation does not silently discard valid predecessors. The coefficient and carry bounds include 18 and 1 respectively. Decimal width growth across a 9/10 boundary is allowed. [S3, S4]

### Short predecessors

`projectK` retains the entire word below width seven. The short proof enumerates every admissible symmetric pair word of width below seven, with coefficients 0–18, positive outside coefficient, and the necessary even centre coefficient at odd width. Width zero is explicitly empty. Widths one and two use direct lists; widths three through six use all 19 choices of the first half-word coefficient, including the empty filtered coefficient-zero slices. The transition from width six to width seven is included in the generic proof. [S3, S4]

The direction of the obligation is correct: whenever the successor has a stored rank, the predecessor must also have a smaller stored rank. A successor absent from the rank tree does not contribute an ancestry obligation. For the actual short transition, `nextWord` is connected to the unchanged carry-normalized decimal operation, including width growth. [S3, S4]

### Code tree and rank descent

The base-19 code starts with a sentinel 1 and records every coefficient. `decode` has a 32-step bound, while the soundness theorem explicitly requires length at most 32; the concrete width is seven. Correct decoding also requires coefficients below 19, and actual projections satisfy that hypothesis. The long-row proof obtains width seven from actual inverse membership, so a row check for another decoded length cannot bypass an actual long transition. [S4]

`lookupC_all` transfers the tree-wide property to a found key. Its logical soundness does not assume the generator produced a sorted tree. This review additionally checked strict sorting, uniqueness, complete literal data and proof-tree alignment. `belowC` rejects missing predecessors and requires a strict rank decrease. A natural-valued rank on the entire backwards closure then bounds the actual pair-orbit time by the terminal rank. The final palindrome step adds one, yielding 11 + 1 = 12. [S3, S4, E1]

For 196, `no_196_of_R` combines the ancestry bound with the existing complete finite check through time 100 and the concrete inequality 12 ≤ 100. Its premise that the target predicate implies the ordinary palindrome predicate follows directly from the definition. It does not assume an unproved all-time fact about 196. [S2, S3]

## 4. Concrete data, enumeration coverage and generator review

The original certificate is `certificate_620.json`, SHA-256 `e6c447fa7efa26e94d1a8064a9336922d3eeb2e1e55176f8043e1cd9dbe3cea5`. The retained certificate and both upstream Python inputs were compared byte for byte to their exact existing repository originals. Their original paths, Git blobs, lengths and hashes are recorded in the supplied `UPSTREAM_PINS.json` and in this review's actual-read manifest. [S5, E4]

The entire active `generate_frozen620.py`, the retained earlier adapter, `gen_code.py` and `scope.py` were inspected before any use of review functions. The active adapter pins all three upstream inputs, replaces discovery with the supplied frozen rank dictionary, and emits a balanced code tree and finite checker modules. The finite partition changes the size of kernel reduction jobs while retaining the original semantic checker and lists. The coverage helper is separately handwritten and hash-pinned. No generator was run during this review, and no new certificate was searched for or substituted. [S5]

The structural helper `Agent104Prefix620DataCoverage` has SHA-256 `d8d672edcda4b39d14247927ee7c7eef221e1da71bee68a0bb67f233006115f5`. Its two lemmas were read in full. For initial coverage, list membership splits the free suffix length into less than four or exactly four, then destructs the first two decimal choices. The short-case original filter is retained; the width-seven slices establish a stronger unfiltered obligation. For short coverage, the half-word decomposition retains the original positivity and centre filter. Neither lemma assumes the property it is meant to establish. [S1, S3]

The active 510 modules comprise 64 data modules, one tree module, 256 leaf-row modules, one internal-row module, one long-row assembly, one handwritten coverage helper, two finite-word data modules, 101 initial check modules, 78 short check modules, two coverage-equality modules, two finite assembly modules and the endpoint. Every module is represented in the exact manifest and reachable from the endpoint. [E1, E2]

The fresh bounded checks established:

| Obligation | Result |
| --- | --- |
| Original certificate nodes / code-tree nodes | 59,189 / 59,189, identical keys and ranks |
| Node widths | five nodes of width 5; three of width 6; 59,181 of width 7 |
| Stored ranks | all natural, maximum 11 |
| Original initial domain | all 10,002 words; maximum initial rank 11 |
| Initial slices | two short words plus 100 slices of 100 width-seven words |
| Complete short domain | 10,467 words |
| Short counts for widths 0–6 | 0, 9, 18, 180, 342, 3,420, 6,498 |
| Short blocks | 78, including empty blocks 002, 021, 040, 059 |
| Concrete finite check modules | all 179 checked against their entire source contracts |
| Finite coverage equalities | all 101 initial and 78 short declarations checked |
| Assembly mappings | all 100 initial and 76 sliced short cases, both direct short widths, and width zero |
| Long predecessor edges | all 71,554 checked for membership and strict rank descent |
| Short predecessor edges into stored targets | all six checked for membership and strict rank descent |
| Full predecessor graph | 71,560 edges; every stored rank equals its exact predecessor height |
| Reachability | every stored node reached backwards from the complete initial domain |
| Long proof assembly | 256 distinct leaves and 255 distinct internal checks, each used once on the same tree |

The two shorter initial words are `[6, 2, 0, 2, 6]` of rank 1 and `[6, 2, 0, 0, 2, 6]` of rank 5. Lengths three and four contribute no admissible initial word. The eleven other layers and terminal empty layer match the original certificate exactly: `10002, 5957, 3483, 4427, 2006, 2810, 6194, 2512, 9770, 6146, 3691, 2191, 0`. [E1, E5]

The arithmetic control uses the inspected retained nonauthor algorithm that enumerates the literal local column equations, rather than the author's fast candidate formulae. The current diagnostic freshly re-executed its finite arithmetic functions and strict literal parser from their exact Git source, with their main entry points disabled. It checked the full certificate graph, not a sample. This reuse is expressly recorded: it is a fresh execution of a previously reviewed nonauthor control, not a claim of a third independently invented arithmetic algorithm. [S6, E1]

## 5. Preserved history and whole incoming source scope

The 1,556 added Lean paths consist of 510 active concrete modules, 718 preserved development or stage source snapshots, 326 untrusted upstream emitter outputs, one author-base audit helper and one retained canonical replay audit source. There are 1,208 distinct incoming Lean blobs. The import closure check excludes all 1,046 nonactive paths from the accepted mathematical endpoint. Their presence does not turn a failed historical build into current success. [E1, E2]

The additional history diagnostic read all 1,046 nonactive paths, representing 701 distinct blobs. It verified all 370 content-addressed historical Lean paths, parsed 514 literal tree definitions and checked all 118,378 recorded code/rank literal occurrences against the original certificate. It also checked 510 historical concrete internal-row statements and all 418 historical finite-word blocks, containing 40,938 word occurrences, against the complete original initial or short domain in each full data file. These are preservation and data-consistency checks. Superseded or failed modules are not newly certified as buildable. [E5]

The earlier coverage-helper source differs from the accepted helper only in an inaccurate documentation sentence about the filter; the actual proof is unchanged. The current comment accurately says that positivity and the centre filter are retained. The earlier generator's changes were inspected as a full diff against the fully read current generator. They implement the finite-list repartition and preservation of retired outputs. The original monolithic and failed partition attempts remain visible, including the original status records. [S5, E5]

Across the two named reviewers, all 11 added Python files are covered: this reviewer read the two adapter versions, both upstream sources, all three independent controls and `development/check_coverage.py`; `/root/pr135_evidence` separately confirmed full reading of `generator/build_concrete.py`, `verification/author-base/build_base.py` and `verification/independent620/rebuild.py`. The evidence reviewer owns all build/provenance log validation. This report does not claim an independent second audit of those logs.

## 6. Retained review, independence and the README finding

The complete retained `review/SEMANTIC_REVIEW.md`, `review/STRUCTURAL_COVERAGE_REVIEW.md`, the three independent Python controls and their result files were inspected. They identify source authors and the separate `/root/strategy_review` semantic reviewer, preserve the earlier pending review state, and append the final frozen-source review. This is meaningful separation of authorship within a shared session. It is not an external peer review, a distinct human account, or an independently eligible GitHub approval. The present reviewer is also a separate nonauthor task in the delivery session. [S6]

The retained controls are tied to the exact scripts, original certificate, manifest and mathematical freeze. The diagnostic read and checked **all 526 published-source links** in the retained final-connection record. This exceeds the smaller subset of direct remote readbacks claimed in the original record; the original evidence's scope is not rewritten. The retained broader sample and negative-control results were read and source-matched, but were not unnecessarily rerun. The fresh graph and source diagnostics reported above resolve the current data and coverage obligations. [E1, E4, S6]

The evidence specialist identified a real README provenance overstatement at the original reviewed head: the author verification sentence described all 510 concrete plus 13 generic modules as explicitly `--trust=0` and single-worker. The generic author-base commands use default maximum trust, and earlier concrete stages used two workers, while the later 431-module stage used one. This is a documentation defect, not a change to the theorem statement. The root published the scoped repair at the updated head; the independent repair reviewer owns exact wording acceptance. This review confirmed that the original text is preserved and the mathematical closure is unchanged. [E5; separate evidence and repair reviews]

The README's numerical PR 128 witness was also checked directly using exact Python integers: seed **19,014,942,070** first becomes a palindrome at time **12**, namely **62,003,033,030,026**, which begins with 620. All values from time zero through twelve and all palindrome tests are retained in `SOURCE_DATA_CHECK.json`. No claim is made here about PR 128's proof build or integration status; root owns that separate check. The witness is not a premise of PR 135. [E1]

## 7. Dependencies that must remain unchanged

The table below fixes the generic sources used by this decision. `DEPENDENCIES.json` contains every full repository path, Git blob, SHA-256, length and inspected reference. `CONCRETE_SOURCES.json` provides the corresponding complete 510-file concrete inventory. A new combined tree must preserve these bytes or receive a new scope-specific review. At the updated head and refreshed accepted base, every generic identity below was checked directly. [E3, E5]

| Module | Git blob | SHA-256 |
| --- | --- | --- |
| `PrefixCertificate` | `ad2f0d745b82ac796e7008894254f753ee396817` | `2b125b95c61604da41821eee4e58ce9a50f4039a7e43117a42194e6560adfca9` |
| `PrefixInverse` | `c9ba79545ec486297946c418014190f1e6f3a1f0` | `0a93622752fa22cf6c8de2efc8500dc313498d59831bb0e5381b3b351e0ab03e` |
| `LongRowsBase` | `efeb2a7680ba99dd3bdb0dfd55c5f4370040e2ab` | `6568c04797f1e4cf1388c08c6142c6566bbfce59ef3d41a0c8df95cd8b7d07aa` |
| `FastInverse` | `db33abe2ec86deed6bd176fdf38a9af7cc5940f0` | `585cb4d197479714edbdbe147c2c1c489742fa0f8eb978571abdc602eada4eee` |
| `FastRowsBase` | `c2879112ab08c6ca3fc9aa2e2119c7a9b5937eb6` | `e6ae5bcf64ca61d4c3d5aba5f1e08a956f969a8c4b98a85bb2b62867064a1984` |
| `Agent124FastPred` | `a539f7b639403cc8f17512759f69740cb7a66d72` | `cb88c693b7161446232df1c8a45cc8e71a84731ccfb9d4164c9dac26b2a91b5f` |
| `LychrelDigitSums` | `8a865176625283648a8a20dd2411ed77670eb0a2` | `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57` |
| `ActualPrefix` | `ceb031e9987db556499fff75b16be4653c3c7ead` | `c136216ed9c4100a268643be9a471b6746320f63d0af2030b6418429e5551e76` |
| `PalindromeBridge` | `a8066f82178786648c2c32b49a333e0c87e5810b` | `6c1de8cf02ec9381e80388e6b4915db6cfa4d1189d3e47c273400f0d37948093` |
| `ShortBoundary` | `ffd22b5e74531de19304c9f1fd9d0dbaae34c826` | `a018a0b73bfc82f12bc6d866dd3b396bf6b217cae3e0448883be04e2c50e50c9` |
| `Agent124PrefixK` | `dc878646e63394c8cd8e42a8ebd54ca6e0463bc2` | `7b9de533a36b5cb684c5a751940af5a98150ea6dba6519fe5a11651933171314` |
| `Agent124PrefixR` | `26355988be2b524401a0d1aad73ec59ccba67580` | `bcb76dbc980957229c1d983bd6b5e36e974a64d7eb2049d30f93b0150c1fcdd2` |
| `Agent124CodeCert` | `4860b198f285848ec19869a8f76e68796f38d13b` | `7feaa64ac30fa69a8b2961d2dc5341eb089087850088d065f8146f07078ea000` |

Additional pinned inputs are the generation manifest (`d2b92c7139f59fe1cb8268addd0d10073780275f06b109bc3cf72933f9170c03`), the active adapter (`8c45b524fb39fa925b57dd7d078dfb0ca84be0635e4c8280e87e4e689ab45024`), upstream `gen_code.py` (`a94f2e4c1b0bf3cbfb82a181ed004a686f767a6eec64f76e2f75d974a4db1433`), upstream `scope.py` (`c51b81cb008e7214a68b65d750ba563f4d912480d326f4c71ea142d60aa51fe2`), the certificate and the coverage helper identified above. These are inputs and source identities; generator trust is not an added logical premise.

## 8. Actual checks, artifacts and limitations

Two bounded Python diagnostics completed successfully, in 2.487 seconds and 1.728 seconds respectively. They use offline `git cat-file --batch`, verify Git blob framing and identity, and write only their own review artifacts. Their exact commands were:

```sh
python3 -B /dev/shm/p196-agent22-d1fa86c3a213/pr135-semantics/check_semantics.py > /dev/shm/p196-agent22-d1fa86c3a213/pr135-semantics/check_semantics.log 2>&1
python3 -B /dev/shm/p196-agent22-d1fa86c3a213/pr135-semantics/check_connections.py > /dev/shm/p196-agent22-d1fa86c3a213/pr135-semantics/check_connections.log 2>&1
```

The first supplemental attempt stopped on the diagnostic's text-separator assumption when parsing a preserved list followed by `end`. It produced no historical-data verdict. Its exact script and log are retained as `check_connections-attempt001.py` and `check_connections-attempt001.log`. The corrected diagnostic uses bracket-balanced literal boundaries and completed successfully. No repository source was changed to accommodate the diagnostic.

Evidence register:

- **E1 — `SOURCE_DATA_CHECK.json`, `check_semantics.py`, `check_semantics.log`:** complete original scope, active source identities, import closure, finite domains, concrete tree, full finite graph, retained-control linkage and numerical witness.
- **E2 — `CONCRETE_SOURCES.json`, `INCOMING_LEAN_SCOPE.json`, `UNMATCHED_RETAINED_LEAN.json`:** exact 510-module inventory and all 1,556 incoming Lean paths with identities and categories.
- **E3 — `DEPENDENCIES.json`:** all 13 generic source paths and identities.
- **E4 — `READ_OBJECTS.json`:** actual source/object reads and hashes for the main diagnostic.
- **E5 — `CONNECTIONS_HISTORY_CHECK.json`, `HISTORICAL_STRUCTURAL_SCOPE.json`, `FINAL_BINDING_READ_OBJECTS.json`, `check_connections.py`, `check_connections.log`:** complete slice connections, preserved-data checks and updated-head/base binding.
- **`EVIDENCE_MANIFEST.json`:** hashes and roles of all review deliverables and the preserved failed diagnostic attempt.

Source register, all at the exact reviewed source head unless the updated binding is specified:

- **S1:** the 510 concrete `proofs/Agent104Prefix620*.lean` modules, especially the endpoint, `DataCoverage`, `InitialCoverage`, `ShortCoverage`, `InitialAll`, `ShortAll`, `RowsBranch` and `RowsAll`.
- **S2:** the exact existing `LychrelDigitSums` dependency and decimal/palindrome/finite-196 lemmas identified in the inspected dependency chain.
- **S3:** `PrefixCertificate`, `PrefixInverse`, `ActualPrefix`, `PalindromeBridge`, `ShortBoundary`, `Agent124PrefixK`, `Agent124PrefixR`.
- **S4:** `FastInverse`, `LongRowsBase`, `FastRowsBase`, `Agent124FastPred`, `Agent124CodeCert`.
- **S5:** `proofs/contributions/agent-104/prefix620-kernel-20261016/generator/`, its pinned upstream originals, and preserved development sources; exact files and hashes are in the read manifests.
- **S6:** the same contribution's `review/` directory, including both narrative reviews, the three `independent_*.py` controls, result files and source pins.

A lexical forbidden-token screen was used only as a source sanity check. It is expressly **not** a transitive axiom audit. This subtask did not execute Lean, rebuild the standard library, rerun the author generator, or independently recertify prior failed source versions. Compilation flags, environment and source provenance, the original certificate proofs' complete axiom output, and qualifying retained kernel verification are the disjoint responsibility of `/root/pr135_evidence`. Combined-tree preservation, final branch identity and publication are the root owner's responsibility.

**No mathematical or source-data obligation remains unfinished in this subtask.** The scoped PASS transfers to a combined tree only while the exact 523 mathematical source identities are preserved and the separate qualifying build/provenance/axiom review and integration gates succeed.
