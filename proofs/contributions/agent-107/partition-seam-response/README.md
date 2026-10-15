# Agent #107：任意分块的接缝响应

本包补齐既有书面 `SEAM_RESPONSE.md` 的全词响应与普通整数算术连接。
研究基线为 `251a7fa1584f45db8cac0a9e6db899bd39b38ced`；任务认领已在
`p196/coordination` 提交 `e6970a06d286e919bf8e506cd92cfc72d2d739f2` 发布。
既有三块质量定理和局部进位敏感性属于引用依赖，本包不重新声称其发现。

## 当前证据状态

五个证明模块已分别在 Lean 4.19.0 下编译；全部依赖也已从源码重建。
整包空目录重建、最终全导出声明公理审计与独立复核仍在进行。
在 `verification.json` 与 `review/` 的完成记录出现前，不应将整包标为
`INDEPENDENTLY-REVIEWED` 或 `INTEGRATED`。默认分支未被本贡献修改。

## 精确范围

- `SeamCoefficients.coefficient_response`：对任意有限系数词和任意切分，
  真实有限输出满足逐系数 `D = E + previous K - 10*K`，包括终端进位和零延拓。
- `SeamRuns.seamDefect_on_block`、`block_defect_sum`：每个真实块的缺陷恰为
  实际输入进位乘以初始九串的指示函数；允许整块全九，并另处理空块终端传递。
- `SeamMass.actual_step_seam_mass`：任意切分的独立归一化原始质量，等于
  实际 `digitSum(step n)` 加九倍缺陷总和；质量相等恰好对应所有缺陷为零。
- `PartitionMass.actual_step_partition_collision_mass` 与
  `actual_step_partition_pair_mass`：任意有限连续分块的数字质量损失系数为9，
  实际下一配对词的质量损失系数为18。所有进位来自实际整词，允许重复边界。
- `PairResponse.numeric_pair_response`：在实际溢出决定的宽度下反射完整修正，
  并通过 `Canonical` 和 `representation_next` 连接普通整数的下一次反转相加。

形式化命名空间均以 `Agent107.` 开头；`All.lean` 收录整包证明模块。
真实数字的前提不可删去后仍称为普通整数的标准表示；非标准输入仅有指定宽度的形式系数含义。
这些结论只控制一次更新，没有证明接缝缺陷会永久再生，也没有解决196或十进制Lychrel存在性。

## 复现与证据保留

固定工具链为 `proofs/research/lean-toolchain` 指定的 Lean 4.19.0，依赖仅为Std
及本仓库已经存在的源码。完整构建入口为本目录 `check.py`（正在完成）。
`development/` 保留成功及失败尝试的源快照、退出码、编译日志和源码指纹。
编译产物、复制的依赖目录和工具链安装属于可重建基础设施，不作为研究源码发布。
禁止 `sorry`、新增假设公理或 `native_decide`；传递公理审计仅允许显式记录的
`propext`、`Classical.choice`、`Quot.sound`。
