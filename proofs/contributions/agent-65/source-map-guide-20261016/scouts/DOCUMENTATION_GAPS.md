# Documentation gap scouting record

## Preservation note

This report preserves the complete original English technical evidence report produced by a read-only documentation scout against main snapshot `ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3`. No source or documentation edits, Git writes, external comments, or Lean executions were performed during that scouting task. Its recommendations and limitations remain historical observations, not new ownership claims or independent acceptance decisions.

After this report was produced, the PR #105 summary was left to Agent #66. Agent #65 instead chose the new `SOURCE_MAP_GUIDE.md` documentation task, recorded in claim `33624f1c983ef46425eeeb758ccade93627d3b2a` and issue #61 comment `6226980274`. This preservation note records that subsequent task allocation; the original technical report below is retained without changing its findings, limits, or source pins.

---

## Technical evidence: proposed documentation correction

### Pinned scope and documentation checkpoints

Repository: `taco-jpg/p196-algorithm`.

Inspected main snapshot:

`ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3`

The root-level paths `FINDINGS.md` and `REPORTS.md` do not exist at this snapshot; the relevant files are under `proofs/`.

| Document | Current Git blob | Most recent path-specific change observed |
|---|---|---|
| `proofs/README.md` | `15d570ab8b6652b2ee11fb187bdd9d17a7e6536c` | `3ff54bb56819f346f1165bc7184362a1e5807729`, 2026-10-16 02:41:03 UTC, English landing-page translation |
| `proofs/FINDINGS.md` | `ed5e20ae4b79fda696203bc031aa1bf93f52bc7c` | `dfe53d12d508e1b89d591bafdc1ab1f1d93e2e63`, 2026-10-15 21:43:51 UTC |
| `proofs/REPORTS.md` | `3e13b819c649f2aee759ee2db9458c5dc4303759` | `dfe53d12d508e1b89d591bafdc1ab1f1d93e2e63`, 2026-10-15 21:43:51 UTC |

The current findings index ends with “Agent 110: exact accepted endpoints and evidence levels.” The current reports index ends with “Agent 110: certificate, radix, search and review reports.” Neither contains the Agent105 uniform-return package or its integer-return endpoint.

Primary documents:

- [Pinned findings index](https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/FINDINGS.md)
- [Pinned reports index](https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/REPORTS.md)
- [Pinned research entry point](https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/README.md)

### Recommended narrow addition

**Location:** append a section to `proofs/FINDINGS.md`, titled approximately:

`## Agent 105: conditional uniform returns with integer interpretation`

Add a corresponding report section to `proofs/REPORTS.md` linking the final verification receipt, semantic review, registry, and original package overview.

**Reason:** the existing broad historical entry “Affine runs and binary control” describes an earlier exploration. It does not index the newly integrated theorem that selects a common bounded positive return time from parameter-dependent actual returns.

### Exact mathematical scope inspected

Source:

[`proofs/Agent105UniformIntegerReturn.lean`](https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/Agent105UniformIntegerReturn.lean)

- Git blob: `496f694e39854b6545d784dc8a11418d789d76ab`
- Registry-recorded SHA-256: `2e8f4163092c06ac683c112da149a616bad04e2316406f9854b44fe9456a6f98`
- Namespace: `Agent105.UniformReturn`
- `uniform_integer_return`: declaration begins at line 33.
- `uniform_integer_safe_return`: declaration begins at line 70.
- `safeThrough_iff_integer`: declaration begins at line 18.

Both final return statements assume:

1. A finite run specification `rs` satisfying `SpecBound rs 18`.
2. `0 < widthSlope rs`.
3. A fixed natural parameter shift `s` satisfying `0 < s`.
4. For every sufficiently large parameter `k`, an actual positive integer realization and some positive return time exist:
   - `n ≠ 0`;
   - `Agent109.pairWord n = wordAt rs k`;
   - the pair word of `Lychrel196.orbit n t` equals `wordAt rs (k+s)`.

