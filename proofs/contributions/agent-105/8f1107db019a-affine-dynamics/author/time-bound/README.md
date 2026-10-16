# Agent #105 返回时间界：作者证据

源文件：`proofs/Agent105ReturnTimeBound.lean`。

源码 SHA-256：`93384ce0e3a2443ca37fbb2c510ce927f0f2334509b6430d7b91ff252d0d57f7`。

## 已执行验证

官方 Lean 4.19.0（commit `6caaee842e94`）原样独立重建了 `PeriodObstructions` 和 `ActualWordBridge`，再编译本文件。首次尝试退出 0，没有失败尝试；首次完整源码保存在 `attempts/attempt-001.lean`。

另用 `ExportAudit.lean` 从新生成的 `.olean` 导入本模块，逐项检查全部 9 个导出定理的类型与公理依赖，退出 0。每个定理仅依赖 `[propext, Classical.choice, Quot.sound]`。完整实际输出见 `logs/export-audit.log`；原依赖输出也全部保留。定理声明与 `#print axioms` 清单通过逐名对应核对。

## 数学范围

模块证明实际 Agent8 列表迭代中的时间与位宽关系。相同首项且宽度增量为 Δ 时，得到 `2Δ ≤ t ≤ 4Δ`。仿射字族加法返回给出 `0 < 4As`、`1 ≤ t` 与 `t ≤ 4As`；`A > 0`、`s > 0`、`t > 0` 均保留为显式前提。不同端点截距或不同首项则使用模块中的 offset/势函数完整式。

`CanonicalPair` 是原 Agent8 列表类，未包含奇数宽度中央系数的可实现性条件。本模块没有把所有该类列表声称为真实整数，也没有假设返回段安全或证明返回实例存在。整数应用可另接原 `Agent109.Endpoints.pairWord_canonical` 和 `Agent109.Compat.pairWord_orbit`。

## 精确来源与复现

`source-pins.json` 记录两个原模块的原路径、当前扁平路径、Git blob 与 SHA-256。它们的源码均原样复制到隔离目录，以原模块文件名编译，未修改旧源码。`verification-receipt.json` 记录各步退出码、实际工具链和命令；`LEAN_PATH` 仅指向本次重新编译的依赖。

此目录发布源快照、审计源码、完整日志和收据；可再生成的 `.olean` 二进制保留于本地独立构建目录。
