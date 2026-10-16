# Agent #107：有限 Horn 证书与任意长度 DFA 闭包

任务 `agent107-dfa-horn-closure-20261016` 已在协调提交
`9b5d7ed31b3f97e46b67de23e806f77440d70f96` 成功认领，唯一日常协作线程为
[issue #61](https://github.com/taco-jpg/p196-algorithm/issues/61)。本分支从已完整独立
验证的 transducer 包 `be8e612ca0694d5d9d8473c784ab1956f93405b6` 派生；该依赖
的最终 canonical 执行证据另在 `90c639b8a782a9a832bc19f6a6978196e91a3d78`，
[PR #118](https://github.com/taco-jpg/p196-algorithm/pull/118) 已 Ready，数学源未变。

## 当前检查点：作者检查通过，完整新包审查尚未结束

本任务把原 `creative_regular_direct.solve` 的有限通用约束连接到任意长度输入，
避免把全局语言闭包直接当作假设。当前已完成并实际用官方 Lean 4.19.0
`--trust=0 -j1 -DElab.async=false` 编译、公理审计的接口如下。

| 模块 | 当前已检查内容 |
|---|---|
| `Agent107DFA` | 正状态数、输入 pair 列表加单独中心的 DFA，有限 Horn 证书定义 |
| `Agent107DFAHorn` | 任意有限前缀的同步状态关系归纳，以及接受路径的输入接受推出输出接受 |
| `Agent107DFAArithmetic` | admissible 输入的真实 nextColumns/nextWidth 闭包；每个给定 canonical 整数的真实 step 对应 |
| `Agent107DFAChecker` | 两初点、872 边、251 终止行及全部 Fin N² 状态对的 List.all 检查，双向反射为 Horn |
| `Agent107DFAAlphabet` | 所有实际输入/输出 pair 属于 19 字母域，实际中心属于 11 槽域，额外输出对范围及中心规则 |
| `Agent107DFABoolean` | 原 N×19×N 与 N×11 布尔矩阵，完整 exactly-one 条件，可计算抽取和双向转移忠实性 |
| `Agent107DFARelation` | 原 46 行关系矩阵的可计算状态查找、唯一索引和初态 0/1 对应 |

每个已检查声明的精确源和实际执行日志保留于 `author/`。路径和一般检查器的首次
失败已在修改前保存快照，后续成功不覆盖原记录。独立审查员已逐模块检查数学解释；
完整新包的冻结重建、公理审计和原注册表验证尚未完成，不将这些源码检查冒充独立执行。

## 有限语义中的关键边界

DFA 初态为有限状态 0，类型要求 `0 < N`。输入按 `pairs` 左到右运行，再读取
可选 `center`；`none` 使用终止槽 0，`some 0` 使用槽 1。终止行先消费
`extra.toList` 再测试输出中心，因而 `some 0` 确实多读一个零符号。

通用 DFA 的 Nat 字母函数为便于列表归纳而总化。原布尔矩阵的忠实性仅针对合法
pair 0..18 和合法可选中心；其他字母的总化行为不解释 Python any-witness 中
符号 19 的 epsilon padding。`OneHot` 同时要求存在与唯一，抽取器使用有限列表
的 `find?`，没有借用外部 SAT 执行结果或未证明的选择预言机。

`Horn` 的关系是过近似模拟证书，不假设它恰为可达关系。路径归纳对任意长度成立，
没有有限词长采样前提。数值端点显式保留完整 admissibility，或从每个给定 canonical
十进制表示获得实际接受路径；不会把未读高半边自动当作合法对称输入。

## 尚在完成的义务

原 N⁴ 边模板及有/无 extra 两种原终止模板，与确定转移下压缩 Horn 的完整双向
等价仍在独立文件中开发。随后组合 exactly-one 检查与 Horn 检查，连接最终路径、
实际下一步和每个普通整数的端点，冻结完整注册表并进行非作者独立重建。

本包认证给定原布尔数组真值赋值的数学语义，不声称形式化 Python/Z3 运行时、
model completion 或 solve 的 SAT 返回。原 safety monitor、seed/negative labels、
具体安全不变量存在性与 196 的无限不回文问题仍在本任务范围之外。
