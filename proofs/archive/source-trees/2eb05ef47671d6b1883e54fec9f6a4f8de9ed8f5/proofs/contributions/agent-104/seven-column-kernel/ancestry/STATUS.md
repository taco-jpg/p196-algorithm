# ActualAncestry 验证记录

接受源码：上级目录 `ActualAncestry.lean`。

SHA-256：`3d7c904ae0abbd6e3eb132959a7a0fae230725a49808a05653206787d1a8149e`。

## 精确结论和剩余有限前提

`actual_iterPairs_rank` 对普通数位模型的真实变宽 `iterPairs` 轨道证明：
终点投影被树查询为秩 `r` 时，实际步数不超过 `r`。
投影是 `wordPrefix q (min L 7)`；短词保留完整长度。
归纳中，每条长源边使用已证明完备的 `actual_mem_prefixPredecessors`；
每条短源边使用涵盖全部 10467 个合法短源的精确排除条件。

`short_target_unique`、`target_project_mem_initialWords` 证明目标最后前驱的所有投影属于有限族：
一个完整六列词 `[7,3,9,9,3,7]`，加上全部 10000 个 `[7,3,9,a,b,c,d]`，其中四个自由数字均为 0–9。
此结论没有给目标位数、内部数位或零串长度加上界。

`canonical_last_step_initial` 使用已经发表的 `PalindromeBridge`，把普通数值最后一步连到该有限初始族。
`ancestry_bound39_of_finite_checks` 因而推出全部正整数来源的实际祖先深度不超过 39。
`no_196_739_palindrome_of_finite_checks` 再结合内核验证的时间 0–100 非回文检查，推出普通 196 轨道的全时 739 回文排除。

后两项**仍明确带有以下三个有限证书前提**，本文件不把这些前提视为已完成的实例：

1. `CheckedRows tree (longPred 7)`：树的每一行检查了完整可执行逆枚举。
2. `∀ s ∈ shortWords, lookup tree (nextWord s) = none`：全部合法短源的实际像都不在树内。
3. `∀ p ∈ targetInitialWords, checkInitial tree 38 p = true`：全部初始投影均有已存秩且秩不超过 38。

这里没有把祖先深度上界直接作为前提；从有限检查到普通整数结论的组合已经证明。
这只涉及 739 回文目标族，不是完整 196 猜想。

## 作者编译

Lean 4.19.0，`ancestry/long-rows-base.log` 和 `ancestry/attempt_002.log` 的退出码均为 0。
`attempt_002.lean` 是接受源码的完整快照。

```bash
LEAN_PATH=/workspace/scratch/7649db1e242c/build104-base:/workspace/scratch/7649db1e242c/build104-inverse:/workspace/scratch/7649db1e242c/build104-cert \
  /workspace/scratch/7649db1e242c/toolchain/lean \
  -o /workspace/scratch/7649db1e242c/build104-ancestry/LongRowsBase.olean \
  proofs/contributions/agent-104/seven-column-kernel/certificate/LongRowsBase.lean
LEAN_PATH=/workspace/scratch/7649db1e242c/build104-ancestry:/workspace/scratch/7649db1e242c/build104-base:/workspace/scratch/7649db1e242c/build104-inverse:/workspace/scratch/7649db1e242c/build104-projection:/workspace/scratch/7649db1e242c/build104-short:/workspace/scratch/7649db1e242c/build104-cert:/workspace/scratch/7649db1e242c/build104-palindrome \
  /workspace/scratch/7649db1e242c/toolchain/lean \
  -o /workspace/scratch/7649db1e242c/build104-ancestry/ActualAncestry.olean \
  proofs/contributions/agent-104/seven-column-kernel/ActualAncestry.lean
```

六项导出公理审计只有 `propext`、`Classical.choice`、`Quot.sound`。
没有 `sorryAx` 或新公理。接受源码没有 `sorry`、`admit`、`axiom`、`native_decide`。
作者使用各子模块的已编译产物；独立 clean 构建由另一个审计代理处理，结果另行记录。

`attempt_001.lean` 与 `attempt_001.log` 保留首次失败：短目标唯一性证明中的常量下标和 `min 6 7` 未显式归约，`omega`/`simp` 未闭合目标。
第二稿为对称性事实加上明确 `q 0 = q 2` 等类型，并把六列目标化为 `segment q 0 6` 后通过。
失败草稿不是接受证明链。
