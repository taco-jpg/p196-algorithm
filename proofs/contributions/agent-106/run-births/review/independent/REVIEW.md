# Agent 106 独立数学与 Lean 审查

审查者：独立 reviewer（非三个被审模块作者）。本报告只覆盖 `NoOverflowBirths.lean`、`BirthFamily.lean`、`OverflowBirths.lean`，不代替 BaseBirths 或 PopulationObstructions 的另行审查。未修改作者源码，未执行 git 写操作。

## 审查结论与精确范围

独立数学、接口审查和完整 Lean 重建均通过，未发现须修正的问题。`build-001/verification.json` 最终状态为 `PASS`：基线、三个目标模块与 AllAxioms 均真实执行 exit 0。56 个公开声明（51 theorem、5 def）公理审计完整通过。当前审查版本的完整 SHA-256 与声明数见 `source_inventory.json`。

可接受的结论是：

- 对任意实际 `Admissible L q`，在实际终止进位为 0 时，物理列 `i < L` 的 0/18 输出及 fresh 出生等价条件成立；中心列排除了旧 9 分支。
- 在实际终止进位为 1 时，全部内部列 `0 < i < L` 的 0/18 输出、非同值旧相邻对的 fresh 出生及邻接 9 的必要性成立。新增两个端点 `i=0,L` 的精确值与非极端性另行覆盖。
- 对每个 `g ≥ 2`，宽度 `g+6` 的完整合法源词 `(1,10,8),18^g,(8,10,1)` 有精确实际无溢出后继 `(3,0,18,17),18^(g-2),(17,18,0,3)`；存在正整数实现，并且该整数本身以及其前两个 reverse-and-add 后继不是回文。
- 这不证明这个家族对更新闭合，不证明出生可以无限再生，不证明任意无限轨道非回文，也不证明 196 或任何数为 Lychrel。`g` 量词描述任意有限尺寸的一步实例，不是时间量词。

## 定义与索引核对

基线 `DecimalDigits.value` 按 `d i * 10^i` 取值，所有索引确为低位优先。`carry q 0=0`，`carry q (i+1)=(q i+carry q i)/10`。`nextColumns` 的分支由实际 `carry q L` 决定，并非自由选择的溢出位。

`Admissible` 包含非空宽度、正外部系数、物理列上界 18、反射对称性及自反中心的偶性。它只约束前 L 列；审查结论没有把无限函数尾部混作十进制数字。基线的 `valid_word_realizable` 给出正整数与 canonical 十进制位实现，故这些不是仅有抽象符号合法性的例子。

无溢出公式使用 `carry q i` 和 `carry q (L-1-i)`，即两边真实归一化数字各自的 incoming carry；没有把后一项误写为 `carry q (L-i)`。两项位界由 `carry_bounded` 和 Admissible 推出。中心 `i=L-1-i` 时两项同一，且旧值必须为偶数，准确排除 9。L=1 也在公式范围内，附加条件并未错误允许中心 9。

溢出后宽度变为 L+1，内部反射位置为 `L-i`，其旧系数由对称性转为 `q (i-1)`；因此公式用相邻旧列 `x=q(i-1),y=q i`，carry 为 `b=carry q i,d=carry q (L-i)`。两个 carry 的前递推关系在 Lean 中显式建立。`0<i<L` 保证所有自然数截断减法所需边界。L=1 无内部列，两个实际端点仍被覆盖。出生定义显式排除旧同值相邻对，准确对应这一溢出祖先约定；不能无条件搬成无溢出的同位置出生定义。

## 全参数家族与数值安全

`actual_carry` 通过 exact column equation、合法输出位界和递归进位归纳，证明展示的 incoming 模板等于实际 carry，而非假设它可实现。`actual_output` 与 `no_overflow` 随后给出真实数字和真实分支；`actual_update` 覆盖所有物理列。

源词在 odd-width 自反中心处落在 18 核心中，满足偶性。`g=2` 的残余核心区间为空，后继中仍有两个新单例 18，旁边分别是 0/17；`g=3` 的残余核心恰为一个中心 18。`exact_18_positions` 排除额外 18 位置，所以“两个新单例、旧核心缩短 2”的表述不依赖漏掉边界的局部算式。

`numeric_canonical_next` 同时证明 successor 的宽度、位界、非零最高位和 value 等式。`numeric_two_steps_safe` 分别证明 n 非回文、step n 非回文、step(step n) 非回文；对 input 使用外列和为 1 排除相同端位，对后两者使用精确 BadWord 前驱判据。私有 `numeric_safe` 只做这个有限步桥接，没有隐藏的不变性前提。

独立有限交叉计算还检查了所有宽度 1..6 的 Admissible 对称词，共 10,467 词、58,041 物理列，及家族 g=2..100 的整数实现，结果全部通过。脚本与报告为 `semantic_check.py/json`。这只是独立语义 sanity check，不作为通用 Lean 定理的证明。例如 g=2 的一个实现是 `19899010 → 20998901 → 31988803`。

## 独立重建与工具审计

审查者执行了下列命令，从之前不存在/为空的独立目录重建基线与三个目标模块；没有使用作者已有 `.olean`：

```sh
LD_PRELOAD=/workspace/scratch/50e90e07524e/runtime/readlink_self.so python3 proofs/contributions/agent-106/run-births/check.py --lean /workspace/scratch/50e90e07524e/runtime/lean-4.19.0-linux/bin/lean --build-dir /workspace/scratch/50e90e07524e/independent-agent106-build-001 --evidence-dir proofs/contributions/agent-106/run-births/review/independent/build-001 --modules NoOverflowBirths BirthFamily OverflowBirths
```

已逐段审查 `check.py`（哈希记在 verification.json）：

1. 拒绝非空构建目录；复制 `.lean` 而不复制对象；将 `LEAN_PATH` 仅设为新构建目录，清除另外两项 Lean 源/sysroot 环境覆盖；Std 来自指定 Lean 4.19.0 安装。
2. 检查实际编译器版本、锁定整个基线源码 SHA-256 `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57`，对精确 import 依赖闭包去注释后拒绝 sorry、admit、native_decide、axiom、unsafe、sorryAx。
3. 在独立目录逐个实际运行 Lean，保存精确命令、exit code、源码/log SHA-256 与耗时；同时验证源文件没有在编译期间改变。源文本扫描未被当作执行成功。
4. 生成单独 `AllAxioms.lean`，包含全部 51 个公开 theorem 及 5 个公开 def 的 `#print axioms`。手工对照源码确认声明枚举完整。匹配输出集合必须与所列 56 项完全一致；只接受 `propext, Classical.choice, Quot.sound`，拒绝 sorryAx、ofReduceBool、trustCompiler 等。
5. 私有 theorem 不单列在公开 inventory；这符合“全部导出 theorem”的范围，它们的公理依赖仍由每个使用者的传递 `#print axioms` 覆盖。另已读审 BirthFamily 的 1 个与 OverflowBirths 的 2 个私有证明，均为显式内核证明。

指定的 preload shim 源码也已阅读：它只将本进程 `/proc/<pid>/exe` 的 readlink 映射为 `/proc/self/exe`，以定位 runtime；没有改写 Lean 源码、证明或 kernel。实际 preload 二进制哈希记录在 verification.json，审查者没有替换它。

形式结果的每个子命令、退出状态与完整日志在 `build-001/`。本报告的通过范围仅对 source_inventory.json 和该构建报告所锁定的字节版本有效。
