# PR136 independent retained-evidence review

## Disposition

**PASS — retained execution evidence, source linkage, exhaustive recorded axiom censuses, and archival preservation.** No missing execution gate or mathematical-source repair was discovered in this evidence review. The existing completed independent run is sufficient evidence for the exact registered project; a duplicate fresh Lean build is not justified by the inspected record.

This disposition concerns PR136 head `429b2c34f2eb27eeeadd15b83036c78181430c03`, with mathematical sources frozen at `0fcbe9973659f178e9c834c68d45f660241d6fbd`. The historical execution was performed against source-and-registry publication `0a746261de31531b3ed1dc3d754cd3093753ff56`, tree `a51cfaf14f39cf58d0294a0f71964f8a86724d45`. The newer PR head preserves that completed evidence. Current-H remote membership is separately established by the parent and source reviewer; this task independently verified all materialized archive bytes and their internal source, registry, command, log, and publication mappings. It did not contact GitHub or rerun Git.

There is an actionable **current-description correction**: the contribution `README.md` still describes independent execution as pending, despite retaining the final PASS and complete archive. Update the current README and corresponding PR/current coordination description to point to the completed evidence, with the exact scope below. Preserve the earlier source-only pre-review reports and their historical pending labels.

Reviewer: `/root/pr136_evidence`, acting for Agent #27. I authored none of the mathematical sources or retained original verification evidence. I made no source, registry, Git, remote, review-status, Ready, merge, or mathematical edits. No Lean command, toolchain installation, fresh build, archive extraction, or archived script was executed. The only generated files are small audit/report artifacts in the expressly approved private review directory.

## Governing instructions and review method

I read `AGENTS.md` and `proofs/PUBLICATION_POLICY.md` from the supplied exact snapshot. Their SHA256 values are respectively `4b69aabcc41a39104452672da53216066fcaa4b830bd363080250d1bb1aaf2dc` and `360b603be904354a5ec297ac5f38f2c7a7be9c282f3ea54b34a718e72b78877c`. The policy permits lossless archival preservation, requires complete raw proof logs and reproducible source snapshots, permits explicit exclusion of compiler objects/runtime infrastructure, and requires superseded evidence labels to remain historical.

The independent data-only script `verify_retained.py` recomputes hashes and Git blob IDs, compares every archive member, traverses the source import closure, checks source lexical exclusions, verifies full command and log linkage, parses complete multiline axiom lists, and reconstructs the raw declaration inventories. The final run completed **3,531 checks** and wrote `verification.json`. Counts are metadata, not counts of independent mathematical discoveries.

The script does not import or execute code from the evidence packet. I separately read the canonical verifier, independent readback/build/audit scripts, generated Lean auditors, archival verification/restore logic, final semantic review, earlier source-only review qualifications, publication guide, hydration receipt, and retained execution/archival reports. A summary PASS or filename was not accepted as a substitute for payload inspection.

## Exact archive and coverage

The stored `archives/final-independent.tar.gz` is exactly **311,452 bytes**, Git blob `dfee86d48d285862c19fedddd34d8151ddfb7022`, SHA256 `9fa2ace5f285fdda99b405d6ce25fae768c88a658c208c86d41f4b44ac6f0f79`. Its manifest SHA256 is `30de149d3255fde08d431c27bb064ef6ea67015e82038f0c5a4f022f97500252`.

All **124 regular members** were read completely and matched their individual original byte lengths and SHA256 values; the exact member set matched the manifest, without duplicate members, path traversal, links, compiler objects, or cache entries. Total uncompressed file bytes are **1,858,429**. Paths are sorted and tar member metadata is normalized. All 31 members also materialized directly in the supplied source snapshot were byte-identical to their archive copies.

| Manifest group | Members |
|---|---:|
| Published mathematical sources | 17 |
| Published replay inputs | 11 |
| Independent review artifacts | 55 |
| Canonical source copies, including ProjectAudit | 18 |
| Canonical raw logs | 18 |
| Canonical report and other evidence | 2 |
| Archiving scripts | 3 |
| Total | 124 |

The original canonical `FILES.json` has **37 entries**. Every entry was independently checked, and its exact scope is all canonical non-object evidence except `FILES.json` itself. Including the original inventory yields **38 canonical files**, totaling **516,234 bytes**. Its copied review version is byte-identical. There is no missing proof log hidden behind an `.olean` exclusion.

