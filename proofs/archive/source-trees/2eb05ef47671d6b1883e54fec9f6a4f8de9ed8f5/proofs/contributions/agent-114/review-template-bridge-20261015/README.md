# Agent #114：模板证明链独立复核与范围回归测试

本目录发布此前已交付但未能推送的完整复核记录，并保留本次发布前的新一轮干净构建。不是新的 P196 证明，不提供有效的无限返回证书实例。

## 结果与状态

复核范围：`Agent109.Compat` 的实际整数兼容性、`Agent109.Endpoints` 的两步与六步模板返回排除，以及 `Agent109.Cert` / `CertCompat` 的条件证书可靠性和整数可实现性。原作者的结果及其他审阅者的贡献保持原有归属；本包是另一次 AI 辅助独立复核，不是外部人类同行评审。

固定数学源码提交：`eec3d5f3646cab50abad6e610ea19626cd249070`。发布分支起点：`2c2551165c13d23b11d44122fc7a504d51053e59`。九份上游源码在这两个提交间的 Git 对象身份未变；复现程序同时核对 Git blob 与 SHA-256。

本次发布前的实际干净构建于 2026-10-15 16:46:36 至 16:47:51 UTC 运行，12 个模块全部退出 0，98 个定理逐一传递公理审计通过。其中 90 个是上游定理，8 个是本包的范围控制，不代表 98 个独立主要成果。没有复用项目旧编译对象。工具链为 Lean 4.19.0 (`6caaee842e94`)，仅使用 Std。公理并集为 `propext`, `Classical.choice`, `Quot.sound`；没有 `sorryAx`、`Lean.ofReduceBool` 或其他被排除的传递公理。

`ScopeRegression.lean` 的八个控制为 LEAN-CHECKED，尚待另一位审阅者独立检查。它们包括 76 的模板返回排除与第二步回文 484 同时成立、13 的六步排除与一步回文 44 同时成立，以及 `CanonicalPair [1]` 不等于整数可实现性。这些是防止误读的测试，不是原定理的反例。

证书存在性端点仍以 `check cert = true` 和初始可实现性为显式前提；本包没有满足前提的证书。发布不构成主线接受或新定理独立审阅。

## 完整证据与历史状态

`archive/history.tar.xz.part00` 至 `part03` 顺序连接后为完整 XZ 压缩 tar，含原始 65 个文件、264371 字节研究内容。原报告、所有已保存失败尝试、源码、完整日志、源码固定记录和旧的未发布协调草稿均逐字节保留。历史报告中的“未推送”和旧分支是当时状态，不是本目录的当前发布状态。历史本地补丁提交 `e80b52f4954aae9cd7ac03ef2c36e99944031d01` 不是 GitHub 主线的子提交。

`archive/publication-replay.tar.xz` 另存本次实际重跑的全部 15 个日志/记录文件。`ARCHIVES.json` 给出分块、压缩及解码后的完整身份；`INVENTORY.tsv` 给出每个原文件的名称、字节数和 SHA-256。三个直接可读的 Lean 文件与历史包内被检查的版本相同。未发布运行时安装、编译对象、缓存和重复上游依赖；它们是可再生基础设施，不是被省略的研究结果。

## 复现

从仓库根目录执行（输出目录必须是新目录或空目录）：

```sh
P=proofs/contributions/agent-114/review-template-bridge-20261015
python3 "$P/check.py" --verify-only --repo-root .
python3 "$P/check.py" --restore-to /tmp/agent114-evidence
python3 "$P/check.py" --repo-root . --lean /absolute/path/to/lean --out /tmp/agent114-clean-replay
```

恢复后，完整原报告在 `/tmp/agent114-evidence/history/README.md`，原机器可读审阅在 `history/review.json`，本次全部构建输出在 `replay/`。构建入口将恢复被校验的原 `reproduce.py`，从空的临时构建目录依次编译依赖、`ScopeRegression`、`AuditAll` 和 `All`，并重复全部 98 项公理审计。

紧急手工恢复（应先核对 `ARCHIVES.json` 的哈希）：

```sh
cat "$P"/archive/history.tar.xz.part0[0-3] > /tmp/agent114-history.tar.xz
mkdir /tmp/agent114-history
xz -dc /tmp/agent114-history.tar.xz | tar -xf - -C /tmp/agent114-history
```

协调认领提交为 `e5fb682001a3fca862db75edd5c3708219518f52`；本任务仅拥有 Agent114 的复核发布路径，没有认领默认分支整合权限，不修改共享索引或他人的源码。
