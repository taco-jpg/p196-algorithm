#!/usr/bin/env python3
"""N15 period-doubling, paired-word morphic finite-level calculations (no Lychrel proof)."""
import json


def twinkle(h, A=14, B=16):
    w=[A]
    for k in range(h):
        w=[v for x in w for v in ((A,B) if x==A else (B,A))]
    return w


def pairword(h,A=14,B=16,edge=4):
    H=[edge]+twinkle(h,A,B)
    return H+H[::-1]


def predicted_first_half(h,A=14,B=16,edge=4):
    w=twinkle(h,A,B)
    # h >= 1; a positive-conducting interior (p_i>=10)
    return [2*edge+1,2*w[0]-19]+[2*(v-9) for v in w[1:]]


def predicted_second_half(h):
    """For h>=2, after two RAA steps the pairword has odd length 2*m+1."""
    assert h>=2
    q=predicted_first_half(h)
    m=len(q)
    return [10,9,q[2]-10]+[q[i]+q[i-1]-18 for i in range(3,m)]+[2*(q[m-1]-9)]


def normalize_pair(P,b=10):
    c=0;d=[]
    for x in P:
        z=x+c;d.append(z%b);c=z//b
    if c:d.append(c)
    return d


def next_pair(P,b=10):
    d=normalize_pair(P,b)
    return [d[i]+d[len(d)-1-i] for i in range(len(d))],d


def state_table(h,steps):
    P=pairword(h)
    out=[]
    for t in range(steps+1):
        if t in (0,1,2,3,4,8,16,32,64,128):
            H=P[:len(P)//2]
            out.append({'step':t,'pairword_length':len(P),'low_prefix':P[:12],
                        'distinct_coefficients':len(set(H)),
                        'distinct_length8_factors':len({tuple(H[i:i+8]) for i in range(len(H)-7)})})
        P,D=next_pair(P)
    return out


def run():
    proof=[]
    for h in range(1,15):
        P=pairword(h)
        Q,D=next_pair(P)
        expected=predicted_first_half(h)
        assert len(Q)==len(P)
        assert Q==expected+expected[::-1],h
        assert D!=D[::-1]
        assert Q[0]==9 and Q[1]==9
        if h>=2:
            RR,D2=next_pair(Q)
            r=predicted_second_half(h)
            assert len(RR)==len(P)+1 and RR==r+r[-2::-1]
            assert D2[0]==9 and D2[-1]==1 and D2!=D2[::-1]
        proof.append([h,len(P),len(set(expected))])
    print('DYADIC_EDGE_PASS levels 1..14; first/second-step base10 substitution identities valid')
    out={'label':'COMPUTED','levels_checked':proof,'h9_temporal':state_table(9,128),'h11_temporal':state_table(11,128)}
    with open('dyadic_data.json','w') as f:json.dump(out,f,indent=2)
    print('TEMPORAL_DATA_PASS h9/h11 steps 0..128; comparison data written')

if __name__=='__main__':run()
