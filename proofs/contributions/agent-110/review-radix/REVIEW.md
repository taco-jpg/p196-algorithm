# RadixExterior 独立审查：接受其限定结论

审查人：**Agent 110 runtime/audit specialist，`/root/runtime_audit`**。
这是与 `RadixExterior.lean` 作者分开的审查执行。额外只读语义复核人是
`/root/runtime_audit/radix_semantics`；该辅助复核没有编译 Lean、运行作者
checker 或写文件。以下重建和整数控制由主审查人实际执行。

冻结源码 SHA-256：

`3aa5f400f939b7888a8e503cc1489514222701078449492f375681129c8e5716`

父代理在审查完成期间提供的远端复现 pin 为
**`1cdc55c89b376faa270d1dffaf21e21b6eedeb4b`**（仓库
`taco-jpg/p196-algorithm`）；对应本地提交为
`ee54c6e7d95cf9cd5d1a4bd530aa2773ac22f33b`，树为
`a01ca07a2ff49f3dae2aa8dd97483e8e624915b8`。
复现者应固定该远端提交并核对上述 source SHA-256；本审查实际验证的是该
源码哈希及记录的三个依赖源码哈希。审查人没有执行 Git 或远程操作。

没有发现新文件中 15 条定理的实质数学错误或错误的结论范围。接受的结果是
关于 **`(phase,Z)` 这一特定观察量的信息不足及其进展势函数限制**。
它既不构造外部状态周期，也不证明全局无周期，更不证明 196 的任何无穷结论。

## 1. 独立重建与公理结果

主审查人重新读出并列出了实际依赖链：

`Std → ExteriorCore → ExteriorCapTwo → ExteriorCoverage → RadixExterior`。

新建时不存在的 `/workspace/scratch/63e10b24caf2/radix-review-build` 作为唯一
项目 `LEAN_PATH`。四份源码从原路径逐字节复制，所有 `.olean` 均在该空目录
现场产生；没有读取作者 `.olean`，也没有读取 `dev-deps`。运行时使用已固定
官方 Lean 4.19.0 / commit `6caaee842e94` 与明确记录的当前进程 readlink
兼容适配器。没有修改官方编译器或标准库。

| 模块 | 显式公共定理 | 其他显式公共声明 | 编译时间（秒） |
|---|---:|---:|---:|
| ExteriorCore | 2 | 10 | 0.525 |
| ExteriorCapTwo | 3 | 0 | 29.146 |
| ExteriorCoverage | 5 | 1 | 0.926 |
| RadixExterior | 15 | 12 | 0.943 |

独立 scanner 枚举并核对了这四份源码中的全部 **48 个显式公共声明**，包括
25 条 theorem 及 23 个 def/abbrev/structure。它不是作者 checker；对于本次
源码所需语法采用失败即停止的解析方式，并检查声明 token 总数。
独立 `ReviewerAudit.lean` 对每个名字恰好查询一次传递公理集。

结果：四次编译、版本查询、完整公理审计均 exit 0。48 项结果无缺漏、无重复；
实际公理并集只有 `propext`、`Quot.sound`，没有 `Classical.choice`、自定义
axiom、`sorryAx` 或 `Lean.ofReduceBool`。源码去注释后还排除了 sorry/admit、
native_decide、unsafe、implemented_by 及声明生成语法。新文件中的有限
`decide` 等式与不等式见证全部无公理。

四份原源码及复制源码在编译后再次校验，哈希未变。完整 argv、环境、时间、
源码/对象/输出哈希、48 项逐声明结果及签名身份在 `verification.json`；
完整输出在 `logs/`；独立源码副本在 `source_snapshots/`。`rebuild.py` 是实际
执行的主审查程序。仓库中的这份审查目录不含编译二进制。

`ExteriorCapTwo` 的有限枚举只是现存 `Canonical` 定义导入链的一部分。
本次障碍证明没有使用 cap-two 枚举结论，不能将此次重建宣传为新的宽度界。

## 2. 所用映射确为原有 outer 更新

新文件没有重定义 `advance`。从未修改的 `ExteriorCore` 可直接读到：

- `k = 1[c ≥ 10]`，`t = c − 9k`；
- `(D,e) = norm B 0`，`(E,γ) = norm (reverse B) k`；
- `u = c + e − 10k`；
- 若 `γ=0`，raw 为 `(D ++ [u]) + (reverse E ++ [t])`；否则为
  `(D ++ [u]) + ([1] ++ reverse E)`；
- 下一 phase 为 `2t`，下一外部字为 raw 去掉最大 `2t` 后缀。

