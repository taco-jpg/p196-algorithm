#!/usr/bin/env python3
"""Agent #123: independent integer controls for the pinned Agent109 checker.

These are finite diagnostic replays, not proofs or a certificate search.
Every executed case is retained in a deterministic, losslessly compressed CSV.
"""
from __future__ import annotations
import argparse, csv, gzip, hashlib, importlib.util, io, itertools, json, pathlib, random, sys

PHASES = [c for c in range(1,18) if c != 9]
GAPS = [(2,2), (2,5), (5,2), (3,4)]
PIN = '5782d26068e7bb07192c098d943c0394116d4fc5'

def pairword(n: int) -> list[int]:
    d=[int(c) for c in str(n)[::-1]] if n else []
    return [x+y for x,y in zip(d,reversed(d))]

def template(c: int,B: list[int],A: list[int],C: list[int],g: int,h: int) -> list[int]:
    return B+[c]*g+A+[18-c]*h+C+[18-c]*h+A[::-1]+[c]*g+B[::-1]

def realize(q: list[int], variant: int) -> int:
    if not q or q != q[::-1] or not 1 <= q[0] <= 18:
        raise ValueError('Noncanonical mirrored input')
    if len(q)%2 and q[len(q)//2]%2: raise ValueError('Odd center')
    d=[0]*len(q)
    for i in range(len(q)//2):
        s=q[i]
        high=min(s,9) if variant==0 else max(s-9, int(i==0))
        d[len(q)-1-i]=high; d[i]=s-high
    if len(q)%2: d[len(q)//2]=q[len(q)//2]//2
    if not all(0<=v<=9 for v in d) or not d[-1]: raise ValueError('Invalid digit realization')
    n=int(''.join(str(v) for v in d[::-1]))
    if pairword(n)!=q: raise AssertionError('Realization mismatch')
    return n

def reverse_add(n: int) -> int:
    # Ordinary decimal integer operation; no template/carry routine is used.
    return n+int(str(n)[::-1])

def main() -> None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('repo_root', type=pathlib.Path);p.add_argument('output',type=pathlib.Path)
    a=p.parse_args();out=a.output.resolve()
    if out.exists(): raise SystemExit('Output must be new')
    out.mkdir(parents=True)
    source=a.repo_root/'proofs/contributions/agent-109/template-return-certificate/certificate_tool.py'
    b=source.read_bytes(); blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
    if blob!=PIN:raise SystemExit('Unexpected certificate_tool.py blob')
    spec=importlib.util.spec_from_file_location('agent109_pinned_tool',source)
    ct=importlib.util.module_from_spec(spec); spec.loader.exec_module(ct)
    report={'agent':123,'status':'RUNNING','tool_git_blob':blob,'tool_sha256':hashlib.sha256(b).hexdigest(),
            'domain':{'phases':PHASES,'B':'empty or one coefficient 1..18',
              'A':'empty or one coefficient 0..18','C':'empty or one even coefficient 0..18',
              'gaps':GAPS,'realizations':'two deterministic digit-split rules'},
            'finite_scope_only':True,'raw_format':'CSV gzip, all executed rows retained'}
    count=0; overflow=0; pal_start=0
    compressed=out/'integer-controls.csv.gz'
    try:
        with compressed.open('wb') as raw, gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0) as gz:
            with io.TextIOWrapper(gz,encoding='utf-8',newline='') as text:
                wr=csv.writer(text);wr.writerow(['index','phase','B','A','C','g','h','split','n','Tn','gamma','Tn_palindrome','raw_pair_match','trim_pair_match'])
                for c,B,A,C in itertools.product(PHASES,[[]]+[[i] for i in range(1,19)],
                                                 [[]]+[[i] for i in range(19)],
                                                 [[]]+[[i] for i in range(0,19,2)]):
                    cp,Br,Ar,Cr,gam,pal=ct.successor(c,B,A,C)
                    trimmed,tr=ct.trim(cp,Br,Ar,Cr)
                    for g,h in GAPS:
                        q=template(c,B,A,C,g,h)
                        rawq=template(cp,Br,Ar,Cr,g-2+gam,h-2+gam)
                        trimq=template(*trimmed,g-2+gam+tr[0]+tr[1],h-2+gam+tr[2]+tr[3])
                        for variant in (0,1):
                            n=realize(q,variant);m=reverse_add(n)
                            pflag=str(m)==str(m)[::-1]
                            qactual=pairword(m)
                            matches=(qactual==rawq,qactual==trimq)
                            wr.writerow([count,c,json.dumps(B),json.dumps(A),json.dumps(C),g,h,variant,n,m,gam,int(pflag),*map(int,matches)])
                            if not all(matches) or pal!=pflag or len(str(m))-len(str(n))!=gam or pflag:
                                raise AssertionError({'case':count,'state':[c,B,A,C],'n':n,'m':m,'matches':matches,'pal':pal})
                            count+=1;overflow+=gam;pal_start+=str(n)==str(n)[::-1]
        # Negative/positive boundary controls for the actual finite-time statement.
        rng=random.Random(12320261015);horizon_rows=[]
        for i in range(4096):
            c=rng.choice(PHASES)
            B=[rng.randrange(19) for _ in range(rng.randrange(7))]
            if B:B[0]=rng.randrange(1,19)
            A=[rng.randrange(19) for _ in range(rng.randrange(7))]
            left=[rng.randrange(19) for _ in range(rng.randrange(5))]
            C=left+([2*rng.randrange(10)] if rng.randrange(2) else [])+left[::-1]
            k=rng.randrange(7);g=2*k+2+rng.randrange(4);h=2*k+2+rng.randrange(4)
            n=realize(template(c,B,A,C,g,h),i%2);orbit=[n];flags=[]
            for _ in range(k+1):
                orbit.append(reverse_add(orbit[-1]));flags.append(str(orbit[-1])==str(orbit[-1])[::-1])
            horizon_rows.append({'index':i,'state':[c,B,A,C],'g':g,'h':h,'k':k,'orbit':orbit,'palindromes':flags})
            if any(flags):raise AssertionError(horizon_rows[-1])
        data=(json.dumps(horizon_rows,separators=(',',':'))+'\n').encode()
        (out/'horizon-controls.json.gz').write_bytes(gzip.compress(data,mtime=0))
        # Concrete endpoint probes only. They do not assert any all-width result.
        report['time_zero_probe']={'n':11888811,'Tn':23777622,'phase':2,'B':[],'A':[],'C':[],'g':2,'h':2,
           'initial_palindrome':str(11888811)==str(11888811)[::-1],
           'next_palindrome':str(23777622)==str(23777622)[::-1]}
        if pairword(11888811)!=template(2,[],[],[],2,2) or reverse_add(11888811)!=23777622:
            raise AssertionError('Time-zero probe mismatch')
        report.update(status='PASS',integer_controls=count,overflow_controls=overflow,
                      palindromic_initial_realizations=pal_start,horizon_templates=len(horizon_rows),
                      horizon_successor_checks=sum(len(x['palindromes']) for x in horizon_rows))
    except BaseException as e:
        report.update(status='FAIL',error=str(e),completed_integer_controls=count);raise
    finally:
        files=[]
        for f in out.glob('*.gz'):
            bs=f.read_bytes();decoded=gzip.decompress(bs)
            files.append({'path':f.name,'bytes':len(bs),'sha256':hashlib.sha256(bs).hexdigest(),
              'decoded_bytes':len(decoded),'decoded_sha256':hashlib.sha256(decoded).hexdigest(),
              'recovery':'gzip -dc '+f.name})
        report['raw_files']=files
        (out/'controls-result.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps({k:v for k,v in report.items() if k not in ('raw_files','domain')},indent=2))

if __name__=='__main__':main()