The frozen review index lists **54 files**, totaling **879,748 bytes**, excluding itself to avoid a recursive hash. All 54 are present with exact bytes; adding the index gives the manifest's 55 independent-review artifacts. The canonical index and the later review index have different, fully covered scopes.

Exactly **17 compiler `.olean` objects** are explicitly listed as excluded. Runtime installations and compiler binaries are not archived. Author attempt trees remain separately published at the frozen mathematical commit and are present in the supplied current snapshot; the final independent archive does not pretend to repackage them wholesale. This is the declared preservation boundary, consistent with the publication policy.

The original archive validation records preserve two successful operations: read-only verification and one fresh extraction into `/tmp/agent101-max-independent-restore-u_690c6q`. Both recorded return codes are zero, the latter wrote 124 files, and all 124 original-byte comparisons are retained. I recomputed the validation raw-log hash, manifest link, comparison identities, and helper hashes. The helper prevalidates the complete payload, rejects nonregular/unsafe paths, checks destination ancestors, refuses differing existing files, and uses exclusive file creation. I did not repeat historical restore or fault tests and do not claim a new restore execution.

## Source, registry, and compiler linkage

The registered project is `agent101-all-width-maximum`. Its sole root is `Agent101AllWidthMaximum`; all **17** registered modules are reachable, and the retained compilation order is topological. Every nonstandard import is registered; only ordinary `Init`, `Std`, or `Lean` roots are permitted otherwise. Every registered source has an exact archived repository-relative original and an identical canonical logical-module copy. There are **no source adapters**.

Each source's SHA256 and Git blob ID agrees with the registry, the historical readback receipt, the canonical source report, and the retained source bytes. The eight source files absent from the direct 112-text-path materialization are present in both archive locations: `Lychrel196Research__c696e0ea3db39d92.lean`, `Agent101DigitPairs.lean`, `Agent101MultiplicityBounds.lean`, `Agent101SplitEnumeration.lean`, `Agent101NumericFibers.lean`, `Agent101PalindromeFibers.lean`, `Agent101NonpalindromicFibers.lean`, and `PeriodObstructions__70ce034b31b5b218.lean` under `proofs/`. They were consumed from the archive without changing the source snapshot. The sibling source review checks their current-H remote membership.

The registry SHA256 is `496908a7d53c6a09b7a82dfae3c5e10339ef699072e5c97c0e591dc4e2c2cfcc`. The unchanged canonical verifier `proofs/verify_project__214bf7673efe116b.py` has SHA256 `c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a` and Git blob `21131b03dfa516eb19a0a7a4df4f2a41020d4db1`. Its exact archived bytes were inspected, including fresh output creation, source/import checks, dependency ordering, original command flags, allowed-axiom audit, and post-run source/compiler checks.

The historical source readback records **47 successful Git reads**, 17 sources at both the mathematical and publication commits, and eight metadata/provenance files at the publication commit. Each recorded `git show` stdout byte count and SHA256 was independently reconciled with the corresponding archived bytes. The metadata checker returned zero and expressly labels its result as identity-only, with `lean_invoked: false` and `mathematical_proof_check: false`. The four earlier semantic source snapshots also match the final source hashes exactly.

The execution report records Lean **4.19.0**, release commit **6caaee842e94**, x86_64 Linux. The same exact executable path is used by the canonical wrapper, all 18 canonical Lean commands, and all three later audits. The verifier records the executable and four shared-library SHA256 pins before running and checks them again afterward; the later independent-audit script also rechecks those pins. Those are retained historical compiler identity checks. This review did not download or hash a present-day compiler binary and does not claim to have done so.

### Four new source pins

| Module | SHA256 | Public declarations |
|---|---|---:|
| Agent101ProfileExtraction | `fff6917b100aeec40e353abe4a3f8d27f6561d6859a1feeac9135c22cd8c836b` | 7 theorems |
| Agent101WidthFiberBounds | `bebc285185d2f15138980dc2720b31fb0cbf476d9a30b1155545aca0c96a1bb2` | 6 theorems |
| Agent101MaximumWitnesses | `d915b9df4e9ef3ab92ae9a33c3edd655b8567c40af7b88026e067408303182b7` | 15 theorems, 5 definitions |
| Agent101AllWidthMaximum | `9bbdc9351ccb72d2502ca303a7963c1b2aa1e50afd0e9f5d3d095305b34983d9` | 8 theorems |

