#!/usr/bin/env python3
"""Read-only PR137 retained-evidence verification; does not invoke Lean or Git mutations."""
import gzip, hashlib, io, json, re, subprocess, tarfile
from pathlib import Path

REPO = "/workspace/scratch/f8aedc6d7adf/agent6-carry"
REVIEW = Path("/workspace/scratch/f8aedc6d7adf/runtime-agent6/review-carry")
H = "f0e2097b82286128005ba81d8e50f2dca4e2d50b"
F = "affa037ad537f3ae66a97008991850ce397f613a"
B = "dca30e76474569a276c2e58bbd6ee0b96c554ecc"
P = "proofs/contributions/agent-6/normalized-carry-accounting-20261016/"
ALLOWED = {"propext", "Quot.sound", "Classical.choice"}

def git(*args):
    return subprocess.check_output(["git", "-C", REPO, *args])
def read(path, ref=H):
    return git("show", ref + ":" + path)
def sha(data):
    return hashlib.sha256(data).hexdigest()
def blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
def identity(data, record):
    assert len(data) == record["bytes"]
    assert sha(data) == record["sha256"]
    if "git_blob_sha1" in record:
        assert blob(data) == record["git_blob_sha1"]

out = {
    "status": "RUNNING",
    "reviewer": "Agent 19 independent retained-evidence specialist",
    "assignment": "Read-only, nonauthor evidence reuse assessment for delivery owner Agent 19",
    "head": H, "frozen_source": F, "reviewed_base": B,
    "new_lean_execution": False, "source_repairs": [], "remote_mutations": [],
    "original_independent_reviewer": "Agent 6 runtime/reproducibility specialist",
    "original_review": "https://github.com/taco-jpg/p196-algorithm/pull/137#pullrequestreview-5554462051",
    "original_review_account": "sodium-qed",
    "formal_review_event": "COMMENTED; shared-account parent relay, not separate-account approval",
}
remote = json.loads(Path(__file__).with_name("remote-changed-files.json").read_text())
changes = [row.split("\t") for row in git("diff", "--name-status", B, H).decode().splitlines()]
assert len(changes) == len(remote) == 127
assert all(status == "A" and path.startswith(P) for status, path in changes)
assert {path for _, path in changes} == {path for path, _ in remote}
for path, expected in remote:
    data = read(path)
    assert blob(data) == expected
    if path.endswith(".json"):
        json.loads(data)
out["complete_diff"] = {"changed_files": 127, "commits": 2,
    "all_added_under_contribution": True, "remote_file_pages": [100, 27],
    "remote_paths_and_blobs_match_git": True,
    "all_changed_blobs_read_all_json_parsed": True,
    "head_tree": git("rev-parse", H+"^{tree}").decode().strip(),
    "head_parent": git("show", "-s", "--format=%P", H).decode().strip(),
    "evidence_checkpoint_diff_files": len(git("diff", "--name-only", F, H).decode().splitlines())}
assert out["complete_diff"]["head_tree"] == "9473febf64d4fa179473e23db88e17d4d5ac7fe6"
assert out["complete_diff"]["head_parent"] == F

deps = json.loads(read(P+"DEPENDENCIES.json"))
registry = json.loads(read(P+"carry.registry.json"))
modules = registry["projects"]["agent6-normalized-carry-accounting"]["modules"]
assert len(modules) == 21
bound = []
for name, record in modules.items():
    data = read(record["path"])
    assert sha(data) == record["sha256"] and blob(data) == record["git_blob"]
    assert data == read(record["path"], F)
    assert data == read(P+"verification/canonical-published-affa037/agent6-normalized-carry-accounting/source/"+name+".lean")
    assert data == (REVIEW/"final/source"/(name+".lean")).read_bytes()
    if name in deps["unchanged_modules"]:
        assert data == read(record["path"], B)
    bound.append({"module": name, "path": record["path"], "bytes": len(data),
                  "sha256": sha(data), "git_blob": blob(data), "imports": record["imports"]})
for name in ("carry.registry.json", "DEPENDENCIES.json", "replay.py"):
    assert read(P+name) == read(P+name, F)
verifier = deps["repository_verifier"]
assert sha(read(verifier["path"])) == verifier["sha256"]
assert read(verifier["path"]) == read(verifier["path"], B)
out["source_binding"] = {"status": "PASS", "modules": bound,
    "total_source_bytes": sum(x["bytes"] for x in bound),
    "inherited_modules_equal_base": 18,
    "frozen_and_head_and_canonical_and_independent_copies_identical": True,
    "registry_dependencies_replay_unchanged_from_freeze": True,
    "repository_verifier_unchanged_from_base": verifier}

# Verify every evidence member and readable copy against the manifest in Git H.
manifest = json.loads(read(P+"verification/independent/PORTABLE_MANIFEST.json"))
archive_data = read(P+"verification/independent/"+manifest["archive"]["file"])
identity(archive_data, manifest["archive"])
with tarfile.open(fileobj=io.BytesIO(archive_data), mode="r:gz") as archive:
    members = archive.getmembers()
    assert [x.name for x in members] == [x["archive_member"] for x in manifest["included"]]
    for member, record in zip(members, manifest["included"]):
        assert member.isfile() and not member.name.startswith("/") and ".." not in member.name.split("/")
        identity(archive.extractfile(member).read(), record)
        identity(Path(record["original_absolute_path"]).read_bytes(), record)
for record in manifest["readable_copies"]:
    identity(read(P+"verification/independent/"+record["file"]), record)
