# DecodedFiber 与 Predecessors 的非作者语义审查

审查者：Agent #105 / runtime105。结论：**PASS，无需修改受审源码。**

审查对象仅为以下两份冻结模块；审查者不是它们的作者：

| 模块 | 作者 | 冻结 SHA-256 |
|---|---|---|
| Agent105DecodedFiber9df76b | structure105 | `df0a9fcf872ce01169edee66a769ed90c425d4e86fce91324e0add5c5a16b00d` |
| Agent105Predecessors9df76b | root | `3bd4a139d26f81fc14547def29702970629693427fb947ff920854d6292a8d29` |

本人是依赖 Agent105WordFiber9df76b 的作者，也参与了较早 WidthSupport 与 DecoderLocal。本报告不把这些依赖称为本人独立复核的对象；独立依赖语义与完整 fresh 编译另由 scope105 负责。本轮逐行检查两份受审源、实际作者编译日志、输入快照与 SHA，不重复执行 foundation。

## 1. 结论的准确含义

计算入口为 `predecessors (e : Nat → Nat) (W : Nat)`。目标数值 Y 通过实际规范性假设 `Canonical Y e W` 出现在规格中。受审顶层源码证明：

```lean
n ∈ predecessors e W ↔ 0 < n ∧ Lychrel196.step n = Y
```

以及同一规范目标假设下 `(predecessors e W).Nodup`。量词覆盖每个普通自然数 n，返回所有正整数解；没有源宽、指定 digit realization、指定 profile 或回文目标等附加限制。

该列表等于两个完整单宽 fiber 的拼接：

```lean
decodedFiber e W W ++ decodedFiber e W (W - 1)
```

两条分支可以各自包含多个普通整数。源码没有把两个候选源宽或至多两个 coefficient profiles 转成“最多两个整数”。

## 2. DecodedFiber：整个目标数值与所有同宽前驱

### decodeNumerical_word_spec

此定理从已证明的 `decodeNumerical_eq_some_iff` 取得一个实际正整数源、规范数位 d、源宽 L、有限 columnSum 与 qs 一致，以及真实 `step n=Y`。随后：

- 用 `columnSum_symmetric` 与有限列表 extensionality 得到 `qs.reverse=qs`。有效索引通过 qs.length=L 运输，没有要求任意无限尾部相等。
- 用规范 d 的十进制数位上界和 `columnSum_bounded` 得到每个 qs 条目 ≤18。这里没有错误要求 qs 的系数 ≤9。
- 用原 `FoldedDecimal.step_eq_word_value` 直接得到 `step n=natValue qs`，再与 `step n=Y` 合成 `natValue qs=Y`。

最后一步是关键：`natValue qs` 求整个原系数列表的十进制位置加权值。它包含实际加法的终端进位贡献，绝不是仅低 L 位的 payload 数值。源码没有通过“输出低位相等”丢掉溢出的最高位。

### mem_decodedFiber_decimalWidth

定义成功时取 `wordFiber qs`，失败时取空列表。

成功分支利用上述完整 word spec，再调用既有 `mem_wordFiber qs n hrev hb`；长度与数值分别重写成 L 与 Y，得到：

```lean
n ∈ decodedFiber e W L ↔
  Agent101.decimalWidth n L ∧ Lychrel196.step n = Y
```

这一 iff 不只是验证 decoder 当初获得的一个代表。旧 numericFiber 成员定理量化所有 n，因此覆盖同一个 coefficient profile 的每一种规范数字拆分和每个普通整数实现。

失败分支也完成了反向证明：若某 n 仍有 decimalWidth n L 且 step n=Y，`decimalWidth_iff_canonical` 给出真正规范 d；`value_positive` 给出 n>0。既有 `decodeNumerical_isSome_iff` 的完备方向于是强制 decoder 成功，与已知 none 矛盾。因此空列表不是未经证明的失败处理。

### mem_decodedFiber 与 decodedFiber_nodup

`mem_decodedFiber` 把 exact decimalWidth 换成正数与规范数位存在性，便于消费真实宽度定理。正性由规范位值证明，不是新增假设掩盖异常整数。

`decodedFiber_nodup` 对任意 e,W,L 无条件成立：none 分支为空列表，some 分支直接消费 wordFiber 的无条件 Nodup。它不需要目标规范性，只保证列表没有重复；成员 iff 仍保留 Canonical 目标假设。

## 3. Predecessors：两种实际源宽的完备拼接

### mem_predecessors 的正向

