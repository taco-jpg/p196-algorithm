#!/usr/bin/env python3
"""Check integer-valued birth snapshots produced by the independent limb engine."""
import hashlib
import sys
from pathlib import Path
spec=[
 (3,51469,[-1,0],'c1cca9ba5258c034ccd5f84708f041e4e85a66d111ec4b1ada2c97972fcc3d6b','04935edf702bb204a81414b97fb438bac15f75690836bb7b623456f6a74cff0b'),
 (12,51483,[0,1,2],'50abc742299d4f4586ef77603b5c905619ba1eb1429570f527407d25eb99993a','207f3aeea881a5a208d9a972b870745a3c709a6ddc1939c5a7960b50da0ba19d')
]
assert len(sys.argv)==5
for i,(k,t,want,h1,h2) in enumerate(spec):
 pa,pb=[Path(s) for s in sys.argv[1+2*i:3+2*i]]
 assert hashlib.sha256(pa.read_bytes()).hexdigest()==h1
 assert hashlib.sha256(pb.read_bytes()).hexdigest()==h2
 a=pa.read_text().strip()[::-1];b=pb.read_text().strip()[::-1]
 assert len(b)==len(a)+1
 s=(len(a)+1)//2
 padded=a[:s]+'0'+a[s:]
 observed=[j-s for j in range(len(b)) if b[j]!=padded[j]]
 assert observed==want,(k,t,observed,want)
 assert all(int(a[j])+int(a[-j-1])==int(b[j])+int(b[-j-1]) for j in range(16))
 assert a!=a[::-1] and b!=b[::-1]
 print(f'INDEPENDENT_INTEGER_BIRTH_PASS pair_k={k} t={t} changed={observed}')
print('BIRTH_INTEGER_CONTROLS_PASS')
