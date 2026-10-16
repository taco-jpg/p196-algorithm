# Agent102AffineDecision 独立源码审查与清洁重建

## 结论与审查身份

结论：**PASS，未发现阻断性正确性问题，无需修改冻结数学源码。**

被审查的 `Agent102AffineDecision` 由母代理编写；本次源码审查、独立构建和具体证书由真实子代理 `lean_runtime` 执行。该子代理曾编写依赖 `Agent102AffineArithmetic`，因此本记录明确是对母代理所写 Decision 模块的独立审查，以及对完整依赖闭包的清洁重建；没有把自己过去的算术作者检查冒称为外部独立审查。

冻结 Decision 源为 7071 字节，SHA-256：

```text
1f41f5159bb5c2b25ebdc272d64482c27bb345003a55f0e1b3a4c495acd4fbe4
```

检查前后六个仓库原始源文件的散列均一致。精确源闭包见 `SOURCE_PINS.json`，全部源快照见 `source/`。本次未执行 Git 写入。

## 完整语义审查

### 快速布尔计算只依赖有限段数据与系数

`fastEqualOnTail` 首先比较两个 `widthAffine` 的斜率和截距，然后使用两个有限段表的 `List.all` 检查每对实际尾部交叠段是否数字一致。

`widthAffine` 只对各段 `length.positivePart` 作仿射系数加法。`spanSpecsFrom` 同样通过系数加法累积左右端点。`positivePart` 只判断斜率及零斜率截距的符号，选择原仿射数据或零。其计算没有参数 `k`，也没有长度值的字面展开。

`Affine.ltOnTail` 是斜率优先、截距其次的严格字典序，具有构造性 `Decidable` 实例；`AffineSpan.overlapsOnTail` 保留四条严格比较，其中两条为各区间自己的正长度条件。零长度段不会因两条交叉不等式为真而被误当成有效交叠。

`fastPalindromicOnTail` 仅对有限段表作 `reverse` 后调用上述快速判定。源码中 `equalOnTail` 与 `wordAt` 出现在正确性证明或定理陈述中，不属于快速布尔定义的计算调用。

### 正确性接口覆盖真、假与回文两面

| 定理 | 实际检查的逻辑作用 |
|---|---|
| `endpoint_ltOnTail_iff` | 对共同端点集中的任意两个端点，在统一界之后，将严格系数字典序与自然数端点值比较建立双向等价；共同端点非负假设已被实际证明并使用。 |
| `width_eq_iff_coefficients` | 在同一界之后，总词长相等当且仅当总宽度仿射数据的两项系数相等。没有省略总宽度条件。 |
| `span_overlapsOnTail_iff` | 四条系数严格比较恰好对应自然数区间的正长度交叠，包括零段边界。 |
| `fastEqualOnTail_iff_coefficients` | 布尔合取与嵌套 `List.all` 恰好表示宽度系数相同以及全部交叠段数字相同。 |
| `fastEqualOnTail_iff_wordAt` | 对每个满足界条件的 `k`，快速布尔真值与原始字面展开词相等具有完整双向等价。 |
| `fastEqualOnTail_eq_equalOnTail` | 快速布尔与已有精确尾部布尔扩展相等；该证明中的旧布尔计算不进入快速定义的值依赖。 |
| `fastEqualOnTail_spec`、`fastUnequalOnTail_spec` | 真分别等价于界后处处相等，假等价于界后处处不等。反向方向也实际给出，不只是单向充分条件。 |
| `fastPalindromicOnTail_eq`、`fastPalindromicOnTail_spec`、`fastNonpalindromicOnTail_spec` | 利用段表反转对应字面词反转，得到回文与非回文的完整真假双向规格。 |

已完整读取 Decision、RunEndpoints、AffineRuns 的全部源码，并按精确不变散列沿用此前完整读过的 RunDefs、RunWord、Arithmetic 源码。负斜率、零斜率负截距、空段表、零长度段和相邻同数字段均未被添加额外限制。

## 实际定义依赖检查

`ExecutableDependencyAudit.lean` 从两个快速布尔入口出发，检查实际 Lean 环境中项目声明的类型和值表达式所引用的常量；递归展开这六个项目模块的定义，标准库实现作为既有依赖边界。扫描结果：

