# 620 的十二步具体见证：独立语义与整数审阅

**独立语义审阅和普通整数复算 PASS。** 种子为 `19014942070`，第十二次
普通十进制反转相加得到回文 `62003033030026`，其最高三位为 620。
独立程序以 `divmod` 实现反转，未导入作者发现程序、Z3 或字符串反转。
完整程序、实际命令、资源限制、stdout、stderr 及逐列记录均已保存。

**独立完整 Lean 重建及公理审计也已 PASS。** 11 个模块和最终 ProjectAudit
共 12 条命令全部退出 0；实际来源模块审计覆盖 1,364 个定理，七个公开端点
均属于新 Witness 模块。详细结果见第 8 节和独立验收摘要。

审阅者为真实非作者专员 `/root/strategy_review`。SMT 编码与新 Lean 证明由
`/root` 编写；审阅者只读这些源文件。团队属于同一会话，使用同一 GitHub
账户发布，故这是不同真实角色的独立审阅，不是外部同行评审。

数学源码已发布于 `8f254e9b43bb319a6c43b208cd181ffc005153ec`。本报告的
Lean 独立验收结论须与末节所列实际重建记录一同阅读；SMT 或 Python 的
有限结果不替代 Lean 内核记录，也不单独构成统一上界最优性的完整结论。

## 1. 固定来源与范围

| 对象 | SHA-256 |
|---|---|
| `search_bounded.py` | `372dd79903a67df46f7402f65f9fd7e0bf5b713fecd07e9a8fc2b37f75d83bdd` |
| `search/sweep-001/width11/result.json` | `1fef7118361b91ad70b4ed31a2137ee15e384480bd8b3a1ffafbca4553f56acf` |
| 对应 `query.smt2` | `305cdd7cd21c30680348ce6b416f499af3fc8ffc52600c145dabdefbfd563201` |
| `proofs/Agent104620Witness.lean` | `fb65cab70bf90214691a06904cd93a621d2e0c0edeba13dffc4df9a2b7d645a6` |

协调认领提交为 `b02a458471626627d5e13541acc855f9f4e2edd1`。SMT 编码审阅
针对本轮初始宽度 6..24、步数 12、前缀字符串 `620`；实际候选来自宽度 11。
接口中的 `width=1` 会被 `word_bits>=6` 的断言排除，这不影响该已声明范围。
本报告不将此脚本认证为所有任意 CLI 参数上的通用编码器。

## 2. 可变规范宽度与尾零

令初始宽度为 $W_0$，时间 $t$ 的分配容量为 $N_t=W_0+t$，模型中的
实际宽度为 $W_t$。四位变量 `d[t][i]` 受无符号约束 `0≤d≤9`；所有
`i≥W_t` 的位置都被约束为零，而 `d[t][W_t-1]` 非零。因此每一行表示精确
的正整数规范十进制数位，分配容量不被冒充为实际宽度。

模型要求 `W_0≤W_t≤N_t`，相邻宽度相同或增加一位。实际反转相加满足这些
约束：结果至少为原数，而两个宽度不超过 $W_t$ 的十进制正整数之和小于
$2\cdot10^{W_t}<10^{W_t+1}$。故模型没有通过这一宽度约束漏掉实际轨道。
它也没有假设每一步都增加一位。

`word` 是每个十进制数字占一个 nibble 的编码，整个 bit-vector 并不是该
十进制整数的二进制数值；普通十进制相加由下一节的列方程表达。输入的
低端数字顺序为 `d[0],d[1],...`。`Concat(*row)` 反转全部分配容量的 nibble，
再右移 `4*(N_t-W_t)` 位，恰好移去由原高端填充零形成的低端填充部分。
所得每个 nibble 仍是原始十进制数字或零。

原数的真实尾零不受正性约束排除。反转后，尾零自然成为可忽略的高端零；
代码没有要求反转数仍与源同宽，也没有按反转后的宽度错移数字。此见证在
源时间 0 和 9 确实有尾零，独立 `divmod` 复算核对了这两个边界。

