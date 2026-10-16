# 环境恢复事件与证据保存范围

本说明是依据当前会话中实际工具输出整理的事实记录，不是遗失原始输出的重新伪造。

## 1. 官方包下载

通过支持的 GitHub 工具读取官方 v4.19.0 release 元数据后，使用正式批准的 shell 下载官方 Linux x86_64 资源。实际 HTTP 状态为 200，下载字节数 343842845。进度条只出现在工具响应中，没有完整进度日志文件。

原始校验输出已保存并复制为 `original/archive-sha256.log`，值为：

```text
6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe  lean-4.19.0-linux.tar.zst
```

## 2. 首次默认 tar 解包失败

实际命令为 `tar --zstd -xf lean-4.19.0-linux.tar.zst`。工具返回了多条相同类别的错误，例如：

```text
Cannot change ownership to uid 1001, gid 1002: Invalid argument
tar: Exiting with failure status due to previous errors
```

最终退出码为 2。该首次失败没有完整磁盘日志；此处只转写观察到的错误类别与结果。随后实际执行 `tar --zstd --no-same-owner -xf lean-4.19.0-linux.tar.zst` 成功，完整成功重跑输出保存为 `original/extract.log`；该日志为空是成功命令没有标准输出或错误输出的结果。

## 3. 普通沙箱中的 Lean 启动失败

解包后，相对路径与绝对路径调用 `lean --version` 均实际返回：

```text
error: failed to locate application
```

退出码为 1。失败消息仅保留在会话工具输出中，没有另存原始磁盘日志。Lake 的直接版本调用可运行。

使用平台 `exec_command` 的 `sandbox_permissions=require_escalated` 正规批准方式调用同一官方 Lean 绝对路径后，实际输出：

```text
Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)
```

随后通过同一批准路径执行的版本检查、Std 冒烟、Lake 构建与数学模块检查均成功。保存的完整成功版本和冒烟日志见 `original/lean-version.log`、`original/lake-version.log`、`original/lean-smoke.log`、`original/lake-build.log`。

## 4. 没有把环境冒烟扩充为数学结论

冒烟文件的两个定理没有公理依赖；自然数消去测试依赖 `propext`。最早的冒烟命令没有 `--trust=0`，记录始终将其与后来实际使用 `--trust=0` 的算术、边界模块编译区分。所有错误修复均未改代理配置、凭据或访问控制。
