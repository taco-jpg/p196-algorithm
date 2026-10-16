# 620 结构化切片覆盖：独立语义补充审阅

**最终冻结版语义与连接审阅 PASS。** 本报告针对发布提交
`dc2123ae4a4513acfe75e0a6cd21c3b6a044bec4`，生成清单 SHA-256 为
`d2b92c7139f59fe1cb8268addd0d10073780275f06b109bc3cf72933f9170c03`。
101 个初态块、78 个短状态块、秩树和全部汇总接口已完成独立有限控制。
完整 523 模块的独立 Lean 编译及公理审计由 `/root/runtime_scout` 另行执行；
本报告不把有限控制或作者 pilot 记为该完整构建已通过。

审阅者：真实非作者专员 `/root/strategy_review`。新覆盖辅助模块由父代理
`/root` 编写；具体切片数据与检查模块由 `/root/scope_scout` 生成。审阅者未
修改这些 Lean 源码。这是同一会话团队内不同真实子代理的独立角色审阅，
对外发布使用同一 GitHub 账户；不是外部同行评审。既有语义检查器仍归属
Agent #124，既有七列实际投影接口的来源见 `source-pins.json`。

## 1. 已固定的辅助模块

`proofs/Agent104Prefix620DataCoverage.lean` 的审阅 SHA-256 为：

```text
d8d672edcda4b39d14247927ee7c7eef221e1da71bee68a0bb67f233006115f5
```

**辅助定理语义审阅 PASS。** 该模块通过原枚举的成员关系证明 `List.all`
性质，不要求比较整个大列表，也没有改变 `Agent124.PrefixK` 的原始枚举、
`Agent124.CodeCert` 的检查器或真实轨道语义。父代理报告该精确版本已经接受
Lean 内核检查，两个辅助定理只依赖 `propext`、`Quot.sound`；本节的独立结论
来自逐行语义审阅。具体实例的完整独立构建证据应另行绑定最终冻结模块。

## 2. 初始集合：所有长度 3 至 7

原始定义 `initialWordsK 7 6 2 0` 先枚举 `j ∈ List.range (7-2)`，将长度为
`j` 的十进制字接在 `[6,2,0]` 后面，再应用原 `initialOK 7` 过滤器。因此
`j=0,1,2,3,4` 精确对应完整长度 3、4、5、6、7。

新 `initialShortWords` 使用 `List.range 4`，枚举 `j=0..3`，且保留同一个
`initialOK 7`。所以长度 3..6 的所有原初始成员仍被覆盖。对于此固定前缀，
过滤后恰为 `[6,2,0,2,6]` 与 `[6,2,0,0,2,6]`；这里的偶中心条件来自原过滤器，
没有被新辅助模块删去。

`initial_all_of_slices` 对任意原初始成员拆出上述 `j`。若 `j<4`，它使用
`hshort`，并将原成员的过滤条件原样传入 `initialShortWords`。否则由 `j<5`
推出 `j=4`，再对原 `digitLists 4` 的递归定义拆出两位 `a,b<10` 以及
`z ∈ digitLists 2`。所得原字就是 `[6,2,0,a,b] ++ z`，属于
`initialSlice a b`。

辅助定理要求全部一百种 `(a,b)` 的切片检查成立。每片包含剩余两位数字的
全部一百种选择。长字分支没有再使用 `initialOK 7` 的假设是合法的：要求
整片都通过足以覆盖原过滤后的成员；而此处所有切片字长度均为 7，原过滤器
本来也全部接受。没有通过删除过滤条件来排除任何原初始状态。

冻结的 `InitialAll` 确实包含一项短初始检查和一百项长初始切片检查，共覆盖
10,002 个初始字。`p` 在辅助定理的所有假设和结论中相同，实际固定为
`initOKC ranks 11`。短分支引用 `initial_cover_short`、`initial_ok000`；
长分支穷尽 `a,b=0..9`，每组引用 `initial_cover_a_b` 与索引
`1+10*a+b` 对应的 `initial_ok`。所有一百项引用已逐项核对。

`init_620` 的结论是原 `initialWordsK 7 6 2 0` 上的完整 `List.all`，然后
直接调用原 `initialBounded_of_all`，得到无附加假设的
`initialBounded : InitialBounded 7 6 2 0 11 (R ranks)`。

## 3. 短字集合：原 mirror 和 symOK 完整保留

原 `symWords n` 从长度 `(n+1)/2` 的全体 `0..18` 半字出发，经 `mirror n`
镜像，再由 `symOK n` 过滤。新 `shortSlice n m a` 只固定半字的首个系数 `a`，
其余部分仍遍历 `lists19 m`，并使用同一个 `mirror n` 与 `symOK n`。

`short_all_of_slices` 的精确长度合同是 `(n+1)/2=m+1`。对任意原成员，它
用该等式展开半字枚举的第一层，获得 `a<19`、`tail ∈ lists19 m`；随后将
原过滤条件原样传给对应切片。故外端正性、奇宽中心偶数条件及全部镜像位置
都得到保留。

