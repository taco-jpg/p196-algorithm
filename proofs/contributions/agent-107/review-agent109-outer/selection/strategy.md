# Agent107 下一任务选择依据（仅规划）

日期：2026-10-15。只读快照：`origin/main = 69eb1a79b4e59a353e6ba30ff19d4fc623df9b65`；`origin/p196/coordination = 80d8054e0028b6040aa9a05aefd43d59f5a7af04`。本轮未 fetch、未修改仓库、未运行 Lean、未认领任务；下述内容不是新数学结果或独立核验结论。

## 唯一建议：独立核验 Agent109 的实际整数外层投影桥

建议根代理在重新检查协调状态后认领窄范围 review：`agent107-review-agent109-outer-projection`，固定作者源码提交 `b2374410d427beb78fc601ee81cf15e34a1ac934`。目标是 `proofs/contributions/agent-109/outer-projection-bridge/` 的 `OuterBridge.lean`、`OuterCompat.lean` 及其两份 Agent7 有限外层依赖。没有必要另造易得推论。

当前核心数学瓶颈仍是：为**一个有限普通十进制种子**提供可无限续接且始终安全的实际全字轨道。任意长有限安全前缀、抽象前缀闭路、条件性返回证书以及受限模板排除都没有给出这个实例。`proofs/FINDINGS.md`、`proofs/README.md` 明确保留该界限。这里选择的桥将有限外层排除真正接到普通整数轨道，补足“抽象外层状态计算是否适用于真实全字”的关键语义环节；它会限制小外层再生方案，但不会解决全局存在问题。

作者任务 `agent109-outer-projection-bridge.json` 为 `READY_FOR_REVIEW`，明确写着本地 Lean checked、尚无 independent review。计划仅核验已实现的 (a) 外层对应和 (b) 实际轨道 cap-two 排除；作者 (c) “每个有效返回证书均含外层长度大于二状态”仍未完成，不纳入此轮。

## 需要独立接受或拒绝的精确端点

实际声明为 `Agent109.OuterCompat.lychrel_cap2_exit`，不是仅有限图表断言。令 `n : Nat`、`p : Fin 8`、`B A C : Agent109.Word`、`g h : Nat`。前提逐项保留：

```lean
Agent109.Bounded B
Agent109.Bounded A
Agent109.Bounded C
B.length ≤ 2
P196.Agent7.Finite.validOuter ⟨2 * (p.val + 1), B⟩ = true
14 ≤ g
14 ≤ h
Agent109.pairWord n = Agent8.template (2 * (p.val + 1)) B A C g h
```

其结论是：

```lean
∃ i, i ≤ 7 ∧ ∃ c' B' A' C' G H,
  2 < B'.length ∧
  B' = (P196.Agent7.Finite.outerIterate i
    ⟨2 * (p.val + 1), B⟩).B ∧
  Agent109.pairWord (Lychrel196.orbit n i) =
    Agent8.template c' B' A' C' G H
```

这只声称存在一个与指定外层迭代相容的模板表示。不能改述为整数退出所有可能模板表示，也不声称此时出现回文、所有种子终止或 196 已进入此模板。

## 实际声明及依赖链

1. `TemplateStep.lean` 的 `Agent109.actual_template_step` 将全字模板变换接到实际 `step`；`Compat.lean` 的 `Agent109.Compat.orbit_eq` 接到仓库的 `Lychrel196.orbit`。
2. `OuterBridge.lean` 的 `Agent109.Outer.outerNext_eq` 对任意 `c B A C` 证明 `outerNext ⟨c,B⟩ = ⟨tOf c + tOf c, stripSuffix (tOf c + tOf c) (Br c B A C)⟩`；`stripSuffix_spec` 提供被去掉尾段确为相位字母重复串。
3. `Agent109.Cert.template_trim`（`template-return-certificate/ReturnCertificate.lean`）与上述结果组成 `actual_step_outer`；`succ_bounded`、`bounded_strip` 保持下一步所需的系数界。
4. `actual_outer_orbit` 在 `2*i ≤ g`、`2*i ≤ h` 下，给出实际 `orbit n i` 的模板表示、受界块，以及 `g ≤ G+2*i`、`h ≤ H+2*i`。`outerIterate_eq` 连接两种递归迭代定义。
5. Agent7 `OuterFinite.lean` 的有限核证 `cap2_exits_by_seven`，经 `OuterBounds.lean` 的 `decode_complete`、`cap2_unencoded`、`exit_witness_of_false` 产生七步内外层长度大于二的时刻。最后 `actual_cap2_exit` 和 `lychrel_cap2_exit` 得到上述实际整数端点。

