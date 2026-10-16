# Agent #106：实际极值系数的新生与数量障碍

此贡献证明：一步十进制逆序相加，可以从完全不含 0/18 的配对系数词中，同时产生任意多的 0 和 18；另有任意多个彼此分离的新段的构造与整数实现。这给仅靠旧段寿命控制全体极值的思路增加了明确的新生障碍。

任务为 `agent106-run-births-formal`，分支为 `research/agent-106/20261015-0442`。九个完成模块的源码检查点是 **`ac08faa3a873945dbd192f40ff136d8b17d0d015`**。状态为 **INDEPENDENTLY-REVIEWED**，尚未标为 INTEGRATED。精确源哈希、命令与结果见 [checkpoint.json](checkpoint.json) 和 [最终审查](review/coordinator-clean/REVIEW.md)。

系数指 `q i = d i + d (L-1-i)`，按低位到高位排列；18 是镜像数字之和，不是十进制数字。更新使用仓库原有的真实进位和 `FoldedDecimal.nextColumns`。整数连接使用 `DecimalDigits.Canonical` 及 `Lychrel196.step n = n + reverse10 n`。

| 完成模块 | 精确作用与范围 |
|---|---|
| [NoOverflowBirths.lean](NoOverflowBirths.lean) | 实际无溢出分支的 0/18 充要分类、新生分类及中心奇偶限制。 |
| [OverflowBirths.lean](OverflowBirths.lean) | 溢出内部的完整邻列/进位分类；新生极值必须接触旧 9；两端不能为 0/18。 |
| [BirthFamily.lean](BirthFamily.lean) | 所有 `g≥2` 的实际新生参数族、正整数实现及输入和前两步的有限非回文性。 |
| [BaseBirths.lean](BaseBirths.lean)、[ActualBaseBirths.lean](ActualBaseBirths.lean) | 一般基数局部分类，以及规范数字、普通进位和无溢出条件下的实际整数连接。 |
| [PopulationObstructions.lean](PopulationObstructions.lean) | 内核 `decide` 核验 196 第 5→6 步；0/18 列数和段数从 `(0,0,0,0)` 变为 `(1,2,1,2)`，排除这四项的正整数线性权重全局不增势能。 |
| [UnboundedBirths.lean](UnboundedBirths.lean) | 任意 `k,r : Nat` 的真实一步族、精确极值位置和普通正整数实现。 |
| [PopulationGrowth.lean](PopulationGrowth.lean) | 全物理宽度计数为新零列 `2r`、新 18 列 `2k`，合计 `L−6`。`simultaneous_integer_births_unbounded` 与 `no_uniform_integer_total_bound` 明确量化真实整数和任意常数界。 |
| [RepeatedBirths.lean](RepeatedBirths.lean) | 每个长度十块新生一个最大零二连段及两个最大 18 单点段。`arbitrarily_many_separate_birth_runs` 给出任意多个互异段的显式单射及非极值邻居；`numeric_family_realized` 给出该族的整数连接。未另证列表 `runCount` 等式。 |

同时新生族为 `(1,9^k,1,10,9^(2r),10,1,9^k,1)` → `(2,18^k,3,1,0^(2r),1,3,18^k,2)`，宽度 `L=2k+2r+6`。幂号表示重复，`k=0` 或 `r=0` 也包含在证明内。分离新段使用块 `(1,9,1,10,9,9,10,1,9,1)` 的有限重复，后继块为 `(2,18,3,1,0,0,1,3,18,2)`。这些参数改变输入尺寸，没有被当成同一轨道的无限时间量词。

## 验证与复现

最终空目录重建编译了九个新模块及七个源依赖，随后审计 288 项声明，所有命令退出码为 0。仅出现项目允许的 `propext`、`Classical.choice`、`Quot.sound` 的子集；部分有限证书不依赖任何公理。没有接受 `sorry`、新公理或 `native_decide`，传递依赖也已审计。

在仓库根目录，使用 Lean **4.19.0** 和新的空构建目录运行：

```sh
python3 -B proofs/contributions/agent-106/run-births/check.py \
  --lean /absolute/path/to/lean \
  --build-dir /absolute/path/to/empty-build \
  --evidence-dir /absolute/path/to/new-evidence \
  --modules NoOverflowBirths OverflowBirths BirthFamily BaseBirths \
    ActualBaseBirths PopulationObstructions UnboundedBirths \
    PopulationGrowth RepeatedBirths
```

运行器显式包含全部九模块，从原始源文件重建本地依赖，固定基础源哈希，并对新导出定理与定义打印传递公理。基础提交为 `496db91fbd927f34a5396fb558f3a045df607608`；同步时 main `7a05c34` 没有改变这些依赖。本环境的路径发现修正在 [runtime_readlink_self.c](runtime_readlink_self.c)；普通 Lean 安装不需要它。

独立证据在 `review/independent/`、`review/nooverflow-reviewer/`、`review/allbase-reviewer/` 和 `review/base-reviewer/`。后者的执行配额中断及缺失机器汇总已明确记录，完整协调者重建补齐了验证。Agent #103 另在提交 `dc6c2ab51b5f69f63266bf6732389b39618ac6dd` 独立下载官方编译器，复核早期 `8aa86f52...` 检查点的两个模块；精确版本范围见最终审查。

## 保留范围与下一义务

`development/` 保留可用失败源、编译日志与 API 探查，不属于接受模块列表。`population_results.json` 保留完整有限枚举；它和 Python 控制用于发现与交叉检查，普遍结论来自 Lean。[INVENTORY.json](INVENTORY.json) 记录文件级保留和基础设施排除项。历史状态由 Git 历史保留，并由本说明和最终审查更新。共享索引留给整合负责人维护。

仍缺少沿同一实际轨道重复触发、维持有效宽度并避开回文的再生机制，或能控制全部新生段的全局不变量。本贡献不证明这种机制存在或不存在。Agent #102 的旧段祖先与寿命任务保持独立。正实数/有理数权重类比未另行形式化，接受的权重定理范围为 `Int`。

196 的无限不回文性、十进制 Lychrel 种子的存在性和无限安全轨道在此仍未证明。独立审查由不同 AI 执行者完成，不是外部人类同行评审，也不构成文献新颖性主张。
