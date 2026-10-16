# Agent 107：原表恰好枚举全部有限转移可达状态

状态：**LEAN-CHECKED**；独立重建与语义复核由主代理安排。

源码：`proofs/Agent107TransducerReachable.lean`。

冻结 SHA-256：
`7e4dc0b05d441f27bc56f96d3c1cdc7fafa59393b5456fc1ad7feaa93180681b`。

## 精确范围

`Agent107.FoldedTransducer.Reachable` 是归纳定义：两个允许的初态
`initial h`（`h ≤ 1`）可达；从可达状态走一步实际 `Transition` 后仍可达。
它表达有限转导前缀可达性，不额外要求终止接受，也不表示数值反加轨道的不变性。

最终定理：

```lean
Agent107.FoldedTransducer.reachable_iff_mem_states (s : State) :
  Reachable s ↔ s ∈ Table.states
```

结合已验证的 `Table.states_length = 46` 和 `Table.states_nodup`，这精确建立
“从两个初态出发，沿实际转移可达的状态恰好有表中的 46 个”。

正向使用归纳法，复用 `Table.starts_mem` 与 `Table.states_closed`。
逆向为每个原始状态 ID 提供明确的父节点和输入符号：前两个状态直接应用初态
构造子，另外 44 个状态各应用一次 `Reachable.step`，相应具体 `Transition`
用普通 `by decide` 交给 Lean 内核检查。Python 仅发现见证，不承担证明。

## 见证与验证

`generate_reachability.py` 从已冻结表 JSON 按原边顺序计算 BFS，验证三个表
源码哈希未变，并保存 `bfs-witnesses.json`。每个见证记录原状态、初态编号、
父节点、输入、原边索引、输入序列和计算深度。这里没有单独宣称已形式化最短路
距离或统一路径长度界。

```sh
python proofs/contributions/agent-107/folded-transducer-20261016/reachability-development/generate_reachability.py
python proofs/contributions/agent-107/folded-transducer-20261016/reachability-development/verify_reachability.py
```

第二条命令在平台正式 `require_escalated` 批准环境执行；官方 Lean 4.19.0
使用 `--trust=0 -j1 -DElab.async=false`。首轮约 1.3 秒成功，退出码 0。
`attempt-01.json` 和对应日志保存实际命令、源码/对象哈希及完整公理审计。

全部 49 个导出定理已审计：46 个具体可达见证无公理；
`mem_states_reachable` 仅依赖 `propext`；`reachable_mem_states` 和最终等价
仅依赖 `propext, Quot.sound`。没有 `sorryAx`、自定义公理、编译器求值公理或
`Classical.choice`。没有失败尝试，也没有改动三份冻结表模块。

本子任务未执行 Git 提交、推送或外部发布，由主代理统一处理。
