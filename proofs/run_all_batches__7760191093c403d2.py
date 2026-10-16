#!/usr/bin/env python3
import concurrent.futures,hashlib,json,os,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BUILD=Path('/workspace/scratch/b9ccc76d924e/build-cap3116')
LEAN='/workspace/scratch/b9ccc76d924e/toolchain-116/lean'

def one(src):
    t=time.monotonic()
    cmd=[LEAN,'-j1','-DElab.async=false','-o',str(BUILD/(src.stem+'.olean')),str(BUILD/src.name)]
    with (ROOT/'development'/f'{src.stem}-build.log').open('w') as log:
        r=subprocess.run(cmd,cwd=BUILD,env={**os.environ,'LEAN_PATH':str(BUILD)},stdout=log,stderr=subprocess.STDOUT)
    result={'module':src.stem,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'elapsed_s':time.monotonic()-t,'exit':r.returncode,'command':cmd}
    (ROOT/'development'/f'{src.stem}-build.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)
    return result

sources=sorted(ROOT.glob('Cap3AllBatch*.lean'))
# Every batch is rebuilt from its recorded source bytes.
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    results=list(pool.map(one,sources))
(ROOT/'development'/'all-batch-build-results.json').write_text(json.dumps(results,indent=2)+'\n')
raise SystemExit(any(x['exit'] for x in results))
