# Agent 106：实际极值系数新生

任务：`agent106-run-births-formal`。基线 `496db91fbd927f34a5396fb558f3a045df607608`，贡献分支 `research/agent-106/20261015-0442`。

当前检查点只接受 `NoOverflowBirths.lean` 与 `BaseBirths.lean` 的已完成局部/实际一步命题。前者连接仓库的 `Admissible`、`nextColumns` 与实际进位，后者给出一般基数的局部算术分类。各作者已经用 Lean 4.19.0 编译和逐项打印公理；独立空目录重建与交叉审查尚未完成。开发快照及日志保留在 `development/`。

完整 196 猜想、无限安全轨道、整体极值消失和无限再生都没有由这里证明。Agent 102 负责旧极值段的祖先与寿命；本任务处理新生机制及其对整体数量势能的障碍。

`check.py` 接受显式模块列表，从空目录编译全部依赖，并审计每个导出定理和定义的传递公理。仅允许 `propext`、`Classical.choice`、`Quot.sound`；拒绝 `native_decide` 等编译器信任捷径。基础源固定 SHA-256，运行时使用官方 Lean 4.19.0。

```sh
python3 proofs/contributions/agent-106/run-births/check.py \
  --lean /absolute/path/to/lean \
  --build-dir /absolute/path/to/empty-build \
  --evidence-dir /absolute/path/to/evidence \
  --modules NoOverflowBirths BaseBirths
```

本环境通过 `runtime_readlink_self.c` 将当前进程的数字 PID 可执行文件路径查询改用 `/proc/self/exe`；仅修正运行时自身路径发现，不更改 Lean 源、内核或库。正常安装不需要它。编译产物、复制的依赖和编译器安装作为可重建基础设施不纳入版本控制。
