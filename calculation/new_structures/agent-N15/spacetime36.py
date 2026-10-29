#!/usr/bin/env python3
"""Finite complete-factor proof and 36-state 16-row dyadic spacetime substitution.
Self-contained standard-Python checker. --write regenerates machine data, --check verifies.
"""
from pathlib import Path
from collections import defaultdict
import json,sys

R,K,EDGE,STOP,MARGIN=7,125,64,18,4
GAMMA=(0,1,1,0,0,0,0,1,0,1,0,1,0,0,1,0,0,1)

def sigma(z):return [q for x in z for q in (x,30-x)]
def w_h(h):
    w=[14]
    for _ in range(h):w=sigma(w)
    return w

def initial(h):
    H=[4]+w_h(h)
    return H+H[::-1]

def normal(p):
    d=[];c=0
    for x in p:
        z=x+c;d.append(z%10);c=z//10
    if c:d.append(c)
    return d

def reverse_add_pair(p):
    d=normal(p)
    return [d[i]+d[-1-i] for i in range(len(d))],d

def a(x):return int(x>=10)
def H(x,y,z):
    p,q=2*(x+y-27),2*(y+z-27)
    return p+q-9*(a(p)+a(q))

def predicted_third(h):
    w=w_h(h);m=len(w)+1
    q=[9,9]+[2*(w[i-1]-9) for i in range(2,m)]
    r=[10,9,q[2]-10]+[q[i]+q[i-1]-18 for i in range(3,m)]+[2*(q[-1]-9)]
    g=[1,0,14,5]+[r[i]+r[i-1]-9*(a(r[i])+a(r[i-1])) for i in range(4,len(r))]
    return g+g[::-1]

def maxrun9(z):
    m=v=0
    for x in z:
        v=v+1 if x==9 else 0;m=max(m,v)
    return m

def carry(z,j,step):
    for x in (j,j+step,j+2*step):
        if z[x]!=9:return a(z[x])
    raise AssertionError('three adjacent neutral 9 coefficients')

def local_step(z,gam):
    q=[]
    for i in range(MARGIN,len(z)-MARGIN):
        low=carry(z,i-1,-1)
        if gam==0:high=carry(z,i+1,+1);q.append((z[i]+low)%10+(z[i]+high)%10)
        else:high=carry(z,i,+1);q.append((z[i]+low)%10+(z[i-1]+high)%10)
    return q

def factors():
    fs=set()
    for x in (14,16):
        for y in (14,16):
            z=[x,y]
            for _ in range(R):z=sigma(z)
            fs.update(tuple(z[i:i+K]) for i in range(len(z)-K+1))
    return sorted(fs)

def bulk_machine():
    fs=factors();assert len(fs)==376
    idx={w:i for i,w in enumerate(fs)}
    children=[]
    for f in fs:
        z=sigma(f);left,right=tuple(z[62:187]),tuple(z[63:188])
        assert left in idx and right in idx
        children.append((idx[left],idx[right]))
    timeline=[]
    for f in fs:
        z=[H(*f[i:i+3]) for i in range(K-2)]
        out=[]
        for s in range(STOP-3+1):
            t=3+s
            if t<STOP:assert maxrun9(z)<=2,(t,f,'source 999')
            out.append(z[61-MARGIN*s])
            if t<STOP:z=local_step(z,GAMMA[t])
        assert len(out)==16 and len(z)==3
        timeline.append(tuple(out))
    uniq={x:i for i,x in enumerate(sorted(set(timeline)))}
    classes=[uniq[x] for x in timeline]
    assert len(uniq)==36
    # Moore refinement over *entire* 16-time output vectors remains 36.
    signatures=[(classes[i],classes[children[i][0]],classes[children[i][1]]) for i in range(len(fs))]
    sigclasses={x:i for i,x in enumerate(sorted(set(signatures)))}
    assert len(sigclasses)==36,'time-vector partition not substitution stable'
    allclasses=[]
    for k in range(36):
        members=[i for i,x in enumerate(classes) if x==k]
        value={(timeline[i],classes[children[i][0]],classes[children[i][1]]) for i in members}
        assert len(value)==1,(k,value)
        (out,left,right),=value
        allclasses.append({'id':k,'outputs_t3_to_t18':list(out),'child0':left,'child1':right,'members':len(members)})
    early={}
    for final in (15,16,17,18):
        distinct={x[:final-2] for x in timeline}
        early[str(final)]=len(distinct)
    assert early=={'15':32,'16':32,'17':32,'18':36},early
    return fs,children,classes,timeline,allclasses,early

