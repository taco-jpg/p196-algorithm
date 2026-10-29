#!/usr/bin/env python3
"""Self-contained all-height 32-state spatial renormalisation of decimal P_15 bulk.
Only standard Python.  Can --write or --check its machine tables.
"""
from pathlib import Path
import json,sys
from collections import Counter

R=7
K=77
GAMMA=(0,1,1,0,0,0,0,1,0,1,0,1,0,0,1)

def sigma(z):return [v for x in z for v in (x,30-x)]
def factors():
    F=set()
    for a in (14,16):
        for b in (14,16):
            x=[a,b]
            for _ in range(R):x=sigma(x)
            F.update(tuple(x[j:j+K]) for j in range(len(x)-K+1))
    return sorted(F)

def a(x):return int(x>=10)
def H(x,y,z):
    r=2*(x+y-27);s=2*(y+z-27)
    return r+s-9*(a(r)+a(s))
def carry(z,i,dr):
    for j in (i,i+dr):
        if z[j]!=9:return a(z[j])
    raise AssertionError('two adjacent 9, symbolic radius insufficient')
def step(z,gamma):
    out=[]
    for i in range(3,len(z)-3):
        left=carry(z,i-1,-1)
        if gamma==0:out.append((z[i]+left)%10+(z[i]+carry(z,i+1,1))%10)
        else:out.append((z[i]+left)%10+(z[i-1]+carry(z,i,1))%10)
    return out

def minimal_machine(states,nexts,out):
    cmap={x:i for i,x in enumerate(sorted(set(out)))}
    cl=[cmap[x] for x in out]
    counts=[len(set(cl))]
    while True:
        signatures=[(cl[i],cl[nexts[i][0]],cl[nexts[i][1]]) for i in range(len(states))]
        kinds={sig:i for i,sig in enumerate(sorted(set(signatures)))}
        c2=[kinds[x] for x in signatures]
        counts.append(len(set(c2)))
        if counts[-1]==counts[-2]:
            cl=c2
            break
        cl=c2
        assert len(counts)<30
    table=[]
    for k in range(counts[-1]):
        members=[i for i,x in enumerate(cl) if x==k]
        sigs={(out[i],cl[nexts[i][0]],cl[nexts[i][1]]) for i in members}
        assert len(sigs)==1,(k,sigs)
        (val,left,right),=sigs
        table.append({'id':k,'output':val,'left':left,'right':right,'members':len(members)})
    return cl,counts,table

def build():
    fs=factors()
    assert len(fs)==240
    idx={w:i for i,w in enumerate(fs)}
    children=[]
    for w in fs:
        sw=sigma(w)
        left,right=tuple(sw[38:115]),tuple(sw[39:116])
        assert left in idx and right in idx
        children.append((idx[left],idx[right]))
    bytime={t:[] for t in range(3,16)}
    for w in fs:
        z=[H(*w[i:i+3]) for i in range(K-2)]
        for s in range(13):
            t=3+s
            bytime[t].append(z[37-3*s])
            if t<15:z=step(z,GAMMA[t])
    quotient=[]
    for t in range(3,16):
        cl,counts,table=minimal_machine(fs,children,bytime[t])
        quotient.append({'time':t,'alphabet':len(set(bytime[t])),'states':len(table),'refinement_counts':counts})
        if t==15:class_ids=cl;classes=table
    assert quotient[-1]['states']==32
    assert quotient[-1]['refinement_counts']==[8,32,32]
    return fs,children,bytime[15],class_ids,classes,quotient

def artifacts():
    F,S,O,cl,classes,history=build()
    lines=['# id 77-letter factor (0=14,1=16) output left_child right_child quotient_class']
    for i,w in enumerate(F):
        code=''.join('0' if v==14 else '1' for v in w)
        lines.append(f'{i}\t{code}\t{O[i]}\t{S[i][0]}\t{S[i][1]}\t{cl[i]}')
    evidence={'label':'PAPER PROOF finite renormalisation machine','base':10,
              'time':15,'substitution':'14->14 16;16->16 14',
              'window':77,'source_states':240,'quotient_states':32,
              'output_values':sorted(set(O)),'quotient_transitions':classes,
              'spatial_identity':'P15(h+1)[2*i-2],P15(h+1)[2*i-1] = outputs of the two induced children of the 77-factor centred at i-2 in w_h',
              'valid_region':'h>=7, 40<=i<=2^h-37',
              'refinement_by_time':history,
              'assumptions':'prior all-height bounded-neutral 15-step proof, gamma schedule 011000010101001; this is spatial, NOT temporal closure'}
    return '\n'.join(lines)+'\n',json.dumps(evidence,indent=2)+'\n'

def main():
    mode=sys.argv[1] if len(sys.argv)>1 else '--check'
    directory=Path(__file__).resolve().parent
    data=[(directory/'renorm32_states.tsv',artifacts()[0]),(directory/'renorm32_quotient.json',artifacts()[1])]
    if mode=='--write':
        for p,s in data:p.write_text(s)
    elif mode=='--check':
        for p,s in data:assert p.read_text()==s,p
    else:raise ValueError('only --write or --check')
    ev=json.loads(data[1][1]);print('RENORM_240_TO_32_PASS',len(ev['quotient_transitions']), 'time15 alphabet',ev['output_values'],
        'class_growth',[(x['time'],x['states']) for x in ev['refinement_by_time']]);
    print('DYADIC_SPATIAL_SUBSTITUTION_COMPOSITION_PASS')

if __name__=='__main__':main()
