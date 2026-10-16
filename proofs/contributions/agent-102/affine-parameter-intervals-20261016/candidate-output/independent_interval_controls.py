#!/usr/bin/env python3
"""独立字面词控制；不实现仿射区间求解器，不导入任何项目代码。"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import sys


HUGE = 10**100
SMALL_POINTS = (0, 1, 2, 3, 4, 5, 6, 7, 11, 19)
MAX_EXPANDED_WORD = 512


@dataclass(frozen=True)
class Run:
    digit: int
    slope: int
    intercept: int


@dataclass(frozen=True)
class Case:
    name: str
    mode: str
    left: tuple[Run, ...]
    right: tuple[Run, ...]
    expected: tuple[tuple[int, int | None], ...]
    points: tuple[int, ...]
    reason: str


def runs(*items: tuple[int, int, int]) -> tuple[Run, ...]:
    return tuple(Run(*item) for item in items)


CASES = (
    Case(
        "two_isolated_points", "equal",
        runs((7, 1, -2), (7, -1, 2)), runs((7, 0, 1)),
        ((1, 2), (3, 4)), SMALL_POINTS,
        "左词长度为|k-2|；同一个数位的长度等于1恰在k=1或3。",
    ),
    Case(
        "bounded_empty_plateau", "equal",
        runs((4, -1, 2), (4, 1, -4)), (),
        ((2, 5),), SMALL_POINTS,
        "两段同时裁空恰在2≤k≤4；其他参数至少一段非空。",
    ),
    Case(
        "equality_with_middle_hole", "equal",
        runs((5, 1, -2), (5, 1, -6)), runs((5, 2, -8)),
        ((0, 3), (6, None)), SMALL_POINTS,
        "k≤2两边为空；k=3,4,5的总长不同；k≥6的总长同为2k-8。",
    ),
    Case(
        "zero_run_inside_positive_span", "equal",
        runs((1, 0, 1), (7, -1, 2), (1, 0, 1)), runs((1, -1, 4)),
        ((2, 3),), SMALL_POINTS,
        "k=2时零长度7段在右侧正长度1段内部；此前同宽异字，之后总宽不同。",
    ),
    Case(
        "clipped_sums_identical", "equal",
        runs((6, 1, 0), (6, -1, 2)), runs((6, 0, 2), (6, 1, -2)),
        ((0, None),), SMALL_POINTS,
        "两个总长度都等于max(k,2)，但逐段裁零分支不同。",
    ),
    Case(
        "same_width_bad_digit_then_tail", "equal",
        runs((1, 1, 0), (2, -1, 3)), runs((1, 1, 0), (1, -1, 3)),
        ((3, None),), SMALL_POINTS,
        "总宽始终相同；k<3时剩余2数位段造成不等，k≥3该段裁空。",
    ),
    Case(
        "literal_zero_is_not_empty", "equal",
        runs((0, 0, 1)), (), (), (0, 1),
        "数位0仍是实际列表元素；[0]与[]始终不同。",
    ),
    Case(
        "bounded_palindrome_interval", "palindrome",
        runs((1, -1, 3), (2, 0, 1), (1, 1, -5)), (),
        ((3, 6),), SMALL_POINTS,
        "3≤k≤5只有中央[2]；左侧或右侧单独非空时首尾不同。",
    ),
    Case(
        "huge_equality_hole", "equal",
        runs((5, 1, -HUGE), (5, 1, -HUGE - 4)), runs((5, 2, -2 * HUGE - 4)),
        ((0, HUGE + 1), (HUGE + 4, None)),
        (0, HUGE - 2, HUGE - 1, HUGE, HUGE + 1, HUGE + 2,
         HUGE + 3, HUGE + 4, HUGE + 5, HUGE + 17),
        "H=10^100；平移前三段关系，精确空档只有H+1,H+2,H+3。",
    ),
    Case(
        "huge_declining_palindrome", "palindrome",
        runs((1, -1, HUGE), (2, 0, 1)), (),
        ((HUGE, None),),
        (HUGE - 3, HUGE - 2, HUGE - 1, HUGE, HUGE + 1, HUGE + 2, HUGE + 17),
        "负斜率1段在k=H裁空；此前首尾分别为1和2，此后词为[2]。",
    ),
)


def literal_word(spec: tuple[Run, ...], k: int) -> list[int]:
    """仅在预选参数展开很短的真实词；不会扫描参数前缀。"""
    assert k >= 0
    counts = [max(0, r.slope * k + r.intercept) for r in spec]
    total = sum(counts)
    if total > MAX_EXPANDED_WORD:
        raise ValueError(f"预选控制意外要求展开{total}个元素")
    word: list[int] = []
    for r, count in zip(spec, counts):
        assert r.digit >= 0
        word.extend([r.digit] * count)
    return word


def member(intervals: tuple[tuple[int, int | None], ...], k: int) -> bool:
    return any(lo <= k and (hi is None or k < hi) for lo, hi in intervals)


def encode_intervals(intervals: tuple[tuple[int, int | None], ...]) -> list[dict]:
    return [{"lo": str(lo), "hi": None if hi is None else str(hi)} for lo, hi in intervals]


def decode_intervals(items: list[dict]) -> tuple[tuple[int, int | None], ...]:
    result = tuple((int(x["lo"]), None if x["hi"] is None else int(x["hi"])) for x in items)
    assert all(lo >= 0 and (hi is None or hi >= 0) for lo, hi in result)
    return result


def union_disagreement(expected: tuple, actual: tuple) -> int | None:
    """比较两个已给有限区间并；只看有限端点，不求解仿射段模板。"""
    points = {0}
    for lo, hi in expected + actual:
        points.add(lo)
        if hi is not None:
            points.add(hi)
    return next((k for k in sorted(points) if member(expected, k) != member(actual, k)), None)


def case_record(case: Case) -> dict:
    def encode_runs(spec: tuple[Run, ...]) -> list[dict]:
        return [{"digit": r.digit, "slope": str(r.slope), "intercept": str(r.intercept)} for r in spec]
    return {
        "id": case.name, "mode": case.mode,
        "left": encode_runs(case.left), "right": encode_runs(case.right),
        "expected_intervals": encode_intervals(case.expected),
        "literal_sample_parameters": [str(k) for k in case.points],
        "expected_set_reason": case.reason,
    }


def diagnostic_controls() -> list[dict]:
    """准确反例针对可能省略的条件；不声称现有Lean实现含这些错误。"""
    k = 1
    separate = max(0, k - 2) + max(0, 2 - k)
    after_sum = max(0, (k - 2) + (2 - k))
    assert separate == 1 and after_sum == 0
    zero_lo, zero_hi, other_lo, other_hi = 1, 1, 0, 2
    crosses = zero_lo < other_hi and other_lo < zero_hi
    overlaps = max(zero_lo, other_lo) < min(zero_hi, other_hi)
    assert crosses and not overlaps
    assert literal_word(runs((1, 0, 1), (7, 0, 0), (1, 0, 1)), 0) == [1, 1]
    assert [] != [0]
    intervals = ((0, 2), (1, None))
    wrong_union_of_complements = ((2, None), (0, 1))
    assert all(member(intervals, k) for k in (0, 1, 2, 3))
    assert member(wrong_union_of_complements, 0)
    return [
        {"id": "clip_each_before_add", "k": "1", "sum_of_clips": separate,
         "clip_of_sum": after_sum},
        {"id": "zero_span_needs_self_nonempty", "empty_span": [1, 1],
         "positive_span": [0, 2], "two_cross_comparisons": True, "actual_overlap": False},
        {"id": "length_condition_not_vacuous", "left": [], "right": [0],
         "bad_overlap_pairs": [], "actual_equal": False},
        {"id": "complement_union_requires_intersection", "input": encode_intervals(intervals),
         "true_complement": [], "wrong_union_has_witness": "0"},
        {"id": "inactive_piece_cannot_contribute", "k": "1",
         "inactive_domain": {"lo": "0", "hi": "1"},
         "inactive_form_value": "0", "actual_count_value": "1",
         "comparison_to_zero_without_domain_would_be_wrong": True},
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--export-cases", type=Path)
    parser.add_argument("--candidate-output", type=Path)
    parser.add_argument("--only", action="append", default=[])
    args = parser.parse_args()
    known = {case.name for case in CASES}
    assert all(name in known for name in args.only)
    selected = [case for case in CASES if not args.only or case.name in args.only]
    candidate = None
    if args.candidate_output:
        supplied = json.loads(args.candidate_output.read_text())
        candidate = {x["id"]: decode_intervals(x["intervals"]) for x in supplied["cases"]}
    report = {
        "author": "/root/research_map", "python": sys.version,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "scope": "有限预选参数上的真实列表展开；没有执行Lean或仿射区间求解器",
        "candidate_output_checked": args.candidate_output is not None,
        "cases": [], "diagnostics": diagnostic_controls(),
    }
    max_length = 0
    sample_count = 0
    for case in selected:
        record = case_record(case)
        record["literal_observations"] = []
        for k in case.points:
            left = literal_word(case.left, k)
            right = left[::-1] if case.mode == "palindrome" else literal_word(case.right, k)
            result = left == right
            expected = member(case.expected, k)
            assert result == expected, (case.name, k, left, right, expected)
            record["literal_observations"].append({
                "k": str(k), "left_length": len(left), "right_length": len(right),
                "actual_equal": result, "expected_membership": expected,
            })
            max_length = max(max_length, len(left), len(right))
            sample_count += 1
        if candidate is not None:
            assert case.name in candidate, ("候选结果缺少场景", case.name)
            witness = union_disagreement(case.expected, candidate[case.name])
            assert witness is None, ("候选区间并与预期不等", case.name, str(witness))
            record["candidate_union_matches_expected"] = True
        report["cases"].append(record)
    report.update({"status": "PASS", "case_count": len(selected),
                   "literal_sample_count": sample_count, "maximum_expanded_word_length": max_length})
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    if args.export_cases:
        args.export_cases.write_text(json.dumps({
            "integer_encoding": "coefficients, parameters, endpoints use decimal strings",
            "cases": [case_record(case) for case in selected],
        }, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: report[key] for key in (
        "status", "case_count", "literal_sample_count", "maximum_expanded_word_length",
        "candidate_output_checked", "script_sha256")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
