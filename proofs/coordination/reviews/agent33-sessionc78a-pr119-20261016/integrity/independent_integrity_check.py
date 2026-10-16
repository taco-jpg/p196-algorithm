#!/usr/bin/env python3
"""Independent retained-evidence integrity audit, Agent 33 /root/pr119_evidence_integrity.
No Lean execution, network operation, source mutation, or evidence deletion.
This script reads only Agent 33's owned PR 119 snapshot/evidence; reports JSON on stdout.
"""
from pathlib import Path, PurePosixPath
import collections, hashlib, io, json, lzma, re, tarfile

R = Path("/dev/shm/p196-agent33-c78a2c28e1af")
E = R / "original-independent-evidence119"
S = R / "snapshot119/proofs/contributions/agent-103/residual-five-fibers-20261016"
H = "b235d662ce481cf43f8db1335c18f5993953af9d"
ALLOWED = {"Classical.choice", "Quot.sound", "propext"}
sha = lambda b: hashlib.sha256(b).hexdigest()
blob = lambda b: hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()
load = lambda p: json.loads(p.read_bytes())
def check(ok, obligation):
    if not ok:
        raise AssertionError(obligation)
def identity(b):
    return {"bytes": len(b), "sha256": sha(b), "git_blob": blob(b)}
def mask(text):
    out, i, depth, quoted = [], 0, 0, False
    while i < len(text):
        pair = text[i:i + 2]
        if depth:
            if pair == "/-":
                depth += 1; i += 2; out += [" ", " "]
            elif pair == "-/":
                depth -= 1; i += 2; out += [" ", " "]
            else:
                out.append("\n" if text[i] == "\n" else " "); i += 1
        elif quoted:
            if text[i] == "\\":
                out += [" ", " "]; i += 2
            else:
                quoted = text[i] != '"'
                out.append("\n" if text[i] == "\n" else " "); i += 1
        elif pair == "/-":
            depth = 1; i += 2; out += [" ", " "]
        elif pair == "--":
            end = text.find("\n", i)
            end = len(text) if end < 0 else end
            out += [" "] * (end - i); i = end
        elif text[i] == '"':
            quoted = True; out.append(" "); i += 1
        else:
            out.append(text[i]); i += 1
    check(not depth and not quoted, "Closed Lean comments and strings")
    return "".join(out)
def imports(b):
    return re.findall(r"^\s*import\s+([\w.]+)\s*$", mask(b.decode()), re.M)
def archive_contents(data, mode):
    with tarfile.open(fileobj=io.BytesIO(data), mode=mode) as archive:
        members = archive.getmembers()
        names = [m.name for m in members]
        check(len(names) == len(set(names)), "No duplicate archive member names")
        check(all(m.isfile() and not PurePosixPath(m.name).is_absolute()
                  and ".." not in PurePosixPath(m.name).parts for m in members),
              "Only regular archive members with safe relative paths")
        return {m.name: archive.extractfile(m).read() for m in members}
def parse_raw_audit(data):
    lines = data.decode().splitlines()
    parsed, unsafe, complete, i = {}, [], [], 0
    while i < len(lines):
        line = lines[i]; i += 1
        if not line.strip():
            continue
        if line.startswith("AUDIT_THEOREM "):
            marker, module, name = line.split(" ", 2)
            check(name not in parsed, "Unique theorem constant: " + name)
            result = lines[i]; i += 1
            prefix = "'" + name + "' "
            check(result.startswith(prefix), "Immediate matching theorem axiom output: " + name)
            tail = result[len(prefix):]
            if tail == "does not depend on any axioms":
                used = []
            else:
                check(tail.startswith("depends on axioms: ["), "Axiom output grammar: " + name)
                while not tail.endswith("]"):
                    tail += " " + lines[i]; i += 1
                used = [a.strip() for a in tail[len("depends on axioms: ["):-1].split(",") if a.strip()]
            check(len(used) == len(set(used)) and set(used) <= ALLOWED,
                  "Distinct allowed theorem axioms only: " + name)
            parsed[name] = {"module": module, "axioms": sorted(used)}
        elif line.startswith("UNSAFE_IMPL "):
            marker, module, name = line.split(" ", 2)
            unsafe.append([module, name])
        elif line.startswith("AUDIT_COMPLETE "):
            complete.append(int(line.split()[1]))
        else:
            raise AssertionError("Unrecognized raw audit content: " + line)
    return parsed, unsafe, complete

