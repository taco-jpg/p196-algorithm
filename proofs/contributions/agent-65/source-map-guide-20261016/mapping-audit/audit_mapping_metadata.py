#!/usr/bin/env python3
"""Audit all source-map records against two pinned Git trees; no mapped blob reads.

Outputs a complete structured result and execution metadata in a new directory.
This checks metadata identities and SHA-256 field syntax, not mapped source bytes.
"""
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys

SNAPSHOT = "ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3"
BASELINE = "2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5"
MAP_PATH = "proofs/SOURCE_MAP.json"
EXPECTED_MAP_SHA256 = "f6354e0411bc63c014c1ca0db07352a22f76ec6890417c097639a77c9539f8ba"
MODE_KIND = {"100644": "blob", "100755": "blob", "120000": "blob", "160000": "commit"}
HEX40 = re.compile(r"[0-9a-f]{40}\Z")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")

class ObjectPairs(list):
    """Keep JSON object pairs distinct from arrays until duplicates are audited."""


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path,
                        help="New output directory; must not already exist")
    args = parser.parse_args()
    repo = args.repo.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    started = datetime.now(timezone.utc).isoformat()
    script = Path(__file__).resolve()
    env = dict(os.environ, GIT_NO_LAZY_FETCH="1", GIT_OPTIONAL_LOCKS="0",
               LC_ALL="C", LANG="C")
    commands = []
    issues = []
    stats = {}
    exceptional = {}
    inputs = {}
    result = {
        "audit": "A65-DOC-002 pinned source-map Git metadata audit",
        "snapshot": SNAPSHOT, "baseline": BASELINE, "map_path": MAP_PATH,
        "scope": "Complete map-key, type, path, mode, and Git object identity comparison",
        "not_claimed": ["Full SHA-256 byte audit of mapped sources", "Full original-layout replay",
                        "Wrapper execution", "Mathematical verification", "Lean compilation"],
        "issues": issues, "counts": stats, "exceptional_cases": exceptional,
        "immutable_inputs": inputs,
    }

    def issue(category, **details):
        issues.append(dict(category=category, **details))

    def git(label, arguments, immutable_source=None):
        argv = ["git", "-C", str(repo), *arguments]
        run = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             env=env, check=False)
        record = {"label": label, "argv": argv, "exit_code": run.returncode,
                  "stdout_bytes": len(run.stdout), "stdout_sha256": sha256(run.stdout),
                  "stderr_bytes": len(run.stderr), "stderr_sha256": sha256(run.stderr),
                  "stderr": run.stderr.decode("utf-8", "backslashreplace")}
        if immutable_source is not None:
            record["immutable_input_reference"] = immutable_source
            record["stdout_preservation"] = "Immutable input identified by source, length, and SHA-256; not a per-entry success report."
        else:
            record["stdout"] = run.stdout.decode("utf-8", "backslashreplace")
        commands.append(record)
        if run.returncode:
            raise RuntimeError("Git input command failed: " + label)
        return run.stdout

    def parse_tree(raw, source):
        tree = {}
        if raw and not raw.endswith(b"\0"):
            issue("tree_missing_final_nul", source=source)
        records = raw.split(b"\0")[:-1] if raw.endswith(b"\0") else raw.split(b"\0")
        for index, record in enumerate(records):
            if not record:
                issue("empty_tree_record", source=source, index=index)
                continue
            try:
                head, name = record.split(b"\t", 1)
                mode, kind, oid = head.decode("ascii").split(" ")
                path = name.decode("utf-8")
            except (ValueError, UnicodeError) as exc:
                issue("invalid_tree_record", source=source, index=index,
                      error=str(exc), raw_hex=record.hex())
                continue
            if path in tree:
                issue("duplicate_tree_path", source=source, path=path)
            if mode not in MODE_KIND or MODE_KIND.get(mode) != kind or not HEX40.fullmatch(oid):
                issue("invalid_tree_metadata", source=source, path=path,
                      mode=mode, kind=kind, oid=oid)
            tree[path] = {"mode": mode, "kind": kind, "oid": oid}
        return tree

    def normalize_json(value, location=""):
        if isinstance(value, ObjectPairs):
            obj = {}
            for key, item in value:
                child = location + "/" + key.replace("~", "~0").replace("/", "~1")
                if key in obj:
                    issue("duplicate_json_key", location=location or "/", key=key)
                obj[key] = normalize_json(item, child)
            return obj
        if isinstance(value, list):
            return [normalize_json(item, location + "/" + str(i)) for i, item in enumerate(value)]
        return value

    def valid_path(value, location, allow_empty=False):
        if not isinstance(value, str):
            issue("invalid_path_type", location=location, observed_type=type(value).__name__)
            return False
        if value == "" and allow_empty:
            return True
        parts = value.split("/")
        if not value or value.startswith("/") or any(p in ("", ".", "..", ".git") for p in parts) or "\0" in value:
            issue("unsafe_or_noncanonical_path", location=location, value=value)
            return False
        return True

    status = "ERROR"
    exit_code = 2
    try:
        version = git("git-version", ["--version"]).decode().strip()
        object_format = git("git-object-format", ["rev-parse", "--show-object-format"]).decode().strip()
        if object_format != "sha1":
            raise RuntimeError("Pinned repository requires SHA-1 Git object IDs; observed " + object_format)
        for label, commit in (("snapshot", SNAPSHOT), ("baseline", BASELINE)):
            resolved = git(label + "-commit", ["rev-parse", "--verify", commit + "^{commit}"]).decode().strip()
            if resolved != commit:
                raise RuntimeError("Commit identity changed for " + label)
            tree_oid = git(label + "-tree-id", ["rev-parse", "--verify", commit + "^{tree}"]).decode().strip()
            raw = git(label + "-tree", ["ls-tree", "-r", "-z", "--full-tree", commit],
                      {"commit": commit, "tree_oid": tree_oid, "representation": "git ls-tree -r -z --full-tree"})
            inputs[label + "_tree"] = {"commit": commit, "tree_oid": tree_oid,
                "bytes": len(raw), "sha256": sha256(raw)}
            tree = parse_tree(raw, label)
            if label == "snapshot":
                current_tree = tree
            else:
                baseline_tree = tree
        map_record = current_tree.get(MAP_PATH)
        if map_record is None or map_record["kind"] != "blob":
            raise RuntimeError("Pinned map path is missing or not a blob")
        raw_map = git("source-map-blob", ["cat-file", "blob", SNAPSHOT + ":" + MAP_PATH],
                      {"commit": SNAPSHOT, "path": MAP_PATH, "blob_oid": map_record["oid"]})
        inputs["source_map"] = {"commit": SNAPSHOT, "path": MAP_PATH,
            "mode": map_record["mode"], "blob_oid": map_record["oid"],
            "bytes": len(raw_map), "sha256": sha256(raw_map)}
        if sha256(raw_map) != EXPECTED_MAP_SHA256:
            issue("pinned_map_sha256_mismatch", expected=EXPECTED_MAP_SHA256, actual=sha256(raw_map))
        blob_oid = hashlib.sha1(b"blob " + str(len(raw_map)).encode() + b"\0" + raw_map).hexdigest()
        if blob_oid != map_record["oid"]:
            issue("map_blob_identity_mismatch", expected=map_record["oid"], actual=blob_oid)
        def reject_constant(token):
            raise ValueError("Nonstandard JSON constant: " + token)
        parsed = json.loads(raw_map.decode("utf-8"), object_pairs_hook=ObjectPairs,
                            parse_constant=reject_constant)
        mapping = normalize_json(parsed)
        if not isinstance(mapping, dict):
            raise ValueError("Map root is not an object")
        if mapping.get("base") != BASELINE or not isinstance(mapping.get("base"), str):
            issue("map_base_mismatch", expected=BASELINE, actual=mapping.get("base"))
        paths = mapping.get("paths")
        if not isinstance(paths, dict):
            raise ValueError("Map paths field is not an object")
        keys = set(paths)
        baseline_keys = set(baseline_tree)
        for path in sorted(baseline_keys - keys):
            issue("baseline_path_missing_from_map", path=path)
        for path in sorted(keys - baseline_keys):
            issue("map_path_absent_from_baseline", path=path)
        stats.update(map_entries=len(paths), baseline_entries=len(baseline_tree),
                     current_entries=len(current_tree), map_keys_equal_baseline=(keys == baseline_keys),
                     missing_map_keys=len(baseline_keys - keys), extra_map_keys=len(keys - baseline_keys))
        modes = Counter()
        selections = Counter()
        optional_fields = Counter()
        unknown_fields = Counter()
        selected_by = defaultdict(list)
        symlinks = []
        gitlinks = []
        empty_current = []
        same_current_preserved = []
        null_current = 0
        baseline_identity_matches = 0
        selected_identity_matches = 0
        selected_baseline_identity_matches = 0
        sha256_syntax_valid = 0
        required = {"current", "preserved", "sha256", "mode", "oid"}
        optional = {"english_current", "english_sha256", "english_note"}
        for original, entry in sorted(paths.items()):
            valid_path(original, "paths/" + original)
            if not isinstance(entry, dict):
                issue("invalid_entry_type", path=original, observed_type=type(entry).__name__)
                continue
            missing = sorted(required - set(entry))
            if missing:
                issue("missing_entry_fields", path=original, fields=missing)
            for key in set(entry) - required - optional:
                unknown_fields[key] += 1
            for key in optional & set(entry):
                optional_fields[key] += 1
                if not isinstance(entry[key], str):
                    issue("invalid_optional_field_type", path=original, field=key,
                          observed_type=type(entry[key]).__name__)
            if "english_current" in entry and isinstance(entry["english_current"], str):
                valid_path(entry["english_current"], original + "/english_current")
            if "english_sha256" in entry and (not isinstance(entry["english_sha256"], str) or not HEX64.fullmatch(entry["english_sha256"])):
                issue("invalid_english_sha256_syntax", path=original, value=entry["english_sha256"])
            if ("english_current" in entry) != ("english_sha256" in entry):
                issue("unpaired_english_presentation_fields", path=original)
            current = entry.get("current")
            preserved = entry.get("preserved")
            if current is None:
                null_current += 1
            elif isinstance(current, str):
                valid_path(current, original + "/current", allow_empty=True)
                if current == "":
                    empty_current.append(original)
            else:
                issue("invalid_current_type", path=original, observed_type=type(current).__name__)
            valid_path(preserved, original + "/preserved")
            if isinstance(current, str) and current == preserved:
                same_current_preserved.append(original)
            mode = entry.get("mode")
            oid = entry.get("oid")
            content_hash = entry.get("sha256")
            if not isinstance(mode, str) or mode not in MODE_KIND:
                issue("invalid_map_mode", path=original, value=mode)
            else:
                modes[mode] += 1
            if not isinstance(oid, str) or not HEX40.fullmatch(oid):
                issue("invalid_map_oid", path=original, value=oid)
            if not isinstance(content_hash, str) or not HEX64.fullmatch(content_hash):
                issue("invalid_sha256_syntax", path=original, value=content_hash)
            else:
                sha256_syntax_valid += 1
            baseline = baseline_tree.get(original)
            if baseline is not None:
                if mode == baseline["mode"] and oid == baseline["oid"]:
                    baseline_identity_matches += 1
                else:
                    issue("recorded_baseline_identity_mismatch", path=original,
                          recorded={"mode": mode, "oid": oid}, baseline=baseline)
            # This is deliberately the wrapper's exact effective selection rule.
            selected = entry.get("current") or entry.get("preserved")
            selection = "current" if entry.get("current") else "preserved"
            selections[selection] += 1
            if not isinstance(selected, str):
                issue("invalid_selected_path_type", path=original,
                      observed_type=type(selected).__name__)
                continue
            valid_path(selected, original + "/selected")
            selected_by[selected].append(original)
            selected_record = current_tree.get(selected)
            if selected_record is None:
                issue("selected_path_missing_from_snapshot", path=original, selected=selected)
            else:
                if mode == selected_record["mode"] and oid == selected_record["oid"]:
                    selected_identity_matches += 1
                else:
                    issue("selected_map_identity_mismatch", path=original, selected=selected,
                          recorded={"mode": mode, "oid": oid}, snapshot=selected_record)
                if baseline is not None:
                    if selected_record == baseline:
                        selected_baseline_identity_matches += 1
                    else:
                        issue("selected_baseline_identity_mismatch", path=original,
                              selected=selected, baseline=baseline, snapshot=selected_record)
            if mode in ("120000", "160000"):
                item = {"original": original, "selected": selected, "selection": selection,
                        "mode": mode, "oid": oid, "baseline": baseline,
                        "selected_snapshot": selected_record}
                (symlinks if mode == "120000" else gitlinks).append(item)
        shared = [{"selected": selected, "original_paths": originals}
                  for selected, originals in sorted(selected_by.items()) if len(originals) > 1]
        # Many-to-one selected paths are not automatically an error: exact per-original
        # identities above establish whether sharing is metadata-consistent.
        stats.update(recorded_baseline_identity_matches=baseline_identity_matches,
                     selected_map_identity_matches=selected_identity_matches,
                     selected_baseline_identity_matches=selected_baseline_identity_matches,
                     unique_effective_selected_paths=len(selected_by),
                     selected_path_collision_groups=len(shared),
                     selected_path_collision_entries=sum(len(item["original_paths"]) for item in shared),
                     map_mode_counts=dict(sorted(modes.items())),
                     baseline_mode_counts=dict(sorted(Counter(x["mode"] for x in baseline_tree.values()).items())),
                     current_tree_mode_counts=dict(sorted(Counter(x["mode"] for x in current_tree.values()).items())),
                     selection_counts=dict(sorted(selections.items())), current_null_entries=null_current,
                     sha256_fields_with_valid_syntax=sha256_syntax_valid,
                     optional_field_counts=dict(sorted(optional_fields.items())),
                     unknown_entry_field_counts=dict(sorted(unknown_fields.items())))
        exceptional.update(symlinks=symlinks, gitlinks=gitlinks,
                           empty_current_fallback_paths=empty_current,
                           current_equals_preserved_paths=same_current_preserved,
                           shared_effective_selected_paths=shared,
                           unknown_top_level_fields=sorted(set(mapping) - {"base", "paths"}))
        result["symlink_boundary"] = "Mode 120000 entries are compared as symlink Git blob identities; target text is neither read nor followed."
        result["optional_metadata_boundary"] = "English field types, path syntax, pairing, and digest syntax are checked; English bytes and target existence are outside effective replay selection."
        result["sha256_boundary"] = "Only the source-map JSON blob itself is byte-hashed. Per-entry sha256 fields are syntax-checked, not validated against source bytes."
        result["git_version"] = version
        status = "PASS" if not issues else "FAIL"
        exit_code = 0 if not issues else 1
    except Exception as exc:
        issue("audit_execution_error", error_type=type(exc).__name__, message=str(exc))
    result["status"] = status
    result["issue_count"] = len(issues)
    result["issue_categories"] = dict(sorted(Counter(x["category"] for x in issues).items()))
    finished = datetime.now(timezone.utc).isoformat()
    metadata = {"started_utc": started, "finished_utc": finished,
        "python_version": sys.version, "python_executable": sys.executable,
        "platform": platform.platform(), "script": {"path": str(script),
        "bytes": script.stat().st_size, "sha256": sha256(script.read_bytes())},
        "original_argv": getattr(sys, "orig_argv", None), "script_argv": sys.argv,
        "cwd": str(Path.cwd()), "repo": str(repo), "output": str(output),
        "environment_overrides": {key: env[key] for key in ("GIT_NO_LAZY_FETCH", "GIT_OPTIONAL_LOCKS", "LC_ALL", "LANG")},
        "git_commands": commands,
        "raw_path_notice": "Absolute workspace paths are raw execution provenance, not editorial navigation links.",
        "input_retention": "Immutable Git-derived input streams are identified by exact source ID, length, and SHA-256; full result and all mismatch records are retained without truncation.",
        "exit_code": exit_code}
    for name, document in (("result.json", result), ("run-metadata.json", metadata)):
        with (output / name).open("x", encoding="utf-8", newline="") as stream:
            json.dump(document, stream, indent=2, ensure_ascii=True)
            stream.write("\n")
    print(json.dumps({"status": status, "issue_count": len(issues),
                      "issue_categories": result["issue_categories"], "counts": stats,
                      "result_path": str(output / "result.json"),
                      "run_metadata_path": str(output / "run-metadata.json"),
                      "scope": result["scope"], "not_claimed": result["not_claimed"]},
                     indent=2, ensure_ascii=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