作者 build 脚本的源码闭包共九个模块：`LychrelDigitSums`、`PeriodObstructions`、`TemplateStep`、`Compat`、`ReturnCertificate`、`OuterFinite`、`OuterBounds`、`OuterBridge`、`OuterCompat`。复制的两个 Agent7 源文件固定于 `da4a1799b74b98b4199cdb224ea7a694b2657651`：

| 文件 | SHA-256 |
|---|---|
| `agent7-deps/OuterFinite.lean` | `3376873da457c698850f604ddda82aeba3e67f4196e5c33d8142bed945c5f3f6` |
| `agent7-deps/OuterBounds.lean` | `75ed5831f0cc1e9c6016672ebef83cf0f46da279432b3694ba075627cb973a76` |

以上为已读源码/作者记录，不代表本轮已重新执行内核核验。

## 碰撞检查

已读取上述实际 Lean 声明，并扫描当前协调任务的 `review.*outer|outer.*review|b237441|ExteriorErasure|erasure.*review`。截至固定协调快照，没有 Agent109 outer-projection 独立审查认领。

| 现有所有者/记录 | 与建议任务的边界 |
|---|---|
| Agent102 `agent102-review-agent109-step-bridge`，REVIEWED | 审的是 `9a2f01e3831763fea87021aa6b9e8af0b94c8beb` 的旧一步模板桥；未覆盖新增外层模块和 Agent7 cap-two 表。其审查记录提交为 `042c462b2050ac6095fd19225b2d578cbfc9a65e`。 |
| Agent101 `agent101-review-outerrank`，REVIEWED | 仅审 `proofs/agent7/OuterRank.lean` 的五个通用定理，不能当成 `OuterFinite` / `OuterBounds` 的独立审查。 |
| Agent103 `agent103-review-agent109-certificate`，REVIEWED | 已审条件返回证书。这里只复核实际引用的 `template_trim` 及精确导入闭包，不重认领证书 soundness 或证书实例工作。 |
| Agent101/102 cap5/6/7 | 有限计算工作；此处固定为 kernel cap-two 与实际整数对应，不重跑大规模搜索。 |
| Agent105 高返回判据、Agent104 七列及 Agent4 whole-word 审查、Agent109 8/17 核验 | 均保留原所有者；本建议不涉及这些范围。 |

Agent109 是作者，并且明确请求该模块独立审查；独立 review 属不同窄范围任务，仍应先由根代理成功发布 claim。本文件本身不产生所有权。

## 有界执行计划和验收

1. 成功 claim 后，在独立空目录提取固定提交九模块，记录提交、所有源码哈希、官方 Lean 4.19.0 (`6caaee842e94`) 编译器来源与哈希。单编译槽完整从源重建，不复用作者 `.olean`。作者日志约三分钟，仅作预算参考。
2. 动态列出新增 `OuterBridge`、`OuterCompat`、`OuterFinite`、`OuterBounds` 的全部导出定理，对每个定理运行 `#print axioms`；审计闭包只允许标准逻辑公理。对全部九份源码扫描 `sorry`、`admit`、`native_decide`、`Lean.ofReduceBool`、新增 `axiom` 和任何替代执行/信任绕过路径。作者脚本的 token scan 未覆盖两个早期依赖，因此独立审查必须覆盖完整闭包。
3. 做逐声明语义核对：有限编码是否穷尽所有长度≤2且系数≤18的词；`validOuter` 的作用；七步计数的首末端点；`stripSuffix` 是否只改变可吸收的带长；`outerIterate` 方向；实际 `pairWord`、`step`、`orbit` 是否保持仓库原语义。避免把“某一指定外层坐标”提升为模板分解唯一性。
4. 专门检查带长边界：声明与 README 使用 **14**，但 `OuterBridge.lean` 顶部和 `actual_cap2_exit` docstring 仍写 **16**。需以真实定理为准，说明七次消耗每次最多二的递推为何允许第七步输出带长为零、而每个被调用的一步公式输入仍至少二；报告该文档差异，不擅自修改作者源。
5. 产出窄范围 `REVIEW.md`、固定源码/编译器清单、完整编译日志和全导出 axiom 审计；所有失败/UNKNOWN 保留。判定必须区分“作者本地 checked”“此次独立 checked”“条件性结论”和“未实现 (c)”。若构建或语义失败，给最小失败点并停在这个边界，不扩展认领新的数学任务。

验收价值是将一个尚未独立复核的真实整数外层桥变为可明确引用的可信基础；不以新增定理数量为目标，不发布新的存在性声称。
