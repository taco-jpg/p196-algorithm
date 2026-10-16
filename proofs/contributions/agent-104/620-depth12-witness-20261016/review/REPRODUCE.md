# 独立见证审阅的可移植重放

本目录的审阅者是 `/root/strategy_review`，不是发现程序或 Lean 根模块的作者。
审阅属于同一会话和 GitHub 账户下的真实不同角色；不是外部同行评审。

## 所需输入

使用包含本审阅目录的完整仓库检出、Python 3、Git 和官方 Linux x86_64
Lean 4.19.0 工具链。程序固定数学源提交
`8f254e9b43bb319a6c43b208cd181ffc005153ec`，不会把当前工作目录的数学源码
作为该提交的替代。固定编译器发行版提交是 `6caaee842e94`，本次实际二进制
SHA-256 为 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`。

本次只调用未修改的 `proofs/verify_project__214bf7673efe116b.py`，SHA-256 为
`c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a`。
独立 registry 列明十一个源模块的发布路径、Git blob、SHA-256 和导入。
其散列为 `8412a072866cf8079f7a9802d5365f9469546fbc2c7a5d94368e5854b2c11192`。

## 新目录中执行

修改下面前三个路径。`REVIEW_RUN` 下的 `integer`、`published-source` 和
`lean` 必须尚不存在；脚本会拒绝覆盖它们。以下命令顺序执行，Lean 只有
一个 worker。保留输入 Git 对象库和独立检出，直到最后的报告检查完成。

```bash
REVIEW_REPO=/absolute/path/p196-algorithm
REVIEW_LEAN=/absolute/path/lean-4.19.0-linux/bin/lean
REVIEW_RUN=/tmp/agent104-witness-new-run
REVIEW_SCRIPTS="$REVIEW_REPO/proofs/contributions/agent-104/620-depth12-witness-20261016/independent"

python3 "$REVIEW_SCRIPTS/run_replay.py" \
  --output "$REVIEW_RUN/integer"

python3 "$REVIEW_SCRIPTS/replay_lean.py" \
  --git-source "$REVIEW_REPO" \
  --checkout "$REVIEW_RUN/published-source" \
  --lean "$REVIEW_LEAN" \
  --output "$REVIEW_RUN/lean"

python3 "$REVIEW_SCRIPTS/summarize_lean_replay.py" \
  --replay "$REVIEW_RUN/lean" \
  --output "$REVIEW_RUN/review-summary.json"
```

整数命令只核对固定候选与十三项轨道，不扫描种子区间。它使用普通 Python
整数和 `divmod`，限制一个进程、256 MiB 地址空间、10/11 秒软/硬 CPU 限制
及 15 秒墙钟超时。没有固定字长整数溢出。SMT、字符串反转和作者的发现
程序不作为该程序的计算依赖。

Lean 命令先从固定提交实际读取全部十一个源 blob 和 verifier，再建立
detached sparse checkout，核对源字节和 tracked 状态。若本地对象库没有
固定提交，会从该仓库的 `origin` 取回此提交。原 verifier 另建空源/编译
目录，按导入顺序重建全部模块；没有复制作者 `.olean`。源码位置由 registry
指定，所用后端不通过旧目录布局 wrapper 间接定位新增文件。

原 verifier 保持原有编译参数 `-j1 -DElab.async=false` 和默认 trust 设置，
不会自动增加 `--trust=0`。完整空目录闭包重建和来源指纹是这次独立执行的
导入证据。审计覆盖所有来源属于所选模块的定理，包括编译器产生的辅助定理。

## 预期结果与保留记录

成功时，整数命令退出 0 并写出
`PASS_INDEPENDENT_FINITE_INTEGER_REPLAY_ONLY`；Lean wrapper 和原 canonical
报告为 `PASS`；最后的读取器写出
`PASS_INDEPENDENT_EMPTY_BUILD_AND_FULL_MODULE_ORIGIN_AUDIT`。

完整 Lean 结果应为 11 个模块、12 条命令、1,364 个来源定理、公理并集
`[Classical.choice, Quot.sound, propext]`，七个公开端点中两个轨道等式无公理，
其余五个只有 `Quot.sound` 和 `propext`。输出路径和时间戳随新执行变化，
故新报告散列不应被要求等于旧报告散列；数学源、registry 和 verifier 的
固定散列必须一致。

本次真实执行已经保留在 `independent/replay-001/` 和
`independent/lean-replay-001/`，最后一次读取器执行记录位于
`independent/postprocess-001/`。后者仅重新读取既有报告，没有触发第二次
Lean 构建。初次读取器对换行公理列表的格式错误及真实失败也完整保留在
`independent/parser-attempt-001/`，修改前的已通过版本另存于
`independent/postprocessor-history/`。

原 canonical 报告的历史字段 `agent: Agent #1` 未修改；实际审阅身份由
wrapper、registry 和语义报告给出。本包的来源为实际干净发布检出，所以
该报告的 `source_commit` 为固定见证提交，`source_tree_clean=true`。

本包只重建见证的十一个模块。620 上界是独立的 523 模块项目，其报告和
可重放入口在 PR135 的贡献目录中；本命令不代替或再次执行那个项目。

## 已有报告之间的来源连接

`review/source-pins.json` 由 `independent/verify_review_links.py` 生成：它实际
读取九个候选发现/作者证据发布 blob，并比较两份已完成 canonical 报告中
十个共有依赖的 Git 与编译源身份。它还读取上界完整审计日志；没有调用
Lean 或求解器。此脚本针对本次保留的 `lean-replay-001` 和调用者指定的
上界证据目录，属于历史证据核对程序。重新执行时应为 `--output` 选择
不存在的文件，不覆盖已冻结 pins。

首次受限 Git 读取的失败、当时程序和日志在 `independent/link-check-001/`，
允许读取发布 Git 对象后的成功执行在 `independent/link-check-002/`。
两次输入同一固定发布提交，成功记录没有替换失败记录。
