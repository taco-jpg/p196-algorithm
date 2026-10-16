# TailSelection 独立复核

复核者：Agent #105 / lean_runtime。原作者：Agent #105 / ownership_audit。

**结果：接受，未发现需要修复的问题。** 未修改原源码。

精确源：`proofs/Agent105TailSelection.lean`，SHA-256 `6357e5bc0cb38368949f376a7e6b907dfac87ec3c93ab7b8d2114e3f75e007a6`。

## 核心检查

在只包含本次源码副本的全新隔离构建目录中，以官方 Lean 4.19.0 / `6caaee842e94` 编译源码，退出 0。随后从本次 `.olean` 单独导入模块，对全部 **2 个定义和 18 个定理** 执行 `#check` 与 `#print axioms`，退出 0。未复用作者的 `.olean`。所有依赖均在 `propext`、`Classical.choice`、`Quot.sound` 的标准集合内；部分声明没有任何公理依赖。

实际完整输出见 `source-compile.log`、`export-audit.log` 和 `lean-version.log`。`source-pin.json` 记录逐项声明清单；`verification-receipt.json` 记录每项公理依赖。

## 数学与范围复核

1. `Eventually P` 表示一个完整自然数尾部，不表示无限散点；`TailStable P` 把整个尾部的真假固定为阈值处的真假。二者通过经典二分得到最终恒真或最终恒假的等价式，逻辑使用明确。
2. 有限覆盖选择器对候选列表归纳。首候选最终恒真时可立即选择；最终恒假时先把覆盖与该否定合并到共同阈值，再严格移除首候选。归纳不会把散点命中误作统一尾部。
3. 空列表的覆盖前提不可能成立：在覆盖阈值本身取一个自然数即可矛盾。列表重复项不影响证明，不需要偷偷加入无重复假设。
4. `List.range B` 经 `j + 1` 精确对应 `1 ≤ t ≤ B`。由正时间前提合法使用 `t - 1 + 1 = t`，没有把零时间纳入候选。`B = 0` 同样使覆盖前提不可能成立。
5. 安全组合检查的是每个 `1 ≤ i ≤ t` 的正中间输出，包括返回终点，不包括时间零；与目标文字中“positive ordinary output”的范围一致。共同尾部阈值允许增大，有限个稳定谓词通过最大阈值合并。
6. `hStable` 是必要的实质前提：例如偶数/奇数两个参数集合能覆盖所有参数，却没有一个集合包含整个尾部。模块并未只凭有限候选数省去稳定性。
7. 最终 `uniform_safe_return_time` 仍显式需要固定时间上界、返回谓词稳定性、安全谓词稳定性及尾部安全覆盖。模块没有给实际反向相加系统偷偷提供其中任何一个前提，也没有独立证明数学研究终目标。

## 复现命令

令 `lean` 指向官方 Lean 4.19.0，将原源复制为 `Agent105TailSelection.lean`，并将本目录的 `IndependentExportAudit.lean` 放在同一全新目录，运行：

```bash
lean -o Agent105TailSelection.olean Agent105TailSelection.lean
LEAN_PATH=. lean IndependentExportAudit.lean
```

本平台实际执行使用正规的 `exec_command sandbox_permissions=require_escalated` 批准路径。
