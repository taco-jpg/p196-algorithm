# Agent107 独立语义审查：Agent109 外层投影整数桥

**判定：PASS（精确定理的数学语义）；两处非阻断性文档限定需要更正。**

审查人：Agent107 / `status_audit`。日期：2026-10-15。任务认领：`agent107-review-agent109-outer`，协调提交 `241d17f64de0495ecad32d2cc2aa68b467748b63`。固定作者源码：`b2374410d427beb78fc601ee81cf15e34a1ac934`，读取位置 `/workspace/scratch/64704429df15/review109-source107`。本审查未修改作者文件，未执行 Lean、有限枚举或数值实验；独立干净重建与公理审计由 `independent_review` 单独负责。本报告的 PASS 只表示下列原始声明与所述数学目的相符、未发现语义缺口，不代替执行报告。

## 固定源码及审查范围

以下 SHA-256 已直接读取文件计算；它们标识本次语义审查对象。

| 文件（均相对 `proofs/contributions/agent-109/`） | SHA-256 |
|---|---|
| `outer-projection-bridge/OuterBridge.lean` | `d0fa857eb84573e3a5afab09c8e3fa0f82244fcc72ad5b5623298bbd0bc2099e` |
| `outer-projection-bridge/OuterCompat.lean` | `56dea5ebfddc5dd31cbc951d38205c74be42e201b40eee622c71fe0df57e4a7c` |
| `outer-projection-bridge/agent7-deps/OuterFinite.lean` | `3376873da457c698850f604ddda82aeba3e67f4196e5c33d8142bed945c5f3f6` |
| `outer-projection-bridge/agent7-deps/OuterBounds.lean` | `75ed5831f0cc1e9c6016672ebef83cf0f46da279432b3694ba075627cb973a76` |
| `template-step-bridge/TemplateStep.lean` | `76ad132fec23f9da8733f72a6baf22c3dbfe68d402a8165766bd8d163549d2ed` |
| `template-step-bridge/Compat.lean` | `73dca78232b0c2c048da4d1d182f84b31c0e95bab283fad603fd342bf38616e6` |
| `template-return-certificate/ReturnCertificate.lean` | `b6d34e8fb031401171b517eef8a2d91222334a5745cc88329e0a2ad13db47058` |

另读取原始 `Lychrel196` 算术定义、Agent8 `PeriodObstructions.lean` 中的 word/template 定义，以及 `2026-10-15-complementary-bulk-quotient/METHOD_AND_PROOF.md` 第 4–6 节的公式 (3)–(11)。两份 Agent7 复制依赖的上游 pin 为 `da4a1799b74b98b4199cdb224ea7a694b2657651`。完整九模块源码/编译器清单及执行状态以独立执行报告为准。

## 1. 实际普通整数对应：PASS

`Agent109.pairWord n` 定义为 `pair (digits n)`；`digits` 从普通 `Nat` 取最低位优先的规范十进制数位，零对应空词。它不是可任意指定长度或补前导零的抽象词。

读到的关键链条为：

- `Agent109.reverse10_eq`、`step_eq_evalL_pair`：数位反转与 `n + reverse10 n` 的数值关系。
- `Agent109.lastPos_pairWord`、`bounded_pair_digits`、`canon_normalize`、`digits_evalL`：加法正规化后的词确为实际后继整数的规范数位。这里保留了实际进位造成的宽度增加，并排除了靠额外前导零改变反射宽度的解释。
- `Agent109.pairWord_step`、`pairWord_orbit`、`actual_template_step`：模板公式接到实际 `step` 和递推轨道，而非仅接到一个另行假定正确的词算子。
- `Agent109.Compat.reverseFuel_eq`、`reverse10_eq`、`step_eq`、`orbit_eq`：副本接到原始 `Lychrel196` 常量。原始 `step n = n + reverse10 n`，`orbit n 0 = n`；没有跳过初始时刻或遇到回文后改变递推。
- `Agent109.Compat.template_eq` 是定义性等式；`Agent109.OuterCompat.lychrel_cap2_exit` 最后显式改写成 `Lychrel196.orbit` 和 `Agent8.template`。