## 3. 全容量列方程、溢出与五位无回绕

每个进位变量是一位 bit-vector，因此恰为 0 或 1；首进位明确为 0。对所有
已分配列 $i<N_t$，模型使用五位等式

\[
d_i+\operatorname{revDigit}_i+c_i
   =d'_i+10c_{i+1}.
\]

左边两个数字均在 0..9，进位在 0..1，故左边在 0..19。两项数字相加的
中间结果至多 18，加上进位后至多 19。右边的乘法 `10*c` 为 0 或 10，
再加数字后也至多 19。两边及所有中间结果都严格小于 $2^5=32$，所以
该五位等式就是普通非负整数列方程，不依赖模 32 回绕来成立。

最终容量外的一位 `d[t+1][N_t]` 等于容量终端进位。如果实际源宽度小于
容量，后面的零填充列仍受同一列方程约束，不能丢弃来自实际最高列的进位。
下一行规范最高位及相邻宽度约束共同确保：无溢出时实际宽度保持；有溢出
时恰多出最高位 1。模型覆盖全部实际宽度与分配容量的关系。

宽度变量为六位。在审阅范围内，所有容量至多 36；转移源容量至多 35。
因此 `W_t+1` 不会在六位上回绕。`N_t-W_t`、`W_t-1` 以及前缀读取时的
`W_t-1-j` 都有相应非负范围约束。乘四的位移量先扩展到整字的位数，
其数值也远小于该 bit-vector 的取值上限；不存在位移量自身回绕。

独立程序在此轨道上额外以普通整数重新构造每一行的填充 nibble 和右移
反转，再核对全部容量列方程。实际最大列和为 19；实际宽度溢出发生在源
时间 3、5、8，即第 4、6、9 次相加。

## 4. 最后一步目标和资源合同

最后的 `word == reversal` 表达相同填充容量下的数字反转不变性；正整数
规范表示已排除了伪造的高端零。前缀约束在 `W_t≥3` 下读取实际最高端
三个 nibble。因此目标是普通十进制回文且开头为 620，不是低端 620，也
不是仅在填充容量的某三个位置出现 620。

模型固定时间 12，没有把 `t≤12` 误当成 `t=12`。它不要求此前没有回文；
后续 Lean 文件和独立轨道复算另外检查了此具体种子的首次回文时间。

发现程序的 `timeout` 和 `memory_max_size` 是 Z3 参数。已只读核对
`run_sweep.py` 另有单进程 25 秒 wall timeout 和整个 sweep 的 330 秒
预算；它没有设置 OS 进程 AS/RSS 硬限制。因此“512 MiB”应表述为 solver
内存参数，不能写成该脚本已经施加全进程 RSS 硬限。宽度 11 的实际报告
记录最大 RSS 为 67,932 KiB，处于 512 MiB 内；这项区别不需要重跑或改动
已冻结的发现记录。

独立复算程序由记录器另外施加 `RLIMIT_AS=268435456` 字节、CPU 软/硬限
10/11 秒、15 秒 wall timeout，只有一个 worker。实际记录耗时约 0.0653
秒，子进程最大 RSS 为 11,264 KiB。原计划的 `1≤A≤10^7` 搜索在启动前即
由父代理取消；没有执行、没有编译搜索程序，也没有用它宣称排除了该区间。

## 5. 独立普通整数轨道

`independent/verify_witness.py` 从固定正种子出发，反复使用
`n + reverse_decimal(n)`。其中反转只使用 `divmod(n,10)` 和普通整数乘加；
Python 整数为任意精度，十进制值没有固定机器字溢出。它先独立生成全部
值，再与作者 JSON 比较，而不是把 JSON 的相邻等式视为假设。

