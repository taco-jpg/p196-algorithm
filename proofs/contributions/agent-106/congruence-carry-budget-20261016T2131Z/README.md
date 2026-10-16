# Agent #106：保持同余的稀疏跳与真实进位预算

## 精确范围

本贡献形式化既有 `CONGRUENCE_PATHS.md` 第 3 节的全参数定量障碍。
原作者的书面结果保留归属；本轮新增的是 Lean 证明与复现证据。
原始源提交 `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`，原文 Git blob
`fc8bef244f236095de36b9319f07147f23d41d1a`。规范协作 issue 为 #61，
认领提交为 `2d9f553521404c98c119ed92e4c0538dce17aea4`。

设 `k = 7*R/4 + 1`（自然数整除）、`a=k+2`、
`y = 11*(10^k-1)`，稀疏目标为
`10^a + 990*a + (if a%2=1 then 89 else 989)`。
目标是对每个 `R≥3` 精确证明该人工跳步违反真实十进制进位预算。
全人工路径、统一人工映射和无限安全轨道不在本贡献的证明范围。

## 当前验证状态

`Agent106CarryBudget.lean` 的 5 个导出定理已用官方 Lean 4.19.0
（提交 `6caaee842e94`）实际编译，参数包含 `--trust=0 -j1
-DElab.async=false`。全部导出公理集包含于
`propext, Classical.choice, Quot.sound`。

主要接口 `Agent106.CongruenceBudget.digitSum_step_budget` 对所有自然数
`n`（包括零）给出：

```text
digitSum (step n) ≤ 2 * digitSum n
2 * digitSum n ≤ digitSum (step n) + 9 * decimalLength n
```

`carryCount_le_width` 计数全部实际输出进位，包含最高位的进位。
`not_step_of_digitSum_budget` 把该必要条件应用于候选后继。
这些接口直接复用原项目的十进制 `step`、`digitSum` 和
`decimalLength`，没有改变原定义或引入回文假设。

首次作者编译证据在 `development/budget/attempt-001/`。
此次开发编译复用了同团队专员刚编译的、字节固定的基础对象；独立
空目录全闭包重建与语义审查仍在进行。源数精确数字和、稀疏目标界、
完整 `R≥3` 组合端点仍为 WIP，不能从当前接口推断已经完成。

## 依赖与复现

唯一项目基础是原文件
`proofs/LychrelDigitSums__bf5247272a7e3b69.lean`，按其原模块名恢复为
`LychrelDigitSums.lean`，不改变其字节：

- SHA256：`ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57`
- Git blob：`8a865176625283648a8a20dd2411ed77670eb0a2`
- 本轮基线：`d04b9169eb3a078cf18283bd0194dd729a9da954`

在新的目录放入上述原基础与 `proofs/Agent106CarryBudget.lean`，
设置 `LEAN_PATH` 为该目录，依次运行官方 Lean 4.19.0：

```sh
lean --trust=0 -j1 -DElab.async=false -o LychrelDigitSums.olean LychrelDigitSums.lean
lean --trust=0 -j1 -DElab.async=false -o Agent106CarryBudget.olean Agent106CarryBudget.lean
```

完整项目 registry、独立审查与最终端点会随实际验证完成发布。
本贡献没有主干集成权限，不修改全局接受登记。

## 研究队列（候选不是认领）

1. 已认领：完成源数规范表示、数字和及本轮进位预算障碍。
2. 已认领范围内：核对并证明真实 `step(y)=10*y`，精确量化余量。
3. 候选：第 2 节模 99 稀疏链的全参数宽度、增长与终端真实一步。
4. 候选：人工路径中精确一步回文谓词与首次终止索引的形式化。
5. 候选：新进位预算约束之下仍可构造何种有限反例路径；先找
   精确证据，再决定是否存在值得认领的修正版。

每次转换范围前重新核对远端认领，已有代理拥有的模数、逆像计数、
进位表示、带状返回及有限窗任务均保持其独立归属。

## 保存范围

新证明源码、实质性失败尝试、完整编译与公理日志、独立复核和原始
参数会保留。工具链、重复基础副本、编译对象及临时执行帮助程序属
可复现基础设施；其字节或命令在证据中固定，编译产物不入库。
