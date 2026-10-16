# 对 Agent102AffineAllParameters 的独立源码审查

审查者：Agent #102 的真实子代理 `/root/lean_runtime`。
被审模块作者为母代理 `/root`；我没有参与该文件的实现或修改。
我的 Controls 是独立消费该接口的作者控制，不将其自测声称为独立审稿。

审查冻结文件：`Agent102AffineAllParameters.lean`，5419 字节，SHA256
`7cd7b3682bcb6f072853a93cbadaaf43e5c2b59767add0a51f1f8938be183e0c`。
我已完整阅读该源文件，以及它所依赖的任意参数压缩比较器声明和实现。
此前已完整审查并核查此次保持不变的 affine tail 组合闭包。

## 结论

该模块实现了对静态仿射段词族、所有自然数参数的相等与回文全称/存在判定。
十二条规格的正反方向齐备，有限前缀与稳定尾部的分界处理正确。
没有发现将“不是全部相等”误当作“全部不等”的量词混淆。
在所审冻结源码和明确语义范围内没有待修复问题。

这项结论由完整源码审查、十模块清洁 `--trust=0` 重建、48 条新定理 literal 公理检查、
297 条 module-origin theorem 常量审计及十个可执行入口的项目依赖检查共同支持。
原始程序和日志均在 `attempts/attempt-002`。

## 全称相等与存在相等

设 `K = equalityCutoff A B`。

`allEqual` 是 `fastEqualOnTail` 与范围 `0,…,K-1` 上 `equalAt` 的 conjunction。
其证明通过 `fastEqualOnTail_spec` 将前者转换为所有 `k≥K` 的词相等，
通过 `equalAt_eq_true_iff` 将有限前缀转换为真实词相等。
随后按 `K≤k` 分情况覆盖全部自然数；反方向直接限制一个全称假设。
由于尾部包含 `K` 而 range 不含 `K`，分界处没有遗漏。

`someEqual` 是同一 tail Bool 与有限前缀 `any` 的 disjunction。
tail 为真时取明确见证 `k=K`；prefix 为真时直接使用所枚举见证。
反方向对给定相等见证按同一分界分类：tail 中的见证由
`fastEqualOnTail_iff_wordAt` 转回 tail Bool；prefix 中的见证进入 range。
这一步使用了已证明的稳定尾部等价，因而不要求把所有自然数枚举到尽头。
`K=0` 时前缀为空，而 `k=0` 仍由尾部覆盖。

## 否定量词

定义 `allUnequal = !someEqual`，其 true 规格为每个参数都不相等。
证明只需把任一相等见证转成 `someEqual=true` 并与否定矛盾，反方向使用 Bool 的穷尽分类。

定义 `someUnequal = !allEqual`，其 true 规格为存在不等参数。
从非全称相等取得反例的方向显式使用 `classical`；该经典推理出现在证明层。
它不是一个返回反例下标的计算函数，也没有声称构造最小反例。
反方向由实际反例否定 `allEqual_spec` 的全称结论。

`allEqual_false_iff` 与 `someEqual_false_iff` 由上述规格和 Bool 否定规则直接得到。
因此 false 分支也分别对应存在反例和全部不等，而非仅单向的 soundness。

## 回文接口

四个回文 Bool 以 `A` 和 `A.reverse` 调用对应相等 Bool。
六条回文规格（四个 true 规格与两个 false iff）统一经 `wordAt_reverse` 改写。
反转段序对每个复制块也给出正确词反转，因而保留零长度、相邻同数字段和任意自然数数字。
没有规范化段结构、删除零数字或隐含非空前提。

## 可执行行为与边界

新模块的计算定义只组合 `fastEqualOnTail`、`equalityCutoff`、`List.range`、
`List.all`、`List.any` 和任意参数的 `equalAt`。
`equalAt` 实际评价各段的整数仿射长度并转为自然数，随后按段宽与区间交叠比较数字；
它不对负斜率或小参数使用稳定尾部的正部替换。

执行依赖审计读取编译后 Lean environment 中的真实常量，从十个 Bool 入口递归遍历
项目定义的类型与值，并在标准库边界记录 `List.range`、`List.all`、`List.any`。
所有入口均未触达 `word`、`wordAt`、`List.replicate`、`equalOnTail` 或 `palindromicOnTail`。
标准库函数的任意实现细节没有被本项目依赖审计重新形式化。

tail 放在 Bool conjunction/disjunction 的左侧。
官方 Lean 4.19.0 的 `Init/Prelude.lean` 将 `Bool.and`、`Bool.or` 标为
`@[macro_inline]` 并提供短路行为。即使某些分支可提前返回，一旦需要有限前缀，
算法仍使用 `List.range K`，因此截距诱导的巨大 K 仍可能代价很高。
没有得到关于系数位数的多项式复杂度定理，也没有使用巨大 cutoff 的全前缀测试。

模块量化的是模板的静态自然数参数 `k`，不是十进制 reverse-add 的迭代次数。
没有证明原仓库某个具体输入达到回文、达到某个最大延迟，或无回文轨道。

## 独立重建与公理审计

实际运行官方 Lean 4.19.0，commit `6caaee842e94`，使用
`--trust=0 -j1 -DElab.async=false`，`LEAN_PATH=.`。
所有十个项目源从固定快照复制到全新目录，未复用项目 `.olean`。
十三个编译子进程均以 0 退出；Std 来自所记录的官方发行。

literal 新定理清单为 RunDecision 的 4 条、AllParameters 的 12 条、Controls 的 32 条。
module-origin 审计另外覆盖十个源模块生成的全部 297 条 theorem 常量，
公理并集仅为 `propext`、`Classical.choice`、`Quot.sound`。
七个由编译器生成的 unsafe 实现占位常量在日志明确另列；没有将它们算作安全新公理，
且它们不出现在任何已审 theorem 的依赖公理集合中。

没有 `sorry`、`admit`、`native_decide` 或自定义证明公理进入成功源。
首版的真实 Controls 递归限制失败，以及 elaboration 恢复产生的 `sorryAx` 日志，
在独立失败目录完整保存。该失败不影响重新编译成功且不含 `sorryAx` 的冻结版本。
