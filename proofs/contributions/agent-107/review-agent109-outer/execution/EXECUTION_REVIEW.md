# Agent109 outer bridge：独立 kernel 执行审查

**执行结论：PASS；最终进程退出码 0，无未解决的执行义务。** 本报告只签署下述源码、依赖来源、实际编译及公理审计。定理语义由本次独立审查的 `status_audit` 另行处理；不在此声称 P196、无限安全或一般终止性。

## 受审版本与独立性

受审 checkout：`/workspace/scratch/64704429df15/review109-source107`，detached commit `b2374410d427beb78fc601ee81cf15e34a1ac934`。工作包为 `proofs/contributions/agent-109/outer-projection-bridge`。reviewer 只写本贡献的 `execution/`，未更改作者源码或进行 Git mutation。

reviewer 独立编写 `independent_kernel_audit.py`，没有执行作者 `build.sh`。实际启动命令为：

```text
cwd: /workspace/scratch/64704429df15/p196-review107
python proofs/contributions/agent-107/review-agent109-outer/execution/independent_kernel_audit.py
```

执行 session 为 `28665`。新建且初始为空的 scratch build 目录为 `/workspace/scratch/64704429df15/agent107-outer109-clean-syq1jnqb`；九份源码经逐字节验证后复制进去。整个过程只有一个 Lean 进程，逐模块顺序运行，未复用任何 project `.olean`。九模块均使用 `lean -j1 -DElab.async=false -o Module.olean Module.lean`；随后独立 audit 同样使用 `-j1 -DElab.async=false`。`LEAN_PATH` 仅指向该 build 目录，清除环境中的 `LEAN_SYSROOT`，对 launcher 的 `LD_PRELOAD` 设为空，再由已知 wrapper 加入指定 readlink shim。

保留的准确执行脚本为 [executed_harness.py](agent107-outer109-clean-syq1jnqb/executed_harness.py)，SHA-256 `559eb6e6ff383035753c1a1431a904a59e8a99e2bafc7251b5464f791318b065`。原脚本在执行后未修改。完整 argv、cwd、退出状态、耗时、stdout/stderr 内容及各自 hash 均在 [manifest.json](agent107-outer109-clean-syq1jnqb/manifest.json)，该清单 SHA-256 为 `39584bff0fd9e33d591b53751dda7a348e4abc506b4f82543e87743039e6038a`。

## 实际构建结果

九输入依赖闭包与作者 build.sh 一致；各 import 在编译前均已由本次 fresh run 产生相应依赖文件，标准库来自下述工具链。九模块和额外完整审计全部退出 0，总计 Lean 编译/审计记录时间 103.394 秒。

| 模块/步骤 | 退出码 | 秒 |
|---|---:|---:|
| `TemplateStep` | 0 | 5.785 |
| `LychrelDigitSums` | 0 | 67.409 |
| `PeriodObstructions` | 0 | 4.351 |
| `Compat` | 0 | 0.473 |
| `ReturnCertificate` | 0 | 3.015 |
| `OuterFinite` | 0 | 19.155 |
| `OuterBounds` | 0 | 0.684 |
| `OuterBridge` | 0 | 1.604 |
| `OuterCompat` | 0 | 0.251 |
| `audit-all-exported` | 0 | 0.667 |

`OuterCompat` 也单独生成了本次 build 的 `.olean`，随后额外审计通过 import 使用该产物。没有用既有作者 build log 替代执行。

## 编译器与可信运行环境

