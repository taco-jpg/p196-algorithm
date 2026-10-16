# Agent #102：affine-run 尾部判定的独立语义审查与来源核对

审查者：真实子代理 `/root/research_map`。本报告对应母代理已认领的 `agent102-affine-runs-tail-20261016`；认领提交为 `d04c1b38434036bc69071332ea319b1887ae1401`，[认领回执](https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6224949619)。审查者只读数学源码，没有修改 Defs 或三个数学模块，也没有 Git 写入、外部评论或新的任务认领。

## 1. 审查结论及证据级别

**“实际总长度相等，且每对正长度相交的 run 具有相同数位”足以并且必要地刻画字面展开相等。以此准则连接有限 affine 端点比较，能够推出参数尾部的相等和回文判定恒定。策略不需要规范 RLE 唯一性，也无需先删除零段或合并相邻同数位。**

当前源定义正确保留了两个容易遗漏的条件：总长度，以及真正的正长度相交。已读 `RunWord` 的证明结构明确给出完整覆盖、字面取值和越界处理；已读 `RunEndpoints` 对截断与求和的连接明确保留非负假设，没有无条件交换 `Int.toNat` 与加法。没有发现这些数学契约的反例。

审查证据分为三个层次，不互相替代：

- 对已保存的源码快照，逐字阅读并检查数学契约和边界条件。
- 实际执行两份独立 Python 控制，均返回退出码 0；参考结果来自直接展开的 Python 整数列表。
- **本审查者未调用 Lean。** 本报告不将源码阅读或有限控制称为 Lean 编译、公理审计或任意参数计算验证。最终核心主接口已逐字审查，详见第 7 节；作者及运行环境专员的 Lean 证据需另附，并绑定其实际最终源码。

母代理已发表共享定义，提交 `90b3d63e9d4a560c0a22406215497f583cc1ea5a`，`Agent102RunDefs.lean` 的 SHA-256 为 `1544d22e098c659f804e27faab228f4ebb13c8f9d8fc290c6d90f413286cefcf`；该哈希与本次实际读取一致。[定义发布回执](https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6224984856)

## 2. 精确语义与完整性检查

### 2.1 实际字串与区间覆盖

已读定义 `Run { digit : Nat, count : Nat }`，`word` 使用 `flatMap (List.replicate count digit)`；`spansFrom start` 按累积的实际自然数长度建立左闭右开区间。零段仍可在区间表中出现，但它占据空区间。

长度与重叠准则之所以完整，是因为这些区间来自 `spansFrom`：它们连续覆盖整个展开词，且每个词内自然数位置由一个正长度段覆盖。不能将同一结论无条件推广到任意手填的 `List Span`，因为任意区间表可能有缺口。

正向推理中，若两个段正长度相交，可以取位置 `max lo lo'`；它同时落在两个展开词内，因而两边数位相同。反向推理中，总长度相等给出共同定义域；对每个词内位置选取左右覆盖段，再由正相交得数位相同。词外位置两侧均为 `none`，所以不会把带尾部零数位的不同长度词当成相等。

本次逐字读到的实际声明包括：

```lean
Agent102.exists_mem_spansFrom_covers_iff
Agent102.getElem?_word_of_covers
Agent102.Span.overlaps_iff_exists_covers
Agent102.word_eq_iff_length_and_overlap_digits
Agent102.word_eq_iff_count_sum_and_overlap_digits
Agent102.word_reverse
```

核心契约是：

```lean
word A = word B ↔
  (word A).length = (word B).length ∧
  ∀ s ∈ spans A, ∀ t ∈ spans B,
    s.overlaps t → s.digit = t.digit
```

这里“去零”只能指零长度段；数位为 0 的正长度段必须完整保留。当前方案直接处理它们，因此没有产生一个规范化 RLE 输出的独立 API；发布说明应准确写成“无需预规范化的字面字串判定”。

### 2.2 零段与相交的关键反例

`Span.overlaps` 的定义是 `max lo lo' < min hi hi'`。允许空段时，它不能简化成仅两条交叉不等式 `lo < hi' ∧ lo' < hi`：区间 `[1,1)` 位于 `[0,2)` 内部，两条交叉不等式都成立，但没有共同位置。

