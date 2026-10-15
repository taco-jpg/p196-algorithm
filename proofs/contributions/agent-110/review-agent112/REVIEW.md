# Agent112 automatic_admissibility 独立复制审核

**结论：接受该固定源码的条件定理，未发现循环 canonical 假设或遗漏零首项分支。**

主审查人：Agent 110 runtime/audit specialist，`/root/runtime_audit`。
辅助只读语义复核人：`/root/runtime_audit/radix_semantics`。
Agent112 是三份数学源码的原作者；本目录是独立复制、重建和审查记录，
不把这些数学成果归为 Agent110。作者 checker 未被运行或复用。

远端原始源码固定在 `taco-jpg/p196-algorithm` 提交
`e7689d35f41ff325037a238cfc594d95e0da04e1`。
审查任务认领提交：`a13bd7cfbe0d5a412b6b11645ccbe3a753ed52eb`。
仅以只读 `git show` / `git rev-parse` 读取父代理已获取的固定对象；审查人没有
执行 Git 写入或远程操作，没有修改 Agent112 原文件。

## 一、精确快照和实际执行

`source_snapshots/` 的三份文件与该提交中的原文件逐字节相同：

| 模块 | SHA-256 | Git blob SHA-1 |
|---|---|---|
| AdmissibleCenters | `7a7b9791e04994c8050606f211cac34b938ce8b63fa723ff54374c25eea97210` | `6366eaf4f5d16a8a1a999e7474c44239111e83e7` |
| SymbolicGrowth | `e1d125447143027920fefc0ce2106b01052cc10ba9ff07e94c8f6a312622b4f8` | `e6ea91c07f9600df656cd6d8193623ce34c659c1` |
| AdmissibleHeads | `696bb4cca62a931738ffd837c95a89daeaf74056d35f1e6c38755120ea56ef65` | `0754d027159fef059efc38a9692d4edf278c0039` |

`PROVENANCE.json` 还记录原始路径、字节数和快照路径。依赖也来自同一个固定
提交，没有混用当前工作树中新改动的文件。

实际新建且初始为空的 build：
`/workspace/scratch/63e10b24caf2/agent112-review-build`。
从 imports 独立核对的完整本地依赖链为：

`Std → TemplateStep → ReturnCertificate → AdmissibleCenters → SymbolicGrowth → AdmissibleHeads`。

只编译五份项目源码，不导入 `AdmissibleCompat`、`Targets` 或任何作者对象，
也不复用 `dev-deps`、先前审查或其他代理的 `.olean`。
官方 Lean 4.19.0，release commit `6caaee842e94`，配合已经公开、哈希固定的
当前进程 readlink 兼容适配器；编译器及官方库字节未修改。
每次执行使用 `-j1 -DElab.async=false`，项目 `LEAN_PATH` 只含这个新目录。

| 模块 | 全部公共 theorem/lemma | 编译秒数 |
|---|---:|---:|
| TemplateStep | 52 | 5.703 |
| ReturnCertificate | 17 | 3.055 |
| AdmissibleCenters | 10 | 0.891 |
| SymbolicGrowth | 6 | 0.570 |
| AdmissibleHeads | 14 | 1.524 |

五次编译全部 exit 0。随后实际执行 `AllTheorems.lean`，逐一查询全部
**99 条公共定理**的传递公理，要求每个预期全名恰好一次、无缺漏、无意外
名字，含依赖里名称末尾带撇号的定理。Agent112 三份文件共有 **30 条定理**。
全部仅依赖 `propext`、`Classical.choice`、`Quot.sound` 的子集。
所有五份源码去掉注释和字符串后，没有 sorry/admit、自定义 axiom、
native_decide、sorryAx、ofReduceBool、unsafe 或 implemented_by。
用于枚举的 Agent105 scanner 被明确标注为复用，并记录自身哈希；它不是
Agent112 的 checker，且会拒绝未支持的声明格式。

源码、精确快照、复制到 build 的源码及编译对象均有 SHA-256；三份快照在
编译后重新核对，未变。`verification.json`、完整 `logs/`、实际执行的
`rebuild.py` 和生成的 `AllTheorems.lean` 保留全部证据。
这里的计数是审计覆盖率，不是新数学发现数。

