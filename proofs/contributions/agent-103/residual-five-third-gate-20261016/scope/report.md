# Agent 103 下一阶段只读排重与源码接口报告

审阅者：Agent 103 / scope_scan（非 Git 写者）。日期：2026-10-16。

## 结论与状态

建议的窄目标是：把已经完整枚举的具体残余五族前像 `F_r` 的**再前一层普通正整数前像存在性**，等价归约为四个外侧数位等式及原 Agent 105 扫描器在中央 `2*r` 个数位上的接受条件；同时保留所有源宽度的排除结论。第四层必溢出已经有通用原定理，本任务只需要组合应用。

这里给出的是认领前的源码级范围和依赖勘察。没有新建该目标的 Lean 证明，没有运行数学搜索或枚举；也没有把源码阅读升级为新目标已验证。新 claim 必须由父代理确认。

## 已读取的排重范围

- 远端 coordination：`890e61a9b58558d02583caec1ed53eeb0c78374b`，143 个任务。先前 139 个完整记录加 25 个变化记录逐一合并，全部路径/blob 对最新目录匹配。证据：`latest-current-claims-890e61a9.json`。
- issue #61：本轮第 4、5 页共 106 条，读取到 6225739375。证据：`latest-issue61-pages4-5.json`。Agent 105 完整数值 decoder 发布为 6225616331；其完整普通前像列表已经在 6225704364 宣布实际认领，不能再描述成只有 proposal。
- 最新 main：`755b25cdf6b5e5eb811a9555ffbdc2fdd4c1271e`，proofs tree `a398e5f23eb4768117eb4b5b3cbd60032b0c9040`，2622 个未截断条目、1839 个顶层 Lean 文件。与此前已读的 58afcada 比较，12 个新增顶层 Lean 源逐一读取：Agent 100 Group II、Agent 1 Group III/periodic、ExteriorUpdateLaw，未出现本具体 d5 第三层端点。
- 本地原 main 1833 个非 archive Lean 文件、1446 个不同源码内容的声明扫描；292 个 archive task JSON 逐一检查。历史 Agent 119 EightFamilies 任务明确把 d=5 标为 OPEN，未认领为已解。
- 原 `p196_all_palindromes_and_eight_families.md` 第 4 节明确留下 `(2,12,9^(2r),12,2)` 的再逆向外侧 `(1,6)` 分支。它报告有限深度语言仍非空，没有给出统一 d5 深度上界。
- 原 `p196_exact_ancestor_depth.md` 中“d=5 深度 2”的族要求二进制回文块恰有 11 个 1，不能用于本 `fam 5 r`。
- 原 `DecimalFiniteAncestry.numeric_ancestor_depth_le` 给出固定目标的 `4 * decimalLength target` 上界，随 r 增长，不是本族的统一常数界。

以上只构成在这些实际读取记录中的排重；不宣称覆盖其他参与者尚未发布的源码。父代理正式认领时仍应刷新 coordination。

### 相邻任务边界

- Agent 105 `agent105-9df76b-all-predecessors-20261016` 已认领通用 `predecessors e W` 列表及全自然数 membership/Nodup，使用原 decoder 和 Agent 101 ProfileExtraction。其范围明确排除 Agent 103 residual-five 特化、first-hit2 和有限反向实例。本候选不构造通用列表、不重证解码器、不重证对称词拆分。
- Agent 101 的跨宽最大重数、固定 profile 分拆计数和初始回文过滤继续保留。本候选不增加一般计数主张。
- Agent 3 的三层 dead prefix 是受保护的 `[14,14,14,5] ++ tail` 路径和等宽末进位零条件；不是本具体普通整数前像端点。
- Agent 107 forward folded transducer、其他 2641/5523/5524/620 前缀均属不同任务。

## 候选精确接口（尚未证明）

使用既有：
`middle r = 33 * 10^(2*r+2) + 22`，
`fiber r = Agent101.numericFiber (2 :: 12 :: List.replicate r 9) none`。
令 `W = 2*r+4`，`hn : n ∈ fiber r`，
`he : Canonical n e W`。

拟证明：

```lean
(∃ a, 0 < a ∧ step a = n) ↔
  e 0 = 1 ∧ e (W - 1) = 1 ∧
  e 1 = 6 ∧ e (W - 2) = 6 ∧
  (Agent105DecoderScan9df76b.scan
    (2 * r) (fun i => e (i + 2)) 0 0).isSome = true
```

同时，每一个正整数前像 `a`，无论先给它哪一个实际 canonical 源宽 `L`，都必须满足 `L = W`、`carry (columnSum d L) L = 0`，以及源 pair coefficient 的前两项为 1、6。

