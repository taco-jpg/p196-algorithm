# Horn 闭包的真实数值推论：作者检查

作者角色：Agent #107 委派的 `scope_scout`。独占源码：
`proofs/Agent107DFAArithmetic.lean`，仅导入冻结的 `Agent107DFAHorn`。

## 两个条件性结论

`horn_next_closed` 对任意宽度、任意 admissible 完整列和字，在有限 `Horn M R`
证书及输入 DFA 接受的前提下，给出真实 `nextWidth`、`nextColumns` 的折叠字接受。
它组合上一任务的 `actual_accepts`、`accepting_output` 与本任务的
`horn_accepting_output`，不重做数值转换证明。

`horn_canonical_step` 对每个给定 `Canonical n d L`，若其折叠列和字被 DFA 接受，
则存在真实 `Lychrel196.step n` 的 canonical 表示，宽度恰为
`nextWidth (columnSum d L) L`，且真实输出表示的折叠列和字仍被 DFA 接受。
此处直接复用上一任务的 `canonical_step_path`。

没有断言具体 Horn 证书存在，没有附加或假定 seed、安全语言、长期不回文结论。
若后续接入原 `FoldedDecimal.representedBy_closed`，应取
`A L q := Admissible L q ∧ M.accepts (foldPrefix L q)`，以原
`NormalizationBridge.admissible_next` 和 `horn_next_closed` 提供它要求的完整闭包
前提；本文件不重写该既有 wrapper。

## 冻结与实际执行

首次执行 `author/arithmetic-001` 于 2026-10-16 22:15:11 UTC 真实退出 0；无失败尝试。
执行前保存了完整源快照，实际命令与日志均在该目录。工具链为官方 Lean 4.19.0，
参数为 `--trust=0 -j1 -DElab.async=false`。两个端点显式公理审计均为：

```text
[propext, Quot.sound]
```

冻结源 SHA256：

```text
10c24e67d811fcda392de2e473cf907793da82a12d0fd5cfc4dc890b50b40169
```

依赖的冻结 Horn 源 SHA256：

```text
e443d30c868d50de911662b885354e53853b7802f415fc41a09ba2317b2974a7
```

这是导入先前冻结依赖 olean 的作者检查，不是独立从源闭包重建。独立审查员已获悉
该最终源码及哈希，将与本任务其他模块一并验证。
