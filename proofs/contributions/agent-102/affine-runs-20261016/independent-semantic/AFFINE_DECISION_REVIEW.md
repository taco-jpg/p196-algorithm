# Agent102AffineDecision 独立源码语义审查

审查者：真实子代理 /root/research_map。作者为母代理 /root；本审查者没有参与新模块实现，没有改动数学模块，没有执行 Lean。本文补充 AFFINE_RUN_REVIEW.md，不替代核心五模块的既有审查。

## 结论与冻结对象

对冻结的 Agent102AffineDecision.lean 全文及其依赖契约逐项实读后，未发现需要修改的数学语义问题。可执行的 fastEqualOnTail 确实只处理有限 run 目录的系数、数位和端点次序；wordAt 与 equalityCutoff 仅出现在正确性定理和原判定值的等价证明中，不进入新 Bool 的定义。

- 源路径：proofs/Agent102AffineDecision.lean。
- 审查快照：[Agent102AffineDecision.review-snapshot.lean](sources/Agent102AffineDecision.review-snapshot.lean)。
- 工作树 HEAD 实读：cba5dc441289bbed383972aa522a45c473879396。
- SHA256：1f41f5159bb5c2b25ebdc272d64482c27bb345003a55f0e1b3a4c495acd4fbe4。
- 文件长度：7071 字节。
- 独立字节 pin：[affine-decision-source-pin.json](affine-decision-source-pin.json)。

母代理另报告 attempt-005 六模块及后续七模块构建、公理审计通过；这些属于其运行证据。本文只断言实际发生的源码审查和文件字节核对。本文没有将旧 Python 控制改称为新 Bool 的执行测试，也没有将文本中的 #print axioms 指令视为本审查者执行过的审计。

## 1. 可执行定义保存了完整的等价条件

新判定在源码中是以下两个有限条件的 Bool 合取：

1. widthAffine A 与 widthAffine B 的斜率、截距分别相等。
2. 对 spanSpecs A 与 spanSpecs B 的每一对区间，若它们最终有正长度相交，则其数位相同。

第一个条件保证真实总长度相等。只有相交数字一致不能排除一侧存在额外后缀；例如单个数位 4、长度分别为 1 和 2 的两个词，所有真正相交的位置都相等，但两个词不相等。新定义没有漏掉这一条件。

第二个条件枚举所有区间对，并不要求两侧 run 数量相同、不要求第 i 段对应第 i 段，也不要求目录已合并相邻相同数位。已经在 RunWord 中证明的覆盖与数位读取定理提供实际列表语义；新模块只把其有限条件改写为尾部系数条件。长段被另一目录拆成若干相同数位短段时，判定仍可通过。

新程序没有 List.replicate、wordAt、equalOnTail 或 equalityCutoff 调用。它仍要进行有限精度整数运算，系数数值大小会影响运算成本；此处没有证明机器时间或内存的渐近界，也不把源码中可能重复计算 spanSpecs B 的表达式假定为已被编译器缓存。准确的收益是：目录循环大小不随展开词的总长度增加。

## 2. 字典序只能在正确阈值后连接真实端点

Affine.ltOnTail f g 定义为：

    f.slope < g.slope
      或 (f.slope = g.slope 且 f.intercept < g.intercept)

这个定义适用于整数系数，包括负斜率。它描述最终严格次序，并不声称在任意小参数处等于数值比较。endpoint_ltOnTail_iff 的实质是，在两个被比较函数均来自 endpoints A ++ endpoints B 且 k ≥ equalityCutoff A B 时，将该字典序精确连接到 Int.toNat 后的自然数端点严格次序。

证明中的两个必要环节都存在：

- compareCutoff_le_pairCutoff 加 pairCutoff_le_equalityCutoff 给出当前端点对所需的比较阈值。原标量界为 |b_f| + |b_g| + 1；不是把两个截距之差的绝对值误认成当前源定义。
- combined_endpoints_nonneg 分别证明 f.eval k 与 g.eval k 非负。因此 Int.toNat 不会把两个不同负数同时截为 0；源码没有无条件把整数严格不等式运到自然数。

核心 equalityCutoff 同时包含两侧 lengthCutoff 和 endpoints A ++ endpoints B 全组合的 pairCutoff。端点目录包含总宽及每段的 lo、hi，故同一列表内部的两个自身端点也受比较界控制。这与下面四项交叠条件完全匹配。

## 3. 四项交叠条件没有遗漏空段边界

AffineSpan.overlapsOnTail s t 逐项要求：

    s.lo < s.hi
    s.lo < t.hi
    t.lo < s.hi
    t.lo < t.hi

这里每个“小于”都是 ltOnTail。span_overlapsOnTail_iff 对四项分别调用 endpoint_ltOnTail_iff，再用既有 Span.overlaps_iff_four 组合，结果恰为自然数区间的真正正交叠：

    max s.lo t.lo < min s.hi t.hi

两个自身严格比较必不可少。例如空内部段 [1,1) 与 [0,2) 满足两条交叉不等式，却没有任何共同覆盖的位置。当前四项形式把它排除，所以零段上任意数位不会使两个相等词被误拒绝。

