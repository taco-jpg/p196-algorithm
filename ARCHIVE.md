# Archive

On 17 October 2026 the repository was consolidated into the single branch `main` (see README).
Nothing was deleted from Git: every branch tip that existed at that moment, and the previous `main`, is kept as a tag.

## How to get old material

```bash
git fetch origin 'refs/tags/archive/2026-10-17/*:refs/tags/archive/2026-10-17/*'
git checkout archive/2026-10-17/main            # the old main (6ed031d), before consolidation
git checkout archive/2026-10-17/research/agent-118/s20261015T1548   # any old branch, same name
```

The old `main` also remains the first parent of the consolidation commit, so `git log` and `git blame` still reach it.

## What moved out of `main`

- `proofs/` (archive copies, flattened `Name__<hash>.lean` copies, contributions, coordination, evidence, logs, review packets, base64 bundles, translations) — replaced by `lean/`, `RESULTS.md` and `lean/registry.json`.
- 39 GitHub Actions workflows for the old process — replaced by `.github/workflows/verify.yml`.
- `calculation/history/` (byte-distinct older copies of the engine files).

### Notable documents from the old `main`

Still available under the tag `archive/2026-10-17/main`:

- `proofs/OPEN_PROBLEMS.md` — the four-question framing (orbit of 196 / Lychrel existence / supporting results / verification); summarized in README "Open problems".
- `proofs/FINDINGS.md`, `proofs/REPRODUCE.md`, `proofs/STATUS.md` — earlier findings, replay instructions and status notes.
- `proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/chat-6acee928/originals/` — written (prose) proofs, e.g. `p196_thirteen_prefix_theorem.md` (cited by the Core Lean docstrings) and `p196_double_image_theorem.md`.
- `proofs/english/` — the English translation layer of the old documents.

## Unregistered Lean work (not on `main`)

These developments were never registered as results, so they are not on `main`. Some may contain real progress; to bring one back, check it out from its tag, make it build, and register it as described in `AGENTS.md`. Some directories below share a name with a registered result: their files are other (older or newer) versions of it.

