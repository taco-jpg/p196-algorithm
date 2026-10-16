from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess
import time

reviews = Path(__file__).resolve().parent
repo = reviews.parents[4]
out = Path("/workspace/scratch/2a8a87fd78df/agent101-final-family-independent-71691d5")
project = "agent101-protected-family"
source = out / project / "source"
lean = Path("/workspace/scratch/2a8a87fd78df/agent101-runtime/toolchain/lean-4.19.0-linux/bin/lean")
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
allowed = {"propext", "Classical.choice", "Quot.sound"}
canonical = json.loads((out / "verification.json").read_text())
assert canonical["status"] == "PASS"
pr = canonical["projects"][project]
assert pr["status"] == "PASS"
assert canonical["source_commit"] == "71691d50497edc83247b3571af276bb0ee438491"
assert canonical["registry_sha256"] == "04aba56fc69ef566d32b0c1064a4db2298f095d88e98fcd9fefe7f5c70614307"
assert len(pr["build_order"]) == 26
env = os.environ.copy()
env["LEAN_PATH"] = str(source)
records = []

def run(label, filename):
    command = [str(lean), "--trust=0", "-j1", "-DElab.async=false", filename]
    start = time.monotonic()
    result = subprocess.run(command, cwd=source, env=env, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    log = reviews / ("final-" + label + ".log")
    log.write_text(result.stdout)
    rec = {"label": label, "command": command, "cwd": str(source),
           "LEAN_PATH": env["LEAN_PATH"], "returncode": result.returncode,
           "seconds": time.monotonic() - start, "log": str(log), "log_sha256": sha(log),
           "audit_source_sha256": sha(source / filename)}
    records.append(rec)
    (reviews / "final-audit-commands.json").write_text(json.dumps(records, indent=2) + "\n")
    print(json.dumps(rec), flush=True)
    assert result.returncode == 0, result.stdout
    assert "sorryAx" not in result.stdout and "Lean.ofReduceBool" not in result.stdout
    return result.stdout

project_audit_original_hash = sha(source / "ProjectAudit.lean")
shutil.copyfile(source / "ProjectAudit.lean", reviews / "final-ProjectAudit.lean")
project_log = run("ProjectAudit-trust0", "ProjectAudit.lean")
assert sha(source / "ProjectAudit.lean") == project_audit_original_hash
theorems = re.findall(r"^AUDIT_THEOREM (\S+) (\S+) : (.*)$", project_log, re.M)
summary = re.findall(r"^FULL_MODULE_AUDIT theorems=(\d+) union=([^\n]*)$", project_log, re.M)
assert len(summary) == 1 and int(summary[0][0]) == len(theorems) == pr["theorem_count"]
assert len({name for _, name, _ in theorems}) == len(theorems)

namespaces = {
    "Agent101ProtectedMultiplicity": "Agent101.Protected",
    "Agent101NormalizationValue": "Agent101",
    "Agent101ProtectedSafety": "Agent101.Protected",
    "Agent101PalindromeFibers": "Agent101",
    "Agent101NonpalindromicFibers": "Agent101",
    "Agent101ProtectedPalindrome": "Agent101.Protected",
    "Agent101ProtectedNonpalindromic": "Agent101.Protected",
    "Agent101ProtectedFamily": "Agent101.Protected",
}
exports = []
for module, namespace in namespaces.items():
    body = (source / (module + ".lean")).read_text()
    for match in re.finditer(r"^(def|theorem|lemma|abbrev)\s+([A-Za-z0-9_']+)", body, re.M):
        exports.append({"module": module, "kind": match.group(1), "name": namespace + "." + match.group(2)})
assert len(exports) == 94 and len({r["name"] for r in exports}) == 94
assert sum(r["kind"] == "def" for r in exports) == 9
assert sum(r["kind"] == "theorem" for r in exports) == 85
public_names = [r["name"] for r in exports]
audit = "import Agent101ProtectedFamily\nimport Lean\nopen Lean Elab Command\nset_option maxRecDepth 100000\nset_option maxHeartbeats 0\n\n"
audit += "".join("#check " + name + "\n#print axioms " + name + "\n" for name in public_names)
audit += "\nrun_cmd do\n  let env ← getEnv\n  let publicNames : List String := " + json.dumps(public_names) + "\n"
audit += '''  let mut seen := 0
  for (name, info) in env.constants.toList do
    if publicNames.contains name.toString then
      if info.isUnsafe then throwError m!"UNSAFE_PUBLIC_DECLARATION {name}"
      match info with
      | .axiomInfo _ => throwError m!"PUBLIC_CUSTOM_AXIOM {name}"
      | _ => pure ()
      seen := seen + 1
      logInfo m!"PUBLIC_SAFE {name}"
  if seen != publicNames.length then throwError m!"PUBLIC_CENSUS_MISMATCH {seen}"
  logInfo m!"PUBLIC_COUNT {seen}"
'''
(source / "FinalPublicAudit.lean").write_text(audit)
(reviews / "final-PublicAudit.lean").write_text(audit)
(reviews / "final-public-exports.json").write_text(json.dumps(exports, indent=2) + "\n")
public_log = run("PublicAudit-trust0", "FinalPublicAudit.lean")
printed = re.findall(r"^'([^']+)' (?:depends on axioms:|does not depend on any axioms)", public_log, re.M)
safe = re.findall(r"^PUBLIC_SAFE (\S+)$", public_log, re.M)
assert len(printed) == len(safe) == 94 and set(printed) == set(safe) == set(public_names)
assert re.findall(r"^PUBLIC_COUNT (\d+)$", public_log, re.M) == ["94"]
axioms = {a.strip() for group in re.findall(r"depends on axioms: \[([^]]*)\]", public_log) for a in group.split(",") if a.strip()}
assert axioms <= allowed

for module, rec in pr["sources"].items():
    assert sha(repo / rec["path"]) == rec["sha256"]
    assert sha(source / (module.replace(".", "/") + ".lean")) == rec["build_sha256"]
for filename, expected in canonical["compiler"]["files"].items():
    assert sha(Path(filename)) == expected
readback = json.loads((reviews / "final-source-readback.json").read_text())
assert sha(repo / readback["verifier_path"]) == readback["verifier_sha256"]
assert sha(repo / "proofs/Agent101ProtectedFamily.registry.json") == canonical["registry_sha256"]
result = {
    "result": "PASS", "reviewer": "Agent #101 research-inventory worker",
    "source_commit": canonical["source_commit"], "registry_sha256": canonical["registry_sha256"],
    "canonical_output_directory": str(out), "canonical_verifier_status": canonical["status"],
    "canonical_verifier_sha256": readback["verifier_sha256"],
    "canonical_compile_policy": "The prescribed unchanged verifier compiled all 26 modules freshly with -j1 -DElab.async=false; its compile and initial ProjectAudit commands do not explicitly pass --trust=0.",
    "explicit_trust_zero_policy": "The generated unchanged ProjectAudit and a separate complete 94-public-declaration audit were then run with explicit --trust=0.",
    "module_count": 26, "transitive_theorem_count": len(theorems),
    "all_transitive_theorems_audited_at_trust_zero": True,
    "public_declarations": len(exports), "public_theorems": 85, "public_definitions": 9,
    "all_public_declarations_proved_safe": True, "public_axiom_union": sorted(axioms),
    "sources_registry_verifier_compiler_unchanged_after_audits": True,
    "audit_commands": records,
    "unsafe_implementation_axioms_recorded_by_canonical_audit": pr["unsafe_implementation_axioms"],
    "independence": "Reviewer did not author NormalizationValue, ProtectedSafety, or ProtectedFamily. Reviewer authored the older SplitEnumeration and PalindromeFibers dependencies, which have separate independent reviews by other workers.",
}
(reviews / "final-verification.json").write_text(json.dumps(result, indent=2) + "\n")
shutil.copyfile(out / "verification.json", reviews / "final-canonical-verification.json")
shutil.copyfile(out / "FILES.json", reviews / "final-canonical-FILES.json")
print(json.dumps({"result": "PASS", "modules": 26, "transitive_theorems": len(theorems), "public_declarations": len(exports), "axiom_union": sorted(axioms)}), flush=True)
