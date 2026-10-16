# 第三门检查点：独立陈述范围审查

审查者：Agent #100 的 `runtime_setup` 子代理；不是这三份数学源码的作者。本文审查三份冻结源的陈述及证明结构。完整独立 clean build 与全公理审计的实际结果另见 `result.json`，本文的静态判断本身不冒充编译 PASS。

## 源码身份与依赖

- `Agent100ThirdGateBoundary.lean`：SHA256 `7f6992f08e7f7b75e0a609d54a64f9ac7c2b80344296761be111e740ef48a96c`，8 个具名定理。
- `Agent100ThirdGateNumeric.lean`：SHA256 `b1ff8e06cf63d34a935f826b806dbd02fcf3808b83511e062f91a3d64da7e3db`，12 个具名定理。
- `Agent100ThirdGateControls.lean`：SHA256 `44bb4ea1256cf0b5b6c42183de1b477a723c1d1e76e0cfe5273956b483367749`，8 个具名定理。
- 最终 roots 为 Numeric 与 Controls，预期精确闭包为六个原始依赖、GroupII Dynamics/Safety/DoubleGate 与三个 ThirdGate 模块，共十二模块。GroupIIDefect 不在此 import 闭包内。

## Boundary：两列前提确实支持两步外列结论

`Admissible L q` 的完整含义保持原样：正宽度、正外列、有效前缀上每列不超过 18、前缀对称，以及奇数宽度中列的偶性。它不要求无限函数尾部为零，也不把超出 18 的冗余系数词当成真实 pair word。

`penultimate_carry_low/high` 用前缀对称性把倒数第二列化成第 1 列。`q 1 ≤ 8` 保证末前进位为 0；`10 ≤ q 1` 结合 admissibility 的上界保证末前进位为 1。阈值 9 被有意留空；这两个定理没有误写成穷尽 dichotomy。`2 ≤ L` 使使用的索引位于有效前缀，Nat 截断减法经过明确的算术等式处理。

`sixteen_low_one_step` 的前提为外列 16、第 1 列 `z`、`z ≤ 1`。第一步发生 overflow，宽度增长一位，前两列为 `(7, 7+z)`。`sixteen_high_one_step` 把第 1 列换为 `16+z`，第一步前两列为 `(7, 14+z)`。两者都从 admissibility 推导实际末进位，没有要求整个 tail 的形状。

`next_outer_seven_low/high` 在外列 7 时证明 no overflow，宽度保持；第 1 列的低、高区间分别决定下一步外列 14、15。因此 `two_steps_outer_fourteen/fifteen` 的两步结果均为宽度 `L+1`，外列分别为 14、15。该结论只确定宽度及外列，并不声称其余所有列与某个固定模板一致。

## Numeric：时间四到时间六连接到实际家族

`componentOrbit` 从原 `component r 1 1 6`、宽度 `2r+6` 开始；`wholeOrbit` 从 DoubleGate.initial、宽度 `2r+7` 开始。`iterPairs` 从时间 0 起计数，与普通 `orbit n k` 的精确步数一致。

`spacerBit r` 在 `r=1` 时为 1，其余为 0。返回 component 的前两列是 `(16, spacerBit r)`；返回 whole 的前两列是 `(16, 16+spacerBit r)`。最短 spacer 的相邻列叠加被明确保留，而非默认 `r≥2`。`component_four_front/whole_four_front` 使用已冻结 DoubleGate 的四步返回定理，并仅在有效前缀的索引 0、1 读取结果。

`component_six_boundary/whole_six_boundary` 使用 `iterPairs_admissible` 保证时间四状态满足 Boundary 的合法性输入，以已证的 `iterPairs_add` 拼接四步和两步。最终 component 的实际宽度为 `2r+7`、外列 14；whole 的实际宽度为 `2r+8`、外列 15。`sixth_widths_compatible` 精确证明后者比前者宽一位，所以失配并非宽度取错造成。

## 失败见证位于有效前缀

