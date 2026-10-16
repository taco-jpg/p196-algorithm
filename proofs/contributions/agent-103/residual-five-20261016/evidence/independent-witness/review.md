# Witness 独立语义与 Lean 重建审阅

审阅者：Agent #103 scope_scan；被审源码由 source_audit 独立编写。

- 冻结源码 SHA-256：`bdd3abc30bd4a24fe27df657c21dcc92555d8b3fa26f2c7c3abd3e7091bd1d3f`。
- Lean 4.19.0 在新的空产物目录内实际编译退出 0。全部 26 个 theorem 声明公理打印：21 个不依赖公理，5 个仅依赖 `propext`、`Quot.sound`。没有 `sorryAx`、自定义公理或 `native_decide`。
- 使用原始 `Lychrel196.step`、`orbit`、`Palindrome`；时间零包含初值，反转会去掉由末尾零产生的前导零。六个明确步进等式全部经内核归约。
- 与原手稿第 4 节逐项核对七个整数完全一致。Python 标准整型和字符串十进制反转独立重算，所得轨道、首回文时间与各位宽一致。该计算仅作交叉审计，Lean 定理不依赖 Python。
- 七个模 99 余数为 `11,22,44,88,77,55,11`。全时刻匹配使用原 `Agent423.TemporalResidues.orbit_mod99_pow_of_dvd11`，分别应用于 seed 与实际 `orbit 196 3 = 7436`；没有把有限七项计算冒充无限时间结论。
- 初值为正且异于 196。0 至 5 时刻均非回文，第 6 时刻达到 `55*(10^32+1)`，即 `fam 5 15` 的数值。`first_positive_hit_six` 陈述的合取与原 `DecimalDelayBridge.FirstPositiveHit` 定义逐项相同。
- 时刻 4 的完整对和系数为 `[2,12] ++ [9]*30 ++ [12,2]`；下一次加法第 2 至 33 列进位为 1，第 34 列终端进位为 0。与 Shape 模块的 r=15 特例一致。
- `mod99_trajectory_insufficient` 只否定“具有相同整个模 99 未来轨迹的任意正初值都不能达到该成员”的命题，不声称 196 会达到它，也不推出原猜想。

第一次独立编译仅发现三条已被 `rw` 归约闭合后的多余 `decide`，失败源码和日志完整保存在相邻 `witness-review` 目录。作者删除三条多余 tactic 后，本冻结源码通过，定理陈述与数值未变化。
