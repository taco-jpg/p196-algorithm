# 原 Boolean 编码的有限字母域：作者检查

作者角色：Agent #107 委派的 `scope_scout`。独占源码：
`proofs/Agent107DFAAlphabet.lean`，仅导入冻结 `Agent107DFA`。
全部新声明位于 `Agent107.FoldedDFA.Encoding`。

`CenterValid` 对 `none` 为真，对 `some v` 要求 `v < 19 ∧ v % 2 = 0`，带可判定实例。
`centerCode` 保留原 Python 的 11 槽编码：`none ↦ 0`、`some v ↦ v / 2 + 1`。
`centerCode_none`、`centerCode_some_zero` 是两个 simp 端点，分别为 0、1；
`centerCode_lt` 给出合法中心的编码严格小于 11。

对任意实际表成员，公开端点分别证明：

- `edge_input_lt`、`edge_output_lt`：边输入和输出均严格小于 19。
- `terminal_input_valid`、`terminal_output_valid`：终止行的输入中心、输出中心均合法。
- `terminal_extra_lt`：每个可选额外输出对严格小于 19。
- `terminal_extra_center_none`：若额外输出对存在，则输出中心为 `none`。

证明先对原 46 个字面状态用内核 `decide` 检查一次 `delay.toNat < 10`，再使用
已经冻结的 `Table.edge_sound` 和 `Table.terminal_sound`，结合余数界推导一般性
结论。不重新生成或重新枚举 872 条边、251 条终止行，也不使用 native reduction。

## 实际检查

首次尝试 `alphabet-001` 于 2026-10-16 22:19:54 UTC 真实退出 0，无失败尝试。
官方 Lean 4.19.0，参数 `--trust=0 -j1 -DElab.async=false`。
执行前保存完整源快照，并保存实际命令、标准输出、标准错误和退出码。

9 个公开 theorem 与 1 个私有延迟上界 theorem 全部显式打印公理；两个 centerCode
等式无公理，其余 8 个只使用 `propext`、`Quot.sound`。

冻结源 SHA256：

```text
64f13d225a8d4439d0e69384b01138173006897f3c5536708c953d3ae25aa534
```

冻结依赖 `Agent107DFA.lean` SHA256：

```text
d0fe8accc9d80110230ea3b4061f554d8d9d9dc5b8ea1a89f44e7d2fc977969e
```

本次仅为导入已构建冻结依赖的作者检查。独立审查员已收到冻结源，将另外执行完整
从源依赖闭包检查；不得将本记录描述为独立验证。
