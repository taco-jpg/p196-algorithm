# Agent #107：完整 folded transducer 认证

当前任务：`agent107-folded-transducer-20261016`。认领提交
`fe5a0ef1760a0afa936168ac1cfc52987d28b451`；原始主干
`98d59927ad89c42f438ea857ec5750a0df3b91db`。

本包将原 `fst_graph` 的两个初态、完整进位转换与中心终止规则接到
`FoldedDecimal.nextColumns`、实际 `nextWidth` 和普通整数的规范表示。
共享定义 `Agent107TransducerDefs.lean` 已在官方 Lean 4.19.0 下编译。
完整路径、具体图表和输出对应尚在开发，当前整体状态为 **WIP**。

`baseline/` 保存独立基础重编译与七个复用接口的公理/依赖审计。
基础源为 `Lychrel196Research__c696e0ea3db39d92.lean`，Git blob
`c6c1f5441c54a36f2d82b3ef78dff1ccdbc5a506`；声明来源不变。
工具链为 Lean 4.19.0，release commit `6caaee842e94`；新证明排除
`sorry`、新增数学公理和 `native_decide`，记录实际标准逻辑公理。

路径的唯一性只涉及从零到半宽的有限状态序列，不涉及未读取的函数尾部。
原无溢出分支使用的 Int `-1` 哨兵保留；奇长溢出的额外输出 pair 单独保留。
此任务不提供安全闭合语言实例，也不证明 196 或其他固定种子的无限不回文性。

编译器、`.olean`、依赖复制目录和运行缓存是可再生成基础设施，不纳入源码发布；
实际证明源码、失败尝试、日志、精确来源和独立审查证据按阶段完整保留。
