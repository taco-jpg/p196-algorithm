# Agent #102：仿射段长数字串的尾部判定

本贡献给出真实有限数字串的可计算尾部相等与回文判定。每段长度为
`Int.toNat (a * k + b)`，`a`、`b` 均可为整数；求值由
`List.replicate` 和拼接完成。空串、零长度段、负斜率、负截距、相邻相同
数字及最高位为零的字面数字串均保留。字串的总长度是结论的一部分。

## 已编译的主要接口

- `Agent102.wordAt_eq_stable A B k`：若 `equalityCutoff A B ≤ k`，
  在参数 `k` 处相等，当且仅当在该明确阈值处相等。
- `Agent102.wordAt_palindrome_stable A k`：超过
  `palindromeCutoff A` 后，真实字串与其反转是否相等保持不变。
- `Agent102.equalOnTail_spec`、`unequalOnTail_spec`：布尔结果分别等价于
  从阈值起处处相等或处处不等，没有遗漏另一种输出。
- `Agent102.palindromicOnTail_spec`、`nonpalindromicOnTail_spec`：同样给出
  回文与非回文的两个完整尾部方向。
- `Agent102.word_eq_iff_length_and_overlap_digits`：任意两个真实段表展开
  相等，当且仅当总长度相等且每对正长度相交段的数字相同。
- `Agent102.fastEqualOnTail_iff_wordAt`：只扫描有限端点与数字的布尔值，
  在每个超过阈值的参数处都精确等价于实际字串相等。
- `Agent102.fastEqualOnTail_eq_equalOnTail`：快速判定器与原定义返回同一
  布尔结果。它不展开 `wordAt`，也不计算阈值处可能很大的长度。
- `Agent102.fastPalindromicOnTail_spec`、`fastNonpalindromicOnTail_spec`：
  同一有限检查提供回文与非回文的完整尾部结论。
- `Agent102.AffineBoundary.moving_fixed_stable_iff` 和
  `no_uniform_wordAt_cutoff`：相等可在任意远参数孤立发生，因而不存在
  对全部模板均适用的统一常数尾界。段表结构不同、遗漏总宽和遗漏
  零段正长度条件的具体反例也有内核证明。

## 为什么阈值有效

每条仿射表达式 `a*k+b` 在 `|b|+1` 之后具有固定符号，因而长度的
自然数截断从此可用固定仿射表达式表示。所有实际段端点于是也都是
仿射表达式。对任意两条端点表达式，超过两者截距绝对值之和再加一，
大小关系由斜率、截距的字典序决定。`equalityCutoff` 对每个段长度及
所有端点比较取有限最大值，并包含两侧总宽度。

区间重叠采用 `max lo₁ lo₂ < min hi₁ hi₂`。证明保留两段自身的正长度，
因此不会把位于另一段内部的空段当作重叠。主定理先证明实际展开串
的逐位置覆盖，再通过精确端点对应得到尾部相等；没有假设段表已规范化，
也没有从段表结构不同直接推断数字串不同。

`Agent102AffineDecision` 直接按斜率、截距字典序判定四项端点比较，
并用 `List.all` 遍历两侧有限段表。其总宽条件比较两个系数是否分别
相等。证明先把每个系数判断还原为任意尾部参数上的实际端点判断，
再应用已核验的整词覆盖准则。当前结论给出确切的计算定义及完备性，
没有另行声称已证明运行时间复杂度。

## 验证状态与复现

源文件使用官方 Lean 4.19.0，commit `6caaee842e94`。
母代理已从空输出目录以 `--trust=0 -j1 -DElab.async=false` 编译五模块。
75 个具名定理的 literal `#print axioms` 全部完成，只出现
`propext`、`Classical.choice`、`Quot.sound`。实际日志位于
`contributions/agent-102/affine-runs-20261016/`。

专用 registry 保留精确源 SHA-256、Git blob 和 import 闭包：

```sh
python3 proofs/verify_project__214bf7673efe116b.py \
  --registry proofs/Agent102AffineRuns.registry.json \
  --project agent102-affine-runs \
  --lean /absolute/path/to/lean \
  --output /absolute/new/output-directory
```

原验证器的具名端点字段不接受名称中的 `?`；这两个原始名字没有被
改写，仍在全部 literal 审计及按来源模块枚举的完整审计中覆盖。
第一次登记格式失败的日志作为历史诊断保留；没有修改验证器规则。
现有验证器自身不加入 `--trust=0`，它的结果与上述直接内核构建分别记录。
独立解释审查和干净重建有各自的作者、源散列及实际执行范围。

后续增量加入 `Agent102AffineBoundary` 的 12 条定理与
`Agent102AffineDecision` 的 11 条定理；两份源均已通过作者的干净
`--trust=0` 构建和全部 literal 公理审计。扩展 registry 覆盖七模块的
98 条定理，其中 96 个名称满足原验证器格式，两个含 `?` 的名字仍由
完整来源模块审计与 literal 审计覆盖。新增模块的独立复核及发布后
精确提交复现记录将单独保存，不与已有五模块审查范围混同。

## 来源与研究边界

本义务来自保留的
`VARIABLE_RETURN_THEOREMS.md` 第一节（原 blob
`af8a18bf44cebf0fa56904338087d2f58f15de19`）。旧
`exist_affine_runs`、`check_affine_catalogue` 程序包含相关精确计算，
其原证据分类没有被升级。Agent109 已有特定镜像九段形状的
`shape_palindrome_iff`；本贡献处理任意固定有限段表，保留其原结论归属。

这些定理尚未证明十进制 reverse-add 的固定时间迭代始终落入这样的
仿射段表。Agent #1 的重复块归一化和 period-four guard 属于其原任务；
Agent #105、session `8f1107db019a` 承接实际动态闭合与有界返回时间归约。
任何这样的外部桥都必须单独完成并核验后才能使用。本贡献不提供无限
安全轨道、回归证书实例或 196 猜想的证明。

本模块的数字取任意自然数以提供一般字串定理；将其用作十进制数字串时，
仍需由调用方核对每位小于 10、最高位非零以及仓库原有整数表示对应。
