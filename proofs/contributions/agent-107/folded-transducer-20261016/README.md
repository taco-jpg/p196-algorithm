# Agent #107：完整 folded transducer 认证

任务：`agent107-folded-transducer-20261016`。协调认领提交：
`fe5a0ef1760a0afa936168ac1cfc52987d28b451`；原始主干快照：
`98d59927ad89c42f438ea857ec5750a0df3b91db`。
唯一外部协作线程为 [issue #61](https://github.com/taco-jpg/p196-algorithm/issues/61)，
认领、源码发布和远端回读由 Agent #107 root 统一代传。

本贡献将原 Python `fst_graph` 的两个初态、完整进位转换、中心终止和输出规则，
接到原 Lean `FoldedDecimal.nextColumns`、实际 `nextWidth` 与普通正整数的
`Lychrel196.step`。成果包括完整有限路径及表索引历史的存在与唯一性、接受输入的
合法重建、真实整数一步实现，以及字面图表的双向完整性。固定图表含 **46 个状态、
872 条边、251 条终止行**；所有状态恰好是从两个初态经有限次 `Transition` 可达的状态。

## 当前检查与发布状态

全部 **11 个新数学模块**及完整基础已由独立审查员从空目录起步重编译，实际使用
Lean 4.19.0 `--trust=0 -j1 -DElab.async=false`，全部退出 0。最终独立状态为
`INDEPENDENT_CLEAN_REBUILD_AND_AXIOM_AUDIT_PASS`，证据位于
`semantic-review/clean-rebuild-20261016T214242.588596Z/manifest.json`。
Graph 已冻结并纳入该重建，不再保留未检查的数学 WIP。

新源码有 407 个显式 `theorem` 声明；按实际来源模块进行的完整审计覆盖 551 个
theorem，计入 private 与自动生成证明。它们不是 551 个手写数学结论。
实际公理分布：206 个无公理，204 个仅 `propext`，139 个为 `propext` 与
`Quot.sound`，2 个还使用 `Classical.choice`。后两者恰为 Graph 的
`accepting_indexed_exists`、`admissible_unique_history`，用于从有限表成员见证选取
索引。完整清单见 `semantic-review/independent-audit-summary.json`。

注册表保持 `catalogue_complete: false`，仅覆盖本任务。生成注册表不是执行原
canonical verifier；其正式运行和发布结果须另按实际执行记录说明。
全部 11 份冻结数学源现已发布到精确源码 checkpoint
[`f0fddaf7baf6131a6d92210ce00189c5532c7825`](https://github.com/taco-jpg/p196-algorithm/commit/f0fddaf7baf6131a6d92210ce00189c5532c7825)，
root 已逐个 Git blob 远端回读且全部匹配。这个 checkpoint 是数学源码阶段；完整证据、
注册表与本文随后由 root 发布，并在 issue #61 记录新的提交与回读。
旧的、仅到 Path 的早期 checkpoint 不再作为全部数学源码的发布依据。

## 精确来源与复用边界

| 来源文件 | Git blob | 本任务复用内容 |
|---|---|---|
| `proofs/creative_regular_direct__8988fd8c6a0aad92.py` | `5658e577de22431ee029cf49c2ff640321dc0d8a` | `fst_graph` 的状态顺序、两初态、边与逐对输出公式 |
| `proofs/persist_spacetime_weighted__d53dd1c09dcfc34a.py` | `8274715ce60ab084b602a08184ed909ee41a1f28` | 中心终止行、额外输出对、输出中心及实际有限路径语义 |
| `proofs/creative_regular_invariant__ea923cdb26a39825.py` | `fa334ba0f094998c206f1eccc529b375c1c5351b` | 上述 Python 的原始公共依赖，独立提取时一并核对 |
| `proofs/Lychrel196Research__c696e0ea3db39d92.lean` | `c6c1f5441c54a36f2d82b3ef78dff1ccdbc5a506` | 原十进制定义、折叠进位迹、有效字实现与数值表示保持定理 |

原有证明的声明来源保持不变。Path 直接复用
`even_folded_trace_sound`、`odd_folded_trace_sound` 和延迟更新定理；Input 复用
`valid_word_realizable`；Output 复用 `folded_emission_*` 与奇偶中心公式；Numeric
复用 `representation_next`、`NormalizationBridge.canonical_admissible`。
`baseline/` 保留基础源的独立重编译，以及七个重点复用接口的公理和直接依赖审计。

图表作者的 `table-development/generate_tables.py` 生成可审查的 Lean 字面数据，
而数学正确性由 Lean 中一般性的表可靠性、完整性和去重定理给出。独立审查员另写
`semantic-review/compare_literal_table.py`，重新执行原 Python AST 并解析实际 Lean
字面列表，不导入作者生成器或 `extracted-tables.json`；其逐项有序匹配结果见
`semantic-review/literal-table-comparison.json`。Python 比对是来源核对证据，
不会替代内核对一般性定理的检查。

## Defs：与原算法相同的有限语义

`State` 的五个字段是 `overflow`、`low`、`high`、`delay : Int`、`started : Bool`。
两个初态分别选择最终溢出位 0、1。无溢出分支保留原始 **Int `-1` 哨兵**；
溢出分支初始延迟为 1，后续记录刚读到的高位输出数字。

`Transition s q t` 同时要求输入列和不超过 18、首对列和为正、下一高进位不超过 1、
高位进位关系正确，以及完整状态等于确定的 `nextState`。它没有删掉 `started`
或延迟信息。`Terminal` 检查已读过一对或存在正中心；偶宽要求两侧进位会合，
奇宽还要求中心不超过 18、中心为偶数、中心进位正确。

`Accepts L q p` 使用状态函数 `p : Nat → State` 的前缀：初态 `p 0`、恰好
`L / 2` 次成对转换和 `p (L / 2)` 的终止条件。`finitePath` 将这段轨迹明确存成
长度 `L / 2 + 1` 的 `List State`。`Word` 由有限 `pairs` 和可选 `center` 组成。

## 完整路径、输入重建与输出

### 路径存在和唯一性

`actual_accepts` 对每个 `Admissible L q` 给出真实进位构成的完整接受路径。
`accepting_state_eq_actual` 证明任意接受路径在所有 `i ≤ L / 2` 上与之相同。
`accepting_finitePath_unique`、`exists_unique_finitePath` 把此结论转成实际有限列表
的唯一性与存在唯一性。Graph 的 `accepting_state_unique` 与
`accepting_finitePath_unique_unrestricted` 进一步只要求两个路径都接受同一个 `q`，
不要求该 `q` 未被读取的高半边已经 admissible。

唯一性始终针对被读取的有限前缀。`Boundary.accepted_tail_not_unique` 给出明确反例：
两条状态函数可以都接受同一单数字输入、具有相同 `finitePath`，但其无限尾部不同。
因此本任务不声称整个 `Nat → State` 函数唯一。

### 任意接受输入为何必须先重建

`Accepts L q p` 只读取低半边及可能存在的中心；它本身无法约束 `q` 未被读取的
高半边。Input 定义：

```lean
symmetrize L q i := if i ≤ L - 1 - i then q i else q (L - 1 - i)
```

`reconstructed_admissible` 从任意 `Accepts L q p` 推出重建字的完整 admissibility：
宽度正、最外列和正、有限范围内所有列和不超过 18、镜像对称、中心偶性。
`accepts_symmetrize` 是双向等价；`foldPrefix_symmetrize` 和 `pathOutput_symmetrize`
证明重建不改变任何读取的输入或路径输出。随后 `accepting_input_realizable`
才调用原有有限正整数实现定理。这一步没有偷偷假设原 `q` 已经对称。

### 四种输出情况

设输入宽度为 `L`，末端高位延迟为 `d`，奇宽中心列和为 `c`，低进位为 `a`。
每次成对转换按原 `emit` 公式产生一个输出对；末端规则如下。

| 输入宽度 | 最终溢出 | 末端额外输出对 | 输出中心 | 实际输出宽度 |
|---|---:|---|---|---:|
| `2k` | 0 | 无 | 无 | `2k` |
| `2k` | 1 | 无 | `2d` | `2k + 1` |
| `2k + 1` | 0 | 无 | `2 * ((c + a) % 10)` | `2k + 1` |
| `2k + 1` | 1 | `(c + a) % 10 + d` | 无 | `2k + 2` |

Output 的四个分支定理逐一证明上述规则。总端点 `accepting_output` 对 admissible
输入证明 `pathOutput L q p = foldPrefix (nextWidth q L) (nextColumns q L)`。
奇宽溢出的额外对保持在有限 `pairs` 的末尾，没有丢弃或误当作中心。

### 普通整数的双向一步实现

Numeric 中的 `canonical_step_path` 从每个 canonical 十进制整数表示构造接受路径，
且输出是其真实 `Lychrel196.step n` 的 canonical 表示的折叠列和字。
`canonical_accepting_step` 对任意已给定接受路径保留更强的完整有限输出列和关系。

反向的 `accepting_numeric_realizable` 只假设任意 `Accepts L q p`，得到正整数 `n`、
其 canonical 输入表示，以及真实 `step n` 的 canonical 输出表示；输入折叠字恰为
原 `foldPrefix L q`，输出折叠字恰为原 `pathOutput L q p`。输出宽度严格为重建字的
`nextWidth (symmetrize L q) L`。本结论允许同一个列和字有多个数字实现，不把有限
状态路径唯一性误说成数字实现唯一性。

## 字面图表、精确可达性与索引历史

TablesData 保留原顺序的 46 状态、872 边和 251 终止行。TablesChecks 对每个来源
状态的有限候选使用内核 `decide` 证明；Tables 将逐行结果组合成一般性定理。

- `states_length`、`edges_length`、`terminals_length` 给出准确数量。
- `states_nodup`、`edges_nodup`、`terminals_nodup` 排除重复。
- `edge_mem_iff` 将字面边成员关系与 `Transition`、准确的 `emit` 输出双向对应。
- `terminal_mem_iff` 将字面终止行与 `Terminal`、额外输出对、输出中心双向对应。
- `states_closed` 证明状态表对允许转换封闭。
- `reachable_iff_mem_states` 将状态表成员关系与两个初态的有限转换可达性双向对应。
  每个非初态有明确的前驱、输入列和及内核检查的转换见证。

因此 46 是精确可达状态数，不只是一个足够大的封闭候选状态集合。872 和 251
同时有列表去重及语义完整性支持。

Graph 的 `graphAccepts_iff_accepts` 把具体表路径和代数 `Accepts` 双向对应。
`History L` 保存 `L / 2` 个有限边索引及一个终止行索引。`IndexedAccepts` 仅要求
被索引行的来源、输入、目标与路径匹配，以及终止行的来源、中心匹配；**没有把正确
输出当作接受条件**。`indexed_edge_eq`、`indexed_terminal_eq`、`indexed_output`
从表可靠性推出完整行和输出相等。

`accepting_indexed_exists` 给出每条接受路径的索引历史；`indexed_history_unique`
结合有限路径唯一性与表去重，证明任意同输入的两个被接受索引历史相等，即使它们
附带的无限状态函数尾部不同。`admissible_unique_history` 给出 admissible 字的
唯一索引历史存在性。最终 `indexed_numeric_realizable` 将纯表读取的
`historyOutput` 接到普通正整数及真实 `step n`，无需预设原 `q` admissible。

`History.terminalIndex` 是 0 至 250 的局部终止行号；原 Python `history_path`
将最后一项编码为 `872 + terminalIndex`，所以它的全局坐标范围是 0 至 1122。
两者使用相同的有序边表和终止表，但本包正式声明针对分离的 `History` 记录，
没有冒称已经形式化 Python 列表函数本身。奇宽溢出的额外对进入输出字，不增加
本次输入历史的边索引数。此表示约定已由图表作者及独立审查员分别核对。

## 检查证据与实际分工

| 层 | 作者/执行者 | 主要证据与实际状态 |
|---|---|---|
| Defs、Output、Graph | Agent #107 root | `author/defs-001` 成功；Output 的失败源和日志保留在 `output-001` 至 `output-003`，`output-004` 成功；Graph 首次成功并独立复核 |
| Path | 委派的路径作者 `scope_scout` | `path-development/build-01.log` 失败及源快照保留；`build-02.log`、`build-03.log` 成功；另有边界实例检查 |
| Input | 同一路径作者 | `input-development/attempt-01.lean` 与失败日志保留；`build-02.log` 成功，13 个导出端点审计 |
| Numeric | 同一路径作者 | `numeric-development/attempt-01/` 首次成功，3 个导出端点审计 |
| 三个 Tables 模块 | 委派的图表作者 `lean_runtime` | `table-development/attempt-01` 的失败日志与当时 SHA 保留；失败源已事后重建并精确匹配当时 SHA，详见下文；`attempt-02.json` 三模块全部成功，共 292 个显式定理 |
| Reachable | 同一图表作者 | `reachability-development/attempt-01.json` 成功，共 49 个显式定理 |
| Boundary 与语义审查 | 独立审查员 `semantic_review` | 15 个边界定理；另执行原 Python 与 Lean 字面数据的独立匹配、完整依赖重建及来源模块审计 |

这些是真实委派角色，不冒用其他协作代理的身份。Boundary 由语义审查员编写，
其自身编译记录不会被包装成“另一个作者的独立验证”；图表作者已另从新目录完成
Boundary 的交叉编译与审查，并实际通过。
完整基础与主要证明的独立重建使用审查员独立创建的构建目录，未复用作者 olean。

工具链为官方 Lean **4.19.0**，release commit **`6caaee842e94`**。
作者与独立检查使用 `--trust=0 -j1 -DElab.async=false`。不使用 `sorry`、`admit`、
新增数学公理、`native_decide`、`Lean.ofReduceBool` 或跳过内核检查的承认路径。
标准验证器允许的三项逻辑公理保持原配置；实际三项并集及两处 choice 使用已在文首
逐项交代。定理计数只是审计覆盖量，不能作为数学难度或推进幅度的指标。

独立审计脚本曾出现名称打印类型错误，其失败日志保留；这不是 Lean 数学模块的
编译失败。最终以 manifest 中实际退出码、精确源哈希和审计日志为准，不以脚本
名称或目录名称推定通过。最终审计原始输出为
`all-exported-axioms-extension-3.stdout.log`；独立说明见
`semantic-review/最终独立审查.md`。

图表第一轮执行收到 signal 9；失败日志和当时源 SHA 保留，但原 `/tmp` 同名源文件
后来被覆盖，未当时单独保存。发布前已从保留生成器明确逆转后来的分行、iff 和拆分
编辑，完成**事后字节精确重建**。`table-development/attempt-01-source.lean` 的
SHA256 为 `5119a7e3b109bea4404805350eb4913fbb561411e27fffe65f1804b4dc22440c`，
与原失败执行时记录完全一致；步骤、生成器哈希和比对结果见
`attempt-01-reconstruction.json` 与 `reconstruct_attempt01.py`。它不是当时留存的快照，
原失败日志没有改写。

基础依赖审计的初次工具脚本也因保留字变量名而失败，未当时单独保存失败源码。
`baseline/dependency-audit-reconstruction/` 现保存失败/成功源码、日志及执行记录等
10 个文件。失败源经反向局部变量重命名**事后重建**，SHA256
`ea06f27608a402d7b0bb9cb9a0333f720754e80d9a7ff53b7525ee31d0ae0f4b`
精确匹配当时记录；完整说明见 `failed-initial-source-reconstruction.json`。
这些恢复说明没有修改原基础 manifest，也没有把工具失败转换为证明成功。

## 注册表与复现

`proofs/Agent107Transducer.registry.json` 使用原 canonical verifier 的 schema 1。
每个模块记录真实源路径、SHA256、Git blob 与精确 import 列表。生成脚本
`generate_registry.py` 检查全部冻结哈希，只注册 roots 的依赖闭包；源哈希不符时
停止，不会把变化后的 WIP 源冒充原冻结结果。

```sh
python3 proofs/contributions/agent-107/folded-transducer-20261016/generate_registry.py
```

最终 roots 只需 `Agent107TransducerGraph` 与 `Agent107TransducerBoundary`，因为
Graph 已导入 Numeric 与 Reachable，从而覆盖全部 11 个新模块及完整基础。
生成器不执行数学验证，也不会把注册状态自动改成 checked。
最终注册表已由未修改的原验证器执行一次 `--check-only`，真实退出 0；证据为
`registry-source-check-final/verification.json`，状态明确是
`SOURCE_AND_IMPORT_CHECK_ONLY`，`mathematical_proof_check: false`。
先前仅注册表说明文字不同的来源检查也保留在 `registry-source-check/`。

原验证器为 `proofs/verify_project__214bf7673efe116b.py`，Git blob
`21131b03dfa516eb19a0a7a4df4f2a41020d4db1`；本任务不修改它。完整验证命令为：

```sh
python3 proofs/verify_project__214bf7673efe116b.py \
  --lean /absolute/path/to/lean-4.19.0-linux/bin/lean \
  --registry proofs/Agent107Transducer.registry.json \
  --project agent107-folded-transducer \
  --output /new/empty/evidence-directory
```

必须使用新的输出目录；旧执行不覆盖。原验证器从源码复制构建并审计所选模块的
全部 theorem；`--check-only` 仅检查来源与 import 闭包，不能称为 Lean 验证。
由于本注册表是局部贡献目录，必须显式使用 `--project`，不据此宣布仓库级 PASS。
原验证器自身的报告 `agent` 字段保留原作者信息；实际执行者与独立审查归属由本任务
额外执行记录说明，不篡改原验证器来更名。

编译器、`.olean`、依赖复制目录和运行缓存是可再生成基础设施，不纳入源码发布；
实际证明源码、冻结源快照、失败日志、精确来源和独立审查证据按阶段保留；失败源的
当时留存或事后重建状态须分别按上述说明及相应 manifest 读取。

## 数学范围

本任务证明完整有限转换器与真实十进制一步运算之间的对应关系，并把原 Python
路径使用中的唯一性断言变成有限路径和有限索引历史定理。它没有构造安全闭合语言
实例，没有给出无限接受轨迹，也没有证明 196 或其他固定种子的无限不回文性。
后续若使用本接口构造不变量，仍必须另行证明非空性、真实一步封闭性和回文坏字排除。
