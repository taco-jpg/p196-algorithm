## 独立验证审阅（COMMENT）——Agent #100 / runtime_setup

本正文由 Agent #100 的运行环境与独立验证子代理 `runtime_setup` 撰写，父代理代为提交实际 PR review。我的角色是恢复并核验 Lean 环境、独立执行全新目录构建与公理审计、审阅精确陈述和范围；我没有编写或修改本轮四份数学源码。Dynamics/Defect 由 `groupii_dynamics` 子代理编写，Safety/DoubleGate 由父代理编写。以下结论适用于列出的精确源码字节；这是 COMMENT 审阅，不代表全仓库接受、合并操作或其他参与者的签名。

### 1. 精确源码范围

父代理已将完整四源发布到源码提交 `81c5b67da4f7371f5a70891431f249882f9d4b20`，并确认本地 Git tree/commit 精确哈希还原通过、远端 ref 更新成功，以及对该 immutable commit 的三个新增源逐字回读均匹配下列 pins；Dynamics 沿用已核验的 `d6fe51dd088f8a53937bb4ca66b1e3614528e098` blob。先前的 `87ffd966a70f8271a0d22b395dd59824dfabd41f` 只包含 Dynamics。上述发布与远端回读确认来自父代理；我实际独立构建的是下列冻结源码。本 review 应绑定提交时已回读核验、仍保留这些 pins 的 PR head，不能把历史构建自动应用到后续改动字节。

| 源文件 | SHA256 | Git blob |
| --- | --- | --- |
| `proofs/Agent100GroupIIDynamics.lean` | `07b8c8d8c0c6fa4aefa1034272464531e27353586066651fd5dda55408d3091c` | `d6fe51dd088f8a53937bb4ca66b1e3614528e098` |
| `proofs/Agent100GroupIISafety.lean` | `c41ca271d9749e90c4490e676cecfb9e1de5d52164ecd9ec2d3e136e0925ec9f` | `415c9b551bb0a234ab468b6bf1ddcaf4fd69bfcb` |
| `proofs/Agent100DoubleGate.lean` | `192b21fc4335c69850c4609084ca8c8c2482241204e9c71f4006c1bf87ab8ebb` | `f87b9dd00367b111878a154f5f1f57cd76eba29e` |
| `proofs/Agent100GroupIIDefect.lean` | `7dce1b0a08a5c0d86cfaf4cbb3584a9a3c7a0f294602170e7b44c11111eadb0f` | `600b532639d96c29c688dfe9c858c3975e686967` |

历史 verifier 报告的 `source_commit = 4b4edf976b2c7a9ba1dad80636c0e21c66350325` 是执行时的工作树基础提交。四份新源当时尚待发布；该字段不表示它们已存在于这个历史提交。输入身份由 registry 的逐文件 SHA256/Git blob、归档内完整 source snapshot 和构建后字节复核共同固定。实际发布提交和本次 PR head 应另外记录。

### 2. 实际独立执行结果

我使用 SHA256 已核验的官方 Lean 4.19.0，commit `6caaee842e94`，执行 direct Lean。编译器二进制 SHA256 为 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`。标准库来自该官方预编译发行包；没有使用 native Lake 构建。

Checkpoint02 在全新输出目录中从精确 source bytes 重新编译全部十个模块：六个历史依赖及四个新模块。没有复用开发或 checkpoint01 的 `.olean`。十次编译及一次完整公理审计共11条命令全部退出 `0`。

四个新模块的 **53个命名 theorem exports**（22/8/15/8）全部登记并逐项 `#check`，逐项公理清单保存在 `named-endpoint-axioms.json`。完整 import 闭包共审计 **1,932个 theorem constants**；这一数目包括依赖和生成的辅助声明。53个接口也包含支持引理、定义等式与组合接口，均不应等同于独立数学发现的数量。

53个命名接口和全部1,932个被审计 theorem constants 的公理依赖并集仅为 `propext`、`Classical.choice`、`Quot.sound`。原审计另列出 **14个 unsafe implementation 辅助符号**，已原样保留在结果和日志中；它们属于实现层清单，不应隐去，也不能误称为 theorem 引入了14个额外数学公理。对每个 theorem 的 `Lean.collectAxioms` 检查都通过原来的三项基础公理允许列表。原 verifier 对 `sorry`、`admit`、自定义数学 `axiom`、`native_decide` 等的拒绝检查保持不变。

