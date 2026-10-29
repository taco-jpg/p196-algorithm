#!/usr/bin/env python3
"""Agent W04: finite two-port loop witness for TWO INDEPENDENT decimal counters.
Every universal edge follows by pumping two disjoint state-self-loop columns.
No oracle/future iterate is used in the finite-state soundness check.
"""
import random
import json
from pathlib import Path

PHASES = [
    ((10,),8,0,(5,11),16,0,(8,)),
    ((1,9),16,1,(13,7,9),14,1,(15,16)),
    ((3,9,13),14,2,(7,16,9,9),10,2,(12,14)),
    ((7,9,7),10,3,(9,16,13,0,0),2,2,(6,10)),
    ((14,18,15,1),2,4,(0,14,7,1,0),4,2,(13,0)),
    ((5,14,15,7,3),4,5,(2,5,12,8,1,4),8,2,(4,)),
    ((11,9,11,15,6),8,5,(4,11,4,17,2,8),16,2,(8,))
]
ODD=(0,1,1,1,1,0,0)
GAMMA=(1,0,0,0,1,0)

def half(t,m,n):
    L,x,_,J,y,_,R=PHASES[t]
    assert m>=0 and n>=0
    return tuple(L)+(x,)*m+tuple(J)+(y,)*n+tuple(R)

def complete(H,odd):
    return H+ (H[-2::-1] if odd else H[::-1])

