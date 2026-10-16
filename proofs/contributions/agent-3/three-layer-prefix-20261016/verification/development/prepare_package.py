#!/usr/bin/env python3
"""Prepare the frozen task-three pins and retain the unchanged guard provenance.

This packaging step uses existing repository bytes. It does not compile proofs,
run the historical generator, invoke Git, or mutate any mathematical source.
"""
from __future__ import annotations

import ast
import difflib
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
VERIFY = HERE.parent
CONTRIBUTION = VERIFY.parent
REPO = HERE.parents[5]
OLD = REPO / "proofs/contributions/agent-3/two-history-20261016/verification"
BASE = "89287c9d3eb7dd801c2b1a59eff03140d47d24ec"
PUBLISHED = "6ce47fddb10f15b4af1025954f1694825093673d"
TREE = "a3448c1d0da258403a3e3f44cd2ca3eeec052da2"
CLAIM = "3fbf616030a09c373b62b285827ff4851ada2052"
OLD_DRIVER_SHA = "bf91485edd05e0afb993f4c67949300ce1251d2d74808d1e0e52dbb97372fdcb"
OLD_MANIFEST_SHA = "055a7a18a87e56c4c786943517874fd7f82b2e4a138f7c9a8bd6846c85948f84"
FROZEN = {
    "DeadPrefix": "09c01111e2eb2f57637fe7d3a04e45aca4ca3d20c0248dc349e956c6ffc1fc64",
    "ActualDepth": "dcc9655c0fe9f60419fc60b821e225f705f3ce713792419586d623125ca9d0e2",
    "SharpHistoryFamily": "6e3b02999b118ed00133d7bebdbf553a6f19d6bfaec4f6abbf982ab7ee2fb002",
    "SharpHistoryTheorem": "d6afdf3e252b1b223ad30548ba6f72a3ba17604dfba43563ea28a5a9435a2f29",
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def save_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def reduced_ast(source: str) -> str:
    tree = ast.parse(source)
    assert isinstance(tree.body[0], ast.Expr)
    assert isinstance(tree.body[0].value, ast.Constant)
    assert isinstance(tree.body[0].value.value, str)
    del tree.body[0]
    tree.body = [node for node in tree.body if not (
        isinstance(node, ast.Assign)
        and len(node.targets) == 1
        and isinstance(node.targets[0], ast.Name)
        and node.targets[0].id == "AUDIT_NAMESPACES"
    )]
    return ast.dump(tree, include_attributes=False)


def main() -> None:
    old_bytes = (OLD / "verify.py").read_bytes()
    old_manifest_bytes = (OLD / "source-pins.json").read_bytes()
    assert sha(old_bytes) == OLD_DRIVER_SHA
    assert sha(old_manifest_bytes) == OLD_MANIFEST_SHA
    previous = old_bytes.decode()
    old_description = "Rebuild the pinned Agent #3 two-history proof and audit every declaration."
    new_description = "Rebuild the pinned Agent #3 three-layer proof and audit every declaration."
    old_namespaces = 'AUDIT_NAMESPACES = {"P196.Agent3.OverflowHorizon", "P196.Agent3.TwoHistory"}'
    new_namespaces = 'AUDIT_NAMESPACES = {"P196.Agent3.OverflowHorizon", "P196.Agent3.TwoHistory", "P196.Agent3.ThreeLayer"}'
    assert previous.count(old_description) == 1
    assert previous.count(old_namespaces) == 1
    current = previous.replace(old_description, new_description).replace(old_namespaces, new_namespaces)
    assert current.replace(new_description, old_description).replace(new_namespaces, old_namespaces) == previous
    assert reduced_ast(current) == reduced_ast(previous)
    (VERIFY / "verify.py").write_text(current)
    (VERIFY / "verify.py").chmod(0o755)
    (HERE / "driver-adaptation.diff").write_text("".join(difflib.unified_diff(
        previous.splitlines(keepends=True), current.splitlines(keepends=True),
        fromfile="two-history-20261016/verification/verify.py",
        tofile="three-layer-prefix-20261016/verification/verify.py",
    )))
    backup = HERE / "README-before-packaging.md"
    if not backup.exists():
        shutil.copyfile(CONTRIBUTION / "README.md", backup)

    spec = importlib.util.spec_from_file_location("frozen_depth_verifier", VERIFY / "verify.py")
    assert spec and spec.loader
    driver = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(driver)
    manifest = json.loads(old_manifest_bytes)
    manifest["contribution"] = "Agent #3 exact two zero-carry layers for a protected finite-horizon subfamily, 2026-10-16"
    manifest["source_base_commit"] = BASE
    manifest["mathematical_source_commit"] = PUBLISHED
    manifest["mathematical_source_tree"] = TREE
    manifest["inherited_two_history_source_commit"] = "a5d84665cfe4897387d80178fbcce79cd128c23e"
    manifest["claim_commit"] = CLAIM
    manifest["claim_blob"] = "be0cafbb0173110b2ffc14617401885a015ce8fa"
    manifest["inherited_safe_image_note"] = manifest.pop("source_note")
    preservation = json.loads((CONTRIBUTION / "source-preservation/source_identity.json").read_text())
    assert preservation["status"] == "PASS"
    historical = []
    for record in preservation["sources"]:
        source = CONTRIBUTION / "source-preservation" / record["filename"]
        data = source.read_bytes()
        assert sha(data) == record["sha256"]
        assert blob(data) == record["git_blob"]
        historical.append({
            "source": str(source.relative_to(REPO)),
            "sha256": sha(data), "git_blob": blob(data), "bytes": len(data),
            "source_commit": PUBLISHED,
            "archive_snapshot": record["archive_snapshot"],
            "archive_path": record["archive_path"],
            "verification_scope": "Original-byte source identity; no historical generator execution or full-graph verification.",
        })
    manifest["source_note"] = historical[0]
    manifest["historical_sources"] = historical
    manifest["audit_namespaces"] = sorted(driver.AUDIT_NAMESPACES)

    assert len(manifest["modules"]) == 23
    for record in manifest["modules"]:
        data = (REPO / record["source"]).read_bytes()
        assert sha(data) == record["sha256"], record["module"]
        assert blob(data) == record["git_blob"], record["module"]
        if record.get("generation") == "two_history":
            record.setdefault("source_commit", "a5d84665cfe4897387d80178fbcce79cd128c23e")
        record.setdefault("source_commit", BASE)

    for module, expected in FROZEN.items():
        path = CONTRIBUTION / (module + ".lean")
        data = path.read_bytes()
        assert sha(data) == expected, module
        code = driver.code_only(data.decode())
        driver.source_scan(code)
        declarations = driver.source_declarations(code)
        manifest["modules"].append({
            "module": module, "source": str(path.relative_to(REPO)),
            "sha256": sha(data), "git_blob": blob(data),
            "role": "contribution", "imports": driver.imports_of(code),
            "source_commit": PUBLISHED, "generation": "three_layer_prefix",
            "exports": [item["name"] for item in declarations if not item["private"]],
            "explicit_declarations": [{key: item[key] for key in ("name", "kind", "private")}
                                      for item in declarations],
        })
    manifest["pinned_module_count"] = 27
    manifest["audited_module_count"] = 17
    manifest["explicit_declaration_count"] = 231
    contributions = [record for record in manifest["modules"] if record["role"] == "contribution"]
    assert len(contributions) == 17
    assert sum(len(record["explicit_declarations"]) for record in contributions) == 231
    assert sum(item["private"] for record in contributions for item in record["explicit_declarations"]) == 3
    available = {"Std"}
    for record in manifest["modules"]:
        code = driver.code_only((REPO / record["source"]).read_text())
        driver.source_scan(code)
        assert driver.imports_of(code) == record["imports"]
        assert set(record["imports"]) <= available
        available.add(record["module"])
    save_json(VERIFY / "source-pins.json", manifest)

    retained = []
    for filename in ("check_verifier_guards.py", "verifier-guard-checks.json", "verifier-guard-checks.log"):
        source = OLD / "development" / filename
        destination = HERE / ("inherited-" + filename)
        shutil.copyfile(source, destination)
        retained.append({"source": str(source.relative_to(REPO)),
                         "source_commit": BASE, "retained": str(destination.relative_to(VERIFY)),
                         "sha256": sha(destination.read_bytes())})
    checks = json.loads((HERE / "inherited-verifier-guard-checks.json").read_text())
    assert checks["result"] == "PASS" and len(checks["checks"]) == 14
    assert checks["verifier_sha256"] == OLD_DRIVER_SHA
    assert all(item["result"] == "PASS" for item in checks["checks"])
    save_json(HERE / "verifier-provenance.json", {
        "status": "PASS",
        "verification_scope": "Driver adaptation provenance; inherited guard outcomes are not a fresh test run.",
        "driver_predecessor": {"source": str((OLD / "verify.py").relative_to(REPO)),
                               "source_commit": BASE, "sha256": OLD_DRIVER_SHA},
        "manifest_predecessor": {"source": str((OLD / "source-pins.json").relative_to(REPO)),
                                 "source_commit": BASE, "sha256": OLD_MANIFEST_SHA},
        "current_driver_sha256": sha((VERIFY / "verify.py").read_bytes()),
        "current_manifest_sha256": sha((VERIFY / "source-pins.json").read_bytes()),
        "allowed_changes": ["Module docstring describes the three-layer contribution.",
                            "AUDIT_NAMESPACES adds P196.Agent3.ThreeLayer; no existing namespace is removed."],
        "otherwise_byte_identical": True,
        "ast_identical_after_removing_only_module_docstring_and_namespace_assignment": True,
        "acceptance_check_logic_unchanged": True,
        "guard_suite": {"count": 14, "result": "PASS", "fresh_run": False,
                        "tested_driver_sha256": OLD_DRIVER_SHA,
                        "reason_for_reuse": "Every acceptance check is unchanged; only the contribution namespace set is extended.",
                        "retained_original_files": retained},
        "mathematical_source_commit": PUBLISHED,
        "preflight_source_count": 27, "preflight_explicit_declaration_count": 231,
        "new_module_explicit_counts": {record["module"]: len(record["explicit_declarations"])
                                       for record in manifest["modules"][-4:]},
        "preparation_script_sha256": sha(Path(__file__).read_bytes()),
    })
    print(json.dumps({"status": "PASS", "modules": 27, "audited_modules": 17,
                      "explicit_declarations": 231,
                      "driver_sha256": sha((VERIFY / "verify.py").read_bytes()),
                      "manifest_sha256": sha((VERIFY / "source-pins.json").read_bytes())}, indent=2))


if __name__ == "__main__":
    main()