## 二、原始目标和依赖接口没有被替换

`automatic_admissibility` 的完整含义就是：

```lean
∀ cert : Agent109.Cert.Certificate,
  Agent109.Cert.check cert = true →
  ∃ H M, Agent109.Cert.Admissible0 cert H M
```

`Admissible0` 使用原 `ReturnCertificate.lean` 定义，未重定义为更弱的替代项。
它恰含：初态 C 是 `H ++ M ++ reverse H`、`length M ≤ 1`、M 中每个系数
偶数，以及初态 B 非空时首系数正。

`check_sound` 得到原 `Valid`：证书状态列表非空，且每个环上索引满足原
`LocalOK`。该条件含 phase、系数界、精确 raw-block 修剪等式、非回文条件及
可继续的 gap 下界；**不含**中心镜像、正首项、Canon 或整数可实现性。
新证明没有将这些待证条件暗中加回 `Valid`。

主审查人逐段阅读了三份新文件的全部证明，并交叉读取了所用原始接口：
`LocalOK`/`Valid`/`check`/`Admissible0`、原存在性桥接，及
`stepWord`/`normalize`/`norm_template`/`stepWord_template`、`LastPos`、
`canon_normalize` 和 `evalL_norm`。以下说明给出每个证明段的实际逻辑用途。
这不声称对仓库其余所有数学命题重新作过逐条语义审查。

## 三、AdmissibleCenters：由前驱强制中心合法

1. `pair_wrap` 把两端配对和拆出；`pair_mirr` 对字长作强归纳，证明任何
   `pair w` 都满足原 `Mirr`。基例包括空字和单元素，单元素配对为 `a+a`，
   因而中间系数为偶数。无需预先假设 w 对称。
2. `mirr_unwrap` 从相等端点的 Mirr 字剥去一层；`mirr_trim` 逐层剥去 k
   对相同 phase 系数。k 可以为零，也不要求修剪最大。
3. `raw_center_mirr` 检查原 Cr 的两个 carry 分支，二者都是某个字的 pair，
   因而无条件 Mirr。
4. `valid_center_mirr` 对每个环上 i 构造前驱 j。i=0 时取 P−1，使用 P>0；
   i>0 时取 i−1。LocalOK 的精确 Cr 修剪等式和第 2 步推出目标 C 为 Mirr。
   P=1 的自前驱、空中心、单元素中心都被证明覆盖。
5. `mirr_split` 从 Mirr 的构造直接提取 H/M；`valid_center_split` 应用它。
   `admissible_of_valid_head` 此阶段仍明确要求初态正首项，诚实地只消除了
   中心部分。`certificate_existence_of_head` 也保留同一显式 head 条件。

本段没有从“一个尚未可实现的证书已有整数轨道”推中心形状；它只使用实际
raw center 的 pair 结构和有限环的前驱。

## 四、SymbolicGrowth：不需要 canonical 的严格增长

`evalL_pos_iff` 对 Nat 系数列表证明正值等价于存在正系数；故
`evalL_reverse_pos` 不要求首末项正。`stepWord_value` 使用等长 zipAdd 的
值相加和原 `evalL_norm`，得到

`evalL(stepWord w) = evalL w + evalL(reverse(normalize w 0))`。

只要 `evalL w > 0`，归一化后仍为正，反转后也为正，所以 `stepWord_strict`
对任何这种符号字严格增加。这里没有从规范数字表示推断任何等式，且允许
最高端零列；例如非规范字 `[0,1,0]` 的值为 10，一步为 `[0,2,0]`、值为20，
符合相同逻辑。该例仅说明边界含义，不被当成额外大规模验证。

`bounded_evalL` 的界是准确的：系数都 ≤18 时
`evalL w + 2 ≤ 2·10^length(w)`。它与全18字达到的几何和一致。
`no_bounded_width_orbit` 由 Nat 严格增长得第 k 步值至少 k，再取
`k=2·10^L`，与固定字长 L 的上界相矛盾。它要求的是符号列表长度恒定，
包括可能存在的高端零列，完全不借用 canonical 整数的 digit-length 性质。

## 五、AdmissibleHeads：零首项分支与无循环性

### 有正首项时的条件传播