这逐项对应原 complementary-band 说明中的真实归一化外部公式。
`overflow` 也直接取同一个 `norm (reverse B) k` 的末进位，没有自由选取进位。
这里的“actual”准确指上述确定的原映射；新 Lean 文件没有新证明一个对所有
普通整数、所有 gap 的语义桥接。

为独立检查有限语义，主审查人另写 `semantic_controls.py`，不导入作者 Python
程序。它以中央 phase 字长 **9、10、17** 构造三份普通十进制整数，直接使用
整数加法及十进制字符串反转，逐步计算新的实际数字 mirrored-sum word，
验证其外部字、phase、中央常数字段以及实际位数增长。全部 **15 次加法**
匹配下述五步外部路径；完整整数和字保存在 `semantic-controls.json`。
这是有限语义控制，不能替代一般 bridge 或无穷安全性的证明。

## 3. Z 的精确定义和见证

`value10 B = Σ Bᵢ 10ⁱ`，其中列表首元素赋最低指数；
`centeredValue c B = Σ(Bᵢ − c)10ⁱ`。
`centeredValue_formula` 对任意有限 B 证明：

`9 centeredValue c B = 9 value10 B − c(10^length(B) − 1)`。

因此 `radixDefect` 正是所宣称的 Z。附加任意数量的 phase 字母 c 不改变
centeredValue，也不改变观察量 `(c,Z)`；归纳证明没有长度或 canonical
假设遗漏。Z 可以为负，代码使用 Int，不会产生 Nat 截断。

独立手算与整数控制都得到：

| 时间 | phase | 外部字 | Z | 下一步 overflow |
|---:|---:|---|---:|---:|
| 0 | 6 | `[13]` | 63 | 1 |
| 1 | 12 | `[4,10]` | −252 | 0 |
| 2 | 6 | `[9,1]` | −423 | 0 |
| 3 | 12 | `[18,2]` | −846 | 1 |
| 4 | 6 | `[9,11,5]` | −423 | 1 |
| 5 | 12 | `[10,1,7,11]` | −14508 | 未用于证明 |

六个状态的 phase 都为允许的正偶数，所有系数在 0..18，非空字首系数为正，
末系数不同于当前 phase，故都满足原有 `Canonical`。

`ReachedAfterOverflow s` 表示存在一个 canonical 祖先 a，其计算出的
overflow 为 1，而 s 是从 `advance a` 开始再迭代有限步得到。取时间 0 的
ancestor 后，source/middle/endpoint 分别再迭代 1/2/3 步，见证完全正确。
该定义没有声称祖先来自 196，也不声称整个轨道无限存在于某个 safe 类中。

时间 2 与时间 4 只有观察量相等。其字长分别为 2 和 3，状态严格不等；
`witness_not_state_return` 对这一点有单独 kernel 证明。不得把表中的观察值
回返称为外部状态周期。

## 4. 两个主要障碍定理的逻辑

**`no_autonomous_radix_factor`：正确。** F 被要求在所有同时 canonical 且
ReachedAfterOverflow 的状态上给出观察量下一值。source 与 endpoint 都在
这个量化域内，输入观察量都是 `(6,−423)`，而后继分别是 `(12,−846)` 与
`(12,−14508)`。单值函数不可能同时满足这两个等式。定理只排除此指定观察量
上的统一确定性更新，允许使用更丰富的状态信息或限制到不含这两个见证的域。

**`no_overflow_strict_radix_observable`：正确。** P 只能依赖观察量。证明
取 source→middle 上的 weak 关系和 middle→endpoint 上的 strict 关系，
后者的实际 overflow=1。给定混合传递性 `weak a b ∧ strict b c → strict a c`
可推出首尾 strict；首尾观察量相等便违反 strict 非自反性。
证明不需要额外假设 weak 的反身性、strict 的全序性或任意长链归纳。
整数势函数包装使用普通 ≤ 与 <，由 omega 证明所需关系性质，范围准确。

它排除的是依赖 `(phase,Z)` 且**每一步弱增加、每个实际 overflow 严格增加**
的指定势函数类。它没有排除更详细的有序信息、额外 carry 记忆、非单调论证，
也没有得出所有外部周期存在或不存在的结论。

`radix_observation_is_order_sensitive` 正确表明该观察量并非普遍反转不变：
交换 `[1,5]` 与 `[5,1]` 可以改变 Z。它不声称 Z 对外部状态单射；主要反例
恰好证明这种单射信息不足。

## 审查签署

**Reviewed-by: Agent 110 runtime/audit specialist (`/root/runtime_audit`)**

辅助只读手算复核：`/root/runtime_audit/radix_semantics`。
签署针对上述冻结 SHA-256 和此目录记录的实际执行；这是明文审查身份声明，
不是密码学签名。最终 verdict：**ACCEPT WITH STATED SCOPE**。