def firstdiff(d):
    return next(((i,d[i],d[-1-i]) for i in range(len(d)//2) if d[i]!=d[-1-i]),None)

def boundaries():
    # With margin four over 15 steps, source dependency cone at most 4*15.
    # EDGE 64 + cone 60 + input 3 =127 < 128, so only last-letter parity
    # matters for the outer/centre windows once h>=10.
    assert EDGE+MARGIN*(STOP-3)+3<1<<R
    witness={}
    for h in range(2,12):
        p=initial(h); ww=[]
        for t in range(STOP):
            if t==3:assert p==predicted_third(h)
            if 3<=t<STOP:
                assert maxrun9(p)<=2,(h,t)
                assert p[0]!=9,(h,t,'root')
            q,d=reverse_add_pair(p)
            assert len(q)-len(p)==GAMMA[t],(h,t,'gamma')
            z=firstdiff(d)
            assert z is not None,(h,t,'palindrome')
            ww.append(z)
            if t>=3:
                m=len(p)//2
                if m>2*MARGIN:
                    calc=local_step(p[:m],GAMMA[t]); assert calc==q[MARGIN:m-MARGIN],(h,t,'bulk')
            p=q
        witness[h]=ww
    assert all(witness[h]==witness[10] for h in range(3,12))
    for h in (12,13):
        base=10+(h&1)
        p,q=initial(h),initial(base)
        for t in range(STOP+1):
            if t>=3:
                n=min(EDGE,len(q)//2-2)
                assert p[:n]==q[:n] and p[-n:]==q[-n:],(h,t,'end')
                mp,mq=len(p)//2,len(q)//2
                assert p[mp-n:mp+n]==q[mq-n:mq+n],(h,t,'centre')
            if t<STOP:p,_=reverse_add_pair(p);q,_=reverse_add_pair(q)
    return [list(x) for x in witness[10]],[list(x) for x in witness[2]]

def artifacts():
    F,S,cl,timelines,classes,early=bulk_machine()
    ww,ww2=boundaries()
    lines=['# id 125-letter TM-factor as 0/1 class child0 child1 outputs_t3..t18_csv']
    for i,f in enumerate(F):
        binary=''.join('0' if x==14 else '1' for x in f)
        labels=','.join(str(v) for v in timelines[i])
        lines.append(f'{i}\t{binary}\t{cl[i]}\t{S[i][0]}\t{S[i][1]}\t{labels}')
    doc={'label':'PAPER PROOF finite 18-step all-height dyadic spatial-timeslab','base':10,
         'time_range':[3,18],'initial_reverse_add_steps_all_heights':18,
         'hierarchy':'sigma(14)=14 16, sigma(16)=16 14','factor_length':K,
         'factor_count':len(F),'height_block':1<<R,'bounded_neutral_run':2,
         'gamma':list(GAMMA),'quotient_states':36,
         'Moore_refinement':'36 -> 36 fixed point',
         'quotient_time_prefix_counts':early,
         'boundary_parity_classes':[10,11],'small_height_exceptions':list(range(2,10)),
         'real_decimal_nonpal_witnesses_h>=3_t1..t18':ww,
         'real_decimal_nonpal_witnesses_h2_t1..t18':ww2,
         'quotient_transitions':classes,
         'spatial_identity':'at every time t3..t18, for w_h 125-factor centred c and i=c+2, P_t(h)[i]=class.outputs[t-3]. Under sigma, children correspond to P_t(h+1)[2i-2] and [2i-1].',
         'region':'h>=7, 64<=i<=2^h-61',
         'limits':'no temporal strip return; no infinite decimal Lychrel proof; time18 requires 36 rather than 32 classes'}
    return '\n'.join(lines)+'\n',json.dumps(doc,indent=2)+'\n'

def main():
    mode=sys.argv[1] if len(sys.argv)>1 else '--check'
    tsv,doc=artifacts();b=Path(__file__).resolve().parent
    files=((b/'spacetime36_states.tsv',tsv),(b/'spacetime36_quotient.json',doc))
    if mode=='--write':
        for p,s in files:p.write_text(s)
    elif mode=='--check':
        for p,s in files:assert p.read_text()==s,p
    else:raise ValueError('--write / --check')
    print('SPACETIME_36_STATE_ALL_HEIGHT_PASS', 'factor_states=376', 'quotient=36',
          'prefix=32,32,32,36', 'gamma',''.join(map(str,GAMMA)))
    print('EIGHTEEN_STEP_BOUND_RUN_ALL_HEIGHT_PASS')
if __name__=='__main__':main()
