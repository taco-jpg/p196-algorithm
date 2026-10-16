# FamilyRatio 交付

固定源码 `Agent108WindowFamilyRatio.lean` SHA256：`051dcb42849d9cffb2fec0de77af138b6d7d6c415ff27d65725dcdf9cfcf7afc`。完整模块已真实 --trust=0 编译 exit 0，5 条公开定理和 6 条私有桥的传递公理仅为标准三公理。首次完整编译即通过；前两轮独立代数前置检查也已保留。父代理负责非作者的整链独立重建。

namespace 为 `Agent108.WindowWeights`。窗口宽度 b+1，物理缓冲 B=b+c，所有 b,c,k,r 均为任意 Nat。

`localBeta b psi` 定义为 windowProduct b psi (localBlock b true) / psi(buffer(b+1))^(b+4)，与 FamilyProducts 的 blockProduct true 分子定义等价。`localBeta_pos b psi hp` 证明其严格为正，只用 PositivePotential 的合法窗口前提。

公开接口：

- `targetHalf_weight_pos b c k r psi hp`：目标 windowProduct 严格为正。
- `blockProducts_binary_factor b psi es hp`：块乘积等于 q^((b+4)*es.length)*binaryWeight(localBeta b psi) es。
- `inputHalf_product_ratio b c k psi es hp`：源 windowProduct 等于 endpointConstant b k psi * targetHalf(b+c,k,es.length) 的 windowProduct * binaryWeight(localBeta b psi) es。
- `inputHalf_exact_total b c k r psi hp`：按 choices r 的 List 求和，精确等于 endpointConstant b k psi * targetHalf(b+c,k,r) 的 windowProduct * (1+localBeta b psi)^r。

取物理缓冲 B=4*(b+1) 时，使用 c=3*b+4，随后用自然数环恒等式重写 b+c。choices r 为 List(List Bool)，现有 choices_mem_length 与 choices_nodup 可用于 finite-index 桥。

若固定 r 的额外宽度权重已统一成实数标量 s，可使用现成 sum_map_real_mul 与 inputHalf_exact_total 将其提出总和，再用 ring 重排为 C*(s*targetProduct)*(1+beta)^r；这个标量等式本身不要求 s 为正。该步骤应在实际来源/目标宽度一致性被证明后接入。

完整快照、日志、依赖哈希与执行命令见 full-attempt01/ 及 family-ratio-verification.json。
