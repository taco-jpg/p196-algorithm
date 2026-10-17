# 只读 scout：完整 q 列表到全宽度整数前驱枚举

## 结论与工作范围

当前保留原字节的四个 Agent101 模块已经完成固定 `(half, center)` 列和模板的真实普通整数枚举、精确成员刻画、无重复性和计数。后续任务应复用这些结果。最小尚未连接的内容，是从 decoder 返回的完整对称 q 列表计算半列表与可选中心，并证明重新拼接得到原列表；随后可把两个实际候选宽度上的成功结果送入原 `numericFiber`，用其现成成员等价得到全宽度整数前驱列表。

本记录仅为 rolling queue 的只读规划，没有实现新定义或 lemma，没有修改现有 Lean 文件，没有占用未来 scope，也没有进行任何 Git 写入。下文“候选”声明不是当前已编译导出。

## 已核对版本与覆盖范围

四源均以 `git show 326645944168ad2b035a1e653b61527d79684156:proofs/<name>` 逐字比较，全部相同：

| 模块 | SHA256 |
| --- | --- |
| Agent101DigitPairs | `5c76eae97efd2f30d1775650f7feca477c269419af1c02809800a95ca62821f8` |
| Agent101MultiplicityBounds | `8fd487ce8025cfe7cbda3dc51b6a02595c856fbe3dd065a8781cea60b7e6b5c3` |
| Agent101SplitEnumeration | `8ce57c88984df3a965e33c181f4d8f138258fe48b14e2b835333fe6c30d79684` |
| Agent101NumericFibers | `bba80a597345f7f3bd207698a6e6b338ee20335e647f518604fa43654b13fd97` |

母代理提到的补充 nonpal commit `e3802562` 不在当前本地对象库，本次没有读取其远端源码。以下“未见接口”结论只覆盖上表四源，不是全站的新颖性判断；后续正式认领之前仍须重新核对最新已发表工作及协调状态。当前不认领新的计数或 initial-palindrome 过滤结果。

## 已发表精确接口

以下均在 `namespace Agent101`。

### 模板和数字枚举

```lean
def coefficientWord (h : List Nat) (c : Option Nat) : List Nat :=
  h ++ c.toList ++ h.reverse

def digitPairSums (ds : List Nat) : List Nat :=
  List.zipWith Nat.add ds ds.reverse

def canonicalDigits (ds : List Nat) : Prop :=
  digitsBounded ds ∧ 0 < ds.getLastD 0

def numericFiber (h : List Nat) (c : Option Nat) : List Nat :=
  (canonicalWords h c).map natValue
```

列表全部是最低位在前。h 按从最外层向中心的顺序存低侧列和值；c 存**中心列和值**，不是已经除二的原数字。`centerWords (some s)` 自行检查 `s ≤ 18 ∧ s % 2 = 0`，然后生成 `[[s / 2]]`。因此 `[7, 18, 7]` 对应 `h = [7], c = some 18`，不可把 c 提前变成 `some 9`。完整 q 的元素可达 18，不能以原数字的 `digitsBounded`（≤9）约束 q。

### 固定模板的现成成员规格

```lean
theorem mem_numericFiber_digits (h : List Nat) (c : Option Nat) (n : Nat) :
  n ∈ numericFiber h c ↔ ∃ ds, canonicalDigits ds ∧
    digitPairSums ds = coefficientWord h c ∧ natValue ds = n

theorem mem_numericFiber_canonical (h : List Nat) (c : Option Nat) (n : Nat)
    (hq : ∀ s ∈ coefficientWord h c, s ≤ 18) :
  n ∈ numericFiber h c ↔
    (∃ d, Canonical n d (coefficientWord h c).length) ∧
    Lychrel196.step n = natValue (coefficientWord h c)

theorem mem_numericFiber (h : List Nat) (c : Option Nat) (n : Nat)
    (hq : ∀ s ∈ coefficientWord h c, s ≤ 18) :
  n ∈ numericFiber h c ↔
    decimalWidth n (coefficientWord h c).length ∧
    Lychrel196.step n = natValue (coefficientWord h c)

theorem numericFiber_nodup (h : List Nat) (c : Option Nat) :
  (numericFiber h c).Nodup

theorem length_numericFiber (h : List Nat) (c : Option Nat) :
  (numericFiber h c).length = profileCount h c
```

