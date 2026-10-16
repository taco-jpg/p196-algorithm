# Agent #102 运行环境与数学模块作者证据

本目录由 Agent #102 的真实子代理 `lean_runtime` 整理，记录其编写的标量仿射算术与边界模块的作者自检。公用定义由母代理维护，`Agent102RunWord` 沿用其已有精确源码。本目录不表示对子代理自己所写证明完成了独立同行审查。

母代理给出的已有发布关联为提交 `a3329eda74fc419d76c185fa843d9e6e1602a09b` 与 PR #93。本次整理仅新增本目录文件，没有执行 Git 写入。冻结模块源码及顶层 registry 均保持原样。

## 保存的实质尝试

| 目录 | 原始结果 | 保存内容 |
|---|---|---|
| `runtime/original` | 官方 Lean 4.19.0 与 Lake 可运行，Std 冒烟成功 | 原始恢复说明和脚本、版本与下载包校验记录、冒烟源与配置、直接 Lean 和 Lake 日志 |
| `arithmetic/attempt01` | 首版编译通过 | 当次完整两模块源码与编译日志 |
| `arithmetic/checkpoint-build` | 新目录再次编译通过，完整审计 17 个导出定理 | 精确两模块源码、逐条 literal `#print axioms` 的 `Audit.lean`、全部日志 |
| `arithmetic/checkpoint-evidence` | 上述成功作者检查的证据快照 | 原始 registry、verification、文件清单、源码和日志 |
| `boundary/attempt01` | 失败，退出 1 | 四模块完整源码与每一步日志；没有删去失败后的公理诊断输出 |
| `boundary/attempt02` | 修复后在新目录编译通过，审计 12 个定理 | 四模块完整源码与全部日志 |
| `boundary/evidence` | 上述边界作者检查的证据快照 | 原始 registry、verification、文件清单、源码、成功和失败日志 |

数学模块的实际检查均使用官方 Lean 4.19.0、commit `6caaee842e94` 和 `--trust=0`。最早的运行环境冒烟使用直接 Lean 与 Lake 默认编译选项，原始日志没有声称该次冒烟使用了 `--trust=0`。

算术模块全部 17 个导出定理的公理依赖包含于 `{propext, Classical.choice, Quot.sound}`；边界模块全部 12 个定理的并集为 `{propext, Quot.sound}`。这些是具体模块的作者检查结果。

## 冻结身份

| 模块 | SHA-256 |
|---|---|
| `Agent102RunDefs` | `1544d22e098c659f804e27faab228f4ebb13c8f9d8fc290c6d90f413286cefcf` |
| `Agent102RunWord` | `ffaeac956ec8e22ef6f40c9fff6cd07382339b1306de993a273f2f282a1d8edd` |
| `Agent102AffineArithmetic` | `a36d4a0e572ab083cb8408ee71a5d2281bc838df508ce184e6a313a23b9a3df2` |
| `Agent102AffineBoundary` 最终版 | `7dda5da29f8086b7a35b30f041e6092da2b8ea97bd315b5a1b75c6934d01c35a` |
| `Agent102AffineBoundary` 失败首版 | `aa5d97b2e7baa2156f67aa45a2d5db76d7f081a25fff29621eadcc609b48889d` |

`COPY_ORIGINS.json` 逐文件记录原始位置、归档位置、大小与 SHA-256，原始文件按字节复制。`SHA256SUMS` 覆盖本目录所有文件，唯一例外为校验清单自身。

## 唯一数学失败与修复

边界首版的两个闭例直接调用 `decide`，但类型类搜索未展开 `Span.overlaps`，因此无法合成对应的 `Decidable` 实例。原始完整日志在 `boundary/attempt01/Agent102AffineBoundary.log`；失败源码与全部依赖位于同一目录。

修复仅在两个闭例中显式展开 `Span.overlaps`，并在零段例中展开 `emptySpan` 与 `coveringSpan`。没有更改定理陈述或公用定义。精确差异保存在 `boundary/repair.diff`。

