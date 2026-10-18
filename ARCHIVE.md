# Archive

On 17 October 2026 the repository was consolidated into the single branch `main` (see README).
Nothing was lost: every old branch tip, every pull request and the previous `main` are contained in the history of one of 60 tags `archive/2026-10-17/...` listed below. Tags whose commit was already inside another tag's history were removed as redundant.

## How to get old material

```bash
git fetch origin 'refs/tags/archive/2026-10-17/*:refs/tags/archive/2026-10-17/*'
git checkout archive/2026-10-17/main     # the old main (6ed031d), before consolidation
git fetch origin pull/135/head && git checkout FETCH_HEAD    # any pull request, by number (GitHub keeps these)
```

The old `main` is also the first parent of the consolidation commit, so `git log` and `git blame` still reach it. An old branch that is not in the tag list below is an ancestor of one that is; the table at the end says which.

## What moved out of `main`

- `proofs/` (archive copies, flattened `Name__<hash>.lean` copies, contributions, coordination, evidence, logs, review packets, base64 bundles, translations) — replaced by `lean/`, `RESULTS.md` and `lean/registry.json`.
- 39 GitHub Actions workflows for the old process — replaced by `.github/workflows/verify.yml`.
- `calculation/history/` (byte-distinct older copies of the engine files).

### Notable documents from the old `main`

Available under the tag `archive/2026-10-17/main`:

- `proofs/OPEN_PROBLEMS.md` — the four-question framing (orbit of 196 / Lychrel existence / supporting results / verification); summarized in README "Open problems".
- `proofs/FINDINGS.md`, `proofs/REPRODUCE.md`, `proofs/STATUS.md` — earlier findings, replay instructions and status notes.
- `proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/chat-6acee928/originals/` — written (prose) proofs, e.g. `p196_thirteen_prefix_theorem.md` (cited by the Core Lean docstrings), `p196_double_image_theorem.md` and `p196_uniform_five_layer_obstruction.md`.
- `proofs/english/` — the English translation layer of the old documents.

## Unregistered Lean drafts that are not on `main`

Every distinct Lean file from every branch and pull request was compiled on 17 October 2026 (Lean 4.19.0). Every draft file that proves at least one theorem statement found nowhere else is now on `main` (results about 196 in `lean/P196/<Result>/`, the rest in `lean/P196/Drafts/`). The files counted below are what is left: earlier versions, copies and attempts whose theorem statements all already appear on `main`, files that do not compile, and files using `sorry`, `native_decide` or custom axioms. "Compiles" counts files that built without errors and without `sorry`.

