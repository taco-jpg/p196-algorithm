# RebaseAlgebra：作者增量检查

作者：Agent #100 / session20261016T2052Z 的真实子代理 `runtime_setup`。
claim：`e1bc61f552413f4a1ed6cef86c88265d39fd896d`。
本目录是源作者自检，**不是独立重建或独立验收**。父代理负责所有 Git 写入；本子代理只写本数学文件和本 development 子目录。

## 冻结源

- 正式路径：`proofs/Agent100GroupIIRebaseAlgebra.lean`
- SHA256：`d62f8769d9d2ee0ecf2ec3f0b0dffcd6c19cd5383692207e0e044b7649df02ff`
- Git blob：`d5185542692625baa8fc0dc171b58e86b53f6260`
- 成功快照：`attempt02.lean` 与 `attempt02/Agent100GroupIIRebaseAlgebra.lean`，均与正式源逐字相同。
- 公开项：3 个定义、5 个定理。完整原始声明见 `inventory.json`。

## 确切范围

namespace 为 `Agent100.GroupIIRebase`。`rebaseDelta` 在 `r+1,r+5` 为 `+1`，在 `r+2,r+4` 为 `-1`，其余为零；`rebasedInt` 为既有 `finiteNextComponent` 的 Int cast 加此修正；`rebasedComponent` 仅定义为其 `Int.toNat`。

五个定理分别证明：具体修正加其 `previous` 恰为原 `overflowDefect`；signed component 相对实际轨道有限零延拓的全索引等式；具体 signed 相邻和的代数展开；符号 middle 的第二输出在全宽 `i<2*r+8` 上等于该 signed 相邻和；实际 wholeOrbit time2 的相同全宽结论。左边界由原 `RawSymmetryObstruction.previous` 的零值处理，右端包含实际新增末列。`r=1` 包含在完整参数域中。

本模块没有证明或假设 `rebasedInt` 非负，没有将 `Int.toNat` 自动视为保值，没有证明自然 component 的 `Admissible`、安全性或普通整数实现。后续 Profiles 与父包装层提供相应独立义务。这里仅复用已有 defect 与实际轨道接口；没有重造一般 `(1+x)` 逆像定理，也未使用另一 Agent100 的 WIP 前两列接口。

## 真实执行与失败保留

`attempt01` 实际退出 1：左端 if 的化简不足、误用不存在的 `Nat.cast_add` 名称，以及试图在函数参数下直接改写逐点等式。源、完整日志、命令和元数据均保留；该失败产生的 `sorryAx` 报告明确 **排除于接受证据**。

`attempt02` 使用官方 Lean 4.19.0，`--trust=0 -j1 -DElab.async=false`，实际退出 0。五个定理均有字面 `#print axioms`：`rebasedInt_actual_component` 仅依赖 `propext, Quot.sound`，其余四个依赖 `propext, Classical.choice, Quot.sound`。日志仅有 `rebase_delta_overlap` 的未使用 `hr` 警告；该特殊代数恒等式实际上不需要这个较强前提，公开接口仍保留认领的 `r≥1`。

`definition-audit.lean` 单独导入冻结模块，实际退出 0，三个共享定义的字面 axiom 报告均为空。

成功主日志 SHA256：`c0f96c167f1d60f850184fc08c717d0e2ab50410b168070fa57098f6116d0086`。
定义审计日志 SHA256：`ce0021b03d5c8110c194d75d70e26c17332f5484f4a8613acbd58752b40139d5`。

旧依赖使用父指定、已由另一专员独立重建的 18 模块 olean 目录。本轮没有重跑旧闭包；`inventory.json` 固定了所用每个依赖源与 olean 的 SHA256。具体 cwd、LEAN_PATH 和 argv 保存在每次 JSON 记录中，避免把作者增量检查混称为全闭包 fresh build。
