# Checkpoint02 独立陈述与语义审阅

审阅者为 Agent #100 的 `runtime_setup` 子代理。四份冻结数学源的精确 SHA256、Git blob 和53个命名 theorem 陈述保存在 `registry.json` 与 `statement-inventory.json`。Dynamics/Defect 作者为 `groupii_dynamics` 子代理；Safety/DoubleGate 由父代理提供。审阅与最终独立构建不修改这四份源。

## 一、七核心域与有限返回

Dynamics 的22个接口沿用 checkpoint01 的独立陈述审阅：`r≥1`、`1≤p≤4`、`5≤u≤8`、`5≤v≤6`、`u+v≤13`；分量宽度 `2r+6`、整字宽度 `2r+7`。返回分量出现六列核心 `1,4u−19,4v−18,4v−18,4u−19,1`。`r=1` 处第一邻列是 `4p+1`，该边界由实际移位相加定义和专门定理保留。两步结论只使用已从域推导的 carry/no-overflow，不假设返回等式。

## 二、Safety 的8个接口

- `initial_admissible`、`middle_admissible` 为沿用初始字和新中间字建立标准 `Admissible` 条件，未把可实现性本身加入域假设。
- `initial_not_bad` 用中心系数 `2v≥10` 排除全小系数分支，用外系数 `p≤4` 排除外系数11分支。`middle_not_bad` 相应使用 `2u+1≥11` 和 `2p≤8`。这两个排除条件调用原 `BadWord` 定义，未改写坏字集合。
- `numeric_middle` 和 `numeric_return` 对任意满足指定 canonical representation 和原 pair sums 的普通整数建立一步/两步实际 `orbit` 表示，并保留原宽度。桥接使用原 `representation_next`。
- `numeric_two_step_safety` 通过原 `PairDelayBridge.palindrome_iff_bad` 证明正时间1和2的输出不回文；没有把初始时间0纳入已证明安全范围。
- `realized_safe_gate` 调用已保留的 `valid_word_realizable` 解除 canonical realization 前提：域中每个参数存在真正的有限正整数实现。该存在命题同时给出两次正时间安全和两步返回表示；不是无限整数提升或 Lychrel 存在结论。

## 三、DoubleGate 的15个接口

组合起点固定为旧门参数 `(p,u,v)=(1,1,6)`。其两步返回字与第二组初始参数 `(4,5,5)` 的字逐列相同；`first_domain` 和 `second_domain` 分别核验两个不同域。旧域不能封闭并不意味着新域不能接续，这里的接续由明确等式完成。

`handoff_word` 本身是定义等式（`rfl`）。真正的时间演化拼接另由 `whole_handoff`、`component_four_return`、`whole_four_return` 等陈述完成。`iterPairs_add` 是迭代合成恒等式；`two_steps_from_matching` 只要求长度 `L` 内的表示相等，使用保留的有限前缀 carry congruence 推导，不要求两函数在无关尾部全局相等，也不把 q 的 carry 作为额外假设。

时间3的整字与分量分别由 `whole_three`、`component_three` 给出。`time_three_overlap_fails` 在列 `r+1` 证明二次修复前再次出现差1，故四步结果不是把四个单步都假设成重叠律后机械拼接。

普通整数结论 `numeric_handoff`、`numeric_four_return` 通过 canonical bridge 与 `orbit_add` 连接；`numeric_four_step_safety` 的量词明确是 `1≤k≤4`。`realized_safe_double_gate` 对每个 `r≥1` 给出正整数实现和这四个正时间输出的安全性，且给出时间4的完整 pair word。它不声称时间5以后安全、第四步后回到同一原形状、或可无限重复双门。

## 四、Defect 的8个接口

比较字使用导入的 `DelayedOverlapGate.redundant = 2 * initial`。它的中心为 `4v≥20`，所以明确证明 `redundant_not_admissible`；该字只用于系数/归一化误差比较，没有被当作真实 admissible pair word。

以实际 `middle − redundant` 的有符号系数差比较，五个核心值为 `(1,−19,−18,−19,1)`。归一化后数字差为 `(1,1,0,−1,−1)`，在宽度 `2r+7` 内反对称。两个比较字的 no-overflow 均有证明，`seam_cancels_next` 再调用原 `columnSum_eq_of_antisymmetric_difference` 得出下一 reflected sum 相同。这里是归一化后的精确抵消，没有把未归一化系数差当作数字差。

`returnedComponent_not_same_shape` 用索引 `r` 处新增系数1，排除在同一 spacer/宽度下等于任意旧四核心 `component r p' u' v'`。陈述只需要 `r≥1`，不依赖新域；其结论是当前形状族不闭合，未扩张成对所有可能再编码、变宽度或后续更新机制的否定。

## 五、独立普通整数与索引控制

`independent_decimal_controls.py` 不调用 Lean，也不读取 `.olean`。它直接用精确 Python 整数实现普通十进制反转相加；对每个被测试的对称 pair word 给出两种合法数字分拆，并核对 nonzero leading digit、初始 pair sums 和实际输出。

- Group II：全部28组 `(p,u,v)`、六个 spacer `1,2,3,5,10,20`、两种分拆，共336个实际整数实现；检查一步/两步 pair word、安全性与宽度保持。
- Defect：168组参数；逐列核对有符号系数差、归一化数字差、反对称、下一步抵消、两比较字无溢出、冗余字超过18及新形状见证。
- DoubleGate：六个 spacer、两种分拆，共12条实际四步轨道；检查时间2交接、时间3中间字、时间4返回字、分量四步返回、时间3重叠失败、四个正时间非回文和宽度。

全部2,976项命名断言通过，完整参数、整数轨道与结果保留在 JSON 中。此处有限样本只辅助检查模型解释与索引；任意正 `r` 及任意 canonical realization 的结论依赖实际 Lean 证明。

## 六、接受范围与历史失败

53个导出接口包含支持引理、定义等式和组合接口，不能直接称作53项独立发现。全闭包 theorem constant 审计另含历史依赖与自动辅助声明，应单独报告。

只有 registry 精确固定的最终四源及其独立 freshbuild/full-axiom audit 属于本 checkpoint 的有效验证。所有失败 development attempts 均标记 `EXCLUDED_FROM_ACCEPTED_VALIDATION`，保留历史但不计为 PASS；作者成功 attempts 也与本次独立验证分开。

审阅结论：未发现把旧域与新域混同、隐含排除最短间隔、用不可实现冗余字替代普通整数、正时间偏移一位、或从有限修复外推无限闭合的问题。最终执行状态与精确公理清单以 `result.json`、`named-endpoint-axioms.json` 和完整原始日志为准。
