# Agent 111 数字层作者对总定理和位置池的独立源码审阅

日期：2026-10-15。结论：**在下列固定源码版本中，未发现阻断性缺陷。**

本次独立审阅对象是其他作者编写的 `Saturation.lean` 与 `DigitPools.lean`，并追读 `ArithmeticCRT.lean`、`ModularSpan.lean`、`PairWeights.lean`、`OuterBlock.lean`、`ModulusSplit.lean`、`PeriodExistence.lean`、`ResidueOrbit.lean` 的相关组合契约。本审阅者是 `PalindromeDigits.lean` 的作者，因此**不把该文件计作独立审阅成果**；只检查位置池对它的接口实例化是否满足声明的前提。普通反转和精确数字表示的语义取自现有核心 `Lychrel196Research.lean`。

本报告属于独立源码与数学语义审阅。没有把作者提供的编译成功记录当作本次独立全链条 fresh build；最终新目录重建与公理检查由另一专员完成。本次没有修改 Lean 源码。

## 固定源码 SHA-256

| 文件 | SHA-256 |
|---|---|
| `Saturation.lean` | `a638ff9844afa378dfe168feeaa8be372d2f2b5f6f3c1ff62ca5c2fe9f0685e0` |
| `DigitPools.lean` | `40981b1b8f2874c9ed179e113f5dae95776c0cfe9e1e49fa521fe4cee61aa7ec` |
| `ArithmeticCRT.lean` | `c5709b1de255e43d84a4d323257b13f9a314872d77cae955ac9c0c088ced59a5` |
| `ModularSpan.lean` | `1cad197771ad6a4a9577ac08d3e1a4afe143e354a96a261b8ebaa2c687c09754` |
| `PairWeights.lean` | `8b4d5b4b85a9c1957705ca13cc848483418593a7268818ba2f0e791b8d19c7ae` |
| `OuterBlock.lean` | `bccb6914ec1070c5d291881af8c806bb6735f9369b45b79029dc19662a163705` |
| `ModulusSplit.lean` | `b5d01b31bb37c24c60b8af544329f86341637af7d442ca29aaca7ac60a49bf7f` |
| `PeriodExistence.lean` | `e670385bb0e423fdb9db8f487bd53d5ab4bc4d745cad37f2de20f1f832f6e6dd` |
| `ResidueOrbit.lean` | `989e42134e6ae6c05775f569cc1b4cd916d0d45d5d87b6e471cbf3fe3e2cdfc6` |
| `PalindromeDigits.lean`（仅固定接口依赖；非本次独立审阅） | `323bee6eee1e85ec6f8e75226e2f037ee8f5bf2cfa07b25d0ea7b7fd9211789f` |
| `proofs/research/Lychrel196Research.lean`（既有核心语义依赖） | `f8950d138fa4231b536059e2334d36b6496de3d25a806f4cf3925941aa05144c` |

## 量词和覆盖范围

`Saturation.lean` 的 `exists_saturation_bound` 对每个 `M : Nat`、`0 < M` 构造一个 `B`。`B` 由只依赖 `M` 的分解 `k,u,q` 及模 `q` 的正周期 `r` 得到。`SaturationAbove M B` 的定义随后量化 **所有** `L ≥ B` 和 **所有**自然数 `a`；没有把阈值偷偷放到 `L` 或 `a` 后面，也不要求 `a < M`。

`exact_length_palindrome_residues` 保持 `∃ B, ∀ L, B ≤ L → ∀ a, ... ↔ ...` 的正确顺序。右侧正是单位数字限制与偶数位的 11 限制。`decimal_modulus_decomposition_coprime` 和 `exists_positive_ten_period` 都在总定理内部实例化，不把分解或周期作为未完成的外部假设。`M = 0` 被最终定理明确排除；`saturation_of_split` 自身的正 `u,q` 也使 `M=u*q` 必定为正。

明确界 `2*k+4*q*r` 适用于任意符合接口的 `k,u,q,r`。代码没有声称选到最小 `k`、最小正周期或最小阈值；自动分解可能返回比纸面最紧选择更大的 `k`。这是正确的适用范围，不是存在性定理的缺口。

## 位置池与精确位数的实例化

`DigitPools.lean` 的 `alignIndex` 满足 `k ≤ start < k+r` 且 `start % r = a % r`。其中自然数减法没有丢失所需信息：`k % r < r` 保证 `a+r-k%r` 是预期的非负差。

`positions` 实际递归构造有限列表，长度恰为指定计数。`positions_endpoint` 提供最后一项所需的强界 `i+r ≤ start+r*n`；配合 `start<k+r`，得到 `n≤q` 时严格的 `i<k+q*r`。因此没有因对齐偏移而多消耗一个周期的空间。

第一个池位于 `[k,k+q*r)`，第二个池位于 `[k+q*r,k+2*q*r)`。`selectedPositions_nodup` 用这两个空间区间证明跨池不同，池内则用 `r>0` 证明严格增长。该证明只需限制第一池长度就能证明跨池不同；第二池长度限制在 `selectedPositions_bounds` 中另外使用，不存在遗漏。

