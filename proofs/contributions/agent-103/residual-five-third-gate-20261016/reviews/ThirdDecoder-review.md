# ResidualFiveThirdDecoder 非作者源码与作者日志审阅

审阅者：Agent #103 / source_audit（实际子代理 `/root/source_audit`）。作者：Agent #103 / scope_scan。日期：2026-10-16。

**结论：PASS，未发现需要修改的问题。** 本结论只覆盖下述冻结源码的语义与已存在的作者编译记录；本次没有运行 Lean，也不声称已经代替 runtime 的完整全新构建。审阅者自己编写的 `ResidualFiveThirdWidth` 明确排除于非作者审核范围，它在这里仅作为已固定的依赖接口使用。没有自我批准或 GitHub 审批动作。

## 精确源码与实际作者证据

- 模块：`ResidualFiveThirdDecoder`。
- 冻结 SHA-256：`bf170d875b2539ff04bbabfacf11af0206026366752a88376d6fd0a0606fb84e`。
- 工作源与作者 `attempt-003` 的完整源逐字一致，副本见 `source-snapshot/ResidualFiveThirdDecoder.lean`。
- 实际作者命令使用官方 Lean 4.19.0，参数为 `--trust=0 -j1 -DElab.async=false`，退出码 `0`。
- 五个源码定理均有实际 `#print axioms` 输出；全部只含 `propext`、`Classical.choice`、`Quot.sound` 的子集，成功日志没有 warning、error 或 `sorryAx`。
- 原始 `argv.json`、`manifest.json`、stdout、stderr、完整日志和源码均已保存于 `author-evidence/decoder-attempt-003/`；其源、对象和日志哈希均已对照作者 manifest 重新核验。没有复制旧对象来冒称新构建。

机器记录见 `ThirdDecoder-review.json`，其中保存全部五个定理的实际公理输出、精确作者参数与依赖路径，以及每个保存文件的原始路径、字节数和 SHA-256。

## 语义审阅

### 外侧两次扫描与根的正性检查

`scan_forced_boundary` 给的是原 `scan` 的完整 `Option (List Nat)` 等式。它将最低位在前的外侧数位 `(1,1)`、次外侧 `(6,6)` 精确解为系数 `1`、`6`，两次解码后的低、高边界进位仍均为 `0`。剩余扫描宽度为 `2*r`，数位函数为 `fun i => e (i+2)`，返回的系数词仅被两层原 `wrapDigits` 包回。

两个固定局部解码值通过原函数上的 kernel `decide` 验证。原局部实现的候选即使含自然数截断减法，也必须通过 `ValidEdge` 的两条完整十进制列等式；这里没有把截减候选本身当作有效解。

`decodeNumerical_forced_boundary` 仍使用原 `decodeNumerical` 与 `decodeAtWidth`。宽度 `2*r+4` 始终为正，末进位请求为 `0`，返回词最外系数为 `1`，因而原根正性检查自动满足。这没有在中央词上额外施加根正性条件。

### r = 0 与目标 canonical 契约

`r=0` 时剩余扫描为原 `scan 0 _ 0 0 = some []`，正确接受空中央词。不会因为中央宽度为零而误调用会拒绝它的根 `decodeAtWidth`。外侧四个数位占据位置 `0,1,2,3`，没有重叠或越界。

最前面的两个纯函数等式不需要数位有界假设。真正使用数值存在性语义时，`fixed_width_predecessor_iff_scan` 明确保留 `Canonical n e (2*r+4)`，由其提供原数值解码器所需的合法十进制数位、非零最高位和实际数值等式。没有把任意函数当作普通整数的 canonical 表示。

### 实际正整数存在性与所有源宽度

`fixed_width_predecessor_iff_scan` 直接调用原 `Agent105NumericDecoder9df76b.decodeNumerical_isSome_iff`。已读取其原证明及 `realize_payload`：反向确实利用原 `valid_word_realizable` 构造正整数及 canonical 数位，并通过原 `step_eq_word_value` 证明 `step z = n`；存在性不是未消除的证书假设，也不是只存在一个符号系数词。

完整 `fiber_predecessor_iff` 的正向从任意 `z>0`、`step z=n` 开始，使用原 `canonical_exists` 取得任意实际宽度，再调用已固定的 Width 接口强制该宽度为 `2*r+4`。因此公开定理没有额外的源宽度前提。反向则由四个外数位等式及中央接受条件直接得到真实的同宽正整数前像；它没有假定该前像已经存在。

调用者宽度版本 `fiber_predecessor_iff_of_width` 显式保留 `W=2*r+4`，以自然数算术核对 `W-1=2*r+3` 与 `W-2=2*r+2`，没有忽略自然数减法的下界。

## 已复核的原依赖与范围

审阅已读取原 `Agent105DecoderLocal9df76b`、`Agent105DecoderScan9df76b`、`Agent105DecoderTarget9df76b`、`Agent105NumericDecoder9df76b` 的实际相关源码。六个新增原依赖的完整原文、开发编译日志和 `development.json` 都保存在 `dependency-evidence/`。

该开发环境记录准确标为复用 17 个已核验对象、实际编译 6 个新增原模块的开发环境；它明确不是全新闭包构建。此前核验的 Research 基础体与 import-only forwarding 兼容关系仍由该独立记录保留，没有把两个完整基础体一起加载。

公开 iff 仍要求中央扫描实际接受，不能把四个外数位条件单独升级为存在性，不能据此宣称候选数为 `10^r`。本模块没有统一祖先深度上界、196 全程不回文或整数轨道可达性的结论。

## 真实失败记录与隔离

`attempt-001` 的实际退出码为 `1`，错误为 `simp made no progress`；该失败日志中的两个后续公理输出含 `sorryAx`。完整失败源及日志保存在 `isolated-history/decoder-attempt-001/`，没有生成 `.olean`。

`attempt-002` 将该已经可以通过定义展开闭合的分支改为 `rfl`，核心三个定理实际 PASS。两轮源的完整差异见 `decoder-attempt001-to002.diff`。`attempt-003` 增加完整 iff 和宽度包装后首次实际 PASS。

成功轮的 `LEAN_PATH` 只含 Width 的已通过作者对象目录和 runtime 的 23 模块开发环境，不含失败目录；本审阅没有隐去真实失败，也没有把失败日志当作成功证明。
