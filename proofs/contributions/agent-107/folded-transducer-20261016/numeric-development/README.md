# 数值实现桥：作者检查记录

本模块将完整 folded-transducer 路径接到 `Lychrel196.step n`，复用基础源码中
`FoldedDecimal.representation_next`，不另行定义数字运算或假定一个数值闭包。

## 导出义务

1. `canonical_accepting_step`：对给定的 canonical 输入、完整有限列和表示、
   admissibility 与接受路径，得到真实 `step n` 的 canonical 表示；保留下一步的
   完整有限列和等式，并证明其折叠字等于路径输出。
2. `canonical_step_path`：从 canonical 输入直接构造实际接受路径；可允许的输入
   条件由原有 `NormalizationBridge.canonical_admissible` 提供。
3. `accepting_numeric_realizable`：只假设 `Accepts L q p`，即得到正整数 `n`、
   它的 canonical 输入表示及真实 `step n` 的 canonical 输出表示；原折叠输入
   与输出逐字相同。未读取的高半边先经冻结 Input 模块重建，输出宽度严格为
   `nextWidth (symmetrize L q) L`。

不存在“原 q 未读取的高半边也必须正确”的隐含假设。没有对无关函数尾部提出
相等要求，也没有把数值唯一性等同于 digit realization 唯一性。

## 作者检查复现

从项目根目录运行（每次使用新的证据目录名）：

```sh
python3 proofs/contributions/agent-107/folded-transducer-20261016/numeric-development/run_numeric.py attempt-01
```

脚本保留检查时的完整源文件、标准输出、标准错误、实际命令、源哈希、依赖源哈希、
耗时和退出码。Lean 固定使用 4.19.0，参数为 `--trust=0 -j1 -DElab.async=false`。
此脚本导入已经构建的依赖 olean，因此只记录作者检查；独立从源闭包重建另由审查人进行。

## 冻结结果

`attempt-01` 于 2026-10-16 21:46:53 UTC 真实退出 0，无失败尝试。
三个导出端点均显式打印公理依赖，全部恰为 `propext`、`Quot.sound`。
冻结源 SHA256：

```text
67d88fb4dea6639a0230c5d0f93d8ed778e6393c073679233ab0e792160e086a
```

作者检查使用的 Output 冻结源 SHA256：

```text
5e71e9bd7a693e19fed7716e71a951d4c06708f42cffc8b1afde4f65aa6e2d67
```

完整记录见 `attempt-01/execution.json`、源快照及编译器输出。
