# Agent 108：有限二元权重与实数增长代数

本目录属于已认领任务 `agent108-buffered-window-weights-b31b8818`。

正式源码为 `proofs/Agent108WindowObstruction.lean`，共有 10 个导出定理。
其依赖是 `Agent108WindowDefs.lean`、Lean 4.19.0（`6caaee842e94`）和
Mathlib `c44e0c8ee63ca166450922a373c7409c5d26b00b`。Mathlib 使用官方编译缓存，
没有声称从源码重建整个 Mathlib。

## 已完成的结论

- `binaryWeight` 对每个 false 位赋权 1，对每个 true 位赋权 beta，再相乘。
- `choices r` 中的每个列表长度都是 r，且没有重复列表。
- 遍历 `choices r` 的精确权重总和等于 `(1 + beta)^r`。
- 逐项权重公式 `C * targetWeight * binaryWeight beta es` 可传递为有限总和公式。
- 当 C 和 beta 是严格正实数时，`C * (1 + beta)^r` 随自然数 r 无界。
- 若一个任意函数 incoming 支配该精确几何子族总量，且每个 targetWeight 为正，
  则不存在对所有 r 成立的有限实常数 K，使 `incoming r <= K * targetWeight r`。

最后一项是显式带假设的代数接口。将它应用于实际反转加法的 incoming 算子，
仍需独立证明实际子族权重公式、子族包含关系和正权重。这个文件不证明任何
实际算术转移，也不证明无限不回文性或 196 结论。

## 验证证据

`attempts/001/` 保留首次编译的原始源码和日志：末尾匿名 section 没有先关闭，
因此编译失败。这个尝试没有被标成通过。

`attempts/002/` 保留修复后的源码、每个编译命令、退出码、完整输出和公理审计。
Defs、Obstruction 和 AlgebraAxioms 三个模块全部退出 0；10 个定理全部得到
恰好一次公理报告。传递依赖只包含 `propext`、`Classical.choice`、`Quot.sound`
的子集，没有 `sorryAx`、`Lean.ofReduceBool` 或新增公理。

`latest-verification.json` 是此次通过记录；每次尝试的独立记录保持不变。
编译 `.olean` 放在本次临时构建目录，不属于应发布的数学源码或证据。
