# Agent 107：原始有限折叠转导表的 Lean 验证

状态：**LEAN-CHECKED**，等待独立空目录重建与语义复核。

这组文件精确保留原始 Python 的 46 个状态、872 条边和 251 条终止记录。
它证明表内转移与终止记录的正确性和完备性，不构成任何不回文不变语言、
无限轨道或 196 猜想的证明。

## 源码与复现

`generate_tables.py` 只抽取并执行原始 `C`、`D`、`fst_graph` 函数的 AST，以及
weighted 文件原始 `TERMS/TS/NW` 顶层节点，不导入求解器，也不改原算法。
它另行枚举所有表内状态与 `q=0..18`、`bn=0..1`、全部可能中心，逐项验证
生成表的内容和顺序。原始整数状态 ID 保存在 `extracted-tables.json`。
来源 Git blob、SHA-256 和生成源哈希保存在 `extraction-manifest.json`。

```sh
python proofs/contributions/agent-107/folded-transducer-20261016/table-development/generate_tables.py
python proofs/contributions/agent-107/folded-transducer-20261016/table-development/verify_tables.py
```

第二条命令须在当前平台正式 `require_escalated` 批准环境执行。它使用未经
修改的官方 Lean 4.19.0，固定 `--trust=0 -j1 -DElab.async=false`。
默认重编译三个模块；显式 `--reuse-checked` 仅在各模块源和对象哈希均匹配时
复用已成功检查的对象。独立审查应从空输出目录与固定依赖源码重建。

## 模块与已证明接口

- `Agent107TransducerTablesData.lean`：完整字面表、46/872/251 长度定理、
  状态表无重复与两个初态的成员资格。
- `Agent107TransducerTablesChecks.lean`：46 组小证书，分别证明边和终止行的
  正确性、全部有限输入选择的完备性、行内无重复与固定源状态。
- `Agent107TransducerTables.lean`：用通用 `nodup_blocks` 组合行内无重复和
  不重复状态键；提供 `edge_sound`、`transition_complete`、`states_closed`、
  `terminal_sound`、`terminal_complete`、`edge_mem_iff`、`terminal_mem_iff`。

公共边完备性量化任意目标状态，使用实际 `Transition` 的约束归约到有限
输入与后继高位进位；终止完备性量化任意 `Option Nat` 中心，并从 `Terminal`
推出中心界限。奇数宽度溢出的额外符号被保留在 `TerminalRow.extra`，且与
`terminalExtra` 精确相等，没有丢弃这个额外输出。

本组表模块建立初态属于表、表对实际转移封闭、所有表内合法转移与终止均被
准确列举；它本身未证明每个列举状态可达。这个方向现已由单独的
`Agent107TransducerReachable.lean` 补齐，证据见同任务的
`reachability-development/`。

## 实际验证证据

`attempt-02.json` 记录三个模块全部成功编译：Data 约 3.1 秒、Checks 约
116.3 秒、公共 Tables 约 13.4 秒。`attempt-03.json` 与对应日志逐一审计
全部 **292 个导出定理**：96 项无公理，184 项仅 `propext`，12 项仅
`propext, Quot.sound`。没有 `Classical.choice`、`sorryAx`、自定义公理或
编译器求值公理。辅助定理数量是证书分块数量，不是独立数学发现数量。

首次单体边表无重复检查在约 101.9 秒时被信号 `-9` 终止，没有 Lean 错误
诊断。失败记录保留在 `attempt-01.*`；现用分行证明和普通 Lean 组合定理
完成同一结论，不降低证明标准。

首轮失败源码当时没有另存快照，其临时同名文件被后续拆分模块覆盖。发布前已
通过 `reconstruct_attempt01.py` 从保留生成器明确逆转后续编辑，事后重建为
`attempt-01-source.lean`。重建 SHA-256 严格等于原失败执行记录中的
`5119a7e3b109bea4404805350eb4913fbb561411e27fffe65f1804b4dc22440c`。
`attempt-01-reconstruction.json` 明确说明这是事后重建及其步骤，不能称作
当时已经保留的源码快照；原失败日志未修改。

冻结源哈希与依赖观测记录见 `source-freeze.json`。本子任务未执行任何
Git 提交、推送或外部发布，由主代理统一处理。