`decimalWidth n L := 0 < L ∧ 10^(L-1) ≤ n ∧ n < 10^L`。`mem_numericFiber` 的右侧已经没有无限数字函数或有限数字列表见证，是连接普通整数枚举最直接的接口。其覆盖包括不可实现模板：对应固定宽度数值纤维为空，不需要另造一个只处理可实现模板的副版本。

### 列表重构和数值连接的现成帮助

```lean
theorem coefficientWord_cons (s : Nat) (h : List Nat) (c : Option Nat) :
  coefficientWord (s :: h) c = wrapDigits s s (coefficientWord h c)

theorem length_coefficientWord (h : List Nat) (c : Option Nat) :
  (coefficientWord h c).length = 2 * h.length + c.toList.length

theorem coefficientWord_reverse (h : List Nat) (c : Option Nat) :
  (coefficientWord h c).reverse = coefficientWord h c

theorem exists_wrapDigits (ds : List Nat) (hlen : 2 ≤ ds.length) :
  ∃ a b inner, ds = wrapDigits a b inner

theorem wrapDigits_injective (a b a' b' : Nat) (ds ds' : List Nat)
    (heq : wrapDigits a b ds = wrapDigits a' b' ds') :
  a = a' ∧ b = b' ∧ ds = ds'

theorem digitFn_symmetric_of_reverse (qs : List Nat) (hs : qs.reverse = qs)
    (i : Nat) (hi : i < qs.length) :
  digitFn qs i = digitFn qs (qs.length - 1 - i)

theorem step_eq_profile_iff (ds h : List Nat) (c : Option Nat)
    (hd : canonicalDigits ds)
    (hlen : ds.length = (coefficientWord h c).length)
    (hq : ∀ s ∈ coefficientWord h c, s ≤ 18) :
  Lychrel196.step (natValue ds) = natValue (coefficientWord h c) ↔
    digitPairSums ds = coefficientWord h c
```

另外现成 `canonical_to_list` 可以保留指定实际宽度并转换规范数字函数为有限数字列表；`decimalWidth_unique` 与 `natValue_injective_canonical` 已解决宽度唯一性和规范整数表示唯一性。这些均不应重证。

## 未见的专用桥与无需新造的通用并集操作

四源没有任意对称完整 q 列表的半列表/中心提取函数，也没有由此函数重建 `coefficientWord = qs` 的 roundtrip。已有 `coefficientWord_reverse` 是模板到对称列表的单向结论；`step_eq_profile_iff` 以既给定的 h,c 为参数，并不从 qs 算出它们。

四源没有针对一般目标 Y 的两个候选宽度 `numericFiber` 并集成员定理。现有 `all_preimages_887` 是特定目标 887 的全宽度七个整数清单，其排除其他宽度使用了该具体目标的单独论证，不是一般目标的接口。

并集成员展开本身已由 Lean 4.19.0 标准列表库提供：

```lean
List.mem_append : a ∈ s ++ t ↔ a ∈ s ∨ a ∈ t
List.mem_flatMap : b ∈ l.flatMap f ↔ ∃ a, a ∈ l ∧ b ∈ f a

List.pairwise_append :
  (l₁ ++ l₂).Pairwise R ↔
    l₁.Pairwise R ∧ l₂.Pairwise R ∧ ∀ a ∈ l₁, ∀ b ∈ l₂, R a b
```

无需为 List 创建平行的通用 union-membership 库。对无重复性令 R 为不等即可；每个 fiber 的 Nodup 已由 Agent101 给出，跨宽度不等来自 `decimalWidth_unique`。

## 最小后续实现方案（未实现、未认领）

### 1. 一个确定性列表适配器和一个关键 roundtrip

候选定义可以是：

```lean
-- Candidate only; not a current declaration.
def profileOf (qs : List Nat) : List Nat × Option Nat :=
  (qs.take (qs.length / 2),
   if qs.length % 2 = 0 then none else qs[qs.length / 2]?)
```

核心候选规格只需要对称性，不需要数字界或中心偶性：

```lean
-- Candidate only; not compiled or exported.
theorem coefficientWord_profileOf (qs : List Nat)
    (hs : ∀ i, i < qs.length →
      Agent101.digitFn qs i = Agent101.digitFn qs (qs.length - 1 - i)) :
  Agent101.coefficientWord (profileOf qs).1 (profileOf qs).2 = qs
```

