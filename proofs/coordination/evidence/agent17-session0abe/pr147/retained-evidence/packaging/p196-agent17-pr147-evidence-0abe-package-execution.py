#!/usr/bin/env python3
from pathlib import Path
import datetime, hashlib, json, subprocess
BASE=Path('/dev/shm')
NAME='p196-agent17-pr147-evidence-0abe'
sha=lambda b:hashlib.sha256(b).hexdigest()
script=BASE/(NAME+'-package.py')
command=['python',str(script)]
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
process=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
stdout=BASE/(NAME+'-packaging.stdout.txt')
stderr=BASE/(NAME+'-packaging.stderr.txt')
stdout.write_bytes(process.stdout)
stderr.write_bytes(process.stderr)
receipt=BASE/(NAME+'-packaging-execution.json')
receipt.write_text(json.dumps({'command':command,'started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':process.returncode,'script_sha256':sha(script.read_bytes()),'stdout':{'path':str(stdout),'bytes':len(process.stdout),'sha256':sha(process.stdout)},'stderr':{'path':str(stderr),'bytes':len(process.stderr),'sha256':sha(process.stderr)},'lean_processes_executed':0},indent=2)+'\n')
artifacts=[BASE/(NAME+s) for s in ['.tar.xz','-package.py','-package-execution.py','-packaging-verification.json','-packaging.stdout.txt','-packaging.stderr.txt','-packaging-execution.json']]
external=BASE/(NAME+'-PACKAGING-ARTIFACTS.json')
entries={str(p):{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in artifacts if p.exists()}
external.write_text(json.dumps({'scope':'All new external packaging artifacts. This manifest excludes itself to avoid recursive hashing. Original review directory and its original NEW-ARTIFACTS.json remain unchanged.','status':'PASS' if process.returncode==0 else 'FAIL','files':entries},indent=2)+'\n')
print(json.dumps({'exit_code':process.returncode,'files':entries,'external_manifest':{'path':str(external),'bytes':external.stat().st_size,'sha256':sha(external.read_bytes())}},indent=2))
if process.returncode:print(process.stderr.decode())
raise SystemExit(process.returncode)

