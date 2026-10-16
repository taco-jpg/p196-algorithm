# Target 模块独立语义审查

## 结论与身份

未发现阻断问题，也未要求修改冻结源码。本审查由 `/root/runtime105` 完成；被审模块由母代理编写，审查者没有编写或修改该模块。本报告不把本人编写的 Local 或上一阶段 WidthSupport 计入独立自审。

- 模块：`Agent105DecoderTarget9df76b`。
- 冻结源：`proofs/Agent105DecoderTarget9df76b.lean`。
- SHA256：`2c2cbf18088e0a281ff78547cc3b2aa465050504c9139fc2839fb70e86db7c9d`。
- 审查时读取当前字节并核对哈希；同字节副本保存在 `local/target-semantic-reviewed-source/Agent105DecoderTarget9df76b.lean`。
- 范围：两个定义、四个公开定理、所调用原基础定义与主要数值桥接接口。未修改作者源码或 Git 状态。

## 精确数学范围

`PayloadSpec e L h q` 包含原 `Admissible L q`，加上所有 `i < L` 的 `output q i = e i` 及 `carry q L = h`。原 `Admissible` 的五项条件是 `0 < L`、`0 < q 0`、实际范围系数不超过 18、镜像对称，以及实际中心系数为偶数。这足以经原 `valid_word_realizable` 构造一个真实正整数及其规范 L 位数字，并保留所有范围内列和。

`WidthChoice e W L h` 精确区分 `W = L ∧ h = 0` 与 `W = L + 1 ∧ h = 1 ∧ e L = 1`。`Canonical Y e W` 给出正的实际目标宽度、受界数位和非零最高位。该前提排除零目标；`Admissible` 排除空输入宽度与零列和词。任何更宽的零值接口均不是这四个定理当前宣称的范围。

溢出分支只要求额外最高位为 1，没有要求移除最高位后的低 L 位自身是规范数。此处正确保留前导零乃至全零 payload；例如 `step 5 = 10` 在 `W = 2, L = 1` 的低位是 0。未来 Scan 包装不得额外拒绝这种输入。

## 四个定理逐项检查

| 定理 | 已核实的语义和证明路径 |
| --- | --- |
| `payload_congr` | 只替换 `i < L` 的 q 值。原 `admissible_congr`、`output_congr_upto`、`carry_congr_upto` 分别保持可实现性、L 个实际输出位与最终进位。无需函数无限尾部相等。 |
| `realize_payload` | 从 Admissible 构造 `n > 0`、`Canonical n d L` 和范围内列和保真。经原 `step_eq_word_value` 与 `value_output` 把实际 `Lychrel196.step n` 化为目标低 L 位加最终进位，再由 WidthChoice 和目标 Canonical 数值等式得到 `step n = Y`。结论具有真实普通整数语义。 |
| `canonical_predecessor_payload` | 对一个已给定的规范实际前驱，使用 `step_width_cases` 得到唯一对应的宽度/进位分支；以原规范下一步数字和目标同宽数字的唯一性取得范围内输出相等。溢出最高位的 1 从实际 `extended` 与最终进位得到。没有将归一化后的下一列和词误当作目标数字。 |
| `positive_predecessor_iff_finite_payload` | 正向用 `List.ofFn (Fin L)` 精确保留 L 个实际列和，并由 `Agent101.digitFn` 恢复范围内函数；反向调用 `realize_payload`。长度证据在反向未被单独使用是正常的，因为 PayloadSpec 已按 L 约束所读取位置；存在量词仍准确给出有限长度 L 的证书。 |

## 解释边界与后续连接条件

这组结果是给定规范目标和固定输入宽度 L 的数值前驱存在等价，尚未自行断言任何可执行扫描函数会找到该有限证书。完整 decoder 的接受 iff、失败 iff、枚举条数或具体前驱计数需要后续 Scan/包装定理；本模块没有宣称这些尚未连接的结论。

`q` 是输入数字的列和词，而 `e` 是真实输出数字。`q` 与 `e` 的函数尾部没有参与对应宽度内的数值解释。有限化采用超界补零的 `Agent101.digitFn`，没有添加无限尾部一致性假设。

显式 `0 < n` 与 `Canonical n d L` 在存在结论中同时出现符合接口目的；虽可由规范性推出正性，并不引入不当限制。只有被给定的目标 `Canonical` 用于数值重组和规范唯一性；未假设任意溢出低位 payload 的规范性。

## 核验记录的区分

已读取作者 `target/attempt002/result.json` 与完整 `compile.log`：原 Lean 4.19.0、真实 `--trust=0 -j1 -DElab.async=false`，退出码 0，记录哈希与冻结源相同；四个公开定理的打印公理均为 `[propext, Quot.sound]`。这是作者开发编译记录。本报告提供非作者语义审查，不将该记录描述为独立空目录重编。独立全链 freshbuild 和 module-origin 公理审计由 scope105 负责，避免重复构建基础模块。

## 所检查的本地依据

- 当前冻结 Target 全文及作者成功编译记录。
- 原基础 `Lychrel196Research__c696e0ea3db39d92.lean` 中 `Canonical`、`Admissible`、`valid_word_realizable`、`value_output`、`step_eq_word_value`、范围内 congruence 与 canonical_admissible。
- `Agent101NumericFibers.lean` 中超界补零的 `digitFn` 定义。
- 既有 `Agent105WidthSupport9df76b.lean` 的 `canonical_digits_unique` 与 `step_width_cases`。读取这些依赖是核对 Target 的调用语义，不构成对本人所著依赖的新独立验收。
