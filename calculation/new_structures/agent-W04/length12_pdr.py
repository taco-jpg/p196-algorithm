#!/usr/bin/env python3
"""Agent W04: exact 12-step positive-resource transfer into the second decimal band.
Every universal edge follows by pumping two disjoint state-self-loop columns.
No oracle/future iterate is used in the finite-state soundness check.
"""
import random
import json
from pathlib import Path

PHASES = [((11, 9, 8, 17), 8, 0, (9, 16, 7, 8, 8), 16, 0, (8,)), ((2, 1, 18), 16, 1, (18, 6, 14, 15, 16, 15), 14, -1, (15, 16)), ((4, 3, 17), 14, 1, (17, 14, 9, 12, 14, 12), 10, -1, (12, 14)), ((8, 7, 15), 10, 1, (16, 10, 0, 6, 10, 6), 2, -1, (6, 10)), ((16, 15, 11), 2, 1, (14, 1, 1, 13, 0, 13), 4, -1, (13, 0)), ((7, 13, 8), 4, 1, (7, 6, 2, 5, 4, 4), 8, 0, (4,)), ((15, 6, 17), 8, 1, (14, 12, 4, 10, 8, 8), 16, 0, (8,)), ((6, 12, 14), 16, 1, (13, 8, 7, 5, 9, 16, 15), 14, -1, (15, 16)), ((13, 5, 10), 14, 1, (7, 17, 14, 11, 9, 13, 12), 10, -1, (12, 14)), ((4, 9, 6, 6), 10, 0, (12, 15, 13, 7, 2, 4, 7, 4), 2, -2, (4, 8)), ((8, 18, 12, 13, 1), 2, -1, (6, 12, 7, 15, 4, 8, 14, 8), 4, -2, (8, 16)), ((17, 17, 6, 7, 3), 4, -1, (13, 4, 16, 10, 9, 17, 8, 17), 8, -2, (17, 13)), ((8, 16, 14, 13, 10, 7), 8, 0, (11, 8, 1, 8), 16, 1, (12, 8))]
ODD=(0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1)
GAMMA=(1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1)

def half(t,m,n):
    L,x,a,J,y,b,R=PHASES[t]
    assert m>=0 and n>=0
    return tuple(L)+(x,)*(m+a)+tuple(J)+(y,)*(n+b)+tuple(R)

def complete(H,odd):
    return H+ (H[-2::-1] if odd else H[::-1])

def loops(t,m,n):
    A=PHASES[t]; B=PHASES[t+1]
    dm=0; dn=0
    h=half(t,m,n); k=half(t+1,m,n)
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
    stop1=min(len(A[0])+m+A[2],len(B[0])+m+B[2])
    base2=max(len(A[0])+m+A[2]+len(A[3]),len(B[0])+m+B[2]+len(B[3]))
    stop2=min(len(A[0])+m+A[2]+len(A[3])+n+A[5],len(B[0])+m+B[2]+len(B[3])+n+B[5])
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
    for t in range(len(PHASES)):
        raw=str(N); assert raw[0]!='0'
        pair=tuple(int(raw[-1-i])+int(raw[i]) for i in range(len(raw)))
        assert pair==complete(half(t,m,n),ODD[t]),(m,n,t)
        assert raw!=raw[::-1]
        if t<len(PHASES)-1:N=N+int(raw[::-1])
    return len(str(N))

def check():
    base=10; cert=[]
    for t in range(len(PHASES)-1):
        g,dm,dn,c=loops(t,base,base)
        cert.append((t,g,dm,dn,c))
        print('EDGE',t,'gamma',g,'deltas',dm,dn,'self-loops',c)
        # Inserting the first, the second or both loop letters is independently checked.
        for mm,nn in ((10,10),(11,10),(10,11),(11,11),(17,19),(19,17),(50,50)):
            x=loops(t,mm,nn)
            assert x[:3]==(g,dm,dn)
    # Initial independent counters m>=8,n>=5 ensure all six edge source runs >=3.
    rng=random.Random(47404)
    cases=[(10,10),(10,13),(13,10),(25,100),(100,25),(500,500)]+[(rng.randint(10,90),rng.randint(10,90)) for _ in range(90)]
    for m,n in cases:
        for t in range(len(PHASES)-1):
            loops(t,m,n)
        integer_oracle(m,n)
    # Early synchronized N19 k=5,6,7 are separate controls, not used to infer an all-k claim.
    for k in (10,11,12):integer_oracle(k,k)
    print('ALL_PUMP_PROOFS_PASS: twelve universally valid independent-counter RESOURCE TRANSFER edges for runs >=3')
    print('IND_INT_REPLAY_PASS:',len(cases)+3,'positive seeds, all thirteen phases, no palindrome')
    print('THEOREM: initial m>=10,n>=10, twelve transitions; after six lengths (m+1,n), after twelve (m,n+1)')
    return cert

def assert_data(raw):
    assert raw['base']==10 and raw['base_run_length']==10
    assert raw['phase_parities']==list(ODD)
    assert raw['phase_overflows']==list(GAMMA)
    for i,row in enumerate(raw['phases']):
        L,x,a,J,y,b,R=PHASES[i]
        assert row==dict(prefix=list(L),left_symbol=x,left_offset=a,junction=list(J),
                         right_symbol=y,right_offset=b,suffix=list(R))
    assert len(raw['edges'])==12
    for edge,record in enumerate(raw['edges']):
        g,dm,dn,cs=loops(edge,10,10)
        desired=dict(edge=edge,gamma=g,first_counter_delta=dm,second_counter_delta=dn,
                     pumps=[dict(cut=p[0],state=list(p[1]),column=list(p[2])) for p in cs])
        assert record==desired,('CERTIFICATE_MUTATION',edge)

def certificate_controls():
    raw=json.loads((Path(__file__).parent/'length12_witness.json').read_text())
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
