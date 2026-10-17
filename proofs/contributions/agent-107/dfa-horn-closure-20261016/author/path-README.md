# 全长度 Horn 路径闭包：作者检查

作者角色：Agent #107 委派的 `scope_scout`。独占源码为
`proofs/Agent107DFAHorn.lean`；未修改上一任务的任何数学源。

## 两个端点

- `horn_prefix_invariant`：任意完整 `Accepts L q p` 的每个前缀 `i ≤ L / 2`，
  输入 DFA 在前 `i` 个输入对上的运行状态、输出 DFA 在前 `i` 个逐边输出上的运行状态，
  连同 `p i` 都满足证书关系 `R`。
- `horn_accepting_output`：仅由有限 `Horn M R`、`Accepts L q p` 及
  `M.accepts (foldPrefix L q)`，推出 `M.accepts (pathOutput L q p)`。

没有词长上限，没有原 `q` 未读高半边的 admissibility 假设，也没有把语言闭包作为
证书字段。证明复用冻结 Graph 的完整表路径对应，复用冻结 DFA 的 `run_ofFn_succ`
与 `run_append`。末端统一先运行 `extra.toList` 再检查 `outputCenter`，因而同时保留
单数字输入的零次成对转换与奇宽溢出的额外输出对。

## 实际执行

| 尝试 | 退出码 | 源 SHA256 | 结果 |
|---|---:|---|---|
| `path-001` | 1 | `07b26b463f82b46152afe8648b6ab9a89914270a01b0736c2215f5e8b80c6ad9` | 隐式 `simp` 未对含多次索引投影的输出 `ofFn` 匹配运行后继引理；本次不接受 |
| `path-002` | 0 | `e443d30c868d50de911662b885354e53853b7802f415fc41a09ba2317b2974a7` | 显式实例化两个 `run_ofFn_succ` 后全部通过 |

两次尝试均在执行前保存当时完整源码，另存实际命令、标准输出、标准错误和退出码，
无需事后恢复。最终两个端点显式 `#print axioms` 均为：

```text
[propext, Quot.sound]
```

固定依赖 `Agent107DFA.lean` SHA256：

```text
d0fe8accc9d80110230ea3b4061f554d8d9d9dc5b8ea1a89f44e7d2fc977969e
```

工具链为官方 Lean 4.19.0，实际参数为 `--trust=0 -j1 -DElab.async=false`。
检查脚本 `path-run.py` 导入已构建且冻结的依赖 olean，因此本记录仅是作者检查，
不是独立从源依赖闭包重建。完整独立审查由另一角色另行执行。