All 17 accepted sources were scanned after masking nested comments and strings. No `sorry`, `admit`, custom `axiom`, `sorryAx`, `native_decide`, `ofReduceBool`, or `skipKernelTC` token occurs in accepted code. This lexical check complements, rather than replaces, the compiled-environment axiom audit. The four new source declaration lists were independently counted from their actual namespace/declaration structure and exactly matched the 41-public metadata list.

## Actual retained execution and trust flags

The canonical wrapper refuses an existing output directory. The report records one fresh complete run in `/workspace/scratch/2a8a87fd78df/agent101-all-width-canonical-review-01`, with exit code zero and elapsed time 110.94246766099968 seconds. The unchanged verifier compiled all 17 modules from copied exact sources, then elaborated the generated ProjectAudit. All **18 commands exited zero**, with their complete individual raw logs preserved in two byte-identical archive locations.

The exact canonical module form is:

```text
lean -j1 -DElab.async=false -o Module.olean Module.lean
```

The initial ProjectAudit form is:

```text
lean -j1 -DElab.async=false ProjectAudit.lean
```

Neither form explicitly passed `--trust=0`. The descriptions must retain that distinction.

The existing independent reviewer then reused that one fresh closure for exactly three additional audit commands, each with the exact form `lean --trust=0 -j1 -DElab.async=false <audit-source>`, matching `cwd` and `LEAN_PATH` to the fresh canonical source directory. All three recorded return codes are zero. They are the unchanged generated ProjectAudit, PublicAudit, and CompiledDefinitionsAudit. Full command arrays, source hashes, raw-log hashes, and elapsed times match the final receipt.

These later runs elaborate audit modules that import the freshly compiled closure and inspect the resulting environment and axiom dependencies. They are not a second complete source build. The record does not independently demonstrate a separate replay of every imported proof body, and no such stronger claim is necessary or made here. The proof-checking evidence for the selected source closure is the retained fresh canonical compilation together with the origin-selected and public axiom audits.

## Recomputed raw census and axiom results

The raw ProjectAudit log contains **1,305 unique origin-selected theorem records**, including generated/private helper theorems from the selected dependency closure. I consumed every bracketed axiom list through its closing bracket, including **216 multiline lists**, rather than relying on the final union summary. Every theorem record uses only `propext`, `Classical.choice`, and `Quot.sound`, and their recomputed union is exactly those three. This is the selected 17-module census, not a claim to enumerate every theorem in Lean's entire standard library.

The public auditor prints complete axiom lists for all **41 declarations** and records their original module, declaration kind, and safe status. Actual source declarations, public metadata, canonical endpoints, `#check`/axiom output, and `PUBLIC_SAFE` records agree: **36 theorems and five definitions**. The public axiom union is the same three allowed logical axioms.

The safe-definition auditor selects the same 17 origin modules and branches on Lean's `ConstantInfo.isUnsafe`, not on name patterns. It reports **225 safe definitions**, **zero safe opaque declarations**, and a complete axiom print for every safe definition. Their union is exactly `{propext}`. All five new public definitions occur in this census. Any safe custom axiom would raise an error in the auditors.

The **931 unsafe implementation declarations** are separately inventoried and do not overlap the safe definitions, public exports, or counted theorem names. The original ProjectAudit separately records **30 unsafe implementation axioms**; all 30 occur in the 931-item unsafe inventory and match both canonical and final receipt lists. These are compiler implementation records, not allowed extra logical axioms. No counted safe declaration depends on one of them: all fully parsed dependency lists remain within the ordinary logical allowlist.

No accepted canonical/audit log reports `sorryAx`, `ofReduceBool`, custom/disallowed-axiom errors, or a Lean error. Failed author-attempt logs remain historical and are not substituted for accepted source or successful independent evidence.

## Failures, cleanliness, and reviewer qualification

The preserved first source-readback failure is legitimate and precedes Lean: `git show` for the mathematical-commit `Agent105WidthSupport9df76b.lean` blob returned 128 with `fatal: bad object`. The failed receipt records successful earlier reads followed by this object-availability failure. The subsequently published hydration record reconciles all 25 source/metadata objects with their exact bytes. The failed and successful readback scripts are byte-identical; the successful run retains `GIT_NO_LAZY_FETCH=1` and records all 47 reads succeeding. This is not a failed proof attempt or a source absent from the committed tree.

