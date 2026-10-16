# Agent #102 端点模块独立复核

复核者为真实子代理 `/root/word_intervals`。被复核的 `Agent102RunEndpoints.lean` 由母代理 `/root` 编写；复核者只读该源码并另建 `EndpointReview.lean`，未修改母代理源码。

## 结论与版本

未发现需要修改的数学缺口。`Agent102RunDefs`、`Agent102AffineArithmetic`、`Agent102RunEndpoints`、`Agent102RunWord`、`EndpointReview` 五个模块均在本轮新建的空构建目录中编译成功，返回码均为 0。编译使用的 Lean 版本、完整命令与全部文件校验值见 `manifest.json`。

被复核端点源码的 SHA256 为：

`297199a5a4c51f2981b27df76413669474e7598238ab9087a50788d5b548e129`

重建前后母代理端点源码未变化。证据目录只包含源文件、日志及校验记录，不包含 `.olean`。

## 关键数学检查

`widthAffine_eval` 使用每段 `positivePart` 在阈值之后与实际 `Int.toNat` 长度一致的结论，逐段累加得到实际 `wordAt` 的总长度。负斜率或负常数的段最终贡献零；没有把负长度计入总宽。

`spanSpecsFrom_at` 明确要求当前起点在所考察参数处非负，并利用每段 `positivePart` 求值非负维持递归起点非负。`Int.toNat_add` 的两个非负前提均有证据。其结论是整个区间列表的相等，保留段顺序、数字以及所有左右边界，包括零长度段。

`spanSpecsFrom_nonneg` 和 `spanSpecs_nonneg` 证明每个保存区间的左右仿射端点求值均非负。这避免了随后从整数端点转换为自然数端点时发生未说明的负数截断。

`endpoints` 除每个区间的左右端点外还显式保留总宽。空输入时没有区间，但 `endpoints [] = [Affine.zero]`；总宽端点依然存在。因此没有遗漏空词的边界情形。

## 独立导出的全称检查

以下三个定理位于单独的 `EndpointReview.lean`，通过已冻结模块接口重新导出，而未修改实现。

| 定理 | 已证明的性质 |
| --- | --- |
| `Agent102.EndpointReview.exact_coverage` | 参数超过长度阈值后，某仿射区间覆盖下标 `i`，当且仅当 `i` 是实际 `wordAt` 的合法下标。 |
| `Agent102.EndpointReview.exact_digit` | 任意保存区间覆盖某下标时，实际词在该下标的 `getElem?` 等于该区间的数字。 |
| `Agent102.EndpointReview.endpoint_bounds` | 每个保存端点求值均位于整数闭区间 `[0, (wordAt rs k).length]` 内。 |

三者的公理依赖均仅为 Lean 标准公理 `propext`、`Classical.choice`、`Quot.sound`。

## 退化边界控制

十一条命题检查了空输入的阈值、词、区间及端点，以及一个同时包含负斜率、负常数、增长段、零长度段和相邻同数字段的混合输入。它们全部使用 `rfl` 或 Lean 内核的 `decide` 证明，公理审计均为无公理依赖。

混合输入在参数 4 时的段长依次为 `[0, 0, 3, 0, 2]`，实际词为五个数字 `5`。保存区间依次为 `[8,0,0)`、`[4,0,0)`、`[5,0,3)`、`[5,3,3)`、`[5,3,5)`；这里每组三元组依次表示数字、左端点和右端点。还检查了从常数起点 7 开始的全部区间平移。

## 失败与修正记录

`endpoint-review-001` 保留本复核文件的首次失败源和日志。错误仅是复核文件引用了不存在的标准库名字 `Int.le_of_eq`，后改为已知等式改写加自反性。该次运行中母代理的定义、算术和端点三个模块已经全部成功。本轮 `endpoint-review-002` 连同复核文件全部成功。

词区间模块的独立发布证据位于同级 `release-001`。其中 `Audit.lean` 对本词模块 27 个导出声明逐字执行 `#print axioms`，全部通过；主定理 `word_eq_iff_length_and_overlap_digits` 允许空表、零长度段以及相邻相同数字。

本复核结论只涉及字面 run 拼接与仿射端点描述，不包含十进制进位运算或 P196 全局命题。
