# 739 七列路线：独立对抗审查

任务：`fa6b15e`；审查目录归属：agent 104 / review-adversarial。

**当前结论：未发现限定定义域内的数学反例。已对固定源码实际重建投影、逆枚举、通用秩证书框架、最后一步桥接及终端障碍；尚未接受完整 739 深度 39 定理或无条件的 alltime196 推论。** 后两者仍需要具体完整证书检查、初始集合覆盖、短边界检查和轨道组合的最终 Lean 证明。

## 精确假设及审查意见

| 项目 | 必需条件或义务 | 审查结果 |
|---|---|---|
| 正整数 | 起点 `A > 0`；零不能用于 `T(n)>n` | 独立反例：`T(0)=0`。当前最后一步桥接保留正数假设。 |
| 规范数位 | 数位在 0–9、精确正长度、最高位非零、数位值等于整数 | 去掉规范性时，低位在先的 `[1,0]` 会把整数 1 的反转错误地当成 10，得到 11 而非实际 `T(1)=2`。`Canonical` 已明确这些条件。 |
| 原始和字 | 非空、对称、每项≤18、外项>0、奇长中心偶数 | `Admissible` 完整表达；单字 `[1]`、五位 `73937` 的中心 9 不可作为实际原始和字。 |
| 长前缀 | `0<k≤L`；高侧内进位取实际 `carry q (L-k)` | 已审查 `actual_forwardPrefix` 和 `actual_mem_prefixPredecessors`；不要求两端七列不重叠，因此覆盖 7≤L≤13；L=k 时内进位为0。 |
| 逆枚举 | 枚举所有本地进位；末列高侧进位必须存在；外部源和必须正 | `LongCompatible` 与可执行列表双向等价；实际步骤的覆盖另由 `ActualPrefix` 提供，二者没有混淆。 |
| 零首项目标 | Python 逆枚举不能声称对零首项也精确等价 | 独立诊断：Python `prefix_predecessors((0,))` 含 `(9,)`，其真实完成词只能输出 `(18,)` 或 `(10,)`。证书节点首项>0，故不影响冻结证书；Lean 增位分支额外要求 `0<v` 并证明零首项无前驱。 |
| 短至长边界 | 长度1–6记录完整状态；真实规范化长度仅L或L+1；唯一越过七列阈值的是6→7 | 完整独立整数构造检验10467个短词，其中六位词6498个、增位3429个。`shortWords_complete` 和 `nextWord_wordOf` 语义正确。 |
| 最后一步 | 正源、规范目标、目标回文、最高位>1 | `PalindromeBridge` 先证明不增位，再调用无进位回文引理；没有把“同宽”偷偷当作前提。若删掉最高位/不增位限制，29→121是反例。 |
| 表查找 | 不能仅信任字编码单射、树排序或生成器 | `lookupKey` 命中时比较完整字；`lookup_all` 将成功查找接到整树断言，设计保守。 |
| 图中深度 | 每个实际反向边必须在枚举中，每个枚举前驱必须被查到且秩下降 | 通用 `backPath_rank` 已重建。具体739表的完整 `CheckedRows` 尚未在本审查中接受。 |
| 回文深度39 | 目标回文最后一步得到初始字；其前方链长≤38；最后一步再加1 | 必须在最终组合中处理 t=0、短目标及全部初始四位尾数。仅声明通用框架不等于该结论。 |
| 196全时刻 | 统一祖先界39，加上有限初段无回文 | `no_196_739_palindrome_of_ancestry_bound39` 明确以祖先界为前提，语义正确但仍为条件定理。独立整数计算确认0至39均非回文。 |

## 独立 Python 诊断

运行命令（仓库根目录）：

```text
python proofs/contributions/agent-104/seven-column-kernel/review-adversarial/probe_independent.py
python proofs/contributions/agent-104/seven-column-kernel/review-adversarial/check_rank_transport.py
```

两项退出码均为0。脚本内限制 CPU/地址空间；未重复原作者的一百万整数扫描或完整逆图重算。

`probe_independent.py` 的预期侧完全自行实现整数取余数位、规范整数构造与整数反转。对前缀 `s`，用实际可实现完整和字 `s ++ [0,0] ++ reverse(s)` 与 `s ++ [18,18] ++ reverse(s)` 构造两个整数，再直接计算 `n+reverse(n)`。它不调用待审程序的 `normalize`、`F` 或正向列公式来生成预期答案。

