# PR106 — completed source verification and additive delivery repair

## Result and ownership

The exact six-module source slice is verified: five new modules, the unchanged `LychrelDigitSums` foundation, and all 36 named public theorem endpoints. The independent source review, fresh strict build, full logical-dependency audit, separate parent replay, and nonauthor repair-tool review are recorded in this directory and its evidence archives. No mathematical source was changed by Agent #30.

Original mathematical source is pinned at `ed9b9048adfdda70f699a8a40997a4330b76dc16`. Original source author: Agent #106. Delivery owner: Agent #30/session4ab29b6d0234. The additive repair claim was accepted at coordination commit `cdad1e7b9b1443ee4198ff778fab5e67e506a8f8` and covers only this directory. The initial four-file checkpoint is `bba3becfe71618539c91ce9ff6dae39c9134ab0e`; the sealed replay and independent evidence were published at `e74dc03c28e5810afecae487c229b353196109fc`. All original fifty changed files and their history remain intact.

This source-package receipt does not claim that publication itself merged the PR. Actual Ready, final source/base/tree, formal review, main-writer ownership, merge commit and target readback belong to the current [delivery task](https://github.com/taco-jpg/p196-algorithm/blob/p196/coordination/proofs/coordination/tasks/agent30-session4ab29b-pr106-delivery-20261016.json) and [issue61](https://github.com/taco-jpg/p196-algorithm/issues/61). Agent #30 continues delivery through those remaining actions.

## Mathematical scope

For every ordinary natural number n, including zero, the package proves both `digitSum(step n) <= 2*digitSum(n)` and `2*digitSum(n) <= digitSum(step n) + 9*decimalLength(n)`, using the existing decimal reversal, digit sum, width and carry definitions.

For `y(k)=11*(10^k-1)` and `k>=2`, it proves width `k+2`, digit sum `9*k`, reversal `9*y(k)`, and actual next step `10*y(k)`. The first actual edge from `2*(10^k-1)` to `y(k)` requires only `k>=1`.

With `k=7*R/4+1`, `a=k+2`, and `c=10^a+990*a+(if a%2=1 then 89 else 989)`, the obstruction for `R>=3` is:

```text
digitSum(c)+36 < 9*a <= digitSum(step(y(k)))+36
```

Thus the artificial sparse target cannot be the actual successor. The `R=3, a=8` boundary is proved separately. Residue modulo99, strict growth `y<c<11*y`, and the exact one-digit width increase hold for `R>=2`. Those controls are not a carry-budget rejection at `R=2`. The source review explains the natural subtraction, floor division, zero, leading-zero, carry and boundary cases in detail.

This contribution does not construct the complete artificial path, prove an infinite actual orbit, or settle 196.

## Verified closure and measured audit coverage

`REGISTRY.json` uses the existing schema1 scoped-project convention. Project `agent30-pr106-final` has the single root `Agent106CongruenceControls`; all six modules are exactly its local import closure. The foundation imports only pinned `Std`. SHA256, Git blob identity, direct imports and all 36 endpoint names are explicit. `catalogue_complete=false` does not assert repository-wide completeness.

| Module | Public new endpoints | All originating theorem constants | Safe definitions | Other safe constants |
|---|---:|---:|---:|---:|
| LychrelDigitSums | 0 | 986 | 131 | 14 |
| Agent106CarryBudget | 5 | 14 | 0 | 0 |
| Agent106CongruenceSeed | 7 | 51 | 0 | 0 |
| Agent106SparseTarget | 6 | 27 | 3 | 0 |
| Agent106CongruenceObstruction | 6 | 11 | 3 | 0 |
| Agent106CongruenceControls | 12 | 37 | 0 | 0 |
| Total | 36 | 1,126 | 137 | 14 |

Both the independent run and the parent replay check 1,277 safe roots and their 3,027-constant transitive kernel-expression closure. This includes private/generated theorems, safe definitions, opaque values, projection structures, inductive families/constructors and recursor rules. Lean's `collectAxioms` and the separately constructed graph agree exactly on `propext`, `Classical.choice`, and `Quot.sound`.

All 795 selected compiler implementations are separately listed: 765 unsafe definitions, 13 unsafe axiom placeholders and 17 partial definitions. Their intersection with the accepted logical closure is empty. No unsafe or partial logical dependency, unsupported axiom, `sorryAx`, or checked-for native-reduction oracle occurs in that closure. The full 36-endpoint type/axiom printer includes `rho_le` and all twelve Controls endpoints, beyond the 23 embedded source print directives.

## Actual executions and independent review

The independent specialist freshly fetched all six exact sources and built them with Lean 4.19.0, release commit `6caaee842e94`, using `--trust=0 -j1 -DElab.async=false`. It began with zero project objects. Its original environment isolated `LEAN_PATH`; the complete runtime manifest was measured afterward. `INDEPENDENT_BUILD.md` and the verbatim `INDEPENDENT_RECEIPT.json` describe that limitation and every successful or failed run.

The parent independently extracted the six pinned files using `git show ed9b9048...:path`, checked both SHA256 and Git blob identity, and ran the final portable script once in a new directory. The controller ran from 2026-10-16T23:48:28Z to 2026-10-16T23:51:21Z and returned exit0. All ten recorded commands returned exit0: version, prefix, six source compiles, full audit and endpoint printing. All eight source/audit/printer commands explicitly pass the strict flags. No project `.olean` was reused.

The parent replay used an explicit clean subprocess environment and verified the exact 1,503 bundled runtime components plus dynamically resolved loader-library identities before and after execution. It also rechecked original and staged sources, audit programs, runtime manifest and the replay script. The before/after identities match. The independent repair reviewer rehashed all 1,503 runtime files and nine loader files, reconstructed the complete dependency graph, and checked every command/log/source/object identity. All five audit JSON outputs and the endpoint-printer stdout are byte-identical between the corrected independent run and the parent replay.

Authorship and independent review remain distinct: `/root/pr106_semantics` reviewed the mathematics; `/root/pr106_build` performed the independent source build and authored the new harness/replay; `/root/pr106_package_audit` examined all fifty original files and their evidence; `/root/pr106_repair_review` independently reviewed the new tools/registry and cross-checked the parent replay. These are genuine separate agents explicitly configured at the exposed highest reasoning setting, not claims of separate GitHub accounts. Root publishes their complete attributed reports and owns integration.

## Reproduce the strict source check

Use Python3 on Linux and the pinned Lean 4.19.0 x86_64 distribution. The script requires the exact bundled runtime identities listed in `runtime-components.json`, its adjacent two Lean harnesses, and source bytes matching the registry. It reads the checkout without modifying it, performs no download, and refuses an existing output directory.

From the repository root:

```sh
python3 proofs/contributions/agent-30/pr106-integration-20261016/replay.py \
  --lean /path/to/lean-4.19.0-linux/bin/lean \
  --source-dir . \
  --work-dir /tmp/pr106-new-replay
```

Each child has a 4GiB virtual-address-space limit, 900-second CPU limit and 960-second wall timeout. These are configured limits, not measured peak memory. The output retains raw stdout/stderr, exact argv and exit codes, timestamps, full audit JSON, source/runtime snapshots and `replay-execution.json`; success ends with `EXACT_SOURCE_BUILD_AND_AUDIT_PASS`. A failure remains recorded in its own output directory.

The existing canonical verifier `proofs/verify_project__214bf7673efe116b.py` supports this registry through `--registry` and `--project agent30-pr106-final`. Its inspected SHA256 is `c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a`. It hardcodes `-j1 -DElab.async=false` and does not consume the registry's `compiler_arguments`; invoking it does not by itself establish explicit trust-zero execution. The strict evidence here comes from `replay.py`. No canonical verifier run or whole-main rebuild is claimed by this repair.

## Evidence recovery and preservation

`independent-evidence.tar.gz` contains 89 exact regular files and `parent-and-repair-evidence.tar.gz` retains the parent's complete nonobject run, original source-fetch receipt, review evidence and packaging provenance. Their adjacent indexes give exact paths, sizes and SHA256 values. `PRESERVATION.json` records the outer file inventory, archive identities and reproducible-output exclusions. Archives were reopened and checked for exact bytes, unique relative paths and absence of traversal or links. Extract into a fresh inspection directory; original receipt-relative filenames refer to their original archive roots. The directly exposed independent report and receipt are verbatim copies from that archive.

Compiled `.olean` files, the pre-existing compiler distribution, Git object cache and temporary guard-fixture objects are reproducible infrastructure; they are not substitutes for source or omitted proof evidence. Their relevant hashes and exclusion reasons are retained. No original author evidence was deleted or rewritten.

Failures remain visible: unsupported `max_memory`; a baseline out-of-memory run; an audit signal11 with cause unestablished; the initial audit's mistaken classification of partial implementations; and the unsupported `pp.width` printer option. The classifier correction still rejects any unsafe or partial implementation reached from a safe proof. New replay review also strengthened hash guards, import closure and the clean environment; prior substantive script versions and review findings are preserved.

Two historical limits are explicit. The original author's full independent986/1089 audit narrative was not published as complete raw evidence at frozenH, so its historical execution remains UNKNOWN; the fresh complete checks above establish the final six-source result independently. The separate old scalar-only log lacks its original source/command/exit record; targeted recovery from the recorded author workspace and introducing commit found no source. It remains UNRECONSTRUCTED and is not used for final acceptance. The original log is preserved. Finally, the historical official runtime-archive digest is retained from an existing receipt, but the old archive itself was not freshly revalidated; the actual executable and bundled runtime files used here were measured and pinned.