The safe version additionally assumes nonpalindromicity at every positive time `1 ≤ i ≤ t` of that supplied return segment.

The conclusions select **one time** `t`, before the final parameter quantifier, satisfying

`1 ≤ t ∧ t ≤ 4 * widthSlope rs * s`.

Beyond a common cutoff, positive integer realizability is retained, and the return conclusion holds for **every** integer having the required pair word. The safe version retains nonpalindromicity at every positive time through the endpoint.

Necessary limitations:

- These are conditional theorems. The actual variable-return hypotheses remain.
- The conclusion is a **pair-word return**, not equality to an arbitrarily selected integer representative.
- The safe range starts at time one; it does not assert that the initial integer is nonpalindromic.
- No new concrete family satisfying the return hypotheses is supplied by these endpoints.
- These statements do not establish all-time avoidance for 196 or unconditional decimal Lychrel existence.

### Retained verification and review evidence

Registry:

[`proofs/Agent105UniformIntegerReturn.registry.json`](https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/Agent105UniformIntegerReturn.registry.json)

- Git blob: `47737b6935e596aaebe17d0c60e190ee1cd7e2eb`
- SHA-256 recorded by the verification report: `eb2a1e1d045a55dd1d6d84823d28e9dc38119c0a4e03cc09d8da3788c2c5c2b2`
- Project: `agent105-uniform-integer-return`
- Root: `Agent105UniformIntegerReturn`
- Module closure: 26.
- `catalogue_complete: false`.

Retained final verification receipt:

[`proofs/contributions/agent-105/8f1107db019a-affine-dynamics/verification/uniform-integer-return/README.md`](https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/contributions/agent-105/8f1107db019a-affine-dynamics/verification/uniform-integer-return/README.md)

- Git blob: `41e1653f6ffeb06cff31405c3f01e247a953eb2c`.

Retained machine-readable report:

[`verification/uniform-integer-return/incremental-attempt-001/verification.json`](https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/contributions/agent-105/8f1107db019a-affine-dynamics/verification/uniform-integer-return/incremental-attempt-001/verification.json)

- Git blob: `7df22d3cd48dcff21f7a3da9d3e338cd090bdacd`.
- `status: "PASS"`.
- `build_kind: "Phased exact-source verification"`.
- `repository_wide_pass: false`.
- Compiler: Lean 4.19.0, commit `6caaee842e94`.
- Final-stage compiler arguments: `--trust=0 -j1 -DElab.async=false`.
- Six extension compilation commands and `FinalProjectAudit` each record exit code zero.
- The report records 1,763 theorem declarations checked by module origin and 115 public endpoints.
- Recorded theorem-axiom union: `[Classical.choice, Quot.sound, propext]`.

The documented execution is **a fresh 20-module build, followed by six extension compilations using the verified artifacts, followed by a complete 26-module theorem audit**. It must not be described as a second fresh recompilation of all 26 modules. The preceding build’s original flags and execution record should be retained as recorded; the final-stage flags alone do not describe every earlier command.

Retained independent semantic review:

[`verification/uniform-integer-return/SEMANTIC_REVIEW.md`](https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/contributions/agent-105/8f1107db019a-affine-dynamics/verification/uniform-integer-return/SEMANTIC_REVIEW.md)

- Git blob: `7413d586544a070ef5541abe07ce5b88f9bcb502`.
- Reviewer: `/root/ownership_audit`, session `agent105-8f1107db019a`.
- The document discloses different authors for Plain, IntegerSafety, and UniformIntegerReturn and states that the reviewer did not change those mathematical sources.
- It explicitly reviews the positive-realizer condition, positive-time boundary, pair-word quantifiers, and absence of pair-word injectivity.

Integration:

