# Boundary 独立交叉审查

结论：**通过本模块的独立语义审查、独立源码重建和完整模块来源公理审计**。
审查者为真实子代理 `lean_runtime`；被审查模块作者为另一真实子代理
`semantic_review`。本记录只赋予 `Agent107TransducerBoundary.lean` 独立审查状态，
不为审查者本人编写的 Tables/Reachable 赋予独立审查状态。

冻结 Boundary SHA-256：
`cbdc094ba800bf4198bc5a1f2ece8b971aaea91ed2ceb2f1b36a24a978baa89c`。

## 15 个公开端点的语义核对

| 端点 | 核对结果 |
|---|---|
| `initial_no_overflow_sentinel` | 无溢出初态的有符号延迟确为 `-1`，没有改为自然数零。 |
| `initial_overflow_delay` | 溢出初态的延迟为追加进位 `1`。 |
| `no_overflow_preserves_sentinel` | `nextState` 在无溢出分支始终保留 `-1`，无需额外转移假设。 |
| `actual_no_overflow_sentinel` | `actualState` 在实际末进位为零时也保留相同哨兵。 |
| `first_pair_zero_rejected` | 初态 `started=false`，实际转移定义要求第一个成对符号为正；零被拒绝。 |
| `odd_center_rejected` | 原算法仅枚举偶数中心；`Terminal` 中的偶性约束被准确检查。 |
| `oversized_center_rejected` | 原中心范围为 `0..18`，大于 18 的值不可能终止。 |
| `empty_input_rejected` | `L=0` 时初态直接面对 `none` 中心，`started=false` 且没有正中心，因此不接受空词。 |
| `one_digit_accepts_iff` | `L=1` 没有成对转移，唯一被读取的状态是 `p 0`；完整条件为中心正、至多 18、偶数且 `q 0 / 10 = h`，并保留 `h≤1`。 |
| `one_digit_no_overflow_example` | 中心输入 8、初态 0 被接受；折叠输出为零个成对符号和中心 16。 |
| `one_digit_overflow_example` | 中心输入 10、初态 1 被接受；折叠输出为额外成对符号 `[1]`，没有中心。 |
| `no_overflow_has_no_extra` | 无溢出分支从不额外追加成对符号。 |
| `even_overflow_has_center` | 输入无中心时，溢出输出无额外成对符号而具有 `2 * delay.toNat` 中心。 |
| `odd_overflow_has_extra_pair` | 输入有中心时，溢出输出追加该中心输出数字与延迟数字之和，并没有输出中心。 |
| `accepted_tail_not_unique` | 两个接受路径函数在 `L=1` 被消费的唯一状态 `p 0` 相同，未消费的 `p 1` 可不同；有限状态列表相同而完整函数不相同。 |

后两项溢出公式的前提是 `overflow ≠ 0`，不是 `overflow = 1`。这是对字面函数
定义的正确一般化；它们不额外声称任意这样的状态都可达或满足数字界限。
`.toNat` 与 Defs 中的实际有符号延迟处理完全一致。

对照 `Agent107TransducerPath.lean`，唯一性范围明确为 `0..L/2` 的有限前缀，
`finitePath` 包含终止状态。边界反例正好排除了错误的整个无限函数唯一性，
没有与 Path 的有限前缀唯一性冲突。Path 仅供本次语义对照，不在本次独立审查
状态的覆盖范围内。

没有发现需要修改 Boundary 源码的正确性问题。

## 独立执行与依赖来源

`review_boundary.py` 创建全新的空目录，复制并实际重编译当前 Defs 与 Boundary，
没有加载作者的 Boundary 对象，也没有加载主代理构建目录中的 Defs 对象。
唯一复用的项目依赖是审查者本人此前从原始仓库源码独立重编的
`Lychrel196Research.olean`；其原提交、blob、源码与对象 SHA-256 均在本次
`manifest.json` 中明确记录，并在执行前与现有原源码逐项核对。

官方 Lean 4.19.0，commit `6caaee842e94`，固定
`--trust=0 -j1 -DElab.async=false`。独立 Defs 编译约 0.55 秒，Boundary 编译约
0.55 秒，模块来源审计约 2.60 秒；全部退出码为 0。

公理审计使用 `env.getModuleIdxFor?` 和实际导入模块名筛选
`Agent107TransducerBoundary`，审计其 **30 个定理声明**，覆盖 15 个公开端点
以及私有/自动生成的辅助证明。没有只用命名空间前缀或源码正则替代模块来源。
审计结果：15 项无公理，7 项仅 `propext`，8 项仅 `propext, Quot.sound`。
没有自定义公理、`sorryAx`、编译器求值公理或 `Classical.choice`。

实际命令、隔离目录、退出码、来源和对象哈希保存在 `manifest.json`；
完整审计源与输出分别保存在 `BoundaryModuleOriginAudit.lean` 和
`module-origin-audit.stdout.log`。执行结束后再次确认被审查源码未变。
本次没有失败尝试，也没有修改冻结源码或执行 Git 写操作。
