# Agent #121：合并版模板安全定理复核与边界回归

## 结论与证据级别

本目录是非独占的补充复核，不认领 Agent #109 或 Agent #103 的数学成果。

- **上游源码复核：PASS。** 在独立的空目录内，实际重建了主分支快照的七个相关模块，并检查普通整数语义、有限时间量词及传递公理依赖。
- **新增回归证书：LEAN-CHECKED。** `Agent121ScopeRegression.lean` 包含精确接口检查、实际整数反例及十进制语义哨兵测试。没有外部审查者独立审查本文件，不能将它标成 INDEPENDENTLY-REVIEWED。
- **远程发布：BLOCKED / LOCAL ONLY。** 本次环境未提供 GitHub 写入动作，本地 Git 网络解析也失败。因此没有发布任务认领、贡献分支、提交、PR 或协调更新；没有修改 main。这里的文件与 SESSION.json 不构成远程任务保留。
- **主问题：本次没有得到 P196 的全时间证明，也没有得到新的十进制 Lychrel 存在性证明。**

## 固定输入与实际执行

被复核的 main 提交：`eec3d5f3646cab50abad6e610ea19626cd249070`。
源文件的逐项 SHA-256 和字节数见 `source-pins.json`。七项源码也全部匹配 Agent #103 在
`proofs/contributions/agent-103/review-agent109-step-safety/sources.sha256`
中保留的审查输入，比较结果见 `upstream-reviewer-hash-comparison.json`。

编译器报告为 Lean 4.19.0，发布提交 `6caaee842e94`。本次从仓库已有的 Agent #9 检查器工件取得运行时，并核对工件 SHA-256；没有另行编译 Lean，也没有声称从上游发布站独立下载了另一份编译器。精确来源、工件号、哈希见 `PROVENANCE.json`。

项目模块从源码重新编译，没有复用作者的项目 `.olean`。最终重建使用
`-j1 -DElab.async=false`，七个上游模块、回归模块及审计入口全部退出 0。
标准库随固定 Lean 运行时提供，不使用 Mathlib。

最终显式审计覆盖 99 个上游源码定理和 10 个本地回归定理。
另一个 Lean 环境枚举程序检查了同一命名空间内的 292 个定理常量，包括自动生成的辅助常量。
这些数字是审计覆盖率，不是新数学成果的数量。

所有被检查定理的传递公理依赖均包含于：
`propext`、`Classical.choice`、`Quot.sound`。
这是项目已有的标准逻辑公理范围，没有把缺失数学结论新增为公理。
具体的整数轨迹、首次回文时间、相位边界及十进制哨兵证书均报告不依赖任何公理；
调用上游一般定理的两个接口检查继承上述标准逻辑公理。
未发现 `sorryAx`、`Lean.ofReduceBool` 或其他额外公理。
辅助源码扫描也没有发现生效的 `sorry`、`admit`、`native_decide`、自定义 `axiom`、
`unsafe`、`implemented_by` 或 `extern`。

## 数学含义检查

### 1. 原定理确实作用于普通整数，但只保证指定的正时间区间

`Agent109.NoPalCompat.lychrel_template_orbit_safe` 的输入包括：

- `Phase c`，即 `1 ≤ c ≤ 17` 且 `c ≠ 9`；
- 块 B、A、C 的系数都不超过 18；
- `pairWord n = Agent8.template c B A C g h`；
- `2*k+2 ≤ g` 且 `2*k+2 ≤ h`。

结论是：对 `1 ≤ i ≤ k+1`，
`¬ Lychrel196.Palindrome (Lychrel196.orbit n i)`。

`exact_finite_safety_contract` 用原来的 `Lychrel196.orbit`、
`Lychrel196.Palindrome`、`Agent8.template` 再次检查了这个精确接口。
这里的模板系数是镜像数位之和，不是允许“大于 9 的十进制数位”。
`Compat` 将复制的符号连接到已有的整数定义，`pairWord_step` 证明真实一步运算的对应，
不是把任意符号轨迹当作已经存在的整数轨迹。

`Agent109.NoPal.not_stepPal` 的实际前提只需要 Phase c 和 B、A 的界；
该定理本身不要求 C 有界。普通整数应用仍使用桥接定理要求的完整前提。
其归一化模 9 论证以及互补进位矛盾已通过实际编译核验。
有限迭代证明同时使用精确模板更新和后继块有界性，不能跳过这些桥接义务。

### 2. 合格模板可以在保证区间外到达回文

`terminating_seed_template` 在内核中证明：

```lean
Agent109.pairWord 99770022 = Agent8.template 11 [] [] [] 2 2
```

相位 11 合法，空块有界，两个带长都为 2，所以它满足 `k=0` 的有限安全定理。
`terminating_seed_certified_first_step` 实际调用上游定理，得到第 1 步非回文。
另外两个纯内核计算证书证明完整轨迹及首次命中：

```text
时间 0：  99770022
时间 1： 121777821
时间 2： 250554942
时间 3： 500009994
时间 4： 999909999  （回文）
```

`terminating_seed_first_hit` 同时证明时间 0、1、2、3 都不是回文。
`terminating_seed_not_lychrel` 证明 `¬ Lychrel196.IsLychrel 99770022`。
因此，“属于这种局部模板”不能单独保证全时间避回文。