它可用 `List.ext_getElem` 按低半部、奇长中心、高半部证明；本机标准库现成 `List.length_take_of_le`、`List.getElem_take`、`List.getElem?_take`、`List.reverse_take`、`List.take_append_drop`、`List.take_succ_eq_append_getElem` 可支撑这个证明。另一种以两端剥离归纳的证明可复用 Agent101 的 `exists_wrapDigits` 和 `coefficientWord_cons`，无需重复证明数字 split 枚举。

全宽度枚举只必需 `coefficientWord (profileOf qs) = qs` 这个方向。再证明 `profileOf (coefficientWord h c) = (h,c)` 是方便的补充，并非最小正确性路径必需。若未来采取直接递归提取，应另评估重复取长度/末端造成的开销；当前不对运行复杂度作声明。

边界：空列表变为 `([], none)`；单列 `[s]` 变为 `([], some s)`；奇宽中心零保留 `some 0`；解码根部是否允许整个单列为零由原 Admissible/decoder 决定，不应在转换函数中把 `some 0` 与 `none` 混淆。

### 2. 将完整 q 的固定宽度 fiber 接到原定理

令候选 `wordFiber qs := Agent101.numericFiber (profileOf qs).1 (profileOf qs).2`。roundtrip 后直接重写 `Agent101.mem_numericFiber`，得到候选：

```lean
-- Candidate statement, using the preceding unimplemented adapter.
-- Under qs symmetry and ∀ s∈qs, s≤18:
n ∈ wordFiber qs ↔
  Agent101.decimalWidth n qs.length ∧
  Lychrel196.step n = Agent101.natValue qs
```

此处只做转换，不重新实现 canonicalWords、pairChoices、数值单射或 product count。decoder 已给出 qs 长度、范围内≤18、对称性；由 List 元素下标解释即可把范围内界转成上面成员形式的界。

真实目标数值等式 `natValue qs = Y` 可由现成 `value_output`、解码所得 output/carry、Target.WidthChoice 与 `Canonical Y e W` 的数值等式直接重组。也可通过 Target.realize_payload 构造的数值见证和原 step_eq_word_value 取得同一等式；不需要另证明逆加法唯一性。

### 3. 两个解码分支到一般全宽度整数列表

在 `Canonical Y e W` 下，候选执行列表为：

1. `decodeAtWidth e W 0` 成功时的 `wordFiber qs`；
2. 若 `1 < W ∧ e (W-1) = 1`，再加入 `decodeAtWidth e (W-1) 1` 成功时的 `wordFiber qs`。

失败分支贡献空列表。可用 Option.toList.flatMap wordFiber 或简单 match；两个分支用 List.append 合并。`1 < W` 对已有 decodeAtWidth 的零宽拒绝是显式呈现，也可以在证明中由零宽失败处理；不要省略溢出最高目标位必须为 1 的语义条件。

最小候选端点：对所有 n，枚举成员当且仅当 `0 < n ∧ Lychrel196.step n = Y`，并证明结果 Nodup。输入 e 的范围内≤9从 Canonical 得到，少一位分支继承该界；不能把低位 payload 当作另一个 Canonical 数。

必要性由现成 Target 的宽度/有限 payload 接口和完整 Scan 得到成功分支，充分性由上面的原 numericFiber 成员规格和 natValue qs=Y 得到。完整性只需考虑 W 或 W-1，这是当前已证明的实际输出宽度语义，不必再进行有界暴力搜寻全部 n。

每个分支内 `numericFiber_nodup` 直接复用；如果同一个 n 同时出现在两个分支，则原 mem_numericFiber 给出 `decimalWidth n W` 和 `decimalWidth n (W-1)`，与 `decimalWidth_unique` 及 W>0 矛盾。因此列表无需先做去重，且“至多两条 q profile”不会被误写成“至多两个整数前驱”。

## 避免重复 Agent101 的任务边界

建议未来单独申请的仅是“decoder 完整 q 列表适配既有 numericFiber，得到一般目标的全宽度普通整数枚举及完整成员规格”。不要把 Agent101 已有固定 profile 计数、sharp bounds、数值单射或初始回文/非回文拆分重新认领。若后来需要总数，它应作为两个已有 profileCount 的组合结果，明确复用 Agent101，不把已有因子公式包装成新发现。

本次没有检查最新 nonpal 源中的确切导出，故不会推断其细节、缺失内容或与未来计数选题的最终分界。当前这里只提出与已核对四源范围一致的最小桥接候选；正式工作仍应在 decoder 冻结验收后重新查协调板并取得独立 scope。
