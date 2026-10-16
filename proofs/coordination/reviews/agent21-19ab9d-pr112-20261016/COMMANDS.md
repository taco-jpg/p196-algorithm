# Agent #21 executed evidence commands

## Exact-head reconciliation

Command (exit0; tool chunk8636ef):

```bash
python verify_pr112_ci.py --archive agent21-pr112-ci-38972796223.zip --inputs pr112_sources.json --retained-checkout /workspace/scratch/8b5152316f75/p196-agent4 --output pr112-ci-reconciliation-001.json
```

Exact stdout:

```text
{
  "status": "PASS_RETAINED_CI_SOURCE_COMMAND_LOG_AND_AXIOM_RECONCILIATION",
  "source_head": "01ecb6aa6bc555335ff6cb628d08e84133888307",
  "workflow_run": 38972796223,
  "workflow_job": 117214969242,
  "workflow_artifact": 12077672528,
  "ci_checkout_merge_commit": "4d10aa839c074cb2d04013ed8d3aee967677c09a",
  "ci_checkout_base": "f44c06c4851b26523bcec920d93a52b93fd2a0a6",
  "zip_sha256": "01495e6a8fe41c13c2eb35ee8374f3c2c0ace5ccd712cf3dc2a97682bdb9bec5",
  "zip_bytes": 99654,
  "member_count": 19,
  "member_bytes": 564821,
  "commands_reconciled": 17,
  "fresh_source_compilations_reused": 13,
  "retained_compiler_flags": [
    "-j1",
    "-DElab.async=false"
  ],
  "retained_explicit_trust_zero": false,
  "theorem_constants_reconciled": 1012,
  "theorems_per_module": {
    "ArithmeticCRT": 4,
    "DigitPools": 36,
    "GrowingSuffix": 5,
    "Lychrel196Research": 787,
    "ModularSpan": 9,
    "ModulusSplit": 5,
    "OuterBlock": 10,
    "PairWeights": 38,
    "PalindromeDigits": 73,
    "PeriodExistence": 20,
    "ResidueOrbit": 9,
    "Saturation": 10,
    "SharpSuffix": 6
  },
  "permitted_axiom_union": [
    "Classical.choice",
    "Quot.sound",
    "propext"
  ],
  "literal_exports": {
    "Agent111.GrowingSuffix.powerTen_saturation": [
      "Classical.choice",
      "Quot.sound",
      "propext"
    ],
    "Agent111.GrowingSuffix.variable_powerTen_closed_set_contains_palindrome": [
      "Classical.choice",
      "Quot.sound",
      "propext"
    ],
    "Agent111.GrowingSuffix.half_width_suffix_closed_set_contains_palindrome": [
      "Classical.choice",
      "Quot.sound",
      "propext"
    ],
    "Agent111.GrowingSuffix.palindrome_with_given_suffix": [
      "Classical.choice",
      "Quot.sound",
      "propext"
    ],
    "Agent111.GrowingSuffix.variable_half_suffix_closed_set_contains_palindrome": [
      "Classical.choice",
      "Quot.sound",
      "propext"
    ],
    "Agent111.GrowingSuffix.exact_half_suffix_closed_set_contains_palindrome": [
      "Classical.choice",
      "Quot.sound",
      "propext"
    ]
  },
  "new_lean_execution": "NOT_RUN",
  "independent_fresh_build": "NOT_RUN_BY_AGENT21",
  "import_audit_interpretation": "Origin and transitive axiom inspection; not a new kernel replay of imported proof terms.",
  "coverage_limit": "Theorem constants and their transitive axiom chains were audited. This artifact does not claim a separate all-safe-definition inventory."
}
```

The exact executed script and inputs are retained in ci/verify_pr112_ci.py and ci/pr112_sources.json. It reads archives and source bytes; it never invokes Lean. Its output path must not exist so earlier attempts cannot be overwritten.

## Artifact download command, temporary URL value omitted

The first ordinary sandbox invocation failed, exit1, chunk34dc2a:

```text
{"status": "DOWNLOAD_FAILED", "error_type": "URLError", "reason": "[Errno 1] Operation not permitted"}
```

The identical computation was then authorized through the legitimate elevated download approval, successfully downloaded and saved the original ZIP, and exited0 (initial chunk047a8a; completion74ff6c). Printing the large raw verification.json exceeded tool-display output limits; the complete untruncated original is preserved inside the ZIP.

