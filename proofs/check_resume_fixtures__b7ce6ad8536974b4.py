#!/usr/bin/env python3
"""Read-only negative fixtures for the scalar builder's resume predicate."""
import importlib.util
import json
from pathlib import Path
import tempfile

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "2026-10-15-scalar-finite-certificate-formal/verify.py"
spec = importlib.util.spec_from_file_location("scalar_resume_audited", SOURCE)
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def main():
    checked = []
    with tempfile.TemporaryDirectory(prefix="scalar-resume-fixture-") as temporary:
        build = Path(temporary)
        (build / "logs").mkdir()
        originals = {"D.lean": b"dependency source", "D.olean": b"dependency object",
                     "M.lean": b"module source", "M.olean": b"module object",
                     "logs/M.log": b"successful compilation log"}
        for name, blob in originals.items():
            (build / name).write_bytes(blob)
        identity = builder.digest(b"compiler and exact settings")
        dependencies = builder.dependency_fingerprints(build, ["D"])
        record = dict(status="PASS", exit_code=0, module="M",
                      source_sha256=builder.digest(originals["M.lean"]),
                      compiler_identity_sha256=identity,
                      dependency_fingerprints=dependencies,
                      dependencies_unchanged=True, source_unchanged=True,
                      olean_sha256=builder.file_hash(build / "M.olean"),
                      log_sha256=builder.file_hash(build / "logs/M.log"))

        def check(label, expected, rec=None, compiler=None, blob=None):
            observed = builder.reusable(record if rec is None else rec, "M",
                originals["M.lean"] if blob is None else blob,
                builder.dependency_fingerprints(build, ["D"]),
                identity if compiler is None else compiler, build)
            assert observed is expected, (label, observed, expected)
            checked.append(dict(case=label, expected=expected, observed=observed))

        check("unchanged exact record accepted", True)
        for filename in originals:
            (build / filename).write_bytes(originals[filename] + b" changed")
            check("changed " + filename + " rejected", False)
            (build / filename).write_bytes(originals[filename])
        check("changed source snapshot rejected", False, blob=b"changed source snapshot")
        check("changed compiler/settings identity rejected", False, compiler="different identity")
        for key in record:
            modified = dict(record)
            del modified[key]
            check("missing " + key + " rejected", False, rec=modified)
        for key, value in (("exit_code", 1), ("status", "RUNNING"),
                           ("source_unchanged", False), ("dependencies_unchanged", False)):
            check("invalid " + key + " rejected", False, rec={**record, key: value})
        check("empty legacy record rejected", False, rec={})
        for filename in ("M.olean", "logs/M.log", "M.lean"):
            (build / filename).unlink()
            check("missing " + filename + " rejected", False)
            (build / filename).write_bytes(originals[filename])
        check("restored exact record accepted", True)
    report = dict(result="PASS", cases=len(checked), checks=checked,
                  checker_source=str(SOURCE.relative_to(HERE.parent)),
                  checker_sha256=builder.file_hash(SOURCE),
                  scope="Isolated reusable() fixtures and source review; no Lean build or live-file mutation.")
    (HERE / "fixture_results.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in ("result", "cases", "checker_sha256")}))


if __name__ == "__main__":
    main()
