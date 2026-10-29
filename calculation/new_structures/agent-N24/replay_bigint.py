#!/usr/bin/env python3
"""Independent exact decimal integer replay: no pair-word recurrence is used.
Run: python3 replay_bigint.py hybrid_data.json [steps]
A finite 20k-step computation, NOT an infinite Lychrel certificate.
"""
import sys, json, hashlib
sys.set_int_max_str_digits(0)

def start_number(data):
    left = data['B'][0] + data['W'][0]*data['initial_lattice_copies'] + [9]*data['initial_neutral_width']
    P = left+[data['central_pair_coefficient']]+left[::-1]
    d = [0]*len(P)
    for i in range(len(P)//2):
        d[i]=min(P[i],9)
        d[-1-i]=P[i]-d[i]
        assert 0<=d[-1-i]<=9
    d[len(P)//2]=P[len(P)//2]//2
    assert d[-1]>0 and P[len(P)//2]%2==0
    return int(''.join(str(x) for x in d[::-1]))

def main(data, steps):
    N=start_number(data); original=len(str(N)); length=original
    B,W,g=data['B'],data['W'],data['overflow']
    p=data['period']; q=data['lattice_period']; k=data['anchor_length']
    samples=[]; max_difference=0; first_digest=''; last_digest=''
    for t in range(steps+1):
        s=str(N); n=len(s)
        assert n==length, ('overflow',t,n,length)
        assert s != s[::-1], ('palindrome',t)
        mismatch=next((j for j in range(n//2) if s[j]!=s[-1-j]), n//2)
        max_difference=max(max_difference,mismatch)
        assert mismatch<n//2
        for j in range(len(B[0])+k):
            observed=(ord(s[-1-j])-48)+(ord(s[j])-48)
            expected=B[t%p][j] if j<len(B[0]) else W[t%p][(j-len(B[0]))%q]
            assert observed==expected, ('shape',t,j,observed,expected)
        if t%1000==0 or t==steps:
            frontier=0
            for j in range(len(B[0]),n//2):
                if (ord(s[-1-j])-48)+(ord(s[j])-48)!=W[t%p][(j-len(B[0]))%q]: break
                frontier+=1
            samples.append([t,n,frontier,mismatch])
            digest=hashlib.sha256(s.encode('ascii')).hexdigest()
            if t==0:first_digest=digest
            if t==steps:last_digest=digest
        if t<steps:
            N+=int(s[::-1])
            length+=g[t%p]
    return dict(method='ordinary Python big integers',steps=steps,initial_digits=original,final_digits=length,
                samples=samples,maximum_first_mirrored_digit_difference_index=max_difference,
                seed_sha256=first_digest,final_sha256=last_digest,success=True)
if __name__=='__main__':
    with open(sys.argv[1] if len(sys.argv)>1 else 'hybrid_data.json') as f:d=json.load(f)
    steps=int(sys.argv[2]) if len(sys.argv)>2 else d['steps']
    print(json.dumps(main(d,steps),indent=2))
