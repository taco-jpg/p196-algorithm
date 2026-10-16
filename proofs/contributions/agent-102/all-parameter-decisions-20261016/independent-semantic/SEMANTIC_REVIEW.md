# 任意参数与全参数压缩判定：独立源码语义审查

## 结论与责任区分

独立审查者为真实子代理 /root/research_map。完整实读以下两个冻结模块及其基础接口后，未发现数学语义缺陷：任意参数比较始终使用真实截断段长；全参数判定正确分割有限前缀与稳定尾部；全称、存在及其否定没有混淆。审查状态为 SOURCE-SEMANTIC-PASS。

本审查者没有实现这两个数学模块，没有修改数学源码，没有执行 Lean，没有作 Git 写入或外部发布。Agent102RunDecision 的作者是 /root/word_intervals；Agent102AffineAllParameters 的作者是母代理 /root。内核构建和公理审计由作者及 /root/lean_runtime 的独立执行记录提供，不能算成本审查者运行过 Lean。

| 冻结文件 | 字节数 | SHA256 |
| --- | ---: | --- |
| Agent102RunDecision.lean | 1986 | e8d876593b4eec5248afe1dbc53cc6fc704b1ba106402a31637aca3120ece9f8 |
| Agent102AffineAllParameters.lean | 5419 | 7cd7b3682bcb6f072853a93cbadaaf43e5c2b59767add0a51f1f8938be183e0c |

精确副本保存在 [sources/Agent102RunDecision.lean](sources/Agent102RunDecision.lean) 和 [sources/Agent102AffineAllParameters.lean](sources/Agent102AffineAllParameters.lean)，全体依赖字节 pin 见 [source-pins.json](source-pins.json)。基础提交为 cba5dc441289bbed383972aa522a45c473879396。

母代理说明首稿为 5417 字节，两处否定化简所用引理修正为 Bool.not_eq_true'，原失败源与日志已保留。本文已重新读取并核对实际 5419 字节冻结源，没有把初稿当作通过版本；没有修改任何定理陈述的作者说明与当前冻结源分开记录。

## 1. compressedEqual 的判定条件完整

compressedEqual 接受任意 A B : List Run，先计算两个有限 spans 目录，然后检查：

- 两侧所有 Run.count 的总和相同；
- 对每一对实际正交叠区间，数位相同。

正交叠直接计算 max(lo,lo') < min(hi,hi')。它等于已证明的 Span.overlaps 定义，因此包含空段所需的两个自身正长度约束，不会把 [1,1) 当成与 [0,2) 有共同位置。

总宽检查不可删除：长度 1 与长度 2 的相同数位块在所有共同位置都相等，但字串不相等。当前定义保留总数目等式；当一侧目录为空时，空的双重 all 条件与该总宽条件合用，仍正确处理另一侧只有零段或含正长度段两种情形。

两个目录可以用不同数量的段表示相同词；相邻相同数位也可以保持为多个 run。程序逐一比较所有正交叠段对，不需要 canonical RLE 唯一性，不把 run 结构相等当成词相等。Nat 数位没有额外小于 10 的限制。

compressedEqual_eq_true_iff 的证明准确地将 Bool.and、两个 List.all 和 decide 展开为无阈值定理 word_eq_iff_count_sum_and_overlap_digits 的右侧，再取其逆向 iff。compressedEqual_eq_false_iff 则对这个 iff 取否定，得到 Bool 假值当且仅当两个实际词不同，没有额外域前提。

## 2. equalAt 没有错误使用尾部正部表示

equalAt A B k 定义为 compressedEqual (runsAt A k) (runsAt B k)。runsAt 对每个原仿射式计算 eval k 后再 Int.toNat；程序没有使用 spanSpecs、positivePart、ltOnTail 或某个参数阈值来代替当前真实长度。

这使负斜率、负截距、k=0 和长度过零位置都属于同一个无条件接口。例如长度 3−k 在参数 0、1、2 时不能用最终零函数代替；equalAt 直接保留其实际长度 3、2、1，在参数 3 起才截为零。

equalAt_eq_true_iff 与 equalAt_eq_false_iff 都只展开 equalAt 和 wordAt，直接套用任意具体 run 判定的真／假规格，没有偷偷增加 k≥K 前提。

## 3. 全参数程序的四个逻辑谓词

设 P(k) 表示 wordAt A k = wordAt B k，K=equalityCutoff A B，T=fastEqualOnTail A B。

| 可执行 Bool | 定义形状 | 真值的精确语义 |
| --- | --- | --- |
| allEqual | T 且对 List.range K 中所有 k 检查 equalAt | 对每个自然数 k，P(k) |
| someEqual | T 或 List.range K 中存在 equalAt 为真 | 存在自然数 k，使 P(k) |
| allUnequal | !someEqual | 对每个自然数 k，非 P(k) |
| someUnequal | !allEqual | 存在自然数 k，使非 P(k) |

