# Agent105IntegerSafety 作者证据

作者：Agent #105 / lean_runtime，session 8f1107db019a。

接受源码：`proofs/Agent105IntegerSafety.lean`。
SHA256：`36fa627f04eb653e7eb136eb0496a70916995b6fdcfec3d69b14219b4318377b`。

## 结果与来源

本模块将原 Agent109.Compat.isLychrel_iff 证明内部的局部 `key` 提取成四个公开定理。原 Compat 源码没有修改。

1. `palindrome_orbit_succ_iff`：整数轨道时间 `k+1` 的回文性，等价于其 pairWord 列表轨道时间 `k` 经进位规范化后的字等于自身反转。
2. `palindrome_orbit_positive_iff`：在显式前提 `1 ≤ i` 下，将上式写成正时间 `i` 与列表时间 `i-1`。
3. `palindrome_orbit_positive_iff_of_pairWord`：保留 `1 ≤ i` 和实际表示等式 `Agent109.pairWord n = w`，允许下游直接代入已给定列表 `w`。
4. `nonpalindrome_orbit_positive_iff_of_pairWord`：同一真实表示下的否定形式，供有限安全段使用。

所有整数迭代均为原 `Lychrel196.orbit`，回文谓词为原 `Lychrel196.Palindrome`；所有列表迭代与规范化均为原 Agent8 常量。第一条证明逐项使用原 `Compat.palindrome_eq`、`Compat.orbit_eq`、`Agent109.orbit`、`Agent109.step_palindrome_iff`、`Agent109.pairWord_orbit`、`Compat.orbit_word_eq` 与 `Compat.normalize_eq`，其余三条只作时间算术及等式替换。

初值 `n` 可为任意自然数；原桥不要求 `n ≠ 0`。正时间前提不可在应用中省略：这里的规范化输出对应下一次整数运算，因此本模块不代替时间 0 的初值非回文条件。本模块也不保证任意列表都有整数实现，不主张某个安全返回实例存在。

## 真实检查

官方 Lean 4.19.0，commit `6caaee842e94`，Release。
新模块首编 `attempts/attempt-001` exit 0，没有失败的证明尝试。
随后从新生成的模块单独导入，逐条执行 `#check` 与 `#print axioms`，`export-audit` exit 0。四条定理的公理集合均只含 `propext`、`Classical.choice`、`Quot.sound`。

依赖仅为 PeriodObstructions、LychrelDigitSums、TemplateStep、Compat 四个模块。`dependency-pins.json` 保留精确当前源路径、原路径、Git blob OID 和 SHA256。全部依赖此前已由本线程在独立 integer-bridge 目录完整重编并审计；本轮根据母代理资源协调复用这些精确依赖的 `.olean`，来源与二进制哈希记录在 `reused-dependency-oleans.json`。不把本轮轻量编译冒称为又一次完整依赖重建。

## 复现命令

```bash
cd /tmp/p196-agent105-toolchain/integer-safety/source
LEAN_PATH=. /tmp/p196-agent105-toolchain/lean-4.19.0-linux/bin/lean -j1 -DElab.async=false -o Agent105IntegerSafety.olean Agent105IntegerSafety.lean
LEAN_PATH=. /tmp/p196-agent105-toolchain/lean-4.19.0-linux/bin/lean -j1 -DElab.async=false -o IntegerSafetyExportAudit.olean IntegerSafetyExportAudit.lean
```

从空目录重建时，按来源映射依次编译 LychrelDigitSums、TemplateStep、PeriodObstructions、Compat，再执行上述两条命令。本子代理不执行 Git 写操作；母代理为唯一 Git writer。
