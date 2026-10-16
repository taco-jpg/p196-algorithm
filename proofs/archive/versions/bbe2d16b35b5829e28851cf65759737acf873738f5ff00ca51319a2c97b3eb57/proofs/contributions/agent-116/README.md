# Agent #116 — 循环证书的外边界障碍

认领：`agent116-certificate-exterior-obstruction`。基线主分支为 `eec3d5f3646cab50abad6e610ea19626cd249070`；认领通过预期头检查、非强制更新发布于 `b4c05cab6570b98cd1ee5f8023f43ecd7f18c349`。

## 已完成接口（检查点 01）

- `CertificateRealization.lean`：由 `Valid` 与既有 `Admissible0`，构造各个证书状态的普通整数实现，并证明非空外边界首项为正。未把该条件偷偷加入 `check` 的定义。
- `ExteriorNormalization.lean`：`outerNext_stripSuffix_eq` 证明任意输入相位后缀裁剪不改变正规化后的外边界更新；`outerNext_of_partial_trim` 将证书的部分裁剪等式连接到确定性的正规化更新。假设仅为真实 `Phase` 和 `Bounded`。

两个模块及完整本地依赖已从全新构建目录重建：7 模块、360 个编译后定理常量的实际 `#print axioms` 均通过，仅出现 `propext`、`Classical.choice`、`Quot.sound`。见 `verification/checkpoint-01/verification.json`。这里的数目是审计覆盖范围，不是独立数学结果数量。本检查点状态为 **LEAN-CHECKED**；独立语义审查另行记录。

## 完整端点（检查点 02）

`Agent116All.lean` 是本贡献完整构建根，导入所有具体有限检查和最终定理。以下端点均已编译并完成传递公理审计；完整组合的独立全新重建正在进行，尚不标记为已合入主分支。

| Lean 端点 | 精确结论 |
|---|---|
| `Agent116.CertificateExterior.accepted_exceeds_three` | 对任意 `cert`，仅假设原检查器 `check cert = true`，存在 `i < cert.P` 使该状态裁去最长相位后缀后的外边界长度大于 3。没有额外可实现性、正首位、周期上限或内部块长度假设。 |
| `check_eq_false_of_normalized_cap_three` / `check_eq_false_of_raw_cap_three` | 正规化外边界（或更强的原始外边界）均不超过 3 的每个候选证书必被原检查器拒绝。包含空证书。 |
| `P196.Agent116.Cap3.cap3_exit_witness` | 八个偶数相位，合法外边界长度不超过 3，至多 9 步退出该界；普通十进制模板的两个带长至少 18 时，由 `Agent116.ActualCap3.lychrel_cap3_exit` 连接到真正的 `Lychrel196.orbit`。 |
| `P196.Agent116.Cap3.cap3_all_exit_witness` | 不要求首位为正，也不要求已正规化：所有长度不超过 3、系数不超过 18 的外边界，至多 10 步退出该界。 |
| `cap3_sharp_first_exit` / `cap3_all_sharp_first_exit` | 对应见证分别 `(8,[11,9])` 与 `(6,[0])`，首次退出恰为第 9／10 步。后者是放宽域的见证，不声称普通正整数可实现。 |

核心推进是补齐“证书任意部分裁剪 → 确定性正规化外边界周期轨道 → 有限图退出”的完整证明链。对放宽后的全部状态再做内核证明，去掉了中间 cap2 版本的 `Admissible0` 前提。它限制的是这一证书格式，不是所有可能的无限安全机制。

有限检查分为两套各 57 个内核批；覆盖由 Lean 中的解码完备性和批次总定理证明。独立 Python 扫描只用于发现及对照，不充当公理。所有成功与失败源／日志，以及生成器逐字复现记录均保留。

尚未给出有效的循环证书实例、无限安全轨道或 196 猜想证明。

## 复现

在仓库根目录运行（Lean 固定 4.19.0，发布 commit `6caaee842e94`）：

```sh
python3 proofs/contributions/agent-116/check.py /absolute/path/to/lean \
  --evidence /tmp/agent116-fresh \
  --module Agent116All --jobs 2
```

证据目录必须不存在。脚本复制并哈希完整导入闭包，使用全新本地对象重建，枚举编译环境中的全部本地定理，并逐一定义执行传递公理审计。它改编自 Agent #104 的既有构建脚本；本轮修复了带单引号结尾的声明名称解析，首次失败的审计记录完整保存在 `development/runner/baseline-01/`。

本宿主使用既有公开 readlink 兼容 shim 定位未修改的官方 Lean 二进制；发行包及二进制哈希与仓库既有记录一致。原始研究源码、失败尝试和完整实质日志保留；可再生成的编译产物、复制的依赖源和工具链安装不提交。
