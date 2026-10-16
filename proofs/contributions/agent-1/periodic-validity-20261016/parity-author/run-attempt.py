#!/usr/bin/env python3
"""Preserve source before every incremental periodic-parity checking attempt."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,time
root=Path(__file__).resolve().parents[5]
evidence=Path(__file__).resolve().parent
build=Path('/workspace/p196-agent1-session-20261016/periodic-validity-parity-build')
lean='/workspace/p196-tools/lean-4.19.0-linux/bin/lean'
name='Agent1PeriodicParity'
attempt=evidence/sys.argv[1]
attempt.mkdir(exist_ok=False)
data=(root/'proofs'/(name+'.lean')).read_bytes()
(attempt/(name+'.lean')).write_bytes(data)
(build/(name+'.lean')).write_bytes(data)
command=[lean,'--trust=0','-j1','-DElab.async=false','-o',name+'.olean',name+'.lean']
t=time.time()
r=subprocess.run(command,cwd=build,env=dict(os.environ,LEAN_PATH=str(build)),text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
(attempt/'build.log').write_text(r.stdout)
(attempt/'result.json').write_text(json.dumps({'command':command,'source_sha256':hashlib.sha256(data).hexdigest(),'exit_code':r.returncode,'elapsed_seconds':time.time()-t},indent=2)+'\n')
print(r.stdout,end='');print('exit',r.returncode)
sys.exit(r.returncode)