- Lean：`Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)`。
- 官方原生 release binary：`/workspace/scratch/64704429df15/toolchain/lean-4.19.0-linux/bin/lean`；SHA-256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`。
- wrapper SHA-256：`6cb7e26f9000b57e81f17c46d4b8bd2b564a379394e38a2c0e3918b2efa84609`。
- 已有 readlink-only shim SHA-256：`100718efe84a5c605d4752eadf9d9f6b14f38d5adbc82ce00407d378f4d9973d`。
- 该工具链 `Std.olean` SHA-256：`7d3771da25b893da62564bf8198487ff28f01af5cbd410be88d493a4921b2bb1`。

已读取 shim C 源码：它只将当前进程 `/proc/<PID>/exe` 的 readlink 请求重定向为 `/proc/self/exe`，用于本 host 的执行文件路径兼容；没有更改 Lean proof/kernel 操作。审查依赖该指定官方二进制及其本地标准库，没有从源 bootstrap Lean 自身。

**移植限定：** 准确执行 harness 固定了 Linux release binary digest，并强制检查这份 host 编译的 shim digest；所以它不是无需修改即可在任意架构/普通 Linux 上执行的通用 launcher。普通 Linux 不需要该 shim，可直接用同版官方 Lean，独立空目录、相同九源码及额外 audit 重放；相应 portable 命令应与本次实际已执行命令区分。这里没有声称执行过第二种环境，也没有为文档移植再运行相同证明。host workaround 源码已由 root 放在同一贡献体系的 `partition-seam-response/environment`。

## 来源、源码清洁性及排除项

九份工作树源码逐字节等于 `git show b2374410:<path>` 的提交内容。本次执行前后的 `git status --porcelain=v1 --untracked-files=all` 均为空，HEAD 始终为上述固定 commit。执行后再次验证当前源码、fresh snapshot 和最初源 hash 一致；另对所有 `.olean`、26 条 recorded command 的 stdout/stderr 文件完成 hash 复核，见 [POSTFLIGHT_INTEGRITY.json](agent107-outer109-clean-syq1jnqb/POSTFLIGHT_INTEGRITY.json)。

`OuterFinite.lean` 和 `OuterBounds.lean` 还与 commit `da4a1799b74b98b4199cdb224ea7a694b2657651` 的 `proofs/agent7/OuterFinite.lean`、`proofs/agent7/OuterBounds.lean` 逐字节比较，完全相同。比对直接使用 git object 内容，并非只接受作者给定 checksum。

全部九份源码进行去除嵌套注释和字符串后的代码扫描，未发现 `sorry`、`admit`、`native_decide`、`ofReduceBool`、新增 `axiom`、`implemented_by`、`unsafe`、`extern` 或 `debug.skipKernelTC`。有限检查的 `decide +kernel` 是本次重新编译的 kernel proof；没有使用 native evaluator shortcut。

| 输入模块 | SHA-256 |
|---|---|
| `TemplateStep` | `76ad132fec23f9da8733f72a6baf22c3dbfe68d402a8165766bd8d163549d2ed` |
| `LychrelDigitSums` | `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57` |
| `PeriodObstructions` | `83102a949036799a929ba72d74ce9d76bc2a11cb3adf61e0bc06b6013b22991a` |
| `Compat` | `73dca78232b0c2c048da4d1d182f84b31c0e95bab283fad603fd342bf38616e6` |
| `ReturnCertificate` | `b6d34e8fb031401171b517eef8a2d91222334a5745cc88329e0a2ad13db47058` |
| `OuterFinite` | `3376873da457c698850f604ddda82aeba3e67f4196e5c33d8142bed945c5f3f6` |
| `OuterBounds` | `75ed5831f0cc1e9c6016672ebef83cf0f46da279432b3694ba075627cb973a76` |
| `OuterBridge` | `d0fa857eb84573e3a5afab09c8e3fa0f82244fcc72ad5b5623298bbd0bc2099e` |
| `OuterCompat` | `56dea5ebfddc5dd31cbc951d38205c74be42e201b40eee622c71fe0df57e4a7c` |

## 全部公开目标定理的公理审计

重新枚举并显式审计四模块全部 23 个公开 theorem：OuterBridge 15 个、OuterCompat 1 个、OuterFinite 3 个、OuterBounds 4 个。目标模块没有 private theorem。作者 OuterBridge 文件只显式 `#print axioms` 了其中 6 个；本次额外加入未覆盖的 `normalize7_eq`、`kOf_eq`、`norm_digits_le`、`zipAdd_le`、`k_le`、`t_le`、`u_le`、`bounded_strip`、`outerIterate_eq`，没有将作者局部 audit 误称为完整 audit。

额外生成且实际执行的文件为 [IndependentOuterAxioms.lean](agent107-outer109-clean-syq1jnqb/IndependentOuterAxioms.lean)，完整输出为 [audit-all-exported.stdout.log](agent107-outer109-clean-syq1jnqb/audit-all-exported.stdout.log)。每个名字都有对应的 Lean axiom 报告，无缺漏。

- 5 个 theorem 无公理依赖；其中包括 `cap2_exits_by_seven`、`cap2_sharp_six`、`cap2_sharp_seven`。
- 1 个 theorem 只依赖 `propext`。
- 12 个 theorem 依赖 `propext` 与 `Quot.sound`。
- 5 个 theorem 依赖 `propext`、`Classical.choice`、`Quot.sound`。

总公理并集严格为上述三种允许的标准公理，没有其它 axiom、`sorryAx` 或 `Lean.ofReduceBool`。`actual_cap2_exit` 和 `lychrel_cap2_exit` 使用三者，因此不能把整个 bridge 描述成 axiom-free。其余五个项目依赖模块均重新编译并扫描；此处逐个公开名称审计的范围是指定四模块，所用传递证明依赖由 `#print axioms` 一并覆盖。

签署：Agent107 independent kernel-execution reviewer。一次 fresh sequential build 已完成，无执行层阻断项；语义及结论适用范围以独立 statement review 为准。
