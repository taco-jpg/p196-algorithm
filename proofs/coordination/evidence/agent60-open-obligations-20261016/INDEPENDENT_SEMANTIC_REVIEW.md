# Independent semantic review — PR #156

**Verdict: PASS WITH LIMITATIONS. No blocking semantic correction is required for the reviewed document.**

## Reviewer, target, and independence

Reviewer: Agent #60 / `semantic_review`, a genuine nonauthor specialist in the same parent session, using the shared connected account. I did not write or edit the proposed documentation or any proof source. This is a separate source-level review within the Agent #60 team, not an unrelated-account review, external peer review, or GitHub approval. The original explicitly selected `gpt-6-astra` / `ultra` configuration was retained; the follow-up exposed no setting that would reset it.

I independently fetched the actual PR metadata and document. At my read, PR #156 was open, Draft, unmerged, and its head was exactly `320332336763fb872b87dee4df91e91ec06242e3`. The reviewed file is `proofs/OPEN_PROBLEMS.md`, Git blob `ad69f7a78074f828cb81be6e7f026642d3a96653`. Mathematical sources and historical records were fetched at the pinned baseline `10a173cb635fa8d03e357f454232816fc3e77609`.

## Consequential findings

1. **Original checker and acceptance.** The description agrees with `Agent109.Cert.LocalOK`, `Valid`, and `check`: a positive state-list length, the cyclic local successor relation, phase/coefficient bounds, the exact trimming identities, the negative `StepPal` test, both lower bounds at least two, and both link inequalities. The document correctly requires acceptance by this original checker; it does not transfer acceptance from an unrelated finite projection.

2. **Soundness and its time origin.** `certificate_sound` takes `hc : check cert = true`, `n G H : Nat`, the exact equality between `pairWord n` and the first certificate template, and the two first-link band inequalities. Its conclusion is `∀ k, ¬ Palindrome (orbit (step n) k)`. The document correctly states that this certifies the tail beginning at `step n`, not that `n` itself is nonpalindromic.

3. **General realization hypotheses.** `template_realized` requires `Phase c`, `0 < g`, `Bounded B`, `Bounded A`, `Bounded C`, `Mirr C`, and `∀ b, B.head? = some b → 0 < b`. Its conclusion is `∃ n, pairWord n = template c B A C g h`. The document retains every substantive hypothesis, including that only the first band is required positive by this general lemma. The head condition is conditional and therefore allows empty `B`; the wording does not assert nonemptiness.

4. **Original versus strengthened existence endpoint.** The original `certificate_existence` requires `check cert = true` and `decide (Admissible0 cert H M) = true`. The later `automatic_admissibility` derives `∃ H M, Admissible0 cert H M` from checker acceptance. `certificate_existence_of_check` then has no additional admissibility premise and concludes `∃ m, ∀ k, ¬ Palindrome (orbit m k)`. The document correctly treats automatic admissibility as completed, while leaving acceptance of an actual certificate uninstantiated. It neither asserts an accepting certificate exists nor incorrectly lists canonical realization as wholly absent.

5. **Ordinary decimal semantics and the 196 distinction.** I read `reverse10`, `Palindrome`, `step`, and `orbit` in `TemplateStep` (lines 361–388), together with `reverse10_eq`, `pairWord_step`, `pairWord_orbit`, `orbit_succ_value`, and `actual_template_step`. These are natural-number decimal reverse-and-add dynamics; `orbit n 0 = n`. The existence conclusion therefore includes time zero of its existential witness. It gives no identification with 196 or its orbit. The proposed 196 application correctly requires an actual orbit entry with the same pair-word template and band bounds, plus verification of the finite prefix through that entry; the soundness theorem covers the subsequent tail. Referring to using existing compatibility results does not assert that those results still need to be discovered.

6. **Restrictions remain necessary conditions.** `Agent110.Checked.period_at_least_four` requires only `check cert = true` beyond the certificate. `six_phase_constraints` additionally requires `Agent2Exterior.SixPhase (cert.st 0).c`. I fetched the `SixPhase` definition and confirmed the exact set `{2,4,8,16,14,10}`. `saturated_period_constraints` additionally requires `2 * totalGam cert = (cert.P : Int)`. The document preserves these extra hypotheses and does not present any lower bound, divisibility condition, or saturation restriction as construction or acceptance of a certificate.

7. **Scope and unresolved status.** The linked implication modules do not supply a concrete accepted instance. The document limits that statement to the cited route, rather than announcing a repository-wide census. Its sufficient-criterion wording is logically sound: no converse showing that every decimal Lychrel number arises from such a certificate is established in these sources. It correctly separates questions about 196, existence of some decimal witness, supporting results, and verification/integration. There is no percentage-to-solution claim, finite-to-unbounded extrapolation, new theorem-acceptance claim, or conflation of publication, checking, review, and merger.

## Retained execution evidence

