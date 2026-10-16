#!/usr/bin/env python3
"""Reconcile retained PR112 CI bytes; this script never invokes Lean."""
from pathlib import Path
import argparse, ast, collections, hashlib, json, re, zipfile

def sha(data):
    return hashlib.sha256(data).hexdigest()

def blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def printed(text):
    rows = {}
    for match in re.finditer(r"^'(.+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)", text, re.M):
        assert match[1] not in rows, ("duplicate", match[1])
        rows[match[1]] = sorted(x.strip() for x in (match[2] or "").split(",") if x.strip())
    return rows

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--archive", type=Path, required=True)
parser.add_argument("--inputs", type=Path, required=True)
parser.add_argument("--retained-checkout", type=Path, required=True)
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
assert not args.output.exists(), "Preserve any prior output; choose a new filename."
inputs = json.loads(args.inputs.read_text())
mapping = inputs["mapping"]
order = [m["module"] for m in mapping]
assert len(order) == len(set(order)) == 13
data = args.archive.read_bytes()
assert len(data) == 99654
assert sha(data) == "01495e6a8fe41c13c2eb35ee8374f3c2c0ace5ccd712cf3dc2a97682bdb9bec5"
with zipfile.ZipFile(args.archive) as z:
    names = z.namelist()
    assert len(names) == len(set(names)) == 19
    assert z.testzip() is None
    raw = {name:z.read(name) for name in names}
v = json.loads(raw["verification.json"])
assert v["status"] == "PASS"
assert v["build_order"] == order
assert v["selected_modules"] == ["SharpSuffix"]
assert v["runtime_imports"] == ["Std"]
assert v["fresh_dependency_rebuild"] is True
assert v["isolated_project_import_path"] is True
assert v["local_sources_objects_logs_and_compiler_revalidated"] is True
flags = ["-j1", "-DElab.async=false"]
assert v["flags"] == flags
allowed = ["Classical.choice", "Quot.sound", "propext"]
assert v["allowed_axioms"] == v["axiom_union"] == allowed

original_prefix = "proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/contributions/agent-111/exact-length-residues/"
checker = (args.retained_checkout / (original_prefix + "check.py")).read_bytes()
assert blob(checker) == "4759deab8d954c5d347fa761aeb073f01e209e35"
assert sha(checker) == v["checker_sha256"] == "9fea73de4ea0497a1747e0b635bd1ea5d74d15b7479f89ae1351272f7093a9af"
tree = ast.parse(checker.decode())
pure = ast.Module(body=[node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "audit_source"], type_ignores=[])
namespace = {"json":json}
exec(compile(pure, "<authenticated-checker-audit-source-function>", "exec"), namespace)
expected_audit = namespace["audit_source"](order).encode()
assert expected_audit == raw["AllExportedAxioms.lean"]
assert sha(expected_audit) == v["audit_source_sha256"]

source_bytes = {}
for item in mapping:
    name = item["module"]
    source = inputs["new_sources"][name].encode() if name in inputs["new_sources"] else (args.retained_checkout / item["path"]).read_bytes()
    assert sha(source) == item["sha256"] == v["sources"][name]["source_sha256"], name
    assert blob(source) == item["git_blob"], name
    assert re.findall(r"^import (.+)$", source.decode(), re.M) == item["imports"], name
    deps = [dep for dep in item["imports"] if dep != "Std"]
    record = v["sources"][name]
    assert record["dependencies"] == deps, name
    assert record["dependency_olean_sha256"] == {dep:v["sources"][dep]["olean_sha256"] for dep in deps}, name
    assert record["olean_sha256"] == v["imported_object_sha256"][name], name
    source_bytes[name] = source

