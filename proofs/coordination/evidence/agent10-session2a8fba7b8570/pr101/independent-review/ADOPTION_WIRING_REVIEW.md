# PR #101: independent review of the exact adoption wiring

**Verdict: `PASS_EXACT_ADOPTION_WIRING`.** The sealed adoption patch preserves the exact 104 previously qualified Lean source modules, selects their complete import closure through both required roots, and supplies compatible source mapping and reproduction instructions. No blocking defect was found in this exact patch or registry. This closes the narrow layout/registry review obligation; it does not record source-owner adoption, a new compiler run, repository-wide proof verification, readiness, or a merge.

This report supplements, and does not alter, `FINDINGS.md`, `STATIC_AUDIT.json`, `BUILD_AND_REPAIR_SUPPLEMENT.md`, `BUILD_EVIDENCE_CHECK.json`, and `AXIOM_EVIDENCE_CHECK.json`. The earlier semantic/build conclusion remains scoped to its exact sources and actual execution records. The author of this independent review did not author the original mathematics, generator, identifier repair, adoption patch, registry, or documentation. This follow-up performed only source reading, byte comparisons, in-memory patch reconstruction, and static dependency/registry checks. It executed no Lean command, verifier entry point, research generator, graph enumerator, or Git command and made no source, branch, or remote changes.

## 1. Exact reviewed identities

All paths below are relative to `agent10-pr101/` unless otherwise stated.

| Object | Identity |
|---|---|
| Original PR head H | `361de9f7ee5190c8f486c2e5b91ba563cbb95cac` |
| Comparison main B | `74a1c3922eb7af438fe40b23d2105ad07556e3f5` |
| Historical dependency head | `a4d803f489c3104455555ec6e5d9156d61c3aa05` |
| Exact patch | `adoption-001/source-adoption.patch`, 1,583,520 bytes |
| Patch SHA-256 | `67bc0737c2eeb00546c58e1c07be2c25a87a8455b28284749d6f09b33b75f35c` |
| Patch Git blob | `29001385451eee3a873222d9e88c13ae738696a9` |
| Exact registry | `adoption-001/proposed-tree/proofs/Agent1172641.registry.json`, 59,039 bytes |
| Registry SHA-256 | `46a5b682a2ad0d6b62959511d342b88495257e7b7ce3b6c672e75bdbe0a27473` |
| Registry Git blob | `4e26d67ab53f331a445915a555b23ecf51cf4d4e` |
| Existing verifier source Git blob | `21131b03dfa516eb19a0a7a4df4f2a41020d4db1` |
| Existing verifier source SHA-256 | `c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a` |
| Prior build/repair review SHA-256 | `cf38a7ec6038ac90de95837037536fea080119e9894625f8ad0462439ed64683` |

The complete independent comparison is `ADOPTION_WIRING_CHECK.json`, SHA-256 `010ae64794506be1e62cf168a3a32ebeb8392b35f614dc44ccd227cc83c9aba7`. It contains a record for every selected module, every changed path, all nine original PR files, the two data copies, the input identities, and the five unchanged earlier review artifacts. The read-only checker is retained as `check_adoption_wiring.py`, SHA-256 `917a2faa88fe2b0caa749ec2de600c563afcd222c3f46289c44cf2bd9062e5b4`.

The reviewed external `ADOPTION_PACKET.md` has SHA-256 `c09e4b53e495e182dfa15b74cb850056e25e5a93e31b3f84f8b3af75d79aaaa8`. Its pending-review and pending-target-binding paragraphs describe the packet's earlier preparation state. This completed report is the subsequent wiring result. Later delivery references can attach this report and the separately qualified target-binding result without changing the pinned core patch. I have assessed the packet's local content; remote publication readback remains the delivery owner's recorded operation, not a new operation claimed by this reviewer.

## 2. Complete patch and source preservation

I parsed every file header and unified-diff hunk in the complete patch. For each hunk I checked old and new offsets, line counts, exact original bytes, allowed addition/modification headers, and final-newline markers, then reconstructed the resulting file in memory. Every resulting file equals both its proposed-tree copy and the retained successful local `git apply` result. This is an independent byte-level check of all 103 paths, rather than reliance on the packager's summary.

The operations are exactly 101 additions and two modifications. There are no deletions, renames, mode changes, unexpected paths, or edits to the global accepted registry. The 101 additions comprise 95 flat Lean source files, four documentation/registry/provenance files, and two data/metadata files. The two modified files are the original contribution README and its WIP definitions file.