| Source directory | Lean files | theorems | Tag(s) where it is |
| --- | ---: | ---: | --- |
| `proofs/contributions/agent-118/prefix-kernel` | 1388 | 21656 | `archive/2026-10-17/research/agent-118/s20261015T1548` |
| `proofs/contributions/agent-104/prefix620-kernel-20261016` | 695 | 1117 | `archive/2026-10-17/deep-clean/automation-20261017`, `archive/2026-10-17/deep-clean/build-coverage-20261017` |
| `proofs/contributions/agent-124/prefix-five-six` | 328 | 2303 | `archive/2026-10-17/research/agent-124/s20261015T1600` |
| `proofs/contributions/agent-113/five-layer` | 99 | 1834 | `archive/2026-10-17/research/agent-113/s20261015` |
| `proofs/contributions/agent-124/four-digit-refinements` | 97 | 619 | `archive/2026-10-17/research/agent-124/s20261015T1600` |
| `proofs/contributions/agent-7/odd-nooverflow-fibers-20261016` | 36 | 284 | `archive/2026-10-17/deep-clean/automation-20261017`, `archive/2026-10-17/deep-clean/build-coverage-20261017` |
| `proofs/contributions/agent-108/window-weights-b31b8818` | 23 | 184 | `archive/2026-10-17/deep-clean/automation-20261017`, `archive/2026-10-17/deep-clean/build-coverage-20261017` |
| `proofs/contributions/agent-124/forward-invariant-196` | 19 | 45 | `archive/2026-10-17/research/agent-124/s20261015T1600` |
| `proofs/contributions/agent-102/affine-runs-20261016` | 16 | 34 | `archive/2026-10-17/deep-clean/automation-20261017`, `archive/2026-10-17/deep-clean/build-coverage-20261017` |
| `proofs/contributions/agent-3/two-history-20261016` | 16 | 130 | `archive/2026-10-17/deep-clean/automation-20261017`, `archive/2026-10-17/deep-clean/build-coverage-20261017` |
| `proofs/contributions/agent-7/allbase-overflow-births-20261016` | 14 | 45 | `archive/2026-10-17/formalize/agent-52/general-base-zero-interval-20261016`, `archive/2026-10-17/research/agent-7/base-overflow-20261016T2137Z` |
| `proofs/contributions/agent-117/remaining-prefix-cycles` | 14 | 99 | `archive/2026-10-17/research/agent-117/s20261015` |
| `proofs/contributions/agent-107/folded-transducer-20261016` | 11 | 0 | `archive/2026-10-17/deep-clean/automation-20261017`, `archive/2026-10-17/deep-clean/build-coverage-20261017` |
| `proofs/contributions/agent-1/periodic-width-projection-20261016` | 11 | 2 | `archive/2026-10-17/research/agent-1/periodic-cycle-adapter-20261017T0100Z`, `archive/2026-10-17/research/agent-1/periodic-eighteen-return-20261017T0123Z` |
| `proofs/contributions/agent-9/finite-ensemble-marker-count-20261016` | 9 | 102 | `archive/2026-10-17/deep-clean/automation-20261017`, `archive/2026-10-17/deep-clean/build-coverage-20261017` |
| `proofs/contributions/agent-102/affine-parameter-intervals-20261016` | 9 | 12 | `archive/2026-10-17/research/agent-102/affine-parameter-intervals-20261016T2215Z` |
| `proofs/contributions/agent-103/residual-five-20261016` | 8 | 179 | `archive/2026-10-17/deep-clean/automation-20261017`, `archive/2026-10-17/deep-clean/build-coverage-20261017` |
| `proofs/contributions/agent-103/residual-five-fibers-20261016` | 8 | 74 | `archive/2026-10-17/deep-clean/automation-20261017`, `archive/2026-10-17/deep-clean/build-coverage-20261017` |
| `proofs/contributions/agent-3/three-layer-prefix-20261016` | 8 | 45 | `archive/2026-10-17/deep-clean/automation-20261017`, `archive/2026-10-17/deep-clean/build-coverage-20261017` |
| `proofs/contributions/agent-4/general-base-normalization-20261016` | 8 | 84 | `archive/2026-10-17/formalize/agent-4/general-base-normalization-20261016` |
| `proofs/contributions/agent-15/spectral-carry-charge-43cf6e114472` | 7 | 83 | `archive/2026-10-17/formalize/agent-15/spectral-carry-charge-43cf6e114472`, `archive/2026-10-17/formalize/agent-15/spectral-carry-support-43cf6e114472` |
| `proofs/contributions/agent-1/periodic-prefix-saturation-20261016` | 7 | 0 | `archive/2026-10-17/research/agent-1/periodic-prefix-saturation-20261016T2358Z` |
| `proofs/contributions/agent-101/digit-split-multiplicity-20261016` | 6 | 31 | `archive/2026-10-17/archive/agent-105/ceil-half-suffix-b622465107d1`, `archive/2026-10-17/deep-clean/automation-20261017` |
| `proofs/contributions/agent-102/all-parameter-decisions-20261016` | 6 | 0 | `archive/2026-10-17/deep-clean/automation-20261017`, `archive/2026-10-17/deep-clean/build-coverage-20261017` |
| `proofs/contributions/agent-9/nooverflow-horizon-20261016` | 6 | 41 | `archive/2026-10-17/deep-clean/automation-20261017`, `archive/2026-10-17/deep-clean/build-coverage-20261017` |
| `proofs/contributions/agent-1/periodic-cycle-adapter-20261017` | 6 | 0 | `archive/2026-10-17/research/agent-1/periodic-cycle-adapter-20261017T0100Z`, `archive/2026-10-17/research/agent-1/periodic-eighteen-return-20261017T0123Z` |
| `proofs/contributions/agent-1/periodic-reduced-core-20261017` | 6 | 0 | `archive/2026-10-17/research/agent-1/periodic-reduced-core-20261017T0135Z` |
| `proofs/contributions/agent-3/prefix-contraction-20261016` | 6 | 71 | `archive/2026-10-17/research/agent-3/prefix-contraction-20261016-2232` |
| `proofs/contributions/agent-107/dfa-horn-closure-20261016` | 5 | 27 | `archive/2026-10-17/research/agent-1/agent104-monitor-verification-20261017T0307Z`, `archive/2026-10-17/research/agent-104/dfa-safety-monitor-20261016T2250Z` |
| `proofs/contributions/agent-1/periodic-return-core-20261016` | 5 | 0 | `archive/2026-10-17/research/agent-1/periodic-cycle-adapter-20261017T0100Z`, `archive/2026-10-17/research/agent-1/periodic-eighteen-return-20261017T0123Z` |
| `proofs/contributions/agent-1/periodic-eighteen-return-20261017` | 5 | 0 | `archive/2026-10-17/research/agent-1/periodic-eighteen-return-20261017T0123Z`, `archive/2026-10-17/research/agent-1/periodic-reduced-core-20261017T0135Z` |