`L ≥ 2*k+4*q*r` 推出每个被选位置满足 `k≤i` 且 **严格** `i<L-1-i`。它排除了中心自配对、不同低位与镜像位碰撞，并保证镜像位置也至少为 `k`。最紧边界 `i=k+2*q*r-1`、`L=2*k+4*q*r` 时仍有 `L-1-i=k+2*q*r>i`。

`residue_pools_realize` 将上述具体 `Nodup` 与 `LowerPositions` 证明传入 `two_pool_realization`，并使用 `positions_length` 把两个列表长度还原为 `x,y`。两个权重相等式来自实际索引余数和镜像周期定理；没有把目标余数作为数字构造的假设。该接口返回核心的 `DecimalDigits.Canonical P d L` 与 `Lychrel196.Palindrome P`。核心 `Canonical` 包含数字界、非零最高位及 `value d L=P`，`Palindrome` 定义为普通 `reverse10 P=P`；未观察到局部定义遮蔽或替换。总定理又由同一个 `hc` 导出 `0<P`。

## 边界与敌手检查

| 检查点 | 结果与理由 |
|---|---|
| `M=1` | 分解允许 `u=q=1`；正周期存在，全部模 1 余数等于 0。兼容性条件为真，仍返回正的真实回文。 |
| `q=1` | `shifted_modular_span` 的 `x<q,y<q` 强制 `x=y=0`；两池为空，基础外框已完成要求。没有调用模逆或要求 `q>1`。 |
| `r=1` | 两种索引标签都等于 0，但两个空间区间仍不相交。第二池条件使用 `i%r=1%r`，没有错误地要求余数等于自然数 1。 |
| `a=0`、`10∣M` | 不兼容，必要条件拒绝它；总定理没有承诺构造以 0 结尾的正回文。 |
| `a=0`、`10∤M` | 允许的零余数没有遗漏。若 `a%u=0`，外块构造可选择 `A=u`；它由 `10∤u` 保持非零单位数字，并由适当真因子界得到 `A<10^k`。 |
| `u=1` | 外块可取非零单位数字，模 1 保持条件平凡，CRT 仍成立。 |
| `u=10^k` | 兼容性保证余数单位数字非零，因此使用不加 `u` 的分支；不会构造越界外块。 |
| 偶数 `L` | 三元 gcd 为 `gcd(q,11)`，由 `q∣M` 推出它整除 `gcd(M,11)`，进而整除 `a`。外框由偶数对称性被 11 整除，满足同一个 gcd 条件。 |
| 奇数 `L` | 权重 gcd 为 1，两个 span 前提均由 `1∣_` 给出；没有额外的 11 限制。 |
| `11` 的高次因子 | 权重 gcd 精确等于 11，而非只证明它被 11 整除；因此不会错误增加 `121∣a` 等要求。 |
| 指数中的 `L-1`、`L-2` | `k≥1` 和长度界在调用前推出 `L≥2`；镜像周期运输另外取得 `i<L`，自然数截断不会改变所用差值。 |

## 模数拼接与必要方向

`shifted_modular_span` 使用 `b=a+q-C%q`，而不是会截断负差的 `a-C`。由于 `C%q<q`，有精确恒等式 `C%q+b=a+q`。其三元 gcd 同时整除 `a`、`q`、`C`，因此整除 `C%q` 和所选 `b`。最终得到的等式方向为 `(C+x*c0+y*c1)%q=a%q`。

总定理中 `hPu : P%u=A%u` 与 `hAu : A%u=a%u` 正向传递；`hPq` 与上述 span 等式也正向传递。`crt_mod_eq` 的结论是 `P%(u*q)=a%(u*q)`，随后 `M=u*q` 的重写与目标一致。CRT 证明使用整数差与 Bézout 恒等式，不要求 `P≥a`，故自然数大小顺序不构成漏洞。

必要方向在 `ResidueOrbit.lean` 中从真实 `Canonical`、真实 `Palindrome` 及 `p%M=a%M` 推出兼容性：正回文单位数字非零；偶数位回文被 11 整除；这两项经整除 `M` 的因子沿余数等式运输。最终 iff 的必要与充分两条方向没有交换或减弱。

## 后续推论与审阅边界

`every_orbit_matches_palindrome` 只断言某个实际轨道状态与构造回文同宽同余，不声称两数相等或轨道命中回文。`fixed_modulus_closed_set_contains_palindrome` 将构造出的饱和阈值和集合的最终饱和阈值取最大值；正性保证正数域上的前向闭合可逐步应用。其转移方向为从轨道中的集合成员推出同宽同余回文属于集合，与所声明结论一致。

未发现需要修改的 Lean 声明。此报告支持上列哈希版本的组合证明和边界处理；不替代对本人所写数字语义文件的独立审查，也不替代最终 fresh build 与全依赖公理审计。
