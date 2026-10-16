# FamilyProducts 独立复核

结论：PASS。复核者为 semantic_scout，未参与 `Agent108WindowFamilyProducts.lean` 的编写，本次未修改作者源码。

## 固定对象与真实重建

固定源 SHA256：`d4449500c98887a82dca222af318e8d99e8ef0d1ad5e58719658406c1650fdc8`。

从新建的空 `build/` 顺序编译精确快照：Defs、Products、Weights、FamilyProducts。编译前的 LEAN_PATH 仅包含这个新 build；固定 wrapper 追加 Mathlib 与其精确依赖缓存，没有引入其他 Agent108 构建目录。四模块与最后的独立公理审计全部 exit 0，均使用 `--trust=0 -j1 -DElab.async=false` 和正式 require_escalated 执行。

审计覆盖四模块全部 32 个公开声明，包括 FamilyProducts 的定义 `blockProduct` 及其 8 条公开定理。所有声明只依赖 `propext`、`Classical.choice`、`Quot.sound` 的子集。完整命令、源/依赖哈希、逐模块 stdout/stderr 与全部公理列表见 `verification.json` 和 `logs/`。结束时再次读取作者文件，其哈希仍与快照完全一致。

## 语义约定

令窗口宽度为 b+1，物理缓冲长度 B=b+c，q=psi(9^(b+1))，n=es.length。这里重复幂表示字母重复，数值 q 的幂表示实数乘幂。所有 b,c,k,r 都是任意自然数；因此 B>=b，且全部非负额外缓冲 c 都被覆盖。窗口只保留完整窗口，不添加边界填充。

## 逐声明复核

| 声明 | 精确语义及审查结论 |
|---|---|
| blockProduct | 对实际字 9^b ++ block e ++ 9^b 使用窗口宽 b+1，与定义 localBlock 完全一致。 |
| blockProduct_pos | 仅用合法窗口正性；两种实际块的字母分别为 9 或 14,14,4,4，加上缓冲 9，全部 <=18。 |
| blockProduct_false | 全九字长度 2b+4，完整窗口恰有 b+4 个，故为 q^(b+4)。 |
| prefix_buffer_product | [a]9^(b+c) 有一个含 a 的首窗口，后接 c 个全九窗口，因子为 psi([a]9^b)*q^c。a 无需合法性假设，因为这是无条件乘积等式。 |
| block_buffer_product | 局部块后增加 c 个九产生恰好 c 个全九窗口，因子为 blockProduct*q^c。 |
| blocks_buffer_product | 对 9^b ++ blocks B es ++ [a]18^k，每个块贡献局部乘积及 c 个额外全九窗口，故公共因子 q^(c*n)，并留下 endpoint b k a。 |
| assembledHalf_product | 额外初始缓冲再贡献 q^c，合成 q^(c*(n+1))。首字母和尾字母均保留为任意 a,z。 |
| inputHalf_product | 精确实例化 assembledHalf 的 a=5、z=14；与 Defs 的实际 inputHalf 定义直接一致。 |
| targetHalf_product | 原目标九字串长度 r*(B+4)+B+1；置 N=r*(B+4)+c 后等于 9^(b+N)[9]。空块 assembledHalf 给出 q^N 和 endpoint b k 9。 |

## 边界与指数

- r=0 / es=[]：输入公式变为首窗口乘 q^c 乘 endpoint 14；目标公式变为首窗口乘 q^c 乘 endpoint 9。不存在零块时遗失的初始缓冲因子。
- c=0：所有额外缓冲因子为 q^0=1，证明不需要 q 非零。
- b=0：窗口为单字母窗口，重叠缓冲为空；上述各式退化为逐字母乘积，局部块含恰好 4 个窗口。
- k=0：端点仍含一个完整窗口。目标末尾的额外九属于 endpoint 9，未被错误吸收到公共 q 指数中。
- k<b、k=b、k>b：该模块将尾端原样交给 endpoint；没有引入 k>=b 或其他中心长度前提。

总窗口计数提供一致性检查。输入完整窗口数为 n*(B+4)+c+k+2；因式分解贡献 1+c*(n+1)+n*(b+4)+(k+1)，二者相同。目标贡献 1+[r*(B+4)+c]+(k+1)，同样等于实际完整窗口数。

源与目标长缓冲因子的对齐是自然数恒等式

    c*(n+1)+(b+4)*n = n*(b+c+4)+c.

各分解均借助长度恰为 b 的共享九缓冲使用已独立核验的窗口重叠定理；共享缓冲自身长度小于 b+1，不额外贡献完整窗口。对重复九缓冲的重新结合与合并没有交换异种字母的次序。

## 结论范围

该固定模块完整实现了要求的有限窗口整词乘积接口，语义和核验均通过；无需源码修正。实际 reverse-add 转移、来源注入及数值半字编码由 Embedding 接入，另行复核。