| Source directory | Lean files | compiles | theorems | Tag that contains it |
| --- | ---: | ---: | ---: | --- |
| `proofs/contributions/2026-10-15-scalar-finite-certificate-formal/generated` | 31 | 28 | 2691 | `archive/2026-10-17/main` |
| `proofs/contributions/agent-103/broader-return-formal` | 21 | 21 | 2676 | `archive/2026-10-17/main` |
| `proofs/contributions/agent-104/prefix620-kernel-20261016` | 369 | 3 | 593 | `archive/2026-10-17/main` |
| `proofs/contributions/agent-119/four-column-prefix` | 22 | 21 | 526 | `archive/2026-10-17/main` |
| `proofs/contributions/agent-104/seven-column-kernel` | 48 | 46 | 498 | `archive/2026-10-17/main` |
| `proofs/contributions/agent-108/window-weights-b31b8818` | 30 | 0 | 282 | `archive/2026-10-17/main` |
| `proofs/contributions/agent-7/odd-nooverflow-fibers-20261016` | 20 | 11 | 127 | `archive/2026-10-17/main` |
| `proofs/contributions/agent-103/residual-five-20261016` | 5 | 0 | 67 | `archive/2026-10-17/main` |
| `proofs/contributions/agent-122/finite-seed-countermodel` | 6 | 0 | 62 | `archive/2026-10-17/research/agent-119/s20261015T2005-eight-families` |
| `proofs/contributions/agent-3/prefix-contraction-20261016` | 5 | 1 | 54 | `archive/2026-10-17/research/agent-3/prefix-contraction-20261016-2232` |
| `proofs/contributions/agent-7/allbase-overflow-births-20261016` | 13 | 2 | 37 | `archive/2026-10-17/formalize/agent-52/general-base-zero-interval-20261016` |
| `proofs/contributions/agent-101/digit-split-multiplicity-20261016` | 6 | 2 | 31 | `archive/2026-10-17/main` |
| `proofs/contributions/agent-104/review-agent13-real-weights` | 5 | 1 | 30 | `archive/2026-10-17/main` |
| `proofs/contributions/agent-52/digit-sum-density-20261016` | 2 | 0 | 29 | `archive/2026-10-17/formalize/agent-52/digit-sum-density-20261016` |
| `proofs/contributions/agent-107/dfa-horn-closure-20261016` | 5 | 2 | 27 | `archive/2026-10-17/research/agent-1/agent104-monitor-verification-20261017T0307Z` |
| `proofs/contributions/agent-15/spectral-carry-charge-43cf6e114472` | 2 | 1 | 25 | `archive/2026-10-17/formalize/agent-15/spectral-carry-charge-43cf6e114472` |
| `proofs/contributions/agent-9/finite-ensemble-marker-count-20261016` | 4 | 2 | 24 | `archive/2026-10-17/main` |
| `proofs/contributions/agent-104/dfa-safety-monitor-20261016` | 1 | 0 | 23 | `archive/2026-10-17/research/agent-104/dfa-safety-monitor-20261016T2250Z` |
| `proofs/contributions/agent-103/residual-five-fibers-20261016` | 3 | 0 | 21 | `archive/2026-10-17/main` |
| `proofs/contributions/agent-109/boundary-kernel-recheck` | 6 | 6 | 18 | `archive/2026-10-17/main` |
| `proofs/contributions/agent-111/exact-length-residues` | 13 | 7 | 15 | `archive/2026-10-17/research/agent-119/s20261015T2005-eight-families` |
| `proofs/contributions/2026-10-15-agent8-complementary-bulk/SaturationPaths.lean` | 1 | 0 | 14 | `archive/2026-10-17/main` |
| `proofs/contributions/agent-102/affine-runs-20261016` | 14 | 13 | 14 | `archive/2026-10-17/main` |
| `proofs/contributions/agent-1/agent104-monitor-verification-20261017` | 2 | 0 | 14 | `archive/2026-10-17/research/agent-1/agent104-monitor-verification-20261017T0307Z` |
| `proofs/contributions/agent-103/residual-five-third-gate-20261016` | 4 | 0 | 14 | `archive/2026-10-17/research/agent-1/pr165-verification-20261017T0118Z` |
| `proofs/contributions/agent-103/residual-five-firsthit-two-20261016` | 3 | 0 | 14 | `archive/2026-10-17/research/agent-103/residual-five-firsthit-two-20261016T2200Z` |
| `proofs/contributions/agent-100/groupII-overflow-sharpness-20261016` | 3 | 1 | 12 | `archive/2026-10-17/main` |
| `proofs/contributions/agent-100/groupII-rebase-20261016` | 4 | 2 | 11 | `archive/2026-10-17/main` |
| `proofs/contributions/agent-105/actual-high-return` | 5 | 4 | 10 | `archive/2026-10-17/main` |
| `proofs/contributions/agent-116/integration` | 1 | 1 | 10 | `archive/2026-10-17/research/agent-115/s20261015-review-broader` |
| `proofs/contributions/agent-1/groupIII-handoff-20261016` | 4 | 4 | 10 | `archive/2026-10-17/main` |
| `proofs/contributions/agent-106/run-births` | 4 | 3 | 8 | `archive/2026-10-17/main` |
| `proofs/contributions/agent-116/certificate-exterior` | 2 | 2 | 8 | `archive/2026-10-17/research/agent-115/s20261015-review-broader` |
| `proofs/contributions/agent-121/review-agent116-checkpoint01` | 7 | 1 | 7 | `archive/2026-10-17/research/agent-119/s20261015T2005-eight-families` |
| `proofs/contributions/2026-10-15-scalar-period-composition/ScalarBound.lean` | 1 | 1 | 7 | `archive/2026-10-17/main` |
| `proofs/contributions/agent-1/pr165-verification-20261017` | 1 | 0 | 7 | `archive/2026-10-17/research/agent-1/pr165-verification-20261017T0118Z` |
| `proofs/contributions/agent-105/ceil-half-suffix-8f1107db019a` | 1 | 0 | 6 | `archive/2026-10-17/research/agent-1/ceilhalf-verification-20261017T0210Z` |
| `proofs/contributions/agent-111/growing-tenpower-suffix-20261016` | 2 | 0 | 6 | `archive/2026-10-17/research/agent-1/ceilhalf-verification-20261017T0210Z` |
| `proofs/contributions/agent-105/inverse-boundaries-9df76b-20261016` | 1 | 0 | 6 | `archive/2026-10-17/main` |
| `proofs/contributions/agent-106/congruence-carry-budget-20261016T2131Z` | 3 | 2 | 6 | `archive/2026-10-17/main` |
| `proofs/contributions/agent-105/all-predecessors-9df76b-20261016` | 3 | 2 | 6 | `archive/2026-10-17/research/agent-1/backward-layers-verification-20261017T0142Z` |
| `proofs/contributions/agent-1/ceilhalf-verification-20261017` | 2 | 1 | 6 | `archive/2026-10-17/research/agent-1/ceilhalf-verification-20261017T0210Z` |
| `proofs/contributions/agent-108/modular-autonomy` | 12 | 8 | 5 | `archive/2026-10-17/main` |
| `proofs/contributions/2026-10-15-scalar-finite-certificate-formal/ScalarHierarchy.lean` | 1 | 1 | 5 | `archive/2026-10-17/main` |
| `proofs/contributions/agent-111/bounded-variable-modulus-20261016` | 1 | 0 | 5 | `archive/2026-10-17/main` |
| `proofs/contributions/2026-10-15-scalar-finite-certificate-formal/ScalarHierarchyData.lean` | 1 | 1 | 4 | `archive/2026-10-17/main` |
| `proofs/contributions/agent-105/numeric-decoder-9df76b-20261016` | 1 | 0 | 4 | `archive/2026-10-17/research/agent-1/backward-layers-verification-20261017T0142Z` |
| `proofs/contributions/agent-101/two-history-realization-count-20261016` | 1 | 0 | 4 | `archive/2026-10-17/research/agent-101/two-history-realizations-20261016T2238Z` |
| `proofs/contributions/agent-17/m99-a07-uniform-finite-seed` | 1 | 1 | 3 | `archive/2026-10-17/main` |
| `proofs/contributions/agent-315/temporal-column-11-99` | 1 | 1 | 3 | `archive/2026-10-17/main` |
| `proofs/contributions/agent-1/backward-layers-verification-20261017` | 1 | 0 | 3 | `archive/2026-10-17/research/agent-1/backward-layers-verification-20261017T0142Z` |
| `proofs/contributions/agent-16/m99-a06` | 1 | 0 | 3 | `archive/2026-10-17/research/agent-16/m99-a06-20261015` |
| `proofs/contributions/agent-217/uniformity` | 1 | 0 | 3 | `archive/2026-10-17/research/agent-217/s20261015-uniformity` |
| `proofs/contributions/2026-10-15-scalar-finite-certificate-formal/RangeChecks.lean` | 1 | 1 | 2 | `archive/2026-10-17/main` |
| `proofs/contributions/agent-15/sixphase-temporal-profile` | 1 | 0 | 2 | `archive/2026-10-17/research/agent-15/s20261015T2014` |
| `proofs/contributions/agent-124/prefix-five-six` | 1 | 1 | 1 | `archive/2026-10-17/research/agent-124/s20261015T1600` |

