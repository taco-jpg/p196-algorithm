#!/usr/bin/env python3
"""Pin only frozen sources in a scoped registry; this script proves nothing.

All mathematical source hashes, including Graph, are frozen after real author
checks. This is not a replacement or modification of the canonical verifier.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[4]
PROJECT = "agent107-folded-transducer"
NAMESPACE = "Agent107.FoldedTransducer."
FROZEN = {
    "Lychrel196Research": "f8950d138fa4231b536059e2334d36b6496de3d25a806f4cf3925941aa05144c",
    "Agent107TransducerDefs": "5df72daaa1a29f7df4d9b967215b735b7e39ebbd9245d1135d1073473178a530",
    "Agent107TransducerPath": "718a0a82b010f75949e02ed7665e61f1b5014c38c4661726cebd00ac0f6db21c",
    "Agent107TransducerInput": "91fbfa4d00f3c8ef8229c571f26847246b72502a24f4a7bd7de7692f898c873b",
    "Agent107TransducerOutput": "5e71e9bd7a693e19fed7716e71a951d4c06708f42cffc8b1afde4f65aa6e2d67",
    "Agent107TransducerNumeric": "67d88fb4dea6639a0230c5d0f93d8ed778e6393c073679233ab0e792160e086a",
    "Agent107TransducerTablesData": "70bc2285605fb1b581bc0bc14adef8593ee451b312adb5f79fcf19cce83988ef",
    "Agent107TransducerTablesChecks": "3b87f981d86ed80d8870ea627c7459f7b3b0bffa987fe13378b2f29966b3a60b",
    "Agent107TransducerTables": "418febdd3cfcf513b2727543532b00e8add1881c1c826dc8112f96365523c67f",
    "Agent107TransducerReachable": "7e4dc0b05d441f27bc56f96d3c1cdc7fafa59393b5456fc1ad7feaa93180681b",
    "Agent107TransducerBoundary": "cbdc094ba800bf4198bc5a1f2ece8b971aaea91ed2ceb2f1b36a24a978baa89c",
    "Agent107TransducerGraph": "b24422cb928ab6d9abc796478ab6c0c2631106f5c196385646c631a6f310b02a",
}
CLAIMS = {
    "A107-PATH": ["actual_accepts", "accepting_state_eq_actual",
                  "accepting_finitePath_unique", "exists_unique_finitePath"],
    "A107-OUTPUT": ["actual_output_even_no_overflow", "actual_output_even_overflow",
                    "actual_output_odd_no_overflow", "actual_output_odd_overflow",
                    "actual_output", "accepting_output"],
    "A107-INPUT": ["accepts_symmetrize", "foldPrefix_symmetrize", "pathOutput_symmetrize",
                   "reconstructed_admissible", "accepting_input_realizable"],
    "A107-NUMERIC": ["canonical_accepting_step", "canonical_step_path", "accepting_numeric_realizable"],
    "A107-TABLE": ["Table.states_length", "Table.edges_length", "Table.terminals_length",
                   "Table.states_nodup", "Table.edges_nodup", "Table.terminals_nodup",
                   "Table.edge_mem_iff", "Table.terminal_mem_iff", "Table.states_closed"],
    "A107-REACHABLE": ["reachable_iff_mem_states"],
    "A107-BOUNDARY": ["Boundary.initial_no_overflow_sentinel", "Boundary.empty_input_rejected",
                      "Boundary.one_digit_accepts_iff", "Boundary.odd_center_rejected",
                      "Boundary.oversized_center_rejected", "Boundary.first_pair_zero_rejected",
                      "Boundary.odd_overflow_has_extra_pair", "Boundary.accepted_tail_not_unique"],
    "A107-GRAPH": ["accepting_states_mem", "graphAccepts_iff_accepts", "accepting_state_unique",
                   "accepting_finitePath_unique_unrestricted", "indexed_edge_eq", "indexed_terminal_eq",
                   "indexed_accepts", "accepting_indexed_exists", "indexed_output", "nodup_get_injective",
                   "indexed_history_unique", "admissible_unique_history", "indexed_numeric_realizable"],
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "proofs/Agent107Transducer.registry.json")
    args = parser.parse_args()
    roots = ["Agent107TransducerGraph", "Agent107TransducerBoundary"]
    frozen = dict(FROZEN)
    claims = dict(CLAIMS)

    verifier_path = ROOT / "proofs/verify_project__214bf7673efe116b.py"
    spec = importlib.util.spec_from_file_location("agent107_original_verifier", verifier_path)
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    modules = {}

    def visit(name):
        if name in modules:
            return
        if name.split(".")[0] in {"Init", "Std", "Lean"}:
            return
        if name not in frozen:
            raise ValueError("Unfrozen project import: " + name)
        relative = ("proofs/Lychrel196Research__c696e0ea3db39d92.lean" if name == "Lychrel196Research"
                    else "proofs/" + name + ".lean")
        data = (ROOT / relative).read_bytes()
        sha = hashlib.sha256(data).hexdigest()
        if sha != frozen[name]:
            raise ValueError("Frozen source changed: " + relative)
        code = verifier.code_only(data.decode())
        imports = [d for line in re.findall(r"^\s*import\s+([^\n]+)", code, re.M) for d in line.split()]
        modules[name] = {
            "path": relative, "sha256": sha,
            "git_blob": hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest(),
            "imports": imports,
        }
        for dependency in imports:
            visit(dependency)

    for root in roots:
        visit(root)
    registry = {
        "schema_version": 1,
        "catalogue_complete": False,
        "catalogue_blockers": ["此注册表仅覆盖 Agent #107 当前任务，不是全仓库已接受成果目录。"],
        "toolchain": {"version": "4.19.0", "commit": "6caaee842e94",
                      "allowed_axioms": ["propext", "Classical.choice", "Quot.sound"]},
        "projects": {PROJECT: {
            "scope": "原 46 状态 folded transducer 的精确 872 边/251 终止行、完整有限路径、四分支输出和普通正整数一步实现；不提供安全闭合语言或无限不回文结论。",
            "roots": roots, "modules": modules}},
        "claims": [{"id": key, "project": PROJECT, "endpoints": [NAMESPACE + e for e in endpoints]}
                   for key, endpoints in claims.items()],
        "source_baseline": "98d59927ad89c42f438ea857ec5750a0df3b91db",
        "coordination_claim_commit": "fe5a0ef1760a0afa936168ac1cfc52987d28b451",
        "accepted_global_registry_modified": False,
        "registration_status": "SOURCE_PINS_ONLY_NO_VERIFICATION_ASSERTION",
        "pending_roots": [],
        "verification_note": "生成注册表只固定来源与检查目标，不声称该注册表已通过正式验证。作者检查与独立重建证据见任务 README；发布/远端回读由 root 另行记录。",
        "canonical_verifier": {"path": str(verifier_path.relative_to(ROOT)),
                               "sha256": hashlib.sha256(verifier_path.read_bytes()).hexdigest(),
                               "modified": False},
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"registry": str(args.output), "roots": roots, "module_count": len(modules),
                      "endpoint_count": sum(len(c["endpoints"]) for c in registry["claims"]),
                      "pending_roots": registry["pending_roots"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
