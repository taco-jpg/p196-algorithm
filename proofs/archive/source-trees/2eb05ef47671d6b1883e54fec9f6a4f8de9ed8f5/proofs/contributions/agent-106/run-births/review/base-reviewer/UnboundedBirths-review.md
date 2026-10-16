# UnboundedBirths 独立语义审查

审查角色：base_generalization（未参与被审模块证明编写）。被审作者：birth_family。

冻结被审文件 `../../UnboundedBirths.lean`，SHA256：
`2b1d22d74db73da5ef93cdd8f559d859a6d0a066d5df777c01234c59af458666`。

语义审查通过。形式构造的源为

`(1,9^k,1,10,9^(2r),10,1,9^k,1)`，

真实单步后继为

`(2,18^k,3,1,0^(2r),1,3,18^k,2)`。

逐项核查：

1. 宽度 `2k+2r+6` 为偶数，源反射对称、外侧正、值在0..18，奇数中心障碍不适用；源每个范围内坐标都不是0或18。
2. 指定携入区间由 `exact_column_equation` 与输出 digit 界归纳确认等于已有 `carry`；未把猜测 carry 直接用作实际 carry 假设。最终 carry 证明为0。
3. `actual_update` 使用已有 `nextColumns`，包含真实 nooverflow 分支和真实镜像坐标；所有范围内坐标都由精确公式覆盖。
4. 中央零区间长度2r，两侧18区间各长k；`exact_extreme_positions` 同时排除额外极值坐标。k=0或r=0时相关带为空，定义和证明均一致。
5. `family_realized` 使用原有 `valid_word_realizable` 得到正整数与规范数字。`numeric_family_realized` 使用原有 `representation_next`，分别连接输入n和实际 `Lychrel196.step n`，不是纯符号转移包装。
6. `arbitrarily_long_birth_bands B` 取 `k=r=B+1`，给出至少B+1连续新零与新18，均来自旧9，源全宽无任何旧极值。它是任意尺寸的单步存在结论，不暗示同一轨道重复产生、无限安全或196轨道结论。

作者依审查建议将“absorbing extreme coefficients”注释改成“extreme coefficients”，消除了未由定理保证的逐点吸收表述。无其他语义修改要求。

独立额外控制：`unbounded_independent_controls.py` 完全不用项目的计算函数，独立构造规范十进制digit witness，以Python整数直接计算 `n + reverse(n)`，检查全宽目标及精确极值坐标。参数 `k,r=0..7` 与 `(100,0),(0,100),(100,100)` 共67例全部通过；这只是形式证明之外的语义对照。

干净编译使用新建的仓库外scratch目录，从原始 `proofs/research/continuation/LychrelDigitSums.lean` 重新编译底座，再编译冻结被审源。底座SHA256为 `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57`。编译及公理检查的最终机器结果见 `UnboundedBirths-review.json`，逐条公理输出见 `UnboundedBirths.log`。

## Agent #106 coordinator retention note

The reviewer turn reached its execution quota after writing this semantic review and the two build logs, before creating `UnboundedBirths-review.json`. That absent machine report is not claimed as retained evidence. The source review and independent integer controls are complete; the coordinator is performing a separately recorded aggregate clean rebuild to close the execution-record gap.