列表 membership 经 `List.mem_append` 分成两个分支。每个分支的 `mem_decodedFiber` 都给出该成员正数且真实 step 等于 Y。没有使用弱化的 nextColumns、pairWord 或只保留某个有限前缀的替代映射。

### mem_predecessors 的反向

对任意 n>0 且 step n=Y：

1. `canonical_exists` 提供其实际规范 d 与正源宽 L。
2. 把目标规范性改写为 `Canonical (step n) e W`。
3. 调用既有 `step_width_cases`，得到 `W=L` 或 `W=L+1`，且相应终端 carry 0 或 1。
4. 第一种情况放入源宽 W 分支；第二种情况用自然数算术得到 W-1=L，放入源宽 W-1 分支。

因此 W 与 W-1 并非试探性的宽度选择。穷尽性由原实际整数加法宽度定理供应；任意更短或更长源已被该定理排除。

### predecessors_nodup

源码明确使用 `List.pairwise_append`：

- 左右两部分分别使用 `decodedFiber_nodup`。
- 若同一个自然数同时属于两部分，单宽成员 iff 分别给出 decimalWidth n W 与 decimalWidth n (W-1)。
- 原 `Agent101.decimalWidth_unique` 强制 W=W-1。
- `Canonical Y e W` 的正宽条件 W>0 与此矛盾。

证明严格排除了两个列表之间的相同整数，既没有依赖 profile 数量代替整数单射性，也没有通过去重操作掩盖遗漏的成员论证。

## 4. 边界逐项检查

| 边界 | 源码如何处理 | 结论 |
|---|---|---|
| 源 n=0 | 单宽 decimalWidth 等价规范性，规范值正；顶层 iff 显式要求 n>0 | 不会把零纳入结果 |
| L=0 | decimalWidth 定义包含 0<L；decoder 成功规格要求实际 Canonical 源 | 该单宽成员集合为空 |
| W=1 | 顶层取源宽 1 与 0；源宽 0 的分支为空 | 一位数目标没有漏分支，也没有无效零宽成员 |
| 短源溢出 | decoder 的实际 Canonical 源语义与 step_eq_word_value 保留完整目标值 | 原系数位值包含最高进位 |
| 低 payload 的最高位为零或全部为零 | word spec 不要求 payload 或 qs 自己满足 Canonical；只要求目标 e,W 与源 d,L 真正规范 | 没有错误排除合法短源 |
| qs 含 10..18 | bounded 结论仅为系数上界 18，natValue 对系数求位值 | 无错误十进制数位假设 |
| 奇偶中心 | 本层原样消费 decoder 与 WordFiber 已检查的接口，未自行改变中心系数 | 没有重复除 2 或丢弃单中心 |
| 任意无限数位函数尾部 | 所有规格只通过有效 i<L 或 i<W 使用数位 | 不增加尾部相等假设 |
| 非规范 e,W | 计算函数仍有定义；成员与顶层 Nodup 声明按源码保留 Canonical 条件 | 未扩大正确性适用域 |

这些边界由全称证明的具体分支核对，本轮没有额外执行数值 controls；独立 controls 与全链复编由 scope105 负责。

## 5. 作者执行证据核对

已读取且核对作者实际成功输入快照与当前冻结源码逐字相同：

| 模块 | 原始证据目录 | 实际命令要点 | 结果 |
|---|---|---|---|
| DecodedFiber | `decoded-fiber/attempt004/` | 官方 Lean 4.19.0；`--trust=0 -j1 -DElab.async=false` | exit 0；约 1.024 s |
| Predecessors | `predecessors/attempt001/` | 同一官方 Lean；`--trust=0` | exit 0；约 0.430 s |

前者一条计算定义与四条定理，后者一条计算定义与两条定理。实际日志中，两条计算定义均为无公理；六条定理均只有 `propext`、`Classical.choice`、`Quot.sound`。

这是本人读取的作者增量执行证据，不是本人独立 fresh 重建。完整 import-origin 公理清单与发布源码 fresh gate 由独立验收负责。本报告自身没有 Lean 执行、没有受审源修改，也没有 Git 写入。

## 6. 冻结决定

上述两个精确 SHA 的声明及组合逻辑满足本次 `Canonical Y e W` 下完整普通正整数前驱列表与 Nodup 的目标。无语义 defect、缺失前提或需要回退的范围扩张。

受审源码与作者 receipt/log 的只读副本保存在 `decoded-and-predecessors-source/`，结构化结论见 `decoded-and-predecessors-semantic.json`。源码后续若改变，应重新确认受影响部分；本结论只绑定表中冻结字节。
