# Group II 上域 time2 重定基：完整 22 出口作者检查点

任务 `agent100-groupII-rebased-overlap-20261016`，作者为 Agent #100 / session20261016T2052Z。此检查点包含 `Agent100GroupIIRebaseAlgebra` 的 5 个定理、`Agent100GroupIIRebaseProfiles` 的 11 个定理，以及 `Agent100GroupIIRebaseNumeric` 的 6 个定理，共 **22 个出口**。三个模块均已实际通过 Lean 4.19.0 **`--trust=0` 作者增量检查**。新任务 21 模块独立 fresh 构建与审查正在运行，尚未宣称完成。

## 认领与源基线

- 成功 claim：`e1bc61f552413f4a1ed6cef86c88265d39fd896d`。
- task blob：`a277d7843d3509cf60a581ce06fb8d451975bea3`。
- issue #61 收据：[6225719769](https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6225719769)。
- 分支：`research/agent-100/groupII-rebase-20261016T2212Z`。
- 完整前置 overflow 源基线：`686cac2696e4e4e059c1b9d6a313f5519f6f4176`，即本会话的 [PR #125](https://github.com/taco-jpg/p196-algorithm/pull/125)。父代理已实际创建并回读该 PR。当前新 rebase 任务在本检查点尚无 PR。

## 数学范围与已检查结论

参数采用原 `UpperDomain`：`r≥1`、`5≤p≤9`、`5≤u≤8`、`5≤v≤6`、`u+v≤13`，包含全部七个核心以及 `r=1`。实际两步 component 的有限宽度为 `2*r+7`；在其有限零延拓上加四处整数修正：`r+1,r+5` 加 `1`，`r+2,r+4` 减 `1`。`rebasedComponent` 定义为修正结果的 `Int.toNat`。

Algebra5 证明此具体修正的相邻和等于已有 overflow 缺陷，并得到实际 time2 whole 在完整宽度 `2*r+8` 内的 **signed** 重叠恒等式。Profiles11 先证明四个修正位置的真实列值：外侧两处 `2*u-9`，内侧两处 `2*(u+v)-18`；再证明所有索引上的 signed 非负与上界，以及 `Int.toNat` 转换后的整数值恰等于转换前值。由此得到原定义 `Admissible (2*r+7) rebasedComponent`、对称性、中心偶数、正外列和有限尾零。非负性是独立证明义务，未用 `toNat` 截断隐藏负数。

冻结源：

| 模块 | 出口数 | SHA256 |
|---|---:|---|
| [Agent100GroupIIRebaseAlgebra.lean](../../../Agent100GroupIIRebaseAlgebra.lean) | 5 | `d62f8769d9d2ee0ecf2ec3f0b0dffcd6c19cd5383692207e0e044b7649df02ff` |
| [Agent100GroupIIRebaseProfiles.lean](../../../Agent100GroupIIRebaseProfiles.lean) | 11 | `2a95c9e88f315f3e317532e92a66afcc6dd09e1a97c2b5260fe97fae1c4b6771` |
| [Agent100GroupIIRebaseNumeric.lean](../../../Agent100GroupIIRebaseNumeric.lean) | 6 | `cecda22da5480e5b5fa5743f193a5aa68965cef707652e999d8da8087a0e0d41` |

Numeric6 已完成自然数与普通整数提升：

- `actual_whole_rebased` 在全部 `i < 2*r+8` 上证明真实 time2 whole 等于 `shiftOne rebasedComponent`，包含最高列 `i=2*r+7`。
- `rebased_component_realizable` 给每个参数组一个正整数 `a` 与宽 `2*r+7` 的 canonical 数字 `da`，其配对列恰为修正组件 `C`。
- 对**任意**原始 `n,d`，只要 `Canonical n d (2*r+7)` 且初始有效配对列对应 `initial`，`numeric_rebased_overlap` 与 `numeric_rebased_realization` 就给出真实 `orbit n 2` 的宽 `2*r+8` canonical 表示；全部有效列等于 `C` 的重叠，也等于正实现 `a,da` 的配对列经 `finiteWord` 截断后的重叠。
- `realized_rebased_overlap` 进一步给每个参数组同时存在的正原始输入及正修正组件实现，解除初始实现存在性前提。
- `rebased_differs_at_flank` 证明在 `i=r+1`，`C` 与真实 `componentOrbit … 2` 的整数列差为 **1**。此正组件实现不被等同于原组件整数的真实第二步输出。

新任务 21 模块独立 fresh 构建与审查正在运行，尚无完成结论。这里不声明一般 `(1+x)` 逆像分类、唯一性、后续安全性或 196 结论。

## 验证状态的准确区分

22 个新定理均有实际 `#print axioms`。Profiles11 仅依赖 `propext, Quot.sound`；Algebra 中 4 项与 Numeric 中 4 项另依赖 `Classical.choice`，其他项仅前两项。作者执行记录、命令、成功与失败源及完整日志分别位于 [development/algebra](development/algebra/README.md)、[Profiles 作者记录](development/profiles/author-execution.json) 和 [Numeric 实际执行收据](development/numeric/attempt01/receipt.json)。失败尝试的错误恢复 `sorryAx` 报告不属于接受证明。

Numeric `attempt01` 实际退出 0，参数为 `--trust=0 -j1 -DElab.async=false`。其 Git blob 为 `2da082c6ebe444d3e8f2ed793428ff259e04abc4`；[成功日志](development/numeric/attempt01/compile.log) SHA256 为 `cb70df8f10bb992994dd76ab5e9b46a4fd77d3cae6dd411a9b10a7c1e05d24ac`。成功源码快照与正式 Numeric 源逐字节一致。

本轮作者增量检查导入前置 18 模块的已有 olean，没有重编旧闭包。前置 overflow 已达到 **canonical18 构建及显式 `--trust=0` full-import audit 均 PASS**，最终证据待发布。canonical 构建本身采用默认 trust（max），与随后明确 `--trust=0` 的 full-import audit 分别记录；不把两者混称为同一显式 trust0 源码重建。该前置验证也不是本次新 rebase 的独立 fresh21 审查；后者目前仍在运行。

## 490 行有限控制与无损归档

指定 `r=1..12,30,100`、`p=5..9`、七核心，共 490 行全部通过。每行保留 `A0/Q0/A1/Q1/A2/Q2/Delta/CInt` 及所有检查字段；有限控制不能替代全 `r` 的 Lean 证明。

- 原始数据：[author-scout.jsonl](development/controls/author-scout.jsonl)，SHA256 `a1aa0dbf22c68afc238378f24d7ccfce59aaee4ee104256416e1b6a684ffae3c`。
- 无损压缩：[author-scout.jsonl.xz](controls/author-scout.jsonl.xz)。已实际解码并与原件逐字节比较通过，见 [author-compression.json](controls/author-compression.json)。
- [脚本](development/controls/author-scout.py)、[完整运行日志](development/controls/author-scout.log)、[汇总](development/controls/author-scout-summary.json) 均保留。

解码示例：

```sh
xz -dc controls/author-scout.jsonl.xz > decoded-author-scout.jsonl
cmp decoded-author-scout.jsonl development/controls/author-scout.jsonl
```

以上是可复核命令示例；本次实际 round-trip 使用 Python 标准库 `lzma` 解码和字节相等断言，结果与散列已记录。

## 归属与沿用成果

Agent8 的共同溢出一般传输、有限差分与相关定义继续完整归属 Agent8，沿用 [PR #84](https://github.com/taco-jpg/p196-algorithm/pull/84) 精确源 `8874b2ee291dc7a253b3b89fbbf0efd86812ae4d`；本任务只证明当前具体族的修正与合法性。当前源基线 PR125 属于本会话的 GroupII overflow sharpness；原 GroupII 修复为本会话已合并的 PR88，第三门边界是另一个本会话任务 PR103。

另一 Agent100 / session212248Z 的 `586bf0b67efd520363fb68455dd3c683945ccdaa` 属于原 `(1,1,6)` time6 的任意非负逆像障碍及既有前两列必要条件；本任务保留其归属，不将其当作 PR125，也不为其填写未经实读的 PR 编号。复制的历史归属报告将它当时的状态标为 WIP / NOT LEAN-CHECKED；这是报告读取时状态，非当前状态判断。

归属报告已从 scratch **逐字复制并核对**：[Markdown](ownership/next-rebase-ownership-report.md)、[JSON](ownership/next-rebase-ownership-report.json)。报告是所列快照内的有界审查，不是全仓库不存在性证明；正文里的历史待认领结尾予以原样保留，本任务后续成功 claim 由上方新收据记录。

机器可读的出口清单、源 pins、状态边界、归属与压缩核验见 [PUBLICATION.json](PUBLICATION.json)。本次材料更新只修改这份 README 与 PUBLICATION.json；未修改 Lean 源或独立审查目录，也未进行 Git 写入。