## Drafts left out because they are too heavy to build

These 5 draft files compile and prove statements found nowhere else, but they are large `decide` certificates (or depend on one) that need 20-40 GB of memory and up to an hour per file, beyond the build budget in AGENTS.md rule 8 (an ordinary 16 GB machine, which is also what GitHub Actions has). They stay in the archive tags; to bring one back, split or rewrite its certificate so each file fits the budget.

| Original path | Tag that contains it |
| --- | --- |
| `proofs/contributions/2026-10-15-scalar-hierarchy-review/source_snapshots/ScalarHierarchy.lean` | `archive/2026-10-17/research/agent-1/ceilhalf-verification-20261017T0210Z` |
| `proofs/contributions/2026-10-15-scalar-period-composition/ScalarBound.lean` | `archive/2026-10-17/research/agent-1/ceilhalf-verification-20261017T0210Z` |
| `proofs/contributions/agent-103/broader-return-formal/BroaderScalarBound.lean` | `archive/2026-10-17/research/agent-1/ceilhalf-verification-20261017T0210Z` |
| `proofs/contributions/agent-103/broader-return-formal/stage2/BroaderBound.lean` | `archive/2026-10-17/research/agent-1/ceilhalf-verification-20261017T0210Z` |
| `proofs/contributions/agent-103/broader-return-formal/stage2/generated/BroaderHierarchy.lean` | `archive/2026-10-17/research/agent-1/ceilhalf-verification-20261017T0210Z` |

## Tags

60 tags:

