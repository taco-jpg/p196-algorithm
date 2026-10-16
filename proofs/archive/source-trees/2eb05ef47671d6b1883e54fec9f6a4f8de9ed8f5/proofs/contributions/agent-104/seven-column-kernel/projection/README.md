# 实际全字到长前缀的核验记录

证据类型：**形式定理**。日期：2026-10-15。Lean 4.19.0。

主源码为上一级 `ActualPrefix.lean`，命名空间 `SevenColumnProjection`。

已核验的精确结论：

- `actual_forwardPrefix`：对任意 `Admissible L q` 与 `k ≤ L`，以唯一实际内侧高进位 `DecimalDigits.carry q (L-k)` 运行纯 List 的确定性 `forwardPrefix`，恰等于 `nextColumns q L` 的长度 k 前缀。
- `actual_forward_admitted`：上述实际进位属于 `{0,1}`，所以两个高内侧进位的枚举包含真实输出。
- `actual_longCompatible`：再要求 `0 < k`，真实前缀满足 `PrefixInverse.lean` 中的逐列逆向关系。
- `actual_mem_prefixPredecessors`：真实来源前缀确实属于目标前缀的可执行逆向枚举结果；没有把真实转移的覆盖性作为额外前提。
- `wordPrefix_eq_range_map`：所用递归 List 前缀等于 `(List.range k).map q`，可直接与短来源模块对接。

全部结论只要求 `k ≤ L`，包括两端前缀重叠和 `k=L`。后者实际高内侧进位为零。七列是取 `k=7` 的特例。低端与高端进位均从同一完整实际字 `q` 计算，不假定其独立。

`forwardPrefix` 与 `verify_certificates.py:forward_prefixes` 的单一进位分支逐项对应：先低端正序进位，后高端逆序进位；不增位逐项相加，增位将高端数字序列前接 1，再按低端序列长度截断相加。`highDigits_segment` 对该逆序计算给出实际进位与实际数位的同时等式。

## 复现

在仓库根目录，令 `P196_LEAN` 为 Lean 4.19.0 可执行程序（本次使用环境兼容包装器 `/workspace/scratch/7649db1e242c/toolchain/lean`），运行：

```sh
P196_LEAN=/path/to/lean P196_BUILD=/tmp/p196-projection-build \
  bash proofs/contributions/agent-104/seven-column-kernel/projection/verify.sh
```

源码依赖为 `proofs/research/continuation/LychrelDigitSums.lean`、同目录的 `PrefixInverse.lean`。依赖和主源码的 SHA-256 见 `verification.json`。`base-build.log`、`inverse-final-build.log` 和 `final-build.log` 保存本次构建及传递公理审计输出。

最终七项打印审计只出现普通逻辑公理 `propext`、`Quot.sound`，以及关系桥接的 `Classical.choice`；没有 `sorryAx`、`Lean.ofReduceBool`、`native_decide` 或自定义公理。

## 历史尝试与范围

`draft-01` 至 `draft-03` 保留了保留字命名错误和增位尾部的化简顺序错误；`draft-04` 是确定性正向投影的首个成功版本。`draft-05` 的逆向桥接因递归 carry 提前展开而失败；`draft-06` 是全部桥接通过的版本。失败日志中的 `sorryAx` 是 Lean 对未完成声明的错误恢复产物，**不属于最终核验结果**。所有原始草稿和日志均保留，未以成功版本替换。

本模块不证明短来源分支，不核验五份有限秩证书，也不推出完整 P196 猜想。它完成的是实际完整字与长前缀图之间的精确语义连接。可重建的 `.olean`、编译目录与工具链属于运行基础设施，不纳入研究成果。
