# Agent #102：全参数控制证书与独立组合审查

正式 claim：`e685d582b0bd1035733a1f86751af54b07e78792`；receipt：`6225373772`。

本包由真实子代理 `/root/lean_runtime` 整理。我的作者文件为
`proofs/Agent102AllParameterControls.lean`；我对母代理的
`Agent102AffineAllParameters.lean` 进行了独立完整源码审查和实际清洁重建。
对自己编写的 Controls 的核查属于作者验证，不冒称独立审稿。
本工作没有执行 Git 写入。

## 已完成结果

- Controls：32 条定理，SHA256
  `a1bb882b1b8396406f82e9814bc4522d2f2d13b96c7e859fad0d6d650c1914d2`，9187 字节。
- AllParameters：12 条规格定理，冻结 SHA256
  `7cd7b3682bcb6f072853a93cbadaaf43e5c2b59767add0a51f1f8938be183e0c`，5419 字节。
- 任意参数 RunDecision：SHA256
  `e8d876593b4eec5248afe1dbc53cc6fc704b1ba106402a31637aca3120ece9f8`。
- 十个项目源码模块及三个审计模块全部在新输出目录以
  `--trust=0 -j1 -DElab.async=false` 通过。
- 48 条新增具名定理逐条 literal `#print axioms` 检查通过；其中 13 条闭控制证书没有公理依赖。
- 十个选中源模块按真实 module origin 全量枚举了 297 条 theorem 常量，公理并集仅为
  `propext`、`Classical.choice`、`Quot.sound`。
- 另外明确记录了七个 unsafe 实现占位常量；这些不是上述定理的证明依赖。
- 十个 Bool 入口的项目定义依赖检查不达 `word`、`wordAt`、`List.replicate`
  或旧的展开词 tail checker；全参数入口确实依赖 `List.range`。

## 阅读入口

- `CONTROLS.md`：作者控制的数学含义、量词真值和巨大参数证书。
- `REVIEW.md`：对 AllParameters 的独立审查，包含证明逻辑、执行边界与适用范围。
- `REPAIRS.md`、`REPAIR.diff`：首版真实失败与唯一修复。
- `NEW_THEOREMS.json`：48 条 literal 定理和逐条公理集合。
- `attempts/attempt-001`：首版失败源、完整编译日志和实际子进程退出码。
- `attempts/attempt-002`：成功的全部源码、三个审计程序、日志、环境与执行记录。
- `COPY_ORIGINS.json`：原始文件的绝对来源和字节散列；这些原始文件按字节复制。
- `SHA256SUMS`：整个本包的散列清单（不包含清单自身）。

## 可复现命令

实际执行的官方 Lean 为：

```text
/workspace/scratch/fb513c1676b0/agent102-runtime/lean-4.19.0-linux/bin/lean
Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)
```

官方可执行文件 SHA256：
`92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`。
标准库来自该发行；本包清洁重建的是列出的项目源码闭包，未声称从源码重建整个 Lean 发行。

在本包目录执行以下命令。`--output` 必须是一个尚不存在的目录；脚本不会覆盖旧证据。
Lean 路径可替换为同版本官方发行的绝对路径。

```bash
sha256sum -c SHA256SUMS
python3 reproduce.py \
  --snapshot attempts/attempt-002/source \
  --output /tmp/agent102-universal-controls-replay-001 \
  --lean /workspace/scratch/fb513c1676b0/agent102-runtime/lean-4.19.0-linux/bin/lean
```

`reproduce.py` 已实际用于本包的成功 attempt-002，并非仅提供未经运行的示例。
它先验证 `SOURCE_PINS.json`、检查精确 Lean 版本，再将源码复制到新目录，
设置 `LEAN_PATH=.`，按依赖顺序逐项生成新的 `.olean`，保存原始 stdout/stderr 和退出码。
本次环境执行 Lean 需要受支持的 `require_escalated` 审批；已按正规路径批准执行，
未改变网络代理、权限策略或凭据。

复现保留的失败首版可改用 `attempts/attempt-001/source` 和新的输出目录。
该输入预期在 Controls 处以非零码退出并报告八个默认递归深度限制错误；
它是失败证据，不是可接受数学证明。

```bash
python3 reproduce.py \
  --snapshot attempts/attempt-001/source \
  --output /tmp/agent102-universal-controls-failure-replay-001 \
  --lean /workspace/scratch/fb513c1676b0/agent102-runtime/lean-4.19.0-linux/bin/lean
```

每条实际命令的完整 argv、cwd、`LEAN_PATH`、子进程退出码和测得用时均在
对应 `verification.json`。用时仅记录本次执行，不构成复杂度或通用性能保证。

## 源码与证据边界

本任务只新增 Controls，并未修改已有七个冻结数学源码或其他代理的源码。
尤其 `Agent102RunWord.lean` 保持 SHA256
`ffaeac956ec8e22ef6f40c9fff6cd07382339b1306de993a273f2f282a1d8edd`。
本包不包含 `.olean`、运行时二进制或官方巨型压缩包；具体排除说明见 `EXCLUSIONS.md`。
