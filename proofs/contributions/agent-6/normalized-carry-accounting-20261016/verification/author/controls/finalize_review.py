"""Summarize retained final compiler and origin-audit receipts without rerunning Lean."""
from pathlib import Path
import hashlib
import json
import re


scratch = Path(__file__).resolve().parent
root = scratch.parents[1]
source = root / "agent6-carry/proofs/contributions/agent-6/normalized-carry-accounting-20261016/CarryControls.lean"
raw = source.read_bytes()
text = raw.decode()
namespace = "Agent6.CarryControls."
public = [namespace + name for name in re.findall(
    r"(?m)^(?:@\[[^\]]*\]\s*)*theorem\s+([A-Za-z0-9_']+)", text)]
private = re.findall(r"(?m)^private\s+theorem\s+([A-Za-z0-9_']+)", text)
prints = re.findall(r"(?m)^#print axioms (\S+)$", text)
assert len(public) == 7 and set(public) == set(prints) and len(prints) == 7
assert not private
assert text.startswith("import CertificateCarryAccounting\n")
all_attempts = []
for path in sorted((scratch / "attempts").glob("*/verification.json")):
    receipt = json.loads(path.read_text())
    all_attempts.append((path.parent, receipt))
author_candidates = [(path, receipt) for path, receipt in all_attempts
                     if receipt["module"] == "CarryControls"
                     and receipt["exit_code"] == 0
                     and receipt["source_sha256"] == hashlib.sha256(raw).hexdigest()]
audit_candidates = [(path, receipt) for path, receipt in all_attempts
                    if receipt["module"] == "CarryControlsAudit"
                    and receipt["exit_code"] == 0]
assert author_candidates and audit_candidates
author, author_receipt = author_candidates[-1]
audit, audit_receipt = audit_candidates[-1]
assert (author / source.name).read_bytes() == raw
assert any(item["module"] == "CarryControls"
           and item["sha256"] == author_receipt["output_object"]["sha256"]
           for item in audit_receipt["dependency_oleans"])
allowed = {"propext", "Classical.choice", "Quot.sound"}
exports = {}
for name, axioms, empty in re.findall(
        r"'([^']+)' (?:depends on axioms:\s*\[([^\]]*)\]|(does not depend on any axioms))",
        (author / "compile.log").read_text()):
    exports[name] = sorted(a.strip() for a in axioms.split(",") if a.strip())
