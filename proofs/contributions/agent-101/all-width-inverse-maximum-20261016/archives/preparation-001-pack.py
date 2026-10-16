#!/usr/bin/env python3
"""Archive frozen all-width-maximum evidence, only after the review receipt.

The safe path, regular-file, normalized tar/gzip, and restored-input repack
machinery is reused from the earlier final-independent packer. Selection and
receipt checks are specific to this exact 17-module project. No Lean or Git
command is invoked. All inputs remain present and unchanged.
"""

import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import stat
import tarfile


PROJECT = "agent101-all-width-maximum"
PACKET = "proofs/contributions/agent-101/all-width-inverse-maximum-20261016"
REGISTRY = "proofs/Agent101AllWidthMaximum.registry.json"
REGISTRY_SHA = "496908a7d53c6a09b7a82dfae3c5e10339ef699072e5c97c0e591dc4e2c2cfcc"
VERIFIER = "proofs/verify_project__214bf7673efe116b.py"
VERIFIER_SHA = "c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a"
OLD_ARCHIVES = "proofs/contributions/agent-101/protected-numeric-multiplicity-20261016/archives"
OLD_PACKER_SHA = "345e34d541dec68abf22d0fad1ec57fdbb22e9d2c1c65aa0f9fb7bfb38df0a66"
HELPER_SHA = "8022d9a0c75bce41048a0fee59a1878f431d52e5f80eeb1d6fce00ce09ba6e76"
ARCHIVE = "final-independent.tar.gz"
MANIFEST = "final-independent-manifest.json"
EXCLUDED_PARTS = {"__pycache__", ".cache", "cache", ".lake"}
EXCLUDED_ENDINGS = (".olean", ".olean.tmp", ".ilean", ".ilean.tmp", ".pyc", ".pyo",
                    ".o", ".a", ".so", ".dylib", ".dll")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_name(name):
    p = PurePosixPath(name)
    if not name or "\\" in name or "\0" in name or p.is_absolute():
        raise ValueError("Invalid archive path: " + name)
    if p.as_posix() != name or any(s in (".", "..") for s in p.parts):
        raise ValueError("Non-normalized archive path: " + name)
    return p


def read_regular(path):
    if not stat.S_ISREG(path.lstat().st_mode):
        raise ValueError("Expected a regular evidence file: " + str(path))
    return path.read_bytes()


