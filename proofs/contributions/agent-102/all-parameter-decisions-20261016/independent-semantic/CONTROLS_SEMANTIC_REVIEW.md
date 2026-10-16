# 新全参数控制模块的独立语义审查

审查者：/root/research_map。控制作者与内核运行者：/root/lean_runtime。审查者完整读取冻结源并核对三组巨量公式，没有执行 Lean，没有运行或新造重复的 Python 测试矩阵。

冻结源：[sources/Agent102AllParameterControls.lean](sources/Agent102AllParameterControls.lean)，9187 字节，SHA256 a1bb882b1b8396406f82e9814bc4522d2f2d13b96c7e859fad0d6d650c1914d2。运行专员已确认该字节版本冻结。本次源码语义审查通过，无需修改数学陈述。

## 1. 小族控制覆盖的是不同量词情况

| 族或目标 | 精确字面性质 | 新控制的实际作用 |
| --- | --- | --- |
| moving 与 fixed 3 | 词相等 iff k=3 | 四个 equality Bool 为假、真、假、真；确认唯一前缀见证没有被尾部不等吞掉 |
| growing | 1 重复 k 次再接单个 2，回文 iff k=0 | 明确包含参数0；尾部非回文但 somePalindromic 为真 |
| declining | 1 重复 max(0,3−k) 次再接单个 2，回文 iff 3≤k | 尾部全回文但 allPalindromic 为假；有限前缀反例被保留 |
| alwaysDifferent | 1 重复 k+1 次，再接 2 重复 k+1 次 | 所有参数非回文；两个存在／全称非回文 Bool 为真，两个回文 Bool 为假 |
| symmetric | 1 重复 k 次、单个2、1 重复 k 次 | 所有参数回文；k=0 仍为单个2 |
| erased 与空目录 | 显式零段和 −k 长度段均为空 | allEqual erased [] 为真；空词回文，不存在空词非回文参数 |
| leadingZero | 对所有 k 都是实际列表 [0,1] | 与 [1] 字面不等且不回文；正长度的零数位没有被删去 |

其中 moving_fixed3_only_eq 复用已有 AffineBoundary.moving_fixed_eq_iff，而不是仅靠有限测试猜出唯一根。growing_palindrome_iff、declining_palindrome_iff 给出整个自然参数域的解析 iff，不是只报告少数参数的 Bool 样本。证明 replicate_one_two_palindrome_iff 在 n=0 与 n>0 两种情形区分首尾数位，适用任意 n。

每组 closed Bool 后，另有通过公开规格得到的真实词命题，因此证书不仅记录程序输出，也接回它意图证明的 forall/exists List 命题。四个 Bool 的混合值说明不能把 !allPalindromic 当成 allNonpalindromic。

## 2. leadingZero 的准确解释

源码中的 leadingZero 是列表首位为0的 [0,1]；本模块只证明它与 [1] 字面不等和它本身非回文。这里没有 Canonical、evalL 或普通整数值相等命题。

若按原仓库低位优先惯例解释两个列表，数值分别是10与1；因此这个控制不能被宣传为“数值相同但字串不同”的十进制反例。本审查已将这点反馈给作者，作者确认报告采用“列表首位为0”的描述。数学控制本身正确，不需要扩大范围或改源。

## 3. 三个巨大单参数证书的真实含义

源码 huge 数值字面量已由本审查的独立文本／整数核对确认：共有101位，精确等于 H=10^100。这只是字面数值核对，不是 Lean 执行。

所有巨大控制都在参数 k=H 调用 equalAt：

1. hugeSplit 的两个数字1段各长 H²+H，中间数字7段长度0；hugeMerged 的单段长2H²+2H。合并后词完全相同，huge_split_at 为真。
2. hugeOne 长 H²+H；hugeWidthChanged 長 H²+H+1。两侧所有共同位置相同但总长差1，因此 huge_width_at 为假。它检验保留总宽条件的必要性。
3. hugeNegative 的额外数字5段长度为 max(0,−H²+H)=0，剩余数字1段与 hugeOne 相同，所以 huge_negative_at 为真。

三条相应 semantics 定理都通过 equalAt 的无阈值 iff 得到实际词等式或不等式。它们没有展开 H² 规模的列表，也没有调用 allEqual、someEqual 或相应巨大 cutoff 的 List.range。大参数的可核验证书因此没有被偷换成“全参数枚举巨大前缀也很快”的性能承诺。

## 4. 32 条显式定理的逐组覆盖

完整审查包括：

- 通用列表引理1条：replicate_one_two_palindrome_iff。
- moving 组4条：解析唯一根、四Bool组合、存在／不等存在命题、有限前缀见证。
- growing 组5条：word公式、回文iff、Bool组合、存在命题、k=0前缀见证。
- declining 组5条：word公式、回文iff、Bool组合、存在命题、前缀阻碍。
- alwaysDifferent 组2条：Bool组合及全称非回文。
- symmetric 组2条：Bool组合及全称回文。
- empty／zero 组3条：closed控制、实际空词等式、空词回文。
- 列表首零组4条：实际word公式、closed控制、全称不等、全称非回文。
- 巨大单参数组6条：3个closed Bool与3个实际词命题。

合计32条，均在冻结源中具有对应声明与 #print axioms 指令。文本里存在指令不等于本审查者执行了指令。

## 5. 运行证据的归属与本次停止点

运行专员另报告：attempt-002 的十模块 clean --trust=0 -j1 -DElab.async=false 全部 exit0；32条 Controls literal 审计与另两模块合计48条新定理均通过；13个闭证书无公理依赖；完整 module-origin 审计覆盖297条定理、并集为标准三种公理；十个 Bool 入口的依赖审计没有到达 word/wordAt/replicate，而 all/some 确实到达 range。这是其执行结果，需附其原始日志，不记作本审查者独立执行。

作者也保留了默认 maxRecDepth 不足的首次失败，冻结源只将该执行资源限额调为8192。这个选项影响证明归约允许的深度，并非添加数学公理或替代 kernel 检查；具体成功状态仍依实际运行日志判断。

这些控制已覆盖本次新增量词与压缩执行的具体剩余风险。旧核心已有独立的大范围 Python 控制，本次不再重跑同类百万级配对，也不增加镜像实现的测试来制造数量。审查结论限于精确源语义与明确提供的证据类别。

