#!/usr/bin/env python3
"""Splice two phases of decimal p8/m20 bulk, check transient moving wall by exact pair arithmetic."""
import argparse, json, pathlib, re, statistics

def load(path):
    raw=pathlib.Path(path).read_text()
    line=next(x for x in raw.splitlines() if x.startswith('SCC p=8 ') and 'cyclen=20' in x)
    pathrow,cycrow=line.split(' path=',1)[1].split(' cyc=')
    parse=lambda s:[[int(y) for y in z.split(',')] for z in re.findall(r'\[([^]]+)\]',s)]
    p,c=parse(pathrow),parse(cycrow)
    assert len(p)==39 and len(c)==20 and len(p[0])==len(c[0])==8
    return [v[0] for v in p],[[v[t] for v in c] for t in range(8)]

def step(p):
    carry=0;dig=[]
    for x in p:
        z=x+carry;dig.append(z%10);carry=z//10
    if carry:dig.append(carry)
    out=[dig[i]+dig[-1-i] for i in range(len(dig))]
    assert len(out)==len(p)+(1 if carry else 0)
    return out,carry

def span(p,t,seam,shift,w):
    low=p[:len(p)//2];lo=seam-45;hi=seam+160
    assert lo>50 and hi<len(low)-30
    a=lambda x:w[t%8][(x-39)%20]
    b=lambda x:w[t%8][(x-39+shift)%20]
    start=next((x for x in range(lo,hi) if low[x]!=a(x)),None)
    end=next((x for x in range(hi-1,lo-1,-1) if low[x]!=b(x)),None)
    return {'first_not_A':start,'last_not_B':end,'width':max(0,end-start+1) if start is not None and end is not None else 0}

def run(prefix,w,offset,shift,half,horizon):
    seam=300+offset
    low=[prefix[i] if i<39 else w[0][(i-39+(shift if i>=seam else 0))%20] for i in range(half)]
    p=low+low[::-1];h=[];overflow=[]
    for t in range(horizon+1):
        if t in (0,8,16,32,64):h.append({'t':t,**span(p,t,seam,shift,w)})
        if t==horizon:break
        p,g=step(p);overflow.append(g)
    return h,overflow

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--scc',default='calculation/decimal_frontier/lattice_formats/p8_scc.txt');ap.add_argument('--output',default='');a=ap.parse_args()
    prefix,w=load(a.scc);groups={t:[] for t in (8,16,32,64)};good=0;fail=0;minimum={}
    for offset in range(20):
        for shift in range(1,20):
            events,overflow=run(prefix,w,offset,shift,1000,64)
            if overflow==[1 if i%2==0 else 0 for i in range(64)]:good+=1
            else:fail+=1
            for e in events:
                if e['t'] in groups:
                    t=e['t'];v=e['width'];groups[t].append(v)
                    if t not in minimum or v<minimum[t]['width']:
                        minimum[t]={'width':v,'offset':offset,'shift':shift,'first_not_A':e['first_not_A'],'last_not_B':e['last_not_B']}
    out={'base':10,'p':8,'m':20,'seams':20,'nonzero_shifts':19,'seeds':380,'half_length':1000,'horizon':64,
         'overflow_schedule_matches':good,'overflow_schedule_mismatches':fail,'summary':{str(t):{'minimum':min(v),'median':statistics.median(v),'maximum':max(v),'count_width_le_8':sum(x<=8 for x in v),'argmin':minimum[t]} for t,v in groups.items()},'scope':'exact digit-list coefficient normalization; spliced phases only, no repaired active interface, not a Lychrel result'}
    print(json.dumps(out,indent=2))
    if a.output:pathlib.Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
