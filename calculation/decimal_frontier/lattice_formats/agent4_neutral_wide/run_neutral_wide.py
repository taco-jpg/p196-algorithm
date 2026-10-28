#!/usr/bin/env python3
"""Complete, restartable agent-4 neutral-centre width-12/10 exclusion.
All work files are outside the repository, and success markers are atomic.
Soundness: each coefficient/carry bitmask overapproximates all concrete values,
so a frozen lattice mismatch excludes a prefix only when its target bit is
absent; every complete assignment has singleton exact transitions. Exhausting
all first-digit prefixes for both n-parities with zero survivors at finite H
therefore excludes a centre of that width and ANY temporal period.
Run: python3 calculation/decimal_frontier/lattice_formats/agent4_neutral_wide/run_neutral_wide.py --workdir /tmp/agent4-k1
Add --controls-only for independent checker and short positive/negative controls.
"""
import argparse, hashlib, json, os, re, resource, subprocess, time
from pathlib import Path
HERE=Path(__file__).resolve().parent
REPO=Path(os.environ.get("P196_REPO",str(HERE.parents[3]))).resolve()
SRC=REPO/'calculation/decimal_frontier/lattice_formats/code/kinkdfs_mask.cpp'

def run(args,**kwargs):
    return subprocess.run(list(map(str,args)),check=True,text=True,capture_output=True,**kwargs).stdout

def parse_count(output):
    m=re.search(r'survivors=(\d+)',output)
    if not m:raise AssertionError('Missing survivor count: '+output)
    return int(m[1])

def limit():
    os.nice(10)
    resource.setrlimit(resource.RLIMIT_AS,(3*1024**3,3*1024**3))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--workdir',type=Path,default=Path('/tmp/agent4-neutral-wide'))
    ap.add_argument('--controls-only',action='store_true')
    a=ap.parse_args();a.workdir.mkdir(parents=True,exist_ok=True)
    exe=a.workdir/'kinkdfs_mask'
    run(['g++','-O3','-std=c++17','-DNDEBUG',SRC,'-o',exe])
    data=HERE/'data'
    reference=HERE/'independent_kink_check.py'
    result=run(['python3',reference,exe,data])
    assert '36 PASS' in result and 'Base-26 known-centre positive control: (4, 2) PASS' in result,result
    print(result,flush=True)
    for name,width,H in [('p11',6,30),('p12',6,30)]:
        inp=data/f'neutral_{name}.txt'
        for o in (0,1):
            txt=run([exe,inp,width,H,o,o+1],preexec_fn=limit)
            assert parse_count(txt)==0,(name,o,txt)
            print('previous result control',name,o,'PASS',flush=True)
    if a.controls_only:return
    for name,width,H in [('p11',12,100),('p12',10,80)]:
        inp=data/f'neutral_{name}.txt'
        source_digest=hashlib.sha256(SRC.read_bytes()+inp.read_bytes()).hexdigest()
        for o in (0,1):
            for d in range(19):
                stem=a.workdir/f'{name}_o{o}_d{d:02d}'
                done=stem.with_suffix('.done')
                if done.exists():
                    recorded=json.loads(done.read_text())
                    assert recorded['name']==name and recorded['width']==width and recorded['H']==H and recorded['o']==o and recorded['digit']==d and recorded['survivors']==0 and recorded['source_digest']==source_digest
                    continue
                started=time.monotonic()
                output=run([exe,inp,width,H,o,o+1,d],preexec_fn=limit)
                survivors=parse_count(output)
                if survivors:raise RuntimeError(f'UNDECIDED: survivor {name} {o} {d}: {output}')
                rec=dict(name=name,width=width,H=H,o=o,digit=d,source_digest=source_digest,survivors=survivors,wall_s=round(time.monotonic()-started,3),output=output.strip())
                tmp=stem.with_suffix('.tmp')
                tmp.write_text(json.dumps(rec,indent=2)+'\n')
                os.replace(tmp,done)
                print(name,o,d,'PASS',flush=True)
        assert sum(1 for o in (0,1) for d in range(19) if (a.workdir/f'{name}_o{o}_d{d:02d}.done').exists())==38
        print(name,'ALL 38 PREFIXES PASS: no indefinitely surviving centre for the stated width',flush=True)

if __name__=='__main__':main()
