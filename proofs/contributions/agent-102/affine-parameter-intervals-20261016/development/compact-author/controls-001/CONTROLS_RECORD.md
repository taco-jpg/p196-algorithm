# Compact 具体规模控制

执行者为 `/root/word_intervals`，是 Compact 的作者。本记录属于作者追加控制，不是独立审查，也不证明一般复杂度界。

母代理明确要求对已经发现的两类空区间输入进行具体检查。本轮只新增证据目录内的 `CompactControls.lean`，冻结的工作区数学源码完全未改。

## 三项实际结果

以下三条闭合等式都由 `by decide` 证明：

1. `fastComplement (List.replicate 128 Interval.empty) = univ`。
2. `fastComplement (List.replicate 128 ⟨5, some 3⟩) = univ`。
3. 输入有效区间 `[1,3)`、`[4,6)`，同时混入 128 个零宽空区间和 128 个倒置空区间；实际输出列表精确等于 `[0,1)`、`[3,4)`、`[6,∞)` 三项，顺序也与控制等式一致。

每条声明均执行 literal `#print axioms`，全部输出“不依赖任何公理”。没有使用原生计算决策或未完成证明。

## 实际执行

只运行一次增量命令，使用官方 Lean 4.19 的 `--trust=0 -j1 -DElab.async=false`，返回码为 0。此次调用实测约 0.536 秒；该单次记录不是性能基准或一般复杂度承诺。

依赖复用本作者在 `compact/attempt-001` 中亲自完成的 fresh trust=0 构建产物，执行前重新核对四个依赖的当前源、保存源和 SHA256 一致，并记录实际 `.olean` 的 SHA256。因此本轮应记作“一次增量控制检查”，不能另算一次全闭包 fresh 构建。

控制源 SHA256：`10efd5955b00ace42b8ebacb82c26a3fee14b961d781f0b6b103795e229f8de5`。

完整实际命令、`LEAN_PATH`、依赖记录、返回码和耗时见 `manifest.json`；完整输出见 `CompactControls.log`；复现脚本为 `run_controls.py`。

本目录没有 `.olean`；控制输出另存在同级 `controls-001-empty-build` 中。原始 `SHA256SUMS` 保持原样，加入本说明后的交付校验表单独保存。