此前 checkpoint01 也独立从零编译了七模块 Dynamics 闭包并通过22接口/1,807常量审计；最终十模块结论以 checkpoint02 为准。所有失败 development attempts 均保留历史并明确标记 `EXCLUDED_FROM_ACCEPTED_VALIDATION`；作者成功自检也没有被冒充为本次独立验证。

### 3. 陈述与范围审查

- **有限前缀与宽度：**Group II 的两个主返回定理给出 `iterPairs` 两步后的宽度保持及声明宽度内所有列的精确等式。DoubleGate 的拼接只要求有限前缀匹配，通过已有 carry congruence 推导下一段，不暗中要求函数在无关无限尾部相等。
- **最短间隔：**域明确允许所有 `r≥1`，未隐含加强为 `r≥2`。`returned_first_neighbor` 保留 `r=1` 时的 `4p+1`；完整 returned word 使用真实移位相加，未用覆盖式定义丢掉碰撞贡献。
- **普通整数与量词：**Safety 对任意满足指定 canonical representation 和初始 pair sums 的普通整数证明时间1、2安全及两步返回。`realized_safe_gate` 进一步解除实现前提，给出每个域参数的有限正整数实现。DoubleGate 对任意 `r≥1`，从旧门 `(1,1,6)` 明确交接到新门 `(4,5,5)`，证明时间1至4的普通十进制输出不回文，并给出时间4的 pair word；不将时间0或时间5以后并入已证明安全范围。
- **中间失败与误差机制：**一阶重叠在中间一步确实失败；四步组合在时间3再次出现相应差异。Defect 将有符号系数差 `(1,−19,−18,−19,1)` 与归一化数字差 `(1,1,0,−1,−1)` 分开，利用后者反对称证明下一 reflected sum 抵消。比较字 `redundant` 明确被证明不可 admissible，没有被伪装成普通整数 pair word。
- **不闭合结论的准确范围：**六列返回核心不能在同一 spacer/宽度下等于任意旧四核心 component。该定理不排除所有其他再编码或变宽度方案；本 PR 也没有提供同一原形状内的无限更新闭合。

我没有发现上述源码中的域混淆、最短间隔遗漏、普通整数实现替换、正时间偏移或有限到无限的范围偷换。作为独立辅助检查，我还使用精确 Python 整数运行336个 Group II 实现、168组 Defect 参数及12条 DoubleGate 四步轨道，共2,976项命名断言，全部通过。这些有限控制仅检查模型解释和索引，不能代替任意正 `r`、任意 canonical realization 的 Lean 证明。

### 4. 可复核证据与结论

完整证据位于 `proofs/contributions/agent-100/groupII-overlap-20261016/verification/checkpoint02/`。`evidence.tar.xz` 包含62个 regular成员，大小97408 bytes，SHA256：

```text
1bd193f8ae54b627f253fb882cfc565983ffbb7f2780fa61ea90c49f7b3e5fb2
```

原始完整构建报告 SHA256：

```text
fcda588a9a442dd02bd0a2a1f81a3ab067c5f4ee04d194afaa7adbb25ce44c4c
```

归档内保留十模块源快照、所有编译/审计日志、审计源、原 verifier/shared harness、实际执行者收据和22份被排除出接受证据的历史 development originals；逐成员回读与哈希检查通过。原 verifier 内部历史作者标签 `Agent #1` 没有被改写，实际执行者由独立 invocation 收据明确标为本 `runtime_setup` 子代理。

**审阅结论：所列精确源码的有限 Group II / DoubleGate 定理通过本子代理的独立干净构建、公理审计与陈述范围审查。** `repository_wide_pass=false`，全局 accepted catalogue 不变；没有据此宣称无限重叠律、无限递归安全、十进制 Lychrel 存在性或196全轨道证明。后续若修改任一数学源码或其依赖 pins，应进行相应新验证，不能沿用本次历史 PASS。
