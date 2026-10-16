# PiecewiseCounts 独立重建与审查证据

正式 claim：`47e808147f5f0a0dc5ec7340b062112018288c32`。
审查者为 Agent #102 的真实子代理 `/root/lean_runtime`。
独立审查对象是母代理编写的 PiecewiseCounts；审查者曾编写其中标量和算术依赖，
这一作者关系在所有结论中明确保留。

## 结果

- 冻结 root SHA256：`3236a731b8bb923a3d64896ea281671a634c394a9a267a22fe34a3bba78880eb`。
- 冻结 Compact SHA256：`39f1b6bf2639a18e443c2dc09487d0b6a169cc15a579ebbe491b38a886be36e9`。
- 等待母代理明确确认冻结后才进行最终源码构建。
- 一次独立 clean build：七个项目模块、ReviewerControls 和三个审计模块，共十一项，全部 exit 0。
- 使用官方 Lean 4.19.0，commit `6caaee842e94`，
  `--trust=0 -j1 -DElab.async=false`，`LEAN_PATH=.`。
- 没有复用任何项目 `.olean`；Std 来自记录的官方发行，没有声称重建整个 Lean 工具链。
- 44 条闭包显式定理加四条 reviewer 控制，共 48 条 literal 公理检查全部通过。
- 按真实 module origin 枚举全部 196 条 theorem 常量，其中 192 条属于七个项目模块，
  四条为 reviewer 控制；root 模块中有 39 条 theorem 常量，含六条显式规格及生成定理。
- 公理并集仅为 `propext`、`Classical.choice`、`Quot.sound`。
- 21 个 unsafe 实现占位常量在日志中明确另列；它们没有进入任何已审定理的公理依赖。
- 五个符号入口执行依赖检查均通过；四个闭控制均不依赖任何公理。
- 本次独立构建没有失败尝试，也没有修改作者源或执行 Git 写入。

详细语义审查见 `REVIEW.md`。

## 文件与历史标记

- `final-001/source`：实际成功构建的七模块闭包、控制和三个审计源。
- `final-001/logs`：每个 Lean 子进程的完整原始 stdout/stderr。
- `final-001/verification.json`：实际 argv、cwd、环境路径、退出码与测得用时。
- `final-001/SOURCE_PINS.json`：全部构建源的 SHA256 与大小。
- `final-001/EXPLICIT_THEOREMS.json`、`PARSED_AXIOMS.json`：48 条 literal 名称与完整公理集合。
- `MODULE_ORIGIN_COUNTS.json`：按实际来源模块归集的 theorem 常量数量。
- `FREEZE_RECEIPT.json`：母代理冻结授权及字节核对记录。
- `initial-read-001`：只读阶段保存的候选源码，明确未由 reviewer 编译。
  它的 PiecewiseCounts 已等于最终版本，但 Compact 是较早草稿；正式结论仅使用 `final-001`。
- `rebuild.py`：此次实际使用的 reviewer-owned 清洁重建和审计驱动。
- `ReviewerControls.lean`：驱动输入，与 final-001 中的副本相同。
- `COPY_ORIGINS.json`：所有按字节复制的原始文件的绝对来源、散列和大小。
- `RESULT.json`：机器可读结果与角色边界。
- `SHA256SUMS`：全部包文件的散列清单，不含清单自身。

## 复现

在本包目录执行。输出必须是尚不存在的新目录。
驱动先核对每个依赖散列，复制源码到新目录，生成明确的 literal 与 module-origin 审计，
再依次运行 Lean；不会改动输入源码或复用旧项目产物。

```bash
python3 rebuild.py \
  --proofs final-001/source \
  --root-sha 3236a731b8bb923a3d64896ea281671a634c394a9a267a22fe34a3bba78880eb \
  --compact-sha 39f1b6bf2639a18e443c2dc09487d0b6a169cc15a579ebbe491b38a886be36e9 \
  --lean /workspace/scratch/fb513c1676b0/agent102-runtime/lean-4.19.0-linux/bin/lean \
  --output /tmp/agent102-piecewise-review-replay-001
```

实际官方 Lean 可执行文件 SHA256：
`92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`。
原环境通过受支持的 `require_escalated` 正规审批执行，未更改代理、凭据或访问控制。
用时是本次执行记录，不是普遍性能保证。

## 排除说明

本包保留全部实际构建源、审计程序和原始日志。
排除 `.olean` 等可重新生成的产物、build 中重复的源副本、运行时二进制和官方发行压缩包。
原工作目录中的这些产物没有被删除。
没有复制凭据、全量环境变量或与本次 reviewer 构建无关的其他代理失败记录。
