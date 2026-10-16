# Controls 作者说明

作者：Agent #102 的真实子代理 `/root/lean_runtime`。
冻结源码为 `attempts/attempt-002/source/Agent102AllParameterControls.lean`。
32 条定理全部实际通过 `--trust=0`；下列结论来自源码和对应编译日志。

## 有限前缀不能省略

复用 `AffineBoundary.moving` 与 `AffineBoundary.fixed 3` 后，
`moving_fixed3_only_eq` 给出每个自然数参数的精确条件：

```lean
wordAt AffineBoundary.moving k = wordAt (AffineBoundary.fixed 3) k ↔ k = 3
```

`moving_fixed3_controls` 的四个 Bool 分别为：

| allEqual | someEqual | allUnequal | someUnequal |
|---|---|---|---|
| false | true | false | true |

`moving_fixed3_prefix_witness` 另外核验 `3 < equalityCutoff`、参数 3 的
`equalAt=true` 以及 `fastEqualOnTail=false`。因此唯一的相等参数确实落在有限前缀内。
`moving_fixed3_semantics` 经 `someEqual_spec` 与 `someUnequal_spec` 取得真实的
存在相等参数、存在不等参数两个命题。

对回文给出两个方向相反的精确边界：

- `growing = [1^k, 2]`：`growing_palindrome_iff` 证明回文当且仅当 `k=0`。
  `growing_prefix_witness` 核验 tail checker 为 false，但存在回文的 checker 为 true，
  并明确核验参数 0。
- `declining = [1^max(3-k,0), 2]`：`declining_palindrome_iff` 证明回文当且仅当 `3≤k`。
  源码长度为整数仿射式 `-k+3` 的 `toNat`。
  `declining_prefix_obstruction` 核验 tail checker 为 true、全部参数回文为 false，
  以及参数 0 的反例。

两个精确 iff 都是任意自然数参数的证明，不是仅对若干取值进行枚举。
它们从一般列表引理 `replicate_one_two_palindrome_iff` 得到；正长度情形的
首位为 1，反转后的首位为 2，零长度情形单独归约。

## 四个回文量词接口的闭证书

| 模板族 | allPalindromic | somePalindromic | allNonpalindromic | someNonpalindromic |
|---|---|---|---|---|
| `[1^k,2]` | false | true | false | true |
| `[1^max(3-k,0),2]` | false | true | false | true |
| `[1^(k+1),2^(k+1)]` | false | false | true | true |
| `[1^k,2,1^k]` | true | true | false | false |

每一行的完整四元组都由一条 `by decide` 闭证书核验。
对应的 `*_semantics` 再调用母模块 `_spec` 定理，得到所需的全称或存在命题。
这既检查计算结果，也检查 Bool 真值与语义规格的参数、方向和投影是否匹配。

## 零长度、空词与列表首项为零

`erased = [7^0,8^(-k)]` 中的两段长度在 `toNat` 后恒为零。
`empty_zero_controls` 核验其对所有参数等于空模板，并核验 erased 和 empty
均在所有参数回文、empty 不存在非回文参数。
`zero_runs_semantics` 与 `empty_palindrome` 将这些布尔结果转为原始词命题。

`leadingZero` 是固定列表 `[0,1]`。
`leading_zero_word` 对所有参数证明这个精确字面列表，
`leading_zero_controls` 核验它始终不等于 `[1]`，并且始终非回文；
两个 `*_semantics` 式接口进一步经规格取得全称结论。
这里保留列表首项的 0；没有断言它与 `[1]` 在原仓库低位优先十进制表示下数值相同。

## 巨大单参数压缩证书

源码中 `huge` 是 101 位的自然数字面量，精确等于 `10^100`。
三个巨大例子只执行 `equalAt`，参数均为 `k=huge`：

1. `hugeSplit` 含两个同数字段及中间零长度段；它与 `hugeMerged` 相等。
   两边总长度为 `2·huge²+2·huge`。
2. `hugeOne` 与 `hugeWidthChanged` 的总宽度相差 1，检查器返回 false。
3. `hugeNegative` 首段长度为 `-huge²+huge`，裁为零后与 `hugeOne` 相等。

`huge_split_at`、`huge_width_at`、`huge_negative_at` 都是 `by decide`，
literal 公理日志均报告不依赖任何公理。
随后分别经 `equalAt_eq_true_iff` 或 `equalAt_eq_false_iff` 取得
涉及原始 `wordAt` 的证明；这些规格应用没有展开巨大词。

没有把这些巨大系数模板送入 `allEqual`、`someEqual` 或任何完整前缀扫描。
三个实际证书只证明这些精确实例，不构成算法的复杂度定理或通用性能保证。