失败 elaboration 的后续 `#print axioms` 会打印自动错误恢复产生的 `sorryAx`。该输出被原样保留，属于失败诊断，不能视为成功证明。最终 `boundary/attempt02/Agent102AffineBoundary.log` 的 12 个定理全部通过，且没有 `sorryAx`。

## 可移植的数学复现

从本目录执行校验：

```bash
sha256sum --check SHA256SUMS
```

使用官方 Lean 的绝对路径和一个尚不存在的输出目录：

```bash
python3 reproduce.py \
  --lean /absolute/path/to/lean-4.19.0-linux/bin/lean \
  --case arithmetic-checkpoint \
  --output /absolute/new/agent102-arithmetic-checkpoint

python3 reproduce.py \
  --lean /absolute/path/to/lean-4.19.0-linux/bin/lean \
  --case boundary-final \
  --output /absolute/new/agent102-boundary-final
```

`reproduce.py` 只使用 Python 标准库，核对源文件散列与编译器版本，复制精确源文件到新目录后顺序运行 `lean --trust=0`；全部新日志与编译产物留在指定输出目录。它不写入本归档、不读取或复用归档外的项目 `.olean`，也不执行 Git 操作或网络请求。

如需复现失败首版，必须明确选择该案例：

```bash
python3 reproduce.py \
  --lean /absolute/path/to/lean-4.19.0-linux/bin/lean \
  --case boundary-failed \
  --output /absolute/new/agent102-boundary-expected-failure
```

此案例要求三个依赖模块成功，而最后的边界模块退出 1 并含原有 `Decidable` 合成错误；脚本记为 `EXPECTED_FAILURE_REPRODUCED`，不会标记为数学 PASS。`--case arithmetic-first` 另可重放最早成功的算术源码。

本次归档没有重新运行这些数学证明。保存的 PASS 来自前述实际作者编译；新增复现脚本经静态检查，归档字节与清单已经逐项核对。

## 官方运行环境恢复

官方资源与本次实际下载信息见 `runtime/environment.json`。下载资源为：

<https://github.com/leanprover/lean4/releases/download/v4.19.0/lean-4.19.0-linux.tar.zst>

在一个新目录中下载和解包：

```bash
mkdir /absolute/new/agent102-official-runtime
cd /absolute/new/agent102-official-runtime
curl --fail --location --connect-timeout 20 --max-time 60 \
  --output lean-4.19.0-linux.tar.zst \
  'https://github.com/leanprover/lean4/releases/download/v4.19.0/lean-4.19.0-linux.tar.zst'
sha256sum --check <<'AGENT102_OFFICIAL_HASH'
6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe  lean-4.19.0-linux.tar.zst
AGENT102_OFFICIAL_HASH
tar --zstd --no-same-owner -xf lean-4.19.0-linux.tar.zst
./lean-4.19.0-linux/bin/lean --version
./lean-4.19.0-linux/bin/lake --version
```

本次观察的包大小为 343842845 字节，HTTP 状态 200。以上 SHA-256 是本次从官方 URL 实际下载后计算的值；该旧 release API 的 `digest` 字段为空，没有另行取得官方校验文件。

本会话普通沙箱下的 Lean 启动曾报 `error: failed to locate application`；使用平台的 `require_escalated` 正规批准路径后，实际版本检查与数学编译成功。首次默认 tar 解包因无法恢复 uid 1001、gid 1002 而失败，随后 `--no-same-owner` 解包成功。具体证据保存范围见 `runtime/INCIDENTS.md`，没有改写代理设置或访问控制。

原始环境脚本保留当时的绝对路径，是历史记录。异机复现应采用上述新目录命令与本目录的 `reproduce.py`。排除的运行时与生成产物见 `EXCLUSIONS.md` 和 `EXCLUSIONS.json`。
