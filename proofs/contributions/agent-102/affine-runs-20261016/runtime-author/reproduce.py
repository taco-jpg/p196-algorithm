#!/usr/bin/env python3
"""在全新输出目录重放 Agent #102 保存的数学作者检查。"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys


ARCHIVE = Path(__file__).resolve().parent
CASES = {
    "arithmetic-first": (
        "arithmetic/attempt01",
        ["Agent102RunDefs", "Agent102AffineArithmetic"],
        0,
        9,
    ),
    "arithmetic-checkpoint": (
        "arithmetic/checkpoint-build",
        ["Agent102RunDefs", "Agent102AffineArithmetic", "Audit"],
        0,
        17,
    ),
    "boundary-failed": (
        "boundary/attempt01",
        ["Agent102RunDefs", "Agent102RunWord", "Agent102AffineArithmetic", "Agent102AffineBoundary"],
        1,
        None,
    ),
    "boundary-final": (
        "boundary/attempt02",
        ["Agent102RunDefs", "Agent102RunWord", "Agent102AffineArithmetic", "Agent102AffineBoundary"],
        0,
        12,
    ),
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def axiom_entries(log: str) -> list[dict]:
    result = []
    for line in log.splitlines():
        match = re.fullmatch(r"'([^']+)' depends on axioms: \[([^\]]*)\]", line)
        if match:
            result.append({"name": match[1], "axioms": match[2].split(", ") if match[2] else []})
            continue
        match = re.fullmatch(r"'([^']+)' does not depend on any axioms", line)
        if match:
            result.append({"name": match[1], "axioms": []})
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", required=True, type=Path)
    parser.add_argument("--case", required=True, choices=CASES)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    lean = args.lean.resolve()
    output = args.output.resolve()
    if output == ARCHIVE or output.is_relative_to(ARCHIVE):
        parser.error("输出必须位于归档目录之外，以保持原始证据不变。")
    version = subprocess.check_output([str(lean), "--version"], text=True).strip()
    if not re.search(r"version 4\.19\.0,.*commit 6caaee842e94, Release", version):
        parser.error("需要官方 Lean 4.19.0，commit 6caaee842e94，Release。")
    output.mkdir(parents=True, exist_ok=False)
    source = output / "source"
    logs = output / "logs"
    source.mkdir()
    logs.mkdir()
    folder, modules, expected_final_exit, expected_axiom_count = CASES[args.case]
    origins = {item["destination"]: item for item in json.loads((ARCHIVE / "COPY_ORIGINS.json").read_text())}
    report = {
        "status": "RUNNING",
        "case": args.case,
        "evidence_role": "replay_of_author_source",
        "compiler_version": version,
        "compiler_sha256": sha256(lean.read_bytes()),
        "kernel_trust_level": 0,
        "sources": {},
        "commands": [],
        "repository_wide_pass": False,
    }

    def save() -> None:
        (output / "replay.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")

    try:
        for module in modules:
            relative = folder + "/" + module + ".lean"
            data = (ARCHIVE / relative).read_bytes()
            expected = origins[relative]["sha256"]
            if sha256(data) != expected:
                raise ValueError("源文件散列不一致：" + relative)
            (source / (module + ".lean")).write_bytes(data)
            report["sources"][module] = {"archive_path": relative, "sha256": expected}
        environment = os.environ.copy()
        environment["LEAN_PATH"] = str(source)
        last_log = ""
        for index, module in enumerate(modules):
            command = [str(lean), "--trust=0", "-o", module + ".olean", module + ".lean"]
            log_path = logs / (module + ".log")
            with log_path.open("wb") as stream:
                result = subprocess.run(command, cwd=source, env=environment,
                                        stdout=stream, stderr=subprocess.STDOUT, timeout=180)
            data = log_path.read_bytes()
            last_log = data.decode("utf-8", errors="replace")
            expected_exit = expected_final_exit if index == len(modules) - 1 else 0
            report["commands"].append({"argv": command, "exit_code": result.returncode,
                                       "expected_exit_code": expected_exit,
                                       "log": str(log_path.relative_to(output)), "log_sha256": sha256(data)})
            save()
            print(f"{args.case}: {module} 退出 {result.returncode}", flush=True)
            if result.returncode != expected_exit:
                raise RuntimeError("退出码与保存的案例结果不同：" + module)
        if expected_final_exit:
            if not all(token in last_log for token in ["failed to synthesize", "Decidable", ".overlaps"]):
                raise RuntimeError("失败日志未复现原有 overlap/Decidable 错误。")
            report["status"] = "EXPECTED_FAILURE_REPRODUCED"
            report["mathematical_pass"] = False
        else:
            entries = axiom_entries(last_log)
            if len(entries) != expected_axiom_count or len({item["name"] for item in entries}) != len(entries):
                raise RuntimeError("literal 公理输出缺失、重复或数量不符。")
            allowed = {"propext", "Classical.choice", "Quot.sound"}
            if any(set(item["axioms"]) - allowed for item in entries):
                raise RuntimeError("定理含有允许集合外的公理。")
            report["literal_axiom_entries"] = entries
            report["status"] = "PASS"
            report["mathematical_pass"] = True
        save()
        return 0
    except Exception as error:
        report["status"] = "FAIL"
        report["error"] = str(error)
        save()
        print("复现失败：" + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