模板实现允许词层面无对称性/正性的块，但整数端点另有精确前提 `pairWord n = template ...`。因此不能把任意 `B,A,C` 都说成已实现；反过来，实际实例的中心对称性等限制由该等式承载，端点不需要额外假定一个“全字可实现性桥”。

## 2. 相位、界及确定性外层更新：PASS

`Agent109.Phase c` 精确定义为 `1 ≤ c ∧ c ≤ 17 ∧ c ≠ 9`；`Bounded w` 为所有自然数系数≤18。它们支持带段在首列后重置到确定进位 `kOf c`。排除中性相位 9 是实际公式的必要条件，未被忽略。

`Agent109.Outer.outerNext_eq` 本身是任意 `c,B,A,C` 上的代数定义对应：

```lean
outerNext ⟨c, B⟩ =
  ⟨tOf c + tOf c, stripSuffix (tOf c + tOf c) (Br c B A C)⟩
```

`Br` 虽有 `A,C` 参数，其使用的数据只来自 `norm B 0`、`norm B.reverse (kOf c)`；最终进位 `γ` 与入口数字均由这些块真实计算，未自由选择。`normalize7_eq` 连接两套同长度正规化定义。相位/界条件在后续用于实际公式及进位界，不应误加到这个纯定义对应声明上。

`Agent109.Outer.succ_bounded` 对 `Br,Ar,Cr` 逐块使用正规化数位≤9及两数位相加≤18；`bounded_strip` 保留剩余子词的界。`Agent109.next_phase` 保证下一相位仍合法；整数 cap-two 端点限定 `c=2*(p.val+1)`、`p : Fin 8`，即偶相位 2,4,…,16，满足上述非中性正相位条件。此端点没有声称对全部十六个合法起始相位直接使用同一有限表。

## 3. 去尾、带长和七步门槛：PASS

`stripSuffix c w = (w.reverse.dropWhile (· == c)).reverse` 恰好去掉最长的末尾 `c` 串；`stripSuffix_spec` 给出 `w = stripSuffix c w ++ replicate j c`。`Agent109.Cert.template_trim` 是无证书前提的串连接等式。`actual_step_outer` 只用其中 `B` 去尾情形，其余去段量取零；不需要假定返回证书存在、成立或安全。

将一步的输入带长写成 `G=g+2`、`H=h+2`，原始公式先产生 `g+γ,h+γ`，去掉外层末尾 `j` 个新相位字母后得到：

```text
G_next = G - 2 + γ + j
H_next = H - 2 + γ
```

这里输入已至少二，减法没有下溢含义；`γ` 是实际最终进位，`j≥0`。因此每条带每步损失至多二。`actual_outer_orbit` 显式保留 `g ≤ G+2*i`、`h ≤ H+2*i`，并在归纳后继处先证明当前 `G,H` 可写成 `G'+2,H'+2`，再应用一步公式。没有把“带始终足够长”作为未供应的额外轨道假设。

所以 `14 ≤ g,h` 足以覆盖到时间七：第六时刻用于第七次更新的输入仍至少二；时间七的输出允许为零，并且模板及公式 (8) 本来允许零长度剩余带。无需保证时间七还能再做一次同类更新。`outerIterate_eq` 正确连接 Agent7 尾递归迭代与本模块前向递归迭代。

## 4. 有限 cap-two 证书和精确结论：PASS

`P196.Agent7.Finite.decodeWord` 的范围是空词、19 个一字词、361 个二字词，合计 381 个编码；`decode_complete` 在长度≤2且每项≤18时给出一个编码。`cap2_exits_by_seven` 对八个偶相位和全部这些编码量化，源码使用 `decide +kernel`；其执行/公理信任边界另由独立执行审计核实。

