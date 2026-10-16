# Agent #102 临时 Lean 运行环境

本目录由真实子代理 lean_runtime 准备，仅用于运行环境与最小编译验证。没有克隆、修改或提交 p196 仓库，没有认领数学任务。

## 官方来源

- 发布页：https://github.com/leanprover/lean4/releases/tag/v4.19.0
- 发布元数据：https://api.github.com/repos/leanprover/lean4/releases/tags/v4.19.0
- Linux x86_64 asset ID：250981932。
- 文件：lean-4.19.0-linux.tar.zst。
- 官方元数据的大小与实际下载大小均为 343842845 字节；实际 HTTP 状态 200。
- 实际下载包 SHA-256：6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe。
- 该旧发布元数据的 digest 字段为 null；以上 SHA-256 是本次实际下载计算值，不冒称官方另行发布的校验值。

## 可执行文件与实际版本

Lean：`/workspace/scratch/fb513c1676b0/agent102-runtime/lean-4.19.0-linux/bin/lean`

```text
Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)
```

Lake：`/workspace/scratch/fb513c1676b0/agent102-runtime/lean-4.19.0-linux/bin/lake`

```text
Lake version 5.0.0-6caaee8 (Lean version 4.19.0)
```

## 可复现命令

目录中的 `restore-runtime.sh` 记录官方包下载、已观测校验值复核、解包和编译命令；已恢复后可直接执行：

```bash
bash /workspace/scratch/fb513c1676b0/agent102-runtime/verify-runtime.sh
```

在本平台必须通过 `exec_command` 的 `sandbox_permissions=require_escalated` 正规批准方式运行 Lean。普通沙箱中的同一绝对路径实际报错 `error: failed to locate application`。正式批准后的 `--version`、直接 Lean 编译和 Lake 构建均成功。没有改代理、读取凭据或绕过访问控制。

首次默认 tar 解包因不能恢复 uid 1001、gid 1002 而退出 2；使用 `tar --zstd --no-same-owner` 后解包成功。该选项仅保留当前文件所有者。

## 实际冒烟结果

源文件：`smoke/Smoke.lean`，仅导入发行包自带的 `Std`。

```text
'Agent102Runtime.add_zero_smoke' does not depend on any axioms
'Agent102Runtime.add_cancel_smoke' depends on axioms: [propext]
'Agent102Runtime.reverse_smoke' does not depend on any axioms
```

直接命令 `lean -o smoke/Smoke.olean smoke/Smoke.lean` 退出 0，输出保存于 `lean-smoke.log`；独立 `lake -d smoke build Smoke` 退出 0，输出 `Build completed successfully.`，完整记录保存于 `lake-build.log`。前述两个定理无公理依赖；第三个依赖 Lean 标准公理 `propext`。没有 `sorryAx` 或用户自定义公理。以上只是运行环境冒烟结果，不代表 p196 仓库任何研究模块通过构建。

## 已核对的 #61 协作记录

通过支持的 GitHub 工具读取当时全部 149 条评论，并按运行环境关键词筛选近期记录。与本环境恢复直接相关：

- Agent #5 https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6224478897 ：普通 Git 网络失败，正规批准后的只读 shell 路径成功。
- Agent #4 https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6224542968 ：已实际执行官方 Lean 4.19.0/Lake 与无公理冒烟证明。
- Agent #5 https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6224550308 ：官方 4.19.0，commit 6caaee842e94 与无公理冒烟证明。

这些是已读他人报告；本目录中的编译日志来自本子代理本次实际执行。
