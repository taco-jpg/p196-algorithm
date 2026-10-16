# Agent #102：精确标量仿射不等式区间

正式 claim：`47e808147f5f0a0dc5ec7340b062112018288c32`。
认领 receipt：`6225773147`；scope receipt：`6225680857`。
作者为真实子代理 `/root/lean_runtime`；母代理负责唯一的 Git 写入。
本包是作者证明与验证记录，不自称对作者自己证明的独立审稿。

## 冻结成果

`proofs/Agent102AffineInequalityIntervals.lean`，2411 字节，SHA256：

```text
21def6712029812bc607e5c3c64550ad111ec146da499405b652e26206e86d04
```

唯一直接 import 为 `Agent102ParameterIntervalDefs`，其冻结 SHA256 为
`c06e197c31e902f19345d3e6b390621021f1326d56e7af532302cfae3491949d`。
共享定义再 import 原 `Agent102RunDefs`，SHA256 为
`1544d22e098c659f804e27faab228f4ebb13c8f9d8fc290c6d90f413286cefcf`。
没有依赖新的区间代数、词比较器或尾部定理。

公共 namespace 为 `Agent102.ParameterSets`，四个导出接口为：

```lean
ltInterval (f g : Affine) : Interval
leInterval (f g : Affine) : Interval

contains_ltInterval (f g : Affine) (k : Nat) :
  (ltInterval f g).Contains k ↔ f.eval k < g.eval k

contains_leInterval (f g : Affine) (k : Nat) :
  (leInterval f g).Contains k ↔ f.eval k ≤ g.eval k
```

两条规格对所有自然数参数、任意整数斜率和截距成立，没有 tail、符号、正长度或非空前提。
区间采用左闭右开语义；`hi=none` 表示无穷上界。

## 求解公式与证明依据

令 `a=f.slope-g.slope`、`b=g.intercept-f.intercept`。
原严格不等式等价于 `a*k<b`。

| 条件 | 返回的区间 |
|---|---|
| `0<a` | `[0, toNat((b-1)/a+1))` |
| `a<0` | `[toNat((-b)/(-a)+1), ∞)` |
| `a=0` 且 `0<b` | 全部自然数 |
| `a=0` 且 `b≤0` | 空集 |

两个计算除数分别为 `a` 和 `-a`，只在严格为正的相应分支中使用。
Lean 的整数 Euclidean 除法在这里给出向下取整商；`toNat` 把负端点裁为零。
因此非整数根、整数根、负根以及参数 0 都按原不等式处理。

正斜率分支使用 `Int.le_ediv_iff_mul_le`，将 `a*k<b` 转为
`k≤(b-1)/a`，再与左闭右开上界对应。
负斜率分支使用 `Int.ediv_lt_iff_lt_mul`、`Int.neg_lt_neg_iff`、
`Int.toNat_le` 和 `Int.add_one_le_iff`，直接证明下界对应关系。
斜率差为零时只需比较截距差。

`leInterval f g` 定义为 `ltInterval f ⟨g.slope,g.intercept+1⟩`。
整数上的 `x≤y ↔ x<y+1` 使第二条规格由第一条获得。

实现只做有限次系数算术、符号判断和整数除法；没有 `Nat.range`、参数前缀扫描或词展开。
本包没有声称某个机器模型下的形式化复杂度界。

## 实际 Lean 核查

官方 Lean 4.19.0，commit `6caaee842e94`，实际可执行文件：

```text
/workspace/scratch/fb513c1676b0/agent102-runtime/lean-4.19.0-linux/bin/lean
```

可执行文件 SHA256：
`92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`。
该版本已在此前实际运行确认，本任务复用并核对了同一官方二进制的散列。

成功 `attempt-002` 将三个源码复制到全新输出目录，按依赖顺序使用
`--trust=0 -j1 -DElab.async=false`、`LEAN_PATH=.` 编译，三个 Lean 子进程均 exit 0。
没有复用第一次失败尝试的项目产物。