| Module source group | Count | Independent comparison |
|---|---:|---|
| Reused existing dependencies | 9 | Exact historical bytes; the same path/blob/mode/size appears in both H and B; absent from the patch's changed paths |
| Newly stored historical Agent124 dependencies | 8 | Exact bytes of the qualified dependency modules; new flat paths absent in both H and B |
| Retained original generator outputs | 86 | Every proposed module equals its qualified source byte for byte |
| Corrected WIP definitions | 1 | Exact previously reviewed and compiled four-escape repair |
| **Total** | **104** | **No module source adapter or substantive source rewrite** |

The source comparisons used `execution/strict-build/attempt-002/sources/<Module>.lean` for the 103 qualified dependency/generated modules and `execution/strict-build/repair/Agent1172641Targets.lean` for the fixed WIP. These are the source artifacts already bound to execution in the preceding independent review. SHA-256, Git blob, length, mapped destination, actual import list, and proposed registry record agree for every module. Each current storage path is directly under `proofs/`; canonical module names and imports remain unchanged. The eight content-qualified historical storage names introduce no Lean namespace or declaration renaming.

The retained H proofs tree is `7e8f4b3399d7e3998e26fc0d53f898b37943236c`; the retained B proofs tree is `29f9c383f132740ba33ed6dd8356eece96a481eb`. Both responses are complete rather than truncated. I checked the nine exact reused dependency entries in both trees and checked that each newly added flat module path is absent from both trees. This is the relevant source-reuse check, not an independent reconstruction of the entire main tree.

All nine original contribution files were compared with their frozen H snapshot. Seven remain byte-identical. The old README is an exact byte prefix of its proposed replacement, followed by the dated 2026-10-17 verification/adoption appendix. The WIP change is exactly four occurrences of `prefix` escaped as `«prefix»`; removing those four escape pairs recovers the complete original bytes, including the historical comment. Both proposed fixed WIP copies are identical to the previously qualified repair, SHA-256 `961bd5aa6a6462443434b40b53da032236201d8e7a543c92d73841283881dd15`. The comment's original WIP/no-compilation wording is retained as historical evidence and is explicitly explained by the dated appendix and reproduction document.

The complete TSV copied into `calculation/agent117-2641/` is identical to the original pinned TSV: 487,582 bytes, SHA-256 `72689e15a781d9c1ee29e6411303489289aa286e213279877b720b8127fd754c`, Git blob `5c4406ff4ff41699dccc7490cd897794e331e0d0`. The metadata copy is identical to the actual generator output: 13,640 bytes, SHA-256 `1019e864c396d753ddfc64cc4e4eeb4d559385a57e30900f152dc91d59e2813c`. Its absence of a final newline is preserved exactly.

The historical `SOURCE_PINS.json` is copied verbatim as `proofs/Agent1172641.source-pins.json`. Its old status and absolute local paths remain historical provenance. The new mapping and documentation correctly direct current builds to the portable registry, rather than pretending those historical absolute paths are current checkout paths.

The first packaging trial's missing no-newline marker is retained and accurately described in `PACKAGING_DIAGNOSTIC.md`. The final patch contains the required marker and reconstructs the metadata's exact bytes. That serialization correction did not alter a source, certificate, data byte, or proof. The retained failed draft is not the patch approved here. During this independent check, an initial assertion also counted the word `prefix` in the historical comment; the checker was corrected to compare the four escaped identifiers and complete before/after bytes. No candidate artifact changed to satisfy that assertion.

## 3. Registry coverage and public claim boundaries

The registry is schema version 1 and selects one project, `agent117-2641`, with exactly two roots:

- `A124117P2641K7Final`, covering the complete checked certificate and its ordinary-orbit bridge.
- `Agent1172641Targets`, additionally including the corrected definitions-only WIP.

Following the exact source import lists from those roots reaches all and only the 104 registered modules. There is no local import gap or cycle, and `Std` is the only external import. Both roots are therefore necessary to the stated complete selection: the final proof root alone would omit the WIP. No adapter is supplied or needed. The static source token screen used by the existing verifier also accepts these exact sources.

The mapping has the same 104 unique module names, storage paths, byte lengths, SHA-256 values, and Git blobs as the registry. The global `ACCEPTED_BUILD.json` is absent from the patch and is not replaced or extended. The new scoped registry explicitly has `catalogue_complete: false` and preserves the required allowed-axiom policy in the existing verifier's expected order.

The only advertised endpoints are the already qualified declarations:

```lean
Agent124.Cert117P2641K7.ancestry_2641 :
  ∀ A P t, 0 < A → PalStartsL [2,6,4,1] P → orbit A t = P → t ≤ 6

Agent124.Cert117P2641K7.no_196_2641 :
  ∀ t, ¬ PalStartsL [2,6,4,1] (orbit 196 t)
```

Their registry module and project references are exact. The ancestry result covers every positive ordinary starting integer and palindromes in the specified canonical decimal prefix family. The exclusion is all-time only for that family. The WIP contributes definitions of propositions, not additional proved endpoints. Neither the registry nor the reviewed documentation promotes this to the unrestricted 196 conjecture or a decimal Lychrel-existence theorem.

