from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess

repo = Path(__file__).resolve().parents[5]
reviews = Path(__file__).resolve().parent
commit = "71691d50497edc83247b3571af276bb0ee438491"
registry_path = "proofs/Agent101ProtectedFamily.registry.json"
registry_expected = "04aba56fc69ef566d32b0c1064a4db2298f095d88e98fcd9fefe7f5c70614307"
verifier_path = "proofs/verify_project__214bf7673efe116b.py"
env = os.environ.copy()
env["GIT_NO_LAZY_FETCH"] = "1"
sha = lambda b: hashlib.sha256(b).hexdigest()
git_blob = lambda b: hashlib.sha1(f"blob {len(b)}\0".encode() + b).hexdigest()
commands = []

def git_show(path):
    command = ["git", "show", commit + ":" + path]
    result = subprocess.run(command, cwd=repo, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    commands.append({"command": command, "returncode": result.returncode, "stderr": result.stderr.decode(errors="replace")})
    assert result.returncode == 0, commands[-1]
    return result.stdout

registry_bytes = (repo / registry_path).read_bytes()
registry_committed = git_show(registry_path)
assert registry_bytes == registry_committed
assert sha(registry_bytes) == registry_expected
registry = json.loads(registry_bytes)
modules = registry["projects"]["agent101-protected-family"]["modules"]
assert len(modules) == 26
records = []
committed = {}
for module, spec in modules.items():
    body = git_show(spec["path"])
    committed[module] = body
    workspace = (repo / spec["path"]).read_bytes()
    row = {"module": module, "path": spec["path"], "bytes": len(body),
           "committed_sha256": sha(body), "workspace_sha256": sha(workspace),
           "registry_sha256": spec["sha256"], "committed_git_blob": git_blob(body),
           "registry_git_blob": spec["git_blob"], "workspace_equals_commit": workspace == body}
    row["pass"] = workspace == body and sha(body) == spec["sha256"] and git_blob(body) == spec["git_blob"]
    records.append(row)
    assert row["pass"], row
adapter_checks = []
for module, spec in modules.items():
    if "adapter" not in spec:
        continue
    a = spec["adapter"]
    small = committed[module].splitlines(keepends=True)
    big = committed[a["container_module"]].splitlines(keepends=True)
    start = a["embedded_start_line_1_based"] - 1
    count = a["embedded_line_count"]
    equal = small[0] == b"import Std\n" and big[0] == b"import Std\n" and count == len(small) - 1 and small[1:] == big[start:start+count]
    adapter_checks.append({"module": module, "container": a["container_module"],
        "excluded_original_first_line": small[0].decode().rstrip(), "embedded_start_line_1_based": start + 1,
        "embedded_line_count": count, "entire_original_body_byte_identical": equal})
    assert equal
verifier_committed = git_show(verifier_path)
assert verifier_committed == (repo / verifier_path).read_bytes()
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, env=env, text=True).strip()
report = {"result": "PASS", "checked_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "commit": commit, "observed_head": head, "repository": str(repo), "registry_path": registry_path,
    "registry_sha256": sha(registry_bytes), "registry_workspace_equals_commit": True,
    "module_count": len(records), "modules": records, "adapter_checks": adapter_checks,
    "verifier_path": verifier_path, "verifier_sha256": sha(verifier_committed),
    "verifier_workspace_equals_commit": True, "read_only_git_commands": commands,
    "GIT_NO_LAZY_FETCH": "1", "git_writes_performed": False}
(reviews / "final-source-readback.json").write_text(json.dumps(report, indent=2) + "\n")
(reviews / "final-registry.json").write_bytes(registry_bytes)
print(json.dumps({k: report[k] for k in ["result", "commit", "observed_head", "registry_sha256", "module_count", "adapter_checks", "verifier_sha256"]}, indent=2))
