# 参数集合判定模块：具名独立源码语义审查

## 结论、版本与真实角色

复核者为真实子代理 `/root/word_intervals`。被审模块 `Agent102ParameterSetDecisions.lean` 由母代理 `/root` 编写；本复核者完整读取实际冻结源码，未编写或修改该文件。审查未发现需要修改的语义问题。

- 实际源码长度：4,880 字节。
- SHA256：`bc919ecc2700c9cac5c36285ddeda42b3e2d1e02ed086532ace33f78d5fb8f5c`。
- 审查覆盖：全部 9 个布尔定义、10 条规格定理及底部 10 条 literal 公理审计指令。
- 本目录的同名源码副本与实际受审版本逐字一致。

本轮只做独立源码语义审查，没有运行 Lean。母代理报告的验证是 11 个依赖模块 fresh 构建成功后，核对字节并增量编译此模块；这不能描述为本复核者执行了独立 fresh 12 模块构建，也不能将“11 fresh + 1 incremental”改称另一轮 fresh 12。

依赖 `Agent102RunWord`、`Agent102ParameterIntervalAlgebra`、`Agent102ParameterIntervalCompact` 由本复核者编写，它们的验证仍属于作者验证。本报告的独立角色针对母代理的新 Decisions 模块，不冒称整个依赖链均独立。

## 实际核对的依赖语义

除完整读取 Decisions 外，本复核者完整读取当前 `Agent102AffineRunParameterSets.lean`，其长度为 4,541 字节，SHA256 为 `9b0860cfec3ecfd3059f029a658ed15b63ad2369dea3d6f760c24b207bb53897`。

关键接口 `holds_equalityRegions A B k` 对任意自然数参数给出：

`holds (equalityRegions A B) k ↔ wordAt A k = wordAt B k`。

这个桥以实际总宽相等和实际 run 区间重叠时数字一致为依据。重叠区域保留两条自身正长度不等式及两条交叉不等式，没有把空 run 的端点接触错误算作冲突。总宽检查也保留，因此只满足数字兼容不能绕过词长度差异。

另核对了 `CountExpr.value/pieces`、`comparisonRegion`、`ltRegion/leRegion/eqRegion` 的实际计算定义及相关接口。原子值使用原仿射表达式的 `Int.toNat`，不是仅在尾部成立的仿射替代式。调用链没有为 Decisions 增加 cutoff 或正长度前提。

实际读取了 `wordAt_reverse` 的无前提陈述：

`wordAt A.reverse k = (wordAt A k).reverse`。

因此回文判定依赖的是实际数字词反序，不是 run 列表语法反序相等。对 PiecewiseCounts 的全部独立重建和审查由另一个真实子代理负责，本报告只记录上述实际核对范围。

## 非空判定的假分支

`inhabited_false_iff R` 的陈述精确为：

`inhabited R = false ↔ ∀ k, ¬holds R k`。

正向若某个参数属于区域，已验证的 `inhabited_eq_true_iff` 会给出布尔值为真，与假结果矛盾。反向对实际布尔值分情况；若为真，规格提供某个属于区域的参数，与全称非成员前提矛盾。

这里使用的是已验证布尔计算的两种实际结果，不是把“未能证明非空”当作空域。量词明确覆盖全部自然数。

## 区域等价是外延等价

`equivalentRegions R S` 检查两个集合差的非空值均为假：

- `R ∩ complement S` 为空；
- `S ∩ complement R` 为空。

`equivalentRegions_spec` 的结论是：

`equivalentRegions R S = true ↔ ∀ k, (holds R k ↔ holds S k)`。

展开两个假非空规格与精确交／补规格后，证明得到两个方向的包含。每个包含方向都使用显式 `Classical.byContradiction`，将“无法同时属于一边且不属于另一边”转换为另一边的实际成员命题。反向则分别用点态等价的正向和反向排除两个差集中的成员。

两个差集都被检查；没有把单向包含误作相等。结论也没有要求区间顺序一致、项数一致、无重复、互不相交或端点表示相同。

## 四种相等／不等量词

记 `P(k)` 为 `wordAt A k = wordAt B k`，`E = equalityRegions A B`。

| 布尔定义 | 实际计算 | 真值规格 |
|---|---|---|
| `hasEqualParameter` | `inhabited E` | `∃ k, P(k)` |
| `hasUnequalParameter` | `inhabited (fastComplement E)` | `∃ k, ¬P(k)` |
| `everyParameterEqual` | `!hasUnequalParameter` | `∀ k, P(k)` |
| `everyParameterUnequal` | `!hasEqualParameter` | `∀ k, ¬P(k)` |

补运算放置正确：所有参数相等是否定“存在不等参数”；所有参数不等是否定“存在相等参数”。没有交换全称与存在的补关系。

两个存在规格直接由区域非空规格产生实际自然数见证。`everyParameterEqual_spec` 经区域补与假非空规格得到逐点双重否定，再使用 `Classical.byContradiction (h k)` 消去它。反向用给定相等结果与不等假设直接矛盾。`everyParameterUnequal_spec` 则直接得到全称不等。

经典逻辑只出现在证明中，没有被放进九个可执行布尔定义。当前接口返回布尔值并证明见证存在；没有另外返回见证下标的提取函数。

## 四种回文量词

四个回文布尔定义分别将上面的两个模板设为 `A` 与 `A.reverse`。相应四条规格使用实际 `wordAt_reverse`，分别得到：

- 存在参数使实际词为回文；
- 存在参数使实际词非回文；
- 所有参数的实际词均为回文；
- 所有参数的实际词均非回文。

非回文的存在性与全称命题均沿用正确的相等／不等量词，未发生额外的否定交换。

## 空域、全集与零参数

所有判定直接量化 `Nat`，没有省略零参数，也没有先选取有限参数前缀。空区域和全集使用前面已验证的区域非空与补集规格处理；倒置有限区间、零宽有限区间和无穷上端点没有被排除。

八条词规格没有附加模板非空、段长为正、数字非零、相邻数字不同或参数超过某阈值的前提。因此这些边界输入沿原始 RunDefs 语义处理。

## 可执行路径与结论范围

实际执行路径是有限区间列表的构造、去空、求交、求补和非空检查。Decisions 的计算定义没有调用 `Nat.range`、参数前缀遍历、`wordAt` 或 `List.replicate` 来展开数字词；`wordAt` 出现在正确性规格中。

下游集合构造使用有限 run 表和整数系数运算，上游 `CountExpr.pieces` 在每次加法组合后过滤空 domain。当前 Compact 在补运算前过滤输入，并在每步交之后去空。这里没有据此增加一般多项式复杂度、最小区间表示或无重复输出承诺。

被判定的是静态仿射 run 模板族的自然数参数，不是反转加法的迭代时间；本模块没有引入动态迭代闭包命题。

## 公理记录与源状态

实际源码底部对全部 10 条规格定理有 literal `#print axioms` 指令。母代理保存的作者编译和审计日志应另行配套；本轮未执行这些命令，不冒称本复核者重新产生了审计结果。

母代理已说明首个 Decisions 尝试的失败涉及 `by_contra` 不可用和双重否定证明语法，最终版使用实际可读的 `Classical.byContradiction`。本报告依据最终冻结源审查，不改写或重新分类母代理保留的原始失败记录。

受审源在读取、保存副本和完成报告时均核对指定 SHA256，未修改任何根作者源码或冻结依赖。本目录保留具名报告、被审源副本、实际依赖阅读记录与 SHA256。
