import hashlib, io, json, lzma, re, tarfile, urllib.request
url = "https://raw.githubusercontent.com/taco-jpg/p196-algorithm/10a173cb635fa8d03e357f454232816fc3e77609/proofs/contributions/agent-103/residual-five-fibers-20261016/evidence/complete-replay-evidence.tar.xz"
with urllib.request.urlopen(url, timeout=30) as response:
    packed = response.read(200001)
assert len(packed) == 139624
assert hashlib.sha256(packed).hexdigest() == "1c649565710514ba3896293a5265978c70d98cacf117f2d8eadf43cbd9aac596"
decoder = lzma.LZMADecompressor()
raw = decoder.decompress(packed, max_length=3276801)
assert decoder.eof and len(raw) == 3276800
assert hashlib.sha256(raw).hexdigest() == "3642091361a51e46c578e9e93b99d75b3aa9653d3796499ee80c92b1c4643a12"
archive = tarfile.open(fileobj=io.BytesIO(raw), mode="r:")
members = archive.getmembers()
assert len(members) == 143
assert len({m.name for m in members}) == 143
assert all(m.isfile() and not m.name.startswith("/") and ".." not in m.name.split("/") for m in members)
files = {m.name: archive.extractfile(m).read() for m in members}
index = json.loads(files["FILES.json"])
assert set(index) | {"FILES.json"} == set(files)
for path, meta in index.items():
    assert len(files[path]) == meta["bytes"], path
    assert hashlib.sha256(files[path]).hexdigest() == meta["sha256"], path
v = json.loads(files["verification-clean-001/verification.json"])
assert v["status"] == "PASS" and v["module_count"] == 22
assert len(v["commands"]) == 25
assert all(c["exit_code"] == 0 for c in v["commands"])
for command in v["commands"]:
    path = "verification-clean-001/" + command["log"]
    assert hashlib.sha256(files[path]).hexdigest() == command["log_sha256"], path
builds = [c for c in v["commands"] if c["label"] in v["build_order"]]
assert len(builds) == 22
assert all(all(flag in c["argv"] for flag in ["--trust=0", "-j1", "-DElab.async=false"]) for c in builds)
audit = files["verification-clean-001/logs/AuditAllContributionModules.log"].decode()
inventory = re.findall(r"^AUDIT_THEOREM (\S+) ([^\n]+)$", audit, re.M)
names = [n for _, n in inventory]
completion = re.findall(r"^AUDIT_COMPLETE ([0-9]+)$", audit, re.M)
assert len(names) == len(set(names)) == 1812 and completion == ["1812"]
printed = [(n, []) for n in re.findall(r"^'([^\n]+)' does not depend on any axioms$", audit, re.M)]
printed += [(n, [a.strip() for a in used.split(",") if a.strip()]) for n, used in re.findall(r"^'([^\n]+)' depends on axioms:\s*\[([^\]]*)\]$", audit, re.M)]
assert len(printed) == 1812 and {n for n, _ in printed} == set(names)
assert all(set(a) <= {"propext", "Classical.choice", "Quot.sound"} for _, a in printed)
unsafe = re.findall(r"^UNSAFE_IMPL (\S+) ([^\n]+)$", audit, re.M)
assert len(unsafe) == 33
structural = json.loads(files["registry-check-only-001/verification.json"])
result = {"status":"PASS_RETAINED_EVIDENCE_INSPECTION","source_commit":"10a173cb635fa8d03e357f454232816fc3e77609","archive_sha256":hashlib.sha256(packed).hexdigest(),"archive_git_blob":hashlib.sha1(("blob "+str(len(packed))+"\0").encode()+packed).hexdigest(),"archive_members":143,"indexed_member_hashes_checked":142,"archive_file_index_sha256":hashlib.sha256(files["FILES.json"]).hexdigest(),"payload_bytes":sum(map(len,files.values())),"original_build_status":v["status"],"original_build_started":v.get("started_utc"),"original_build_finished":v.get("finished_utc"),"original_compilation_count":len(builds),"original_command_count":len(v["commands"]),"original_all_command_exits_zero":True,"original_command_logs_hashes_checked":len(v["commands"]),"actual_raw_theorem_records":len(names),"actual_raw_axiom_results":len(printed),"allowed_axiom_union":sorted(set(a for _,used in printed for a in used)),"raw_unsafe_implementation_axiom_entries":len(unsafe),"unsafe_scope":"axiomInfo/isUnsafe branch only, not all unsafe definitions","original_structural_status":structural.get("status"),"original_structural_math_check":structural.get("mathematical_proof_check"),"original_structural_repository_wide_pass":structural.get("repository_wide_pass"),"fresh_lean_execution":False,"disk_extraction":False,"network_source":url,"python_version":__import__("sys").version,"verification_record_sha256":hashlib.sha256(files["verification-clean-001/verification.json"]).hexdigest(),"raw_audit_log_sha256":hashlib.sha256(files["verification-clean-001/logs/AuditAllContributionModules.log"]).hexdigest()}
print(json.dumps(result, indent=2))
