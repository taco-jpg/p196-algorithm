# Agent #107：原 canonical verifier 独立运行结果

**结果：PASS，exit 0。** 从已发布提交 `be8e612ca0694d5d9d8473c784ab1956f93405b6` 的干净隔离工作树实际执行原未改 verifier；12 个注册模块全部从源码重编，随后总模块来源公理审计成功。13 个 Lean 命令全部 exit 0。

UTC 开始 `2026-10-16T22:02:47.437707+00:00`，结束 `2026-10-16T22:05:39.720553+00:00`；实测耗时 `172.28276` 秒。运行前后 HEAD 相同、工作树状态为空。原 verifier SHA256 为 `c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a`；注册表 SHA256 为 `2a897d49fe54eba72f48e68e7888b3fe9d21aa2cc58f1abb2d48a0a68bd4b238`。实际命令见同目录 `invocation.json` 的 argv。

调用者是 Agent #107；原 `verification.json` 的 `agent: Agent #1` 是原脚本作者字段，完整保留。此为显式选择项目的 scoped gate，原报告 `repository_wide_pass` 为 false，不能外推为整个仓库全部项目通过。

本次原脚本 Lean 命令未显式设置 `--trust=0`，没有修改脚本以改变该行为。此前作者及独立检查已分别显式使用 `--trust=0`；两类证据分开保留。本记录不把本次原脚本命令称为显式 trust-zero 检查。

## 完整模块来源审计

总计 **1338 条定理**，其中基础模块 **787 条**、Agent107 模块 **551 条**。审计含各模块辅助定理，按实际 `env.getModuleIdxFor?` 来源筛选，不只检查列出的公共端点。

| 模块 | 定理数 |
|---|---:|
| `Agent107TransducerBoundary` | 21 |
| `Agent107TransducerDefs` | 18 |
| `Agent107TransducerGraph` | 26 |
| `Agent107TransducerInput` | 25 |
| `Agent107TransducerNumeric` | 3 |
| `Agent107TransducerOutput` | 50 |
| `Agent107TransducerPath` | 36 |
| `Agent107TransducerReachable` | 51 |
| `Agent107TransducerTables` | 23 |
| `Agent107TransducerTablesChecks` | 276 |
| `Agent107TransducerTablesData` | 22 |
| `Lychrel196Research` | 787 |

所有定理依赖的公理并集恰为 `Classical.choice`、`Quot.sound`、`propext`；无自定义或其他禁止公理依赖。按照完整跨行日志归一化后：

| 公理集合 | 定理数 |
|---|---:|
| 无 | 324 |
| `Classical.choice`, `Quot.sound`, `propext` | 74 |
| `Quot.sound`, `propext` | 700 |
| `propext` | 240 |

原脚本同时报告 **18 个 unsafe implementation 占位**：基础模块 13 个、Defs 2 个、TablesData 3 个。这是原脚本对 `axiomInfo.isUnsafe` 的分类；所有已审计定理的公理依赖仍仅包含上述三个允许项。没有将这些实现占位隐去或计作新的数学假设。精确名称如下：

- `Lychrel196Research`：`List.flatMapTR.go._at.OverflowNormalizationCertificate.finishFuel._spec_1`
- `Lychrel196Research`：`List.mapTR.loop._at.OverflowNormalizationCertificate.feed._spec_1`
- `Agent107TransducerDefs`：`_private.Init.Data.Option.Basic.0.Option.decEqOption.«_@».Init.Data.Option.Basic._hyg.4._at._private.Agent107TransducerDefs.0.Agent107.FoldedTransducer.decEqWord.«_@».Agent107TransducerDefs._hyg.1078._spec_1`
- `Lychrel196Research`：`List.mapTR.loop._at.OverflowNormalizationCertificate.initials._spec_2`
- `Agent107TransducerTablesData`：`List.flatMapTR.go._at.Agent107.FoldedTransducer.Table.terminals._spec_1`
- `Agent107TransducerTablesData`：`List.mapTR.loop._at.Agent107.FoldedTransducer.Table.centers._spec_1`
- `Lychrel196Research`：`List.mapTR.loop._at.OverflowNormalizationCertificate.next._spec_1`
- `Agent107TransducerDefs`：`Option.repr._at._private.Agent107TransducerDefs.0.Agent107.FoldedTransducer.reprWord.«_@».Agent107TransducerDefs._hyg.1223._spec_1`
- `Lychrel196Research`：`List.mapTR.loop._at.OverflowNormalizationCertificate.initials._spec_1`
- `Lychrel196Research`：`List.flatMapTR.go._at.OverflowNormalizationCertificate.finals._spec_1`
- `Agent107TransducerTablesData`：`List.flatMapTR.go._at.Agent107.FoldedTransducer.Table.edges._spec_1`
- `Lychrel196Research`：`List.repr'._at._private.Lychrel196Research.0.OverflowNormalizationCertificate.reprState.«_@».Lychrel196Research._hyg.20378._spec_1`
- `Lychrel196Research`：`OverflowCarryNormalization.iterPairs._elambda_1`
- `Lychrel196Research`：`List.flatMapTR.go._at.OverflowNormalizationCertificate.initials._spec_3`
- `Lychrel196Research`：`List.flatMapTR.go._at.OverflowNormalizationCertificate.next._spec_2`
- `Lychrel196Research`：`List.flatMapTR.go._at.OverflowNormalizationCertificate.feed._spec_2`
- `Lychrel196Research`：`List.flatMapTR.go._at.OverflowNormalizationCertificate.finals._spec_2`
- `Lychrel196Research`：`List.flatMapTR.go._at.OverflowNormalizationCertificate.edge._spec_1`

## 证据完整性

原 `FILES.json` 的 27 项逐文件 SHA256 和字节数均已复核匹配；原清单自身 SHA256 为 `5d0892a8eb1be94ae10467735bb8d3ab419c06fc73cec48a7ab2a66b5d591405`，与运行结束时记录一致。原 `verification.json`、全部日志、构建源码快照、自动生成的 `ProjectAudit.lean` 均未修改。

本 invocation 子目录在原 verifier 退出后另行加入，保留调用者收据、原 verifier/registry 字节快照、外围日志和本汇总；`INVOCATION_FILES.json` 覆盖补充后的全部非 `.olean` 文件。原 `FILES.json` 原字节不变。

运行前曾发现该隔离工作树尚未物化（13,991 条删除状态、verifier/registry 缺失）。当时 verifier 未启动，也没有 Lean 数学失败。主代理随后完成 checkout 物化；本次运行入口独立确认干净状态和源码与 HEAD 的字节一致性。诊断单独记录于 `setup-diagnostic.json`，未伪装成编译失败或原始即时快照。
