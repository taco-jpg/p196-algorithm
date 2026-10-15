# Agent107 独立审查：数学边界与执行状态

本文件由独立 review 子代理维护。**当前状态：独立 clean rebuild 与 66 个公开 theorem 的公理审计已通过；最终签署见 `REVIEW.md`。**

历史状态保留：本文件初稿仅审阅数学正文和源代码，当时为 source-only，尚未独立 build。后续 reviewer 亲自启动 exec session `23410`，产生 `review107-clean-okwe457n/manifest.json` 的 PASS 记录。恢复时已取得同一 session 最终 exit 0，并核对全部源码、快照和日志 hash 一致；没有重复构建，也没有用作者日志代替独立执行证据。

审查正文：`proofs/research/main_existence_attempt/renewal_pass/constructive/collision_response/SEAM_RESPONSE.md`。

## 1. 数学边界

1. **终端 carry 必须保留为单个系数。** 每个 isolated block 的末端 carry 放在它的原始长度处，不能把全局 terminal carry 在所有 `i >= L` 处重复。全局 `D` 在 `L` 处只有实际 `carry q L`，在 `i > L` 处为零。
2. **All-9 block 必须允许 run 长度等于块长。** 此时 isolated final carry 是零；输入 carry 仍可能穿过整个块并形成新的全局最高位。`B=(9,9), H=(18)` 的终端 carry 是 1，而 isolated B 的 carry 是 0。
3. **零块可以出现，不能偷偷缩短 prescribed width。** 原始块长度控制位移。全零块 isolated digits 和质量均为零，但其列数仍占位。块的最终系数为零时，它的 formal pair word 使用 prescribed width，不能自动解释成 ordinary component update。
4. **整体 ordinary pairing 的反射宽度须有真实宽度桥。** 例：单块 `W=(1,0)`，`L=2, gamma=0, K=0, E=1`，prescribed-width 独立表达式是 `1+x`，但实际整数 normalization 是 1，ordinary next pair 是 2。因此 `R exact iff K=0` 若解释为 ordinary pair word，须保留整体 canonical/实际宽度证据。质量相等不能发现这个错误：两种表达式质量都为 2。
5. **质量公式本身不依赖 local clocks 一致。** Reflection 不改变总系数质量。`M(E_j+rev(E_j))=2 M(E_j)`，故 local widths 不同不影响质量，但会影响逐系数式。
6. **零亏损 iff 无活跃 seam 需要非负性。** `K` 的每个系数是 actual carry minus reset carry，必须独立证明其非负。随后有限和为零等价于每一项为零，不能从整式质量相等直接假定逐系数式。
7. **“下一步不回文”只是一阶安全性。** 需要输入为实际普通整数的 canonical digits 所产生的 pair word，并使用现有 ordinary-step bridge。不能把其结论扩张为下一轮 seam 仍活跃、无限非回文或 196/Lychrel 见证。
8. **无系数界的 generic lemma 只承诺它写出的形式运算。** `PairResponse` 的 generic coefficient identities 没有 `q <= 18` 或 canonical 前提；对这类任意自然数系数，`nextWidth` 是定义的形式宽度，并不自动等于实际十进制位数。例如 `q(0)=100,L=1` 时 terminal carry 为 10，形式 `nextWidth=2`，但整数 100 的宽度为 3。`numeric_pair_response` 的 `Canonical` 和 `hrep` 前提则通过 `representation_next` 证明实际宽度，避免该问题。

## 2. 独立源代码检查项目

- 完整 coefficient response 是否逐系数覆盖 `i<L`、`i=L`、`i>L`，包括 `L=0`。
- `resetRaw` 与任意 boundary 分块的真实 isolated normalization 之间是否存在证明，而不只是命名。
- 初始 9-run theorem 的输入是否是真实块、真实输入 carry；避免把所需 transfer 或 defect equation 当作假设。
- mass identity 是否包含各 isolated terminal carries；pair mass 的乘二是否保留在实际 whole width 下。
- ordinary integer bridge 是否从 `Canonical n d L` 出发，并证明/调用实际输出宽度的有效定理。
- 检查导出定理的 hypotheses：不得把 polynomial identity、质量结论、实际宽度等目标的等价式直接作为假设。
- 全部新增 Lean source 不得出现 `sorry`、`admit`、`native_decide` 或新增 axiom。

## 3. 独立执行计划与完成状态

以下为 source freeze 时制定的执行计划，现已全部完成：

1. 对新增源文件和实际依赖源文件记录 SHA-256。
2. 使用独立临时 build 目录，从源文件按 import 依赖顺序重建本地依赖；不能依赖作者生成的新增 `.olean`。
3. 对每个新增导出 theorem 生成并执行 `#print axioms` 审计文件。
4. 保存执行命令、编译器版本、退出码、完整日志和 axiom 集合。
5. 允许的标准 axiom 必须逐一显报：`propext`、`Quot.sound`、`Classical.choice`。若出现其它 axiom，则报告阻断项。
6. 执行前后重新比较 source hashes；有改动则只对一致 hash 的版本声明结论。

完成状态：5 个本地依赖、7 个新增模块及 All 聚合均独立从源码重建；66 个公开 theorem 的 `#print axioms` 报告齐全。公理并集仅 `propext`、`Quot.sound`、`Classical.choice`。两个后续模块 `PairClosure` 和 `PartitionDefect` 已补齐 paired iff、全局 defect sum 与分块 run 之和以及 raw mass 与 isolated block mass 的对应，假设检查见 `REVIEW.md`。完整构建、hash 和公理证据见 `review107-clean-okwe457n/`；恢复复核见 `RESUME_VERIFICATION.json`。
