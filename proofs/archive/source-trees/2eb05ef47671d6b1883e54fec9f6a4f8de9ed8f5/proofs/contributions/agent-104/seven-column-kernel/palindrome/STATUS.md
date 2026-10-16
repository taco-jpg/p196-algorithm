# PalindromeBridge 验证记录

本目录属于 agent #104 的最后一步桥接子任务。接受的源码为上级目录的
`PalindromeBridge.lean`，命名空间为 `SevenColumnKernel.PalindromeBridge`。

## 已证明

- `canonical_unique`：同一普通正整数的 canonical 表示等宽且逐位相同。
- `no_overflow_of_target_leading_gt_one`：目标首位大于 1 时，最后一步没有溢出；此处尚不需要回文假设。
- `canonical_last_step`：加入目标回文假设后，源和目标等宽，全部实际进位为 0，源的完整对称列和逐位等于目标的完整数位，且每项不超过 9。
- `numeric_last_step`：上述结论适用于任意正整数前驱，不需调用方先提供源的数位表示。
- `predecessor_of_739_palindrome`：739 回文的正整数前驱列和从低位开始为 7、3、9，并保留完整数位等式与无进位结论。
- `no_196_target_of_ancestry_bound`：若某个回文目标族的所有正整数祖先深度统一不超过 `B ≤ 100`，则普通 196 轨道在任意时刻均不进入该族。
- `no_196_739_palindrome_of_ancestry_bound39`：把上一项专门化到 739 回文和上界 39。

最后两项是**显式条件定理**；39 步统一祖先界是参数，而不是公理或本文件已证明的结论。本文件不证明完整 196 猜想。

## 编译与公理审计

使用 Lean 4.19.0；直接导入仓库现有 `LychrelDigitSums.lean`。

```bash
mkdir -p /workspace/scratch/7649db1e242c/build104-palindrome
/workspace/scratch/7649db1e242c/toolchain/lean \
  -o /workspace/scratch/7649db1e242c/build104-palindrome/LychrelDigitSums.olean \
  proofs/research/continuation/LychrelDigitSums.lean
LEAN_PATH=/workspace/scratch/7649db1e242c/build104-palindrome \
  /workspace/scratch/7649db1e242c/toolchain/lean \
  -o /workspace/scratch/7649db1e242c/build104-palindrome/PalindromeBridge.olean \
  proofs/contributions/agent-104/seven-column-kernel/PalindromeBridge.lean
```

核心构建退出码 0，日志为 `base-build.log`。接受版本构建退出码 0，日志为
`attempt_002.log`。七项导出定理全部已 `#print axioms`，只出现
`propext`、`Classical.choice`、`Quot.sound`，未出现 `sorryAx` 或额外公理。
接受源码无 `sorry`、`admit`、`axiom`、`native_decide`。

`attempt_001.lean` / `attempt_001.log` 保留首次失败：`subst W` 优先使用另一个宽度等式，导致后续固定宽度注入性参数不匹配。接受版本先清除两个中间长度等式，再沿 `L = W` 替换。失败草稿不是接受证明链。

SHA-256：

```text
LychrelDigitSums.lean
ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57

PalindromeBridge.lean
6c1de8cf02ec9381e80388e6b4915db6cfa4d1189d3e47c273400f0d37948093
```
