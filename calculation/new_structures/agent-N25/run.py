#!/usr/bin/env python3
"""Build and check two independent algorithms for every step; writes no evidence files to the repo."""
import argparse, subprocess, tempfile, pathlib, hashlib, json, time
P=pathlib.Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--steps',type=int,default=20000);parser.add_argument('--gap',type=int,default=40001)
a=parser.parse_args(); assert a.gap>2*a.steps
with tempfile.TemporaryDirectory() as td:
    T=pathlib.Path(td);outputs=[]
    for nm in ['direct','oracle']:
        b=T/nm
        subprocess.run(['g++','-O3','-std=c++17',str(P/(nm+'.cpp')),'-o',str(b)],check=True)
        ts=time.monotonic();r=subprocess.run([str(b),str(a.steps),str(a.gap),str(T/(nm+'.tsv')),str(T/(nm+'.txt'))],capture_output=True,text=True,check=True)
        print(r.stdout.strip(), 'seconds=',round(time.monotonic()-ts,3),flush=True)
        outputs.append((T/(nm+'.tsv'),T/(nm+'.txt')))
    for x,y in zip(outputs[0],outputs[1]):
        assert x.read_bytes()==y.read_bytes(),f'independent mismatch: {x.name}'
    last=outputs[0][1].read_bytes().strip()
    lines=outputs[0][0].read_text().splitlines()
    assert len(lines)==a.steps+1
    summary={'steps':a.steps,'gap':a.gap,'seed_packets':['1789','3141','5926','5358'],'seed_length':16+3*a.gap,'final_length':len(last),'final_sha256':hashlib.sha256(last).hexdigest(),'last':lines[-1].split('\t')[:4], 'checkpoints':[]}
    for t in [0,1,2,3,10,100,1000,5000,10000,15000,20000]:
        if t<=a.steps:
            t0,N,ov,h,prefix,suffix=lines[t].split('\t')
            summary['checkpoints'].append({'t':int(t0),'digits':int(N),'overflows':int(ov),'vacuum_lower_bound':a.gap-2*t+int(ov),'fnv64':h,'prefix':prefix,'suffix':suffix})
    print(json.dumps(summary,indent=2))
