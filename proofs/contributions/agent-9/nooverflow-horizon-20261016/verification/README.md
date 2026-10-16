# Agent #9 independent verification evidence

The final selected 15-module closure passed an independent clean replay under Lean 4.19.0, release commit `6caaee842e94`, with `--trust=0` on every source compilation 和 on the generated axiom audit. The mathematical sources were unchanged.

## Final result

| Check | Recorded result |
| --- | --- |
| Selected mathematical modules compiled | 15, all exit code 0 |
| Historical dependencies | 10 exact original commit/path/blob comparisons |
| Theorem constants audited | 1,539, including private/generated proof auxiliaries |
| Safe definitions/opaque declarations audited | 346 |
| New-module coverage | All 82 theorem constants 和 all five safe definitions from the five new modules |
| Accepted transitive axiom union | `Classical.choice`, `Quot.sound`, `propext` |
| Source/registry/compiler stability | Checked before 和 after the replay; selected inputs unchanged |
| Starting object files in isolated build directory | 0 |
| Raw final status | `PASS_SELECTED_SOURCE_CLOSURE` |

The generated audit walks imported declarations by their source module. It examines every theorem 和 safe definition in the selected closure, rejects safe custom axioms, 和 rejects transitive dependencies outside the three listed standard axioms. It separately records 21 unsafe implementation constants 和 1,041 unsafe implementation definitions from the historical closure; these are compiler implementation declarations, 和 none introduces an accepted theorem or safe-definition dependency outside the permitted axiom set. The source token scan rejects `sorry`, `admit`, `axiom`, `sorryAx`, `native_decide`, `ofReduceBool`, 和 `skipKernelTC` after masking comments 和 strings.

The theorem count includes generated helpers, so it should 不 be described as 1,539 independently authored mathematical results. Likewise, the 82 new-module theorem constants include private helpers 和 generated auxiliaries. `NEW_MODULE_AUDIT.json` lists each exact audited name.

## Replay

From the repository root, with its historical Git objects available:

```bash
python3 proofs/contributions/agent-9/nooverflow-horizon-20261016/verify.py \
  --lean /absolute/path/to/lean-4.19.0/bin/lean \
  --output /absolute/path/to/a-new-output-directory \
  --auditor 'Actual executing person or agent'
```

The output directory must be new. The verifier copies each selected `.lean` file byte-for-byte into a separate source directory, resolves the exact registered import closure, 和 builds objects into an initially empty build directory. `LEAN_PATH` contains only that build directory; the specified compiler supplies its own standard library. No existing project `.olean` is used. The verifier can be run elsewhere using explicit `--repo`, `--package-root`, 和 `--manifest` arguments. It performs read-only Git provenance/status commands with `GIT_OPTIONAL_LOCKS=0`; it does 不 edit the source repository.

Every compiler invocation, exit code, duration, working directory, log hash, source hash, registry hash, selected runtime hash, 和 the auditor identity is recorded in `verification.json`. Unrelated repository changes are recorded without being confused with changes to the selected source snapshot. Exact selected source, registry, 和 compiler changes remain failures.

## Retained evidence

| Directory or file | Meaning |
| --- | --- |
| `independent-full-001/` | Final 15-module runtime-audit execution, explicit `--trust=0`, all theorem/safe-definition audit |
| `independent-core-001/` | Earlier completed 12-module independent execution, retained with its actual original command flags 和 old aggregate |
| `parent-core-001/` | Separate parent execution of that 12-module snapshot; `ATTRIBUTION.json` explains the legacy hardcoded `auditor` field without editing its raw report |
| `independent-counts/` | Completed independent eight-module historical-fiber/count replay |
| `baseline-consolidation-core/` | Original 38-module consolidation replay, with its raw repository-status guard failure preserved 和 a separate scoped source/axiom assessment |
| `COUNT_REVIEW.md` | Independent semantic review of the historical five-module fiber proof 和 intrinsic count extension |
| `NUMERIC_REVIEW.md` | Independent semantic review of the canonical integer bridge, universal transfer, 和 exact time shift |
| `runtime-manifest.json` | Hash inventory of the locally available compiler, shared libraries, 和 shipped Lean object files |
| `sandbox-launch.json` | Actual restricted-launch failure 和 successful runtime comparison evidence |

Each retained run directory has `EVIDENCE_FILES.json` listing its retained files 和 hashes. Compiled objects 和 duplicate source copies omitted from these compact evidence directories are reproducible, 和 are explicitly identified as omitted in `RETENTION.json`. The old 12-module aggregate is separately retained because the canonical aggregate has since gained the numerical endpoint. No omitted file is presented as retained evidence.

The raw 38-module baseline status remains `FAIL`: its strict repository-wide status guard detected the parent-authorized creation of the new contribution during the replay. The separate assessment establishes that all 38 modules compiled, all 3,491 theorem constants passed their axiom audit, 和 all 40 selected source/registry inputs were unchanged. That scoped assessment does 不 relabel the original run as a repository-wide pass.

## Stable identifiers

| Item | SHA256 |
| --- | --- |
| Final source registry | `3198cf758a7d4d6e6d8d3da1c16f8c420bafd3f83c3bfd11accaed7c2ba159f1` |
| Final verifier | `b84886f16cc8dc6e1c0fb1b2659893832c4dc415858320ce83d134cfa1d66c4e` |
| Final independent raw report | `dc1651c45fa2c6d3a9bb961ea53f67513b7452c486255a0bfc431757866efd62` |
| Final audit source | `c74c6e2c6e548567bbf21d7b712b8367d9387cb0fd9ae37077f44612b83740f0` |
| Final audit log | `6daf16f203c93eb831e2667126a6140de1a6e56a62dd2b9170ec56225c7f54c2` |
| Earlier independent 12-module raw report | `e4d56b243d9f68a89878d760bd28083d71a576eaefab301c2d017101044ebd68` |
| Parent 12-module raw report | `91876406895dfef97183cab2815323fadb8217a2072a3ca44b93a7d4a67d3c9d` |

## Mathematical scope

The final construction counts a complete, duplicate-free no-overflow coefficient-word predecessor fiber exactly by `fib m`; its intrinsic membership predicate uses exact width, symmetry, digit-pair bounds, positive exterior, zero final carry, 和 the original word transition. Every listed word has a positive actual integer realization. Every canonical realization of such a predecessor has nonpalindromic orbit values at times 1 through `k + 1`, while every canonical target realization is nonpalindromic at times 0 through `k`.

The exact count is a count of coefficient words. It is 不 an exact count of the possible integer digit splits. The seed may depend on the finite parameters, 和 the construction does 不 supply a fixed seed safe forever or a claim that 196 is Lychrel. These limitations match the actual theorem quantifiers.
