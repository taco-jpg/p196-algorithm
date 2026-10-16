"""Summarize retained compiler receipts; this script does not invoke Lean."""
from pathlib import Path
import hashlib
import json
import re

scratch = Path(__file__).resolve().parent
root = scratch.parents[1]
source = root / "agent6-checker/proofs/contributions/agent-6/certificate-coordinate-audit-20261016/CertificateControls.lean"
raw = source.read_bytes()
text = raw.decode()
namespace = "Agent6.CertificateControls."
public = [namespace + name for name in re.findall(
    r"(?m)^(?:@\[[^\]]*\]\s*)*theorem\s+([A-Za-z0-9_']+)", text)]
prints = re.findall(r"(?m)^#print axioms (\S+)$", text)
assert len(public) == 12 and set(public) == set(prints) and len(prints) == 12
author = scratch / "attempts/CertificateControls-001"
audit = scratch / "attempts/CertificateControlsAudit-001"
author_receipt = json.loads((author / "verification.json").read_text())
audit_receipt = json.loads((audit / "verification.json").read_text())
assert author_receipt["exit_code"] == audit_receipt["exit_code"] == 0
assert (author / source.name).read_bytes() == raw
assert author_receipt["source_sha256"] == hashlib.sha256(raw).hexdigest()
allowed = {"propext", "Classical.choice", "Quot.sound"}
compile_log = (author / "compile.log").read_text()
exports = {}
for name, axioms, empty in re.findall(
        r"'([^']+)' (?:depends on axioms:\s*\[([^\]]*)\]|(does not depend on any axioms))",
        compile_log):
    exports[name] = sorted(a.strip() for a in axioms.split(",") if a.strip())
assert set(exports) == set(public)
assert all(set(v) <= allowed for v in exports.values())
(scratch / "exported-axioms.json").write_text(json.dumps(exports, indent=2) + "\n")
audit_log = (audit / "compile.log").read_text()
declarations = {}
for name, axioms in re.findall(
        r"AUDIT_DECLARATION CertificateControls (\S+) : \[([^\]]*)\]", audit_log):
    declarations[name] = sorted(a.strip() for a in axioms.split(",") if a.strip())
assert all(set(v) <= allowed for v in declarations.values())
summary = re.search(
    r"FULL_MODULE_AUDIT theorems=(\d+) safeDefinitions=(\d+) unsafeImplementations=(\d+) union=\[([^\]]*)\]",
    audit_log)
assert summary
theorems, safe_defs, unsafe_defs = map(int, summary.group(1, 2, 3))
assert len(declarations) == theorems + safe_defs
assert set(public) <= set(declarations)
(scratch / "full-module-axioms.json").write_text(json.dumps(declarations, indent=2) + "\n")
result = {
    "status": "PASS", "role": "Agent #6 author control and axiom review",
    "source_path": str(source), "source_bytes": len(raw),
    "source_sha256": hashlib.sha256(raw).hexdigest(),
    "source_git_blob_sha1": hashlib.sha1(
        b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest(),
    "source_frozen": True, "public_theorem_count": len(public),
    "literal_source_print_axioms_count": len(prints),
    "full_origin_theorem_count": theorems,
    "full_origin_safe_definition_count": safe_defs,
    "compiler_unsafe_implementation_count": unsafe_defs,
    "axiom_union": sorted(set(a for v in declarations.values() for a in v)),
    "author_compile_receipt": str(author / "verification.json"),
    "full_origin_audit_receipt": str(audit / "verification.json"),
    "failed_attempt_count": 0,
    "pinned_lean_sha256": author_receipt["compiler_sha256"],
    "trust_level": 0,
    "scope": "An explicit rejected candidate proving that the necessary coordinate filter is insufficient, plus empty and zero-phase controls.",
    "public_exports": public,
}
(scratch / "RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
manifest = []
for path in sorted(scratch.rglob("*")):
    if not path.is_file() or "build" in path.relative_to(scratch).parts or path.name == "MANIFEST.json":
        continue
    data = path.read_bytes()
    manifest.append({"path": str(path.relative_to(scratch)), "bytes": len(data),
                     "sha256": hashlib.sha256(data).hexdigest()})
(scratch / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(json.dumps(result, indent=2))
print(json.dumps({"evidence_file_count_excluding_manifest": len(manifest),
                  "evidence_bytes_excluding_manifest": sum(p["bytes"] for p in manifest)}, indent=2))
