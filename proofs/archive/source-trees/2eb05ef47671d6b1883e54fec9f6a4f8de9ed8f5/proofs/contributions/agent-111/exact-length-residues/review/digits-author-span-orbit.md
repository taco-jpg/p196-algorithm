# ModularSpan 与 ResidueOrbit 的独立语义审阅

审阅者：Agent 111 数字实现子代理。日期：2026-10-15。

结论：**在下述固定提交中，未发现两份目标文件的数学语义、假设范围、实际轨道连接或依赖方向存在阻断性缺陷。**

## 固定版本与执行边界

指定提交：`c3192d5bf2962298bcb2bb209a0947f657e8a7e5`。本次用 `git rev-parse --verify` 确认该提交对象存在，并用 `git show <commit>:<path>` 读取目标与依赖源码。SHA-256 对相同 `git show` 返回的源码字节计算，不以当前工作树文本代替固定版本。

| 文件 | 固定提交源码 SHA-256 |
|---|---|
| `proofs/contributions/agent-111/exact-length-residues/ModularSpan.lean` | `1cad197771ad6a4a9577ac08d3e1a4afe143e354a96a261b8ebaa2c687c09754` |
| `proofs/contributions/agent-111/exact-length-residues/ResidueOrbit.lean` | `989e42134e6ae6c05775f569cc1b4cd916d0d45d5d87b6e471cbf3fe3e2cdfc6` |
| `proofs/research/Lychrel196Research.lean`（既有语义与轨道引理依赖） | `f8950d138fa4231b536059e2334d36b6496de3d25a806f4cf3925941aa05144c` |
| `proofs/contributions/agent-111/exact-length-residues/Saturation.lean`（关闭条件性假设的下游文件） | `a638ff9844afa378dfe168feeaa8be372d2f2b5f6f3c1ff62ca5c2fe9f0685e0` |

这是**源码及数学语义审阅**，没有执行 Lean 重建，没有将既有编译结果冒充本次独立执行，也没有替代 environment 专员正在进行的全新完整构建与公理依赖检查。本次目标文件由另一专员编写；审阅者没有改动这两份数学源码，也没有执行 Git 写操作。

## ModularSpan：整数张成与有界自然数系数

`gcd_int_span` 对全部自然数 `m,n` 构造整数 Bézout 系数。`m=0` 分支使用 `(0,1)`，覆盖 `n=0`；非零分支递归于严格更小的 `n%m`，利用 `n%m+m*(n/m)=n` 把递归系数变为 `(y-x*(n/m),x)`。减法在 `Int` 中进行，允许负系数；未使用会截断负值的自然数减法代替整数代数。递归方向与 `Nat.gcd_rec` 一致。

`gcd_three_int_span` 的唯一实质条件是 `gcd(q,gcd(c0,c1))∣a`。它先张成外层 gcd，再张成 `gcd(c0,c1)`，最后乘以整除见证 `k`；得到的是严格整数等式 `u*q+x*c0+y*c1=a`。没有把需要证明的模线性组合另列为假设，也没有假设某个未知 Bézout 系数存在。即使三个生成元都为零，整除条件也只允许目标 `a=0`，不会产生无条件张成任意自然数的漏洞。

`modular_span` 的结论系数明确是 **自然数**：`∃ x, x<q ∧ ∃ y, y<q ∧ ...`，其中 `q : Nat` 决定了系数类型。实现将整数系数取欧几里得余数，再用 `toNat`：

- `hq : 0<q` 先提供正的整数模数及非零条件。
- `Int.emod_nonneg` 保证余数非负，所以 `toNat` 不丢失信息；`hX/hY` 明确证明转回整数等于原余数。
- `Int.emod_lt_of_pos` 保证转成自然数的系数严格小于 `q`。
- 原整数等式去掉 `u*q` 后给出目标余数；分别把两个系数替换成它们的余数保留该等式。
- 最后借助自然数到整数的单射和取模转换定理返回自然数余数结论。等式右端是 `a%q`，没有误将未约化的 `a` 当作必须小于 `q`。

边界检查：`q=0` 被有界系数定理的正性前提明确排除；`q=1` 合法，此时返回系数被强制为 `0,0`；`a=0` 合法；`c0` 或 `c1` 为零没有被额外排除；两系数都为零时 gcd 条件正好保证 `q∣a`。结论只证明充分张成方向，注释与声明没有将它误标为未经证明的 iff。

## ResidueOrbit：对象语义与必要条件

文件只 `import Lychrel196Research`，使用核心 `Lychrel196.orbit`、`step`、`reverse10`、`Palindrome` 与 `DecimalDigits.Canonical`，没有定义替代轨道或削弱的“回文”谓词。固定核心中：

- `step n = n + reverse10 n`。
- `orbit n 0 = n`，`orbit n (k+1) = step (orbit n k)`。
- `Palindrome p` 是普通有限自然数反转等式 `reverse10 p=p`。
- `Canonical p d L` 要求 `0<L`、每位 `≤9`、最高位非零以及实际数值 `value d L=p`。

这个轨道按定义继续迭代，即使较早出现回文也不停机；本文件没有偷偷改用“直到第一次回文为止”的有限序列。