def loops(t,m,n):
    A=PHASES[t]; B=PHASES[t+1]
    dm=A[2]-B[2]; dn=A[5]-B[5]
    h=half(t,m,n); k=half(t+1,m+dm,n+dn)
    src=complete(h,ODD[t]);N=len(src)
    # Construct unique low-to-high carry vector by integer digit normalization.
    # The proof kernel below independently checks EVERY local transducer equation.
    carry=[0]; digits=[]
    for p in src:
        s=p+carry[-1]; digits.append(s%10);carry.append(s//10)
    gamma=carry[-1];assert gamma==GAMMA[t]
    if gamma:digits.append(gamma)
    expected=complete(k,ODD[t+1])
    actual=tuple(digits[i]+digits[-i-1] for i in range(len(digits)))
    assert actual==expected, ('edge',t,m,n)
    # Non-deterministic 2-ended carry transducer: verify a concrete accepting path.
    state=(0,gamma,-1);states=[state];outs=[]
    outer=len(h)-ODD[t]
    for i in range(outer):
        p=h[i]
        r=carry[N-1-i]
        a,z,prev=state
        low=p+a;hi=p+r
        assert hi//10==z
        new=(low//10,r,hi%10)
        emit=low%10+(hi%10 if gamma==0 else (1 if i==0 else prev))
        assert emit==k[i], (t,i,p,emit,k[i])
        outs.append(emit);state=new;states.append(state)
    a,z,prev=state
    if ODD[t]:
        mid=h[-1]; assert (mid+a)//10==z
        md=(mid+a)%10
        outs.append(2*md if gamma==0 else md+prev)
    else:
        assert a==z
        if gamma:outs.append(2*prev)
    assert tuple(outs)==k
    assert bool(ODD[t+1])==bool((N+gamma)%2)
    # Identify a self-loop in each of two disjoint aligned input/output bulk runs.
    base1=max(len(A[0]),len(B[0]))
    stop1=min(len(A[0])+m,len(B[0])+m+dm)
    base2=max(len(A[0])+m+len(A[3]),len(B[0])+m+dm+len(B[3]))
    stop2=min(len(A[0])+m+len(A[3])+n,len(B[0])+m+dm+len(B[3])+n+dn)
    cuts=[]
    for j,(start,stop,source,target) in enumerate(((base1,stop1,A[1],B[1]),(base2,stop2,A[4],B[4]))):
        candidates=[i for i in range(start,stop) if states[i]==states[i+1] and h[i]==source and k[i]==target]
        assert candidates, ('NO_PUMP',t,j,m,n,start,stop)
        cut=candidates[0];cuts.append((cut,states[cut],(source,target)))
    assert cuts[0][0]<cuts[1][0]
    return gamma, dm, dn, cuts

def digits_from_pair(H):
    p=complete(H,False);n=len(p)
    d=[0]*n
    for i in range(n//2):
        x=p[i];d[n-1-i]=min(9,x);d[i]=x-d[n-1-i]
    assert d[-1]!=0
    return d

def integer_oracle(m,n):
    # Separate ordinary Python arbitrary-precision integer implementation.
    d=digits_from_pair(half(0,m,n))
    N=int(''.join(str(v) for v in d[::-1]))
    for t in range(7):
        raw=str(N); assert raw[0]!='0'
        pair=tuple(int(raw[-1-i])+int(raw[i]) for i in range(len(raw)))
        assert pair==complete(half(t,m-PHASES[t][2],n-PHASES[t][5]),ODD[t]),(m,n,t)
        assert raw!=raw[::-1]
        if t<6:N=N+int(raw[::-1])
    return len(str(N))

def check():
    base=3; cert=[]
    for t in range(6):
        g,dm,dn,c=loops(t,base,base)
        cert.append((t,g,dm,dn,c))
        print('EDGE',t,'gamma',g,'deltas',dm,dn,'self-loops',c)
        # Inserting the first, the second or both loop letters is independently checked.
        for mm,nn in ((3,3),(4,3),(3,4),(4,4),(7,19),(19,7),(50,50)):
            x=loops(t,mm,nn)
            assert x[:3]==(g,dm,dn)
    # Initial independent counters m>=8,n>=5 ensure all six edge source runs >=3.
    rng=random.Random(47404)
    cases=[(8,5),(8,13),(13,5),(25,100),(100,25),(500,500)]+[(rng.randint(8,90),rng.randint(5,90)) for _ in range(90)]
    for m,n in cases:
        for t in range(6):
            loops(t,m-PHASES[t][2],n-PHASES[t][5])
        integer_oracle(m,n)
    # Early synchronized N19 k=5,6,7 are separate controls, not used to infer an all-k claim.
    for k in (5,6,7):integer_oracle(k,k)
    print('ALL_PUMP_PROOFS_PASS: six universally valid two-INDEPENDENT-counter edges for runs >=3')
    print('IND_INT_REPLAY_PASS:',len(cases)+3,'positive seeds, all seven phases, no palindrome')
    print('THEOREM: initial m>=8,n>=5, six transitions; lengths (m,n) -> (m-5,n-2)')
    return cert

def assert_data(raw):
    assert raw['base']==10 and raw['base_run_length']==3
    assert raw['phase_parities']==list(ODD)
    assert raw['phase_overflows']==list(GAMMA)
    for i,row in enumerate(raw['phases']):
        L,x,a,J,y,b,R=PHASES[i]
        assert row==dict(prefix=list(L),left_symbol=x,left_offset=a,junction=list(J),
                         right_symbol=y,right_offset=b,suffix=list(R))
    assert len(raw['edges'])==6
    for edge,record in enumerate(raw['edges']):
        g,dm,dn,cs=loops(edge,3,3)
        desired=dict(edge=edge,gamma=g,first_counter_delta=dm,second_counter_delta=dn,
                     pumps=[dict(cut=p[0],state=list(p[1]),column=list(p[2])) for p in cs])
        assert record==desired,('CERTIFICATE_MUTATION',edge)

def certificate_controls():
    raw=json.loads((Path(__file__).parent/'witness.json').read_text())
    assert_data(raw)
    bad=json.loads(json.dumps(raw))
    bad['edges'][0]['pumps'][0]['state'][0]^=1
    try: assert_data(bad)
    except AssertionError:pass
    else:raise AssertionError('mutation not rejected')
    print('FINITE_CERTIFICATE_AND_MUTATION_REJECTION_PASS')

if __name__=='__main__':
    certificate_controls()
    check()