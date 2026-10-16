# Embedding 独立复核

结论：PASS。复核者 semantic_scout 未参与 Embedding 源码编写；本次没有修改作者源码。

固定对象：`Agent108WindowEmbedding.lean`，SHA256 `1acb5964188bcb7828bec58cbd8b5328ff9d68467e5951eb3a4bf87d78eb4e7f`。

## 真实编译与依赖边界

新建空 `build/` 后，依次用 `--trust=0 -j1 -DElab.async=false` 正式编译精确 Defs 和 Embedding 快照，全部 exit 0。独立审计覆盖 Embedding 全部 41 个公开声明，以及 Defs 的 9 个公开声明，合计 50；全部传递公理都是 `propext`、`Classical.choice`、`Quot.sound` 的子集。审计包含 expandBits、expandFin、embeddedState、embeddedTarget、finiteStateHalf、bitsFromList 等定义，不只检查定理。

原始依赖复用范围明确为 LychrelDigitSums、Trace、WholeWord、Safety、Indexing、FiniteWords、FamilyStates 的 7 个对象文件，来自 `build-independent-approved02`。该原依赖缓存已有 inventory 的独立构建和 112 声明公理审计记录。本次逐个核验原始源文件、module 副本完全相同，重算 Git blob SHA-1 与 SHA256，并记录复用对象文件 SHA256；随后只把这些对象复制到独立 `original-oleans/`。LEAN_PATH 在 wrapper 追加固定 Mathlib 之前，仅包含本次空 build 和这个原对象目录。本次不重编巨大原依赖模块，也不将该复用描述为整个原链重新从空目录构建。

所有原源均固定于提交 `12a32789056f5eec8247166564ac2ef745c3c9d6`。完整源码路径、Git blob、SHA256、对象 SHA256、命令与字面 stdout/stderr 见 `verification.json`、`SOURCE_PROVENANCE.md` 与 `logs/`。结束时再次核对作者源，哈希未变。

## 原始实际语义

原 `FiniteWord` 是 `(L : Nat) × (Fin L → Fin 19)`，只在声明的有限宽度上保存系数。`digits` 在范围外返回零，`encodeWord` 在每个有效坐标保留原系数。因此该嵌入使用有限规范状态，没有把任意 Nat→Nat 的无限尾部当成不同来源。

原 `MapsTo` 定义精确要求 nextWidth 与目标宽度相同，且每个目标坐标的 nextColumns 都等于目标系数。原 `FiniteWords.mapsTo_actual_step` 和 `actual_step_mapsTo` 将此关系与实际普通十进制 reverse-add 的规范表示双向衔接；`FamilyStates.safe_state_realizable` 提供正整数种子实现。原 `SafeState` 就是仓库的 `WordSafe`：Admissible 加上对应 value 非回文。

新 `embeddedState_spec` 直接实例化原 `familyState_spec`，实际无溢出转移和安全性继续由原族定理负责。新模块没有把一个自定义的符号边关系假设成实际 nextColumns 关系。

## 扩展二元索引

定义

    expandBits p es = false^p ++ flatMap (e ↦ [e] ++ false^p) es

恰在每个选择块之前、之间和之后插入 p 个旧 false 块。若 n=es.length，则扩展长度为

    p + (p+1)*n.

原第 j 个选择位在扩展列表位置 `p+(p+1)*j` 处恢复。恢复定理使用 getElem?，有效和越界情况都一致；因此扩展列表的注入性不依赖预先假设两个列表同长。

`expandFin` 的定义域精确为 `Fin (p+(p+1)*r)`。`ofFn_expandFin` 证明它完整还原扩展列表。虽然定义用 getD false 处理一般可选索引，真实 Fin 域的长度已由 expandBits_length 证明，默认值不会替换任何真实有效坐标。`expandFin_injective` 在上述恢复位置取值，且位置界限由 p+1>0 和 j<r 给出。

p=0 时扩展退化为原选择；r=0 时扩展包含 p 个旧 false 块，函数域 Fin 0 的唯一选择仍映射到一个合法原族成员。这两个边界都包含在统一的定理中。

## 字面块与位序

原 `Trace.blockDigit` 的 false 块为 9,9,9,9，true 块为 14,14,4,4。新 literal block 对四个坐标的 `embedding_block_getElem?` 与它完全对应。

每个旧 false 块贡献四个九，所以 physical buffer 长度是 B=4*p。`blocks_zero_expandBits` 和 `inputHalf_expandBits` 证明的是完整列表恒等式：旧族在扩展位列表处的半字，恰为新长缓冲半字。

原十进制 `DecimalDigits.value` 明确采用最小有效位优先：value d (L+1)=value d L+d L*10^L。原 `reflectHalf` 在 i<h 时保留 H i。新 `finiteStateHalf` 取 range (L/2) 并按递增 i 映射 `digits`，所以方向是低位外端到中心，与 source 列表 [5]、块序列、[14]、尾部十八的方向完全一致。

`inputHalf_zero_getElem?` 覆盖所有 i<halfWidth，而不只覆盖外端或少量观察窗口：i=0 给出 5；随后四元块用商 i/4 与余数 i%4 取位；唯一端点为 14；剩余恰好 k 个有效位置为 18。目标对应 11、4r+1 个九和 k 个十八。有效宽度之外的常数函数尾部没有被包含进有限列表。

## 规范有限半字与宽度

令 R=p+(p+1)*r，原半宽 H=4R+k+2。新源与目标均为原 encodeWord 的完整宽度 2H，故

    embeddedState.width = embeddedTarget.width = 2*(4R+k+2).

这就是 `embeddedState_width`、`embeddedTarget_width` 与 `embedded_width_eq` 的定义等式。它与长缓冲字的半长也相符：

    H = r*(4p+4)+4p+k+2.

`familyState_half` 和 `targetState_half` 借助 digits_encodeWord、reflect_low 及完整 range-map 等式，把每个规范有限状态的低半字与字面列表逐坐标对应。进一步的 `embeddedState_half`、`embeddedTarget_half` 得到 B=4p 的最终源/目标半字。

在这个族里 L=2H，因此 floor(L/2)=H，没有丢失中心位置。`finiteStateHalf` 虽然定义在所有有限状态上，本模块的状态桥针对这些偶宽状态；Incoming 的其他宽度分支由其自身权重定义处理。

## 实际安全前提和最终参数桥

列表、宽度、恢复与注入结论对所有 p,k,r∈Nat 成立。实际 `embeddedState_spec` 和 `embeddedTarget_safe` 明确保留 `0 < k`。因此 k=0 的列表恒等式不会被误读为已经证明该边界上的实际安全转移。

对于窗口宽 b+1，取 p=b+1，则 B=4*(b+1)。FamilyRatio 取 c=3*b+4，使 b+c=B。所有原自由位 r 仍可任意增长；β 和端点常数的定义与该参数替换相容。源与目标完整宽度相同，足以让只依赖宽度的同一权重因子一致。

## 结论

精确来源、有限索引注入、完整位序、实际转移、安全前提、偶宽和半字桥均通过语义复核；无需源码修正。新源码的全部公开声明也已通过独立 trust0 重建和公理审计。Incoming 可以使用这些冻结接口继续完成完整安全入纤维的比较。
