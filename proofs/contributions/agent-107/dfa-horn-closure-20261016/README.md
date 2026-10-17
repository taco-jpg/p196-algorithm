# Agent #107：有限 Horn 证书与任意长度 DFA 闭包

任务 `agent107-dfa-horn-closure-20261016` 在 `p196/coordination` 中认领，日常协作线程为 [issue #61](https://github.com/taco-jpg/p196-algorithm/issues/61)。隔离分支：`research/agent-107/dfa-horn-closure-20261016T2203Z`。

## 当前远端发布状态

七个数学模块已发布，精确源码检查点为 `97fe2e595793a021f9cc73e3139ea90a3ac5f5e7`。本目录中的作者快照、编译日志、来源公理审计和失败尝试均保留。机器可读登记表是 `proofs/Agent107DFAHorn.registry.json`。

上一任务的转导器 PR #118 已在远端合并，合并提交为 `231b1ac8f816760dfbc247b74a371d7b58adbd5b`；因此旧版 README 中“PR #118 仍 Ready/等待集成”的文字已过时。当前 `main` 已继续前进至 `74a1c3922eb7af438fe40b23d2105ad07556e3f5`，本分支没有 main 写入槽。

## 已发布的 Lean 接口

| 模块 | 已检查内容 |
|---|---|
| `Agent107DFA` | 正状态数、有限列表运行、输入 pair 序列加可选中心的 DFA，以及有限 Horn 证书定义 |
| `Agent107DFAHorn` | 任意有限接受路径的前缀关系归纳；输入接受推出实际路径输出接受，无词长采样假设 |
| `Agent107DFAChecker` | 初态、所有 872 条边、251 条终止行和所有有限状态对的布尔检查；检查结果与 Horn 命题双向反射 |
| `Agent107DFAAlphabet` | 输入/输出符号小于 19，中心落在 11 个合法槽，终止额外输出对的边界 |
| `Agent107DFABoolean` | 原始 `N×19×N` 转移数组与 `N×11` 终止数组；每行 exactly-one、有限抽取及转移忠实性 |
| `Agent107DFARelation` | 原 46 状态列表的可计算唯一索引、原矩阵行映射及两个初态索引 |
| `Agent107DFAArithmetic` | 从有限 Horn 证书推出 `nextColumns/nextWidth` 的真实闭包，以及每个给定 canonical 整数表示的实际 reverse-add 下一步 |

关键语义边界仍然明确：`none` 中心编码为槽 0，`some 0` 编码为槽 1；终止行先消费 `extra.toList` 再检查输出中心。额外输出符号 19 的 epsilon padding 不被误当作正常输入字母。关系证书是过近似模拟关系，不要求它恰为可达状态关系。

## 验证状态，避免把报告说大了

作者对上述七个模块执行了官方 Lean 4.19.0，参数为 `--trust=0 -j1 -DElab.async=false`；逐模块公理审计日志在 `author/`。失败尝试保留，尤其 `checker-001` 与 `path-001`，后续成功快照未覆盖它们。`Agent107DFARelation` 的索引反射证明使用允许的 `Classical.choice`，没有将其隐藏为“无公理”。

本会话中已报告一轮独立干净重建通过：20 个模块、1,445 条定理常量（其中新增七模块 128 条），定理公理并集仅为 `propext`、`Quot.sound`、`Classical.choice`。但独立执行的完整原始日志尚未存入本目录，故注册表将该项标为“已报告通过，证据归档待补”，而不是用摘要冒充可复核日志。

**原仓库 canonical verifier 尚未在本任务最终发布提交上重跑。** 当前执行容器没有保留 Lean 4.19.0 可执行文件；这是真实环境限制，不是验证失败，也不构成通过。后续执行者需先检查可用工具链，再在精确分支头的干净检出中运行原验证器，记录源码提交、完整命令、退出码和公理报告；不可把早前转导器提交的 canonical PASS 当作本任务提交的 PASS。

本工作证明的是“给定有限 Horn/Boolean 证书可推出任意长度语言闭包和真实数值一步”的条件性结果。它没有证明某个具体安全证书存在，没有形式化 Python/Z3 的 SAT 求解过程，也没有解决 196 的无限不回文问题。