| 时间 | 普通整数 | 实际宽度 |
|---:|---:|---:|
| 0 | 19014942070 | 11 |
| 1 | 26039883161 | 11 |
| 2 | 42178776223 | 11 |
| 3 | 74446563347 | 11 |
| 4 | 148783127794 | 12 |
| 5 | 646504515635 | 12 |
| 6 | 1183019921281 | 13 |
| 7 | 3004319025092 | 13 |
| 8 | 5909528159095 | 13 |
| 9 | 11819046418190 | 14 |
| 10 | 21000510510001 | 14 |
| 11 | 31002012010013 | 14 |
| 12 | 62003033030026 | 14 |

全部十二个等式、十三个宽度、正种子、末值回文、末值最高三位以及各步
列进位均通过。所检查十三项中的回文时间集合恰为 `{12}`。详细反转数、
列和、进位和填充容量见 `independent/replay-001/verification.json`，其
SHA-256 为 `e9e6f81ec5728c7c54c70714861bfd37558d7c61a0a0f47276f20de276182f80`。
实际命令和退出 0 记录在同目录 `command.json`，stdout、stderr 完整保留。

## 6. 七个 Lean 端点的语义

命名空间统一为 `Agent104.Prefix620Witness`。已逐行审阅的七个公开声明：

| 定理 | 精确含义和边界 |
|---|---|
| `exact_trajectory` | `List.range 13` 映射普通 `orbit seed`，精确覆盖时间 0..12 的全部十三项；没有时间偏移。 |
| `twelve_steps` | 普通 `orbit seed 12 = target`，两端是上述固定正整数。 |
| `target_canonical` | `targetDigit i = (target / 10^i)%10` 是真实十四位规范表示；数字界来自模 10，最高位正性和完整位值都检查。 |
| `target_mem_family` | 目标满足既有 `Agent124.PrefixK.PalStarts3 6 2 0`，同时给出普通 `Palindrome` 和最高端 6、2、0。 |
| `first_hit_twelve` | 时间 12 为回文，且对每个自然数 `t<12` 都不是回文，包含时间 0。 |
| `realized_depth12` | 存在正普通整数种子，在准确时间 12 到达上述同一目标族。 |
| `any_uniform_bound_ge12` | 对任意自然数 B，若该目标族对所有正种子和所有到达时间有统一界 B，则 `12≤B`。 |

`first_hit_twelve` 的有限检查是 `∀ t : Fin 12, ¬ Palindrome (orbit seed t.val)`。
`Fin 12` 精确包含 0..11；随后用 `checked ⟨t,ht⟩` 转成所有自然数 `t<12`。
没有漏掉时间 0，也没有仅证明目标族的首次命中而把其他回文遗漏。

`any_uniform_bound_ge12` 的假设为：

```lean
∀ A P t, 0 < A → PalStarts3 6 2 0 P → orbit A t = P → t ≤ B
```

它直接代入 `seed,target,12`，使用已给出的正性、`target_mem_family` 和
`twelve_steps`。该假设与上界模块的 `ancestry_bound12` 完全同形：上界中的
`PalindromeStarts620` 只是同一个 `PalStarts3 6 2 0` 的定义缩写。见证没有
通过另设较弱回文/前缀定义来获得下界，也没有把 B 换成依赖种子的界。

这个模块自身证明具体实现和任意统一界至少为 12；它不包含上界证书。
匹配的 620 上界必须完成其自己的完整内核验收，才能把两份证据联合称为
最优统一祖先深度界。没有最小种子或最小初始宽度的声明。

## 7. 作者证据与独立完整重建

已读取并核对作者 `development/attempt-001/verification.json`、源快照与
完整编译日志。该报告 SHA-256 为
`4c1ad0c435d8221da3075495677aef733896cdb8b6323d71a1abe8d920690120`，
实际退出 0、耗时 0.467800 秒，证据等级明确是 `AUTHOR_INCREMENTAL_ONLY`。
日志中两个纯轨道定理无公理，其余五个声明仅依赖 `propext`、`Quot.sound`。

