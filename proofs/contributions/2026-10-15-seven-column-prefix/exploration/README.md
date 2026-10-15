# 探索记录及准确范围

这些记录用于保留尝试，不增加定理范围。

- seven_column_screen.jsonl：500 个未列入旧清单、且不属于四种可能增位回文首部的候选；状态上限 100,000。最终记录中 739 有限归零，其余触及上限。
- seven_column_screen_1m.jsonl：提高上限后的旧顺序尝试；只完成 52 个候选，随后主动停止。不是完整筛查。
- seven_column_frontier.jsonl：按前一次到达上限的层数选择 60 个候选；739 有限归零，其余记录为超限。
- seven_column_improvements.jsonl：包含 22 条完成的既有类别复查记录；不是预定 25 项全部完成的声明。
- 两份 accepted_build 日志：包括短边界的最终 Python 证书重建记录。

CAP 仅表示资源上限，不能推出存在无限祖先、存在回文或不存在统一上界。没有把 UNKNOWN 归为失败定理。最终接受项仅为正文和 accepted_cpp_results.json 中的五项。
