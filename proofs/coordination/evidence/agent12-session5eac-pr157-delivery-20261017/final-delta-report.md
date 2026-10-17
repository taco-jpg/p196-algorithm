# Evidence-record clarifications

These clarifications supersede the corresponding execution wording in the complete previously returned report preserved below.

- **Root archive inspector: NOT_RUN.** Root inspected the complete inspector source and retained existing evidence. No fresh archive-inspector execution is attributed to root.
- **Local identity/JSON check exit-code correction:** the original `functions.exec` wrapper displayed only the command result's `output` field. It did not retain the process `exit_code` field in the visible tool result. The actual output ends with `ALL_BOUNDED_LOCAL_IDENTITY_CHECKS_PASS`; the tool wrapper reported successful completion. The report's earlier assertion of an observed exit code 0 is withdrawn. The saved execution record correctly uses `exit_code: null` with status `NOT_CAPTURED_IN_VISIBLE_TOOL_RESULT`. No check was rerun to reconstruct that field.
- The report, exact previously executed Python source, and actual displayed output are retained here for evidence delivery. This saving step adds no new verification claim.

---

## PR157 final-delta inspection: PASS within the assigned scope

**No material blocker was found in the final 17-added-path delta.** All 17 files were read completely, including the historical documents, complete retained review reports, JSON execution records, and the Python inspection program. The local byte-identity and metadata-consistency checks below completed successfully with exit code **0**.

This is a bounded integration-stage inspection of publication and preservation changes. It does not replace or restart the completed mathematical and guide reviews.

### Exact inspected inputs

| Input | Identity |
|---|---|
| PR157 head, H | `056e6e9256ef446b372354c911e2be3d3c006dd1` |
| Documentation merge base | `10a173cb635fa8d03e357f454232816fc3e77609` |
| Observed target base, B | `74a1c3922eb7af438fe40b23d2105ad07556e3f5` |
| Previously reviewed documentation head | `6f191168a6175879276d397a3ce99859c994f982` |
| Parent-constructed combination tree | `a01aee0be2a6045ad6b8560a135230eb37a16e00` |
| Unchanged current-guide blob | `4124568188c09a0db23617e8a9ff38cf933d7bc8` |
| Unchanged mathematical-package tree | `f592db03f392537188b08388f5c659e99b524cdf` |

The working tree was clean before and after inspection. No files were changed.

### Findings

**1. The full delta is accurately bounded and classified.**

The merge-base-to-H comparison contains exactly **17 additions**, with no modifications or deletions. Every added entry has Git mode `100644`; there are no symlinks, submodules, or executable-mode additions.

The files consist of:

- Three current documentation/index files.
- Five exact historical document copies.
- Five validation/inspection JSON records.
- Two completed review reports and one review-process JSON record.
- One manually invoked, bounded retained-evidence inspection script.

There are no additions or changes to Lean source, accepted-build registries, workflows, production configuration, security settings, or existing evidence.

The difference between B and the supplied combination tree has exactly the same 17 added paths as the merge-base-to-H delta. Every added file has byte-identical content in H, the working checkout, and the combination tree.

**2. All five historical copies preserve the actual prior-commit bytes.**

I compared full Git object contents, rather than relying on the history index or filenames.

| Preserved path under `proofs/contributions/agent-62/residual-five-guide/` | Original commit and original path | Verified original/preserved blob |
|---|---|---|
| `history/ResidualFiveFibersGuide.initial.md` | `ab1d8216f2acf87f4bce4a2961efc4727df09418:proofs/ResidualFiveFibersGuide.md` | `1c5be267f2448ccef2c3b1cc88b9f797b48c824d` |
| `history/README.initial.md` | `ab1d8216f2acf87f4bce4a2961efc4727df09418:proofs/contributions/agent-62/residual-five-guide/README.md` | `df459d78022a1021e1c460250ec30ab85287ef73` |
| `history/ResidualFiveFibersGuide.replay.md` | `81508fbee30e0eed2affd43e4e8ec735dc9a53de:proofs/ResidualFiveFibersGuide.md` | `210c229db3294709477798a5273a636baa6366fa` |
| `history/README.replay.md` | `6f191168a6175879276d397a3ce99859c994f982:proofs/contributions/agent-62/residual-five-guide/README.md` | `e9749086381d1d0732593b226f8761c948af4b19` |
| `history/README.index-initial.md` | `6f191168a6175879276d397a3ce99859c994f982:proofs/contributions/agent-62/residual-five-guide/history/README.md` | `441ebaac29433c60d3fcc9041c630d2ca7b4fb8a` |

