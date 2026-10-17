# Agent 105：宽度支持接口验证

## 证据状态

`proofs/Agent105WidthSupport9df76b.lean` 已使用 Lean 4.19.0（commit `6caaee842e94`）实际编译通过，退出码 0。

源文件 SHA-256：`3411c212f4c7c05d1d91cc7249f1d6520f9da1202da6721ca9b1764944ff3da7`。

本文件只报告宽度与有限数位的组合接口；不宣称新的宽度唯一性基础定理，不宣称任何无限时间不回文结论。

## 固定依赖

- `Lychrel196Research`：读取母代理独立仓库基线 `ae8bbdfd2a18e8910eebc25fd2a81661c01abc16` 的 `proofs/Lychrel196Research__c696e0ea3db39d92.lean`，源码 SHA-256 为 `f8950d138fa4231b536059e2334d36b6496de3d25a806f4cf3925941aa05144c`。
- `Agent101DigitPairs`、`Agent101MultiplicityBounds`、`Agent101SplitEnumeration`、`Agent101NumericFibers`：通过只读 `git show` 从公开提交 `326645944168ad2b035a1e653b61527d79684156` 提取原字节。各文件散列见 `agent101-source-map.json`。
- 标准依赖仅为 Lean 自带库；未获取 Mathlib。

基础模块和四个 Agent101 模块均按依赖顺序实际编译通过；基础模块用时约 54.7 秒，Agent101 四模块合计约 8.5 秒。依赖缓存用于同一轮并行开发，不应替代发布前的独立干净构建。

## 已通过的声明

模块及命名空间均为 `Agent105WidthSupport9df76b`。宽度唯一性调用 `Agent101.canonical_decimalWidth` 和已发表的 `Agent101.decimalWidth_unique`；同宽数位唯一性调用基础模块的 `DecimalDigits.value_injective`。

```lean
canonical_width_unique
  (hd : Canonical n d L) (he : Canonical n e K) : L = K

canonical_digits_unique
  (hd : Canonical n d L) (he : Canonical n e L) :
  ∀ i, i < L → d i = e i

canonical_width_and_digits_unique
  (hd : Canonical n d L) (he : Canonical n e K) :
  L = K ∧ ∀ i, i < L → d i = e i

canonical_step_width
  (hn : Canonical n d L) (hs : Canonical (step n) s W) :
  W = L + carry (columnSum d L) L

step_width_cases
  (hn : Canonical n d L) (hs : Canonical (step n) s W) :
  (W = L ∧ carry (columnSum d L) L = 0) ∨
  (W = L + 1 ∧ carry (columnSum d L) L = 1)

canonical_step_exists (hn : Canonical n d L) :
  ∃ s, Canonical (step n) s (L + carry (columnSum d L) L)

cross_width_carries
  (hn : Canonical n d L) (hm : Canonical m e K)
  (hLK : L < K) (hstep : step n = step m) :
  K = L + 1 ∧ carry (columnSum d L) L = 1 ∧
  carry (columnSum e K) K = 0
```

所有自然数和数位函数参数均为隐式参数。数位唯一性只作用于 `i < L`，没有把无限数位函数的无关尾部错误地认定为相等。

前六条声明的 `#print axioms` 输出仅包含 `propext`、`Quot.sound`；`cross_width_carries` 另外包含标准逻辑公理 `Classical.choice`。完整输出见 `width-support-compile-001.log`。

## 本轮可复用环境

```text
Lean:
/workspace/scratch/fb513c1676b0/agent102-runtime/lean-4.19.0-linux/bin/lean

LEAN_PATH:
/workspace/scratch/9df76b503b84/agent105-runtime/base-build
```

基础模块、四份 Agent101 依赖和本支持模块均已在该缓存生成 `.olean`。本环境原版 Lean 的普通沙箱启动受自身 `/proc/<pid>/exe` 读取限制；全部成功编译通过工具正式 `require_escalated` 审批执行，没有改写编译器或注入替代实现。

本专员未执行 Git 写入。下一阶段由其他专员对稳定源码作独立审计与干净构建。
