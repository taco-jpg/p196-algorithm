# 原整数语义桥的独立准备

Agent #105 / lean_runtime 将六个现有源文件按精确 SHA-256 原样复制到全新隔离目录，并以原模块文件名重新编译。六个模块均退出 0；未修改源文件、重造定义或增加数学命题。完整来源与 Git blob 见 `source-pins.json`。

构建顺序：`LychrelDigitSums`、`TemplateStep`、`PeriodObstructions`、`ActualWordBridge`、`Compat`、`IntegerEndpoints`。全部使用官方 Lean 4.19.0 / `6caaee842e94` 和其自带 `Std`，后续依赖只从本次构建目录导入。

从本次生成的 `IntegerEndpoints.olean` 另行导入审计 `Compat` 的全部 16 个定理与 `IntegerEndpoints` 的全部 3 个定理，共 19 个接口；逐项 `#check` 和 `#print axioms`，退出 0。完整实际输出在 `logs/IntegerBridgeAudit.log`，公理仅为 Lean 标准集合中的依赖。

## 后续实际动力学连接点

- `Agent109.Compat.pairWord_step`：原 `Lychrel196.step` 的 pair word 等于原 `Agent8.stepWord`。
- `Agent109.Compat.pairWord_orbit`：对任意 `n,k`，`Agent109.pairWord (Lychrel196.orbit n k) = Agent8.orbit (Agent109.pairWord n) k`。
- `Agent109.Endpoints.pairWord_canonical`：显式前提 `n ≠ 0` 推出原 `Agent8.CanonicalPair (Agent109.pairWord n)`。
- `Agent109.Compat.isLychrel_iff`：把原整数轨道的无限安全命题与原列表规范化输出的非回文命题精确对应；这是等价关系，未提供任何满足条件的见证。

因此给定实际正整数的表示 `pairWord n = Q k`，可直接重写并接入新列表时间界。pair-word 返回不要求选择的两个整数 realization 本身相等；两个不同整数可能有相同 pair word。`CanonicalPair` 也不可反向当作无条件整数可实现性。

## 本次产物位置

可执行构建产物仍在 `/tmp/p196-agent105-toolchain/integer-bridge/source`；本目录发布全部日志、原依赖 pin、19 项导出审计源码和收据。后续实际步闭包完成前，没有新增整数包装证明。
