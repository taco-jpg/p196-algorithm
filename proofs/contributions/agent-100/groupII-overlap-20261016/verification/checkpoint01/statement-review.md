# Checkpoint01 独立陈述审阅

审阅者：Agent #100 的 `runtime_setup` 子代理。作者：`groupii_dynamics` 子代理。审阅对象为冻结的 `proofs/Agent100GroupIIDynamics.lean`，SHA256 `07b8c8d8c0c6fa4aefa1034272464531e27353586066651fd5dda55408d3091c`。本记录属于独立代码/数学陈述审阅；Lean 构建状态与公理结果另见本目录 `result.json` 和原始日志。

## 陈述与实际含义

`Agent100.GroupII.Domain` 明确要求 `r ≥ 1`、`1 ≤ p ≤ 4`、`5 ≤ u ≤ 8`、`5 ≤ v ≤ 6`、`u + v ≤ 13`。它是此模块的新域，与导入的 `DelayedOverlapGate.Domain` 不同。模块沿用后者的 `initial`、`component`、`fiveWord`、`shiftOne` 等定义，但没有改写依赖源码。七个允许 `(u,v)` 值由 `domain_seven_cores` 的单向蕴含陈述给出；该定理不应单独描述为对全部 `(r,p,u,v)` 域的充要刻画。

22 个显式 theorem 均进入 registry 的 endpoints 与逐项陈述 inventory。其中主要动力学结论是：

| 接口 | 已陈述的结论 | 适用范围 |
| --- | --- | --- |
| `component_next` | 原分量一步变成参数加倍的分量 | `Domain`；宽度 `2r+6` 内全部列 |
| `component_double_next` | 加倍分量下一步变成六列核心的 `returnedComponent` | 同一 `Domain`；宽度 `2r+6` 内全部列 |
| `initial_next` | 初始重叠字一步变成新 `middle` | `Domain`；宽度 `2r+7` 内全部列 |
| `middle_next` | 新 `middle` 下一步等于 `shiftOne returnedComponent` | 同一 `Domain`；宽度 `2r+7` 内全部列 |
| `component_two_step_return` | `iterPairs` 两步后宽度仍为 `2r+6`，列等于 `returnedComponent` | 任意满足域的正 `r` |
| `whole_two_step_return` | 整字 `iterPairs` 两步后宽度仍为 `2r+7`，列等于返回分量的移位叠加 | 任意满足域的正 `r`，包括 `r=1` |
| `intermediate_overlap_fails` | 一步结果不等于两个一步分量的移位叠加 | `Domain`；通过列 `r+1` 证实 |

`returned_is_overlap` 是定义展开后的等式（`rfl`），作用是公开命名接口；两步演化的实质内容在 `middle_next` 与两个 `two_step_return` 定理中，不能把定义等式单独当成动力学证明。

## 边界、截断与假设检查

- 所有动力学定理均显式保留 `r ≥ 1`；没有声称 `r=0`。`r=1` 不被排除，也没有隐含升级成 `r≥2`。
- 返回分量的内部六列是 `1, 4u−19, 4v−18, 4v−18, 4u−19, 1`。`domain_core_bounds` 明确给出涉及 Nat 减法的正下界，域内不会因截断减法改变这些预期数值。
- `returned_first_neighbor` 精确陈述 `returned ... 1 = 4p + (if r=1 then 1 else 0)`，因此最短间隔处新增核心系数与外侧系数相加。返回整字使用真实 `shiftOne` 定义，不使用会遮蔽碰撞的条件覆盖布局。
- 原分量、加倍分量、初始整字与中间整字的 carry/no-overflow 均在本模块从 `Domain` 推导。两步定理通过既有 `two_steps_of_explicit_columns` 接口连接这些结论，没有额外假设 carry profile 或最终等式。
- 点态列等式只要求声明宽度以内的索引；两个 `iterPairs` 主定理同时证明宽度保持。返回函数本身在定义域外的值不被伪装成原始无限整数动力学。
- `intermediate_overlap_fails` 的命题是对全列等式的否定。证明选取合法索引 `r+1`，利用 `middle` 的系数 `2u+1` 与加倍重叠初始式的系数 `2u` 得到矛盾。

## 独立有限辅助控制

`independent_decimal_controls.py` 从 pair-column 系数构造精确十进制整数，读取其普通十进制数字并与反射数字相加以计算下一 pair-column 字；没有调用 Lean 或读取开发 `.olean`。它覆盖全部28组 `(p,u,v)` 与 `r ∈ {1,2,3,5,10,20}`，共168例、每例8项断言：初始重叠、分量两步、整字两步、中间缝隙差1、短间隔边界相加、返回分量对称。全部1,344项通过。完整逐例记录保留在 JSON 中。

这些有限控制检查数学模型与索引解释，不能代替任意 `r` 的 Lean 定理证明。

## 本 checkpoint 不包含的结论

此次冻结源只证明条件性的有限 pair-column 两步演化。它不证明返回字仍属于原四核心形状或原参数域，不提供可无限迭代的更新规则，不证明无限重叠律、无限安全、不回文轨道、Lychrel存在性或196的全轨道结论。普通整数实现、安全性与双门结果应分别审核后续 Safety/DoubleGate 模块；新 Defect 模块也不在本次七模块闭包中。

结论：未发现 source 条件被弱化、`r=1` 被遗漏、返回形状被误当原形状，或有限结论被写成无限结论的陈述问题。最终 Lean 状态以实际完整构建收据为准。
