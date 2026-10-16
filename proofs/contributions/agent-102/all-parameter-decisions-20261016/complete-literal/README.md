# 全部 146 条显式定理的增量 literal 公理审计

执行者：Agent #102 的真实子代理 `/root/lean_runtime`。

本次只执行母代理生成的完整 `LiteralAudit.lean`，复用已验证的十个项目 `.olean`。
它是一次增量公理审计，**不是第二次 clean build**。没有重编任何依赖模块，
没有修改冻结数学源、旧证据包或 Git。

## 结果

- 当前十个项目源、成功 `attempt-002/source` 快照和实际已验证 build 中的源副本
  在执行前逐字节一致，并全部符合当前 registry 的 SHA256。
- 对十个源的显式 theorem 声明另外按 namespace 收集，得到 146 个完整名称。
- registry 的普通 endpoint 有 144 个，literal-only 额外 endpoint 有两个。
  两者的并集、十源显式声明名称集、146 条 literal 命令名称集和实际输出名称集完全相等。
- 实际输出顺序也与 literal 源中的 146 条命令逐项一致，无重复或未解析输出。
- 官方 Lean 4.19.0，commit `6caaee842e94`，实际执行退出码为 0。
  本次使用与成功 build 相同 SHA256 的官方可执行文件，并执行
  `--trust=0 -j1 -DElab.async=false`。
- 18 条定理没有公理依赖；完整公理并集仅为
  `propext`、`Classical.choice`、`Quot.sound`。
- 执行前后的十个被复用 `.olean` 的 SHA256 均保持不变。

两个包含 `?` 的名字均被完整保留并实际打印：

| 名称 | 完整公理集合 |
|---|---|
| `Agent102.getElem?_word_of_mem_spansFrom` | `propext`, `Classical.choice`, `Quot.sound` |
| `Agent102.getElem?_word_of_covers` | `propext`, `Classical.choice`, `Quot.sound` |

这 146 条包含旧七模块的 98 条与新增三模块的 48 条显式定理。
它不替代此前对全部 297 条 module-origin theorem 常量（含生成定理）的审计，
也不扩大 registry 已明确限定的仿射字面段词研究范围。

## 文件

- `LiteralAudit.lean`：实际执行的源文件，按字节复制自本贡献目录的 `audit/`。
- `Agent102AllParameters.registry.json`：本次核对的完整 registry 快照。
- `SOURCE_MATCHES.json`：十个源的三方字节一致记录、散列和全部显式声明名称。
- `VERIFIED_OLEANS.json`：被复用的十个编译产物的路径、散列与大小；不包含产物本身。
- `INPUT_RECEIPT.json`：原成功 build 的 receipt 位置及散列、输入来源和核对结果。
- `execute_and_parse.py`：此次实际执行的驱动和完整输出解析程序。
- `run/COMMAND.json`：实际 Lean argv、cwd、`LEAN_PATH`、可执行文件散列与审计类型。
- `run/LiteralAudit.log`：原始完整 stdout/stderr。
- `run/EXECUTION_RECEIPT.json`：实际退出码、用时和日志散列。
- `run/PARSED_AXIOMS.json`：146 条逐项完整公理集合，明确区分普通和 literal-extra 组。
- `run/RESULT.json`：机器可读的核对结果。
- `SHA256SUMS`：本目录全部文件的散列清单，不包含清单自身。

## 复现

本驱动要求已有与记录一致的已验证模块产物；它不会为用户自动重编十个模块。
原成功源码闭包与 clean build 记录在相邻 `runtime-independent/` 包，
原执行时实际复用的目录为：

```text
/workspace/scratch/fb513c1676b0/agent102-arithmetic/universal-controls/attempt-002/run/build
```

在本目录运行以下命令，提供一个新的输出目录即可重做增量审计。
驱动会先验证 literal、registry、源副本、已验证 `.olean` 和官方 Lean 可执行文件的散列。

```bash
python3 execute_and_parse.py \
  --lean /workspace/scratch/fb513c1676b0/agent102-runtime/lean-4.19.0-linux/bin/lean \
  --build /workspace/scratch/fb513c1676b0/agent102-arithmetic/universal-controls/attempt-002/run/build \
  --output /tmp/agent102-complete-literal-replay-001
```

官方 Lean 可执行文件 SHA256：
`92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`。
原执行通过环境支持的 `require_escalated` 正规审批运行，没有变更代理、凭据或访问控制。

本包仅保存审计源、JSON、Python 和文字日志，没有 `.olean`、运行时二进制或压缩发行包。
此前冻结的 64 文件作者/独审包未作修改。