## Tags

Pull requests: the head commit of every pull request is tagged `archive/2026-10-17/pull/<number>`.

Branches: 171 tags, one per branch tip at consolidation time:

| Tag | Commit | Last commit date |
| --- | --- | --- |
| `archive/2026-10-17/main` | `6ed031d21e` | 2026-10-17 11:44 |
| `archive/2026-10-17/archive/agent-105/ceil-half-suffix-b622465107d1` | `b622465107` | 2026-10-16 18:49 |
| `archive/2026-10-17/deep-clean/automation-20261017` | `7002585762` | 2026-10-17 11:00 |
| `archive/2026-10-17/deep-clean/build-coverage-20261017` | `7acc64f81e` | 2026-10-17 11:22 |
| `archive/2026-10-17/docs/agent-60/open-obligations-20261016` | `34e8f2151c` | 2026-10-16 17:21 |
| `archive/2026-10-17/docs/agent-61/status-reproduction-20261016` | `ec90fb1f0f` | 2026-10-16 22:24 |
| `archive/2026-10-17/docs/agent-62/residual-five-guide-20261016-bd61bb` | `056e6e9256` | 2026-10-16 17:34 |
| `archive/2026-10-17/docs/agent-63/report-index-links-20261016` | `fdbfb3b96f` | 2026-10-16 17:25 |
| `archive/2026-10-17/docs/agent-64/finite-horizon-count-20261016-6da1ed9b` | `48d08d3189` | 2026-10-16 17:17 |
| `archive/2026-10-17/docs/agent-65/source-map-guide-20261016-dbfcd4` | `b5448228f3` | 2026-10-16 17:25 |
| `archive/2026-10-17/docs/agent-66/affine-status-20261016-f05b879a` | `5dff11d2ab` | 2026-10-16 17:24 |
| `archive/2026-10-17/formalize/agent-14/carryfree-residue-saturation-20261016` | `1dafcf7c90` | 2026-10-16 16:52 |
| `archive/2026-10-17/formalize/agent-14/spectral-injectivity-20261016` | `719987c7e7` | 2026-10-16 16:32 |
| `archive/2026-10-17/formalize/agent-15/spectral-carry-charge-43cf6e114472` | `679d10a5b1` | 2026-10-16 16:40 |
| `archive/2026-10-17/formalize/agent-15/spectral-carry-support-43cf6e114472` | `708aa41b28` | 2026-10-16 17:04 |
| `archive/2026-10-17/formalize/agent-21/m99-a01-realizability-interface-20261015` | `cf969f404b` | 2026-10-16 10:00 |
| `archive/2026-10-17/formalize/agent-22/m99-a02-guard-review` | `f1806a3e53` | 2026-10-15 20:39 |
| `archive/2026-10-17/formalize/agent-221/finite-seed-bridge-20261015` | `51e05055c5` | 2026-10-15 20:38 |
| `archive/2026-10-17/formalize/agent-222/m99-b222-20261015` | `a9445224e2` | 2026-10-16 09:51 |
| `archive/2026-10-17/formalize/agent-23/m99-a03-20261015` | `e4377b2888` | 2026-10-16 10:00 |
| `archive/2026-10-17/formalize/agent-4/general-base-normalization-20261016` | `f85f7cb73d` | 2026-10-16 11:06 |
| `archive/2026-10-17/formalize/agent-51/spectral-overflow-saturation-20261016` | `7360b12a0a` | 2026-10-16 16:49 |
| `archive/2026-10-17/formalize/agent-51/spectral-reciprocal-moment-20261016` | `4c0382b16f` | 2026-10-16 16:58 |
| `archive/2026-10-17/formalize/agent-52/digit-sum-density-20261016` | `6641b1ea16` | 2026-10-16 16:52 |
| `archive/2026-10-17/formalize/agent-52/general-base-zero-interval-20261016` | `c68b0aaa53` | 2026-10-16 15:21 |
| `archive/2026-10-17/formalize/agent-53/20261016-c04cf11f6ff8` | `a05ac1a31d` | 2026-10-16 16:46 |
| `archive/2026-10-17/formalize/agent-8/common-overflow-defect-20261016` | `8874b2ee29` | 2026-10-16 14:16 |
| `archive/2026-10-17/formalize/agent-8/firsthit-four-endpoints-20261016` | `ae8bbdfd2a` | 2026-10-16 14:16 |
| `archive/2026-10-17/formalize/agent-9/digit-sum-interval-counts-20261016` | `d81784d62b` | 2026-10-16 14:37 |
| `archive/2026-10-17/formalize/agent-9/escape-factorial-bound-20261016` | `18a82d9b5a` | 2026-10-16 14:48 |
| `archive/2026-10-17/formalize/agent-9/finite-ensemble-marker-count-20261016` | `0d1eea6c69` | 2026-10-16 15:32 |
| `archive/2026-10-17/formalize/agent-9/marker-palindrome-intersection-20261016` | `0d1eea6c69` | 2026-10-16 15:32 |
| `archive/2026-10-17/formalize/agent-9/nooverflow-horizon-20261016` | `cb7293629d` | 2026-10-16 14:32 |
| `archive/2026-10-17/formalize/agent-9/one-step-digit-sum-collapse-20261016` | `0bfe5347de` | 2026-10-16 15:15 |
| `archive/2026-10-17/p196/coordination` | `fdd55ec984` | 2026-10-17 12:03 |
| `archive/2026-10-17/research/agent-1/agent104-monitor-verification-20261017T0307Z` | `bf5c945989` | 2026-10-17 03:10 |
| `archive/2026-10-17/research/agent-1/backward-layers-verification-20261017T0142Z` | `c3af0a6132` | 2026-10-17 01:46 |
| `archive/2026-10-17/research/agent-1/ceilhalf-verification-20261017T0210Z` | `a5690de955` | 2026-10-17 02:31 |
| `archive/2026-10-17/research/agent-1/groupIII-delayed-overlap-20261016T2120Z` | `273f9e156f` | 2026-10-16 21:31 |
| `archive/2026-10-17/research/agent-1/groupIII-handoff-20261016T2132Z` | `624cc122e3` | 2026-10-16 21:49 |
| `archive/2026-10-17/research/agent-1/normalization-and-groupIII-20261016T2110Z` | `0431e0a64d` | 2026-10-16 21:17 |
| `archive/2026-10-17/research/agent-1/periodic-block-strip-20261016T2146Z` | `bf4ff74900` | 2026-10-16 21:50 |
| `archive/2026-10-17/research/agent-1/periodic-cycle-adapter-20261017T0100Z` | `7f23ce839f` | 2026-10-17 01:16 |
| `archive/2026-10-17/research/agent-1/periodic-eighteen-return-20261017T0123Z` | `5e67f08231` | 2026-10-17 01:43 |
| `archive/2026-10-17/research/agent-1/periodic-guard-20261016T2122Z` | `95a17ceeab` | 2026-10-16 21:32 |
| `archive/2026-10-17/research/agent-1/periodic-guarded-path-20261017T0017Z` | `cb753e1f5e` | 2026-10-17 01:00 |
| `archive/2026-10-17/research/agent-1/periodic-nine-center-20261017T0209Z` | `fa8cf9024c` | 2026-10-17 02:33 |
| `archive/2026-10-17/research/agent-1/periodic-nine-clock-strip-20261017T0250Z` | `797170d455` | 2026-10-17 03:03 |
| `archive/2026-10-17/research/agent-1/periodic-nine-control-20261017T0219Z` | `83345f579a` | 2026-10-16 23:18 |
| `archive/2026-10-17/research/agent-1/periodic-nine-cycle-20261017T0156Z` | `b8c17a5204` | 2026-10-17 02:06 |
| `archive/2026-10-17/research/agent-1/periodic-nine-excursion-20261017T0240Z` | `098d0285c8` | 2026-10-17 02:50 |
| `archive/2026-10-17/research/agent-1/periodic-outer-catalog-20261016T2252Z` | `159ed83569` | 2026-10-16 23:35 |
| `archive/2026-10-17/research/agent-1/periodic-phase-catalog-20261016T2247Z` | `d299c93027` | 2026-10-16 22:55 |
| `archive/2026-10-17/research/agent-1/periodic-prefix-saturation-20261016T2358Z` | `e4351cd31f` | 2026-10-17 00:21 |
| `archive/2026-10-17/research/agent-1/periodic-reduced-core-20261017T0135Z` | `9ad1851979` | 2026-10-17 01:57 |
| `archive/2026-10-17/research/agent-1/periodic-return-clock-20261016T2345Z` | `ebcaf723d6` | 2026-10-17 00:01 |
| `archive/2026-10-17/research/agent-1/periodic-return-core-20261016T2335Z` | `946c69edf3` | 2026-10-16 23:50 |
| `archive/2026-10-17/research/agent-1/periodic-return-upper-gap-20261017T0020Z` | `502d3f5ea2` | 2026-10-17 01:06 |
| `archive/2026-10-17/research/agent-1/periodic-safety-20261016T2205Z` | `c74c9d1ca1` | 2026-10-16 22:14 |
| `archive/2026-10-17/research/agent-1/periodic-validity-20261016T2153Z` | `ae4e1f09a0` | 2026-10-16 22:02 |
| `archive/2026-10-17/research/agent-1/periodic-width-projection-20261016T2304Z` | `e77289c5f5` | 2026-10-16 23:44 |
| `archive/2026-10-17/research/agent-1/periodic-zero-cycle-20261016T2221Z` | `5d3b027df0` | 2026-10-16 22:37 |
| `archive/2026-10-17/research/agent-1/periodic-zero-escape-20261016T2238Z` | `c440e01ee4` | 2026-10-16 22:44 |
| `archive/2026-10-17/research/agent-1/pr104-review-20261016T2205Z` | `36f3a58b22` | 2026-10-16 22:17 |
| `archive/2026-10-17/research/agent-1/pr165-verification-20261017T0118Z` | `ccd55bec03` | 2026-10-17 01:24 |
| `archive/2026-10-17/research/agent-1/zero-width-loop-20261016T2359Z` | `9e8d30809c` | 2026-10-17 00:14 |
| `archive/2026-10-17/research/agent-100/groupII-overflow-sharpness-20261016T2144Z` | `29b572f523` | 2026-10-16 16:31 |
| `archive/2026-10-17/research/agent-100/groupII-overlap-20261016T2052Z` | `c0534138ff` | 2026-10-16 14:56 |
| `archive/2026-10-17/research/agent-100/groupII-rebase-20261016T2212Z` | `40670be363` | 2026-10-16 15:44 |
| `archive/2026-10-17/research/agent-100/groupII-third-output-20261016T2239Z` | `bc178ab873` | 2026-10-16 15:29 |
| `archive/2026-10-17/research/agent-100/third-gate-boundary-20261016T2126Z` | `6b2a8c7ca8` | 2026-10-16 14:51 |
| `archive/2026-10-17/research/agent-100/third-gate-descent-212248Z` | `586bf0b67e` | 2026-10-16 14:51 |
| `archive/2026-10-17/research/agent-101/all-width-inverse-maximum-20261016T2204Z` | `429b2c34f2` | 2026-10-16 15:46 |
| `archive/2026-10-17/research/agent-101/digit-split-multiplicity-20261016T2103Z` | `a5ebd78fdc` | 2026-10-16 14:26 |
| `archive/2026-10-17/research/agent-101/nonpalindromic-protected-fibers-20261016T2123Z` | `71c2ab3393` | 2026-10-16 15:31 |
| `archive/2026-10-17/research/agent-101/two-history-realizations-20261016T2238Z` | `4e101db40f` | 2026-10-16 20:46 |
| `archive/2026-10-17/research/agent-102/affine-parameter-intervals-20261016T2215Z` | `1c1bff874c` | 2026-10-16 15:41 |
| `archive/2026-10-17/research/agent-102/affine-runs-20261016T2124Z` | `69392ee406` | 2026-10-16 14:59 |
| `archive/2026-10-17/research/agent-102/all-parameter-decisions-20261016T2150Z` | `9361e8a8d1` | 2026-10-16 15:12 |
| `archive/2026-10-17/research/agent-103/residual-five-20261016T2118Z` | `05e4ac30bb` | 2026-10-16 14:47 |
| `archive/2026-10-17/research/agent-103/residual-five-fibers-20261016T2130Z` | `b235d662ce` | 2026-10-16 15:25 |
| `archive/2026-10-17/research/agent-103/residual-five-firsthit-two-20261016T2200Z` | `43219b02c1` | 2026-10-16 15:36 |
| `archive/2026-10-17/research/agent-103/residual-five-predecessor-filter-count-20261016T0025Z` | `cb273afa5b` | 2026-10-16 17:39 |
| `archive/2026-10-17/research/agent-103/residual-five-third-gate-20261016T2230Z` | `64d0a37029` | 2026-10-16 15:45 |
| `archive/2026-10-17/research/agent-104/620-depth12-witness-20261016T2143Z` | `0a5cdbb1d2` | 2026-10-16 15:36 |
| `archive/2026-10-17/research/agent-104/620-kernel-20261016T2122Z` | `32d2b92ec7` | 2026-10-16 16:38 |
| `archive/2026-10-17/research/agent-104/dfa-safety-monitor-20261016T2250Z` | `2d98c81fcd` | 2026-10-16 20:21 |
| `archive/2026-10-17/research/agent-104/exact-zero-gap-20261016T2126Z` | `5bc57fec69` | 2026-10-16 14:49 |
| `archive/2026-10-17/research/agent-104/review-pr100-cylinder-20261016T2227Z` | `e909f26954` | 2026-10-16 14:58 |
| `archive/2026-10-17/research/agent-105/8f1107db019a-affine-dynamics` | `b312815ba8` | 2026-10-16 15:10 |
| `archive/2026-10-17/research/agent-105/all-predecessors-9df76b-20261016` | `d37aa2f2af` | 2026-10-16 15:30 |
| `archive/2026-10-17/research/agent-105/backward-layers-9df76b-20261016` | `59091760af` | 2026-10-16 18:31 |
| `archive/2026-10-17/research/agent-105/ceil-half-suffix-8f1107db019a` | `9ab3c2d211` | 2026-10-16 19:09 |
| `archive/2026-10-17/research/agent-105/cross-width-palindrome-9df76b-20261016` | `cd11afd688` | 2026-10-16 14:49 |
| `archive/2026-10-17/research/agent-105/numeric-decoder-9df76b-20261016` | `ec7aa17a36` | 2026-10-16 15:20 |
| `archive/2026-10-17/research/agent-106/congruence-carry-budget-20261016T2131Z` | `0a490cc9d1` | 2026-10-16 17:05 |
| `archive/2026-10-17/research/agent-106/congruence-finite-path-20261016T2149Z` | `ed9b9048ad` | 2026-10-16 14:48 |
| `archive/2026-10-17/research/agent-107/dfa-horn-closure-20261016T2203Z` | `6f48ca108d` | 2026-10-16 21:37 |
| `archive/2026-10-17/research/agent-107/folded-transducer-20261016T2130Z` | `90c639b8a7` | 2026-10-16 15:13 |
| `archive/2026-10-17/research/agent-108/matrix-weights-b31b8818-20261016` | `de75fed1de` | 2026-10-16 15:17 |
| `archive/2026-10-17/research/agent-108/window-weights-b31b8818-20261016` | `6ee27fa2c3` | 2026-10-16 15:30 |
| `archive/2026-10-17/research/agent-109/s20261015` | `5808b992ab` | 2026-10-15 01:22 |
| `archive/2026-10-17/research/agent-11/m99-a01-20261015` | `d6942d7f9c` | 2026-10-16 10:00 |
| `archive/2026-10-17/research/agent-110/two-step-return-20261016T2123Z` | `51f8f8d523` | 2026-10-16 15:00 |
| `archive/2026-10-17/research/agent-111/bounded-variable-modulus-20261016T2130Z` | `037ab13630` | 2026-10-16 14:41 |
| `archive/2026-10-17/research/agent-111/growing-composite-modulus-20261017T0210Z` | `74a1c3922e` | 2026-10-16 17:02 |
| `archive/2026-10-17/research/agent-111/growing-tenpower-suffix-20261016T2137Z` | `01ecb6aa6b` | 2026-10-16 14:57 |
| `archive/2026-10-17/research/agent-112/cylinder-image-20261016T2130Z` | `e909f26954` | 2026-10-16 14:58 |
| `archive/2026-10-17/research/agent-113/descending-prefix-maximality-20261016T212415Z` | `1476a713c4` | 2026-10-17 10:56 |
| `archive/2026-10-17/research/agent-113/s20261015` | `0be6bd7010` | 2026-10-15 13:34 |
| `archive/2026-10-17/research/agent-114/core17-r3-firsthit-s2124Z` | `920fc826cc` | 2026-10-16 14:58 |
| `archive/2026-10-17/research/agent-114/short-r-firsthit-20261016T2126Z` | `c9a86a40ff` | 2026-10-16 16:52 |
| `archive/2026-10-17/research/agent-115/rho-cycle-balance-20261016T2130Z` | `254b4bc6b5` | 2026-10-16 14:58 |
| `archive/2026-10-17/research/agent-115/s20261015-review-broader` | `fba03a902e` | 2026-10-15 12:55 |
| `archive/2026-10-17/research/agent-117/k7-four-digit-2641-20261016T2129Z` | `361de9f7ee` | 2026-10-16 14:58 |
| `archive/2026-10-17/research/agent-117/k8-2641-depth5-20261016T2200Z` | `7b9e663b3c` | 2026-10-16 15:03 |
| `archive/2026-10-17/research/agent-117/s20261015` | `4acd0c8ba1` | 2026-10-15 12:48 |
| `archive/2026-10-17/research/agent-118/k7-double-5523-5524-20261016T2136Z` | `50f099bef9` | 2026-10-16 14:58 |
| `archive/2026-10-17/research/agent-118/s20261015T1548` | `ebbaf24e66` | 2026-10-15 13:30 |
| `archive/2026-10-17/research/agent-119/s20261015T1555` | `d9a8bfa0fd` | 2026-10-15 12:59 |
| `archive/2026-10-17/research/agent-119/s20261015T2005-eight-families` | `913441a936` | 2026-10-15 13:26 |
| `archive/2026-10-17/research/agent-12/m99-a02-20261015` | `4ca35f4707` | 2026-10-16 09:49 |
| `archive/2026-10-17/research/agent-120/s20261015T1625` | `59779bc975` | 2026-10-15 09:54 |
| `archive/2026-10-17/research/agent-124/s20261015T1600` | `a4d803f489` | 2026-10-15 12:56 |
| `archive/2026-10-17/research/agent-13/m99-a03-20261015` | `60ba0c8c31` | 2026-10-16 10:00 |
| `archive/2026-10-17/research/agent-14/ordinary-exterior-six-twelve-bridge-20261015` | `2a4e13d48c` | 2026-10-15 20:17 |
| `archive/2026-10-17/research/agent-15/s20261015T2014` | `4bde9becd3` | 2026-10-15 20:16 |
| `archive/2026-10-17/research/agent-16/m99-a06-20261015` | `dd49ba717c` | 2026-10-15 20:18 |
| `archive/2026-10-17/research/agent-17/m99-a07-20261015` | `6031b2831a` | 2026-10-16 09:57 |
| `archive/2026-10-17/research/agent-18/20261015-finite-seed` | `585e918a8b` | 2026-10-15 20:18 |
| `archive/2026-10-17/research/agent-2/first-hit-eleven-20261016T2100Z` | `4b4edf976b` | 2026-10-16 11:37 |
| `archive/2026-10-17/research/agent-2/overflow-fibers-20261016T2040Z` | `fb2b832c06` | 2026-10-16 14:19 |
| `archive/2026-10-17/research/agent-211/m99-b211-finite-realizability-audit` | `7117b9d168` | 2026-10-15 20:28 |
| `archive/2026-10-17/research/agent-211/m99-b211-finite-realizability-audit-clean` | `b95e592e98` | 2026-10-15 20:28 |
| `archive/2026-10-17/research/agent-211/review-agent11-finite-scan` | `7df9425e66` | 2026-10-16 09:53 |
| `archive/2026-10-17/research/agent-211/two-phase-a3-extension` | `6d5618b646` | 2026-10-16 09:53 |
| `archive/2026-10-17/research/agent-211/two-phase-b3-extension` | `8c84f43d72` | 2026-10-16 09:53 |
| `archive/2026-10-17/research/agent-211/two-phase-c-extension` | `e03f6e662e` | 2026-10-16 09:53 |
| `archive/2026-10-17/research/agent-211/two-phase-c4-extension` | `3f425f8ebd` | 2026-10-16 09:53 |
| `archive/2026-10-17/research/agent-212/m99-b212-20261015` | `23e373f784` | 2026-10-15 20:32 |
| `archive/2026-10-17/research/agent-213/20261015-gap` | `e2dd014be3` | 2026-10-16 10:00 |
| `archive/2026-10-17/research/agent-215/20261015-saturated8` | `adc0f66099` | 2026-10-16 09:56 |
| `archive/2026-10-17/research/agent-216/s20261015-general-nat-bridge` | `d3766fee26` | 2026-10-15 20:43 |
| `archive/2026-10-17/research/agent-216/s20261015-mod22` | `bbb0732d0f` | 2026-10-16 09:54 |
| `archive/2026-10-17/research/agent-216/s20261015-residue-filter` | `a0010e85e5` | 2026-10-15 20:42 |
| `archive/2026-10-17/research/agent-217/s20261015-uniformity` | `b3a8ccc6b0` | 2026-10-15 20:37 |
| `archive/2026-10-17/research/agent-3/finite-horizon-20261016-2054` | `5084eadce9` | 2026-10-16 14:21 |
| `archive/2026-10-17/research/agent-3/prefix-contraction-20261016-2232` | `e71d54672e` | 2026-10-17 03:20 |
| `archive/2026-10-17/research/agent-3/three-layer-prefix-20261016-2200` | `8a67ea8204` | 2026-10-16 15:27 |
| `archive/2026-10-17/research/agent-3/two-history-20261016-2105` | `89287c9d3e` | 2026-10-16 14:52 |
| `archive/2026-10-17/research/agent-311/m99-c311-20261015` | `0056af75a9` | 2026-10-15 20:49 |
| `archive/2026-10-17/research/agent-312/m99-c312-block-guard-20261015` | `e14488cb23` | 2026-10-15 20:50 |
| `archive/2026-10-17/research/agent-313/m99-c313-20261015` | `ef135dea53` | 2026-10-15 20:51 |
| `archive/2026-10-17/research/agent-314/ordinary-exterior-audit` | `782af1f79c` | 2026-10-15 20:51 |
| `archive/2026-10-17/research/agent-315/s20261015-temporal-columns` | `586690e5ec` | 2026-10-16 10:00 |
| `archive/2026-10-17/research/agent-317/m99-c317-uniformity-20261015` | `e8263d0224` | 2026-10-16 09:58 |
| `archive/2026-10-17/research/agent-318/m99-c318-backward-return-20261015` | `264197c42f` | 2026-10-16 10:00 |
| `archive/2026-10-17/research/agent-4/normalizer-support-20261016-2057` | `4b4edf976b` | 2026-10-16 11:37 |
| `archive/2026-10-17/research/agent-5/absorption-evidence-20261016T2122Z` | `5356cff6c4` | 2026-10-16 14:20 |
| `archive/2026-10-17/research/agent-5/digit-streams-20261016T2108Z` | `9e59a77ae4` | 2026-10-16 15:36 |
| `archive/2026-10-17/research/agent-5/even-base-repair-20261016T2055Z` | `f58625093e` | 2026-10-16 14:05 |
| `archive/2026-10-17/research/agent-5/ordinary-stream-prefix-20261016T2140Z` | `5c4d394f20` | 2026-10-16 15:10 |
| `archive/2026-10-17/research/agent-5/stream-agreement-window-20261016T2205Z` | `9b1535d80a` | 2026-10-16 15:25 |
| `archive/2026-10-17/research/agent-6/certificate-coordinate-audit-20261016` | `dca30e7647` | 2026-10-16 15:06 |
| `archive/2026-10-17/research/agent-6/exterior-coordinate-dynamics-20261016` | `215ec5e5ad` | 2026-10-16 14:35 |
| `archive/2026-10-17/research/agent-6/normalized-carry-accounting-20261016` | `f0e2097b82` | 2026-10-16 15:45 |
| `archive/2026-10-17/research/agent-7/base-overflow-20261016T2137Z` | `c68b0aaa53` | 2026-10-16 15:21 |
| `archive/2026-10-17/research/agent-7/odd-fibers-20261016T2100Z` | `4fb13bd524` | 2026-10-16 15:50 |
| `archive/2026-10-17/research/agent-7/run-renewal-20261016T2225Z` | `638a9957c3` | 2026-10-16 15:33 |
| `archive/2026-10-17/research/agent-9/fibonacci-asymptotic-rate-20261017T0313Z` | `ce4af33479` | 2026-10-17 03:23 |
| `archive/2026-10-17/review/agent-105/pr112-8f1107db019a` | `d43cbd3f3d` | 2026-10-16 18:35 |
