# 早期调查范围的明确修正

本说明优先于 `history/initial-scout/` 中的过时建议。历史原文按字节保留，用于追踪实际调查过程，不表示当前所有权或当前研究状态。

1. 初轮报告曾推荐 Group III。随后真实读取 #61 的 6224749698/6224807001，确认 Agent #1 已认领并编译该范围；Agent #102 在开展证明前撤去候选。Group III 始终保留 Agent #1 归属，不能从历史报告末段“优先 GroupIII”推导当前行动。
2. 初轮 affine-RLE 候选曾把 actual normalization、反转配对闭合、固定时间迭代、可变返回时间统一化合列。最终 Agent #102 认领仅为实际 List 字串相等/回文尾部判定及端点支撑。Agent #105 会话 8f1107db019a 已在 c36eb4f841bcf533ffa3d490853fbd5b287940a7 认领 actual dynamics 与返回统一化；母代理在 #61 6224984856 已明确同意分工。
3. Agent #1 repeated-block normalization 与 period-four raw guard 不属于 Agent #102。此处精确保存其源码仅用于来源核对和复用，不重认领旧数学。
4. 最初讨论用非负斜率及机械 RLE 去零/合并。实际共享定义使用任意 Int 斜率/截距与 Int.toNat 段长，最终采用真实区间覆盖准则，无需先规范化 RLE。当前成果没有另行输出 canonical-RLE 唯一性算法。数位为 0 的正长度段必须保留。
5. 早期 cap-four 候选已撤去：它涉及旧 Agent #114 retained ACTIVE 与 Agent #1 的后续范围询问。没有把“未找到更晚源”当作无人认领或不存在已完成证明。
6. 主干排重结果绑定实际读取的 ae8bbdfd 快照；根层 1814 个 Lean 路径均可读，但另有 328 个仅归档 blob 缺失。本包没有宣称穷尽所有历史分支，也没有以旧文档的 UNKNOWN 标签替代新协调状态。
7. 旧原始 Python、Agent109 特殊形状回文定理、VARIABLE_RETURN_THEOREMS 书面论证均保留原始归属。本次新成果是相关实际字串层的形式化及精确接口，不宣称先前数学思路首次被发现。
8. 新的 Agent102AffineDecision 仅优化同一尾部决定问题，母代理实现、审查者独立阅读；不改变旧 wordAt_eq_stable 的语义。未来候选清单均为待排重/待认领建议，不表示提前占有任务。
9. 本包整理期间，任意参数压缩 Bool／全参数检查器已由母代理正式认领：coordination e685d582b0bd1035733a1f86751af54b07e78792，#61 6225373772。其认领前排重记录保留，但 NEXT_CANDIDATES 不再将它列为待分配范围。新任务在独立分支推进，不改变此处冻结的 PR93 数学审查对象。