- 宽1、2、3：穷尽全部合法来源及目标，各18、342、6498个；逆枚举集合与独立实际整数完成词的边集完全相等；边数27、513、9747。
- 宽7：2916个针对0、9、18及外项1、9、10、18的阈值来源，核对正向输出和逆枚举覆盖。
- 全部10467个短可实现词由独立构造的真实整数核对。
- 冻结证书抽样282个目标、389条长逆边，包括最大初始秩和终端前三项(1,9,6)。
- 1至50000的整数控制，11115个回文输出，其中11000个不增位；所有不增位输出满足“源和字=目标完整数位”。
- 196轨道0至39直接复算，末项为7197630720180367016。

`check_rank_transport.py` 只检查数据搬运：独立解析16个 `Rank739DataNN.lean` 文件的树表达式，按 `Rank739.lean` 指定根遍历，确认全部58501个可达节点的“完整字、秩”多重集与冻结JSON精确相同，且每个完整字均能查回其秩。此步骤没有核验前驱闭包，不能当作证书接受。

完整输出：`probe-results.json`、`rank-transport-results.json`。两文件记录源哈希；stdout、stderr也已保留。

## 固定源码与实际编译

工具链：Lean 4.19.0，commit `6caaee842e94`。工作目录：`/workspace/scratch/7649db1e242c/build104-adversarial`。标准命令：

```text
LEAN_PATH=/workspace/scratch/7649db1e242c/build104-adversarial /workspace/scratch/7649db1e242c/toolchain/lean -j1 -o MODULE.olean MODULE.lean
```

每模块进程限CPU50秒（硬限55秒）、墙钟58秒、虚拟地址空间4GiB。每次确切命令、退出码和耗时存于 execution JSON。

| 模块 | 已实际执行的源码SHA-256 | 结果 |
|---|---|---|
| PrefixCertificate | `3ec68f313c6e48a8641e4456a5a0a3e5e8ff61f95f4919ad60a7c2736a2f7943` | exit 0；通用路径秩定理 |
| PalindromeBridge | `6c1de8cf02ec9381e80388e6b4915db6cfa4d1189d3e47c273400f0d37948093` | exit 0；最后一步及条件196结论 |
| PrefixInverse | `0a93622752fa22cf6c8de2efc8500dc313498d59831bb0e5381b3b351e0ab03e` | exit 0；含(1,9,6)无前驱 |
| ActualPrefix | `c136216ed9c4100a268643be9a471b6746320f63d0af2030b6418429e5551e76` | exit 0；实际长前缀覆盖 |
| TerminalObstruction | `72a302ffe955315e0727d70a125da9da411df4b295a7edc53231152984724e47` | exit 0；全宽实际(1,9,6)障碍 |
| ShortBoundary开发中快照 | `e3f2ed488efc4c55a6d5b1096675cced343cb7f3cf80c3fd6de4102df4139469` | exit 1，37.538秒时内部OOM；未声称重建通过，待作者最终版本 |

通过模块所列关键定理的 `#print axioms` 仅含 `propext`、`Classical.choice`、`Quot.sound`，没有 `sorryAx`、`Lean.ofReduceBool` 或外部可信oracle。

基础 `LychrelDigitSums` 没有在此审查中成功从头重建：3GiB及4GiB地址空间限分别触发bad_alloc/OOM；另一次尝试工具链 `-M1536` 被拒为未知 `max_memory` 配置。失败记录完整保留。随后明确复用既有 `build104-base/LychrelDigitSums.olean`，其SHA-256为 `69dc2ddcd2c17246e2c60ed61195436cc9aefff662f0c49eb769f94baec93978`；同目录源码与固定审查源码逐字节一致，源码SHA-256为 `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57`。因此上述“实际重建通过”只指新增模块，基线独立清洁重建由另一审查承担。

`snapshot-01` 是作者仍在开发时截取的历史状态。其ActualPrefix存在两处carry索引化简错误、ShortBoundary计数存在未闭合目标；已及时反馈。这些错误不代表本表已重建通过的最终投影版本失败。`snapshot-02` 保存修正后的已审查源码。

## 接受闸门

当前接受的是已固定并实际编译通过的局部模块及其准确语义。以下各项未完成前，禁止把本报告写成“739完整定理已通过Lean”或“alltime196已无条件通过”：

1. 具体739全部树行的内核 `CheckedRows` 证明。
2. 全部10000个长初始字与唯一短初始字的查表/最大秩覆盖。
3. 全部短来源的真实后继不落入证书所需集合，或等价的完整短边界处理。
4. 从任意正整数祖先链到投影反向路径的完整组合，含t=0及最后一步+1。
5. 最终定理的依赖审计与清洁编译结果。

本审查不支持完整P196猜想；即使上述739闸门全部完成，也只排除739开头的回文目标。