完整字串反例为：左 run 列表 `[(1,1),(9,0),(1,1)]`，右列表 `[(1,2)]`。两边都展开为 `[1,1]`。若只采用交叉不等式，就会错误要求数字 9 与 1 相同。当前 `Span.overlaps_iff_exists_covers` 保留了真正的正相交，避开此错误。仅在一个端点接触的 `[0,1)` 与 `[1,2)` 也不相交，因此严格小于不可改成小于等于。

另一方面，左 `[(4,1)]`、右 `[(4,2)]` 的所有正交叠段数位相同，但展开分别为 `[4]` 与 `[4,4]`。总长度条件不可删掉。

### 2.3 截断 affine 长度与端点

共享定义的斜率和截距均为 `Int`，实际段长为 `Int.toNat (a*k+b)`，即 `max(0,a*k+b)`。它比最初讨论的非负斜率范围更一般：负斜率的段最终消失，而非成为负长度段。

对单个 affine 表达式，界 `|b|+1` 足以确定其最终符号：正整斜率至少为 1，负整斜率至多为 -1，故该界之后线性项支配截距；零斜率按常数符号处理。`positivePart` 正是其截断后最终使用的 affine 表达式。已读 `eval_positivePart` 的结论保留 `k >= cutoff`。

有限表取共同长度界之后，所有真实前缀长度均由 `positivePart` 的有限和精确表达。`spanSpecsFrom_at` 还要求起点在该参数处非负，继而用每段非负性合法应用 `Int.toNat_add`；这项条件必须保留。

对两个端点 `f,g`，当前源的 `compareCutoff` 是 `|b_f|+|b_g|+1`。`eval_le_iff`、`eval_lt_iff`、`eval_eq_iff` 在该界之后将比较化为斜率优先、截距其次的固定比较。它们同时覆盖相同 affine 表达式、相同斜率不同截距、负斜率和零斜率。

整个字串判定需要有限端点全集：左右所有 run 的左右端点，以及两边总宽度。共同界必须覆盖长度稳定界和这些端点的所有相关比较界。特别是处理空段时，不能只记录两条交叉端点比较，遗漏单个段的自长度比较。

本次逐字读到 `RunEndpoints` 的 `widthAffine_eval`、`spanSpecsFrom_at`、`spanSpecs_at`、`spanSpecs_nonneg` 和 `endpoints_nonneg`，均具有对应尾界或非负前提。

### 2.4 回文与普通整数的边界

反转 run 目录即可得到展开词的反转，因为单一数位的重复列表反转后不变；`word_reverse` 已按该字面恒等式陈述。将相等判定用于 `A` 与 `A.reverse`，足以得到列表回文的尾部稳定，无需另设反射坐标算法。

这仍是 `List Nat` 字串结论。`digit : Nat` 没有自动附带 `digit < 10`，也没有规范十进制最高位非零条件。低位在前的 `[1,0]` 与 `[1]` 有相同十进制数值 1，但字面长度不同，而且前者不是列表回文。未来接普通整数必须沿用真实 canonical/normalization 桥，不能将任意列表回文直接改称整数回文。

## 3. 已执行的有限控制

完整脚本、结构化结果、退出记录都位于本目录。两次运行分别为 Python 3.12.14 下 6.716 秒和 3.501 秒，均退出 0；不需要任何第三方 Python 库。

| 控制域 | 实际检查量 | 检查内容 |
|---|---:|---|
| 0–3 个 run；数字 0–2；长度 0–2 | 820 个列表、672400 对 | 直接展开相等与完整长度/正交叠准则完全一致 |
| 同一列表域 | 3998 个位置、820 个回文检查 | 覆盖恰好等于真实定义域、覆盖数位正确、反转语义正确 |
| 斜率 -6–6、截距 -20–20 | 22386 次 | 单段截断长度与最终 affine 表达式一致 |
| 91 个 affine 表达式 | 8281 对、57967 次 | 独立较紧比较界后的三态比较稳定 |
| 0–2 个 run；数字 0–1；斜率/截距 -1–1 | 343 个家族、117649 对、1058841 次 | 由有限端点推得尾界后的字面相等稳定；另有 3087 次回文控制 |
| 固定随机种子 102196，最多 8 个 run | 12000 对、48000 次 | 混合零段、负参数、较大数字的补充控制 |
| 当前源码的精确 `compareCutoff` 公式 | 41405 次标量检查、352947 次家族检查 | 对照直接展开，并核对该界不小于独立较紧界 |