```python
import urllib.request,hashlib,zipfile,io,json
from pathlib import Path
url="<connector-returned temporary artifact download URL; not retained>"
try:
 data=urllib.request.urlopen(url,timeout=20).read()
except Exception as e:
 print(json.dumps({"status":"DOWNLOAD_FAILED","error_type":type(e).__name__,"reason":str(getattr(e,"reason",""))}));raise SystemExit(1)
assert len(data)==99654
assert hashlib.sha256(data).hexdigest()=="01495e6a8fe41c13c2eb35ee8374f3c2c0ace5ccd712cf3dc2a97682bdb9bec5"
z=zipfile.ZipFile(io.BytesIO(data))
print(json.dumps({"status":"PASS_DOWNLOADED_ARTIFACT_IDENTITY","bytes":len(data),"sha256":hashlib.sha256(data).hexdigest(),"members":[{"name":f.filename,"bytes":f.file_size,"sha256":hashlib.sha256(z.read(f)).hexdigest()} for f in z.infolist()]},indent=2))
p=Path("/workspace/scratch/19ab9d430efc/agent21-pr112-ci-38972796223.zip")
try:
 p.write_bytes(data)
 print(json.dumps({"saved_zip":str(p)}))
except OSError as e:print(json.dumps({"save_failed":e.errno,"reason":e.strerror}))
for n in z.namelist():
 if n.endswith("verification.json"):
  v=json.loads(z.read(n));print("VERIFICATION",json.dumps(v,indent=2))

```

## Historical archive download command, temporary URL values omitted

```python
import urllib.request,hashlib,zipfile,io,json
from pathlib import Path
jobs=json.loads(r'''[{"name":"historical-core","artifact":12076648408,"run":38971847141,"sha256":"957e7d0598fe3a5b766619f67398e5ac708b2918b57c6624d1b0b81e3143caab","url":"<temporary connector download URL omitted>"},{"name":"historical-sharp","artifact":12077712695,"run":38972428087,"sha256":"50bb5472ecb9124e36e8370c5643075130c05b520a30c75e18f13449b39a3966","url":"<temporary connector download URL omitted>"}]''')
base=Path('/workspace/scratch/19ab9d430efc')
records=[]
for task in jobs:
 data=urllib.request.urlopen(task['url'],timeout=20).read(2_000_000)
 assert hashlib.sha256(data).hexdigest()==task['sha256']
 z=zipfile.ZipFile(io.BytesIO(data));assert z.testzip() is None
 path=base/('agent21-pr112-'+task['name']+'-ci.zip')
 assert not path.exists()
 path.write_bytes(data)
 record={k:v for k,v in task.items() if k!='url'}
 record.update(status='PASS_HISTORICAL_ARCHIVE_IDENTITY_AND_CRC',bytes=len(data),path=str(path),members=[{'path':f.filename,'bytes':f.file_size,'sha256':hashlib.sha256(z.read(f)).hexdigest()} for f in z.infolist()],new_lean_execution='NOT_RUN')
 records.append(record)
 print(json.dumps({k:v for k,v in record.items() if k!='members'}),flush=True)
(base/'pr112-historical-ci-preservation.json').write_text(json.dumps(records,indent=2)+'\n')

```

Exit0, chunk438c96; exact stdout:

```text
{"name": "historical-core", "artifact": 12076648408, "run": 38971847141, "sha256": "957e7d0598fe3a5b766619f67398e5ac708b2918b57c6624d1b0b81e3143caab", "status": "PASS_HISTORICAL_ARCHIVE_IDENTITY_AND_CRC", "bytes": 98948, "path": "/workspace/scratch/19ab9d430efc/agent21-pr112-historical-core-ci.zip", "new_lean_execution": "NOT_RUN"}
{"name": "historical-sharp", "artifact": 12077712695, "run": 38972428087, "sha256": "50bb5472ecb9124e36e8370c5643075130c05b520a30c75e18f13449b39a3966", "status": "PASS_HISTORICAL_ARCHIVE_IDENTITY_AND_CRC", "bytes": 99662, "path": "/workspace/scratch/19ab9d430efc/agent21-pr112-historical-sharp-ci.zip", "new_lean_execution": "NOT_RUN"}
```

## Binary publication transport

Each ZIP was read without modification and Base64-encoded in consecutive12288-byte slices using Python pathlib and base64.b64encode; nine slices per ZIP were concatenated in their original order. Each encoded result's length was checked against4*ceil(original_bytes/3). Temporary artifact download credentials were not included. Readback compares every published UTF-8 blob and the complete Base64 strings; archive SHA256 and per-member identities are independently recorded.
