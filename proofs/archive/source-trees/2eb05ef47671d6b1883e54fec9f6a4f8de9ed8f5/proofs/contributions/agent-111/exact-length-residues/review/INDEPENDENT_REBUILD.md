# Agent111 独立干净重建记录

**结论：PASS。** 固定提交的 `All.lean` 导入闭包从全新空目录重建成功：13 个源码模块，1004 条 theorem 声明（包含 private 和编译器生成的辅助定理），全部完成实际 `#print axioms` 审计。

- 固定源码提交：`c3192d5bf2962298bcb2bb209a0947f657e8a7e5`。
- 来源分支：`research/agent-111/s20261015-1534`；仓库：`https://github.com/taco-jpg/p196-algorithm.git`。
- 获取方式：对该提交执行 `git archive`，精确导出基础文件、贡献顶层 Lean 文件及冻结的 `check.py`。未从 live 工作树读取数学源码。
- 归档 SHA-256：`4bebb8633421501d1299a941330fa8aed8ab9a11f2ba21a46c506fbbc04d6135`。
- 检查器 SHA-256：`9fea73de4ea0497a1747e0b635bd1ea5d74d15b7479f89ae1351272f7093a9af`。
- 独立源码快照：`/workspace/scratch/4e3a8a89dfc7/review111-source`。
- 独立构建目录：`/workspace/scratch/4e3a8a89dfc7/build111-independent`；开始前不存在。没有复用作者或共享基础构建的 `.olean`。

实际执行命令：

```sh
python3 /workspace/scratch/4e3a8a89dfc7/review111-source/proofs/contributions/agent-111/exact-length-residues/check.py \
  /workspace/scratch/4e3a8a89dfc7/runtime/lean --module All \
  --build-dir /workspace/scratch/4e3a8a89dfc7/build111-independent \
  --output-dir /workspace/scratch/4e3a8a89dfc7/p196/proofs/contributions/agent-111/exact-length-residues/review/independent-full
```

检查器退出码为 `0`；记录的 17 次编译器/探针命令全部退出 `0`。每次源码编译使用 `-j1 -DElab.async=false`，`LEAN_PATH` 仅指向新的构建目录。累计命令时间 95.104 秒。

| 模块 | 已审计 theorem 声明数 |
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

编译器：`Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)`。原生 executable SHA-256 为 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`。本宿主使用已记录的 readlink 路径适配层；标准 Linux 可直接运行原生 Lean。详细 executable、共享库、预加载库指纹和实际探针输出均在 [verification.json](independent-full/verification.json)。

公理并集为 `propext`、`Classical.choice`、`Quot.sound`，没有 `sorryAx` 或 `Lean.ofReduceBool`。安全的自定义 axiom 声明会被拒绝。
另记录 13 个编译器生成的 unsafe 实现辅助声明；它们没有进入任何已审计 theorem 的传递公理清单。

完成后再次核对固定快照、构建源码、`.olean`、每份编译日志、生成的两份公理审计源码和编译器指纹，全部一致。逐文件 Git 来源与哈希见 [source-pin.json](independent-full/source-pin.json)；最终复核结果见 [REBUILD_PROVENANCE.json](independent-full/REBUILD_PROVENANCE.json)；实际编译器日志位于 [logs/](independent-full/logs/)。

`verification.json` SHA-256：`52b9cf34cb9853cb8e8603340212f5b997a8772fda7782f7973f883fa2612d73`。

执行者负责环境与检查器，没有编写本批数学源码。这是从冻结 Git 对象开始的独立自动化重建，使用同一官方 Lean 实现与冻结项目检查器；不构成外部人类同行审查。结果覆盖源码可重建性与公理审计，不延伸为十进制 Lychrel 存在性或 196 无限避免回文的证明。