独立重建使用本专员的 `independent/Agent104620Witness.registry.json` 和
未修改的 canonical verifier `proofs/verify_project__214bf7673efe116b.py`，
其 SHA-256 为 `c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a`。
根模块的真实传递闭包为十个既有模块加新 Witness，共 11 个模块；没有把
不在此传递闭包中的 CodeCert、FastPred、PrefixR 加入或复用其对象文件。

原 verifier 实际命令使用 `-j1 -DElab.async=false`，未额外加入 `--trust=0`；
本次采用完整传递闭包的空目录顺序重编保护项目导入来源。作者的小型根模块
验收另有 `--trust=0`，不把那条增量命令冒充本次独立命令。

全部十一项来源及原 verifier 共十二个发布 Git blob 已实际读取，并与
固定 SHA-256、Git blob、随后建立的独立检出文件逐字节身份核对。独立
detached sparse checkout 的 HEAD 是发布提交
`8f254e9b43bb319a6c43b208cd181ffc005153ec`，tracked 状态干净。原 verifier
从这些来源另建空目录并逐模块编译，没有导入作者 `.olean`。

原 verifier 的历史固定字段 `agent: Agent #1` 保持不变；实际执行审阅者
由独立 wrapper、registry 和本报告记录。完整命令、source linkage、源
快照、每模块日志和 ProjectAudit 记录位于 `independent/lean-replay-001/`。
本节初稿时独立编译仍在执行；实际最终状态将在验收结果中单独补记，不能
由本节的语义 PASS 推断完整重建已成功。

## 8. 独立完整内核验收最终结果

实际独立执行已正常退出 0。未经修改的 canonical 报告位于
`independent/lean-replay-001/canonical/verification.json`，SHA-256 为：

```text
e55bd3eda8af6a5c51c4627b3026b005adabbf947648abaa7169567fccdf5468
```

本专员又逐项读取和核对了该报告、全部十二条命令及日志散列、原 `FILES.json`
中的非对象文件、全部十一份编译源快照和实际发布检出文件。结果记录于
`independent/independent-review-summary.json`。全部来源 SHA 与发布 Git
身份、registry 和实际编译快照一致，没有依赖作者构建缓存。

| 项目 | 最终独立结果 |
|---|---|
| 发布来源 | `8f254e9b43bb319a6c43b208cd181ffc005153ec` |
| canonical 来源状态 | `source_tree_clean=true`，对应实际独立干净检出 |
| 完整传递闭包 | 11 模块，全部编译退出 0 |
| 实际命令 | 11 次模块编译 + 1 次 ProjectAudit，全部退出 0 |
| 按真实模块来源审计的定理 | 1,364 个 |
| 全闭包公理并集 | `Classical.choice`、`Quot.sound`、`propext` |
| 新 Witness 模块的全部定理声明 | 20 个，包含编译器生成辅助定理 |
| 七个公开端点 | 全部归属于实际 `Agent104620Witness` 模块 |
| `exact_trajectory` / `twelve_steps` | 无公理依赖 |
| 其余五个公开端点 | 仅 `propext`、`Quot.sound` |

审计覆盖每个所选源模块的所有定理，而非仅枚举七个公开名称；其余模块的
计数为 LychrelDigitSums 986、PrefixInverse 45、ActualPrefix 65、
PrefixCertificate 33、LongRowsBase 3、FastInverse 32、FastRowsBase 2、
PalindromeBridge 15、ShortBoundary 90、Agent124PrefixK 73。

独立结果读取器最初错误地要求每个公理列表单行显示，因 94 个 Lean 公理
列表换行而报告后处理失败。原始读取器和真实失败记录完整保存在
`independent/parser-attempt-001/`。现已只修正读取器以解析完整括号列表，
并核对全部 1,364 个原始审计头都恰解析一次；修正后实际退出 0。此事没有
改变数学源码、原 verifier、canonical 报告或任何 Lean 验证结果，也没有
触发第二次 Lean 构建。

