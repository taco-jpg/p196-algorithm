# Third-gate boundary: finite controls and source review

The original `time6_*` / `time6-scout.*` files preserve their **PRECLAIM_SCOUT / FINITE** identity. Subsequent `two-column-*` controls were produced after the parent successfully claimed the task at coordination `2a0d376388cacc83ceab1caf1f2152c195329964` and clarified the other same-number session in issue comment `6225016288`. All Python material remains finite evidence, contains no Lean theorem, and is excluded from Lean builds. Parent Agent #100 is the sole Git/issue publisher.

## Claimed-task two-column controls

The independent source-semantic audit is in `two-column-semantic-review.md`. `two_column_controls.py` fully enumerates the restricted admissible coefficient profiles of widths 2 through 10 described below, using one canonical ordinary integer per profile. The counts refer to actual realizable coefficient profiles, not all ordinary integer splits. Empty parameter cells are separately recorded in `two-column-summary.json` and never counted as examples.

| Condition | Width 2 | Width 3 | Widths 4–10 | Total |
| --- | ---: | ---: | ---: | ---: |
| Prefix `(16,0)` | 0 | 1 | 11,050 | 11,051 |
| Prefix `(16,1)` | 0 | 0 | 11,050 | 11,050 |
| Prefix `(16,16)` | 1 | 1 | 11,050 | 11,052 |
| Prefix `(16,17)` | 0 | 0 | 11,050 | 11,050 |
| Outer 7, second `0..8` | 1 | 5 | 99,450 | 99,456 |
| Outer 7, second `10..18` | 0 | 5 | 99,450 | 99,455 |
| **All profiles** | **2** | **12** | **243,100** | **243,114** |

All width, carry, prefix and outer-coefficient assertions passed, with 287,317 ordinary additions. `two_column_examples.py` preserves small-width actual witnesses and finite counterexamples to weakening the second-column bounds; those counterexamples are not advertised as kernel-checked results.

Reproduce from the repository root:

```sh
python proofs/contributions/agent-100/third-gate-boundary-20261016/controls/two_column_controls.py > proofs/contributions/agent-100/third-gate-boundary-20261016/controls/two-column-controls.log
python proofs/contributions/agent-100/third-gate-boundary-20261016/controls/two_column_examples.py > proofs/contributions/agent-100/third-gate-boundary-20261016/controls/two-column-examples.log
python proofs/contributions/agent-100/third-gate-boundary-20261016/controls/compress_trace.py > proofs/contributions/agent-100/third-gate-boundary-20261016/controls/two-column-compression.log
```

The published complete trace is `two-column-cases.jsonl.xz`. The original `two-column-cases.jsonl.gz` is retained in the execution workspace and its hash remains in the original summary. The XZ transcoder streams the exact original JSONL bytes without changing formatting, values or record order, then independently decompresses the XZ and verifies the complete decoded SHA-256. The original gzip is retained. Both decode to 48,028,259 bytes with SHA-256 `8fb2a448bb9f19905cecccb914a047d5fd114ea144fb0bfbbd51e7d6be5e1abc`. Exact stored sizes/hashes are in `two-column-xz.json` and `two-column-summary.json`. Publishing the smaller XZ together with the decoded hash preserves the complete diagnostic evidence.

## Original preclaim scout: scope and result

The original written argument is `renewal_pass/constructive/STATUS.md` section 4, Git blob `d684dc1865a3e59e1c699ad1ec28a4dbec0a74e2`. Its proposed target compares the actual component and whole pair-word iterates from `A0=component r 1 1 6` and `Q0=Phi1(A0)` at time six. The scout computes one canonical ordinary-integer realization of each of these profiles for each of the nine spacers `1,2,3,4,5,6,10,30,100`, using ordinary integer reverse-add. This makes 108 additions.

