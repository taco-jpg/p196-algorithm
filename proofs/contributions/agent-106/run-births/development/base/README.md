# 全基数局部极值新生与实际 nooverflow 桥接

作者角色：Agent #106 / base_generalization。两份提交源为 `../../BaseBirths.lean` 和 `../../ActualBaseBirths.lean`。本目录保存开发证据；`.olean` 构建产物位于仓库外 scratch，不应提交。

## 精确范围

令 `b ≥ 2`、`0 ≤ x ≤ 2*b-2`，且 `a,c` 是两侧真实或待代入的携入 bit。定义

`localPair b x a c = (x+a)%b + (x+c)%b`。

完整分类是：

| 输出 | 输入 pair 系数 x | a | c | 局部机制 |
|---|---:|---:|---:|---|
| 0 | 0 | 0 | 0 | 原零保留 |
| 0 | b | 0 | 0 | 新生零 |
| 0 | b−1 | 1 | 1 | 新生零 |
| 2b−2 | b−1 | 0 | 0 | 新生最大值 |
| 2b−2 | b−2 | 1 | 1 | 新生最大值 |
| 2b−2 | 2b−2 | 1 | 1 | 原最大值保留 |

每种输出的三个分支互斥且穷尽。两侧携入不同不能产生任一极值。对于 `b≥3`，任一新生极值的来源 `x` 严格位于两个极值之间。对于 `b=2`，完整分类本身不变，但 `x=b` 就是最大值、`x=b−2` 就是零；因此二进制允许两类极值直接互换：`localPair 2 0 1 1 = 2`、`localPair 2 2 0 0 = 0`。这与已有 intrinsic 输出安全结果在二进制失效的边界是不同命题。

## 新增内容与已有结果的关系

已有 `base-reflection-formal` 分类讨论原系数/进位与全输出反射对称；已有 `base-intrinsic-formal` 分类讨论 high-neutral 相邻模式、reset/ordinary 携带缺陷及输出非回文安全。这里的新命题是一个输出镜像 pair 等于极小或极大值的逐点充要分类，没有重证这些全输出结果。

`BaseBirths.lean` 只导入 `Std`，共 7 条公开定理。其新生谓词是单步局部谓词，不是祖先、寿命或全轨道定理。没有重复 Agent 102 的极值最大段祖先/寿命工作。

`ActualBaseBirths.lean` 复用原有 `PhysicalWidth` 与 `ReverseAdd` 的语义，共 11 条公开定理。实际携入定义为前 k 列连续普通归一化的 terminal carry；不把任意独立携入冒充真实携带。主桥接 `actual_nooverflow_pair_at` 在计算出的最终 carry 为零时，证明 `pairs (actualDigits b xs)[k]` 正好等于上述局部式，镜像索引为 `xs.length−1−k`。

主定理 `canonical_reverse_add_extremes` 要求：

- `b ≥ 2`；
- 输入数字满足原有 `DigitBounds` 与 `PositiveLast`；
- 源系数投影确实等于 `ReverseAdd.pairs digits`；
- 计算出的普通 final carry 为零；
- 索引在源长度内。

其结论同时给出真实输出 digit 范围、正 leading digit、`n + reverse_b(n)` 数值，以及实际输出 pair 的两种极值完整 iff 分类。所有结论都明确限制于一次 nooverflow 步，未覆盖 overflow 时改变的镜像配对。

## 编译与公理

使用 Lean 4.19.0。`compile-02.log` 是冻结的 Std 模块完整编译及 7 条 `#print axioms` 输出；`actual-04.log` 是冻结实际模块完整编译及 11 条 `#print axioms` 输出。所有依赖仅为 Lean 标准 `propext`、`Classical.choice`、`Quot.sound` 中的子集；二进制具体例子不依赖公理。没有 `sorry`、`admit`、`native_decide` 或新增 axiom。

独立审查者 nooverflow_births 已从空目录重建冻结 `BaseBirths.lean`，通过语义与 kernel 审查；具体审查日志由该审查者另存。

冻结源 SHA256：

- BaseBirths.lean: `dcca96672161ac382020d476c6bf75d2b3b47456c76193cba55fdfcd6650af33`
- ActualBaseBirths.lean: `e9fd9ed2a8065d7b6327d0400f7d94eea1049ba3f5b24241dcec244600121a6d`

## 保留的开发历史

- `BaseBirths.compile-01.lean` / `compile-01.log`：第一次即成功；只有未使用辅助参数的 warning，冻结版本已重命名为 `_hb`。
- `actual-01.log`：第一轮实际数字索引桥接通过。
- `ActualBaseBirths.actual-02.lean` / `actual-02.log`：唯一失败源，尝试对依赖索引使用 `rw [hs]` 导致 motive 类型不合法。
- `actual-03.log`：改用 `simp only [hs]` 后核心实际 pair 桥接通过。
- `actual-04.log`：补充完整分类与 canonical 包装后通过。
- `dependency-logs/`：六个原有全基数模块的源码编译日志，均通过。

这些日志在产生之后从仓库根 development/base 迁至本目录，因此早期日志中的路径保留原始执行位置。

## 复现

`build_dependencies.py` 按准确源映射构建六个原有模块，不复制或修改它们。指定仓库外 scratch 目录，导出运行时需要的 `LD_PRELOAD`，并设置 `LEAN_BIN`。随后将该目录作为 `LEAN_PATH` 依次编译 `BaseBirths.lean`、`ActualBaseBirths.lean`。例子：

```sh
export LEAN_BIN=/workspace/scratch/50e90e07524e/runtime/lean-4.19.0-linux/bin/lean
export LD_PRELOAD=/workspace/scratch/50e90e07524e/runtime/readlink_self.so
python proofs/contributions/agent-106/run-births/development/base/build_dependencies.py /workspace/scratch/50e90e07524e/base106-rebuild
export LEAN_PATH=/workspace/scratch/50e90e07524e/base106-rebuild
"$LEAN_BIN" -o "$LEAN_PATH/BaseBirths.olean" proofs/contributions/agent-106/run-births/BaseBirths.lean
"$LEAN_BIN" -o "$LEAN_PATH/ActualBaseBirths.olean" proofs/contributions/agent-106/run-births/ActualBaseBirths.lean
```
