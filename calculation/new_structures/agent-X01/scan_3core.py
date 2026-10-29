#!/usr/bin/env python3
"""Exhaustive 19^3 3-cell junction scan, only the specified k=50 clock."""
from relay3 import step
def macro(p,k):
    fold=p[:len(p)//2];xs=[];i=0
    while i<len(fold):
        j=i+1
        while j<len(fold) and fold[j]==fold[i]:j+=1
        if j-i>=k//2 and fold[i] in (14,4):xs.append((fold[i],i,j-i))
        i=j
    return xs
def run(k=50):
    valid=0;wins=[]
    for a in range(19):
        for b in range(19):
            for c in range(19):
                h=[9]+[14]*k+[a,b,c]+[4]*k+[13]
                p=h+h[::-1];original=macro(p,k);odd=True
                for t in range(6):
                    odd=odd and any(v%2 for v in p)
                    p=step(p)
                odd=odd and any(v%2 for v in p)
                xs=macro(p,k)
                if len(xs)!=2 or xs[0][0]!=14 or xs[1][0]!=4 or not odd:continue
                valid+=1
                if xs[0][2]>=original[0][2] and xs[1][2]>=original[1][2]:
                    wins.append((a,b,c,xs[0][2]-original[0][2],xs[1][2]-original[1][2]))
    print('valid',valid,'nonnegative both',wins)
    assert valid==6744
    assert wins==[(5,5,5,0,0),(5,5,14,0,0),(5,14,5,0,0),(5,14,14,0,0)]
if __name__=='__main__':run()