首系数范围明确包含 `a=0`。对应切片由原外端正性过滤为空，可以用空表检查
处理；不能在后续汇总中未经证明地遗漏这个分支。

| 宽度 n | 半字长度 | 辅助定理中的 m |
|---:|---:|---:|
| 1 | 1 | 0 |
| 2 | 1 | 0 |
| 3 | 2 | 1 |
| 4 | 2 | 1 |
| 5 | 3 | 2 |
| 6 | 3 | 2 |

宽度 0 无法满足该正半字长度合同，必须单独处理原 `symWords 0=[]`。
最终采用宽度 1、2 的直接小枚举以及宽度 3..6 各十九片的方案，共 78 个
用于正宽度的检查模块；它与原短字全集的覆盖范围一致。这里的“78”统计检查
模块，其中首系数为零的若干片实际为空。

冻结的 `ShortAll` 对每个短宽度的结论正是
`(symWords n).all (shortOKC ranks)=true`，再将 `n<7` 分为 0..6，调用原
`shortClosed_of_widths`，得到无附加假设的 `short : ShortClosed 7 (R ranks)`。
宽度 0 用 `decide +kernel` 检查原空集合；宽度 1、2 分别连接
`short_cover_w1`/`short_ok000` 与 `short_cover_w2`/`short_ok001`。
宽度 3..6 使用上述辅助定理，分别取 `m=1,1,2,2`，穷尽 `a=0..18`。
四个空切片索引 002、021、040、059 均保留并连接各自的检查。
所有 78 个局部等式和检查引用已逐项核对。

无需新建或假设实际轨道的短宽转移规则；这些检查仍调用原 `shortOKC`。

## 4. 最终端点合同

已逐行核对冻结的 `Agent104Prefix620.lean`。三个根定理的真实全限定名称为：

```text
Agent104.Prefix620.palindromeStarts620_iff
Agent104.Prefix620.ancestry_bound12
Agent104.Prefix620.no_196_620_palindrome
```

其精确声明如下，除这里写出的量化变量和数学前提外，没有未消解的证书、
树正确性、闭包、短字检查或初始秩界假设：

```lean
theorem palindromeStarts620_iff (P : Nat) :
    PalindromeStarts620 P ↔ Lychrel196.Palindrome P ∧
      ∃ e W, DecimalDigits.Canonical P e W ∧ 3 ≤ W ∧
        e (W - 1) = 6 ∧ e (W - 2) = 2 ∧ e (W - 3) = 0

theorem ancestry_bound12 :
    ∀ A P t, 0 < A → PalindromeStarts620 P →
      Lychrel196.orbit A t = P → t ≤ 12

theorem no_196_620_palindrome :
    ∀ t, ¬ PalindromeStarts620 (Lychrel196.orbit 196 t)
```

`PalindromeStarts620` 直接缩写原 `PalStarts3 6 2 0`，等价定理由 `Iff.rfl`
成立。canonical 数位按个位为索引 0；`W-1,W-2,W-3` 因此确实读取最高端的
6、2、0。`3≤W` 使这三次自然数减法对应真实位置。

`ancestry_bound12` 调用原 `ancestry_bound_of_R`，参数固定为
`7,6,2,0,11`；`3≤7`、`2≤6` 由 `decide +kernel` 给出。唯一的证书参数是
具体的 `R ranks`，随后实际传入 `allRows`、`short`、`initialBounded` 三个
已声明的无条件事实。其类型分别是：

```text
allRows        : RowsClosed 7 (R ranks)
short          : ShortClosed 7 (R ranks)
initialBounded : InitialBounded 7 6 2 0 11 (R ranks)
```

原祖先接口明确保留 `0<A`。`t=0` 由自然数上界直接处理；`t=s+1` 时，只对
最后一步前驱时间 `s` 使用秩界 `s≤11`，然后推出 `t≤12`。没有负时间，也
没有从无溢出单独推断无内部进位；最后一步的回文条件仍在原桥接证明中使用。

`no_196_620_palindrome` 调用同一个 `no_196_of_R`，额外通过
`decide +kernel` 给出 `11+1≤100`，并由既有前 100 步无回文结论封闭
所有时间 `t`。它只排除 196 轨道中的 620 首部回文目标族。12 是上界，
没有最优性、所有回文排除或 196 为 Lychrel 数的新增结论。

## 5. 独立有限控制和作者 pilot 的证据等级

`independent_slice_control.py` 已实际运行并退出 0，其记录的清单 SHA 与
最终冻结版完全相同。它没有导入作者生成器或逆像函数，而是独立枚举数位与
半字，解析 Lean 数字字面量，核对局部等式及汇总引用：

| 检查项 | 独立结果 |
|---|---:|
| 全部生成源指纹 | 510 项一致 |
| 初态块 / 初态字 | 101 / 10,002 |
| 短状态块 / 短状态字 | 78 / 10,467 |
| 短状态宽度 0..6 计数 | 0, 9, 18, 180, 342, 3,420, 6,498 |
| 初态局部等式 / 短态局部等式 | 101 / 78 |
| 原检查器合同和相同秩树引用 | 全部 179 项 |
| 对照原冻结 JSON 的初态最大秩 | 11 |
| 普通整数计算得到的排名短边 | 恰为原报告六条 |

