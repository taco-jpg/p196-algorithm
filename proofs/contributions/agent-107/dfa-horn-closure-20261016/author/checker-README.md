# Agent107DFAChecker 作者验证记录

本模块由 Agent #107 的 `lean_runtime` 子代理编写并实际验证。记录中的执行者没有写成 root，也不把作者验证称为独立审查；独立清洁重建与数学审查由未参与编写本模块的 `semantic_review` 另行完成。

## 冻结接口

源码为 `proofs/Agent107DFAChecker.lean`，SHA256：

`a9a411034cf44aeb9752c85246d05140067b88c2c00b5c62651d423af1be2238`

Git blob：`941bf379c7798398bf82c66cce3dcb88828c17f7`。

唯一直接导入为冻结的 `Agent107DFA`，其源码 SHA256 为：

`d0fe8accc9d80110230ea3b4061f554d8d9d9dc5b8ea1a89f44e7d2fc977969e`。

主要端点位于 `Agent107.FoldedDFA` 命名空间：

```lean
def checkHorn {N : Nat} (M : DFA N)
    (rb : State → Fin N → Fin N → Bool) : Bool

theorem checkHorn_iff {N : Nat} (M : DFA N)
    (rb : State → Fin N → Fin N → Bool) :
    checkHorn M rb = true ↔ Horn M (fun s a b => rb s a b = true)
```

另有 `boolImplies_iff`、`allFin_iff`、`checkStarts_iff`、`checkEdges_iff`、`checkTerminals_iff`，分别解释每一层实际布尔计算。

## 检查器及证明范围

`checkStarts` 对字面列表 `[0, 1]` 执行 `List.all`。`checkEdges` 对原 872 条 `Table.edges` 执行外层 `List.all`，每行对 `List.finRange N` 执行两层 `List.all`。`checkTerminals` 对原 251 条终止行使用相同的 `Fin N × Fin N` 枚举。布尔蕴含直接定义为 `!a || b`。这些是有限模板列表；实际执行可以按 `List.all` 的语义提前返回 false，并非每次都强制求值全部模板。

终止条件严格保留 `M.run b r.extra.toList`，包括 `extra = some 0` 时真实读取一个零符号，随后检查 `r.outputCenter`。没有加入字母表范围限制，没有枚举无限的 `State` 类型，也没有用 `decide` 包裹整个 Horn 命题。

反射证明逐层使用真实的 `List.all_eq_true` 和 `List.finRange`/`List.mem_ofFn` 枚举完备性；初态列表与 `h ≤ 1` 的等价性由自然数推理完成。`allFin_iff` 本身包括空 `Fin 0` 情形，正式 DFA 的正性要求由 `M : DFA N` 携带。

## 实际执行与失败保留

`checker-run.py` 在每轮编译前把精确源码复制到新的 `checker-NNN/` 目录，记录源码 SHA256、Git blob、依赖对象 hash、真实命令、UTC 时间、exit code、耗时及 stdout/stderr hash。

第一轮 `checker-001` 的编译 exit 1。原因是初态反向反射在使用 `omega` 前没有化简不可能的空列表成员分支。该轮完整源码与原错误日志保留；Lean 因未完成证明在失败日志中打印的 `sorryAx` 不是通过的证明，未用作任何成功依据。第二轮只补入空列表分支消去，实际编译与审计均 exit 0。

成功轮 `checker-002` 使用官方 Lean 4.19.0，实际命令：

```text
lean --trust=0 -j1 -DElab.async=false -o Agent107DFAChecker.olean Agent107DFAChecker.lean
lean --trust=0 -j1 -DElab.async=false CheckerModuleOriginAudit.lean
```

编译实测 0.422745 秒，来源审计实测 3.608922 秒。公共六个反射端点已逐项 `#print axioms`；完整模块来源审计还覆盖了辅助定理和定义方程，总计 20 条：无公理 6 条，仅 `propext` 5 条，`propext` 加 `Quot.sound` 9 条。没有 `Classical.choice`、其他禁止公理或本模块 unsafe implementation 占位。

本轮作者编译复用 root 对 `Agent107DFA` 的显式 trust-zero 对象以及任务一独立审查/基础构建的依赖对象；精确路径和 hash 已记录在 `execution.json`。没有把这种依赖复用写成一次从空目录重编全部闭包。独立审核须另据 `semantic_review` 的记录。

成功对象位于 `/tmp/agent107-runtime/task2-checker-build/Agent107DFAChecker.olean`，其 SHA256 为 `54a641755a7c68ba269ffd7af8f70225709c14a6190050a2e331e2f661526a0d`。公开证据只保留源码、脚本、日志和 JSON，不复制工具链二进制。

所有本模块作者证据的文件 hash 见 `checker-FILES.json`，冻结信息见 `checker-freeze.json`。
