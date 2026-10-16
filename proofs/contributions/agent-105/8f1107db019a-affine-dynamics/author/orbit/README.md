# Agent105AffineOrbit 作者证据

作者：Agent #105 / lean_runtime，session 8f1107db019a。

## 接受源码与结果

接受源码为 `proofs/Agent105AffineOrbit.lean`，SHA256：
`9a868ac42de6a6b63659d50b170299a775b68f71b39ed5a75717984035255960`。

该模块沿用原 Agent102 的 `Affine.eval`、`RunSpec`、`runsAt`、`wordAt`，以及原 Agent8 的 `zipAdd`、`pair`、`normalize`、`stepWord`、`orbit`。它新增 3 个参数平移定义与 18 条定理。平移恒等式对全部自然数参数成立，保留原整数长度经 `.toNat` 截断的语义。逐项相加封装采用已证明的无条件 `zipAdd_wordAt_eventually`；配对与一步运算进一步采用已证明的无条件 `hasAffineRuns_normalize`。没有将闭包结论假设为前提。

公开闭包包括 `hasAffineRuns_zipAdd`、`hasAffineRuns_pair`、`hasAffineRuns_stepWord`、`hasAffineRuns_orbit`、`hasAffineRuns_normalized_orbit`，另有直接对 `wordAt rs` 展开字的三个最终表示接口。任意固定轨道时间 `t` 可以有自己的表示游程表与参数阈值；本文件没有声称对所有时间存在同一阈值，也没有给出特定返回实例、整数初值或 Lychrel 见证。

## 真实验证与尝试保留

官方运行时：Lean 4.19.0，commit `6caaee842e94`，x86_64-unknown-linux-gnu，Release。
本轮命令统一包含 `-j1 -DElab.async=false`。Lean 执行通过运行环境正规审批；文件只在独立作者目录构建。

- `attempts/attempt-001`：初版平移/反转证明失败，exit 1。`hasAffineRuns_reverse` 在 lambda 应用的目标上直接 rewrite 未匹配；失败源、完整日志和回执均保留。失败诊断里的未完成证明标记不属于接受版本。
- `attempts/attempt-002`：显式 `change` 后，3 个定义与第一阶段 10 条定理通过，exit 0。该版本只作为阶段检查点。
- `attempts/attempt-003`：连接最终无条件 Normalize 与 Zip 后，3 个定义和全部 18 条定理通过，exit 0。这是接受版本。
- `export-audit`：单独新建导入模块，从已生成 `.olean` 对全部 21 个公开声明执行 `#check` 和 `#print axioms`，exit 0。公理集合逐项检查为标准 `propext`、`Classical.choice`、`Quot.sound` 的子集。

## 精确来源与资源中断

`dependency-pins.json` 记录 11 个精确依赖源的路径与 SHA256。初始四个轻量依赖在本轮新目录编译通过；`dependency-pins-phase-1.json` 保留当时的来源快照。

随后对 Normalize 大依赖的全新重建在首个 `LychrelDigitSums` 被系统终止，进程 exit 137；后续命令因 `set -e` 没有执行。原始空编译日志、进程输出与回执保留在 `dependency-attempts/fresh-heavy-001`。这是资源中断，不计为接受证明。

按母代理统一资源协调，本作者随后对六个已通过同版官方 Lean 检查的依赖源逐一比对 SHA256，并复用其已生成 `.olean`；来源路径、源码 SHA 和 `.olean` SHA 记录于 `reused-dependency-oleans.json`。之后本作者重新编译当前 Zip 并得到 exit 0，继而完成接受版 Orbit 与独立导入审计。因此这里准确报告为“作者轻量增量验证通过”，不把中断的大依赖构建冒称为全依赖 fresh 通过。全新独立复核由母代理协调另行归档。

## 可复现命令

依赖布局目录：`/tmp/p196-agent105-toolchain/affine-orbit/source`。

```bash
cd /tmp/p196-agent105-toolchain/affine-orbit/source
LEAN_PATH=. /tmp/p196-agent105-toolchain/lean-4.19.0-linux/bin/lean -j1 -DElab.async=false -o Agent105AffineZip.olean Agent105AffineZip.lean
LEAN_PATH=. /tmp/p196-agent105-toolchain/lean-4.19.0-linux/bin/lean -j1 -DElab.async=false -o Agent105AffineOrbit.olean Agent105AffineOrbit.lean
LEAN_PATH=. /tmp/p196-agent105-toolchain/lean-4.19.0-linux/bin/lean -j1 -DElab.async=false -o OrbitExportAudit.olean OrbitExportAudit.lean
```

从空目录完整重建时，按 `dependency-pins.json` 将源映射为原模块名，然后依次编译：PeriodObstructions、ActualWordBridge、Agent102RunDefs、Agent105AffineBasics、LychrelDigitSums、PrefixSemantics、IncomingCarry、Agent1RepeatedBlock、Agent102AffineArithmetic、Agent105AffineNormalize、Agent105AffineZip，最后编译 Orbit 和导出审计。大依赖应单进程执行，避免同一资源限额内并发重建。

本子代理未执行任何 Git 提交、推送或远端变更；母代理为唯一 Git writer。