此处中央调用必须是原 `scan`，不能换成 `decodeAtWidth`：中央空词以及外系数为零的内层词允许存在，而根的正性约束已经由外层系数 1 保证。r=0 时原 `scan 0 _ 0 0 = some []`，不会人为排除短端点。四个外侧数位条件只把原 14 种外层分拆压到一个分拆；中间扫描仍可拒绝，不能直接把最终候选数宣称为 `10^r`。

这给有限反向证书一个精确、可执行的中心测试，消除第三层的跨宽分支。它本身不证明统一深度上界。

## 保存的 Agent 105 原始源码

共同源提交：`64bb07e9f8d3ffcfd141d58e01ec7e27964c5e5d`。
共同本地目录：

`/workspace/scratch/a1d46b1077ac/agent103-scope/depth-scout-001/source-pins/`

| 文件 | Git blob | SHA-256 |
|---|---|---|
| Agent105NumericDecoder9df76b.lean | 4d49482285253431cc33ac1ccdc1f97c8107df6e | 9a63eb03cb04d9e7fb3294216ab770893ac227c089ddba6d864d73d949229db5 |
| Agent105DecoderScan9df76b.lean | a06bec9190d7a21971b6dafbfe47d30e4b3717d5 | 4e7f3a29e41c3e40adc08326947fe28b5505015f3c68cba67a1cb648318cad1d |
| Agent105DecoderLocal9df76b.lean | e03c9a6cc7aadb7e882c47417411e3e091264683 | 820d28d68005208ac21dd498dcd27660b58d2d147de265dbcd0cf0d7c250e872 |
| Agent105DecoderTarget9df76b.lean | c5daf3b8dc804f4af03826ce08ba7648bb79492a | 2c2cbf18088e0a281ff78547cc3b2aa465050504c9139fc2839fb70e86db7c9d |
| Agent105WidthSupport9df76b.lean | 4100a7560e5e4ef64765d11d815cc84be4138549 | 3411c212f4c7c05d1d91cc7249f1d6520f9da1202da6721ca9b1764944ff3da7 |

所有文件均已逐字保存并重算 Git blob 和 SHA-256 验证。完整作者 registry 也已保存为 `Agent105NumericDecoder9df76b.registry.json`，blob `808b601148de6b04855de42f15e4b1e6eb03d6ab`。

## 原 scan 的真实 signature 和语义

命名空间 `Agent105DecoderScan9df76b`：

```lean
def scan : Nat → (Nat → Nat) → Nat → Nat → Option (List Nat)
  | 0, _, a, b => if a = b then some [] else none
  | 1, e, a, b => (decodeCenter (e 0) a b).map (fun q => [q])
  | L + 2, e, a, b =>
      match decodePair (e 0) (e (L + 1)) a b with
      | none => none
      | some E =>
          (scan L (fun i => e (i + 1)) E.low E.high).map
            (wrapDigits E.coeff E.coeff)
```

数位按最低位在前；a 是当前低端入进位，b 是高端出进位。每个 pair 接受都检查原完整十进制等式，不能只看经过 Nat 截减的候选式。中心奇数宽要求中心系数为偶数；空中心只要求两端进位相同。

```lean
theorem decodeAtWidth_eq_some_iff (e : Nat → Nat) (L h : Nat) (qs : List Nat)
    (he : ∀ i, i < L → e i ≤ 9) :
    decodeAtWidth e L h = some qs ↔
      qs.length = L ∧ Admissible L (digitFn qs) ∧
      (∀ i, i < L → output (digitFn qs) i = e i) ∧
      carry (digitFn qs) L = h
```

命名空间 `Agent105NumericDecoder9df76b`：

```lean
def decodeNumerical (e : Nat → Nat) (W L : Nat) : Option (List Nat) :=
  if W = L then decodeAtWidth e L 0
  else if W = L + 1 ∧ e L = 1 then decodeAtWidth e L 1
  else none

theorem decodeNumerical_isSome_iff
    (Y : Nat) (e : Nat → Nat) (W L : Nat) (htarget : Canonical Y e W) :
    (decodeNumerical e W L).isSome = true ↔
      ∃ n d, 0 < n ∧ Canonical n d L ∧ step n = Y
```

同模块的 `decodeNumerical_eq_some_iff` 还给接受列表长度和真实输入的逐项 `columnSum` 对应。源宽两种情况直接复用 `Agent105WidthSupport9df76b.step_width_cases`：

```lean
theorem step_width_cases {n L W : Nat} {d s : Nat → Nat}
    (hn : Canonical n d L) (hs : Canonical (step n) s W) :
    (W = L ∧ carry (columnSum d L) L = 0) ∨
      (W = L + 1 ∧ carry (columnSum d L) L = 1)
```

`Agent105DecoderTarget9df76b.canonical_predecessor_payload` 则把实际正整数前像直接送到 `WidthChoice ∧ PayloadSpec`，并保留溢出时的原最高位 1 条件。

## 第四层必须溢出：已存在的原接口

