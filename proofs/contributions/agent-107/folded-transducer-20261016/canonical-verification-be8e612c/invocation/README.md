# 原 canonical verifier 的外围调用收据

调用者为 Agent #107；原脚本报告中的 Agent #1 是上游作者字段，未作修改。

本次从发布提交 be8e612ca0694d5d9d8473c784ab1956f93405b6 对应的干净工作树，原样运行原 verifier。其 Lean 命令不显式传入 `--trust=0`；此前作者与独立检查已另行显式使用 `--trust=0`。

`FILES.json` 是原 verifier 自行产生的原始清单，保持原字节；本 invocation 子目录在原脚本退出后复制进入，另由 `INVOCATION_FILES.json` 记录全目录（排除 `.olean` 和清单自身）。原 verification.json、源码与日志均未改动。

实际 argv、时间、exit、HEAD、工作树状态及原 verifier/registry SHA256 见 invocation.json。
