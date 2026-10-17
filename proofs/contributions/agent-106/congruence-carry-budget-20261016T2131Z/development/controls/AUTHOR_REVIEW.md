# Agent #106 控制模块作者检查

冻结源：`proofs/Agent106CongruenceControls.lean`。

- SHA256：`6ef0f20a8a18a0f35264d0007a735aa99b45e0e0f93de1ff865ad708d6cd31f0`
- Git blob：`c95c7591e6363d6671818b208e442bf18da97929`
- 唯一直接导入：`Agent106CongruenceObstruction`。
- 命名空间：`Agent106.CongruenceBudget`。

## 数学范围

本模块核查原文单条人工入口边，而非其后带 ell 参数的整条人工路径。
令 `k = familyIndex R = 7*R/4+1`，`a = familyWidth R = k+2`。
联合定理 `congruence_sparse_entry_controls` 对所有 `R >= 2` 证明源与目标实际整数模 99 均为零、目标严格大于源且小于源的十一倍、真实十进制位宽恰增加一位。
已有进位预算障碍的范围仍为 `R >= 3`，本模块不改变该范围或任何冻结依赖。

## 证明检查

1. 由自然数除法直接推出 `k >= 4`、`a >= 6`，边界 `R = 2` 保留。
2. 尾界对移位参数 `j = a-5` 归纳，基例为 `5939 < 10000`。十的幂每步乘十，线性尾部只增加 990，得到所有 `a >= 5` 的 `990*a+989 < 10^(a-1)`。
3. 使用冻结的 `rho_le` 推出实际目标满足 `10^a <= sparse a < 11*10^(a-1)`。
4. 位宽直接对现有 `DecimalQuantitativeMass.decimalLength` 的除十递归证明：若 `10^a <= n < 10^(a+1)`，则其真实位宽为 `a+1`；未替换定义。
5. 稠密源模 99 由递推式 `dense(k+1) = 10*dense(k)+99` 归纳。目标模 99 使用基础的 `AstraModular.ten_pow_mod99` 和 `rho` 奇偶定义，结论实际对全部自然数参数成立。
6. 入口增长中令 `p=10^k >= 100`。源为 `11*(p-1)`，目标至少 `100*p` 且小于 `110*p`。自然数算术给出 `source < target < 11*source`。
7. 冻结 seed 定理给出源的真实位宽 `k+2=a`；目标位宽 `a+1`，得到精确位宽差。

## 编译与审计证据

- `attempt001.lean` 和原始 `attempt001.log` 保留第一次失败：两处 `Nat.succ` 与加一规范化不足，以及一个已关闭目标后的多余 `decide`；没有补入占位证明。
- `attempt002.lean` 为冻结源码，正式 `--trust=0 -j1 -DElab.async=false` 编译退出码为 0。成功编译原始标准输出为空，保存为 `attempt002.log`。
- `ControlsAudit.lean` 对模块的全部起源定理执行公理闭包审计，退出码为 0。
- 共 37 个起源定理常量，包括 12 个作者公开定理及自动生成／私有辅助定理；公理并集为 `Classical.choice`、`Quot.sound`、`propext`，无自定义或不允许的公理。
- 精确命令、源码哈希、构建路径和依赖哈希见 `compiled-core.json`。

作者检查完成，源已冻结，可交由父代理独立复核。
