#!/usr/bin/env python3
"""Two-column decimal carry-port transducer and physical p8 hybrid witness.

All pairwords are least significant digit first. Reproduces a conditional
anti-palindromic latch for a periodic 0011 inward-carry source.

Run: python3 carry_latch.py p8_hybrid_data.json 20000
"""
import sys,json,random,hashlib

def prefix_next(p0,p1,source):
    assert 1<=p0<=18 and 0<=p1<=18 and source in (0,1)
    lo0=p0%10; c1=p0//10
    lo1=(p1+c1)%10
    upper1=(p1+source)%10
    uppercarry=(p1+source)//10
    upper0=(p0+uppercarry)%10
    overflow=(p0+uppercarry)//10
    if overflow:
        return (lo0+1,lo1+upper0,1)
    return (lo0+upper0,lo1+upper1,0)

def step_digit_list(d):
    carry=0;out=[];n=len(d)
    for i in range(n):
        z=d[i]+d[n-1-i]+carry
        out.append(z%10);carry=z//10
    if carry:out.append(carry)
    return out

def make_digits(P):
    assert P==P[::-1]
    d=[0]*len(P)
    for i in range(len(P)//2):
        p=P[i]
        lo=min(9,p-1) if i==0 else min(9,p)
        d[i]=lo;d[-1-i]=p-lo
        assert 0<=d[-1-i]<10
    if len(P)%2:
        d[len(P)//2]=P[len(P)//2]//2
    assert d[-1]>0
    return d

def carry_port_from_digits(d):
    n=len(d); assert n>=6
    c=0
    for i in range(n-2):
        c=(d[i]+d[-1-i]+c)//10
    return c

def test_random_transducer(trials=30000):
    rng=random.Random(240),
    rng=rng[0]
    checked=0
    for _ in range(trials):
        p0=rng.randrange(1,19)
        p1=rng.randrange(0,19)
        source=rng.randrange(2)
        mid=rng.randrange(0,19)
        # P2 is a forced carry-boundary guard (0 or18).
        half=[p0,p1,18 if source else 0,mid,mid]
        P=half+half[::-1]
        d=make_digits(P)
        actual=carry_port_from_digits(d)
        assert actual==source
        d2=step_digit_list(d)
        P2=[d2[i]+d2[-1-i] for i in range(len(d2))]
        q=prefix_next(p0,p1,source)
        assert q==(P2[0],P2[1],len(d2)-len(d)),(p0,p1,source,q,P2[:2])
        checked+=1
    return checked

X=(5,6,8,13)
Y=(13,14,16,12)
CLOCK=(0,0,1,1)

def clock_theorem_check():
    for i,x in enumerate(X):
        # Even->odd only inner bit is irrelevant for x in X.
        for inner in (0,1):
            assert prefix_next(17,x,inner)==(8,Y[i],1)
        # Odd->even is selected by a physical carry port.
        assert prefix_next(8,Y[i],CLOCK[i])==(17,X[(i+1)%4],0)
    # The least and most significant digits of EVERY odd-phase number
    # are respectively 7,1, when reached from p0=17 even-phase.
    return {'even_p1':X,'odd_p1':Y,'odd_carry_clock':CLOCK,
            'odd_edge_digits_low_high':[7,1], 'even_pair_sum':17}

def actual_hybrid_trace(data,steps):
    assert data['period']==8
    low=data['B'][0]+data['W'][0]*data['initial_lattice_copies']+[9]*data['initial_neutral_width']
    P=low+[data['central_pair_coefficient']]+low[::-1]
    d=make_digits(P)
    witness=clock_theorem_check(); switches=[];samples=[]
    for t in range(steps+1):
        p0=d[0]+d[-1];p1=d[1]+d[-2]
        if t%2==0:
            assert p0==17 and p1==X[(t//2)%4],('even latch',t,p0,p1)
        else:
            assert p0==8 and p1==Y[((t-1)//2)%4],('odd latch',t,p0,p1)
            c=carry_port_from_digits(d)
            assert c==CLOCK[((t-1)//2)%4],('carry clock',t,c)
            switches.append(c)
        assert d!=d[::-1],('palindrome',t)
        if t%1000==0 or t==steps:
            samples.append([t,len(d),p0,p1, switches[-8:] if switches else []])
        if t<steps:
            d=step_digit_list(d)
    assert switches[:16]==list(CLOCK)*4
    witness.update({'checked_steps':steps,'observed_odd_carry_ports':len(switches),
        'sample_states':samples,'last_odd_carry_ports':switches[-16:],
        'end_sha256':hashlib.sha256(''.join(map(str,d[::-1])).encode('ascii')).hexdigest()})
    return witness

if __name__=='__main__':
    data=json.load(open(sys.argv[1] if len(sys.argv)>1 else 'p8_hybrid_data.json'))
    steps=int(sys.argv[2]) if len(sys.argv)>2 else 20000
    n=test_random_transducer()
    w=actual_hybrid_trace(data,steps)
    print(json.dumps({'random_digit_control_trials':n,'carry_latch':w},indent=2))