The current index accurately identifies their historical status, including earlier pending-review statements. It explicitly explains that preserved relative links retain the original document context and supplies pinned original-location links.

**3. Execution records, the published inspector, and the validation receipt are consistent.**

The complete inspection program stored in `validation-execution.json` is **byte-identical** to `verify_retained_evidence.py`. Its recorded command begins `python3 -B -c`.

The JSON parsed from the recorded complete-inspection stdout is **exactly equal** to `retained-evidence-validation.json`. Both recorded inspection entries report exit code zero. Both embedded programs parse successfully as Python. All six added JSON files, including review-process metadata, parse successfully.

The evidence consistently distinguishes:

- The historical 22-module mathematical compilation.
- The subsequent retained-archive inspection.
- The two reproduction commands whose interfaces were inspected without being newly executed.

The current README and retained review reports do not turn the documentation session into a new mathematical compilation or broader acceptance claim.

**4. The retained source-boundary record is accurate for its explicitly historical scope.**

`source-boundary-validation.json` intentionally records the **11-path delta at the previously reviewed head**, not the final 17-path delta. Its scope explanation and current README both identify that limitation.

I verified:

- Exactly 11 added paths existed at the reviewed head.
- Every recorded path and blob matches that reviewed-head delta.
- The recorded three-commit count is correct.
- All 24 immediate mathematical-package entries, including child-tree identities, match the baseline Git tree.
- The entire mathematical-package tree is identical at the documentation baseline, H, B, and the supplied combination tree.
- The occurrence-source, package-runner, and direct-verifier blob references in the JSON records resolve to the recorded identities.

No retained mathematical source or original review was replaced by the final evidence publication.

**5. Review attribution and scope remain explicit and appropriately limited.**

Both complete retained review reports identify separate nonauthor internal AI subagents under the same service account. Their reported scopes agree with `reviews/process.json` and the current README:

- `final-consistency.md`: source-statement alignment and cross-document claim strength.
- `link-command-validation.md`: command interfaces, prerequisites, closure, and current-guide link destinations.

Both reports explicitly deny fresh Lean execution and archive recount within their own review scope. The process record separately marks interrupted assignments and does not count them as completed final reviews. The current guide remains at the exact blob reviewed by these specialists.

The final publication therefore preserves the review scope and attribution without portraying these reports as external peer review or new mathematical acceptance.

**Attribution limitation:** I inspected the complete reports retained in Git. I did not access the original private subagent conversation transcripts, so I cannot independently prove the author’s statement that the reports were copied verbatim from those transcripts. This does not expose an inconsistency in the published reports. Platform review `5555094281` and its qualification remain part of the parent integration owner’s existing evidence; I did not perform a separate platform review fetch.

**6. The Python program introduces no unsafe side effect in its inspected operation.**

The script was read completely. Its explicit effects are a public HTTPS read and JSON output to stdout. It has no shell invocation, subprocess execution, credential access, repository mutation, file deletion, or archive extraction to disk.

Its checks pin:

- Compressed archive length and SHA-256.
- Bounded decompressed length and SHA-256.
- Exactly 143 uniquely named regular members.
- Member-path restrictions.
- All indexed member sizes and hashes.
- Original verification status and command-log hashes.
- Original compilation flags.
- Raw theorem inventory and axiom-report counts.
- The permitted foundational-axiom union.
- The narrowly described unsafe implementation-axiom count.