Every finite row passes the width and boundary checks. With `L=2r+6`, component widths are `L` at times zero through four and `L+1` at times five and six. Whole widths are `L+1` and then `L+2`. At time six the actual component outer coefficient is 14 and the whole outer coefficient is 15, so the index-zero difference `Q6-Phi1(A6)` is 1. Both sides have equal physical width. No infinite function tail is inspected.

For `r=1`, the first two coefficients at time five are `(7,8)` for the component and `(7,15)` for the whole. The other tested spacers give `(7,7)` and `(7,14)`. The shortest-spacer boundary therefore cannot be replaced by the generic positive-gap expression. The nine finite checks do not prove the all-spacer statement or the arbitrary-realization quantifiers.

## Original scout: reproduce

Run from the repository root with ordinary Python 3; no third-party package is required:

```sh
python proofs/contributions/agent-100/third-gate-boundary-20261016/controls/time6_scout.py > proofs/contributions/agent-100/third-gate-boundary-20261016/controls/time6-scout.log
```

The command writes `time6_scout.json`, `time6-summary.json`, and the redirected log. Assertions check the finite widths, both outer coefficients and their index-zero difference. It imports the sibling Group II controls implementation, verifies that dependency's exact SHA-256 `50e73312a3a89a8f90a7d8fc6a40b3280724c764c5e433a2a10734ead2f28f31`, and then uses its ordinary-integer trajectory routine. No Lean compilation is invoked.

The four original scout files were copied from `audit100/`. `original-copy-provenance.json` records their original hashes. The copied Python import path was made relative to the contribution directory, explicit PRECLAIM status and finite assertions/summary were added, and output files were regenerated. The underlying trajectories and row payloads are unchanged. `time6-scout.md` retains the original source analysis with a new status banner.

## Historical preclaim ownership snapshot and limits

`preclaim-ownership.json` records the first refresh at coordination `5020db13f2d5dc3bef8a8074248c9873e1404ec5` with 94 tasks and 220 issue comments. `preclaim-refresh.json` records the later head `c9ef8561d8ac236117102ddeccc758a541591543` with 97 tasks, plus all new issue messages through comment `6225005124` (234 comments). The three new task records cover Agent #105 affine dynamics, cross-width collisions and palindrome-image classification; none owns the specific time-six boundary.

Agent #2's claim `agent2-first-hit-eleven-20261016` (blob `a92dff56f3a9b7c14bed51fbea3ad1a7e44f2217`) owns first positive hit 11 for every canonical whole realization with `r>=5`, and its precise palindrome endpoint. Agent #8's common-overflow claim (current blob `ce464618aab654366db3b310aabc088b460863b6`) owns the general equal-width/equal-carry defect-transport theorem; its new first-hit-four endpoint claim (blob `4bf01f46e7875cd4f3f8f991a18f741c8cd3cb49`) concerns three other cores. These are complementary to the proposed all-`r>=1` paired time-six outer-boundary result, and their sources/ownership must be preserved.

**Potential scope collision:** another Agent #100 session `212248Z` announced in issue comment `6224990702` that it was scouting the third-gate boundary/finite realizability after PR #88. It had no published task claim in this inspected snapshot. Parent Agent #100 was immediately alerted. This is an overlapping intention and requires explicit issue coordination; the absence of a task record must not be described as absence of any competing interest. This folder itself makes no claim and does not authorize substantial formal proof work.

## Published-scope reconciliation

The later issue coordination established this session's time-six boundary claim at `2a0d376388cacc83ceab1caf1f2152c195329964`; session `212248Z` subsequently claimed the complementary second-column descent. The snapshot warning above is historical. All 28 precise Lean exports now have independent semantic review and a separate successful twelve-module clean build in `../verification/checkpoint01/`. The Python examples remain finite diagnostics.

The subsequent variable-p Group II overflow scout belongs to the separate claimed task `agent100-groupII-overflow-sharpness-20261016`, with its own branch and contribution directory. Its locally preserved files are excluded from this third-gate publication. The publication index below records only third-gate evidence; the full decoded JSONL hash fixes every diagnostic row.
