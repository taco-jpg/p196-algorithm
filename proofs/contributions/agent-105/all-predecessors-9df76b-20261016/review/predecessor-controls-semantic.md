# PredecessorControls 的非作者语义审查

审查者：Agent105 / runtime105。源码作者：scope105。结论：PASS，无修改建议。

冻结源码 `Agent105PredecessorControls9df76b.lean` 的 SHA-256 为
`2286e7580ef72d122db6a8c9368aeb4d16aba21d69045ead33e1b9e3ce9378c2`。

## 读取结论

`small_targets` 同时给出目标 1、2、10 的实际 Canonical 证书及完整 predecessors 列表等式，依次为 []、[1]、[5]。规范证书通过已有 `canonicalDigits_iff` 和有限 digit-list 的 bounded/positive-last 化简取得；没有把未经证明的数位函数当作实际目标。与已检查的 `mem_predecessors` 组合后，这些列表等式确实给出全部正整数解。目标 10 保留源 5 的单中心溢出和低 payload 为零边界。

`two_width_121` 同时证明 `Canonical 121 (digitFn [1,2,1]) 3`，以及实际计算顺序下的完整列表：
`[110,92,83,74,65,56,47,38,29]`。
首项来自三位源分支，余下八项来自两位溢出源分支。它检查两个源宽同时出现及多个数字拆分，没有宣称新的全局最大值，也没有把两个 profiles 等同于两个整数。

四个列表等式均由 kernel `decide` 证明；作者先前的 #eval 只用于确定实际列表顺序，不是定理前提。源码只有两条命名 theorem，无新增数学公理或本模块自定义计算映射。

## 证据与独立性

已读取作者 `controls/kernel-attempt-002/result.json` 与完整 compile.log；官方 Lean 4.19.0，`--trust=0 -j1 -DElab.async=false`，exit 0，约 0.491 秒。两条公理输出都只含 `propext`、`Quot.sound`。当前源与该次成功源码快照逐字一致。

本轮是非作者源码语义读审，没有重复编译，也没有修改 controls。初次 canonicalDigits 的 Decidable 实例失败由作者保留在 attempt-001；本审查不把那次失败列为接受证明。

审查者编写过 WordFiber 及部分较早依赖；本报告只独立审查这两条 scope105 controls 的结论、规范目标连接和证据范围，不将本人依赖称作独立自审对象。