这个反例**不反驳**原有限安全定理，**不排除**某个另加闭合条件的安全子族，
**不否定**所有可能的循环证书，更**不是**196 的反例。
没有据此宣称带长界最优。

### 3. 时间 0 和中性相位都不能悄悄加进结论

`palindromic_initial_seed` 证明：11888811 满足相位 2、空块、带长 2 的同类模板表示，
但它在时间 0 就是回文。原定理从时间 1 开始是实质性的边界，不是排版选择。

`neutral_phase_counterexample` 证明：99990000 的镜像数位和是相位 9 的同型模板，
而一次反转相加得到回文 99999999。去掉 `c ≠ 9` 会使对应扩展命题失败。

`normalization_sentinels` 另外检查 `reverse10 0 = 0`、`reverse10 100 = 1`、
`step 100 = 101` 及 `pairWord 0 = []`，避免把前导零补位或字符串长度约定误当成整数语义。

## 协调记录的矛盾与合适的修正

在中途读取的协调头 `9936d67a926f884e7e54a2efd1a91540432cdf3d`，
`agent109-template-step-safety.json` 仍然写 READY_FOR_REVIEW，且说没有独立审查。
但 `agent103-review-agent109-step-safety.json` 已有 REVIEWED / PASS 记录，
审查的是 `5808b992ab4e6c302aa083924e3441f9b47f5216`。
main 中 Agent #103 的 REVIEW.md 和源码哈希记录也存在。
七项输入的哈希一致，加上本次合并版重建，支持将作者侧状态说明交给所有者协调修正，
而不是重新认领一个实际上已完成的证明。

本补丁只添加 Agent #121 自己目录下的记录和回归文件，不改写其他人的任务文件、
README 或共享索引。对上游文档的建议是明确使用“后继值”“正时间区间”措辞；
初始模板表示本身不排除起点是回文。

## 未完成的关键义务与后续同步

`Agent109.Cert.certificate_existence` 仍然是条件定理。它要求一个具体有限证书满足
`check cert = true`，并满足初始状态的可实现性检查。
复核本身不提供这些前提的实例证明。
在 `Inv cert m` 中，安全数 m 被表示成 `step n`；证书不是直接声称其模板前驱 n 自己非回文。
这也解释了为何存在性结论取一个后继作为起点。

得到其他种子的全时间安全轨道，仍不能自动证明 196。
针对 196 的使用还需要真实轨道进入已证安全集合的严格连接，或另一条完整全时间论证。

本轮观察到 Agent #110 已认领直接从证书检查条件推出循环预算限制的任务，
Agent #116 认领相应的外层障碍桥接。这里没有复制或接管这些所有权。
本地反例只用于厘清现有定理的适用范围。

后续同步：Agent #116 的 PR #37 已于本次执行中合并到 main
`2c2551165c13d23b11d44122fc7a504d51053e59`，不再把其 cap-3 证书桥接列为未完成。
本次另有一个固定 checkpoint-01 的独立执行复核，见同级
`review-agent116-checkpoint01/REVIEW.md`。后续更强端点的源码读取与真正执行过的
依赖集合在该记录中严格区分。上述状态矛盾是固定历史协调头上的观察，不声称最新
协调记录仍保持同一文字。

## 复现

将此目录放在仓库中的同名路径，使用固定版本 Lean。`--output` 必须是尚不存在的目录；
脚本不会删除或清空已有目录。它在编译前核对七项源码哈希，遇到版本变化会拒绝继续。

```sh
REVIEW=proofs/contributions/agent-121/merged-template-safety-review
LEAN_BIN=/absolute/path/to/lean-4.19.0-linux/bin/lean
RUN=/tmp/agent121-fresh-review

python3 "$REVIEW/rebuild.py" --repo "$PWD" --lean "$LEAN_BIN" --output "$RUN"
python3 "$REVIEW/audit_environment.py" --run "$RUN" --lean "$LEAN_BIN"
python3 "$REVIEW/scan_sources.py" --repo "$PWD"
python3 "$REVIEW/explore_scope.py"
```

最后一项是保留的候选搜索，不是证明检查器。窗口内没有找到回文的记录明确标为
`NO_HIT_IN_FINITE_WINDOW`，窗口外仍为 UNKNOWN。
选中的短轨迹与文中边界证书另由 Lean 内核核验，不依赖 Python 的正确性。

## 拒绝的执行及保留范围

第一次干净编译的各个 Lean 命令均成功，但审计脚本的字符串解析器错误处理了定理名
`Agent109.Cert.append_inj_left'` 中的撇号，整次脚本因此正确地以 FAIL 结束。
该 FAIL 不能当成已完成审计。原解析器和完整日志保留在 `attempts/`、
`evidence/initial-parser-rejected/`。
修复后另建空目录，重新编译并获得最终 PASS；不是手工修改旧 FAIL 为 PASS。

本目录保留所有本次新增 Lean 源码、审查代码、探索参数和结果、失败记录、
成功编译日志、公理报告、源文件及运行时身份。省略的仅是可重建的项目 `.olean`、
重复构建目录、运行时安装及下载包。其来源与已计算的哈希仍然保留。
目录文件清单及 SHA-256 见 `MANIFEST.json`。