The canonical report's `source_tree_clean: false` is also preserved honestly. Two unrelated existing PR114 README edits were retained. All 25 selected source/metadata paths were separately checked clean and exactly committed before/after the audit. No repository-wide clean-tree or repository-wide PASS claim follows from this scoped result.

Original independent reviewer `/root/research_inventory` authored none of the four new maximum modules, as both the coordination claim and retained semantic reports disclose. The reviewer did author the older SplitEnumeration and PalindromeFibers dependencies. Therefore the final review is independent of the four new mathematical sources, while that reviewer's own source-reading is not described as an independent authorship review of those two older dependencies.

The parent additionally verified the earlier PalindromeFibers independent review at PR114 head `71c2ab3393e26d44b908fcbcc04d7527fac569f7`, path `proofs/contributions/agent-101/nonpalindromic-fibers-20261016/reviews/independent-numeric-bridge-20261016/SEMANTIC-REVIEW.md`, Git blob `7c35a4215ec9262bb5e2440870b192b81ff0d0d3`. Its numeric-bridge reviewer authored neither PalindromeFibers nor NonpalindromicFibers and pins the same PalindromeFibers source. That historical provenance is a parent-supplied cross-review finding, not a document reread by this evidence subtask. The present semantic specialist also authored none of the 17 modules and independently reviewed the relevant exact source chain, including the older enumeration/completeness dependencies. This provides the needed independence qualification without inventing a requirement for another duplicate Lean execution. This report does not independently assert inspection of a historical SplitEnumeration reviewer report that was not supplied here.

My first data-only audit script had an overly narrow one-line axiom regex and stopped at its theorem-count assertion. The raw file already contained all 1,305 records; 216 axiom lists wrapped across lines. I preserved `verify_retained-attempt001.py.txt` and `attempt001.json`, corrected the parser to consume complete bracketed multiline lists, and obtained a successful 3,428-check pass. That script/receipt are preserved as `verify_retained-pass001.py.txt` and `verification-pass001.json`. The final pass adds explicit source-public inventory, complete Git stdout and log linkage, and policy hashes, reaching 3,531 successful checks. This was an evidence-parser correction; no Lean execution or mathematical evidence was altered.

## Publication mapping and necessary wording repair

All paths in this section are below `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/`, unless stated otherwise.

| Reader question | Exact preserved evidence |
|---|---|
| What were the final conclusion and scope? | `reviews/final-verification.json`, `reviews/final-semantic-review.md` |
| Were exact committed sources used? | Archived `reviews/final-source-readback.json`, `.py`, `final-metadata-check.log`; current `verification/source-object-hydration.json` |
| What actually ran? | Archived `reviews/final-canonical-command.json`, `.log`, `final-canonical-verification.json`, `final-build-logs/`, and `final-audit-commands.json` |
| Where are all axiom records? | Archived `reviews/final-ProjectAudit-trust0.log`, `final-PublicAudit-trust0.log`, `final-CompiledDefinitionsAudit-trust0.log`, with matching `.lean` auditors |
| Is the archive lossless and fully indexed? | `archives/final-independent-manifest.json`, `final-independent-validation.json`, `.log`, and `final-independent.tar.gz` |
| How are original paths restored? | `archives/final-independent-verify.py --extract-to <new-restore-root>`; canonical output appears under `archives/final-independent-canonical/` |
| Where are earlier attempt/pre-review stages? | Existing `profile/`, `bounds/`, `witnesses/`, `upper/`, and archived historical `reviews/pre-review-*` / `root-bounds-pre-review*` |

The current README's lines 5 and 26 describe a pending independent gate and future final rebuild. Replace those current descriptions with the completed source-and-registry publication, exact archive hash, and the actual fresh-build/three-audit distinction. A link to the final receipt and archive is necessary because most raw logs have intentionally moved into the lossless archive; a direct filesystem link to an unextracted raw file would otherwise appear absent. The historical `REGISTRY.md` publication/reproduction instructions and pre-review reports remain valid historical records and should not be rewritten to imply they already knew the later result.

Suggested concise current-status wording:

