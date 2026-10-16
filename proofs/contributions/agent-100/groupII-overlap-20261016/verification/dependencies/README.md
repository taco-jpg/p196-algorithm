# Agent #100 Group II 精确依赖重放

本目录由运行环境/独立验证子代理维护。保留六个原始模块的精确路径、Git blob、SHA256 与 imports；不修改原始 Lean 源码。source baseline 为 `4b4edf976b2c7a9ba1dad80636c0e21c66350325`。认领提交为 `11dcdec8a54b9afd2dd0824507045e21c8e2dd4d`，认领 blob 为 `69729731db957686d2b1dd67d80b40af232778df`。

## 首次依赖编译

从工作树根目录运行；`--output` 必须尚不存在：

```sh
python3 proofs/contributions/agent-100/groupII-overlap-20261016/verification/dependencies/replay.py \
  --lean /workspace/scratch/dbb4434dcb2f/runtime100/lean-4.19.0-linux/bin/lean \
  --output /workspace/scratch/dbb4434dcb2f/build100
```

开发时的依赖源码与 `.olean` 位于 `/workspace/scratch/dbb4434dcb2f/build100/dev/source`。设置 `LEAN_PATH` 为该目录即可导入。该目录的已编译对象仅供开发；独立验证必须重新建立全新输出目录。

当前执行环境需让包含 Lean 子进程的整个命令在已获批准的可执行环境运行；默认 sandbox 会报 `failed to locate application`。不修改安全或网络设置。

## 新 source checkpoint

为每个 checkpoint 生成独立 registry，保留六个依赖记录的 `path`、`git_blob`、`sha256`、`imports` 不变；新增模块使用自身精确 source pins 与 imports，指定实际 roots 和需检查的 endpoints。传入 `--registry /absolute/checkpoint.registry.json`；若 project 不叫 `dev`，显式传入 `--project`。每次选择新的 `--output`。

`replay.py` 会验证原 verifier 的 SHA256、六个依赖契约及实际字节，再调用原始 `proofs/verify_project__214bf7673efe116b.py`。原 verifier 负责完整 source/import 闭包校验、拓扑编译和每个选定模块全部 theorem constants 的公理审计。所有标准 imports 仅来自已核验的 Lean 4.19.0。标准基础公理允许列表保持 `propext`、`Classical.choice`、`Quot.sound`。

`--check-only` 仅校验并复制 source/import 闭包，不构成证明验证；正式独立验证不得使用该选项。源闭包不得有额外无关模块，不得遗漏非标准库依赖，不得把 `catalogue_complete` 设为真。

## 证据与身份

每次输出包含原 verifier 的 `verification.json`、`FILES.json`、逐模块日志、审计源与审计日志。`agent100-replay-invocation.json` 另外记录实际执行者、调用参数和 verifier/registry/source pins 哈希。原 verifier 内部固定的 `Agent #1` 标签指其历史作者；不能据此把本次执行归给 Agent #1。

首次构建只验证既有六模块依赖，不产生新 Group II 数学结论，也不构成全仓库接受证明。
