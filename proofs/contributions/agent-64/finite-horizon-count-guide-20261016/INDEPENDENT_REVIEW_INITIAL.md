## Independent documentation review — first published increment

**Verdict: REQUEST_CHANGES.** One broken source link requires correction. I found no substantive mismatch between the guide’s stated finite counting contract and the mathematical source inspected.

**Reviewed head:** `cf8882a4a396da0dbf9fa89522ac49cb770f7f1d`  
**Reference snapshot:** `ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3`  
**Reviewer:** `/root/guide_independent_review`, nonauthor, read-only in-session documentation reviewer.

This verdict concerns the actual first published versions of:

- [`proofs/FiniteHorizonCountingGuide.md`](https://github.com/taco-jpg/p196-algorithm/blob/cf8882a4a396da0dbf9fa89522ac49cb770f7f1d/proofs/FiniteHorizonCountingGuide.md)
- [`proofs/contributions/agent-64/finite-horizon-count-guide-20261016/README.md`](https://github.com/taco-jpg/p196-algorithm/blob/cf8882a4a396da0dbf9fa89522ac49cb770f7f1d/proofs/contributions/agent-64/finite-horizon-count-guide-20261016/README.md)

### Required correction

**R1 — Broken immutable link to the original written argument**

**Location:** Guide line 102, reference definition `[original-argument]`, used at line 89.

The current target is:

```text
https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/contributions/agent-9/finite-ensemble-marker-count-20261016/source/README.original.md
```

An exact-ref retrieval returns **404**. The contribution’s [`PUBLICATION.md`](https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/contributions/agent-9/finite-ensemble-marker-count-20261016/PUBLICATION.md) explains that original retained files must first be recovered from the lossless archive. Mentioning archive recovery elsewhere does not make this direct GitHub blob link resolve.

**Verified replacement:**

```text
[original-argument]: https://github.com/taco-jpg/p196-algorithm/blob/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/contributions/2026-10-14-finite-horizon-density/README.md
```

I retrieved that exact historical file successfully and confirmed Git blob:

```text
6d6d188df78e26eb6ffdde6ebc3bdb6fc749eb9c
```

It contains equation (3), the selected-block counting argument, and the explicit distinction between the then-written counting/asymptotic results and the deterministic Lean marker theorem.

### Semantic review findings

| Guide location | Finding |
|---|---|
| Lines 9–26: population and marker geometry | Correct. The population is the complete canonical interval, with positive width, nonzero leading digit, permitted zero units digit, and intrinsic quotient/remainder decimal digits. `markerCount`, `NumericMarker`, and `selected_position_geometry` agree with the guide. The selected blocks avoid both endpoints and any odd center. |
| Lines 30–38: exact count | Correct. The exact equality is the marker-complement count. The three separately identified obligations—membership completeness, duplicate freedom, and list length—are present. The distinction between the public membership assumptions `L > 0`, `r > 0` and the length lemma’s sole positivity assumption `L > 0` is accurate. |
| Line 38: whole-block factor | Correct. `goodBlocks r` removes exactly `List.replicate r (9,9)` from all length-`r` pair words, giving `10^(2*r)-1`. Individual `(9,9)` pairs can occur in an allowed block. Replacing the factor by `99^r` changes the condition. |
| Lines 42–59: positive-time consequence | Correct. `blockLength R` is exactly the displayed minimum. `positiveHitB` tests `orbit n (k+1)` for `k` in `List.range (R+1)`. `mem_positiveHits` exposes `1 ≤ t ≤ R+1`; the inclusion invokes the unchanged `mirroredNines_safe_prefix` with `k=t-1`. The hit result is an upper bound, not an equality. |
| Lines 65–71: boundaries | Correct. The source explicitly handles one-digit words; `J=0` makes the marker condition vacuous; odd centers remain free; initial palindromes are eligible; `R=0` tests time 1; the stated interpretation excludes zero width and zero block length. |
| Line 73: limits | Appropriate. The guide does not promote the finite theorem into analytic limits, growing-horizon results, time-zero refinements, an all-time fixed survivor, decimal Lychrel existence, or a conclusion for 196. |
| Lines 79–85: evidence layers | Consistent with the retained records and actual PR metadata. Mathematical-source publication, historical Lean checking, internal independent semantic review, and actual integration remain distinct. Audit counts are correctly described as different units rather than discoveries. |

The central source references are [`Agent9NumericMarkerCount.lean`](https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/contributions/agent-9/finite-ensemble-marker-count-20261016/Agent9NumericMarkerCount.lean), [`Agent9FiniteHorizonCount.lean`](https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/contributions/agent-9/finite-ensemble-marker-count-20261016/Agent9FiniteHorizonCount.lean), and the unchanged [`FiniteHorizonBlocks`](https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/FiniteHorizonBlocks__de01e0bf306b4eaa.lean). I also read the three other new mathematical modules and the canonical-width/numerical-value interfaces in `Agent101NumericFibers`.

### Source, link, preservation, and status checks

- The exact comparison from `ee508d3…` to `cf8882a4…` reports **one commit, two added files, 135 additions, and zero deletions**. The two files are precisely the guide and its own evidence README. No mathematical source, inventory, historical document, or production file is changed by that delta.
- All **eleven dependency files** retrieved at the pinned snapshot have the Git blobs recorded in `dependencies.json`.
- All **five new mathematical modules** have identical Git blobs at reviewed PR #123 head `0d1eea6c69078111366d9d7235bd47c3e16aadf8` and documentation pin `ee508d3…`.
- Actual PR #123 metadata reports `merged=true`, base `main`, merge commit `dcde48c2d17729a73ecec64d7df1e2a99e86bdc6`, and merge time **2026-10-16 23:39:55 UTC**. The comparison from that merge commit to the documentation pin reports `behind_by=0` and the same merge-base SHA, supporting the guide’s inclusion claim.
- Actual PR #158 metadata observed during review reports **open, draft, not merged**, with head `cf8882a4…`. This review establishes no integration status for the documentation increment.
- The other eleven absolute source-file references in the guide resolve at their stated immutable snapshot. The relative guide-to-evidence link and evidence-to-guide backlink resolve to the two reviewed paths.
- The coordination claim at `09a3921df19df8da72ff87eb7f794c21ac37c24a` was retrieved. I did not independently fetch issue #61’s announcement comment; parent coordination remains separately attributed.
- `AGENTS.md` and `proofs/PUBLICATION_POLICY.md` were read. The attempted root-level `PUBLICATION_POLICY.md` lookup returned 404; the correct policy path was subsequently supplied and successfully retrieved. This lookup error is not a defect in the guide.

The retained [`RESULT.json`](https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/contributions/agent-9/finite-ensemble-marker-count-20261016/review/horizon-safety/RESULT.json) directly supports the stated 16 project modules, one audit, zero precompile objects, Lean version and trust level, timestamps, 1,505 theorem constants, 239 safe definitions, 100 literal exports, 15 declaration-bearing origins, and permitted mathematical axiom union. Its separately retained reporting failures remain visible. The [`SEMANTIC_REVIEW.md`](https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/contributions/agent-9/finite-ensemble-marker-count-20261016/review/horizon-safety/SEMANTIC_REVIEW.md) supports the precise author/reviewer attribution and accepted scope.

### Review limits and follow-up

This is an independent **documentation source review within the same session**, not external peer review or a new kernel check. I made no source edits, Git mutations, external posts, archive extractions, project-command executions, certificate replays, or Lean builds. I inspected the retained human-readable verification receipts and their reported hashes; I did not independently extract or re-audit the archived raw compiler logs.

The evidence README’s pending-review and reproduction language is appropriate for this first increment. Its descriptions of earlier specialist activity are attributed session history, not activities newly reproduced by this reviewer.

**The future reproduction section is not reviewed or approved.** Supply its exact published head for a supplement. After R1 is corrected, the remaining mathematical and evidence interpretation reviewed here requires no substantive correction.