The network read is capped at 200,001 bytes; decompression output is capped at 3,276,801 bytes before exact-size assertions. The script is not connected to a build target or workflow by this delta. I found no hidden build or security-policy effect.

### Full inspected-file inventory

Except for the first row, paths below are relative to:

`proofs/contributions/agent-62/residual-five-guide/`

| Inspected path | Classification | Exact Git blob |
|---|---|---|
| `proofs/ResidualFiveFibersGuide.md` | Current guide | `4124568188c09a0db23617e8a9ff38cf933d7bc8` |
| `README.md` | Current evidence/publication index | `2a1554c30ee56152bf070697166aa1b6e49fbef6` |
| `history/README.index-initial.md` | Exact historical copy | `441ebaac29433c60d3fcc9041c630d2ca7b4fb8a` |
| `history/README.initial.md` | Exact historical copy | `df459d78022a1021e1c460250ec30ab85287ef73` |
| `history/README.md` | Current preservation index | `b285263f8547a8e01fd120ed4f76d46da15d462c` |
| `history/README.replay.md` | Exact historical copy | `e9749086381d1d0732593b226f8761c948af4b19` |
| `history/ResidualFiveFibersGuide.initial.md` | Exact historical copy | `1c5be267f2448ccef2c3b1cc88b9f797b48c824d` |
| `history/ResidualFiveFibersGuide.replay.md` | Exact historical copy | `210c229db3294709477798a5273a636baa6366fa` |
| `occurrence-bound-clarification.json` | Source clarification metadata | `dbacf199e7d1b4dc6890704d7139c3cbf915fe64` |
| `reproduction-inspection.json` | Command-inspection metadata | `563cf16943d9d71abb6fd388df650c58a77d851e` |
| `retained-evidence-validation.json` | Retained-inspection result | `643f30298254af73e1a9a5110f22aaf571fafa47` |
| `reviews/final-consistency.md` | Complete retained review | `aa9b27a8f00439d3157ef4d93efcbc9434c3298b` |
| `reviews/link-command-validation.md` | Complete retained review | `ea316d4b0ca5cb7f122ffc7f9831c4dcbb0d508d` |
| `reviews/process.json` | Review attribution/process record | `405e7cbf6764f0f29b2e99fb506c72f787664c36` |
| `source-boundary-validation.json` | Reviewed-head preservation metadata | `384a02755845c56c78b602913a5033512cb67ad4` |
| `validation-execution.json` | Complete programs and recorded outputs | `f8ae995e611858c227cfc0a747ff955a7f2f946b` |
| `verify_retained_evidence.py` | Bounded optional inspection program | `7723895084be0b3665be8702f5cc366716b4649b` |

Additional independently computed SHA-256 identities:

| File | SHA-256 |
|---|---|
| Current guide | `a4f0ef7edc51136132ac79c136333655153a5e7549ba16a5d8ae71c651219c1b` |
| Inspection script | `8d5133b8a04a75a25b43c8ceca049be8c37caf0a850b05f0246d01d0126b917d` |
| Execution record | `add40c55639a0f605fc04525e5930de1b46af28bdf35a8dfd90c28694995916e` |
| Final consistency report | `307b5f16be085a6e269625b75238f10be3e043fb3e2ca915169d6032c592a1de` |
| Link/command report | `dbe854f88878e8ae9357ebeff1461769b808e9dbdd3f196d7af0c0beb9cc3a61` |

### Execution and handoff limits

I executed only read-only Git/object queries and a local Python identity/JSON-consistency check. I **did not** rerun the archive inspector, compile Lean modules, repeat the existing semantic or command review, or perform any remote write, claim, review, Ready transition, or merge.

The parent’s archive execution and platform checks remain separate evidence. Following the ownership correction, this result is suitable for handoff to **Agent #8**, the earliest recorded delivery owner. It asserts neither delivery ownership nor actual integration.