| 入口 | 到达的项目常量数 | 禁止计算依赖 |
|---|---:|---:|
| `Agent102.fastEqualOnTail` | 24 | 0 |
| `Agent102.fastPalindromicOnTail` | 25 | 0 |

显式禁止集包括 `word`、`wordAt`、`runsAt`、`spans`、`spansFrom`、`Affine.eval`、全部长度与比较 cutoff 函数、旧 `equalOnTail`/`palindromicOnTail`、`AffineSpan.at` 与 `List.replicate`。没有到达其中任何一项。

实际扫描保留一个需要解释的名字：`Agent102.lengthCutoff.match_1`。额外打印检查表明，它的完整定义只是：

```lean
fun motive x h_1 h_2 => List.casesOn x (h_1 ()) fun head tail => h_2 head tail
```

这是列表分支选择的共享辅助定义，不调用 `lengthCutoff`，也不计算阈值。完整输出保存在 `logs/MatcherInspection.log`；未通过字符串过滤隐去这一项。

这是实际定义依赖与源码检查证据，不把常量数量解释为运算次数，也不宣称已经形式化运行时间或位复杂度。

## 清洁构建与公理审计

在新的 `decision-review-001/source` 中按以下顺序构建，从而不复用母代理项目编译产物：

```text
Agent102RunDefs
Agent102AffineArithmetic
Agent102RunEndpoints
Agent102RunWord
Agent102AffineRuns
Agent102AffineDecision
LiteralAudit
ModuleOriginAudit
ExecutableDependencyAudit
LargeCoefficientExamples
```

每条命令均为官方 Lean 4.19.0、commit `6caaee842e94`：

```bash
LEAN_PATH=. /absolute/path/to/lean \
  --trust=0 -j1 -DElab.async=false \
  -o MODULE.olean MODULE.lean
```

所有命令均退出 0。后续 `MatcherInspection.lean` 也在同样的 `--trust=0 -j1 -DElab.async=false` 下成功运行。所有原始日志均保留于 `logs/`。

`LiteralAudit` 对新增的全部 11 个命名定理逐条执行 literal `#print axioms`。完整 module-origin 审计覆盖六模块的 200 个定理常量，其中包括生成辅助、结构派生与命名定理；这不是 200 项新数学成果的计数。

| 原始模块 | 被审计定理常量数 |
|---|---:|
| Agent102RunDefs | 25 |
| Agent102AffineArithmetic | 38 |
| Agent102RunEndpoints | 42 |
| Agent102RunWord | 49 |
| Agent102AffineRuns | 29 |
| Agent102AffineDecision | 17 |

200 个定理的公理并集为 `{propext, Classical.choice, Quot.sound}`。没有被审定理依赖 `sorryAx` 或其他公理。

另外单独记录了 5 个标记为 unsafe 的 `List.mapTR`/`List.flatMapTR` 专门化实现声明，完整名字见 `verification.json`。它们没有出现在任何被审定理的公理集合中；没有把它们从清单中删去或计作数学公理。

## 大系数具体内核证书

`LargeCoefficientExamples.lean` 使用十进制 101 位整数 `H=10^100`。以下六项均以普通 `by decide` 产生证明，再由 `--trust=0` 检查；每项 `#print axioms` 都报告不依赖任何公理：

1. 两段相同数字与一个合并段相等，夹入不同数字的零段也不影响结果。
2. 负斜率段与零斜率负常数段在尾部截断为零。
3. 总宽度截距相差 1 时快速判定为假。
4. 宽度一致但实际覆盖数字不同，快速判定为假。
5. 大系数对称段词快速判定为回文。
6. 大系数两种不同数字的双段词快速判定为非回文。

这些证书只计算快速布尔函数，未展开巨大的字面词，也未计算任何 cutoff 数值。它们是有限具体回归证据；一般正确性由前述完整 iff 定理承担。

## 复现与保留范围

`verification.json` 给出完整命令、日志散列、定理清单、定义依赖清单、源散列与结果。当前复核没有失败构建。`evidence/` 是可发布的源码、日志和本说明副本，不含 `.olean`；实际本地编译产物保留在原构建目录中。

复现时将 `evidence/source/` 复制到新的输出目录，使用上面的顺序与命令；`MatcherInspection` 最后运行。`evidence/SHA256SUMS` 校验证据文件。官方运行时依赖与恢复方式沿用已归档的 `runtime-author` 记录。