def write_archive(path, rows, contents):
    # Normalize archive metadata; preserve every payload byte, including empty logs.
    with path.open("xb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, compresslevel=9, mtime=0) as gz:
            with tarfile.open(fileobj=gz, mode="w", format=tarfile.PAX_FORMAT) as tar:
                for row in sorted(rows, key=lambda r: r["path"]):
                    name = row["path"]
                    safe_name(name)
                    info = tarfile.TarInfo(name)
                    info.size = row["bytes"]
                    info.mode = 0o644
                    info.uid = info.gid = info.mtime = 0
                    info.uname = info.gname = ""
                    info.type = tarfile.REGTYPE
                    tar.addfile(info, io.BytesIO(contents[name]))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def regular_paths(root):
    paths = []
    for path in sorted(root.rglob("*")):
        mode = path.lstat().st_mode
        if stat.S_ISDIR(mode):
            continue
        require(stat.S_ISREG(mode), "Non-regular evidence: " + str(path))
        paths.append(path)
    return paths


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=here.parents[4])
    parser.add_argument("--canonical-root", type=Path)
    parser.add_argument("--source-commit", help="Full published source/registry commit recorded by the canonical run")
    parser.add_argument("--receipt", type=Path, help="Final frozen reviewer receipt; wait until the reviewer has stopped writing")
    parser.add_argument("--receipt-sha256", help="Exact final receipt hash supplied by the reviewer")
    parser.add_argument("--output-dir", type=Path, default=here)
    parser.add_argument("--repack-from-root", type=Path)
    parser.add_argument("--manifest", type=Path, default=here / MANIFEST)
    args = parser.parse_args()
    out = args.output_dir.absolute()
    out.mkdir(parents=True, exist_ok=True)
    archive = out / ARCHIVE
    require(not archive.exists(), "Refusing to overwrite an existing archive: " + str(archive))

    if args.repack_from_root is not None:
        manifest = json.loads(args.manifest.read_text())
        rows = manifest["members"]
        contents = {}
        for row in rows:
            name = row["path"]
            path = args.repack_from_root.joinpath(*safe_name(name).parts)
            data = read_regular(path)
            require(len(data) == row["bytes"] and digest(data) == row["sha256"],
                    "Restored source differs from the manifest: " + name)
            require(name not in contents, "Duplicate manifest member: " + name)
            contents[name] = data
        write_archive(archive, rows, contents)
        actual = digest(read_regular(archive))
        require(actual == manifest["archive"]["sha256"],
                "Repacked archive bytes differ; retain the result for diagnosis")
        print(json.dumps({"status": "PASS", "mode": "repack", "archive_sha256": actual,
                          "archive_bytes": archive.stat().st_size, "members": len(rows)}))
        return

    require(args.canonical_root is not None and args.receipt is not None,
            "Initial packing requires the frozen canonical directory and final reviewer receipt")
    require(re.fullmatch(r"[0-9a-f]{40}", args.source_commit or "") is not None,
            "Initial packing requires the exact full source/registry commit")
    require(re.fullmatch(r"[0-9a-f]{64}", args.receipt_sha256 or "") is not None,
            "Initial packing requires the reviewer's final receipt SHA256")
    manifest_path = out / MANIFEST
    require(not manifest_path.exists(), "Refusing to overwrite an existing manifest")
    repo = args.repo_root.absolute()
    canonical = args.canonical_root.absolute()
    reviews = repo / PACKET / "reviews"
    receipt_path = args.receipt.absolute()
    require(receipt_path.is_relative_to(reviews), "Final receipt must reside in the owned review packet")
    receipt_bytes = read_regular(receipt_path)
    require(digest(receipt_bytes) == args.receipt_sha256, "Final receipt hash changed")
    receipt = json.loads(receipt_bytes)
    require(receipt.get("result", receipt.get("status")) == "PASS", "Review is not final PASS")
    require(receipt["source_commit"] == args.source_commit, "Reviewer source commit mismatch")
    canonical_bytes = read_regular(canonical / "verification.json")
    canonical_report = json.loads(canonical_bytes)
    project = canonical_report["projects"][PROJECT]
    require(canonical_report["status"] == project["status"] == "PASS", "Canonical run is not final PASS")
    require(canonical_report["source_commit"] == args.source_commit, "Canonical source commit mismatch")
    require(canonical_report["registry_sha256"] == REGISTRY_SHA, "Canonical registry pin changed")
    require(len(project["build_order"]) == len(project["sources"]) == 17, "Expected the complete 17-module closure")
    require(project["theorem_count"] > 0, "Missing exhaustive module-origin theorem audit")
    require(all(command["exit_code"] == 0 for command in project["commands"]), "A canonical command did not pass")
    require(canonical_bytes == read_regular(reviews / "final-canonical-verification.json"),
            "Canonical report and frozen reviewer copy differ")
    canonical_files_bytes = read_regular(canonical / "FILES.json")
    require(canonical_files_bytes == read_regular(reviews / "final-canonical-FILES.json"),
            "Canonical FILES and frozen reviewer copy differ")
    canonical_files = json.loads(canonical_files_bytes)
    require(not any(name.endswith((".olean", ".ilean")) for name in canonical_files),
            "Unexpected compiler-object entry in original FILES inventory")
    for name, rec in canonical_files.items():
        data = read_regular(canonical.joinpath(*safe_name(name).parts))
        require(len(data) == rec["bytes"] and digest(data) == rec["sha256"],
                "Original FILES inventory no longer matches canonical bytes: " + name)
    registry_bytes = read_regular(repo / REGISTRY)
    require(digest(registry_bytes) == REGISTRY_SHA, "Registry hash mismatch")
    registry = json.loads(registry_bytes)
    module_records = registry["projects"][PROJECT]["modules"]
    require(set(module_records) == set(project["sources"]), "Canonical/registry closure differs")
    require(digest(read_regular(repo / VERIFIER)) == VERIFIER_SHA, "Original verifier changed")
    inventory = json.loads(read_regular(repo / PACKET / "PUBLIC_EXPORTS.json"))
    require(inventory["public_declaration_count"] == 41 and inventory["theorem_count"] == 36
            and inventory["definition_count"] == 5, "Public declaration inventory changed")
    require(read_regular(here / "final-independent-verify.py") ==
            read_regular(repo / OLD_ARCHIVES / "final-independent-verify.py"), "Safe extraction helper changed")
    require(digest(read_regular(here / "final-independent-verify.py")) == HELPER_SHA, "Helper pin mismatch")
    require(digest(read_regular(repo / OLD_ARCHIVES / "final-independent-pack.py")) == OLD_PACKER_SHA,
            "Referenced original packer changed")

    rows, contents, origins, exclusions = [], {}, {}, []

    def add(path, name, group, kind, origin_path):
        safe_name(name)
        require(name not in contents, "Duplicate requested archive member: " + name)
        data = read_regular(path)
        rows.append({"path": name, "bytes": len(data), "sha256": digest(data), "group": group,
                     "origin": {"kind": kind, "path": origin_path}})
        contents[name] = data
        origins[name] = path

    def add_repo(path, group):
        name = path.relative_to(repo).as_posix()
        add(path, name, group, "repository", name)

    for module, rec in module_records.items():
        data = read_regular(repo / rec["path"])
        require(digest(data) == rec["sha256"], "Published input hash mismatch: " + module)
        require(project["sources"][module]["sha256"] == rec["sha256"], "Canonical input identity mismatch")
        built = canonical / PROJECT / "source" / (module.replace(".", "/") + ".lean")
        require(digest(read_regular(built)) == project["sources"][module]["build_sha256"],
                "Actual canonical module changed: " + module)
        require(read_regular(built) == data, "Unexpected adapter or source rewrite in this direct-foundation project")
        add_repo(repo / rec["path"], "published-source")

    replay_paths = [REGISTRY, VERIFIER, "proofs/Agent101Nonpalindromic.registry.json",
                    PACKET + "/PUBLIC_EXPORTS.json", PACKET + "/make_registry.py", PACKET + "/REGISTRY.md",
                    PACKET + "/claim-receipt.json", PACKET + "/DEPENDENCIES.json",
                    PACKET + "/bounds/dependencies/agent2/PROVENANCE.json",
                    "proofs/contributions/agent-101/all-width-max-scout-20261016/source-provenance.json"]
    for name in replay_paths:
        add_repo(repo / name, "published-replay-input")

    canonical_prefix = PACKET + "/archives/final-independent-canonical"
    canonical_initial = regular_paths(canonical)
    reviews_initial = regular_paths(reviews)
    for root, paths, kind in ((canonical, canonical_initial, "canonical"),
                              (reviews, reviews_initial, "repository")):
        for path in paths:
            rel = path.relative_to(root)
            if any(part in EXCLUDED_PARTS for part in rel.parts) or path.name.endswith(EXCLUDED_ENDINGS):
                exclusions.append({"kind": kind, "path": rel.as_posix() if kind == "canonical"
                                   else path.relative_to(repo).as_posix()})
                continue
            if kind == "repository":
                add_repo(path, "independent-review")
            else:
                group = "canonical-source" if path.suffix == ".lean" else (
                    "canonical-log" if path.suffix == ".log" else "canonical-report-and-other-evidence")
                add(path, canonical_prefix + "/" + rel.as_posix(), group, kind, rel.as_posix())

    helpers = [here / name for name in ("final-independent-pack.py", "final-independent-verify.py",
                                      "final-independent-validate.py")]
    for path in helpers:
        add_repo(path, "archiving-script")
    rows.sort(key=lambda row: row["path"])
    require(receipt_path.relative_to(repo).as_posix() in contents, "Final receipt was not selected")
    write_archive(archive, rows, contents)
    for row in rows:
        require(read_regular(origins[row["path"]]) == contents[row["path"]],
                "An input changed during packing; retain the archive for diagnosis")
    require(regular_paths(canonical) == canonical_initial and regular_paths(reviews) == reviews_initial,
            "Evidence directory contents changed during packing; wait for the final freeze")
    groups = {group: sum(row["group"] == group for row in rows)
              for group in sorted({row["group"] for row in rows})}
    manifest = {
        "schema_version": 1, "repository": "taco-jpg/p196-algorithm",
        "source_commit": args.source_commit, "registry_sha256": REGISTRY_SHA,
        "archive": {"filename": ARCHIVE, "bytes": archive.stat().st_size,
                    "sha256": digest(read_regular(archive)), "format": "gzip-compressed PAX tar",
                    "member_count": len(rows), "uncompressed_file_bytes": sum(row["bytes"] for row in rows)},
        "member_path_base": "repository root", "canonical_origin_root": str(canonical),
        "canonical_restored_prefix": canonical_prefix,
        "canonical_path_mapping": "External canonical output is rebased below canonical_restored_prefix with its hierarchy and bytes unchanged. Repository files retain their original repository-relative paths.",
        "frozen_review_receipt": {"path": receipt_path.relative_to(repo).as_posix(),
                                  "sha256": args.receipt_sha256},
        "canonical_result": {"status": project["status"], "modules": 17,
                             "theorem_count": project["theorem_count"], "axiom_union": project["axiom_union"],
                             "original_verifier_commands_explicitly_trust_zero": False,
                             "later_explicit_trust_zero_audits": "Retained verbatim in the frozen independent review evidence; consult its receipt and raw logs."},
        "original_canonical_FILES": {"sha256": digest(canonical_files_bytes),
                                     "entry_count": len(canonical_files), "compiler_object_entries": 0,
                                     "scope": "Original verifier snapshot retained verbatim; later audit/review files may not be indexed by this earlier snapshot."},
        "groups": groups,
        "excluded_policy": {"directory_components": sorted(EXCLUDED_PARTS), "filename_endings": list(EXCLUDED_ENDINGS)},
        "excluded_files": exclusions,
        "published_author_attempts_not_repackaged": {
            "source_commit": "0fcbe9973659f178e9c834c68d45f660241d6fbd",
            "directories": [PACKET + "/" + part for part in ("profile", "bounds", "witnesses", "upper")],
            "scope": "Author attempt trees remain separately published and locally unchanged. Only selected exact dependency/provenance inputs from those trees are needed in this final independent archive."},
        "preservation": "All selected original file bytes remain unchanged. Compiler objects are omitted and explicitly listed separately; the original FILES inventory has no compiler-object entries. No Lean or Git command is run by packaging.",
        "archive_metadata_policy": "Sorted regular members; mode 0644; uid/gid/mtime zero; blank owner/group names; gzip filename empty and mtime zero; gzip compression level 9.",
        "reproducibility": "Use --repack-from-root with a restored repository root and this manifest to reproduce and check identical tar.gz bytes in a new output directory.",
        "machinery_reuse": {"original_packer_path": OLD_ARCHIVES + "/final-independent-pack.py",
                            "original_packer_sha256": OLD_PACKER_SHA,
                            "packer_scope": "Reused path/regular-file/normalized tar-gzip/repack machinery; final receipt and source selection adapted to this 17-module contribution.",
                            "original_helper_path": OLD_ARCHIVES + "/final-independent-verify.py",
                            "original_helper_sha256": HELPER_SHA,
                            "helper_modifications": "None: exact byte-identical copy, with the same default filenames in a new directory.",
                            "validation_scope": "Same verify-only, one fresh safe extraction, and original-byte comparison recipe; task-specific restore prefix and metadata label updated."},
        "sidecar_helpers": [{"filename": path.name, "bytes": path.stat().st_size,
                             "sha256": digest(read_regular(path))} for path in helpers],
        "members": rows,
    }
    with manifest_path.open("x") as stream:
        json.dump(manifest, stream, indent=2)
        stream.write("\n")
    print(json.dumps({"status": "PASS", "archive": manifest["archive"], "groups": groups,
                      "manifest_sha256": digest(read_regular(manifest_path)), "excluded_count": len(exclusions),
                      "source_commit": args.source_commit, "receipt_sha256": args.receipt_sha256}))


if __name__ == "__main__":
    main()