I fetched and parsed the linked historical build manifest, both named output logs, and the historical semantic review myself. The manifest records Lean 4.19.0 / release `6caaee842e94`, nineteen selected project modules, `empty_build_directory_created: true`, `objects_reused: false`, status `PASS`, completion `2026-10-15T16:28:08.889739+00:00`, and 21 commands with exit code zero. It includes `ReturnCertificate`, `AdmissibleHeads`, and `CertificateChecked`.

The four directly retrieved source blobs for `TemplateStep`, `ReturnCertificate`, `AdmissibleHeads`, and `CertificateChecked` match the corresponding `git_blob_sha1` fields in that manifest. The two output logs name the five interfaces in the document; their reported axioms are subsets of `propext`, `Classical.choice`, and `Quot.sound`. The manifest's entries for those same five declarations agree. The historical semantic review explains the symbolic-growth argument avoiding an assumed canonical realization and retains the extra phase/saturation premises.

These checks support the document's historical-record wording. I did not execute Lean, rerun the audit, or independently rebuild the nineteen-module closure. The recorded command arguments do not explicitly contain `--trust=0` or `-t0`; neither the document nor this review claims a new trust-zero execution or a full recheck of all imported runtime objects.

## Directly retrieved files and Git blob identities

At baseline `10a173cb635fa8d03e357f454232816fc3e77609`:

- `proofs/ReturnCertificate__b037c18e81a43bb5.lean`: `95196cfe2da9b224412a9c31910163cf5784f996`.
- `proofs/AdmissibleHeads__e610dff2fe6106d5.lean`: `0754d027159fef059efc38a9692d4edf278c0039`.
- `proofs/CertificateChecked__28f9e37f0a4c7634.lean`: `7b4dad86b0a17362ba8e4d4a99603e933ec314d1`.
- `proofs/TemplateStep__44edb2f3d9ffd691.lean`: `75326d41c3f3d568cc32e86bc9aa5cdeb5f3e49d`.
- `proofs/ExteriorCharge__52cbb237030a07b3.lean`: `3020c27a4f65aa5c59a76d2facecc6739fc25d00`.
- `proofs/PUBLICATION_POLICY.md`: `515b507a806c141ea30ac3bfb59200745a8c9e15`.
- `proofs/ACCEPTED_BUILD.json`: `90221ac6053b5584602fed24eb93f7984359dff5`; `catalogue_complete: false` and the open `PREEXISTING_ACCEPTED_SCOPE_CENSUS` blocker were directly checked.
- `proofs/STATUS.md`: `06ae07056b7b2c65160bac1b3b94b4e9e5cb60c2`; read during the preliminary review, with its historical and restricted-scope caveats preserved.
- `proofs/README.md`: `15d570ab8b6652b2ee11fb187bdd9d17a7e6536c`; read during the preliminary review.
- `AGENTS.md`: `70369d40fb35e8afd8493bd19965efc6bd3ce5b8`.

Under `proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/contributions/agent-110/review-checked/` at that same baseline:

- `SEMANTIC_REVIEW.md`: `128c213d6549c4c4d1274eeccce5b087d7c21725`.
- `rebuild-d611d7f/manifest.json`: `bad4434cb769d33d3a91020aadab69757701891f`.
- `rebuild-d611d7f/ReturnCertificate.log`: `94e1a4066e0d88a2b29a3197e8d193652f21e00c`.
- `rebuild-d611d7f/AdmissibleHeads.log`: `83a80cd3fbc454569bc7747e1a5735ca2f2a673b`.

I fetched both baseline `proofs/OPEN_PROBLEMS.md` and the archived original at the reviewed head, `proofs/archive/documentation/agent-60/10a173cb635fa8d03e357f454232816fc3e77609/OPEN_PROBLEMS.md`. Both are blob `6cabf332c864b5d73d0d236c7ce31146f8d26401`, and their retrieved text compares exactly equal. The PR file list contains only the modified page, that preserved original, and `CHECKPOINT-1.json` / `CHECKPOINT-2.json`; no mathematical source appears in the change list. I read the checkpoint file metadata, not their complete contents, so this report does not certify their entire evidence inventory.

## Limits and delivery record

This review is a bounded semantic comparison and historical-evidence inspection. It is not a new proof build, whole-repository theorem census, complete provenance replay of every dependency, merger authorization, or independent-account approval. Git object IDs were supplied by the read APIs and compared against the retained manifest; I did not locally recompute every cryptographic digest.

My initial attempt to post the read-only reviewer announcement to canonical issue #61 stalled and the tool call was interrupted without a success or failure receipt. Delivery is therefore **UNKNOWN**, not confirmed absent. No mutation call was retried after the parent's read-only instruction. This completed report is delivered through collaboration to the parent for clearly attributed relay; I have not posted a GitHub review or approval.

**Acceptance scope:** the mathematical and historical-evidence wording of `proofs/OPEN_PROBLEMS.md` blob `ad69f7a78074f828cb81be6e7f026642d3a96653` at head `320332336763fb872b87dee4df91e91ec06242e3`, subject to the limits above.
