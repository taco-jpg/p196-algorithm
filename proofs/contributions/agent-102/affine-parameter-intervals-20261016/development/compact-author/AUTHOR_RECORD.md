# Agent #102：逐步去空区间模块作者记录

## 冻结与角色

真实作者：`/root/word_intervals`。母代理 `/root` 为唯一 Git 写入者和对外转达者。本模块及其 Algebra 依赖均由本子代理编写，因此本记录是作者验证记录；其他代理的独立源码审查应另外收录。

- claim：`47e808147f5f0a0dc5ec7340b062112018288c32`
- scope：`6225680857`
- receipt：`6225773147`
- 工作树基线：`9361e8a8`
- 冻结源：`/workspace/scratch/fb513c1676b0/p196-agent102-intervals/proofs/Agent102ParameterIntervalCompact.lean`
- 长度：2,169 字节。
- SHA256：`39f1b6bf2639a18e443c2dc09487d0b6a169cc15a579ebbe491b38a886be36e9`

已冻结的 RunDefs、ParameterIntervalDefs、ParameterIntervalAlgebra 未被修改。本轮没有 Git 写入。

## 定义与准确范围

命名空间为 `Agent102.ParameterSets`。四个计算定义是：

```lean
prune R := R.filter (fun I => inhabited [I])
fastInter R S := prune (inter R S)
fastComplement R :=
  (prune R).foldr (fun I acc => fastInter (prune I.complement) acc) univ
fastInterAll Rs := Rs.foldr fastInter univ
```

原输入先去空，确保不再为已删除的零宽或倒置空区间构造补项。单区间补中的空项也先过滤。每个 fold 步骤都调用 `fastInter`，而该运算立即过滤当步交集的空区间；并非等整个补运算完成后才清理。

这些定义没有排序或合并重叠区间，不承诺唯一表示、最少区间数或一般复杂度界。

## 五个证明接口

- `Interval.inhabited_singleton_of_contains {I} {k} (h : I.Contains k) : inhabited [I] = true`。
- `holds_prune R k : holds (prune R) k ↔ holds R k`。
- `holds_fastInter R S k : holds (fastInter R S) k ↔ holds R k ∧ holds S k`。
- `holds_fastComplement R k : holds (fastComplement R) k ↔ ¬holds R k`。
- `holds_fastInterAll Rs k : holds (fastInterAll Rs) k ↔ ∀ R ∈ Rs, holds R k`。

后四个规格定理带 `[simp]` 标记。

`holds_prune` 的反向使用包含点作为单区间非空见证，因此过滤不会删除任何实际包含该点的区间。`holds_fastComplement` 先在局部对任意 fold 列表证明语义，再将该列表取为 `prune R`，最后用 `holds_prune` 还原原输入的成员命题。所有规格允许空区域、倒置有限区间、零宽有限区间及无限上端点。

## 未编译草稿与实际构建

`uncompiled-draft-001` 保留母代理要求输入先去空之前的草稿。它没有被编译，分类为“未编译草稿”，不是数学 FAIL。随后在首次编译前按明确的新指令改为 `(prune R).foldr ...`。

`attempt-001` 是 Compact 唯一实际构建尝试，并完整成功。新建空输出目录，按以下顺序串行编译：

1. `Agent102RunDefs`：exit 0。
2. `Agent102ParameterIntervalDefs`：exit 0。
3. `Agent102ParameterIntervalAlgebra`：exit 0。
4. `Agent102ParameterIntervalCompact`：exit 0。
5. `LiteralAudit`：exit 0。

工具版本：Lean 4.19.0，commit `6caaee842e94`。所有编译使用 `--trust=0 -j1 -DElab.async=false`。`LEAN_PATH` 只指向本轮新建的独占空输出目录。原始命令、版本、源码 SHA、日志及返回码在 `attempt-001/manifest.json` 和 `build-results.json` 中。

全部源码在构建结束时再次核对未变。四个工作区模块均从本轮保存的实际源文件重建，没有复用旧工作区 `.olean`。

## literal 公理审计

全部 9 个显式导出均逐个执行 `#print axioms`。

- 四个计算定义均不依赖任何公理。
- `holds_fastComplement` 仅依赖 `propext`、`Classical.choice`、`Quot.sound`。
- 其余四个定理仅依赖 `propext`、`Quot.sound`。

没有非标准公理依赖；源中没有未完成证明或新增公理。该记录是全部显式导出的 literal 审计，不是完整 module-origin 审计。

## 证据布局

`attempt-001` 保存实际源码快照、成功日志、独立 literal 审计源和日志、执行脚本及结果清单。该目录没有 `.olean`。对应 `attempt-001-empty-build` 单独保存构建产物，可在收录源码与日志证据时排除。

母代理后续要求的具体规模控制将放在独立 `controls-001` 目录，使用证据本地的 `CompactControls.lean`；它不修改冻结数学源，也不替代上面的普遍正确性证明。
