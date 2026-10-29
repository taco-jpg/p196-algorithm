#!/usr/bin/env python3
"""Quarter-base centre boundary: exact arithmetic controls, not a decimal certificate."""
import json
from math import gcd
from pathlib import Path

root=Path(__file__).resolve().parents[3]
def boundary(b):
    assert b>=2 and b%4==2
    return [(5*b-2)//4,(b-2)//2,(3*b-2)//2,(b-2)//4]

def charge(b,e=(0,1,0,1)):
    E=sum((1-2*v)*2**(len(e)-1-i) for i,v in enumerate(e))
    return E,gcd(2**len(e)-1,b-1),E%gcd(2**len(e)-1,b-1)==0

def main():
    for b in (50,146,1286):
        p=root/f"calculation/neutral_band/agent10_base{b}/cert_b{b}.json"
        data=json.loads(p.read_text())
        assert len(data['edges'])==4
        assert [r['e'] for r in data['edges']]==[0,1,0,1]
        assert [r['gamma'] for r in data['edges']]==[0,1,0,1]
        assert [r['v'] for r in data['edges']]==[0,0,1,0]
        actual=[r['C'][0] for r in data['edges']]
        assert actual==boundary(b),(b,actual)
        assert charge(b)[2]
        print(f"PASS base={b}: boundary={actual}; charge={charge(b)}")
    assert boundary(10)==[12,4,14,2]
    assert charge(10)==(5,3,False)
    print("base10 local boundary is integral, but mod-(b-1) exterior charge rules out e=0101")

if __name__=="__main__":main()