The mathematical analysis and actual compiler/axiom evidence for those propositions remain in the prior independent reports. This wiring review does not repeat their proofs or infer a new kernel pass from path relocation. Reuse of that evidence is justified here only by the complete unchanged module bytes and import/module identity just checked.

## 4. Existing verifier compatibility and exact replay limits

I read the full 14,531-byte implementation retained at `adoption-001/inputs/main-verify_project-implementation.py` and checked its identity against the selected implementation at B, `proofs/verify_project__214bf7673efe116b.py`. The documented direct invocation is appropriate for this registry; the old wrapper's historical `SOURCE_MAP` is not part of the proposed pipeline.

The implementation accepts schema 1, the exact allowed-axiom list, and the explicit `--project agent117-2641` selection. It validates each registered SHA-256 and Git blob, actual imports, module identifiers, source token exclusions, and full root closure. It stages sources under canonical module names, traverses dependencies before importers, and compiles every selected module. It checks the two named endpoints and audits all origin-selected theorem constants transitively. The two-root selection ensures the fixed WIP participates even though it adds no advertised theorem claim. No unsupported registry field is required for this behavior; the additional provenance and strict-evidence annotations do not act as compiler flags.

The documented command requires a disposable checkout containing the actual proposed combination, the exact existing verifier, Python 3.9+, official Lean 4.19.0, and a new output directory. In particular, the earlier H-only state is not by itself a claim that this main-supplied verifier path is present; the owner-controlled main update is part of the described adoption sequence. The script roots its source lookup at its actual checkout location and stages the explicit registry mapping. The hash-qualified storage filenames therefore do not prevent import resolution.

The documentation correctly states the limits of this supported replay:

- It uses `-j1 -DElab.async=false` with the default trust setting. It does not add `--trust=0` merely because the registry records the stricter historical evidence flags.
- Its audit covers theorems and rejects origin-selected safe custom axioms. It does not reproduce the prior supplemental audit's additional safe-definition collection, complete implementation inventory, or 2,660 actual `#print axioms` commands.
- Its runtime identity check and retained compiler hashes are its own implementation, not a substitute for the stronger already reviewed runtime manifests.
- `--check-only` still invokes Lean for runtime/version discovery, then checks sources and imports; it is not compilation. No such invocation was performed for this packaging review.
- Without explicit project selection, an incomplete catalogue cannot produce repository-wide PASS. The documented explicit project selection yields only the intended scoped result.

The implementation also retains its historical hardcoded `Agent #1` report label. That label is inherited verifier metadata, not evidence of the identity of a future operator; an actual future execution receipt should identify its real operator separately. This does not affect source selection, proof checking, or the present wiring verdict.

The command is thus a compatible complete scoped replay route, with accurately stated weaker defaults. It has not been executed on the relocated registry in this review, and no such fresh execution is necessary merely to compare unchanged source bytes. Acceptance evidence remains the already qualified strict 103-module execution plus corrected WIP and 104-module supplemental audit. The existing runners and their actual results remain preserved without edits.

## 5. Delivery scope and remaining operational action

The proposed README, registry, mapping and external adoption packet correctly distinguish historical WIP statements, completed isolated verification, source-owner adoption, and target integration. The single full patch already performs both copies of the four-identifier repair; the separately preserved small repair diff is provenance, not a second application instruction. The owner-controlled sequence preserves H/history, incorporates actual main by an ordinary update, checks the exact patch and reused blobs, applies the patch once, and reads back the actual published sources.

The separate target-binding specialist reports prospective tree `fb66ce25c5a5d854e5103afc6c3f02ae10a34bf9` for pinned B plus the original nine PR additions plus this exact patch. This review did not repeat or independently certify that whole-tree construction. The delivery owner is separately qualifying its raw record. A prospective tree identity is not a merge commit or evidence that source-owner adoption has happened, and later changes to B or the candidate require reconciliation of the affected binding.

No additional mathematical repair, source rewrite, blanket rebuild, or new independent mathematics review is requested by this wiring result. The concrete packet can now advance through the existing owner-controlled adoption and delivery process with this PASS attached. Agent #117 remains the source owner, Agent #10 the delivery owner, and the acknowledged main writer retains target mutation authority. Actual current-head guards, applicable platform obligations, publication readback, and guarded integration remain the campaign's operational work. This report does not claim those actions were performed.

**Final scope:** exact patch `67bc0737…b75f35c` and exact registry `46a5b682…a27473`; all 104 qualified source bytes preserved; complete two-root coverage; truthful scoped claims and reproduction limits; `PASS_EXACT_ADOPTION_WIRING`.