| Tag | Commit date |
| --- | --- |
| `archive/2026-10-17/main` | 2026-10-17 11:44 |
| `archive/2026-10-17/docs/agent-61/status-reproduction-20261016` | 2026-10-16 22:24 |
| `archive/2026-10-17/docs/agent-62/residual-five-guide-20261016-bd61bb` | 2026-10-16 17:34 |
| `archive/2026-10-17/formalize/agent-14/carryfree-residue-saturation-20261016` | 2026-10-16 16:52 |
| `archive/2026-10-17/formalize/agent-15/spectral-carry-charge-43cf6e114472` | 2026-10-16 16:40 |
| `archive/2026-10-17/formalize/agent-15/spectral-carry-support-43cf6e114472` | 2026-10-16 17:04 |
| `archive/2026-10-17/formalize/agent-22/m99-a02-guard-review` | 2026-10-15 20:39 |
| `archive/2026-10-17/formalize/agent-4/general-base-normalization-20261016` | 2026-10-16 11:06 |
| `archive/2026-10-17/formalize/agent-51/spectral-reciprocal-moment-20261016` | 2026-10-16 16:58 |
| `archive/2026-10-17/formalize/agent-52/digit-sum-density-20261016` | 2026-10-16 16:52 |
| `archive/2026-10-17/formalize/agent-52/general-base-zero-interval-20261016` | 2026-10-16 15:21 |
| `archive/2026-10-17/formalize/agent-53/20261016-c04cf11f6ff8` | 2026-10-16 16:46 |
| `archive/2026-10-17/p196/coordination` | 2026-10-17 12:03 |
| `archive/2026-10-17/research/agent-1/agent104-monitor-verification-20261017T0307Z` | 2026-10-17 03:10 |
| `archive/2026-10-17/research/agent-1/backward-layers-verification-20261017T0142Z` | 2026-10-17 01:46 |
| `archive/2026-10-17/research/agent-1/ceilhalf-verification-20261017T0210Z` | 2026-10-17 02:31 |
| `archive/2026-10-17/research/agent-1/periodic-guarded-path-20261017T0017Z` | 2026-10-17 01:00 |
| `archive/2026-10-17/research/agent-1/periodic-nine-clock-strip-20261017T0250Z` | 2026-10-17 03:03 |
| `archive/2026-10-17/research/agent-1/periodic-nine-control-20261017T0219Z` | 2026-10-16 23:18 |
| `archive/2026-10-17/research/agent-1/periodic-outer-catalog-20261016T2252Z` | 2026-10-16 23:35 |
| `archive/2026-10-17/research/agent-1/periodic-prefix-saturation-20261016T2358Z` | 2026-10-17 00:21 |
| `archive/2026-10-17/research/agent-1/periodic-reduced-core-20261017T0135Z` | 2026-10-17 01:57 |
| `archive/2026-10-17/research/agent-1/periodic-return-upper-gap-20261017T0020Z` | 2026-10-17 01:06 |
| `archive/2026-10-17/research/agent-1/periodic-width-projection-20261016T2304Z` | 2026-10-16 23:44 |
| `archive/2026-10-17/research/agent-1/pr104-review-20261016T2205Z` | 2026-10-16 22:17 |
| `archive/2026-10-17/research/agent-1/pr165-verification-20261017T0118Z` | 2026-10-17 01:24 |
| `archive/2026-10-17/research/agent-1/zero-width-loop-20261016T2359Z` | 2026-10-17 00:14 |
| `archive/2026-10-17/research/agent-100/third-gate-descent-212248Z` | 2026-10-16 14:51 |
| `archive/2026-10-17/research/agent-101/all-width-inverse-maximum-20261016T2204Z` | 2026-10-16 15:46 |
| `archive/2026-10-17/research/agent-101/two-history-realizations-20261016T2238Z` | 2026-10-16 20:46 |
| `archive/2026-10-17/research/agent-102/affine-parameter-intervals-20261016T2215Z` | 2026-10-16 15:41 |
| `archive/2026-10-17/research/agent-103/residual-five-firsthit-two-20261016T2200Z` | 2026-10-16 15:36 |
| `archive/2026-10-17/research/agent-104/dfa-safety-monitor-20261016T2250Z` | 2026-10-16 20:21 |
| `archive/2026-10-17/research/agent-104/review-pr100-cylinder-20261016T2227Z` | 2026-10-16 14:58 |
| `archive/2026-10-17/research/agent-107/dfa-horn-closure-20261016T2203Z` | 2026-10-16 21:37 |
| `archive/2026-10-17/research/agent-110/two-step-return-20261016T2123Z` | 2026-10-16 15:00 |
| `archive/2026-10-17/research/agent-113/descending-prefix-maximality-20261016T212415Z` | 2026-10-17 10:56 |
| `archive/2026-10-17/research/agent-113/s20261015` | 2026-10-15 13:34 |
| `archive/2026-10-17/research/agent-114/core17-r3-firsthit-s2124Z` | 2026-10-16 14:58 |
| `archive/2026-10-17/research/agent-115/rho-cycle-balance-20261016T2130Z` | 2026-10-16 14:58 |
| `archive/2026-10-17/research/agent-115/s20261015-review-broader` | 2026-10-15 12:55 |
| `archive/2026-10-17/research/agent-117/k7-four-digit-2641-20261016T2129Z` | 2026-10-16 14:58 |
| `archive/2026-10-17/research/agent-117/s20261015` | 2026-10-15 12:48 |
| `archive/2026-10-17/research/agent-118/k7-double-5523-5524-20261016T2136Z` | 2026-10-16 14:58 |
| `archive/2026-10-17/research/agent-118/s20261015T1548` | 2026-10-15 13:30 |
| `archive/2026-10-17/research/agent-119/s20261015T2005-eight-families` | 2026-10-15 13:26 |
| `archive/2026-10-17/research/agent-124/s20261015T1600` | 2026-10-15 12:56 |
| `archive/2026-10-17/research/agent-14/ordinary-exterior-six-twelve-bridge-20261015` | 2026-10-15 20:17 |
| `archive/2026-10-17/research/agent-15/s20261015T2014` | 2026-10-15 20:16 |
| `archive/2026-10-17/research/agent-16/m99-a06-20261015` | 2026-10-15 20:18 |
| `archive/2026-10-17/research/agent-18/20261015-finite-seed` | 2026-10-15 20:18 |
| `archive/2026-10-17/research/agent-211/m99-b211-finite-realizability-audit` | 2026-10-15 20:28 |
| `archive/2026-10-17/research/agent-217/s20261015-uniformity` | 2026-10-15 20:37 |
| `archive/2026-10-17/research/agent-3/prefix-contraction-20261016-2232` | 2026-10-17 03:20 |
| `archive/2026-10-17/research/agent-311/m99-c311-20261015` | 2026-10-15 20:49 |
| `archive/2026-10-17/research/agent-313/m99-c313-20261015` | 2026-10-15 20:51 |
| `archive/2026-10-17/research/agent-314/ordinary-exterior-audit` | 2026-10-15 20:51 |
| `archive/2026-10-17/research/agent-7/run-renewal-20261016T2225Z` | 2026-10-16 15:33 |
| `archive/2026-10-17/research/agent-9/fibonacci-asymptotic-rate-20261017T0313Z` | 2026-10-17 03:23 |
| `archive/2026-10-17/review/agent-105/pr112-8f1107db019a` | 2026-10-16 18:35 |

## Where each old branch went

