#!/usr/bin/env python3
"""Clean Agent #13 real-weight proof build with a pinned Mathlib dependency.

Use --library-audit for the Git-metadata-free development artifact. A normal
Mathlib checkout is validated directly against the exact Git commit and manifest.
Library caches are explicit dependencies, not represented as source rebuilds.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import time

PIN = "c44e0c8ee63ca166450922a373c7409c5d26b00b"
MANIFEST_SHA = "5c6421b650bc87a2427a892a39e5522dc44543ca4ac1bd6e9f08d536c044a752"
SOURCE_INDEX_SHA = "827a626439889f56030a269faf4f4debb1ebe5ac63cadd7ea9e47c1fbdcc96b7"
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
MODULES = ("LychrelDigitSums", "Family", "TargetSafety", "Counting", "Weights", "SqrtBound")
EXPECTED_FAMILY = {
    "LychrelDigitSums": "ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57",
    "Family": "0fb8b09408cc0fa6283c2f3161b62ab915fefa7b6079353a987784d72563b007",
    "TargetSafety": "cedcebb91e5cad563933d1af01a3dfe20def1983ccce8da6dc7b161635b5271d",
    "Counting": "a430efc92f39ff538d4f54b27435676f0c61697ba3ff0e75dbe8565bda8642e0",
}

def sha(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()

def git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()

def verify_library(root: Path, audit: Path | None) -> dict:
    if sha(root / "lake-manifest.json") != MANIFEST_SHA:
        raise ValueError("Mathlib dependency manifest does not match the exact pin.")
    manifest = json.loads((root / "lake-manifest.json").read_text())
    pins = {p["name"]: p["rev"] for p in manifest["packages"]}
    if (root / ".git").exists():
        if git(root, "rev-parse", "HEAD") != PIN:
            raise ValueError("Wrong Mathlib source commit.")
        git(root, "diff", "--exit-code", "HEAD", "--", "*.lean", "lake-manifest.json")
        for name, rev in pins.items():
            package = root / ".lake/packages" / name
            if git(package, "rev-parse", "HEAD") != rev:
                raise ValueError(f"Wrong dependency commit: {name}")
            git(package, "diff", "--exit-code", "HEAD", "--", "*.lean")
        mode = "Pinned clean Git source checkouts; official compiled-library cache"
        count = None
    else:
        if audit is None or sha(audit / "SOURCES.json") != SOURCE_INDEX_SHA:
            raise ValueError("Exact source-audit index required for a Git-free library artifact.")
        if (audit / "MATHLIB_COMMIT.txt").read_text().strip() != PIN:
            raise ValueError("Wrong artifact source commit.")
        artifact_pins = json.loads((audit / "DEPENDENCY_COMMITS.json").read_text())
        if artifact_pins != pins:
            raise ValueError("Artifact dependency commits differ from pinned manifest.")
        rows = json.loads((audit / "SOURCES.json").read_text())
        for row in rows:
            p = root / row["path"]
            if not p.is_file() or p.stat().st_size != row["bytes"] or sha(p) != row["sha256"]:
                raise ValueError(f"Library source mismatch: {row['path']}")
        mode = "All transferred pinned source hashes checked; official compiled-library cache"
        count = len(rows)
    return {"mathlib_commit": PIN, "manifest_sha256": MANIFEST_SHA,
            "dependency_commits": pins, "validation": mode,
            "library_source_files_hashed": count,
            "library_clean_source_rebuild": False}

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", type=Path, required=True)
    parser.add_argument("--mathlib", type=Path, required=True)
    parser.add_argument("--library-audit", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    lean = args.lean.resolve(strict=True)
    lib = args.mathlib.resolve(strict=True)
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    version = subprocess.check_output([str(lean), "--version"], text=True)
    (out / "lean-version.txt").write_text(version)
    if "version 4.19.0," not in version or "6caaee842e94" not in version:
        raise ValueError("Exact Lean 4.19.0 compiler required.")
    library = verify_library(lib, args.library_audit)
    (out / "LIBRARY.json").write_text(json.dumps(library, indent=2) + "\n")
    here = Path(__file__).resolve().parent
    family = here.parent / "safe-predecessor-family"
    repo = here.parents[3]
    hashes: dict[str, str] = {}
    theorem_names: list[str] = []
    steps: list[dict] = []
    roots = [lib / ".lake/build/lib/lean"] + sorted((lib / ".lake/packages").glob("*/.lake/build/lib/lean"))
    with tempfile.TemporaryDirectory(prefix="agent13-real-clean-") as temp:
        build = Path(temp)
        for name in MODULES:
            source = (repo / "proofs/research/continuation/LychrelDigitSums.lean" if name == "LychrelDigitSums"
                      else (family if name in EXPECTED_FAMILY else here) / (name + ".lean"))
            digest = sha(source)
            if name in EXPECTED_FAMILY and digest != EXPECTED_FAMILY[name]:
                raise ValueError(f"Previously checked source changed: {name}")
            data = source.read_bytes()
            hashes[str(source.relative_to(repo))] = digest
            (build / source.name).write_bytes(data)
            if name != "LychrelDigitSums":
                namespace = "Agent13SafeFamily" if name in EXPECTED_FAMILY else "Agent13SafeWeights"
                theorem_names.extend(namespace + "." + n for n in
                    re.findall(r"^theorem\s+(\w+)", data.decode(), re.MULTILINE))
        audit_text = "import SqrtBound\n\n" + "\n".join("#print axioms " + n for n in theorem_names) + "\n"
        (build / "AllAxioms.lean").write_text(audit_text)
        (out / "AllAxioms.lean").write_text(audit_text)
        env = os.environ.copy()
        env["LEAN_PATH"] = ":".join(str(p) for p in [build, *roots])
        for name in (*MODULES, "AllAxioms"):
            cmd = [str(lean), "-o", name + ".olean", name + ".lean"]
            start = time.monotonic()
            try:
                with (out / (name + ".log")).open("wb") as log:
                    result = subprocess.run(cmd, cwd=build, env=env, stdout=log,
                                            stderr=subprocess.STDOUT, timeout=600, check=False)
                status: int | str = result.returncode
            except subprocess.TimeoutExpired:
                status = "TIMEOUT_600_SECONDS"
            steps.append({"module": name, "command": cmd, "exit": status,
                          "seconds": round(time.monotonic() - start, 3)})
            (out / "build-steps.json").write_text(json.dumps(steps, indent=2) + "\n")
            if status != 0:
                raise SystemExit(f"Build did not pass: {name}; see exact retained logs.")
        text = (out / "AllAxioms.log").read_text()
        reports = re.findall(r"'([^']+)' depends on axioms: \[([^]]*)\]", text)
        if {name for name, _ in reports} != set(theorem_names) or len(reports) != len(theorem_names):
            raise ValueError("Missing or duplicate exported-theorem axiom report.")
        for name, axes in reports:
            actual = {a.strip() for a in axes.split(",") if a.strip()}
            if not actual <= ALLOWED_AXIOMS:
                raise ValueError(f"Rejected transitive axioms for {name}: {actual}")
    report = {"agent": 13, "source_snapshot": "c2b6977e43a79caa5ff3bb88801f3ba896986f38",
              "verification": "LEAN_CHECKED; clean contribution and decimal-source rebuild; independent review pending",
              "version": version.strip(), "library": library, "source_sha256": hashes,
              "exported_theorems": theorem_names, "theorem_count": len(theorem_names),
              "axiom_audits": len(reports), "allowed_axioms": sorted(ALLOWED_AXIOMS), "steps": steps}
    (out / "RESULT.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
