#!/usr/bin/env python3
"""Independent Python-bigint carries at four cut coordinates on two decimal orbits."""
from collections import deque
import csv
import sys
sys.set_int_max_str_digits(1000000)
PATH=(17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13)
CYC=(17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13)

def start(half,patch):
    d=[0]*(2*half)
    for j in range(half):
        p=PATH[j] if j<39 else CYC[(j-39)%20]
        if patch and j>=half-patch:p=(7*j+11)%19
        d[j]=min(p,9)
        d[2*half-1-j]=p-d[j]
    return int(''.join(map(str,reversed(d))))

def front(a,b):
    for i in range(min(len(a),len(b))//2):
        if a[-i-1]+a[i]!=b[-i-1]+b[i]:return i
    raise AssertionError('No pairword difference')

def carries_at(s,places):
    positions=sorted(set(places))
    n=len(s);carry=0;ans={}
    for i in range(positions[-1]+1):
        if i in positions:ans[i]=carry
        if i<positions[-1]:carry=(s[-1-i]+s[i]-96+carry>=10)
    return [int(ans[p]) for p in places]

def main():
    a,b=start(5200,0),start(5200,100)
    old=deque(maxlen=88);rows=[];checked=0
    for t in range(2001):
        sa,sb=str(a).encode(),str(b).encode()
        if t>=912:
            f=front(sa,sb)
            n=len(sa)
            positions=[f-100,n-1-(f+74),f+75,n-(f-100)]
            ca=carries_at(sa,positions)
            cb=carries_at(sb,positions)
            row=(ca[0],cb[0],ca[1],cb[1],ca[2],cb[2],ca[3],cb[3])
            if t>=1000:
                assert row==old[0],(t,row,old[0])
                checked+=8
                if t<1088:rows.append((t-1000,)+row)
            old.append(row)
        if t<2000:
            a+=int(sa[::-1]);b+=int(sb[::-1])
    assert checked==8008,checked
    assert len(rows)==88
    headers=['phase','lowA','lowB','highA','highB','lowEndA','lowEndB','highEndA','highEndB']
    with open(sys.argv[1], 'w', newline='') as fh:
        w=csv.writer(fh,lineterminator='\n');w.writerow(headers);w.writerows(rows)
    assert sum(x[3]!=x[4] for x in rows)==49
    print('INDEPENDENT_BIGINT_CARRY_TILE_PASS steps=0..2000 windows=1000..2000 compared_carry_bits=8008 contrast_phases=49')
if __name__=='__main__':main()