原文件：

`proofs/PrefixObstruction__f475c74e30a5df3a.lean`

已复制到上述 `source-pins/PrefixObstruction.lean`。以 main
`755b25cdf6b5e5eb811a9555ffbdc2fdd4c1271e` pin；
blob `efc5b26b0cc561f0f4143f6dbc0f4ff35fdef2c6`，
SHA-256 `1436c61c791f8bb2a982f86c7857c4a6cb70c80280dfdba1aaa4cdfeef2fd97d`。
它只 import `LychrelDigitSums`，正是现有已验证基础体。

命名空间 `DecimalPrefixObstruction`：

```lean
theorem no_overflow_outer_ge_two (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) (hc : carry q L = 0) :
    2 ≤ nextColumns q L 0
```

因此，已经得到的输出 pair coefficient `q0 = 1` 立即排除该前一加法的末进位零；与原 `carry_bounded` 合并即为末进位 1。这只是现有通用定理的具体应用。

同一模块还已有下列更强接口，无须独占或重证：

```lean
theorem overflow_outer_two_second_le_eleven (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) (hL : 2 ≤ L) (hc : carry q L = 1)
    (ho : nextColumns q L 0 = 2) :
    nextColumns q L 1 ≤ 11

theorem even_no_overflow_inverse (q : Nat → Nat) (L i a : Nat)
    (ha : Admissible L q) (hi : i < L) (hc : carry q L = 0)
    (hl : carry q i = 0) (hh : carry q (L - i) = 0)
    (ho : nextColumns q L i = 2 * a) :
    q i = a ∧ carry q (i + 1) = 0 ∧ carry q (L - 1 - i) = 0

theorem overflow_one_six_forces_large_delay (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) (hL : 3 ≤ L) (hc : carry q L = 1)
    (h0 : nextColumns q L 0 = 1) (h1 : nextColumns q L 1 = 6) :
    q 0 = 10 ∧ (q 1 = 5 ∨ q 1 = 14) ∧
      4 ≤ extended q L (L - 2)
```

对本目标，前两个接口已经覆盖“目标外侧 (2,12) 排除溢出，并逆出 (1,6)”这部分一般 pair 动力学。新证明应将其运输到既有 canonical fiber 数位，再连接 decoder 的确切中央返回条件。

对实际 196，还有基线已编译的替代接口
`Agent119.EightFamilies.middle_no_overflow_one (s : Nat)
(hq0 : (V (s+1)).2 0 = 1) (hc : carry (V s).2 (V s).1 = 0) : False`；
可以直接服务父代理的第四步组合。

如果以后用新的第三层定理处理 `orbit196 t = fam 5 r`，最后四次加法的起点是 `t-4,t-3,t-2,t-1`；所需末进位依次为 `1,0,0,0`，宽度应明确为 `t-4` 时 `W-1`，从 `t-3` 到 `t` 时 `W`。目前这些是待证的特化组合目标，不是本报告新增成果。末进位零也不表示内部各列无进位。

## 最小依赖闭包

机器清单：`minimal-closure-pins.json`，包含各模块路径、SHA-256、Git blob、imports，以及现有冻结源路径。

原 Agent 105 数值 decoder 单独闭包为 10 个 Lean 模块（不计 Std）：

1. Lychrel196Research
2. Agent101DigitPairs
3. Agent101MultiplicityBounds
4. Agent101SplitEnumeration
5. Agent101NumericFibers
6. Agent105WidthSupport9df76b
7. Agent105DecoderLocal9df76b
8. Agent105DecoderTarget9df76b
9. Agent105DecoderScan9df76b
10. Agent105NumericDecoder9df76b

完整作者 registry 的 CrossWidthWitness 和 DecoderControls 不在本目标必需闭包。ProfileExtraction 和 Agent 105 新通用前像列表也不必纳入本窄目标。

以既有 `ResidualFiveFiberConclusion` 为根，其冻结已验证闭包是 17 个模块；新增原依赖为上述 WidthSupport 加四个 decoder，以及 PrefixObstruction，共 6 个。于是目标的既有/原始依赖联合闭包为 23 个模块，另加未来新证明模块。清单由实际 import 递归生成。

既有环境的 `Lychrel196Research` 是 import-only forwarder（SHA
`13dd9effbef33d3d10138baed5cb3a6f964691ba895cc5d453f2553f0ac81011`）；
原 decoder registry 中它是完整 Research 基础体。必须沿用此前已核验的基础体兼容关系，统一到现有 `LychrelDigitSums`，不能把两个完整基础体一起加载。清单显式记录此差异。

本报告没有重新编译这 6 个新增原依赖。正式 claim 后由 runtime 做源码恢复和实际 trust=0 编译；本报告中的“已验证”只指此前真正完成的 22 模块环境和明确标注的原作者发布记录。

