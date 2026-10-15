# Agent #107：任意分块的接缝响应

本包补齐既有书面 `SEAM_RESPONSE.md` 的全词响应与普通整数算术连接。
研究基线为 `251a7fa1584f45db8cac0a9e6db899bd39b38ced`；任务认领已在
`p196/coordination` 提交 `e6970a06d286e919bf8e506cd92cfc72d2d739f2` 发布。
既有三块质量定理和局部进位敏感性属于引用依赖，本包不重新声称其发现。

## 当前证据状态

**INDEPENDENTLY-REVIEWED。** 七个证明模块与 `All.lean` 已分别完成作者及独立审查者的
全新空目录重建，五个仓库依赖均从源码重新编译。全部66个公开定理的两份传递公理
报告一致，仅有 `propext`、`Classical.choice`、`Quot.sound`，不是无公理证明。
没有 `sorryAx`、`native_decide` 或 `Lean.ofReduceBool` 依赖。
计数是审计覆盖元数据，不是独立重大结果的数量。

作者证据见 [verification.json](verification.json) 和 [compile.log](compile.log)；
独立签署见 [review/REVIEW.md](review/REVIEW.md)，包括独立执行、假设检查和源码指纹。
完整数学源码已发布于 `1d40f7c156e77dc9894975c9dc583ca92202ff5f`；两次重建的源码
SHA-256 均与此版本一致。[PR #11](https://github.com/taco-jpg/p196-algorithm/pull/11)
准备集成。此状态不声称已进入默认分支或共享接受构建。

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
- `PairClosure.pair_agrees_iff_no_activity` 及其 numeric 版本：同一整词宽度上的
  原始分块配对表达式精确，当且仅当所有接缝缺陷为零；反射不能抵消非零缺陷。
- `PartitionDefect.defect_sum_eq_seamMass`、`raw_mass_eq_isolatedMass`：在 cut 与
  boundary 描述同一分块的明确兼容条件下，连接全局缺陷与逐块初始九串质量，
  并连接原始总质量与各块独立归一化质量。

形式化命名空间均以 `Agent107.` 开头；`All.lean` 收录整包证明模块。
真实数字的前提不可删去后仍称为普通整数的标准表示；非标准输入仅有指定宽度的形式系数含义。
泛型 `q : Nat → Nat` 的 `nextWidth` 不自动等于普通十进制位数；numeric 接口证明此桥。
响应式以有限支持系数函数表达。逐块质量连接已经证明；没有额外声称未列出的
多项式对象或任意块列表的整式 AST 等式。
这些结论只控制一次更新，没有证明接缝缺陷会永久再生，也没有解决196或十进制Lychrel存在性。

## 复现与证据保留

固定工具链为 `proofs/research/lean-toolchain` 指定的 Lean 4.19.0，依赖仅为Std
及本仓库已经存在的源码。完整构建入口为本目录 `check.py`。
在仓库根目录，使用已安装的官方 Lean 4.19.0 执行：

```sh
python3 proofs/contributions/agent-107/partition-seam-response/check.py lean \
  --build-dir /tmp/p196-agent107-clean \
  --output-dir /tmp/p196-agent107-report
```

构建目录必须尚不存在或为空。检查器隔离 `LEAN_PATH`、重编所有依赖、显式导入
全部七模块，逐个执行公开定理的 `#print axioms`，并复核源码、对象、日志、编译器
及依赖指纹。Private helper 的依赖由其使用者的传递审计覆盖。
本环境的实际命令、官方编译器指纹与 readlink 兼容层见 [environment/](environment/)；
普通 Linux 不需要该兼容层。作者与独立构建使用相同官方运行时、不同空构建目录，
没有声称使用不同 Lean 实现或外部人工同行审查。

`development/` 保留成功及失败尝试的源快照、退出码、编译日志和源码指纹。
该目录不在接受构建中；失败草稿保留其失败身份，不构成已证明声明。
编译产物、复制的依赖目录和工具链安装属于可重建基础设施，不作为研究源码发布。
禁止 `sorry`、新增假设公理或 `native_decide`；传递公理审计仅允许显式记录的
`propext`、`Classical.choice`、`Quot.sound`。
