# 首次正命中时间 2：复现说明

需要 Python **3.11+**、官方 Lean **4.19.0 / commit 6caaee842e94**，以及包含本贡献源码的 Git checkout。`SOURCES.json` 固定全部来源；以下输出目录必须尚不存在。

## 完整 fresh 构建与实际公理审计

提供给 `--repo` 的 Git 对象库必须含有以下六个不可变依赖 commit。若缺少，可从项目现有 `origin` 获取：

```sh
git fetch --no-tags origin 913441a936a437e5f4b82d03d7e7fae32da877af
git fetch --no-tags origin 6fae6e659e5c08c59666588c71a4ed06760de85e
git fetch --no-tags origin 326645944168ad2b035a1e653b61527d79684156
git fetch --no-tags origin 05e4ac30bb35ef87446d6d12a0733625c254bb0e
git fetch --no-tags origin 018a49231cd3226506699282f0f173745e6b9f8d
git fetch --no-tags origin 71691d50497edc83247b3571af276bb0ee438491
```

从仓库根目录执行：

```sh
P196_FIRSTHIT_PACKAGE=proofs/contributions/agent-103/residual-five-firsthit-two-20261016
P196_LEAN419=/absolute/path/to/lean-4.19.0-linux/bin/lean
python3 "$P196_FIRSTHIT_PACKAGE/check.py" \
  --repo . \
  --lean "$P196_LEAN419" \
  --evidence /absolute/path/to/new-firsthit-replay
```

驱动从精确 `commit:path` 恢复依赖，核验 Git blob 和 SHA-256，并在验证原 foundation 完整正文后建立唯一的 import-only 转发模块。四个新源按冻结 SHA 原样复制；实际 imports 决定闭包和顺序。全部项目对象在新 snapshot 中用 **`--trust=0 -j1 -DElab.async=false`** 编译，不复制旧项目对象。每个实际 module-origin theorem，包括 private 和编译生成的 proof helper，均得到一条实际 **`#print axioms`** 查询。失败会保留原始证据。

本次唯一完整运行通过 **27 个模块**、**1881 个 theorem 常量**：其中 **1834 个依赖常量 + 47 个新模块常量**。四个新源码含 **20 条 theorem 声明、0 条定义**；环境中属于四新模块的 `defnInfo` / `opaqueInfo` 也为 **0**。每个 theorem 的传递公理均包含于 `{propext, Classical.choice, Quot.sound}`。

安全分类使用两套有明确范围的记录：**33 项 `axiomInfo` 且 `isUnsafe=true` 的实现声明**，以及 **1157 项 `defnInfo` / `opaqueInfo` 清点：216 safe、917 unsafe、24 partial，0 opaque**。这些项全属依赖；四新模块没有新增此类常量。**33 不是所有 unsafe 常量的总数。** 见 [SAFETY_CENSUS.md](SAFETY_CENSUS.md)、[UNSAFE_IMPLEMENTATIONS.json](UNSAFE_IMPLEMENTATIONS.json) 与 [DEFINITION_INVENTORY.json](DEFINITION_INVENTORY.json)。没有任何已记录 unsafe / partial 名称出现在 1881 个 theorem 的公理列表中。

输出中的 `verification.json` 保存实际 Lean argv、环境、退出码、源/对象哈希以及逐项公理结果；`snapshot/AuditAllContributionModules.lean` 和 `logs/AuditAllContributionModules.log` 保留完整查询源及原始输出。工具也清点所有项目定义；仅新模块的 safe 定义会另做公理查询，本次该集合为空。旧定义通过使用它们的 theorem 受到传递公理检查，未对每个旧定义另行声称独立公理审计。

## 发布路径和 imports 兼容检查

additive registry 的单根为 `ResidualFiveFirstHitConclusion`，实际可达全部 27 个注册模块，没有闲置依赖。项目现有 verifier 可检查发布路径、哈希及 imports：

```sh
python3 proofs/verify_project__214bf7673efe116b.py \
  --lean "$P196_LEAN419" \
  --output /absolute/path/to/new-firsthit-registry-check \
  --registry "$P196_FIRSTHIT_PACKAGE/BUILD_REGISTRY.json" \
  --project agent103-residual-five-firsthit \
  --check-only
```

所核对 verifier 的 SHA-256 是 `c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a`。记录中的执行退出 **0**，状态 **`SOURCE_AND_IMPORT_CHECK_ONLY`**。它只验证源路径和导入兼容；上节命令负责完整数学构建。私有 stage 借用只读 Git 元数据且禁用可选锁，没有 Git 写入，也没有复制项目对象。该检查保留 `source_tree_clean=false`，未把私有 stage 说成已提交工作树。

## 已发布证据

[evidence/complete-replay-evidence.tar.xz](evidence/complete-replay-evidence.tar.xz) 保存完整非对象证据；[FILES.json](FILES.json) 的路径相对于归档根，每项附大小与 SHA-256。归档还包含该索引自身。`evidence/ARCHIVE.json` 给出归档哈希、大小及实际成员数；解压到新空目录即可按索引核对。

其中包括 `verification-clean-001/` 的完整运行、`registry-check-only-001/` 的源检查、`author-history/` 中从实际源码 commit `1908a7e91d4c45c9ce455235f40d4b627af7e4d9` 恢复的开发记录、以及具名 peer reviews。Phase 的 `attempt-001` 是实际失败，error / `sorryAx` 输出单独保留；正式闭包只使用冻结成功源。归档不包含可重建对象或无关私聊。

具名非作者审阅见 [non-author-final-review.md](non-author-final-review.md) 及 JSON。结果保留初始回文 `1661` 的边界，并证明完整局部纤维首次严格正时间回文为 2、全时间模 99 轨迹与原 196 的 `7+i` 相位一致。它不声称普通整数可达性或全局回文避免；两项 gate 均不宣称全仓库验收。
