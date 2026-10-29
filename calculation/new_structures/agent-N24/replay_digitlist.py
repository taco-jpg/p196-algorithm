#!/usr/bin/env python3
"""Second implementation: schoolbook digit-list arithmetic, no Python integer reverse/add.
Run: python3 replay_digitlist.py hybrid_data.json [steps]
"""
import sys, json, hashlib

def main(d,steps):
    B,W,g=d['B'],d['W'],d['overflow']
    lo=B[0]+W[0]*d['initial_lattice_copies']+[9]*d['initial_neutral_width']
    P=lo+[d['central_pair_coefficient']]+lo[::-1]
    n=len(P);digits=[0]*n
    for j in range(n//2):
        digits[j]=min(9,P[j]);digits[n-1-j]=P[j]-digits[j]
        assert 0<=digits[n-1-j]<10
    digits[n//2]=P[n//2]//2
    assert digits[-1]>0
    samples=[]; max_mismatch=0; seed_hash=''; final_hash=''
    for t in range(steps+1):
        n=len(digits)
        assert n>2*(len(B[0])+d['anchor_length'])
        mismatch=next((j for j in range(n//2) if digits[j]!=digits[-1-j]),n//2)
        assert mismatch<n//2,('palindrome',t)
        max_mismatch=max(max_mismatch,mismatch)
        for j in range(len(B[0])+d['anchor_length']):
            observed=digits[j]+digits[n-1-j]
            expected=B[t%d['period']][j] if j<len(B[0]) else W[t%d['period']][(j-len(B[0]))%d['lattice_period']]
            assert observed==expected,('shape',t,j,observed,expected)
        if t%1000==0 or t==steps:
            frontier=0
            for j in range(len(B[0]),n//2):
                if digits[j]+digits[n-1-j]!=W[t%d['period']][(j-len(B[0]))%d['lattice_period']]:break
                frontier+=1
            samples.append([t,n,frontier,mismatch])
            digest=hashlib.sha256(''.join(str(x) for x in digits[::-1]).encode()).hexdigest()
            if t==0:seed_hash=digest
            if t==steps:final_hash=digest
        if t<steps:
            carry=0;output=[]
            for j in range(n):
                z=digits[j]+digits[n-1-j]+carry
                output.append(z%10);carry=z//10
            if carry:output.append(carry)
            assert len(output)==n+g[t%d['period']],('overflow',t)
            digits=output
    return dict(method='schoolbook digit-list arithmetic',steps=steps,initial_digits=len(P),final_digits=len(digits),
                samples=samples,maximum_first_mirrored_digit_difference_index=max_mismatch,
                seed_sha256=seed_hash,final_sha256=final_hash,success=True)
if __name__=='__main__':
    with open(sys.argv[1] if len(sys.argv)>1 else 'hybrid_data.json') as f:d=json.load(f)
    steps=int(sys.argv[2]) if len(sys.argv)>2 else d['steps']
    print(json.dumps(main(d,steps),indent=2))
