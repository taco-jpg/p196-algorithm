# 安全分类口径与 33 项 ledger 的准确含义

核对者：**Agent #103 /root/runtime**。此记录补充解释既有原始字段，没有改动旧构建结果、原始日志或数学源码。

## 实际记录的不同类别

在 27 个项目模块的实际 module-origin 环境中，正式审计得到：

| Lean 常量类别及判定 | 项数 | 所属范围 | 保留位置 |
|---|---:|---|---|
| `axiomInfo v` 且 `v.isUnsafe=true` | 33 | 全部为依赖，四新模块为 0 | `UNSAFE_IMPLEMENTATIONS.json` |
| `defnInfo v` 且 `v.safety=.safe` | 216 | 全部为依赖 | `DEFINITION_INVENTORY.json` |
| `defnInfo v` 且 `v.safety=.unsafe` | 917 | 全部为依赖 | `DEFINITION_INVENTORY.json` |
| `defnInfo v` 且 `v.safety=.partial` | 24 | 全部为依赖 | `DEFINITION_INVENTORY.json` |
| `opaqueInfo`，任一安全类别 | 0 | 闭包中没有此类记录 | `DEFINITION_INVENTORY.json` |
| `thmInfo`，实际逐项公理查询 | 1881 | 1834 依赖 + 47 新模块 | 正式 `verification.json` 与原始审计日志 |

**33 的精确含义仅为第一行。** 旧审计字段 `unsafe_implementation_constants` 与原日志前缀 `UNSAFE_IMPL`，由 `check.py` 的 `.axiomInfo v` 分支产生。该分支没有统计 `.defnInfo` 的 `safety`。所以把“33 个 unsafe 实现 helper”读作“环境总共只有 33 个 unsafe 常量”是不正确的。

本次另外记录了全部项目 `.defnInfo` / `.opaqueInfo`，得到 **1157 = 216 + 917 + 24**。源码声明数、生成常量数和安全类别数也不是同一个计数：四新源含 20 条 theorem 声明，编译后产生 47 个 theorem 常量，但没有 definition 或 opaque 常量。

917 和 24 是编译环境中的常量数，包含生成的实现辅助常量；不能将其读作源文件中分别写了 917 条 `unsafe def` 或 24 条 `partial def`。

## 已核对的 Lean API

对应官方编译器 commit 的 [Lean/Declaration.lean](https://github.com/leanprover/lean4/blob/6caaee842e94/src/Lean/Declaration.lean) 明确区分 `AxiomVal.isUnsafe`、`DefinitionVal.safety` 和 `OpaqueVal.isUnsafe`。其中 `ConstantInfo.isUnsafe` 对 `.defnInfo` 只检查 `safety == .unsafe`；`partial` 由独立的 `isPartial` 判断，不能合并算作同一标志。

原官方源保存在归档的 `references/LeanDeclaration.lean`，Git blob 为 `5c175072ac70e161fd5ffc1d9033e7ec1ce8c81c`，SHA-256 为 `e785ec71e3d827c254db293fec6f76aa95c227f2d71e3c80c78098e06655d374`。它是分类 API 的只读参考文件，没有加入数学 import 闭包，也没有触发第二次 Lean 构建。

正式生成器对其他类别使用 `_ => pure ()`；它没有给 `inductInfo`、`ctorInfo`、`recInfo` 的安全标志做完整清点。因此这里也**不把 33+917=950 宣称为所有常量种类的环境 unsafe 总数**。这些边界是此次记录的真实范围。

## theorem 公理结果没有变化

正式审计对 **全部 1881 个 `thmInfo`** 各发出一条实际 `#print axioms`，解析器核对名称唯一性、完成计数及查询结果一一对应。每个结果均为 `{propext, Classical.choice, Quot.sound}` 的子集。33 项 unsafe `axiomInfo` 和所有已记录 unsafe / partial definition 名称均未出现在任何 theorem 的公理列表中。

对第二包已有的 **1812 个 theorem**，本次逐项比较名称、module origin、公理列表，全部相同；原 33 项 `UNSAFE_IMPL` 也逐项相同。新增原 `Agent101PalindromeFibers` 贡献 22 个编译 theorem，加四新模块的 47 个，得到 1881。这是对记录范围的澄清和增补，不是对原公理 PASS 的撤销或弱化。

该审计会拒绝所选项目模块中非 unsafe 的自定义 `axiomInfo`，并保留 unsafe 实现声明 ledger。它不把这些实现声明隐藏，也不对每个旧 safe definition 另行声明公理检查；旧定义在被已审 theorem 使用时由传递公理查询覆盖。实际来源、完整定义逐名清点与标准公理结果均在相应 JSON 及原始日志中保留。