该控制同时验证每个初态块使用 `initOKC ranks 11`、每个短态块使用
`shortOKC ranks`，而不是仅验证数据块数量。局部定义等式用 `rfl`，布尔
检查用 `decide +kernel`；脚本检查这些声明和引用的内容，本身不执行 Lean。

实际读取并核对了作者 `generator/evidence/finite-pilot-003/verification.json`
及其全部五条命令的日志 SHA。报告 SHA-256 为
`f1aaca77506b650d612fef1b58a7910b53977cb21a89a2fd3b3aa74d363a95d9`。
五条命令均退出 0：三项代表性布尔块检查，以及包含全部 101/78 项局部等式
的 `InitialCoverage`、`ShortCoverage`。后两项耗时分别为 16.723 秒和
70.931 秒。这是明确标为 `AUTHOR_BUILD`、`independent_review=false`
的局部 pilot，不能代表全部 179 个布尔块或全部 523 模块已编译通过。

## 6. 实际秩树、长行汇总与已发布来源

`independent_final_connection.py` 另作有限控制并实际退出 0。它只解析冻结
Lean 中的 `.node`、`.empty`、叶引用和合取字面结构，不复用生成器的造树
程序，也不重做完整逆像搜索。

首先，程序遍历实际 `ranks` 定义，验证 256 个叶定义各引用一次、总计
59,189 个节点且编码键严格递增；它用独立的位值公式
`19^length + Σ word[i]*19^(length-1-i)` 重新编码原 JSON 的每个字。
全部 `(code,rank)` 与实际树逐项相同，因此原始图数据的有限控制确实绑定
到这份 Lean 字面数据。

其次，程序将 `allRowsAll` 的每个合取分支与实际树形递归匹配：256 个
`rows_leaf` 各使用一次，255 个 `row_branch` 各使用一次，每个分支的具体
编码键和秩均正确。全部叶合同调用原 `allRowsC_sound`、检查同一
`rowOK ranks 7`；内部节点也检查同一合同。最后 `allRows` 直接由
`rowsClosed_of_all (7≤32) allRowsAll` 给出。叶块和内部节点没有被初态或
短态切片替代。

来源绑定分两级明确记录在 `independent_final_connection.json`：

- 全部 510 个新模块、13 个既有模块、清单、冻结文档和原输入 JSON，共
  526 个路径的实际本地内容计算得到的 Git blob ID，均与发布提交
  `dc2123ae4a4513acfe75e0a6cd21c3b6a044bec4` 的树记录一致；本地 SHA-256
  同时与相应冻结来源清单一致。
- 对 11 个关键 Lean 文件及生成清单、冻结文档，额外实际读取发布 Git
  blob 内容并逐字比较，13 项全相同。报告不会将其余路径的内容寻址比对
  冒称为逐项 Git blob 内容回读。

11 个关键文件为 DataCoverage、DataInitialWords、DataShortWords、
InitialCoverage、ShortCoverage、InitialAll、ShortAll、DataTree、RowsAll、
RowsBranch 及顶层 Agent104Prefix620。精确路径、SHA-256、Git blob、字节数
和三个端点合同另见 `structural-coverage-pins.json`。

## 7. 最终验收状态与先前不足状态的关系

原 `SEMANTIC_REVIEW.md` 首次报告时尚无完整具体实例；本补充报告现已完成
最终冻结版的数据、覆盖、汇总和真实整数端点的独立语义审阅。旧整表
`DecidableEq` 的内存失败以及整表 `rfl` 的栈溢出仍是实际发生过并保留的
失败尝试。它们没有被改记为通过；最终采用的是上述成员关系辅助定理与
局部定义等式的不同覆盖构造。

`SOURCE_FREEZE.json` 中的 `independent_review=PENDING` 是冻结时点的历史
状态，原文件保持不变；此报告更新语义审阅结论。完整 Lean 编译和全闭包
公理审计的状态仍须从 `/root/runtime_scout` 针对同一发布来源的实际结果
读取。当前结论分层如下：

| 层级 | 此报告结论 |
|---|---|
| 原始 JSON 的完整独立有限控制 | PASS，见 `independent_control.json` |
| 新切片数据、原枚举覆盖和所有引用 | PASS，见 `independent_slice_control.json` |
| 实际编码树、长行合取树、已发布来源绑定 | PASS，见 `independent_final_connection.json` |
| 最终三根定理的数学意义、前提及同树连接 | 独立语义审阅 PASS |
| 作者局部 pilot | 已核对五条命令 PASS，范围明确受限 |
| 最终 523 模块独立 Lean 与公理审计 | 本报告冻结时仍另行进行，不提前标为 PASS |

上述有限程序均可在同一工作树直接运行。切片程序的原始清单包含作者绝对
路径，重放应使用其记录的工作树布局；最终连接程序另支持 `--repo` 指定
具有相同平面来源和存档的检出目录。没有重建整个 739 实例，也没有修改已
冻结的 mass 证明及其审阅证据。