四个导出均有实际 literal `#print axioms`：

- `ltInterval`、`leInterval` 无公理依赖。
- `contains_ltInterval`、`contains_leInterval` 的公理集合均为
  `propext`、`Classical.choice`、`Quot.sound`。

成功源不含 `sorry`、`admit`、`native_decide` 或新证明公理。

## 小型闭端点证书

`controls-001/ScalarControls.lean` 在已通过的模块上增量编译成功。
五条控制定理均使用 `by decide`，实际 literal 日志均显示无公理依赖。

1. 正斜率的空集、最小非空区间、整数根与非整数根。
2. 负斜率的严格下界、整数根与非整数根，以及负分子除法得到的全域情形。
3. 相同斜率下截距差为负、零、正的三种情况。
4. 非严格比较在正负斜率整数根处包含等号，相同仿射式得到全域。
5. `H=10^100` 的上下端点与巨大正负斜率，全部直接归约为精确区间端点。

巨大例子没有遍历 `[0,H)`；这些是精确实例证书，不能被当作一般性能定理。

## 失败记录与修复

`attempt-001` 的两个定义依赖模块成功，但严格规格负斜率分支的最后一步 `omega`
未能闭合。完整首版源、日志和实际退出码 1 均保留。
`diagnostic-001` 复制该失败源并增加 `trace_state`，记录了未闭合目标及除法等价假设；
该诊断也以 1 退出，源与日志完整保留。

唯一修复是把该分支的最后两行改为：

```lean
rw [Int.mul_comm, Int.neg_mul, Int.neg_lt_neg_iff] at hdiv
simpa only [and_true, Int.toNat_le, Int.add_one_le_iff] using hdiv
```

四个公共接口和求解公式没有改动。精确差异见 `REPAIR.diff`。
失败日志中的 `sorryAx` 来自 Lean 出错后的 elaboration 恢复，明确属于失败证明；
它没有进入随后独立成功编译的版本。
原失败尝试的外层记录脚本会正常退出；数学成败按保存的 Lean 子进程退出码判断，
没有把外层退出码误当作通过。

## 复现命令

从本包目录执行以下命令。新目录内按依赖顺序重建，随后检查闭例。
这与保留的实际命令使用相同源码和 flags；每条原始 argv、cwd、退出码和日志
位于对应 `verification.json` 或 `receipt.json`。

```bash
A102_LEAN=/workspace/scratch/fb513c1676b0/agent102-runtime/lean-4.19.0-linux/bin/lean
A102_REPLAY=$(mktemp -d /tmp/agent102-scalar-intervals-XXXXXX)
cp attempt-002/source/*.lean "$A102_REPLAY/"
cp controls-001/ScalarControls.lean "$A102_REPLAY/"
cd "$A102_REPLAY"
export LEAN_PATH=.
"$A102_LEAN" --trust=0 -j1 -DElab.async=false -o Agent102RunDefs.olean Agent102RunDefs.lean
"$A102_LEAN" --trust=0 -j1 -DElab.async=false -o Agent102ParameterIntervalDefs.olean Agent102ParameterIntervalDefs.lean
"$A102_LEAN" --trust=0 -j1 -DElab.async=false -o Agent102AffineInequalityIntervals.olean Agent102AffineInequalityIntervals.lean
"$A102_LEAN" --trust=0 -j1 -DElab.async=false ScalarControls.lean
```

要复现首版失败，使用 `attempt-001/source`，第三个模块预期返回 1。
诊断源 `diagnostic-001/Debug.lean` 只 import 共享定义，可在前两个模块已通过后运行；
它预期打印状态并返回 1。

本环境运行 Lean 使用受支持的 `require_escalated` 正规审批，未改变代理、凭据或访问控制。
本包不含 `.olean`、重复 build 源副本、运行时二进制或官方发行压缩包；
完整原始尝试源与编译日志无遗漏，`COPY_ORIGINS.json` 记录按字节复制的来源。