out["independent_archive"] = {"status": "PASS", **manifest["archive"],
    "members": len(manifest["included"]), "member_bytes": sum(x["bytes"] for x in manifest["included"]),
    "readable_copies": len(manifest["readable_copies"]),
    "original_local_evidence_files_equal_published_manifest": True,
    "excluded_compiled_objects": manifest["excluded_file_count"]}

# Other archives preserve historical scope/ownership evidence, not accepted proof inputs.
archives = json.loads(read(P+"scope/ARCHIVES.json")) + [json.loads(read(P+"scope/FOLLOWUP_PR107_ARCHIVE.json"))]
out["scope_archives"] = []
for record in archives:
    data = read(P+"scope/"+record["archive"])
    identity(data, record)
    uncompressed = gzip.decompress(data)
    assert len(uncompressed) == record["uncompressed_tar_bytes"]
    assert sha(uncompressed) == record["uncompressed_tar_sha256"]
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
        members = archive.getmembers()
        assert [m.name for m in members] == [m["archive_member"] for m in record["members"]]
        for member, rec in zip(members, record["members"]):
            assert member.isfile() and not member.name.startswith("/") and ".." not in member.name.split("/")
            identity(archive.extractfile(member).read(), rec)
    out["scope_archives"].append({"archive": record["archive"], "sha256": sha(data),
        "member_count": len(record["members"]), "status": "PASS"})

# Recheck retained commands/raw log hashes; do not execute compiler.
compilation = json.loads((REVIEW/"final/build/compilation.json").read_text())
audit = json.loads((REVIEW/"final/audit/verification.json").read_text())
assert compilation["status"] == "COMPILED_PENDING_INDEPENDENT_AXIOM_AUDIT"
assert audit["status"] == "PASS"
for rec in compilation["commands"] + audit["commands"]:
    assert rec["exit_code"] == 0
    assert sha((REVIEW/"final"/rec["log"]).read_bytes()) == rec["log_sha256"]
    if rec["label"] in compilation["build_order"] or rec in audit["commands"]:
        assert all(flag in rec["argv"] for flag in ["--trust=0", "-j1", "-DElab.async=false"])
assert len(compilation["build_order"]) == 21
assert compilation["fresh_project_objects"] and not compilation["reused_dependency_objects"]
assert compilation["runner_sha256"] == sha((REVIEW/"compile_exact.py").read_bytes())
assert audit["runner_sha256"] == sha((REVIEW/"audit_final.py").read_bytes())

constants = json.loads((REVIEW/"final/audit/module-constants.json").read_text())
axioms = json.loads((REVIEW/"final/audit/full-module-axioms.json").read_text())
raw = (REVIEW/"final/audit/logs/ModuleAudit.log").read_text()
entries = [(n, [x.strip() for x in v.split(",") if x.strip()])
    for n, v in re.findall(r"^'(.+)' depends on axioms:\s*\[([^\]]*)\]", raw, re.M)]
entries += [(n, []) for n in re.findall(r"^'(.+)' does not depend on any axioms$", raw, re.M)]
printed = dict(entries)
assert len(entries) == len(printed) == len(axioms) == 973
assert set(printed) == {r["name"] for r in axioms}
assert all(set(r["axioms"]) == set(printed[r["name"]]) and set(r["axioms"]) <= ALLOWED for r in axioms)
assert len(constants) == len({r["name"] for r in constants}) == 1437
assert {r["name"] for r in axioms if r["kind"] == "theorem"} == {r["name"] for r in constants if r["kind"] == "theorem"}
literal = json.loads((REVIEW/"final/audit/literal-source-axioms.json").read_text())
assert sum(len(r) for r in literal.values()) == 16
assert all(set(ax) == set(printed[name]) for rec in literal.values() for name, ax in rec.items())
inherited = json.loads((REVIEW/"final/MODULE_ORIGIN_COMPARISON.json").read_text())
assert inherited["status"] == "PASS"
assert all(not inherited[k] for k in ["added_names", "missing_names", "origin_or_kind_changes", "axiom_set_or_origin_changes"])
out["retained_execution"] = {
    "status": "PASS_REVALIDATED", "compiler": compilation["compiler"],
    "commands": compilation["commands"] + audit["commands"],
    "fresh_project_objects": True, "inherited_or_author_objects_reused": False,
    "all_command_log_hashes_and_exit_codes_revalidated": True,
    "module_compiles": 21, "audit_commands": 2, "version_prefix_commands": 2,
    "permitted_axioms": sorted(ALLOWED),
    "theorem_constants": 712, "safe_definitions": 261,
    "printed_structured_axiom_entries_rechecked": 973,
    "module_constants": 1437, "new_literal_receipts": 16,
    "generated_unsafe_implementation_definitions": 428,
    "generated_unsafe_implementation_axioms": 11,
    "unsafe_constants_not_in_accepted_theorem_safe_definition_axiom_chains": True,
    "inherited_comparison": inherited}
out["scope_limits"] = [
    "No fresh Lean execution performed by this specialist.",
    "Exact source/dependency evidence reuse passes; root delivery owner must verify current combined target tree and platform requirements.",
    "COMMENT evidence is nonauthor same-project review, not an external reviewer or separate-account approval.",
    "Checker endpoints remain conditional on original check cert = true; no accepting certificate or integer/196 conclusion.",
    "Failed author attempts remain failures and are excluded from accepted registry/source closure.",
]
out["status"] = "PASS_REUSE_EXACT_HEAD_RETAINED_REVIEW_AND_VERIFICATION"
print(json.dumps(out, indent=2))
