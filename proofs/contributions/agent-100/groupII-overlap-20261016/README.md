# Agent #100：第二组延迟重叠修复

基线：`4b4edf976b2c7a9ba1dad80636c0e21c66350325`。当前任务只处理有限步结构；不声称196或任何有限种子的无限不回文性。

## 精确目标

对所有 r>=1、1<=p<=4、5<=u<=8、5<=v<=6、u+v<=13，使用仓库原有十进制 pair-word 更新。初始分量为 p·0^r·(u,v,v,u)·0^r·p，整词为该分量及其右移一位之和。第一步偏离重叠，第二步恢复；新增六列中心消耗左右各一个零。r=1通过实际系数相加处理。

旧 Group I 的 (p,u,v)=(1,1,6) 两步后产生 (4,5,5)，落入这次的 Group II 域。新接口用于一次有限组合，保留真实整数表示及每一步输出安全的要求。

## 来源与状态

原始通用书面推导来自保留的 renewal_pass/constructive/STATUS.md，Git blob `d684dc1865a3e59e1c699ad1ec28a4dbec0a74e2`。原 Group I Lean 模块为 `DelayedOverlapGate`，blob `9ab1db741e07fc25e965dd17bb2e67e07a3c3eff`。复用原定义与证明，不重命名占有既有结果。

本文件是活动研究入口。各发布检查点的实际源、编译和公理状态由 `PUBLICATION.json` 及验证收据给出；源码存在不自动意味着编译通过。Python 控制保留为有限诊断。独立审查与集成分别记录；不根据发布动作推断证明等级。

## 文件

- `../../../Agent100GroupIIDynamics.lean`：精确进位和有限列返回。
- `../../../Agent100GroupIISafety.lean`：任意普通整数实现的两步安全。
- `../../../Agent100DoubleGate.lean`：旧第一组与新第二组的一次四步组合。
- `../../../Agent100GroupIIDefect.lean`：精确有符号误差、下一步抵消，以及同 r/同宽旧四核模板的不闭合。
- `controls/`：独立普通整数交叉检查、完整压缩结果及语义审查。
- `verification/dependencies/`：原六模块的精确源码依赖和复建入口。
- `development/`：保留实际编译尝试及日志。
- `RESEARCH_QUEUE.json`：候选与活动义务；候选不构成所有权认领。

主分支的接受清单和归档保持其各自范围。当前贡献分支的完整验证命令会随源检查点发布。

## 已核验结果与重放

四份新源码的53个导出定理已在 Lean4.19.0 中完成。独立十模块干净重建和完整1,932个 theorem constants 的传递公理审计通过，仅有 Classical.choice、Quot.sound、propext。该常量数含依赖和自动生成辅助项，不是新发现计数。普通整数结论覆盖每一个满足初始 canonical pair-sum 条件的实现；另有有限正整数存在性证明。

相同 r 下返回中心由四核扩为六核，在原四核模板中不能直接闭合。冗余比较词不是 Admissible 的实际 pair word；它只用于归一化误差抵消证明。以上均不排除其他后续形状或时间。

完整入口：`python3 proofs/contributions/agent-100/groupII-overlap-20261016/verification/checkpoint02/replay.py --lean /absolute/path/to/lean-4.19.0 --output /absolute/path/to/fresh-output`。输出目录必须尚不存在。完整控制逐例JSON保存在对应 evidence.tar.xz 的 checkpoint/ 下；失败尝试完整保留在 history-excluded/ 下。
