#!/usr/bin/env python3
"""Package the frozen final independent evidence, or reproduce its tar bytes."""

import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import stat
import tarfile


COMMIT = "71691d50497edc83247b3571af276bb0ee438491"
REGISTRY_SHA = "04aba56fc69ef566d32b0c1064a4db2298f095d88e98fcd9fefe7f5c70614307"
ARCHIVE = "final-independent.tar.gz"
MANIFEST = "final-independent-manifest.json"
EXCLUDED_PARTS = {"__pycache__", ".cache", "cache", ".lake", "counts-build"}
EXCLUDED_ENDINGS = (".olean", ".olean.tmp", ".ilean", ".ilean.tmp", ".pyc", ".pyo")


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


def main():
    here = Path(__file__).resolve().parent
    default_repo = here.parents[4]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=default_repo)
    parser.add_argument("--canonical-root", type=Path,
                        default=Path("/workspace/scratch/2a8a87fd78df/agent101-final-family-independent-71691d5"))
    parser.add_argument("--output-dir", type=Path, default=here)
    parser.add_argument("--repack-from-root", type=Path,
                        help="Recreate exactly the member set in --manifest from a restored repository root")
    parser.add_argument("--manifest", type=Path, default=here / MANIFEST)
    args = parser.parse_args()
    out = args.output_dir.absolute()
    out.mkdir(parents=True, exist_ok=True)
    archive = out / ARCHIVE
    if archive.exists():
        raise SystemExit("Refusing to overwrite an existing archive: " + str(archive))

    if args.repack_from_root is not None:
        manifest = json.loads(args.manifest.read_text())
        rows = manifest["members"]
        contents = {}
        for row in rows:
            name = row["path"]
            path = args.repack_from_root.joinpath(*safe_name(name).parts)
            data = read_regular(path)
            if len(data) != row["bytes"] or digest(data) != row["sha256"]:
                raise ValueError("Restored source differs from the manifest: " + name)
            if name in contents:
                raise ValueError("Duplicate manifest member: " + name)
            contents[name] = data
        write_archive(archive, rows, contents)
        actual = digest(archive.read_bytes())
        if actual != manifest["archive"]["sha256"]:
            raise ValueError("Repacked archive bytes differ; retain the result for diagnosis")
        print(json.dumps({"status": "PASS", "mode": "repack", "archive_sha256": actual,
                          "archive_bytes": archive.stat().st_size, "members": len(rows)}))
        return

    manifest_path = out / MANIFEST
    if manifest_path.exists():
        raise SystemExit("Refusing to overwrite an existing manifest: " + str(manifest_path))
    repo = args.repo_root.absolute()
    canonical = args.canonical_root.absolute()
    contribution_rel = Path("proofs/contributions/agent-101/protected-numeric-multiplicity-20261016")
    contribution = repo / contribution_rel
    reviews = contribution / "reviews"
    canonical_prefix = (contribution_rel / "archives/final-independent-canonical").as_posix()
    receipt = json.loads(read_regular(reviews / "final-verification.json"))
    canonical_bytes = read_regular(canonical / "verification.json")
    canonical_report = json.loads(canonical_bytes)
    project = canonical_report["projects"]["agent101-protected-family"]
    assert receipt["result"] == canonical_report["status"] == project["status"] == "PASS"
    assert receipt["source_commit"] == canonical_report["source_commit"] == COMMIT
    assert canonical_report["registry_sha256"] == REGISTRY_SHA
    assert len(project["build_order"]) == 26 and project["theorem_count"] == 1783
    assert receipt["public_declarations"] == 94
    assert canonical_bytes == read_regular(reviews / "final-canonical-verification.json")
    assert read_regular(canonical / "FILES.json") == read_regular(reviews / "final-canonical-FILES.json")
    assert digest(read_regular(repo / "proofs/Agent101ProtectedFamily.registry.json")) == REGISTRY_SHA
    readback = json.loads(read_regular(reviews / "final-source-readback.json"))
    assert digest(read_regular(repo / readback["verifier_path"])) == readback["verifier_sha256"]

    rows, contents, origins, exclusions = [], {}, {}, []

    def add(path, name, group, kind, origin_path):
        safe_name(name)
        if name in contents:
            raise ValueError("Duplicate requested archive member: " + name)
        data = read_regular(path)
        row = {"path": name, "bytes": len(data), "sha256": digest(data), "group": group,
               "origin": {"kind": kind, "path": origin_path}}
        rows.append(row)
        contents[name] = data
        origins[name] = path

    def add_repo(path, group):
        name = path.relative_to(repo).as_posix()
        add(path, name, group, "repository", name)

    # Preserve the original published inputs at their original repository paths.
    for module, rec in project["sources"].items():
        path = repo / rec["path"]
        assert digest(read_regular(path)) == rec["sha256"]
        add_repo(path, "published-source")
        built = canonical / "agent101-protected-family/source" / (module + ".lean")
        assert digest(read_regular(built)) == rec["build_sha256"]
    for name in ("proofs/Agent101ProtectedFamily.registry.json", "proofs/verify_project__214bf7673efe116b.py"):
        add_repo(repo / name, "published-replay-input")

    # Keep the actual canonical build inputs, including its foundation adapter.
    canonical_source_names, canonical_log_names = [], []
    for path in sorted(canonical.rglob("*")):
        st = path.lstat()
        rel = path.relative_to(canonical)
        if stat.S_ISDIR(st.st_mode):
            continue
        if not stat.S_ISREG(st.st_mode):
            raise ValueError("Non-regular canonical evidence: " + str(path))
        if any(p in EXCLUDED_PARTS for p in rel.parts) or path.name.endswith(EXCLUDED_ENDINGS):
            exclusions.append({"kind": "canonical", "path": rel.as_posix()})
            continue
        if path.suffix == ".lean" and rel.parent.as_posix() == "agent101-protected-family/source":
            group = "canonical-source"
            canonical_source_names.append(path.name)
        elif path.suffix == ".log" and rel.parent.as_posix() == "agent101-protected-family/logs":
            group = "canonical-log"
            canonical_log_names.append(path.name)
        elif rel.as_posix() in ("verification.json", "FILES.json"):
            group = "canonical-report"
        else:
            raise ValueError("Unexpected file in frozen canonical evidence: " + rel.as_posix())
        add(path, canonical_prefix + "/" + rel.as_posix(), group, "canonical", rel.as_posix())
    expected_sources = {m + ".lean" for m in project["build_order"]} | {"ProjectAudit.lean", "FinalPublicAudit.lean"}
    assert set(canonical_source_names) == expected_sources and len(canonical_source_names) == 28
    assert set(canonical_log_names) == {m + ".log" for m in project["build_order"]} | {"ProjectAudit.log"}
    assert len(canonical_log_names) == 27

    # Preserve existing final receipts and audits without changing their paths.
    for prefix in sorted(reviews.glob("final-*")):
        candidates = sorted(prefix.rglob("*")) if prefix.is_dir() else [prefix]
        for path in candidates:
            st = path.lstat()
            if stat.S_ISDIR(st.st_mode):
                continue
            if any(s in EXCLUDED_PARTS for s in path.relative_to(reviews).parts) or path.name.endswith(EXCLUDED_ENDINGS):
                exclusions.append({"kind": "repository", "path": path.relative_to(repo).as_posix()})
                continue
            add_repo(path, "final-independent-review")

    # Include the complete incremental nonpalindromic review and its input receipts.
    selected_counts = sorted(reviews.glob("counts-nonpalindromic-*"))
    assert len(selected_counts) == 6
    for module in ("Agent101NonpalindromicFibers", "Agent101ProtectedNonpalindromic"):
        selected_counts += [reviews / ("counts-" + module + ".log"),
                            reviews / "counts-sources" / (module + ".lean")]
    selected_counts += [reviews / name for name in (
        "counts-verification.json", "counts-palindrome-verification.json",
        "counts-semantic-review.md", "counts-palindrome-semantic-review.md")]
    for path in selected_counts:
        add_repo(path, "counts-nonpalindromic-review")

    prior_archives = []
    prior_names = set()
    for path in (
        contribution / "archives/manifest.json",
        repo / "proofs/contributions/agent-101/nonpalindromic-fibers-20261016/archives/generic-verification.manifest.json",
    ):
        old = json.loads(read_regular(path))
        prior_names.update(row["path"] for row in old["members"])
        if isinstance(old["archive"], dict):
            filename, expected_sha = old["archive"]["filename"], old["archive"]["sha256"]
        else:
            filename, expected_sha = old["archive"], old["archive_sha256"]
        old_archive = path.parent / filename
        assert digest(read_regular(old_archive)) == expected_sha
        prior_archives.append({"manifest_path": path.relative_to(repo).as_posix(),
                               "manifest_sha256": digest(read_regular(path)),
                               "archive_sha256": expected_sha, "member_count": len(old["members"])})
    overlap = sorted(prior_names & set(contents))
    assert not overlap, "Previously archived member paths were selected: " + repr(overlap)
    rows.sort(key=lambda r: r["path"])
    write_archive(archive, rows, contents)
    for row in rows:
        assert read_regular(origins[row["path"]]) == contents[row["path"]]

    original_helper = contribution / "archives/verify-runtime-development.py"
    adapted_helper = here / "final-independent-verify.py"
    expected_helper = read_regular(original_helper).replace(
        b'here / "runtime-development.tar.gz"', b'here / "final-independent.tar.gz"').replace(
        b'here / "manifest.json"', b'here / "final-independent-manifest.json"')
    assert read_regular(adapted_helper) == expected_helper
    groups = {group: sum(row["group"] == group for row in rows) for group in sorted({r["group"] for r in rows})}
    manifest = {
        "schema_version": 1,
        "repository": "taco-jpg/p196-algorithm",
        "source_commit": COMMIT,
        "registry_sha256": REGISTRY_SHA,
        "archive": {"filename": ARCHIVE, "bytes": archive.stat().st_size,
                    "sha256": digest(read_regular(archive)), "format": "gzip-compressed PAX tar",
                    "member_count": len(rows), "uncompressed_file_bytes": sum(r["bytes"] for r in rows)},
        "member_path_base": "repository root",
        "canonical_origin_root": str(canonical),
        "canonical_restored_prefix": canonical_prefix,
        "canonical_path_mapping": "Only external canonical output names are rebased below canonical_restored_prefix; their relative hierarchy and bytes are preserved. Repository files retain their original repository-relative names.",
        "groups": groups,
        "excluded_policy": {"directory_components": sorted(EXCLUDED_PARTS), "filename_endings": list(EXCLUDED_ENDINGS)},
        "excluded_files": exclusions,
        "prior_archives_not_repeated": prior_archives,
        "prior_archive_member_path_overlap": overlap,
        "shared_dependency_policy": "No old development or generic-verification member paths are copied. The complete final canonical snapshot and original published inputs intentionally retain dependencies whose bytes also occur in older source snapshots.",
        "preservation": "All original files remain unchanged. File bytes and paths are preserved; tar metadata is normalized. The original canonical FILES report is retained verbatim, including references to excluded compiler objects. No Lean or Git command is run by packaging.",
        "archive_metadata_policy": "Sorted regular members; mode 0644; uid/gid/mtime zero; blank owner/group names; gzip filename empty and mtime zero; gzip compression level 9.",
        "reproducibility": "Use --repack-from-root with an extracted repository root and this manifest to reproduce and check the same tar.gz bytes in a new output directory.",
        "helper_reuse": {"original_path": original_helper.relative_to(repo).as_posix(),
                         "original_sha256": digest(read_regular(original_helper)),
                         "modification": "Only the default archive and manifest filenames were replaced; verification and safe extraction logic are byte-identical."},
        "sidecar_helpers": [{"filename": p.name, "bytes": p.stat().st_size, "sha256": digest(read_regular(p))}
                            for p in (Path(__file__).resolve(), adapted_helper)],
        "members": rows,
    }
    with manifest_path.open("x") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")
    print(json.dumps({"status": "PASS", "archive": manifest["archive"], "groups": groups,
                      "manifest_sha256": digest(read_regular(manifest_path)),
                      "excluded_count": len(exclusions), "old_member_overlap": len(overlap)}))


if __name__ == "__main__":
    main()