def main():
    result = {
        "status": "IN_PROGRESS", "reviewer": "Agent #33 /root/pr119_evidence_integrity",
        "role": "Independent nonauthor evidence-integrity reviewer; no source authorship",
        "source_head": H, "fresh_lean_execution": "NOT_RUN",
        "verification_classification": "REUSED_EVIDENCE",
        "scope": "Actual retained archive/source/log byte binding, not a repeated mathematical semantic review."
    }
    archive = (S / "evidence/complete-replay-evidence.tar.xz").read_bytes()
    tar = lzma.decompress(archive)
    check(len(archive) == 139624 and sha(archive) == "1c649565710514ba3896293a5265978c70d98cacf117f2d8eadf43cbd9aac596",
          "Original archive pinned bytes/SHA256")
    check(len(tar) == 3276800 and sha(tar) == "3642091361a51e46c578e9e93b99d75b3aa9653d3796499ee80c92b1c4643a12",
          "Original uncompressed tar pinned bytes/SHA256")
    contents = archive_contents(tar, "r:")
    index = json.loads(contents["FILES.json"])
    check(len(contents) == 143 and len(index) == 142 and set(contents) == set(index) | {"FILES.json"},
          "Exact original archive/index membership")
    actual_names = {str(p.relative_to(E)) for p in E.rglob("*") if p.is_file()}
    check(actual_names == set(contents), "Exact extracted evidence membership")
    for name, data in contents.items():
        check((E / name).read_bytes() == data, "Extracted original byte identity: " + name)
        if name in index:
            check(len(data) == index[name]["bytes"] and sha(data) == index[name]["sha256"],
                  "Original indexed byte length/SHA256: " + name)
    check(sum(map(len, contents.values())) == 3161584, "Original payload byte total")
    nested = {}
    for path in E.rglob("FILES.json"):
        entries = load(path)
        for name, record in entries.items():
            data = (path.parent / name).read_bytes()
            check(len(data) == record["bytes"] and sha(data) == record["sha256"],
                  "Nested FILES record: " + str(path.relative_to(E)) + ":" + name)
        nested[str(path.relative_to(E))] = len(entries)
    result["original_archive"] = {
        "status": "PASS", **identity(archive), "regular_members": 143, "indexed_members": 142,
        "exact_membership": True, "payload_bytes": 3161584,
        "tar_bytes": len(tar), "tar_sha256": sha(tar), "nested_indexes_verified": nested
    }

    dev = (S / "evidence/development-evidence.tar.xz").read_bytes()
    dm = load(S / "evidence/development-evidence.manifest.json")
    check(len(dev) == 121316 == dm["archive_bytes"] and
          sha(dev) == "394bbafb99db5f1e09e656489c5ab884ab246149cef41120336d86e7092084d2" == dm["archive_sha256"],
          "Development archive pinned bytes/SHA256")
    dc = archive_contents(dev, "r:xz")
    check(len(dc) == len(dm["files"]) == dm["file_count"] == 66 and set(dc) == set(dm["files"]),
          "Development exact 66-member/index membership")
    for name, data in dc.items():
        check(len(data) == dm["files"][name]["bytes"] and sha(data) == dm["files"][name]["sha256"],
              "Development indexed bytes/SHA256: " + name)
    historical_failures = {
        name: {"sha256": sha(data), "raw_log": data.decode(errors="replace")}
        for name, data in dc.items()
        if name.endswith(".log") and any(token in data for token in [b"error:", b"failed", b"unsolved goals"])
    }
    result["development_archive"] = {
        "status": "PASS", **identity(dev), "members_verified": 66, "exact_membership": True,
        "historical_failed_log_members_preserved": historical_failures,
        "historical_failure_note": "Failed development logs, including historical sorryAx in bridge attempts, remain preserved outside the accepted build closure."
    }

    manifest = load(R / "source119-byte-manifest.json")
    bm = {entry["path"]: entry for entry in manifest}
    check(len(manifest) == len(bm) == 46, "46 unique PR byte-manifest entries")
    check(set(bm) == {str(p.relative_to(R / "snapshot119")) for p in (R / "snapshot119").rglob("*") if p.is_file()},
          "Exact 46-file PR snapshot membership")
    for path, record in bm.items():
        data = (R / "snapshot119" / path).read_bytes()
        check(identity(data) == {key: record[key] for key in ["bytes", "sha256", "git_blob"]},
              "PR file bytes/SHA256/Git blob: " + path)
    result["final_pr_snapshot"] = {
        "status": "PASS", "files_verified": 46, "exact_membership": True,
        "source_byte_manifest": identity((R / "source119-byte-manifest.json").read_bytes()),
        "head_binding_note": "Root obtained this manifest from exact H; this reviewer independently verifies every local byte/Git-blob match."
    }

    v = load(E / "verification-clean-001/verification.json")
    cs = v["commands"]
    check(len(cs) == len({c["label"] for c in cs}) == 25, "25 unique command records")
    check([c["label"] for c in cs] == ["version", "prefix"] + v["build_order"] + ["AuditAllContributionModules"],
          "Recorded command order exactly version/prefix/22 modules/audit")
    for c in cs:
        check(c["exit_code"] == 0, "Recorded zero command exit: " + c["label"])
        check(sha((E / "verification-clean-001" / c["log"]).read_bytes()) == c["log_sha256"],
              "Actual command log hash: " + c["label"])
        check(c["argv"][0] == v["lean"]["path"], "Exact recorded compiler path: " + c["label"])
        if c["label"] not in ["version", "prefix"]:
            expected = [v["lean"]["path"], "--trust=0", "-j1", "-DElab.async=false"]
            if c["label"] != "AuditAllContributionModules":
                expected += ["-o", c["label"] + ".olean"]
            expected += [c["label"] + ".lean"]
            check(c["argv"] == expected, "Exact compile/audit argv: " + c["label"])
            check(c["environment"]["LEAN_PATH"] == c["cwd"] and c["cwd"].endswith("/verification-clean-001/snapshot"),
                  "Isolated compiled source environment: " + c["label"])
    check((E / "verification-clean-001/logs/version.log").read_text().strip() == v["lean"]["version"] ==
          "Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)",
          "Actual Lean version log")
    check((E / "verification-clean-001/logs/prefix.log").read_text().strip() == v["lean"]["runtime_prefix"],
          "Actual runtime prefix log")
    result["recorded_execution"] = {
        "status": "PASS", "commands": 25, "zero_exits": 25, "actual_logs_verified": 25,
        "module_compilations": 22, "audit_invocations": 1, "version_prefix_queries": 2,
        "compiler_arguments": ["--trust=0", "-j1", "-DElab.async=false"],
        "lean": v["lean"], "started_utc": v["started_utc"], "finished_utc": v["finished_utc"],
        "runtime_binary_hashes_recomputed_now": False,
        "runtime_binary_note": "Runtime binaries and .olean objects are intentionally absent from the archive; original immutable hash records are retained, not presented as fresh binary verification."
    }

    audit_bytes = (E / "verification-clean-001/logs/AuditAllContributionModules.log").read_bytes()
    parsed, unsafe, complete = parse_raw_audit(audit_bytes)
    check(complete == [1812] and len(parsed) == 1812, "Exact raw audit completion/count")
    check(parsed == v["theorems"], "Every raw theorem name/module/axiom-set matches verification report")
    counts = {m: 0 for m in v["build_order"]}
    for entry in parsed.values():
        counts[entry["module"]] += 1
    review = load(E / "non-author-final-review.json")
    check(counts == v["module_theorem_counts"] == review["compiled_module_theorem_counts"],
          "All module theorem counts")
    check(len(unsafe) == len(set(map(tuple, unsafe))) == 33 and unsafe == v["unsafe_implementation_constants"],
          "Exactly 33 distinct raw unsafe implementation axiomInfo entries")
    ledger = load(E / "UNSAFE_IMPLEMENTATIONS.json")
    check(sorted(map(tuple, unsafe)) == sorted((d["module"], d["constant"]) for d in ledger["entries"]),
          "All unsafe ledger entries match actual raw log")
    check(ledger["source_log_sha256"] == sha(audit_bytes), "Unsafe ledger raw-log binding")
    new = set(v["selected_new_modules"])
    check(sum(counts[m] for m in new) == 111 and len(parsed) - 111 == 1701, "111 new and 1701 dependency theorem constants")
    check(sum(m in new for m, n in unsafe) == 3 and sum(m not in new for m, n in unsafe) == 30,
          "3 new and 30 inherited implementation axiomInfo entries")
    union = sorted({a for entry in parsed.values() for a in entry["axioms"]})
    check(union == v["axiom_union"] == review["axiom_union"] == ledger["theorem_transitive_axiom_union"] == sorted(ALLOWED),
          "Exact foundational theorem axiom union")
    check(not {n for m, n in unsafe} & set(union), "No implementation axiom in theorem transitive dependencies")
    for name, entry in review["registry_claim_endpoints_verified_in_actual_full_audit"].items():
        check(parsed[name] == entry, "Registry endpoint exact module/axioms: " + name)
    audit_source = (E / "verification-clean-001/snapshot/AuditAllContributionModules.lean").read_bytes()
    check(sha(audit_source) == v["audit_source_sha256"], "Audit source actual SHA256")
    check("| .axiomInfo v =>" in audit_source.decode() and
          'if v.isUnsafe then logInfo m!"UNSAFE_IMPL {mod} {name}"' in audit_source.decode(),
          "Unsafe ledger classification is axiomInfo/isUnsafe")
    result["raw_audit"] = {
        "status": "PASS", "raw_log": identity(audit_bytes), "audit_source": identity(audit_source),
        "theorem_constants": 1812, "new_module_constants": 111, "dependency_constants": 1701,
        "module_counts": counts, "axiom_union": union, "registry_endpoints_matched": 11,
        "unparsed_nonblank_output": 0, "unsafe_axiomInfo_count": 33,
        "unsafe_axiomInfo_inherited": 30, "unsafe_axiomInfo_new": 3,
        "unsafe_axiomInfo_used_by_theorems": 0,
        "unsafe_scope": "Only ConstantInfo.axiomInfo entries with isUnsafe; not all unsafe defnInfo definitions."
    }

    src = load(S / "SOURCES.json")
    reg = load(S / "BUILD_REGISTRY.json")
    mods = reg["projects"]["agent103-residual-five-fibers"]["modules"]
    rs = load(E / "registry-source-evidence.json")
    freeze = load(E / "source-freeze.json")
    check(set(v["sources"]) == set(mods) == set(src["dependencies"]) | set(src["new_modules"]),
          "All 22 source module sets agree")
    identical = {}
    for name in ["check.py", "SOURCES.json", "BUILD_REGISTRY.json", "FILES.json",
                 "UNSAFE_IMPLEMENTATIONS.json", "non-author-final-review.json", "non-author-final-review.md", "REPRODUCE.md"]:
        data = (E / name).read_bytes()
        check(data == (S / name).read_bytes(), "Original/final exact byte identity: " + name)
        identical[name] = identity(data)
    inv = load(E / "full-build-invocation.json")
    check(inv["observed_process_exit_code"] == 0 and inv["recorded_after_completion"],
          "Full driver process exit zero observed after completion")
    for doc in [v, inv]:
        check(doc["driver_sha256"] == sha((S / "check.py").read_bytes()), "Actual driver hash binding")
        check(doc["manifest_sha256"] == sha((S / "SOURCES.json").read_bytes()), "Actual SOURCES manifest hash binding")
    check(rs["registry_sha256"] == sha((S / "BUILD_REGISTRY.json").read_bytes()), "Actual registry source evidence hash")
    check(inv["started_utc_from_driver"] == v["started_utc"] and inv["finished_utc_from_driver"] == v["finished_utc"],
          "Full driver invocation timestamps")
    theorem_counts, definition_counts, bound, external = {}, {}, [], []
    for module, record in mods.items():
        orig = (E / "verification-clean-001/originals" / (module + ".lean")).read_bytes()
        compiled = (E / "verification-clean-001/snapshot" / (module + ".lean")).read_bytes()
        vr = v["sources"][module]
        sr = (src["dependencies"] | src["new_modules"])[module]
        check(sha(orig) == vr["original_sha256"] == sr["sha256"] and len(orig) == vr["original_bytes"],
              "Original source length/SHA256: " + module)
        check(blob(orig) == vr.get("git_blob", vr.get("git_blob_of_bytes")) == sr.get("git_blob", sr.get("git_blob_of_bytes")),
              "Original source Git blob: " + module)
        check(sha(compiled) == vr["compiled_sha256"] == record["sha256"] and blob(compiled) == record["git_blob"],
              "Compiled source SHA256/Git blob: " + module)
        check(imports(compiled) == vr["imports"] == record["imports"] == sr["imports"],
              "Actual compiled source imports: " + module)
        if module in src["dependencies"]:
            check(imports(orig) == sr["original_imports"], "Actual original dependency imports: " + module)
        if "adapter" not in sr:
            check(orig == compiled, "Unadapted source bytes unchanged: " + module)
        stage = E / "registry-check-only-001/agent103-residual-five-fibers/source" / (module + ".lean")
        check(stage.read_bytes() == compiled, "Compiled and published-path staged source bytes: " + module)
        rr = rs["module_sources"][module]
        check(rr["sha256"] == sha(compiled) and rr["git_blob"] == blob(compiled) and
              rr["registry_path"] == record["path"] and rr["imports"] == imports(compiled),
              "Published-path source evidence record: " + module)
        if record["path"] in bm:
            check((R / "snapshot119" / record["path"]).read_bytes() == compiled,
                  "Exact final PR source bytes: " + module)
            check(bm[record["path"]]["sha256"] == record["sha256"] and bm[record["path"]]["git_blob"] == record["git_blob"],
                  "Final PR byte-manifest registry binding: " + module)
            bound.append(module)
        else:
            external.append({"module": module, "path": record["path"], "sha256": record["sha256"], "git_blob": record["git_blob"]})
        if module in src["new_modules"]:
            check((E / (module + ".lean")).read_bytes() == (S / (module + ".lean")).read_bytes() == orig,
                  "Archived/final/compiled new source bytes: " + module)
            check(freeze["new_modules"][module]["sha256"] == sha(orig) and
                  freeze["new_modules"][module]["git_blob"] == blob(orig), "New source freeze: " + module)
            code = mask(orig.decode())
            theorem_counts[module] = len(re.findall(r"^\s*(?:(?:private|protected)\s+)?theorem\s+", code, re.M))
            definition_counts[module] = len(re.findall(r"^\s*(?:(?:private|protected|noncomputable|unsafe)\s+)*def\s+", code, re.M))
        else:
            fr = freeze["dependency_sources"][module]
            check(fr["sha256"] == sha(orig) and fr["git_blob"] == blob(orig), "Dependency source freeze: " + module)
    check(len(bound) == len(external) == 11, "11 PR and 11 existing-main source partition")
    check(theorem_counts == review["source_theorem_counts"] and sum(theorem_counts.values()) == 63, "63 written theorem declarations")
    check(definition_counts == review["source_definition_counts"] and sum(definition_counts.values()) == 8, "8 written definitions")
    seen, active = set(), set()
    def visit(module):
        if module in seen:
            return
        check(module not in active, "Acyclic imports: " + module)
        active.add(module)
        for dependency in mods[module]["imports"]:
            if dependency not in ["Std", "Init", "Lean"]:
                check(dependency in mods, "Registered source import: " + dependency)
                visit(dependency)
        active.remove(module); seen.add(module)
    roots = reg["projects"]["agent103-residual-five-fibers"]["roots"]
    check(roots == ["ResidualFiveFilteredConclusion"], "Exact sole registry root")
    visit(roots[0])
    check(seen == set(mods), "Sole root reaches all 22 modules")
    positions = {m: i for i, m in enumerate(v["build_order"])}
    for module, record in mods.items():
        for dependency in record["imports"]:
            if dependency in mods:
                check(positions[dependency] < positions[module], "Recorded build topological order: " + module)

    original = (E / "verification-clean-001/originals/Lychrel196Research.lean").read_bytes()
    container = (E / "verification-clean-001/originals/LychrelDigitSums.lean").read_bytes()
    adapter = src["dependencies"]["Lychrel196Research"]["adapter"]
    prefix = adapter["excluded_exact_prefix_utf8"].encode()
    check(original.startswith(prefix) and container.startswith(prefix) and prefix == b"import Std\n", "Foundation import prefix")
    body = original[len(prefix):]
    offset = container.find(body)
    check(container.count(body) == 1 and offset == 329 and container[:offset].count(b"\n") + 1 == 11 and
          len(body) == 177451 and len(body.splitlines(keepends=True)) == 4444, "Unique complete foundation body containment")
    check(sha(body) == "c457c36664c186ce10f38d492460fe67f5318c7edf14ff9b930b00b7f67f3402", "Foundation body SHA256")
    forwarder = (E / "verification-clean-001/snapshot/Lychrel196Research.lean").read_bytes()
    check(forwarder == b"import LychrelDigitSums\n" == adapter["exact_compiled_source_utf8"].encode(), "Exact 24-byte forwarder")
    pre = load(E / "dependency-audit-001/verification.json")
    check(pre["theorems"] == {name: entry for name, entry in parsed.items() if entry["module"] not in src["new_modules"]},
          "All 1701 dependency theorem names/origins/axioms unchanged from preflight")
    ci = load(E / "registry-check-only-invocation.json")
    check(ci["exit_code"] == 0 and ci["registry_sha256"] == sha((S / "BUILD_REGISTRY.json").read_bytes()) and
          ci["log_sha256"] == sha((E / "registry-check-only-001.log").read_bytes()), "Recorded source-only checker exit/log/registry")
    result["source_closure"] = {
        "status": "PASS", "original_and_compiled_modules_verified": 22,
        "staged_registry_sources_verified": 22, "pr_bound_new_and_vendored_modules": bound,
        "existing_main_pins_for_root_to_bind": external, "single_root": roots[0],
        "all_registered_modules_reachable": True, "recorded_build_order_topological": True,
        "written_theorem_counts": theorem_counts, "written_theorem_total": 63, "written_definition_total": 8,
        "identical_archived_and_final_files": identical,
        "full_build_invocation": identity((E / "full-build-invocation.json").read_bytes()),
        "full_build_process_observed_exit": 0, "dependency_preflight_theorems_exact": 1701,
        "registry_check_only": "Recorded exit0, actual log and registry hashes verified; source/import compatibility only, not Lean compilation."
    }
    result["foundation_adapter"] = {
        "status": "PASS", "original_bytes": len(original), "body_bytes": len(body),
        "body_lines": 4444, "body_sha256": sha(body), "unique_container_occurrence": True,
        "container_start_byte_zero_based": offset, "container_start_line_one_based": 11,
        "compiled_forwarder": identity(forwarder), "compiled_forwarder_utf8": forwarder.decode()
    }
    packaging = load(S / "evidence/PACKAGING_FILES.json")
    absent = {name: record for name, record in packaging.items() if not (S / "evidence" / name).is_file()}
    result["packaging_receipt_inventory"] = {
        "unpublished_helper_entries": absent,
        "original_runtime_evidence_complete": True,
        "original_mathematical_review_retained": ["non-author-final-review.md", "non-author-final-review.json"],
        "all_seven_module_review_jsons_retained": all((E / "reviews" / (m + ".review.json")).is_file() for m in src["new_modules"]),
        "assessment": "These helper entries are outside the original 142-entry evidence index. No missing accepted-source, raw compiler log, full theorem audit, or original semantic review was found. Their absence from this package does not invalidate the verified mathematical evidence."
    }
    result["limitations"] = [
        "No fresh Lean execution was requested or performed; all kernel runtime results are retained original nonauthor evidence.",
        "Root must maintain current remote H binding, fresh main 11-source pin binding, combined-tree validity, platform gates, and target ownership.",
        "This reviewer did not reverify omitted toolchain binaries or .olean objects and does not claim repository-wide execution.",
        "The 33-entry unsafe ledger covers axiomInfo/isUnsafe only, not all unsafe definitions.",
        "Historical failed development logs remain intact and are not accepted theorem evidence."
    ]
    result["conclusion"] = (
        "PASS_REUSED_EVIDENCE_FOR_BYTE_IDENTICAL_SOURCE_CLOSURE: actual retained source, commands, logs, "
        "audit results, manifests and original independent review are mutually byte-bound. The evidence "
        "qualifies for reuse for the unchanged 22-module closure, with current PR/main binding handled by "
        "the delivery owner. Fresh execution is NOT_RUN."
    )
    result["status"] = "PASS"
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
