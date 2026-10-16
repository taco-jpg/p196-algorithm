#!/usr/bin/env python3
"""Kernel-check generated rank modules against an existing dependency build.

The build directory must contain freshly checked SixPrefix and its imports,
including both Lean source and object files. This runner freezes local
source copies, records source and object
hashes, and limits both process and Lean-internal parallelism. It does not
download a runtime, trust an external rank graph, or use native_decide.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

HERE = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(build: Path, lean: str, workers: int, resume: bool) -> int:
    build = build.resolve()
    if not 1 <= workers <= 4:
        raise ValueError("workers must lie between 1 and 4")
    for module in ("SixPrefix", "BoundaryTransducer", "LychrelDigitSums"):
        for suffix in (".lean", ".olean"):
            if not (build / (module + suffix)).is_file():
                raise FileNotFoundError(f"Missing checked dependency: {module}{suffix}")
    module_names = ["RankData"] + [f"RankChecks{i}" for i in range(7)] + ["RankChecks", "RankCertificate"]
    manifest_path = build / "rank_build.json"
    previous = json.loads(manifest_path.read_text()) if resume and manifest_path.is_file() else {}
    manifest = {"status": "RUNNING", "lean": lean, "lean_threads": 1,
                "async_theorem_elaboration": False,
                "parallel_processes": workers,
                "imports": {}, "sources": {}, "modules": {}}
    for module in ("SixPrefix", "BoundaryTransducer", "LychrelDigitSums"):
        info = {"olean_sha256": digest(build / (module + ".olean"))}
        source = build / (module + ".lean")
        if source.is_file():
            info["source_sha256"] = digest(source)
        manifest["imports"][module] = info
    for module in module_names:
        source = HERE / (module + ".lean")
        target = build / source.name
        if source.resolve() != target:
            shutil.copyfile(source, target)
        manifest["sources"][module] = {
            "repo_relative_path": "proofs/contributions/" + HERE.name + "/" + source.name,
            "source_sha256": digest(source), "source_bytes": source.stat().st_size}
    reusable = previous.get("modules", {}) if previous.get("imports") == manifest["imports"] else {}

    def save() -> None:
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")

    env = os.environ.copy()
    env["LEAN_PATH"] = str(build)

    def compile_module(module: str) -> tuple[str, dict]:
        source = build / (module + ".lean")
        out = build / (module + ".olean")
        logpath = build / (module + ".log")
        command = [lean, "-j1", "-DElab.async=false", "-o", out.name, source.name]
        direct_imports = {
            "RankData": ("SixPrefix", "BoundaryTransducer"),
            **{f"RankChecks{i}": ("RankData",) for i in range(7)},
            "RankChecks": tuple(f"RankChecks{i}" for i in range(7)),
            "RankCertificate": ("RankChecks",),
        }

        def dependency_fingerprints() -> dict:
            return {name: {
                "source_sha256": digest(build / (name + ".lean")),
                "olean_sha256": digest(build / (name + ".olean")),
            } for name in direct_imports[module]}

        dependencies_before = dependency_fingerprints()
        cached = reusable.get(module)
        if (cached and cached.get("exit_code") == 0 and cached.get("source_unchanged")
                and cached.get("dependencies_unchanged") is True
                and cached.get("dependency_fingerprints") == dependencies_before
                and cached.get("command") == command and out.is_file() and logpath.is_file()
                and cached.get("source_sha256") == digest(source)
                and cached.get("olean_sha256") == digest(out)
                and cached.get("log_sha256") == digest(logpath)):
            result = dict(cached, reused_from_verified_same_build=True)
            print(module + " reused exact-hash checked object", flush=True)
            return module, result
        start = time.monotonic()
        with logpath.open("w") as log:
            process = subprocess.run(command, cwd=build, env=env, stdout=log,
                                     stderr=subprocess.STDOUT)
        result = {"command": command, "exit_code": process.returncode,
                  "seconds": round(time.monotonic() - start, 3),
                  "source_sha256": digest(source), "log_sha256": digest(logpath),
                  "dependency_fingerprints": dependencies_before,
                  "dependencies_unchanged": dependency_fingerprints() == dependencies_before,
                  "source_unchanged": digest(source) == manifest["sources"][module]["source_sha256"]}
        if process.returncode == 0:
            result["olean_sha256"] = digest(out)
        print(module + " " + json.dumps(result), flush=True)
        return module, result

    def record(item: tuple[str, dict]) -> bool:
        module, result = item
        manifest["modules"][module] = result
        save()
        return (result["exit_code"] == 0 and result["source_unchanged"]
                and result.get("dependencies_unchanged") is True)

    save()
    successful = record(compile_module("RankData"))
    if successful:
        pending = iter(f"RankChecks{i}" for i in range(7))
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
            active = {pool.submit(compile_module, next(pending)) for _ in range(workers)}
            while active:
                done, active = concurrent.futures.wait(active,
                    return_when=concurrent.futures.FIRST_COMPLETED)
                for future in done:
                    successful = record(future.result()) and successful
                    if successful:
                        module = next(pending, None)
                        if module is not None:
                            active.add(pool.submit(compile_module, module))
    if successful:
        for module in ("RankChecks", "RankCertificate"):
            successful = record(compile_module(module))
            if not successful:
                break
    manifest["status"] = "PASS" if successful else "FAIL"
    save()
    return 0 if successful else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build", required=True, type=Path)
    parser.add_argument("--lean", default="lean")
    parser.add_argument("--workers", default=1, type=int)
    parser.add_argument("--resume", action="store_true",
        help="Reuse only logged successful modules with matching import/source/object/log hashes")
    args = parser.parse_args()
    raise SystemExit(verify(args.build, args.lean, args.workers, args.resume))
