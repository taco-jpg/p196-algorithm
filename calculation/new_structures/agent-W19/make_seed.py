#!/usr/bin/env python3
"""Independent literal decimal construction of non-gauge period-eight eraser seeds."""
import argparse
from pathlib import Path
B=(17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13)
W=(17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13)
C=((14,9,9,0),(0,14,9,0))
def seed(packets=12,copies=300,gap=1,mask=0):
    assert packets>=1 and gap>=1
    half=list(B)+list(W)*copies
    for j in range(packets):
        half.extend(C[(mask>>j)&1])
        if j+1<packets:half.extend(list(W)*gap)
    low=[min(x,9) for x in half]
    high=[x-y for x,y in zip(half,low)]
    digits=low+high[::-1]
    assert digits[-1]>0 and all(0<=d<=9 for d in digits)
    return ''.join(str(d) for d in digits[::-1])
if __name__=='__main__':
    a=argparse.ArgumentParser()
    a.add_argument('--packets',type=int,default=12)
    a.add_argument('--copies',type=int,default=300)
    a.add_argument('--gap',type=int,default=1)
    a.add_argument('--out',type=Path,default=Path('/tmp/w19_seed'))
    args=a.parse_args()
    for name,mask in [('zero',0),('ones',(1<<args.packets)-1)]:
        s=seed(args.packets,args.copies,args.gap,mask)
        dest=Path(str(args.out)+'_'+name+'.txt')
        dest.write_text(s+'\n')
        print(name,len(s),dest)