compiler = v["compiler"]
assert compiler["version"] == raw["logs/compiler-version.log"].decode().strip()
assert compiler["version"] == "Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)"
assert compiler["prefix"] == raw["logs/compiler-prefix.log"].decode().strip()
assert compiler["probe_output"] == raw["logs/compiler-probe.log"].decode().strip()
assert compiler["probe_output"].endswith("P196_PRELOAD=")
assert compiler["native_executable"] == compiler["invoked_executable"]
expected_fingerprints = {
    compiler["prefix"]+"/bin/lean":"92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023",
    compiler["prefix"]+"/lib/lean/Std.olean":"7d3771da25b893da62564bf8198487ff28f01af5cbd410be88d493a4921b2bb1",
    compiler["prefix"]+"/lib/lean/libleanshared.so":"2ab605c74c78f9ba4431a7b5305a4b28a9071d8a826f223eb14fe5530f78e14d",
    compiler["prefix"]+"/lib/lean/libleanshared_1.so":"44bc5837306f8e24a5db0db56d56ca3114415bd65e3b107426d3c93e21d20098"
}
assert compiler["fingerprints"] == expected_fingerprints
commands = v["commands"]
assert [c["label"] for c in commands] == ["compiler-version","compiler-prefix","compiler-probe"] + order + ["AllExportedAxioms"]
for c in commands:
    assert c["exit_code"] == 0
    assert sha(raw[c["log"]]) == c["log_sha256"], c["label"]
    assert c["command"][0] == compiler["invoked_executable"]
    if c["label"] in order:
        name = c["label"]
        assert c["command"][1:] == flags + ["-o",name+".olean",name+".lean"]
    if c["label"] == "AllExportedAxioms":
        assert c["command"][1:] == flags + ["AllExportedAxioms.lean"]

audit = raw["logs/AllExportedAxioms.log"].decode()
inventory = re.findall(r"^AUDIT_THEOREM (\S+) (\S+)$", audit, re.M)
axioms = printed(audit)
assert len(inventory) == len({name for mod,name in inventory}) == len(axioms) == v["theorem_count"] == 1012
rebuilt = {name:{"module":module,"axioms":axioms[name]} for module,name in inventory}
assert rebuilt == v["theorems"]
assert all(set(r["axioms"]) <= set(allowed) for r in rebuilt.values())
assert dict(collections.Counter(module for module,name in inventory)) == v["theorems_per_module"]
unsafe = [{"module":module,"name":name} for module,name in re.findall(r"^UNSAFE_IMPLEMENTATION_AXIOM (\S+) (\S+)$",audit,re.M)]
assert unsafe == v["unsafe_implementation_axioms"]
assert len(unsafe) == 13 and all(r["module"] == "Lychrel196Research" for r in unsafe)
assert not any(r["name"] in axes for r in unsafe for axes in axioms.values())
imports = re.findall(r"^AUDIT_IMPORT (\S+)$",audit,re.M)
assert set(imports) == set(v["imported_object_sha256"])
assert set(order) <= set(imports)
literal = {}
for name in ["GrowingSuffix","SharpSuffix"]:
    expected_names = re.findall(r"^#print axioms (.+)$", source_bytes[name].decode(), re.M)
    actual = printed(raw["logs/"+name+".log"].decode())
    assert set(expected_names) == set(actual)
    assert all(actual[n] == rebuilt[n]["axioms"] for n in expected_names)
    literal.update(actual)
assert len(literal) == 6
result = {
    "status":"PASS_RETAINED_CI_SOURCE_COMMAND_LOG_AND_AXIOM_RECONCILIATION",
    "source_head":inputs["source_head"],
    "workflow_run":38972796223,
    "workflow_job":117214969242,
    "workflow_artifact":12077672528,
    "ci_checkout_merge_commit":"4d10aa839c074cb2d04013ed8d3aee967677c09a",
    "ci_checkout_base":"f44c06c4851b26523bcec920d93a52b93fd2a0a6",
    "zip_sha256":sha(data),
    "zip_bytes":len(data),
    "member_count":len(raw),
    "member_bytes":sum(len(x) for x in raw.values()),
    "members":[{"path":name,"bytes":len(content),"sha256":sha(content)} for name,content in raw.items()],
    "sources":[{**item,"bytes":len(source_bytes[item["module"]])} for item in mapping],
    "commands_reconciled":len(commands),
    "fresh_source_compilations_reused":13,
    "retained_compiler_flags":flags,
    "retained_explicit_trust_zero":False,
    "theorem_constants_reconciled":1012,
    "theorems_per_module":v["theorems_per_module"],
    "unsafe_implementation_axioms_separately_classified":unsafe,
    "permitted_axiom_union":allowed,
    "literal_exports":literal,
    "new_lean_execution":"NOT_RUN",
    "independent_fresh_build":"NOT_RUN_BY_AGENT21",
    "import_audit_interpretation":"Origin and transitive axiom inspection; not a new kernel replay of imported proof terms.",
    "coverage_limit":"Theorem constants and their transitive axiom chains were audited. This artifact does not claim a separate all-safe-definition inventory."
}
args.output.write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({k:value for k,value in result.items() if k not in ["members","sources","unsafe_implementation_axioms_separately_classified"]},indent=2))
