# Scan 模块独立语义审查

## 结论与独立性

对冻结源码未发现阻断问题，也没有修改建议。审查者为 `/root/runtime105`，作者为 `/root/structure105`；审查者未编写或修改被审 Scan 模块。本人编写的 Local 依赖不计入本次独立自审。

- 模块：`Agent105DecoderScan9df76b`。
- SHA256：`4e7f3a29e41c3e40adc08326947fe28b5505015f3c68cba67a1cb648318cad1d`。
- 审查范围：两个执行定义、八个公开定理及原 `forward_trace_unique` 的实际声明和证明。
- 同字节副本：`local/scan-semantic-reviewed-source/Agent105DecoderScan9df76b.lean`。

## 执行递归与状态方向

列表为最低位在前。`scan L e a b` 的 a 是剩余区间最低列的入进位，b 是最高列的出进位。一次双端解码返回 `E.low` 作为低列出进位、`E.high` 作为高列入进位；递归处理长度 L 的内部，输出两端包同一 `E.coeff` 的对称列表。两条 Local 方程分别是 `q + a = e_low + 10 * low` 与 `q + high = e_high + 10 * b`，方向与拼接的完整前向列方程一致。

空内部要求 a = b，这是偶宽中心的同一边界进位会合；单列内部要求中心系数不超过 18、为偶数且满足唯一列方程。总宽每次减少二，执行算法是有限递归，不依赖存在性 oracle。

`decodeAtWidth` 只在根部要求 `0 < L`、`h ≤ 1`，并在扫描成功后要求 `0 < digitFn qs 0`。这一外列和值正性与原 Admissible 的物理可实现性条件相同。内部可出现零系数，输入整数也可有零个位，溢出后的低位 payload 也可以不规范或全零。

## 定理核对

| 定理组 | 语义核对 |
| --- | --- |
| `digitFn_wrap_zero`、`digitFn_wrap_last`、`digitFn_wrap_inner` | 读取范围分别对应低端、最高端和内部偏移，末位索引是内部长度加 1，无误。 |
| `wrap_word_conditions` | 同一外系数包装保持有界性和镜像。新总长至少二，任何自身镜像中心必在内部，因此正确转移原中心偶性，不强加外列偶性。 |
| `scan_sound` | 在两端进位为 bit 的前提下，成功给出准确长度、所有范围内系数≤18、镜像和中心偶性，以及覆盖 `0..L` 的 bit trace 与每一列原方程。拼接 trace 的 `C(i+1)=c(i)` 在内部边界上包含 `i=L`，最高出进位另设 b，索引一致。 |
| `scan_complete` | 对任何满足同样完整列方程的有限词，分别处理长度 0、1、≥2；原 exists_wrapDigits 拆解后由对称性证明两端相同，提取实际 c1 与 c(L+1)，用 Local 完整规格恢复唯一边，再递归恢复内部。未假设求解器已经成功。 |
| `decodeAtWidth_eq_some_iff` | 成功当且仅当返回列表长度为 L、原 Admissible 成立、原 output 在 L 位内等于目标 payload、原 carry 在 L 处等于 h。前向通过数字界导出除10递推，再用原 forward_trace_unique 识别真实进位；反向选择原 carry 作为 trace，以 column_equation 和 carry_bounded 调用完整性。 |
| `decodeAtWidth_isSome_iff` | 对 Option 的两分支作穷尽分解，把 some iff 精确转为有限 payload 存在性，未丢失 h、长度、外系数正性或范围内输出条件。 |

## 必须保留的数字域前提

最终两个定理都明确要求 `he : ∀ i, i < L → e i ≤ 9`。这不是多余假设：从 `q i + c i = e i + 10 * c(i+1)` 推出标准十进制商为 c(i+1)，需要余数 e i 在 0 到 9 内。

执行函数本身没有额外扫描并拒绝非法 e 数字，内部 soundness 也只宣称完整方程 trace。例如按现有定义，`e 0 = 10, L = 1, h = 0` 可以返回 `[10]`，但其实际列进位为 1、实际输出为 0。这不是已声明定理的反例，因为 he 不成立；它明确了后续面向任意自然数目标的包装必须由 Canonical 数位或标准取位函数供应 he，不能省略这一前提。该例仅用于说明声明边界，不宣称本次额外完成了 Lean 计算测试。

对真正的目标 Canonical，e 在实际目标宽度内的数字界已满足；溢出时 L 是目标宽度减一，低位数字继承该界，但不需要低位集合本身为 Canonical。

## 结果范围

本模块完成固定源宽度和终端进位下的有限物理 payload 解码。与 Target 的数值桥相接后可得到真实正整数前驱存在性；本模块自身没有输出所有普通整数 digit split，也没有重证 Agent101 的固定 profile 计数、初始回文扣除或任何无限轨道结论。

扫描结果的列表长度是结论的一部分，`digitFn` 的超界补零仅为有限列表解释服务。无关的目标数位函数尾部既未读取，也未进入 theorem 的范围内规格。

## 编译证据与独立验收的区分

已读取作者 `scan/attempt008.json` 和完整 `.log`：真实 Lean 4.19.0 `--trust=0`，退出码 0，耗时约 2.283 秒，日志源哈希与本次冻结字节相同。八个公开定理的公理均在 `propext`、`Classical.choice`、`Quot.sound` 之内；第一个简单索引定理没有公理依赖。

这是作者开发缓存编译。当前报告提供非作者语义审查，不把作者缓存记录冒称为独立空目录重编，也不把读取自著 Local 依赖冒称为非作者自审。全链独立 freshbuild、模块来源和公理审计由 scope105 负责。