负斜率段在超过其长度阈值后消失：positivePart 将其长度函数置为零；这样的 span 仍可留在目录中，但自身 lo 与 hi 系数相同，自身严格比较为假。负常数段同理。斜率为零、截距为零的真零段也正确为空。一个“数位为 0、长度为正”的段则不会被删去；数位值与段长是不同字段。

## 4. 总宽的系数相等是有阈值的数学结论

width_eq_iff_coefficients 的契约是：

    k ≥ equalityCutoff A B →
      ((wordAt A k).length = (wordAt B k).length
        ↔ widthAffine A 与 widthAffine B 的斜率、截距均相等)

其证明先把两个 widthAffine 放入共同端点目录，取得对应 compareCutoff；再使用 Affine.eval_eq_iff，将充分大参数处的相等提升为两项系数分别相等；最后通过 widthAffine_eval 运回真实列表长度。

这一步没有把“两个仿射式在某个任意参数处相等”错当成系数相等。斜率不同的两个式子可以在远处有一个孤立交点，但正确比较阈值已越过这种可能性。此前核心审查中保留的大参数孤立相等反例正说明该前提不可删除。

## 5. 全部 11 个显式定理的契约与证明连接

| 声明 | 精确作用及独立核查 |
| --- | --- |
| endpoint_ltOnTail_iff | 共同目录成员、k ≥ K、两侧端点非负齐备后，尾部字典序等价于真实自然数端点比较。 |
| width_eq_iff_coefficients | 使用总宽目录成员、eval_eq_iff 与 widthAffine_eval，取得真实长度相等的完整系数判据。 |
| span_overlapsOnTail_iff | 四个端点成员均显式给出；四次比较逐项对应真正正交叠，包含两个自身正长度条件。 |
| fastEqualOnTail_iff_coefficients | Bool.and、decide 与两层 List.all 精确展开为宽度系数等式和所有区间对的条件，不丢弃空目录情形。 |
| fastEqualOnTail_iff_wordAt | 在 k ≥ K 下双向结合无假设目录对齐的 wordAt_eq_iff_spans、宽度系数等价和交叠等价。 |
| fastEqualOnTail_eq_equalOnTail | 在 k = K 取得前一定理，分别讨论新 Bool 的 false/true，证明两个 Bool 的值真正相等。 |
| fastEqualOnTail_spec | 经 Bool 值等式复用 equalOnTail_spec，真值等价于所有 k ≥ K 的真实词相等。 |
| fastUnequalOnTail_spec | 经 Bool 值等式复用 unequalOnTail_spec，假值等价于所有 k ≥ K 的真实词不相等。 |
| fastPalindromicOnTail_eq | 定义性地将两侧取为 A 和 A.reverse，得到与原 palindromicOnTail 相同的 Bool。 |
| fastPalindromicOnTail_spec | 复用原反转桥与回文尾部真值契约，阈值为 palindromeCutoff A。 |
| fastNonpalindromicOnTail_spec | 复用原回文尾部假值契约，结论确为所有充分大参数的真实词非回文。 |

fastEqualOnTail_iff_wordAt 中两个方向的交叠转换也已核对：由有限尾部条件推出词相等时，以 span_overlapsOnTail_iff 的反向把实际交叠转为尾部交叠；由实际词相等推出有限条件时，用正向把尾部交叠转为实际交叠。没有把 mp/mpr 对调。

## 6. false 分支与反转接口

新 Bool 和旧 Bool 的相等证明中，false 分支先用 iff_wordAt 的反向证明否定 K 处真实词相等，再化简旧 decide；true 分支直接由正向取得真实词相等。随后两个 forall-tail 规格都继承已证明的稳定性，因而没有使用不成立的“非全称蕴含全称否定”。

fastPalindromicOnTail A 只调用 fastEqualOnTail A A.reverse。既有 wordAt_reverse 对所有自然参数都把反转 run 目录精确连接到实际词反转，单段 replicate 的反转保持数位与长度。这包括空目录、全零长度目录、相邻相同数位和会消失的负斜率段。

空词的字面回文判定为真。这个数学约定适合 List 层，但不能静默改写成某个正整数的十进制位表示或安全轨道。源码没有给 digit 添加小于 10 的假设，没有 canonical numeral 前提，也没有引入 normalize、stepWord 或实际轨道时间。

## 7. 对下一阶段接口的明确边界

这个模块输出的是尾部常值判定，不接受任意参数 k。它不能直接用在 k < K：positivePart 是最终表示，ltOnTail 是最终次序，二者都可能在前缀失真。

如后续正式认领“任意参数的压缩 Bool”，应在 runsAt A k 的真实截断长度上，复用已有无阈值定理 word_eq_iff_count_sum_and_overlap_digits；然后独立证明有限前缀检查与本尾部规格组合后的全参数量词。那是下一项可审查工作，不是本冻结模块已经提供的接口。全参数一词只指输入模板参数，不给 actual reverse-add 轨道结论。

## 8. 证据分类

- 本文：独立源码语义审查，通过；没有执行 Lean。
- [AFFINE_RUN_REVIEW.md](AFFINE_RUN_REVIEW.md)：核心区间与尾部证明的独立审查、两次已实际执行的有限 Python 控制及来源归属。
- [sources/](sources/)：实际源码快照，不是重新写出的近似伪码。
- 母代理与 lean_runtime 的 fresh build、literal/module-origin 公理审计：另附其真实日志，本文不替代也不虚报。

