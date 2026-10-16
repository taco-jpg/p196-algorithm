# Agent105UniformReturnPlain 独立审查

复核者：Agent #105 / lean_runtime。作者：Agent #105 / source_scout。
接受源码 SHA256：`0d4d048c017966827be4d146ef52d50de8ea3fc777fd7f21220c73694f5155af`。
复核者没有修改待审源码；本次只写审查材料和独立编译目录。

## 结论

两个公开纯返回端点的量词、实际运算语义和精确时间界均与目标相符。独立目录中使用官方 Lean 4.19.0、`--trust=0 -j1 -DElab.async=false` 重新编译该新模块，exit 0；再从该新生成模块逐条执行 `#check`、完整 `#print`（保留证明项）与 `#print axioms`，exit 0。两个定理的公理集合均为标准 `propext`、`Classical.choice`、`Quot.sound`。

本次新建待审模块的 `.olean`，没有使用作者的该模块输出；20 个传递依赖逐一核对仓库源 SHA、作者布局源 SHA、导入表，再复用既有同版 Lean 输出。`dependency-reuse-receipt.json` 保留精确来源与二进制哈希。因此本报告是“新模块独立 fresh 编译及语义复核”，不称为又一次全依赖 fresh 重建。大型全依赖检查按母代理安排单独进行。

## 逐量词审查

### uniform_bounded_return

前提是存在参数阈值，使每个之后的 k 都存在一个正整数时间 t，满足 `1 ≤ t ≤ B` 并给出实际等式 `Agent8.orbit (Q k) t = Q (k+s)`。这里的 t 可以随 k 变化。

结论把同一个 t 放在 `∃ K, ∀ k, K ≤ k → ...` 之前，所以得到整条参数尾部共用的时间，而不是仅有无穷多个零散参数。该 t 仍显式满足 `1 ≤ t ≤ B`。一般接口允许 s=0；只有第二个有正宽度增量的接口要求 s>0。B=0 时正时间覆盖前提不可能成立，有限选择定理正确处理这一退化情形。

其证明使用 `actual_return_tailStable` 和 `uniform_bounded_tail_selection`。前者由原列表轨道的已证固定时间仿射闭包及参数平移，结合真实展开字的等式稳定性得到；后者的有限候选集合为时间 1 至 B。稳定性由具体定理提供，没有在这个端点额外假设为尚未证明的算术事实。每个固定时间可有自己的尾部阈值，有限选择只需有限次合并阈值。

### uniform_return_wordAt

显式保留以下前提：固定有限 `RunSpec` 表、符号界 18、`0 < widthSlope rs`、`0 < s`、实际列表 eventual canonicality，以及每个充分大参数处存在正时间实际返回。前提和结论都没有 `SafeThrough`、非回文性或安全性假设。

证明首先合并 canonical、return 与 head/width 的三个参数阈值。对任一充分大的 k，取它给定的实际返回时间 t。头部在 k 与 k+s 处都落在已证常值尾部，从而得到原 potential 界所需的相同外符号。`wordAt_head_width_eventually` 同时给出实际自然数列表宽度差恰为 `widthSlope rs * s`，而不是截断后的形式差。

随后 `word_family_return_time_bound` 在完整 hA、hs、ht、canonical、实际返回、同头、宽度等式前提下得出 `1 ≤ t ≤ 4 * widthSlope rs * s`。这一步得到对每个尾部参数都有效的同一有限时间上界；最后再应用第一个纯返回端点选出全尾部共用时间。没有将输入的变时间存在性直接当作统一时间，也没有只对有限样本验证返回。

## 与原书面条款的对应

已读取原 `VARIABLE_RETURN_THEOREMS.md` 第 1 节。只读历史源与当前 `SOURCE_MAP.json` 中 SHA256 完全一致；原文和来源记录保留在 `references/`。

书面条款的纯返回断言先于可选的安全返回加强。本模块正好补足纯返回部分；原 `uniform_safe_return_wordAt` 处理额外给定安全返回段的版本。因此不需要为纯返回输入人为增加避回文性。

书面正长度仿射族的原斜率均非负时，`widthSlope_int_eq_slope_sum` 证明形式化宽度斜率精确等于原整数斜率总和 A。当前形式化还允许长度表达式经原 `.toNat` 语义最终消失、负截距和空游程；其真实 eventual width 由 Shape 模块处理。这不改变书面正长度族的实例。

原 `Agent8.CanonicalPair` 是列表谓词，没有附带奇数宽度中项偶性。故该纯列表端点不应单独表述成“任意此列表一定有普通整数实现”；实际整数版本必须带 `pairWord` 实现并通过原 Compat 桥转移。它也没有给出特定初值、变时间返回实例或无限避回文见证，不涵盖乘性参数更新或增长的游程目录。

## 完整尝试记录

新模块首轮独立编译成功。导出审计驱动第一轮因 `pp.width` 不是该版本有效的展示选项而 exit 1；该驱动、完整输出和失败回执保留于 `export-audit/attempt-001`。移除该展示选项后再次审计 exit 0，待审 Lean 源字节始终不变。

## 复现

```bash
cd /tmp/p196-agent105-toolchain/uniform-plain-review/attempt-001/source
LEAN_PATH=. /tmp/p196-agent105-toolchain/lean-4.19.0-linux/bin/lean --trust=0 -j1 -DElab.async=false -o Agent105UniformReturnPlain.olean Agent105UniformReturnPlain.lean
LEAN_PATH=. /tmp/p196-agent105-toolchain/lean-4.19.0-linux/bin/lean --trust=0 -j1 -DElab.async=false -o UniformPlainExportAudit.olean UniformPlainExportAudit.lean
```
