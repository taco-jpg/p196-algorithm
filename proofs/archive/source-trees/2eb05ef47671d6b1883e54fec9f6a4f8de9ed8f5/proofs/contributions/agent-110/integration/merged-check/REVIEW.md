# 合并树集成检查：PASS

签署：`/root/runtime_audit`，Agent 110 的独立基础设施与审查执行者。完成时间：`2026-10-15T16:40:19.465121+00:00`。

这是对既有独立审查闭包的源码比对和根模块重新编译，**不是一次新的完整空目录闭包重建**。本次新输出目录为 `/workspace/scratch/63e10b24caf2/integration-root-check`；明确只读复用 20 个依赖 `.olean`，重新编译 3 个根模块。未写入依赖目录，未修改数学源码，未执行 Git 写入或远端操作。

## 冻结对象与检查结果

- 目标合并提交：`b337ce1e3c3058468bc1562bf30e536f685960dd`，树：`89ad2eb97815cd721df7d82316e396c0931d6ca7`；确认父提交包含 main `2c2551165c13d23b11d44122fc7a504d51053e59`。
- 运行开始与结束观察到的 HEAD 均为 `4ceb839b4bd24b1d6aeeef3cfa091bf6bf6034e2`。允许后续文档与审查证据提交改变 HEAD；数学源码仍逐字节绑定上述合并提交。
- 19 个 certificate 模块和 4 个 Radix 模块的当前工作区源码，全部逐字节等于合并提交的 Git 对象，全部 SHA256 与独立审查记录一致。
- 19 个 certificate 源码另外逐字节等于已获取的远端提交 `eb4817f0973cbbe2a059af33d5dc53877a5275b7`；4 个 Radix 源码另外逐字节等于已获取的远端提交 `1cdc55c89b376faa270d1dffaf21e21b6eedeb4b`。逐文件 SHA256、Git blob 和路径见 `source-hashes.tsv` 及 `result.json`。
- `CertificateChecked`、`All`、`RadixExterior` 从这些实际合并源码重新编译，全部 exit 0；实际 `lean --deps` 输出确认根模块和直接导入指向本次输出或指定独立审查目录。
- 显式重做 Checked 的 3 个定理和 Radix 的全部 15 个定理的 `#print axioms`，18/18 通过；公理集合分别与先前审查一致，联合仅为 `propext`、`Classical.choice`、`Quot.sound`。
- 结束后再次核对全部 23 个工作区源文件、全部 23 个原审查对象以及两份审查收据：哈希均未变化。原审查的 3 个根 `.olean` 仅用于校验历史对象，不用于本次根编译。

## 独立完整闭包审查依据

1. certificate 19 模块：[`../../review-checked/rebuild-d611d7f/manifest.json`](../../review-checked/rebuild-d611d7f/manifest.json)，SHA256 `1a03fa46d6ab20224be224ef50bd7664af87e616a2643c963f2078c1add98906`。该收据为 PASS，`objects_reused=false`；对象目录 `/workspace/scratch/63e10b24caf2/reviewer-build/checked-d611d7f`。本次复用其中 17 个依赖对象。
2. Radix 4 模块：[`../../review-radix/verification.json`](../../review-radix/verification.json)，SHA256 `81851617ff0edcff9204df273cd97ca4714fc6c5ebe89382ae4a6c5927282b1f`。该收据为 PASS，`project_object_reuse=false`；对象目录 `/workspace/scratch/63e10b24caf2/radix-review-build`。本次复用其中 3 个依赖对象。

完整闭包的声明审计由这两份独立重建收据支撑，本次没有把 18 个端点检查冒充完整闭包重新审计。已审查源码和对象哈希一致，18 个端点的传递公理结果也一致。

## 实际声明范围

重新读取了合并后的 `CertificateChecked.lean` 与 `RadixExterior.lean`；`EndpointTypes.lean` 的实际输出保存在 `logs/EndpointTypes.log`。

- `period_at_least_four` 的前提只有 `check cert = true`，结论 `4 ≤ cert.P`。
- `six_phase_constraints` 仍要求 `check cert = true` 和初始 `SixPhase`；结论含 `O = 2(G+H)`、非负及整除预算、`2O ≤ P ≤ 4O`、`P % 6 = 0`、`42 ≤ P`。原始 admissibility 经 Agent 112 的冻结源码推导，没有增加循环 canonical 假设。
- `saturated_period_constraints` 另外**显式要求** `2 * totalGam cert = (cert.P : Int)`，再推出 `P % 72 = 0` 和 `72 ≤ P`；没有声称 check 单独强制饱和。
- Radix 量仍为 `Z = 9 * value10 B - c * (10^length(B)-1)`，观察值为 `(phase, Z)`。两个不可能性定理都限定为对所有 canonical 且实际 after-overflow 状态成立的观察值更新/单调性假设；其结论否定这些普遍假设。
- `witness_not_state_return` 明确给出 `endpoint ≠ source`；观察值返回不等于状态周期。本次结果不提供一个通过 check 的具体 certificate，也不证明 196 的全局结论。

## 执行环境与保留的失败

实际版本：`Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)`。执行官方 4.19.0 编译器，经既有 `runtime-audit/lean` 启动器及已记录的窄 `/proc/self/exe` 路径兼容适配器启动；编译器、启动器、适配器 SHA256 均记于 `result.json`。环境显式清除继承的 Lean 路径与动态加载配置，再设置记录中的 `LEAN_PATH`。

- `attempt-01-preflight/`：HEAD 被文档/证据提交推进，旧的严格 HEAD 等式前置断言停止；**没有启动编译器，不是 Lean 失败**。保留原驱动和原因记录。
- `attempt-02-unsupported-display-option/`：三个数学根模块和 18 端点公理检查已通过；自写签名查询脚本使用了 Lean 4.19 不支持的 `pp.width` 显示选项，因此签名查询 exit 1。保留完整驱动、输出、失败结果；只删除该显示选项后，新建空根输出目录并重做本次所有根编译与审计，全部通过。

最终执行驱动：`check.py`。实际命令、退出码、日志及哈希：`commands.txt`、`logs/`、`result.json`。驱动有意要求新输出目录与 `logs/` 不存在；重现时应使用新的检查副本与空输出路径，不能覆盖现有证据或把已有根对象误当新编译。

最终 `result.json` SHA256：`268959d1baddfc985fec42ba480216cdbc3b62dcbb59025aaad9cf8f0a81800e`。