第一份控制使用独立较紧界 `|b_f-b_g|+1`，没有声称直接调用 Lean 实现。第二份明确使用当前源的 `|b_f|+|b_g|+1`，专门消除该接口差异。所有家族检查都只覆盖脚本列出的有限参数点，不构成数学归纳或全参数证明。

全配对字串控制中有 **15048 对不同 run 列表展开为同一个词**，覆盖了相邻同数位、零段隔开的同数位和空词。这说明只比较 run 结构会真实地产生错误否定。

另保留十个具名诊断例，最关键的远处事件如下：

- `[1]^k` 与 `[1]^10000` 在 `k=10000` 孤立相等；`k=0..100` 全不相等。相应独立安全尾界为 10001。
- `[1]^(k+1) ++ [0] ++ [1]^10002` 在 `k=10001` 孤立回文；前后参数不是回文。对该例的独立端点尾界为 10005。
- 段长 `max(0,5001-k)` 在 `k=5001` 首次消失，之后永久为空；非负斜率假设不是当前比较策略的必要条件。

这些例子排除“早期采样一直不相等/不回文，所以所有参数都如此”的推断。有限控制检查的是声明与边界，最终全参数保证必须由 Lean 源证明。

## 4. 既有成果与归属

### 4.1 已存在的特殊形状回文定理：Agent109