这里 List.range K 精确覆盖 0≤k<K，尾部规格覆盖 K≤k。两部分既没有遗漏 k=0，也没有遗漏 k=K；不存在只查 1..K 或将尾部下界误写为 K<k 的问题。

特别地，allUnequal 使用的是 !someEqual。若等式仅在一个有限参数成立，allEqual 为假、someEqual 为真，此时 allUnequal 与 someUnequal 分别是假、真。源码正确保留了这种“既有相等参数，也有不相等参数”的情况。

## 4. 四个主规格的证明方向

### allEqual_spec

Bool 与有限 all 展开后，正向取得尾部全称证明和前缀全称证明。任意给定 k，以 K≤k 分支：大参数用尾部，小参数由否定分支推出 k<K，再用前缀。逆向从真正的全自然数全称命题分别限制到两部分即可。证明没有先假定有限采样足以代表尾部；尾部的完备性来自已证 fastEqualOnTail_spec。

### someEqual_spec

正向有两个分支。若 T 为真，源码取具体自然数 K 作为存在见证，并用尾部规格在 K≤K 处得到真实词等式；若前缀 any 为真，则保留其实际 k 和对应等式。

逆向从任意真实见证 k 出发：若 K≤k，用 fastEqualOnTail_iff_wordAt 的反向得到 T 为真；否则将该见证放入 List.range K。这里必需的是尾部 iff，只有单向“Bool 真则相等”无法完成这一方向。当前源码使用了正确的完整接口。

### allUnequal_spec

由于 someEqual 已有存在命题的 iff，其 Bool 假值恰好排除全部可能的相等参数。证明正向取任意 k 及假设相等推出 someEqual 真，与否定 Bool 冲突；逆向分别讨论 someEqual 的两个值，真值会产生被全称不等排除的真实见证。没有把“不是所有参数相等”误当成“所有参数不等”。

### someUnequal_spec

程序本身为 !allEqual。证明使用 classical，在不存在反例时逐个 k 推出相等，从而推出 allEqual 为真，矛盾；逆向从实际反例排除 allEqual 的真值。此处的经典推理只在证明项中，不是对无限域执行不可计算搜索的 Bool 实现。

该规格给出存在命题，并没有返回具体或最小的反例索引。allEqual_false_iff 继承同一个存在结论；若使用者需要可执行的反例位置，需要另外构造提取算法，不能把当前 Bool 当成已返回该位置。

## 5. 全部 16 个新公开定理的覆盖

RunDecision 的四条定理已分别核查：

- compressedEqual_eq_true_iff、compressedEqual_eq_false_iff；
- equalAt_eq_true_iff、equalAt_eq_false_iff。

AllParameters 的十二条定理已分别核查：

- allEqual_spec、someEqual_spec、allUnequal_spec、someUnequal_spec；
- allEqual_false_iff、someEqual_false_iff；
- allPalindromic_spec、somePalindromic_spec、allNonpalindromic_spec、someNonpalindromic_spec；
- allPalindromic_false_iff、somePalindromic_false_iff。

两个相等 Bool 的显式 false 规格，分别是存在反例和全称不等。两处 Bool.not_eq_true' 只把 Bool 否定为真的形式转换成原 Bool 为假，不改变量词。其余否定 Bool 的语义已经由四个主规格及定义精确限定。

## 6. 回文桥接保持原始字面意义

四个回文 Bool 只将第二目录取为 A.reverse。四个真值规格与两个 false 规格使用原 wordAt_reverse，故最终谓词确实是 wordAt A k 等于自身反转，而不是目录结构回文、数值回文或正规化后的回文。

空词在 List 层是回文；全零长度目录也可产生空词。数位为 0 的正长度段仍占据位置。整个新接口没有消去零数位，没有自动裁去表示前导／末尾零，没有加入 canonical numeral 或正整数存在假设。

所有量词均针对固定有限 RunSpec 目录的自然参数。它们不涉及 normalize、stepWord、实际轨道时间、196，或 Agent105 的固定时间仿射动力学闭合。若将来把静态族证明用于实际轨道，仍需独立保留对应的动态表示与整数桥接前提。

## 7. 计算边界与验证分类

新十个 Bool 入口的源码依赖是有限 counts／spans、标量系数比较以及 List.range K 上的 all/any；没有在可执行定义中调用 word、wordAt 或 List.replicate。证明陈述依然直接引用真实词，这正是压缩程序与实际 List 语义的连接。

全参数检查仍可能遍历巨大的 K 个参数并构造相应范围目录。当前结果没有承诺只按系数位数复杂度完成所有参数搜索。三个巨大参数控制只调用 equalAt，没有把巨大系数送进全参数前缀枚举；详见 [CONTROLS_SEMANTIC_REVIEW.md](CONTROLS_SEMANTIC_REVIEW.md)。

此次没有重复旧百万级 Python 区间／标量控制。现有新内核控制已覆盖新增量词的全部关键分支，独立工作集中于算法定义、推理方向、实际字串接口与控制解释。作者和运行专员提供的编译／公理审计日志应与本语义审查一并收录，不能相互替代。