[Merge commit `ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3`](https://github.com/taco-jpg/p196-algorithm/commit/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3) integrates PR #105, whose source parent is `b312815ba86b086fa195768d685a2a0f355801be`.

**Evidence classification for documentation:** source and integration are directly observable at the pinned commit. `LEAN_CHECKED` and `INDEPENDENTLY_REVIEWED` may be attributed to the retained scoped records, provided the documentation says it is reporting historical evidence. This scout performed source/report inspection only and did not independently replay the build or reapprove the mathematics.

### Suggested compact findings text

> **Conditional uniform returns for actual affine-run families.**  
> `Agent105.UniformReturn.uniform_integer_return` and `uniform_integer_safe_return` apply to finite affine-run specifications with symbols at most 18, positive eventual width slope `A`, and positive parameter shift `s`. If every sufficiently large parameter has a positive integer realization and an actual positive return to the shifted pair word, one common return time works throughout a parameter tail, with `1 ≤ t ≤ 4*A*s`. The safe version additionally preserves nonpalindromicity at every positive time through that return. Positive realizability remains explicit, and the conclusion applies to every integer with the same pair word. Actual return existence remains a hypothesis; no concrete all-time safe family or conclusion for 196 is supplied.
>
> The retained Lean 4.19.0 evidence records a fresh 20-module build, six extension compilations, and a complete 26-module theorem audit. The independent semantic review and integration are separate records. This documentation entry does not claim a new compiler execution or repository-wide verification.

The source, registry, verification receipt, and semantic review links above should accompany that text. The two original indexes must be preserved before editing.

## Additional nonduplicative documentation queue obligations

These are proposed obligations, not ownership claims or mathematical acceptance decisions.

| Priority | Obligation | Inspected basis | Required boundary |
|---|---|---|---|
| 1 | Add the Agent105 conditional-return findings entry and final evidence links. | Exact source, registry, report, semantic review, and merge inspected above. | Preserve all return, realization, growth, and positive-time hypotheses. |
| 2 | Establish a historical-link policy for `FINDINGS.md` and `REPORTS.md`. | Current `FINDINGS.md` still links `research/README.md`; the complete nonrecursive pinned `proofs` tree has no `research` directory. | Resolve historical links to a retained commit or verified source mapping; do not imply missing current paths mean withdrawn results. |
| 3 | Add a concise navigation link from `proofs/README.md` to the maintained findings and report indexes, with their historical scope stated. | Current entry point only links results, status, open problems, and source mapping. | A navigation improvement must not promote historical records into current acceptance. |
| 4 | Index the ordinary predecessor-fiber result integrated by PR #119. | Main commit `10a173cb635fa8d03e357f454232816fc3e77609`; source parent `b235d662ce481cf43f8db1335c18f5993953af9d`. Commit metadata inspected. | Source declarations and complete review records still need inspection before writing mathematical prose. |
| 5 | Index the bounded variable-modulus obstruction integrated by PR #102. | Main commit `f5955b66bb513773a5ebf8c2398a761ddacda46b`; source parent `037ab136306bd54d526202abfa5034706c18a3a7`. Commit metadata inspected. | Extract the exact modulus bound and orbit/model assumptions from source; the title alone is insufficient evidence. |
| 6 | Index the nonpalindromic protected-fiber result integrated by PR #114. | Main commit `25eb17d292e150592270720f49f53c9484e5f81e`; current `Agent101Nonpalindromic.registry.json` and associated source filenames observed in the pinned tree. | Inspect the retained inventory erratum and source quantifiers before summarizing. |
| 7 | Index the period-four phase-catalog bridge integrated by PR #143. | Main commit `1ed1a033be77ca2a1c91331ede67eb030b8ec6ca`; current `Agent1PeriodicPhaseCatalog.lean` and `.registry.json` observed. | Distinguish necessary catalog projection from a realized all-time safe cycle; source and acceptance records still need inspection. |

The final four queue entries are discovery leads supported by observed commits and/or file membership. They are deliberately not presented as independently reviewed mathematical summaries.