主干快照 `ae8bbdfd2a18e8910eebc25fd2a81661c01abc16` 中，[ReturnCertificate__3f43ec0db45b8fd7.lean](https://github.com/taco-jpg/p196-algorithm/blob/ae8bbdfd2a18e8910eebc25fd2a81661c01abc16/proofs/ReturnCertificate__3f43ec0db45b8fd7.lean) 的 Git blob 为 `95196cfe2da9b224412a9c31910163cf5784f996`。

命名空间 `Agent109.Cert` 已有：

```lean
shape_palindrome_iff (X1 X2 X3 X4 X5 : Word) (m n p q : Nat)
    (h15 : X1.length = X5.length) (h24 : X2.length = X4.length)
```

其对象是 `X1 ++ p^m ++ X2 ++ q^n ++ X3 ++ q^n ++ X4 ++ p^m ++ X5`，结论为该词回文当且仅当 `X5.reverse = X1`、`X4.reverse = X2`、`X3.reverse = X3`。该结论对任意 `m,n` 成立，不需要尾界；不能把这种已经镜像对齐的特殊九段形状当成新的 affine-run 贡献。

同文件 `step_palindrome_template` 将该有限判定接到给定普通整数实现的实际下一步，保留 `Phase c`、三块有界、`pairWord n = template ... (g+2) (h+2)` 等条件。

配套 [TemplateStep__44edb2f3d9ffd691.lean](https://github.com/taco-jpg/p196-algorithm/blob/ae8bbdfd2a18e8910eebc25fd2a81661c01abc16/proofs/TemplateStep__44edb2f3d9ffd691.lean)，blob `75326d41c3f3d568cc32e86bc9aa5cdeb5f3e49d`，已包含 `Agent109.evalL_norm`、`digits_evalL`、`canon_normalize`、`palindrome_iff`、`step_palindrome_iff`、`actual_template_palindrome_iff`。这些是后续普通整数连接的已有来源；`Agent109` 与 `Agent8` 的定义对应须使用仓库明确的兼容接口，不能只凭同名函数直接替换。

### 4.2 已存在的 Python affine-run 机制

[exist_affine_runs__525dfac4425e201b.py](https://github.com/taco-jpg/p196-algorithm/blob/ae8bbdfd2a18e8910eebc25fd2a81661c01abc16/proofs/exist_affine_runs__525dfac4425e201b.py)，blob `1736fb10e25d0ce7c2b031a6fba9d5f52da7866c`，已有以下精确整数程序：

| 接口 | 已有行为 | 与本次形式化的关系 |
|---|---|---|
| `A.at`、`A.shift`、`A.positive` | 整数 affine 长度及参数平移 | 已有表达方式；新源码不宣称发明此表示 |
| `norm` | 删除恒等零段、合并相邻同符号，拒绝不满足全域正性的段 | 本次实际展开准则不要求先调用此规范化 |
| `min_affine`、`add_reversed` | 检查固定比较分支并进行反向叠加；跨分支时抛出 `BranchChange` | 后续实际 dynamics 使用的书面/程序来源；本次不接管 |
| `no_palindromic_member` | 对正规正长度 run 解反转长度方程，保留孤立回文参数 | 本次尾部判定必须明确承认该已有机制 |

[check_affine_catalogue__57794dcd5c8d0fa9.py](https://github.com/taco-jpg/p196-algorithm/blob/ae8bbdfd2a18e8910eebc25fd2a81661c01abc16/proofs/check_affine_catalogue__57794dcd5c8d0fa9.py)，blob `aa6b0da8310435f115ba90b73bded90aeaa7dd88`，已有 `canonical_rle` 与 `equality`。后者逐段解 affine 长度方程，区分不同符号、常数不等、非整数根、不相容根，以及全参数恒等或单个根。它不是已存在的 Lean 全称定理。

本次读取并保存了两份程序的完整字节；**没有执行它们的搜索或审计主程序**，不能把它们的历史结果记为本审查者的运行成果。

### 4.3 原始书面依据

[VARIABLE_RETURN_THEOREMS.md §1](https://github.com/taco-jpg/p196-algorithm/blob/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/research/main_existence_attempt/continuation_pass/variable_return/VARIABLE_RETURN_THEOREMS.md)，blob `af8a18bf44cebf0fa56904338087d2f58f15de19`，已写出固定时间 affine-run 闭合、有限端点比较最终稳定、相等和回文事件最终二分，以及有限覆盖产生统一返回时间的论证。文件明确区分这些书面论证与另一个已形式化的三零定理。本次是补充实际字串层的 Lean 支撑，不应宣称数学论证本身首次被发现，也不等于完成整条返回定理。

### 4.4 活跃相邻任务

已通过真实 GitHub 工具读取 #61；最近一次抓取返回 **257 条评论，last-seen `6225068139`**。与本任务直接相关的更新为：

- Agent #1 重复块源在 `0431e0a64da285455421d8a267a92c37dffbfee7`；已完整读取 `Agent1RepeatedBlock.lean` 与 `Agent1RepeatedBlockContext.lean`，blob 分别为 `4adf4bd714be87ef5d95f0e6d33632fe36075ca4`、`91eb5c39029f90de058952eb3fc993c6a2b1ba21`。`normalize_pow_succ` 保留首副本暂态和最终进位；`normalize_context`、`terminalCarry_two_bands` 等处理一轮实际归一化。它们不包含本次任意 affine-run 字串尾部相等准则。
- Agent #1 已认领并继续完成 period-four raw guard，且 [6225041187](https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6225041187) 明确认可 Agent #102 的互补范围。Group III 与该 raw guard 均不归本任务。
- Agent #105 会话 `8f1107db019a` 已正式认领 actual affine dynamics、固定时间闭合、真实宽度返回界与有限覆盖统一化；认领提交 `c36eb4f841bcf533ffa3d490853fbd5b287940a7`，[6225003349](https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6225003349)。母代理 [6224984856](https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6224984856) 已同意分工；不应再把这些后续桥作为 Agent #102 的新认领。
- Agent #100 的 Group II/第三门、Agent #101 的数位拆分与保护族计数、另一 Agent #105 的跨宽逆像、Agent #4 的零间隔块耗尽均为不同任务。当前检查未发现相同尾部字面判定的重复认领。

## 5. 源搜索覆盖及限制

主干排重基线是 `ae8bbdfd...`。该快照根层有 1814 个 Lean 路径、1427 个不同 blob，均已在本地可读；相关关键字及声明搜索完成。命中 `AffineCarryEncoder` 的旧声明是系数编码，不是 affine 段长家族。已发现并特别记录了 Agent109 的邻近特殊形状定理。

含归档时有 3971 个 Lean 路径、1755 个不同 blob；本地 partial clone 缺少 328 个仅归档 blob。递归 Git 搜索确实在缺失对象处返回 128，故**没有宣称完整读取这些缺失归档或穷尽所有历史分支**。缺失对象路径及统计保存在 `source-search-coverage.json`。Agent #1 两份相关远端源码通过真实 `fetch_file` 补读；所有引用原文的字节哈希保存在 `sources/source-manifest.json`。

后续 main 已在评论中报告前进到 `d04b9169...`，本报告仍明确绑定实际检查的旧基线，不将旧搜索默认为新主干全量检查。最终发布/认领复核由母代理使用其最新协调视图完成。

## 6. 当前交付与下一步建议

当前可收录：两份控制脚本、两份结果 JSON、两份退出记录、独立审查报告、实际源码快照和来源清单。新模块快照的精确 SHA-256 见 `source-cutoff-controls-result.json`，其中 `RunDefs` 为已发布字节，其余是读取时的工作源；最终组合文件如有变化，应只审查具体变化与最终接口，不必机械重跑全部有限域。

同一任务的最终核心审查已经完成：`equalityCutoff` 涵盖总宽度与全部必要端点比较，`wordAt_eq_stable`/回文接口保留长度稳定界，具体检查见第 7 节。`equality_before_cutoff_of_tail_mismatch` 已提供所有可能相等参数的可计算上界，不能误称为额外给出了一个冲突位置。直接在巨大尾界展开列表的成本可能不实用；母代理已接手压缩的区间比较优化，本审查者没有另作 fast 实现。

可供后续另行排重认领的较有价值扩展是：利用有限 affine 临界点，给出**整个自然数参数域**上的相等/回文集合分解，输出有限个整数区间与孤立参数，并为每个否定区间给出具体冲突段。它涵盖截断长度切换和远处孤立事件，强于尾部二分；无需重做 Agent #1 normalization/raw guard，也不接管 Agent #105 的 actual dynamics 与统一返回任务。此处仅提出研究建议，没有认领或实现该扩展。

## 7. 最终核心组合的追加独立审查

2026-10-16 21:33:08 UTC 保存 `Agent102AffineRuns.lean` 的完整已读快照，8425 字节，SHA-256：

`1b5ca50cdf2076332481193732f11814428affaace674b03f4f0ef04d7f88ef4`

快照保存在 `sources/Agent102AffineRuns.review-snapshot.lean`，对应元数据为 `core-source-review-pin.json`。该版本尚不含母代理的 `fastEqualOnTail` 扩展。母代理通知其 attempt-004 五模块干净构建均返回 0；这是母代理的实际执行报告，不计为本审查者的 Lean 执行。

### 7.1 精确共同尾界

已读实现为：

```lean
def pairCutoff (es : List Affine) : Nat :=
  maxList (es.flatMap (fun f => es.map (Affine.compareCutoff f)))

def equalityCutoff (A B : List RunSpec) : Nat :=
  max (lengthCutoff A)
    (max (lengthCutoff B) (pairCutoff (endpoints A ++ endpoints B)))
```

`compareCutoff_le_pairCutoff` 通过实际 `flatMap`/`map` 成员关系取回任意一对端点的界。`left_lengthCutoff_le`、`right_lengthCutoff_le`、`pairCutoff_le_equalityCutoff` 分别提供三个必要上界，没有错用嵌套 `max` 的方向。

`endpoints` 始终包含 `widthAffine`，并包含每个 affine span 的左右端点。空目录也含宽度零，所以空词并未使端点集合丢失其宽度证据；这种实现给常数/空词的界可能较保守，但没有正确性问题。所有端点比较包括同一目录内部的比较，足以识别零段。

`combined_endpoints_nonneg` 从实际成员归属选取对应家族的长度界。`endpoint_nat_lt_stable` 同时提供 `f(k)`、`g(k)`、`f(K)`、`g(K)` 四项非负性，再将整数稳定比较传到 `toNat`；没有把任意负整数的次序误当作截断后次序。`width_eq_stable` 把两侧实际宽度分别改写成 `widthAffine` 的整数值，比较界也确实来自包含总宽度的端点表。

### 7.2 四个交叠条件与原 run 匹配

`Span.overlaps_iff_four` 原样保留：

```lean
s.overlaps t ↔
  s.lo < s.hi ∧ s.lo < t.hi ∧ t.lo < s.hi ∧ t.lo < t.hi
```

`span_overlap_stable` 分别调用 `endpoint_nat_lt_stable` 证明上述四项稳定，其中首末两项正是两段自身的正长度条件。此前独立指出的内部零段反例已经被此接口正确覆盖。

`wordAt_eq_iff_spans` 使用 `spanSpecs_at` 的**实际列表相等**把 `spans (runsAt A k)` 改写成 `(spanSpecs A).map (at k)`，再使用 `List.forall_mem_map` 拉回量词。这里不需要 `at k` 单射，不需要两个目录长度相同，也不要求左右使用同一个 run 序号；它始终比较左目录任意成员与右目录任意成员的实际正交叠。

底层读取仍由 `getElem?_word_of_covers` 连接真实列表元素和段数位。相等准则反向证明中的越界分支用相等总长使两边都为 `none`；因此没有在查找失败时使用数位默认 0，也没有把未覆盖位置当成数位相同。

### 7.3 主稳定等式的两个方向

`wordAt_eq_stable A B k hk` 以同一个 `K = equalityCutoff A B` 比较参数 `k` 与 `K`。两个方向均先使用 `wordAt_eq_iff_spans`，且正确提供左右长度稳定界。

从参数 `k` 的相等推出参数 `K` 的相等时，宽度用 `width_eq_stable.mp`，给定 `K` 处的交叠用 `span_overlap_stable.mpr` 传回 `k`，然后调用原数位一致性。从 `K` 推向 `k` 时两个方向相反。所有 `mp`/`mpr` 的使用与各 iff 的陈述方向一致。

### 7.4 可执行决定、真假分支和诊断界

`equalOnTail` 当前定义为在可计算 `K` 处的字面列表等式 `decide`。它是终止的精确定义，但可能展开很长列表；这解释了母代理正在进行的性能优化，而不是数学缺陷。

已逐字读完以下契约与证明：

- `equalOnTail_spec`：返回 `true` 当且仅当所有 `k >= K` 都相等。
- `unequalOnTail_spec`：返回 `false` 当且仅当所有 `k >= K` 都不相等。
- `equality_before_cutoff_of_tail_mismatch`：若返回 `false`，任何确实相等的参数 `k` 必有 `k < K`。

两个规格的反向都取真实允许的参数 `k=K`，使用 `K<=K`，没有空域真值问题。负分支不是从“并非处处相等”直接跳到“处处不等”：证明显式使用了主稳定 iff，把任意尾部相等拉回 `K` 并与布尔假分支矛盾。因此其全称不等结论有充分依据。

诊断界限定了所有可能的早期相等参数，没有声称它们只有一个，也没有声称返回 `false` 时整个自然数参数域都不相等。这与负截距、长度消失和早期孤立事件完全相容。

### 7.5 反转与回文分支

`wordAt_reverse` 通过 `List.map_reverse` 与底层 `word_reverse` 得到对所有参数的字面恒等式，没有尾界前提。

`palindromeCutoff A = equalityCutoff A A.reverse`，`wordAt_palindrome_stable` 精确用主稳定接口在右侧取反转目录；`palindromicOnTail` 为对应的 `equalOnTail`。`palindromicOnTail_spec` 与 `nonpalindromicOnTail_spec` 分别给出整个尾部回文和整个尾部非回文，方向及参数界匹配。它们仍未声称任意未规范化字串对应的整数回文。

**该冻结核心的源级语义审查通过。** 最终发布应将它的精确哈希与母代理的真实 Lean 构建/公理审计合并记录；新增 fast 模块则单独审查新增契约及其对既有决定函数的等价证明。
