# Checkpoint01：Dynamics 独立干净重建

本检查由 Agent #100 的 `runtime_setup` 子代理独立执行，源文件由 `groupii_dynamics` 子代理编写。冻结源为 `proofs/Agent100GroupIIDynamics.lean`，SHA256 `07b8c8d8c0c6fa4aefa1034272464531e27353586066651fd5dda55408d3091c`，Git blob `d6fe51dd088f8a53937bb4ca66b1e3614528e098`。

注册表保留六个已锁定依赖，另加入该冻结源；根模块为 `Agent100GroupIIDynamics`，22个显式 theorem 全部登记为检查 endpoints。`statement-inventory.json` 保留每个陈述的源文本与哈希。重建不读取开发 `.olean`，只在新目录从精确 source bytes 编译七模块，再对完整闭包的 theorem constants 运行公理审计。

从工作树内执行：

```sh
python3 proofs/contributions/agent-100/groupII-overlap-20261016/verification/checkpoint01/replay.py \
  --lean /workspace/scratch/dbb4434dcb2f/runtime100/lean-4.19.0-linux/bin/lean \
  --output /absolute/path/to/new-checkpoint01-output
```

`--output` 必须不存在；当前执行环境必须使用已批准、能够运行 Lean 的执行方式。正式证据来自完整构建，不接受 `--check-only`。上游 verifier 的内部历史作者标签保留为 Agent #1，实际运行归属另见 `agent100-replay-invocation.json`。

此次范围为条件性的有限两步 pair-column 动力学与重叠恢复。尚未加入 Safety/DoubleGate 源，不声明无限递归、不变域、Lychrel存在性或196轨道结论；全局 accepted catalogue 不变。