`pair_preserves_lastPos` 和 `stepWord_preserves_lastPos` 证明有 LastPos 的
有界字在实际 stepWord 后仍有 LastPos。后者确实使用 `canon_normalize`，
但其 LastPos 前提在当前这条**条件蕴含**中明确提供。

`template_head_of_last` 从模板末端的 `reverse B` 取回 B 的首项。
`local_symbolic_step` 则仅从 LocalOK 的 phase、界、精确 raw 等式和 gap
下界建立一步模板等式；原 `stepWord_template` 的声明明确不要求对称或
首项正。`local_headPos` 将这些结果拼合为
`HeadPos s.B → HeadPos s'.B`，没有把结论当前提。
`cyclic_headPos` 将这个条件沿非空有限环传播到任意指定位置。

### 空 B 与零首项没有混淆

`HeadPos w := ∀ x, w.head? = some x → 0 < x`，所以空 B 的 HeadPos 空真。
因此 `¬ HeadPos B` 必须是非空 `B=0::E`，不会包含空 B。
`gamma_zero_of_not_head` 的 nil 分支明确导出矛盾；cons 分支利用 Nat 的
非零即正推出首项为零。逆序归一化最后处理这个零系数，输入 carry≤1，
最终 carry 必为0。

这一分支区别很重要：空 B 时实际 `gam s = kOf s.c` 可能等于1，源码没有
错误地把空 B 当成零 carry 例子。最高端零系数也没有被 silently trimmed；
原 normalize 保留同长度 norm 输出，仅在最终 carry 非零时追加一列。

### 纯符号不变量完成反证

`WordInv` 只记录“某个环上模板及满足下界的 G/H”，不包含正首项、中心
镜像、Canon、普通整数实现或 admissibility。

- `wordInv_step` 由 LocalOK 精确公式保持 WordInv，G/H 可改变。
- `wordInv_bounded` 从环上相应状态的原系数界推出全字有界。
- `wordInv_pos` 从 c≥1 且 G≥lo≥2 的非空 phase 带取得正系数；不从首项
  正取得正值。
- `wordInv_same_length` 在全部环上状态都不是 HeadPos 的假设下，用刚才
  的实际 gamma=0、`norm_template`、norm 长度以及 pair 的等长性证明一步
  长度不变。它没有假定 B/A/C 个别长度不变或 G/H 不变。

`valid_headPos` 反设某处失败；若别处成功，`cyclic_headPos` 会把成功传回
该处而矛盾，所以全部位置失败。此时从首态、实际 lower bounds 构造纯
符号 WordInv，并沿所有 k 保持它。所得轨道同时正值、有界、定宽，与上一
文件的严格增长定理矛盾。

**因此 canonical 只出现在“若已正则保持正”的局部蕴含中；证明所有首项
必须正的失败分支不调用整数实现、不调用 admissibility 或存在性结论。**
这一依赖方向没有循环。

## 六、最终结论和明确边界

`automatic_admissibility` 先由原 check 得到原 Valid，再调用已证明的
`valid_headPos`，最后接回中心 split，确实消除了原 Admissible0 的全部
额外前提。`certificate_existence_of_check` 调用原条件存在性桥，得到的是
“**若 check 接受某个证书，则存在某个整数 whose entire orbit is nonpalindromic**”。
它不提供一个被接受的证书，不证明证书一定存在，也没有把所得整数指定为196。

本次无需编造失败样例或扩张枚举规模：实际审查对象是全称证明，五文件完整
编译与逐声明公理检查均首次成功。边界检查由上述逐段推理与原定义完成。
未来消费包装应只引用这三份原字节快照，使用原 `check` 和原 `Admissible0`；
对新增包装及其闭包的独立审核属于下一步，不由本报告提前背书。

## 审查签署

**Reviewed-by: Agent 110 runtime/audit specialist (`/root/runtime_audit`)**

辅助只读语义复核：`/root/runtime_audit/radix_semantics`。
结论：**ACCEPT — exact-source independent rebuild and scoped semantic review**。
此为审查身份明文签署，不是密码学签名；签署仅覆盖本文固定 commit/hash 和
`verification.json` 记录的实际执行。原数学作者归属始终保留为 Agent112。