`validOuter` 明确检查：系数≤18；非空时第一个系数正；非空时最后一个系数不等于相位。空 `B` 被接受。有限结论没有把后继强行截断回 cap-two 集合：`staysSmall 7` 沿完整 `outerNext` 递推，检查时间 0,…,7 共八个状态的外层长度。`exit_witness_of_false` 将失败转换成这个闭区间内的退出时刻。只有初始状态需要 `validOuter`；证明没有遗漏一个本应额外供应的逐步 validity 保持前提。

`Agent109.Outer.actual_cap2_exit` 和 `Agent109.OuterCompat.lychrel_cap2_exit` 的全部实质前提是：三个块受界、初始外层长度≤2、上述 initial validity、两带至少 14，以及一个实际整数的精确模板实现。结论给出 `i≤7` 及一个模板表示，其 `B'` 等于指定 `outerIterate i` 的外层，且 `B'.length>2`。初始长度≤2自动排除该见证在时间零，但正式声明保留较弱的 `i≤7` 表述，没有问题。

结论是**指定外层坐标沿真实轨道的退出**。它不证明整数不能换用另一组块/带长表示，也不证明完整模板分解唯一，不是回文出现、全局终止或 Lychrel 存在结论。`cap2_sharp_six`、`cap2_sharp_seven` 的 sharpness 仅是 Agent7 外层轨道事实；本模块没有另给实际整数达到七步上界的专门实例，不能静默升级为整数端点的已实现最优性。

## 5. 非空性与无循环前提

对前提相容性的语义检查可取 `p=0,c=2,B=A=C=[]`、`g=h=14`：三个块受界，空外层通过 `validOuter`；所需 pair word 是 `2^14 ++ 16^28 ++ 2^14`。与之对应的规范数位候选为 `D=1^14 ++ 8^28 ++ 1^14`，令 `n=Agent109.evalL D`；`digits_evalL` 及 `pair` 定义解释了该实现方式。这里幂上标只表示重复串。这个例型用于检查假设没有要求矛盾的数位/相位条件，不是本报告新增的 kernel-checked 实例；未运行或发表新的实例定理。该候选本身为回文也无妨，因为被审端点根本没有要求起始安全。

外层桥没有假定待证的退出结果、没有假定全轨道可实现，也未把安全或返回性塞进 validity。引入 `ReturnCertificate` 只是为了可直接使用 `template_trim`；该引理是串代数，其证明不依赖 `Valid`、`check_sound`、Lychrel soundness 或任何证书实例。

## 6. 需要纠正的文档限定及未完成范围

1. `OuterBridge.lean` 文件开头及 `actual_cap2_exit` 的 docstring 仍写带长至少 **16**；实际声明及 README 为 **14**。后者有正确的逐步预算。作者应统一为 14，并注明终点带长可以为零。这是过强旧描述，不是定理失败。
2. `actual_outer_orbit` 的 docstring 将所有时刻的外层称为“maximally trimmed”。该通用定理没有要求初始 `B` 已去尾，因此时间零只能称为**给定外层坐标**；从一次 `outerNext` 以后才按定义取最大去尾。可将说明改成“specified exterior, maximally suffix-trimmed after each transition”，或另明确初始 normalization 前提。最终 cap-two 端点的 `validOuter` 已保证初始 `B` 无该相位末尾，因此其用途无缺口。不要为了修正文案悄然加强已发布定理前提。

`agent109-outer-projection-bridge` 任务所列 (c)“每个被接受的返回证书均有一个去尾外层长度大于二的状态”仍未在该包实现。既有 `Agent109.Cert.Valid` 只约束显式 trimming 分解、相位、界和带预算，并未把本包的最大去尾坐标识别作为已证公理。不能仅凭此七步实际坐标退出定理，便宣布所有证书的列出外层状态也已完成同一排除；证书状态与最大去尾投影的对应仍需独立声明/证明。该未完成工作与本次 (a)/(b) 独立审查分开，且本报告不启动它。

签署：Agent107 / `status_audit`，2026-10-15。**原始精确数学端点语义 PASS；上述两条描述需修正或在发布审查中明确覆盖；kernel 执行结论由单独执行记录给出。**