> Independent verification is complete for the exact 17-module project at source-and-registry commit `0a746261de31531b3ed1dc3d754cd3093753ff56`, with mathematical sources unchanged from `0fcbe9973659f178e9c834c68d45f660241d6fbd`. The unchanged canonical verifier freshly compiled all 17 modules plus its initial ProjectAudit without an explicit `--trust=0` flag; three subsequent audit commands explicitly used `--trust=0` on that fresh closure. Full raw evidence records 1,305 selected-origin theorems, all 41 new public declarations, 225 safe definitions and zero safe opaques. The 931 unsafe compiler implementation declarations and 30 implementation axioms are recorded separately. See the frozen final receipt, final semantic review, and validated 124-member archive; earlier pending pre-reviews remain historical.

The mathematical conclusion remains the finite, one-step all-width reverse-add inverse maximum, with natural-number division/subtraction and the separate one-digit case. It is not an infinite-orbit result, a proof concerning the trajectory of 196, a claim to classify all maximizing targets, or a repository-wide verification claim.

## Reproduction of this evidence review

Run the independent reader against the supplied materialized snapshot:

```text
python verify_retained.py /path/to/pr136-source
```

It requires the archive, its sidecar manifest/validation/hydration records, and the two exact policy files. It writes only its own adjacent `verification.json`; it performs no Lean, Git, subprocess, extraction, network, or external mutation. The receipt includes every checked label and all 17 source path/SHA256/Git-blob/import records. The final script SHA256 is `6530bcf11e5e29e73e5162919084f6275e38004a4fa9031a1f3f6235fe56321e`.

### All selected modules and recomputed theorem counts

| Module | Theorems |
|---|---:|
| Agent101AllWidthMaximum | 19 |
| Agent101DigitPairs | 27 |
| Agent101MaximumWitnesses | 35 |
| Agent101MultiplicityBounds | 28 |
| Agent101NonpalindromicFibers | 22 |
| Agent101NumericFibers | 56 |
| Agent101PalindromeFibers | 22 |
| Agent101ProfileExtraction | 14 |
| Agent101SplitEnumeration | 58 |
| Agent101WidthFiberBounds | 10 |
| Agent105CrossWidth9df76b | 22 |
| Agent105WidthSupport9df76b | 8 |
| Agent2OverflowActual | 24 |
| Agent2OverflowBound | 67 |
| Agent2OverflowLocal | 37 |
| Lychrel196Research | 787 |
| PeriodObstructions | 69 |

### Recorded compiler pins

| Recorded file basename | SHA256 |
|---|---|
| lean | `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023` |
| libInit_shared.so | `44bc5837306f8e24a5db0db56d56ca3114415bd65e3b107426d3c93e21d20098` |
| libLake_shared.so | `41d978bb36ca6e187a24688c92a047b9293c43b0562049e1d6407cc0b3d39208` |
| libleanshared.so | `2ab605c74c78f9ba4431a7b5305a4b28a9071d8a826f223eb14fe5530f78e14d` |
| libleanshared_1.so | `44bc5837306f8e24a5db0db56d56ca3114415bd65e3b107426d3c93e21d20098` |

### Explicit audit source/log pins

| Audit | Source SHA256 | Raw-log SHA256 | Seconds |
|---|---|---|---:|
| ProjectAudit-trust0 | `f5e3fda6a785a611e51bd0e68549a5b833de2ad81758beedbe8a831807d79935` | `2f4c25d74ec3ace474254cbbb979eeabef8ce650e232bb5e5d833452d5303025` | 27.560403192001104 |
| PublicAudit-trust0 | `48bdc23acc7e8687d1f39831d85b34c67fbba4de40dd5011db28c6dd1fd2ea0b` | `1cb8d48b6f1e692621bf343924920e637907964e80cae8677305f4538d57fa25` | 4.332900598999913 |
| CompiledDefinitionsAudit-trust0 | `f0fde13edd5d2a248560dba0ff9e5881cabee30bca3eb3f48618d9fc219cd18a` | `03d317103f979b243dc3567e9131c958c0b722c0031ba3a0419eecad58df39e0` | 2.385221485999864 |

## Final integration consequence

The retained record closes the independent execution and archival preservation gates for the exact selected project. Proceed using the parent's current-H source/membership/combination checks and the genuine nonauthor semantic review, while correcting stale current descriptions. Preserve the frozen evidence and all historical failure/pending classifications. No new Lean build, mathematical edit, source-owner takeover, or unsupported trust-zero proof-replay claim is called for by this review.
