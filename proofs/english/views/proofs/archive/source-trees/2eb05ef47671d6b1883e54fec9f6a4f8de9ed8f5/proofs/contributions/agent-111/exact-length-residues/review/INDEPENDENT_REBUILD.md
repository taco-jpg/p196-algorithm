# Agent111 independent clean-rebuild record

**Conclusion: PASS.** The pinned commit's `All.lean` import closure rebuilt successfully in a fresh empty directory:13 source modules,1,004 theorem declarations including private/compiler-generated helpers, all actually audited with `#print axioms`.

- Pinned source commit: `c3192d5bf2962298bcb2bb209a0947f657e8a7e5`.
- Source branch: `research/agent-111/s20261015-1534`; repository: `https://github.com/taco-jpg/p196-algorithm.git`.
- Acquisition: `git archive` of that commit exported exact foundation files, top-level contribution Lean files, and frozen `check.py`; no mathematical source came from a live working tree.
- Archive SHA-256: `4bebb8633421501d1299a941330fa8aed8ab9a11f2ba21a46c506fbbc04d6135`.
- Checker SHA-256: `9fea73de4ea0497a1747e0b635bd1ea5d74d15b7479f89ae1351272f7093a9af`.
- Independent source snapshot: `/workspace/scratch/4e3a8a89dfc7/review111-source`.
- Independent build directory: `/workspace/scratch/4e3a8a89dfc7/build111-independent`, absent initially. No author/shared foundation `.olean` files were reused.

Actual execution command:

```sh
python3 /workspace/scratch/4e3a8a89dfc7/review111-source/proofs/contributions/agent-111/exact-length-residues/check.py \
  /workspace/scratch/4e3a8a89dfc7/runtime/lean --module All \
  --build-dir /workspace/scratch/4e3a8a89dfc7/build111-independent \
  --output-dir /workspace/scratch/4e3a8a89dfc7/p196/proofs/contributions/agent-111/exact-length-residues/review/independent-full
```

Checker exit code0; all17 recorded compiler/probe commands exited0. Each source compilation used `-j1 -DElab.async=false`, with `LEAN_PATH` pointing only to the new build directory. Total command time:95.104 seconds.

| Module | Audited theorem declarations |
|---|---:|
| `OuterBlock` | 10 |
| `ModulusSplit` | 5 |
| `PeriodExistence` | 20 |
| `ModularSpan` | 9 |
| `ArithmeticCRT` | 4 |
| `Lychrel196Research` | 787 |
| `PalindromeDigits` | 73 |
| `PairWeights` | 38 |
| `DigitPools` | 36 |
| `ResidueOrbit` | 9 |
| `Saturation` | 10 |
| `ExplicitBound` | 3 |
| `All` | 0 |

Compiler: `Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)`; native executable SHA-256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. This host used the recorded readlink adapter; ordinary Linux can run native Lean directly. Executable/shared/preload-library fingerprints and actual probe outputs are in [verification.json](independent-full/verification.json).

Axiom union: `propext`, `Classical.choice`, `Quot.sound`, with no `sorryAx` or `Lean.ofReduceBool`. Kernel-safe custom axiom declarations are rejected.
Thirteen compiler-generated unsafe implementation helpers are separately recorded; none enters an audited theorem's transitive axiom list.

After completion, pinned snapshots, build sources, `.olean` files, every compiler log, both generated axiom-audit sources, and compiler fingerprints were rechecked and matched. Per-file Git provenance/hashes: [source-pin.json](independent-full/source-pin.json); final checks: [REBUILD_PROVENANCE.json](independent-full/REBUILD_PROVENANCE.json); actual logs: [logs/](independent-full/logs/).

`verification.json` SHA-256：`52b9cf34cb9853cb8e8603340212f5b997a8772fda7782f7973f883fa2612d73`。

The executor handled environment/checker work and did not write these mathematical sources. This is an independent automated rebuild from frozen Git objects using the same official Lean implementation and frozen project checker, not external human peer review. It covers source reproducibility and axiom audits, not decimal Lychrel existence or infinite palindrome avoidance by196.