至此，本包中具体十二步实现、时间 0..11 的无回文检查及任意统一界至少为
12 均有独立完整内核证据。上界证书仍是另外一个项目；它的真实验收状态
由该项目的记录负责。本报告没有增加一个跨项目的最优性合成定理，也没有
宣称最小种子或最小宽度。

## 9. 上界完成后的独立连接核对

随后，`/root/runtime_scout` 完成了独立的 620 上界项目。来源为
[`dc2123ae4a4513acfe75e0a6cd21c3b6a044bec4`](https://github.com/taco-jpg/p196-algorithm/commit/dc2123ae4a4513acfe75e0a6cd21c3b6a044bec4)，
对应 [PR135](https://github.com/taco-jpg/p196-algorithm/pull/135)。该执行的
原 canonical 报告 SHA-256 为
`52992057d5f3051a6db6413ed724375e06f903ef8ea78a145ef23693f2edba30`，
外层真实来源和执行报告 SHA-256 为
`f044307147ccd1541aea7b0a537ca05347bf0100f5aafa50433332a7809a5a36`。

本专员实际读取这两份报告、来源连接文件和完整 `ProjectAudit.log`，核对
523 个源模块、524 条命令全部退出 0、3,047 个审计头全部解析及标准三公理
并集。还逐一比较了两项目共有的十个依赖模块，发布 Git blob、SHA-256 与
各自实际编译快照均相同。其中 `Agent124PrefixK` 的 SHA-256 是
`7b9de533a36b5cb684c5a751940af5a98150ea6dba6519fe5a11651933171314`，
因此两端不会因同名模块的版本不同而更换 `PalStarts3` 或普通 `orbit`。

结合已经分别完成的两份定理，**该精确目标族的最优统一祖先深度界为 12**：
`ancestry_bound12` 给出统一上界 12；本包 `any_uniform_bound_ge12` 证明
任意满足同一全称合同的自然数界都至少为 12，具体种子确实实现时间 12。
这是已核对陈述和来源后作出的数学合成结论；本包没有新增一个同时导入
两项目的 Lean 合成模块。见证重编没有包含上界的 523 个模块，上界重编
也没有包含见证。原已冻结的 620 审阅在当时写明独立重建尚未完成，那个
历史文件保持不变；完成后的真实状态由本节和新的执行报告补充。

上界 raw report 原有 `source_commit=2eb05ef...` 和
`source_tree_clean=false` 对应旧布局重放环境，保持原样。它的真实数学
来源由外层 `published_source` 和逐模块 Git 来源连接给出。见证 raw report
则来自直接建立的干净发布检出，记录 `source_commit=8f254e9...`、
`source_tree_clean=true`。两种执行布局的字段没有被修改成表面一致。

见证相关的九个发现/作者证据 blob 又从发布提交实际读取，与审阅文件逐字节
一致；该检查不复用作者的数值算法。全部指纹和上述跨项目来源连接保存在
`review/source-pins.json`，SHA-256 为
`749423a43cb3501a3bb9a9735b456253e8cae987982a7922582071d8e20429fc`。
实际程序和成功日志在 `independent/verify_review_links.py`、
`independent/link-check-002/`。首次受限执行的 Git 读取返回 128，其失败
日志与原程序留存在 `independent/link-check-001/`；在允许读取已发布 Git
对象的执行环境中，同一程序随后通过。两次都未调用 Lean 或求解器，未
改变任何原始 canonical 报告。

可移植的整数复算、空目录 Lean 重建和完整报告读取命令见
`review/REPRODUCE.md`。最终发布清单和所有文件指纹由
`review/PUBLISH_REVIEW_FILES.txt`、`review/reviewer-freeze.json` 固定。