assert set(exports) == set(public)
assert all(set(v) <= allowed for v in exports.values())
(scratch / "exported-axioms.json").write_text(json.dumps(exports, indent=2) + "\n")
audit_log = (audit / "compile.log").read_text()
declarations = {}
for name, axioms in re.findall(
        r"AUDIT_DECLARATION CarryControls (\S+) : \[([^\]]*)\]", audit_log):
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
failed = sum(receipt["exit_code"] != 0 for _, receipt in all_attempts)
body = raw.split(b"\n", 1)[1]
initial = scratch / "attempts/CarryControls-001/CarryControls.lean"
assert initial.read_bytes().split(b"\n", 1)[1] == body
result = {
    "status": "PASS", "role": "Agent #6 author boundary controls and origin audit",
    "source_path": str(source), "source_bytes": len(raw),
    "source_sha256": hashlib.sha256(raw).hexdigest(),
    "source_git_blob_sha1": hashlib.sha1(
        b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest(),
    "source_frozen": True,
    "claim_coordination_commit": "1bd2354c2447febf38df9b69fb670e988abfc72a",
    "claim_blob": "6642f91e3a0a9898a150240b919d2b110d07a1b6",
    "final_import": "CertificateCarryAccounting",
    "theorem_body_sha256": hashlib.sha256(body).hexdigest(),
    "theorem_bodies_unchanged_from_first_pass": True,
    "public_theorem_count": len(public),
    "explicit_private_theorem_count": len(private),
    "literal_source_print_axioms_count": len(prints),
    "full_origin_theorem_count": theorems,
    "full_origin_safe_definition_count": safe_defs,
    "compiler_unsafe_implementation_count": unsafe_defs,
    "axiom_union": sorted(set(a for v in declarations.values() for a in v)),
    "author_compile_receipt": str(author / "verification.json"),
    "full_origin_audit_receipt": str(audit / "verification.json"),
    "retained_attempt_count": len(all_attempts),
    "failed_attempt_count": failed,
    "pinned_lean_sha256": author_receipt["compiler_sha256"],
    "trust_level": 0,
    "scope": "Exact carry/indicator controls and formal failures of unrestricted identities. No accepted certificate or cycle assertion.",
    "public_exports": public,
    "independent_review": "Separate runtime review, not established by this author receipt.",
}
(scratch / "RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
review = f"""# Carry boundary controls: author verification

The seven public controls pass the pinned Lean 4.19.0 kernel at trust level zero.
The final source imports `CertificateCarryAccounting`, bringing the structural
carry and certificate accounting modules into the registry root. Only this
import changed after the first successful control build; the theorem bodies
are byte-identical to that earlier attempt.

## Exact mathematical content

All examples use `controlState c B = {{ c := c, B := B, A := [], C := [] }}`.
These are original row values, with no assertion of an accepted certificate.

| Phase | Raw B | Stripped B | Raw gam | Stripped carry | Stripped indicator | Purpose |
| --- | --- | --- | ---: | ---: | ---: | --- |
| 19 | [19] | [] | 2 | 1 | 1 | Unrestricted carry invariance fails; the raw indicator is also 1. |
| 2 | [20] | [20] | 2 | 2 | 1 | Permitted phase and unchanged stripping do not remove the coefficient-bound requirement. |
| 18 | [18] | [] | 1 | 1 | 1 | The empty word retains incoming carry one. |
| 9 | [9] | [] | 0 | 0 | 0 | Neutral phase is a meaningful zero-carry boundary. |
| 0 | [0] | [] | 0 | 0 | 0 | Zero phase and zero coefficient are included. |
| 19 | [18] | [18] | 1 | 1 | 1 | A bounded exterior works above phase eighteen. |

The first two controls explicitly prove raw carry 2. The latter four use
coefficients within the existing bound of eighteen. Their exact conjunctions
are in the frozen source; auxiliary zero-carry table entries are definitional
reductions of the same empty words and incoming phase carry.

The negative theorem `unrestricted_strip_carry_invariance_false` proves:

```text
not (forall c B, overflow c (stripSuffix c B) = overflow c B).
```

The combined theorem `indicator_eq_gam_without_bounded_false` proves both:

```text
not (forall s, overflowBit (stateOuter s) = gam s),
not (forall s, Phase s.c -> overflowBit (stateOuter s) = gam s).
```

These are failures of unrestricted identities. They do not contradict the
bounded-state interface, establish a cycle, or produce an accepted certificate.

## Source and trust evidence

- Source: `{source}`
- Source SHA256: `{result['source_sha256']}`
- Git blob SHA1: `{result['source_git_blob_sha1']}`
- Source bytes: {len(raw)}
- Claim coordination: `{result['claim_coordination_commit']}`
- Claim blob: `{result['claim_blob']}`
- Public theorem declarations and literal `#print axioms` receipts: {len(public)} each
- Explicit private theorem declarations: {len(private)}
- Full module-origin theorem constants: {theorems}
- Full module-origin safe definitions: {safe_defs}
- Separately recorded compiler unsafe implementations: {unsafe_defs}
- Axiom union for all safe audited declarations: `{', '.join(result['axiom_union']) or 'none'}`
- Retained actual attempts: {len(all_attempts)}; failed attempts: {failed}

The compiler binary SHA256 is `{result['pinned_lean_sha256']}`.
Every invocation uses `--trust=0 -j1 -DElab.async=false`. The initial pass uses
the inherited eighteen objects that runtime matched to its existing successful
review; unchanged baseline modules were not recompiled here. The final pass
adds the freshly built structural and accounting objects. Exact paths, object
hashes, commands, source snapshots, and elapsed times are retained in each
`verification.json`. Raw compiler logs are unchanged.

The source-level receipt checks all seven literal exports. `CarryControlsAudit`
selects every theorem and definition by its actual imported module origin,
includes generated theorem constants, rejects nonstandard axioms in safe
declarations, and records compiler unsafe implementations separately. This is
an author audit; runtime's independent combined review is a distinct gate.

`check_controls.py` records each actual execution in a fresh attempt directory.
`finalize_review.py` only summarizes existing receipts and hashes; it does not
invoke Lean. Compiled objects are retained locally for dependency use but
excluded from the portable evidence manifest.
"""
(scratch / "REVIEW.md").write_text(review)
manifest = []
for path in sorted(scratch.rglob("*")):
    if not path.is_file() or path.name == "MANIFEST.json" or path.suffix in {".olean", ".ilean"}:
        continue
    data = path.read_bytes()
    manifest.append({"path": str(path.relative_to(scratch)), "bytes": len(data),
                     "sha256": hashlib.sha256(data).hexdigest()})
(scratch / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(json.dumps(result, indent=2))
print(json.dumps({"evidence_file_count_excluding_manifest": len(manifest),
                  "evidence_bytes_excluding_manifest": sum(p["bytes"] for p in manifest)}, indent=2))
