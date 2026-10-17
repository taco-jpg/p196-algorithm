# Agent107DFARelation 作者验证记录

本模块由 Agent #107 的 `lean_runtime` 子代理编写并实际验证；作者编译不冒称独立审查。独立数学审查及清洁重建由 `semantic_review` 另行完成。

## 冻结源码与接口

源码：`proofs/Agent107DFARelation.lean`。

SHA256：`64d8606e1592428cb184b40e5cd2650175c78411a046a68c72f2a24a78a2b748`。

Git blob：`c5df077e095550189168b1452796a5679ed92405`。

唯一直接依赖为 `Agent107DFA`，其冻结源码 SHA256 为 `d0fe8accc9d80110230ea3b4061f554d8d9d9dc5b8ea1a89f44e7d2fc977969e`。

命名空间：`Agent107.FoldedDFA.Encoding`。

```lean
abbrev TableIndex := Fin Table.states.length
def stateAt (i : TableIndex) : State
def stateIndex? (s : State) : Option TableIndex

def liftRelation {N : Nat}
    (rawR : TableIndex → Fin N → Fin N → Bool)
    (s : State) (a b : Fin N) : Bool
```

`stateAt` 使用原列表的 `get`；`stateIndex?` 直接使用可执行的 `Table.states.finIdxOf?`，返回原列表首次匹配的有界索引。它不是非计算性的选择函数。已有 `Table.states_length` 证明列表长度为 46；`Table.states_nodup` 与已验证的 `nodup_get_injective` 保证行索引唯一。

主要证明：

- `stateIndex?_stateAt i`：读取原第 i 行再查找，返回 `some i`。
- `stateIndex?_eq_some_iff s i`：返回 `some i` 当且仅当 `stateAt i = s`。
- `stateIndex?_eq_none_iff s`：返回 `none` 当且仅当状态不属于原表。
- `state_mem_iff_exists_stateAt` 与 `state_mem_iff_exists_index`：原表成员恰好对应有限行索引。
- `liftRelation_stateAt rawR i a b`：提升到 State 后读取原第 i 行，结果精确等于 `rawR i a b`。
- `liftRelation_of_not_mem`：原表外状态的提升关系为 false。

## 原初态行的核对

实现前直接读取了原 `Agent107TransducerTablesData.lean` 的状态列表，并与 `Agent107TransducerDefs.lean` 的 `initial` 定义核对：

| 原行索引 | 状态字段 `(overflow, low, high, delay, started)` | 对应初态 |
|---|---|---|
| 0 | `(0, 0, 0, -1, false)` | `initial 0` |
| 1 | `(1, 0, 1, 1, false)` | `initial 1` |

`initial0Index`、`initial1Index` 的值分别为 0、1。`stateAt_initial0Index`、`stateAt_initial1Index` 以 `rfl` 核验原表顺序。对应的查找定理、`liftRelation_initial0`、`liftRelation_initial1` 以及 `_start` 特化，精确连接原 `R[0][0][0]` 与 `R[1][0][0]`；DFA 的 `M.start` 正是值为 0 的有界索引。

## 实际编译与完整来源审计

每轮在编译前保存精确源码快照；`relation-run.py` 记录实际执行者、命令、UTC 时间、源码 hash/blob、依赖对象 hash、exit code、耗时、stdout/stderr hash。

`relation-001` 编译 exit 1：标准库第一匹配证明中的前驱索引本身是 `Fin`，首版再次从其数值重建 Fin 后，`omega` 未将投影认作同一个值。首轮源码和错误日志完整保留。第二轮直接使用原 Fin 索引的相等性，再由严格不等式推出矛盾。失败日志因不完整目标出现的 `sorryAx` 没有作为任何通过依据。

`relation-002` 使用官方 Lean 4.19.0：

```text
lean --trust=0 -j1 -DElab.async=false -o Agent107DFARelation.olean Agent107DFARelation.lean
lean --trust=0 -j1 -DElab.async=false RelationModuleOriginAudit.lean
```

编译 exit 0，实测 0.564318 秒；模块来源审计 exit 0，实测 2.902822 秒。按实际模块来源审计全部 23 条定理，包括辅助证明和定义方程：

| 公理集合 | 条数 |
|---|---:|
| 无 | 8 |
| `propext` | 1 |
| `propext`、`Quot.sound` | 1 |
| `propext`、`Quot.sound`、`Classical.choice` | 13 |

没有其他公理依赖，也没有本模块 unsafe implementation 占位。此模块的索引反射证明确实包含允许的 `Classical.choice` 依赖，未隐藏或声明为无 Choice。

作者构建复用 root 已显式 trust-zero 编译的 DFA 以及任务一已检查依赖对象，具体路径/hash 见 `execution.json`。这不是从空目录重编全部闭包；后者由独立审查提供。成功对象位于 `/tmp/agent107-runtime/task2-relation-build/Agent107DFARelation.olean`，SHA256 为 `1b0b2be57e9b6e59f027c5728069c7a826b6e6fe8eee3a97912ab93376bb6b9e`。

公开作者证据只包含源码、脚本、日志和 JSON。`relation-freeze.json` 记录全部公共端点；`relation-FILES.json` 列出所有本模块作者证据的字节数和 SHA256。