`finiteWord L q` 在 `i<L` 时取 `q i`，其余归零；这是形成有限 component 的 `shiftOne` 时明确去掉无语义尾部的操作。`third_overlap_fails` 否定的是整个有效 whole 前缀都等于该有限 component 的一步移位和。反证仅取 `i=0`，它位于实际宽度内部，得到 `15=14` 的矛盾。它不依赖任何尾部值，也不声称两个无限函数逐点不等的更强特定形式。

结论排除了同一初始 `(1,1,6)` 家族、同一 component 演化、同一 `shiftOne` 重叠方式在时间六的第三次两步修复。它没有排除其他 component、重编码、移位、时间或宽度变换下的后续表示。

## 普通整数的量词与非空性

`numeric_six_boundary` 对所有自然数 `n`、数字函数 `d` 和 `r≥1` 成立，只要求 `Canonical n d (2r+7)` 及该有效前缀的 pair sums 等于初始词。通过既有 `iterPairs_representation`，给出实际普通反转相加 `orbit n 6` 的 canonical 表示、宽度 `2r+8`、外列 15，以及全部有效前缀与 symbolic wholeOrbit 的逐列一致性。

`numeric_third_overlap_fails` 对同样的任意实现传递有限前缀失配。其 `∃ e` 是该实际整数的 canonical 数字表示，不是引入另一个自由的整数轨道。`realized_six_boundary` 从已有 `realized_safe_double_gate` 提取每个 `r≥1` 的一个正整数初始实现，消除前提可能完全无实例的疑问。

这三条 Numeric 定理没有声称时间五或六非回文；外列 15 也没有被当成任意更强的无限安全证书。现有四步安全性来自旧 DoubleGate 结论。没有无限 renewal、Lychrel 存在性或 196 结论。

## Controls：三个边界疑问有具体、合法的核验对象

`admissible_from_finite_check` 将 `Fin L` 上的列上界、对称性、中列偶性，以及单独的正宽度/正外列假设转回原 `Admissible`。这保留全部 admissibility 条件；不把有限检查误认为没有宽度限制的无限列检查。

第 1 组控制使用宽度均为 5 的词 `[7,9,0,9,7]` 与 `[7,9,10,9,7]`，数字按最低有效列先列出。它们都有相同的 `(7,9)` 前两列，但下一步外列分别为 14 与 15。两词的 admissibility 与实际 `nextWidth/nextColumns` 均纳入定理结论；`neighbor_nine_not_determined` 用这两个合法见证否定单靠该前缀确定下一步外列的全称命题。这精确说明遗漏的阈值 9 依赖内部进位，并不声称所有 9 前缀都有这两种延拓。

第 2 组控制使用 `[16,2,18,18,2,16]`，宽度 6，第二列 `z=2`。其两步结果宽度为 7、外列为 15。`low_bound_two_false` 因而否定把原低分支假设 `z≤1` 放宽到 `z≤2` 后仍统一得外列 14 的全称结论；没有把一个反例推广成所有 `z=2` 都为 15。

第 3 组控制使用 `[16,16]`，满足最小允许宽度 `L=2` 的高分支。第一步宽度 3、前两列 `(7,14)`；第二步仍宽度 3、外列 15。`ordinary_97_control` 完整给出普通整数 `97 → 176 → 847`，每个数字函数 canonical，并核验初始全部两列和后两步全部三列。这里的具体 witness 不被冒充为 `(1,1,6)` 主家族的实例；它验证的是局部 Boundary 高分支的最短宽度及普通十进制语义。

具体计算使用 kernel `decide`，没有 `native_decide` 或不受审计的外部求值证明。Controls 的有限例子是已编入 Lean 的定理和反例，不替代 Numeric 关于所有 `r≥1` 与所有普通实现的泛化证明。

## 审查结论与验证边界

未发现三模块的 `r=1` 遗漏、前缀与无限尾部混淆、时间偏移、假设偷换或有限结论夸大。静态审查覆盖全部 28 个新增具名接口；完整 source pins、公理集合和独立 clean-build 结果由同目录 registry、statement inventory、result 和 evidence 记录。

开发失败与作者自检日志保留为历史，均不代替本检查点的独立 fresh build。source baseline 字段只记录实际执行时的 Git base，不隐含三份新源当时已经包含在该提交中。
