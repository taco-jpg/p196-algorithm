# README 接口与计数备忘

这是供母代理撰写正文使用的工程备忘；没有修改仓库 README。

## 已核对的数量口径

12 个 Agent105 顶层模块包含 **115 条公开定理、18 个公开定义，共 133 个公开声明**。Normalize 中另有 1 条 private theorem，不计入公开接口数。原 Agent1、Agent8、Agent102、Agent109 的依赖定理以及编译器自动产生的证明辅助项均不计入这 115 条。

逐文件源声明清点后，另生成 Lean 导入驱动，对全部 133 个公开名字逐项执行 `#check` 和 `#print axioms`。官方 Lean 4.19.0、`--trust=0 -j1 -DElab.async=false`，exit 0；所有公理均在标准 `propext`、`Classical.choice`、`Quot.sound` 集合内。源 SHA 在审计前后相同。这是公开接口数量与类型检查；大型全依赖 fresh 核验的状态须引用独立验证报告。

| 模块 | 公开定理 | 公开定义 |
|---|---:|---:|
| `Agent105AffineBasics` | 13 | 4 |
| `Agent105AffineNormalize` | 16 | 2 |
| `Agent105AffineOrbit` | 18 | 3 |
| `Agent105AffineShape` | 15 | 2 |
| `Agent105AffineStability` | 6 | 0 |
| `Agent105AffineZip` | 7 | 3 |
| `Agent105IntegerSafety` | 4 | 0 |
| `Agent105ReturnTimeBound` | 9 | 0 |
| `Agent105TailSelection` | 18 | 2 |
| `Agent105UniformIntegerReturn` | 3 | 0 |
| `Agent105UniformReturn` | 4 | 2 |
| `Agent105UniformReturnPlain` | 2 | 0 |
| **合计** | **115** | **18** |

## 正文应突出说明的四个最终端点

以下四项位于 `Agent105.UniformReturn` namespace。

| 接口 | 给定的返回信息 | 得到的结论 |
|---|---|---|
| `uniform_return_wordAt` | 固定有界仿射游程族、正宽度斜率、正加性参数位移、尾部 canonical 列表，以及每个充分大参数处的正时间返回 | 存在一个固定 `1 ≤ t ≤ 4 * widthSlope rs * s`，使整条参数尾部都在该时间返回 |
| `uniform_safe_return_wordAt` | 同上，并给定各返回段每个正时间输出避回文 | 同一固定返回时间对整条尾部成立，而且 `1..t` 全部输出仍避回文，包含返回端点 |
| `uniform_integer_return` | 每个充分大参数有正整数实现及正时间 pair-word 返回 | 得到同一固定有界时间；保留每个尾部参数的正整数可实现性，并对所有该 pair word 的整数实现同时给出返回 |
| `uniform_integer_safe_return` | 上述实际正整数返回段还避开所有正时间回文 | 在同一固定有界时间下，对所有实现同时给出 pair-word 返回及 `1..t` 的实际整数避回文 |

返回是原 `Agent8.orbit` 的实际列表等式，整数端点通过原 `Agent109.Compat.pairWord_orbit` 与 `Lychrel196.orbit` 连接。对于任选的两个整数实现，不能把 pair-word 等式改写成整数本身相等。

## 支撑链对应接口

| 作用 | 主要接口 |
|---|---|
| 实际有限时间仿射闭包 | `Agent105.AffineDynamics.hasAffineRuns_orbit` |
| 实际规范化数字输出闭包 | `Agent105.AffineDynamics.hasAffineRuns_normalized_orbit` |
| 固定时间返回的尾部真值稳定 | `Agent105.UniformReturn.actual_return_tailStable` |
| 真实宽度的加性参数增量 | `Agent105.AffineShape.wordAt_length_shift` |
| 尾部同头与宽度数据 | `Agent105.AffineShape.wordAt_head_width_eventually` |
| 实际同头返回时间界 | `Agent105.ReturnTimeBound.word_family_return_time_bound` |
| 有限候选时间的整条尾部选择 | `Agent105.TailSelection.uniform_bounded_tail_selection` |
| 实际正时间整数回文桥 | `Agent105.IntegerSafety.palindrome_orbit_positive_iff_of_pairWord` |

其中规范化和逐项相加的最终接口已消除早期辅助版本中的标量前提；最终纯返回与安全返回定理没有将实际仿射闭包、等式稳定性、同头或时间界设成未证明的额外前提。

## 范围用语

- `Eventually` 指存在阈值之后每个自然参数都成立。结论的同一个 t 位于整个参数尾部量词之前。
- 时间 t 的正性、宽度斜率正性、参数位移正性以及返回覆盖存在性均保留；后者是实质输入，本结果不构造返回实例。
- 原 `CanonicalPair` 是列表条件，不能单独当作任意列表有正整数实现的定理。整数端点显式给出并保留实现性。
- 安全段为正时间 `1..t`，包括终点；不提供时间 0 初值非回文性。
- 该结果处理固定有限仿射游程族的加性参数更新。它没有给出 196 或某个十进制初值的无限避回文结论。

完整逐项名字、源 SHA、Lean 驱动、日志与回执在 `review/interface-inventory/lean-runtime/`。
