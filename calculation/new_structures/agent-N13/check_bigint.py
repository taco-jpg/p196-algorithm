#!/usr/bin/env python3
"""Independent decimal bigint replay. Usage:
 python3 check_bigint.py seed.txt START END [stride=1000]
START=0 reads seed.txt; START>0 reads checkpoint_START.txt in seed directory.
This program uses Python's arbitrary-precision int and converts through decimal strings;
it never calls the separate digit-array evolution engine.
"""
import sys,time,os
sys.set_int_max_str_digits(0)
seed_path=sys.argv[1]; begin=int(sys.argv[2]);end=int(sys.argv[3]);stride=int(sys.argv[4]) if len(sys.argv)>4 else 1000
assert 0<=begin<=end
folder=os.path.dirname(seed_path)
file=seed_path if begin==0 else os.path.join(folder,f'checkpoint_{begin}.txt')
with open(file) as f: n=int(f.read().strip())
expected=((17,8,17,8,17,8,17,8),(5,13,6,14,8,16,13,12),
          (0,5,11,8,17,16,14,9),(1,1,2,4,8,16,14,10),
          (13,5,10,3,6,14,10,6),(4,8,16,8,17,14,10,2),
          (14,9,18,16,13,12,6,7),(12,8,16,16,14,9,0,6))
start=time.monotonic()
for t in range(begin,end+1):
    s=str(n)
    if s==s[::-1]: raise ValueError(f'palindrome t={t}')
    for j in range(8):
        q=int(s[j])+int(s[-1-j]);assert q==expected[j][t%8],(t,j,q)
    if t%stride==0 or t==end:
        print(f't={t} digits={len(s)} low24={s[-24:][::-1]} high24={s[:24]} elapsed={time.monotonic()-start:.2f}',flush=True)
    if t<end:n += int(s[::-1])
# Output full arbitrary precision integer to support exact restarting at end.
with open(os.path.join(folder,f'checkpoint_{end}.txt'),'w') as f:f.write(s+'\n')
print(f'INDEPENDENT_BIGINT_{begin}_{end}_PASS',flush=True)