`palindrome_not_dvd10` 从真实反转的单位数字等于原最高位，以及 `reverse10 p=p` 推出 `p%10` 非零；最高位正性取自传入的同一个 `Canonical` 证据。`even_palindrome_dvd11` 用精确长度的反转模 11 关系推出偶数位回文被 11 整除。它使用的是确证的 `11∣99` 特例，并未假设所有模数有自主反转更新规律。

`palindrome_residue_compatible` 沿 `p%M=a%M` 运输必要条件时，只对已证明整除 `M` 的因子使用 `Nat.dvd_mod_iff`：第一项因子为假设中的 10，第二项为 `gcd(M,11)`。因此不会把“模 M 相等”错误解释为“任意其他模数相等”。`a` 无需约化；`M=1`、`a=0` 的情形也没有遗漏。该必要方向本身允许 `M=0`，这是取模 0 等于原数时仍成立的条件语句，并非对模 0 饱和存在性的断言。

`Compatible` 精确包含两项必要限制。`SaturationAbove` 是待证明的性质定义：一个阈值之上，每个精确宽度、每个兼容余数均有正的实际回文。`palindrome_residue_iff_of_saturation` 的充分方向明确使用调用者提供的 `hs`，必要方向使用前述必要条件；本文件没有把定义直接当成无条件定理。

## 真实轨道连接、正性与时间范围

`orbit_matches_palindrome_of_saturation` 假设 `hn : 0<n`，调用固定核心的 `AstraModular.large_width_compatible_residue M n B hn`。该引理返回的是同一个实际状态 `orbit n t` 的 `Canonical`、`B≤L`、时间范围 `6+4*B≤t≤7+4*B` 及其实际余数的兼容性。

追读该核心接口的直接证明链确认：

1. `large_width_compatible_state` 从正起点的真实数字表示出发，结合 `late_compatible_state` 和 `DecimalWidthGrowth.numeric_width_bounds`。
2. `numeric_width_bounds` 的结论包含 `Canonical (orbit n K) e W`，不只是抽象字长；其语义连接使用既有 `iterPairs_representation`。
3. 晚期兼容状态由真实轨道在第 6 步后被 11 整除，以及不可能连续两步单位数字为零得到。
4. 最后的 `large_width_compatible_residue` 只把整除/非整除性质运输到模 `M` 的余数；不调用回文饱和性，也不调用本贡献的总定理。

本文件对 `hs` 的具体调用目标是 `a=orbit n t%M`，所传兼容性与此精确匹配。得到 `p%M=(orbit n t%M)%M` 后，用 `Nat.mod_mod` 和对称性变成声明所需的 `orbit n t%M=p%M`。返回的两个 `Canonical` 使用相同 `L`，分别对应轨道状态和构造回文；没有把数字函数 `d,e` 或两数混同。它只声称同宽同余，不声称轨道状态等于 `p` 或最终必然命中回文。

## 集合结论：非空、正性及双阈值

`closed_saturated_contains_palindrome_of_saturation` 的非空条件是 `∃n,0<n∧S n`，强于只允许零元素的非空集合。`hclosed` 只要求对正的成员前向闭合。证明以该正起点为归纳基，逐步调用核心 `orbit_positive n hn k`，因此每次应用 `hclosed` 的正性前提都有真实证据；不要求未经证明的全体自然数闭合，也不会把集合 `{0}` 错误当成目标反例。

`SetSaturatedAbove S M C` 要求在每个 `L≥C` 内，同宽、同余的两个实际规范十进制数具有相同成员资格。它允许不同长度采用不同的余数集合；对 `0` 或没有规范表示的对象没有不必要要求。

回文饱和阈值 `B` 与集合饱和阈值 `C` 分别从两个存在性假设取得。证明把前者提升到 `max B C` 后寻找轨道状态，保证同时满足两个阈值，避免从“最终”集合性质错误推到过短位数。归纳得到 `S(orbit n t)` 后，用 `S(orbit n t)↔S p` 的 `.mp` 方向得到 `S p`，并保留 `p>0` 和实际 `Palindrome p`。

## 非循环性与证据限制

| 模块或接口 | 前提来源 | 是否留下或循环使用目标结论 |
|---|---|---|
| `ModularSpan` | 只导入 `Std`；欧几里得算法与整除条件 | 没有饱和性、轨道或回文假设。 |
| `ResidueOrbit` 必要方向 | 核心真实反转、规范数字、已给回文 | 从见证推出限制，未调用充分性。 |
| `ResidueOrbit` 匹配/集合方向 | 显式 `SaturationAbove` 或其存在性假设，加核心轨道事实 | 条件性在声明中完整可见；不在本文件伪造存在性。 |
| 固定核心轨道兼容接口 | 实际轨道数字增长、模 11 与单位数字事实 | 核心只导入 `Std`，不反向导入本贡献。 |
| 下游 `Saturation.exists_saturation_bound` | 模数分解、正周期、外块、权重、span、位置池及 CRT | 单独构造饱和性，再用于关闭条件性推论；不借集合结论或轨道匹配来证明自身。 |

对两份固定目标源码进行受限文本扫描，没有发现 `sorry`、`admit`、`native_decide` 或自定义 `axiom` 声明。此扫描是源码检查，不等同于 Lean 的传递公理审计。最终完整构建、可执行证据和公理闭包应引用 environment 专员的独立结果。

本次没有发现需要修补的目标声明。对核心直接接口的追读用于确认本贡献调用的真实语义和非循环依赖；本报告不声称重新独立审计既有核心中全部四千余行证明。