| Old branch | Contained in tag |
| --- | --- |
| `archive/agent-105/ceil-half-suffix-b622465107d1` | `archive/2026-10-17/research/agent-1/ceilhalf-verification-20261017T0210Z` |
| `deep-clean/automation-20261017` | `archive/2026-10-17/main` |
| `deep-clean/build-coverage-20261017` | `archive/2026-10-17/main` |
| `docs/agent-60/open-obligations-20261016` | `archive/2026-10-17/main` |
| `docs/agent-61/status-reproduction-20261016` | `archive/2026-10-17/docs/agent-61/status-reproduction-20261016` |
| `docs/agent-62/residual-five-guide-20261016-bd61bb` | `archive/2026-10-17/docs/agent-62/residual-five-guide-20261016-bd61bb` |
| `docs/agent-63/report-index-links-20261016` | `archive/2026-10-17/main` |
| `docs/agent-64/finite-horizon-count-20261016-6da1ed9b` | `archive/2026-10-17/main` |
| `docs/agent-65/source-map-guide-20261016-dbfcd4` | `archive/2026-10-17/main` |
| `docs/agent-66/affine-status-20261016-f05b879a` | `archive/2026-10-17/main` |
| `formalize/agent-14/carryfree-residue-saturation-20261016` | `archive/2026-10-17/formalize/agent-14/carryfree-residue-saturation-20261016` |
| `formalize/agent-14/spectral-injectivity-20261016` | `archive/2026-10-17/main` |
| `formalize/agent-15/spectral-carry-charge-43cf6e114472` | `archive/2026-10-17/formalize/agent-15/spectral-carry-charge-43cf6e114472` |
| `formalize/agent-15/spectral-carry-support-43cf6e114472` | `archive/2026-10-17/formalize/agent-15/spectral-carry-support-43cf6e114472` |
| `formalize/agent-21/m99-a01-realizability-interface-20261015` | `archive/2026-10-17/main` |
| `formalize/agent-22/m99-a02-guard-review` | `archive/2026-10-17/formalize/agent-22/m99-a02-guard-review` |
| `formalize/agent-221/finite-seed-bridge-20261015` | `archive/2026-10-17/main` |
| `formalize/agent-222/m99-b222-20261015` | `archive/2026-10-17/main` |
| `formalize/agent-23/m99-a03-20261015` | `archive/2026-10-17/main` |
| `formalize/agent-4/general-base-normalization-20261016` | `archive/2026-10-17/formalize/agent-4/general-base-normalization-20261016` |
| `formalize/agent-51/spectral-overflow-saturation-20261016` | `archive/2026-10-17/formalize/agent-51/spectral-reciprocal-moment-20261016` |
| `formalize/agent-51/spectral-reciprocal-moment-20261016` | `archive/2026-10-17/formalize/agent-51/spectral-reciprocal-moment-20261016` |
| `formalize/agent-52/digit-sum-density-20261016` | `archive/2026-10-17/formalize/agent-52/digit-sum-density-20261016` |
| `formalize/agent-52/general-base-zero-interval-20261016` | `archive/2026-10-17/formalize/agent-52/general-base-zero-interval-20261016` |
| `formalize/agent-53/20261016-c04cf11f6ff8` | `archive/2026-10-17/formalize/agent-53/20261016-c04cf11f6ff8` |
| `formalize/agent-8/common-overflow-defect-20261016` | `archive/2026-10-17/main` |
| `formalize/agent-8/firsthit-four-endpoints-20261016` | `archive/2026-10-17/main` |
| `formalize/agent-9/digit-sum-interval-counts-20261016` | `archive/2026-10-17/main` |
| `formalize/agent-9/escape-factorial-bound-20261016` | `archive/2026-10-17/main` |
| `formalize/agent-9/finite-ensemble-marker-count-20261016` | `archive/2026-10-17/main` |
| `formalize/agent-9/marker-palindrome-intersection-20261016` | `archive/2026-10-17/main` |
| `formalize/agent-9/nooverflow-horizon-20261016` | `archive/2026-10-17/main` |
| `formalize/agent-9/one-step-digit-sum-collapse-20261016` | `archive/2026-10-17/main` |
| `main` | `archive/2026-10-17/main` |
| `p196/coordination` | `archive/2026-10-17/p196/coordination` |
| `research/agent-1/agent104-monitor-verification-20261017T0307Z` | `archive/2026-10-17/research/agent-1/agent104-monitor-verification-20261017T0307Z` |
| `research/agent-1/backward-layers-verification-20261017T0142Z` | `archive/2026-10-17/research/agent-1/backward-layers-verification-20261017T0142Z` |
| `research/agent-1/ceilhalf-verification-20261017T0210Z` | `archive/2026-10-17/research/agent-1/ceilhalf-verification-20261017T0210Z` |
| `research/agent-1/groupIII-delayed-overlap-20261016T2120Z` | `archive/2026-10-17/main` |
| `research/agent-1/groupIII-handoff-20261016T2132Z` | `archive/2026-10-17/main` |
| `research/agent-1/normalization-and-groupIII-20261016T2110Z` | `archive/2026-10-17/main` |
| `research/agent-1/periodic-block-strip-20261016T2146Z` | `archive/2026-10-17/main` |
| `research/agent-1/periodic-cycle-adapter-20261017T0100Z` | `archive/2026-10-17/research/agent-1/periodic-reduced-core-20261017T0135Z` |
| `research/agent-1/periodic-eighteen-return-20261017T0123Z` | `archive/2026-10-17/research/agent-1/periodic-reduced-core-20261017T0135Z` |
| `research/agent-1/periodic-guard-20261016T2122Z` | `archive/2026-10-17/main` |
| `research/agent-1/periodic-guarded-path-20261017T0017Z` | `archive/2026-10-17/research/agent-1/periodic-guarded-path-20261017T0017Z` |
| `research/agent-1/periodic-nine-center-20261017T0209Z` | `archive/2026-10-17/research/agent-1/periodic-nine-clock-strip-20261017T0250Z` |
| `research/agent-1/periodic-nine-clock-strip-20261017T0250Z` | `archive/2026-10-17/research/agent-1/periodic-nine-clock-strip-20261017T0250Z` |
| `research/agent-1/periodic-nine-control-20261017T0219Z` | `archive/2026-10-17/research/agent-1/periodic-nine-control-20261017T0219Z` |
| `research/agent-1/periodic-nine-cycle-20261017T0156Z` | `archive/2026-10-17/research/agent-1/periodic-nine-control-20261017T0219Z` |
| `research/agent-1/periodic-nine-excursion-20261017T0240Z` | `archive/2026-10-17/research/agent-1/periodic-nine-clock-strip-20261017T0250Z` |
| `research/agent-1/periodic-outer-catalog-20261016T2252Z` | `archive/2026-10-17/research/agent-1/periodic-outer-catalog-20261016T2252Z` |
| `research/agent-1/periodic-phase-catalog-20261016T2247Z` | `archive/2026-10-17/main` |
| `research/agent-1/periodic-prefix-saturation-20261016T2358Z` | `archive/2026-10-17/research/agent-1/periodic-prefix-saturation-20261016T2358Z` |
| `research/agent-1/periodic-reduced-core-20261017T0135Z` | `archive/2026-10-17/research/agent-1/periodic-reduced-core-20261017T0135Z` |
| `research/agent-1/periodic-return-clock-20261016T2345Z` | `archive/2026-10-17/research/agent-1/periodic-return-upper-gap-20261017T0020Z` |
| `research/agent-1/periodic-return-core-20261016T2335Z` | `archive/2026-10-17/research/agent-1/periodic-guarded-path-20261017T0017Z` |
| `research/agent-1/periodic-return-upper-gap-20261017T0020Z` | `archive/2026-10-17/research/agent-1/periodic-return-upper-gap-20261017T0020Z` |
| `research/agent-1/periodic-safety-20261016T2205Z` | `archive/2026-10-17/main` |
| `research/agent-1/periodic-validity-20261016T2153Z` | `archive/2026-10-17/main` |
| `research/agent-1/periodic-width-projection-20261016T2304Z` | `archive/2026-10-17/research/agent-1/periodic-width-projection-20261016T2304Z` |
| `research/agent-1/periodic-zero-cycle-20261016T2221Z` | `archive/2026-10-17/main` |
| `research/agent-1/periodic-zero-escape-20261016T2238Z` | `archive/2026-10-17/main` |
| `research/agent-1/pr104-review-20261016T2205Z` | `archive/2026-10-17/research/agent-1/pr104-review-20261016T2205Z` |
| `research/agent-1/pr165-verification-20261017T0118Z` | `archive/2026-10-17/research/agent-1/pr165-verification-20261017T0118Z` |
| `research/agent-1/zero-width-loop-20261016T2359Z` | `archive/2026-10-17/research/agent-1/zero-width-loop-20261016T2359Z` |
| `research/agent-100/groupII-overflow-sharpness-20261016T2144Z` | `archive/2026-10-17/main` |
| `research/agent-100/groupII-overlap-20261016T2052Z` | `archive/2026-10-17/main` |
| `research/agent-100/groupII-rebase-20261016T2212Z` | `archive/2026-10-17/main` |
| `research/agent-100/groupII-third-output-20261016T2239Z` | `archive/2026-10-17/main` |
| `research/agent-100/third-gate-boundary-20261016T2126Z` | `archive/2026-10-17/main` |
| `research/agent-100/third-gate-descent-212248Z` | `archive/2026-10-17/research/agent-100/third-gate-descent-212248Z` |
| `research/agent-101/all-width-inverse-maximum-20261016T2204Z` | `archive/2026-10-17/research/agent-101/all-width-inverse-maximum-20261016T2204Z` |
| `research/agent-101/digit-split-multiplicity-20261016T2103Z` | `archive/2026-10-17/main` |
| `research/agent-101/nonpalindromic-protected-fibers-20261016T2123Z` | `archive/2026-10-17/main` |
| `research/agent-101/two-history-realizations-20261016T2238Z` | `archive/2026-10-17/research/agent-101/two-history-realizations-20261016T2238Z` |
| `research/agent-102/affine-parameter-intervals-20261016T2215Z` | `archive/2026-10-17/research/agent-102/affine-parameter-intervals-20261016T2215Z` |
| `research/agent-102/affine-runs-20261016T2124Z` | `archive/2026-10-17/main` |
| `research/agent-102/all-parameter-decisions-20261016T2150Z` | `archive/2026-10-17/main` |
| `research/agent-103/residual-five-20261016T2118Z` | `archive/2026-10-17/main` |
| `research/agent-103/residual-five-fibers-20261016T2130Z` | `archive/2026-10-17/main` |
| `research/agent-103/residual-five-firsthit-two-20261016T2200Z` | `archive/2026-10-17/research/agent-103/residual-five-firsthit-two-20261016T2200Z` |
| `research/agent-103/residual-five-predecessor-filter-count-20261016T0025Z` | `archive/2026-10-17/research/agent-1/pr165-verification-20261017T0118Z` |
| `research/agent-103/residual-five-third-gate-20261016T2230Z` | `archive/2026-10-17/research/agent-1/pr165-verification-20261017T0118Z` |
| `research/agent-104/620-depth12-witness-20261016T2143Z` | `archive/2026-10-17/main` |
| `research/agent-104/620-kernel-20261016T2122Z` | `archive/2026-10-17/main` |
| `research/agent-104/dfa-safety-monitor-20261016T2250Z` | `archive/2026-10-17/research/agent-104/dfa-safety-monitor-20261016T2250Z` |
| `research/agent-104/exact-zero-gap-20261016T2126Z` | `archive/2026-10-17/main` |
| `research/agent-104/review-pr100-cylinder-20261016T2227Z` | `archive/2026-10-17/research/agent-104/review-pr100-cylinder-20261016T2227Z` |
| `research/agent-105/8f1107db019a-affine-dynamics` | `archive/2026-10-17/main` |
| `research/agent-105/all-predecessors-9df76b-20261016` | `archive/2026-10-17/research/agent-1/backward-layers-verification-20261017T0142Z` |
| `research/agent-105/backward-layers-9df76b-20261016` | `archive/2026-10-17/research/agent-1/backward-layers-verification-20261017T0142Z` |
| `research/agent-105/ceil-half-suffix-8f1107db019a` | `archive/2026-10-17/research/agent-1/ceilhalf-verification-20261017T0210Z` |
| `research/agent-105/cross-width-palindrome-9df76b-20261016` | `archive/2026-10-17/main` |
| `research/agent-105/numeric-decoder-9df76b-20261016` | `archive/2026-10-17/main` |
| `research/agent-106/congruence-carry-budget-20261016T2131Z` | `archive/2026-10-17/main` |
| `research/agent-106/congruence-finite-path-20261016T2149Z` | `archive/2026-10-17/main` |
| `research/agent-107/dfa-horn-closure-20261016T2203Z` | `archive/2026-10-17/research/agent-107/dfa-horn-closure-20261016T2203Z` |
| `research/agent-107/folded-transducer-20261016T2130Z` | `archive/2026-10-17/main` |
| `research/agent-108/matrix-weights-b31b8818-20261016` | `archive/2026-10-17/main` |
| `research/agent-108/window-weights-b31b8818-20261016` | `archive/2026-10-17/main` |
| `research/agent-109/s20261015` | `archive/2026-10-17/main` |
| `research/agent-11/m99-a01-20261015` | `archive/2026-10-17/main` |
| `research/agent-110/two-step-return-20261016T2123Z` | `archive/2026-10-17/research/agent-110/two-step-return-20261016T2123Z` |
| `research/agent-111/bounded-variable-modulus-20261016T2130Z` | `archive/2026-10-17/main` |
| `research/agent-111/growing-composite-modulus-20261017T0210Z` | `archive/2026-10-17/main` |
| `research/agent-111/growing-tenpower-suffix-20261016T2137Z` | `archive/2026-10-17/review/agent-105/pr112-8f1107db019a` |
| `research/agent-112/cylinder-image-20261016T2130Z` | `archive/2026-10-17/research/agent-104/review-pr100-cylinder-20261016T2227Z` |
| `research/agent-113/descending-prefix-maximality-20261016T212415Z` | `archive/2026-10-17/research/agent-113/descending-prefix-maximality-20261016T212415Z` |
| `research/agent-113/s20261015` | `archive/2026-10-17/research/agent-113/s20261015` |
| `research/agent-114/core17-r3-firsthit-s2124Z` | `archive/2026-10-17/research/agent-114/core17-r3-firsthit-s2124Z` |
| `research/agent-114/short-r-firsthit-20261016T2126Z` | `archive/2026-10-17/main` |
| `research/agent-115/rho-cycle-balance-20261016T2130Z` | `archive/2026-10-17/research/agent-115/rho-cycle-balance-20261016T2130Z` |
| `research/agent-115/s20261015-review-broader` | `archive/2026-10-17/research/agent-115/s20261015-review-broader` |
| `research/agent-117/k7-four-digit-2641-20261016T2129Z` | `archive/2026-10-17/research/agent-117/k7-four-digit-2641-20261016T2129Z` |
| `research/agent-117/k8-2641-depth5-20261016T2200Z` | `archive/2026-10-17/main` |
| `research/agent-117/s20261015` | `archive/2026-10-17/research/agent-117/s20261015` |
| `research/agent-118/k7-double-5523-5524-20261016T2136Z` | `archive/2026-10-17/research/agent-118/k7-double-5523-5524-20261016T2136Z` |
| `research/agent-118/s20261015T1548` | `archive/2026-10-17/research/agent-118/s20261015T1548` |
| `research/agent-119/s20261015T1555` | `archive/2026-10-17/main` |
| `research/agent-119/s20261015T2005-eight-families` | `archive/2026-10-17/research/agent-119/s20261015T2005-eight-families` |
| `research/agent-12/m99-a02-20261015` | `archive/2026-10-17/main` |
| `research/agent-120/s20261015T1625` | `archive/2026-10-17/main` |
| `research/agent-124/s20261015T1600` | `archive/2026-10-17/research/agent-124/s20261015T1600` |
| `research/agent-13/m99-a03-20261015` | `archive/2026-10-17/main` |
| `research/agent-14/ordinary-exterior-six-twelve-bridge-20261015` | `archive/2026-10-17/research/agent-14/ordinary-exterior-six-twelve-bridge-20261015` |
| `research/agent-15/s20261015T2014` | `archive/2026-10-17/research/agent-15/s20261015T2014` |
| `research/agent-16/m99-a06-20261015` | `archive/2026-10-17/research/agent-16/m99-a06-20261015` |
| `research/agent-17/m99-a07-20261015` | `archive/2026-10-17/main` |
| `research/agent-18/20261015-finite-seed` | `archive/2026-10-17/research/agent-18/20261015-finite-seed` |
| `research/agent-2/first-hit-eleven-20261016T2100Z` | `archive/2026-10-17/main` |
| `research/agent-2/overflow-fibers-20261016T2040Z` | `archive/2026-10-17/main` |
| `research/agent-211/m99-b211-finite-realizability-audit` | `archive/2026-10-17/research/agent-211/m99-b211-finite-realizability-audit` |
| `research/agent-211/m99-b211-finite-realizability-audit-clean` | `archive/2026-10-17/main` |
| `research/agent-211/review-agent11-finite-scan` | `archive/2026-10-17/main` |
| `research/agent-211/two-phase-a3-extension` | `archive/2026-10-17/main` |
| `research/agent-211/two-phase-b3-extension` | `archive/2026-10-17/main` |
| `research/agent-211/two-phase-c-extension` | `archive/2026-10-17/main` |
| `research/agent-211/two-phase-c4-extension` | `archive/2026-10-17/main` |
| `research/agent-212/m99-b212-20261015` | `archive/2026-10-17/main` |
| `research/agent-213/20261015-gap` | `archive/2026-10-17/main` |
| `research/agent-215/20261015-saturated8` | `archive/2026-10-17/main` |
| `research/agent-216/s20261015-general-nat-bridge` | `archive/2026-10-17/main` |
| `research/agent-216/s20261015-mod22` | `archive/2026-10-17/main` |
| `research/agent-216/s20261015-residue-filter` | `archive/2026-10-17/main` |
| `research/agent-217/s20261015-uniformity` | `archive/2026-10-17/research/agent-217/s20261015-uniformity` |
| `research/agent-3/finite-horizon-20261016-2054` | `archive/2026-10-17/main` |
| `research/agent-3/prefix-contraction-20261016-2232` | `archive/2026-10-17/research/agent-3/prefix-contraction-20261016-2232` |
| `research/agent-3/three-layer-prefix-20261016-2200` | `archive/2026-10-17/main` |
| `research/agent-3/two-history-20261016-2105` | `archive/2026-10-17/main` |
| `research/agent-311/m99-c311-20261015` | `archive/2026-10-17/research/agent-311/m99-c311-20261015` |
| `research/agent-312/m99-c312-block-guard-20261015` | `archive/2026-10-17/main` |
| `research/agent-313/m99-c313-20261015` | `archive/2026-10-17/research/agent-313/m99-c313-20261015` |
| `research/agent-314/ordinary-exterior-audit` | `archive/2026-10-17/research/agent-314/ordinary-exterior-audit` |
| `research/agent-315/s20261015-temporal-columns` | `archive/2026-10-17/main` |
| `research/agent-317/m99-c317-uniformity-20261015` | `archive/2026-10-17/main` |
| `research/agent-318/m99-c318-backward-return-20261015` | `archive/2026-10-17/main` |
| `research/agent-4/normalizer-support-20261016-2057` | `archive/2026-10-17/main` |
| `research/agent-5/absorption-evidence-20261016T2122Z` | `archive/2026-10-17/main` |
| `research/agent-5/digit-streams-20261016T2108Z` | `archive/2026-10-17/main` |
| `research/agent-5/even-base-repair-20261016T2055Z` | `archive/2026-10-17/main` |
| `research/agent-5/ordinary-stream-prefix-20261016T2140Z` | `archive/2026-10-17/main` |
| `research/agent-5/stream-agreement-window-20261016T2205Z` | `archive/2026-10-17/main` |
| `research/agent-6/certificate-coordinate-audit-20261016` | `archive/2026-10-17/main` |
| `research/agent-6/exterior-coordinate-dynamics-20261016` | `archive/2026-10-17/main` |
| `research/agent-6/normalized-carry-accounting-20261016` | `archive/2026-10-17/main` |
| `research/agent-7/base-overflow-20261016T2137Z` | `archive/2026-10-17/formalize/agent-52/general-base-zero-interval-20261016` |
| `research/agent-7/odd-fibers-20261016T2100Z` | `archive/2026-10-17/main` |
| `research/agent-7/run-renewal-20261016T2225Z` | `archive/2026-10-17/research/agent-7/run-renewal-20261016T2225Z` |
| `research/agent-9/fibonacci-asymptotic-rate-20261017T0313Z` | `archive/2026-10-17/research/agent-9/fibonacci-asymptotic-rate-20261017T0313Z` |
| `review/agent-105/pr112-8f1107db019a` | `archive/2026-10-17/review/agent-105/pr112-8f1107db019a` |
