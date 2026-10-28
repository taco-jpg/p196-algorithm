"""Test the mod-(b-1) charge law: s(B)=sum B_i;  s(B') == 2 s(B) + 1 - 2 e1  (mod b-1)  for every autonomous B step (random words with Hyp-compatible e2=1-e1, trimmed or not).
Also check on exterior cycles (p11,p12 base 10; base 11, 20; stream 10 cycles)."""
import sys, random, re
sys.path.insert(0,'..'); sys.path.insert(0,'.')
import lib, mirror as m
from parse_bw import parse_bw
random.seed(1)
bad=0; tot=0
for b in [3,4,5,7,10,11,16,20]:
    for _ in range(20000):
        n=random.randint(1,9)
        B=[random.randint(0,2*b-2) for _ in range(n)]
        if B[-1]==b-1: continue
        nb,e1,gm,u=lib.Bstep(b,B)
        tot+=1
        if (sum(nb)-(2*sum(B)+1-2*e1))%(b-1)!=0: bad+=1
print("random single steps: total",tot,"violations",bad)
# exterior cycles from bauto witness lines
files=sys.argv[1:]
for f in files:
    for line in open(f):
        if 'ACCEPT' not in line or 'B_t=' not in line: continue
        b,p,g,e,Bs=parse_bw(line)
        ok=True
        for t in range(p):
            nb,e1,gm,u=lib.Bstep(b,Bs[t])
            if (sum(Bs[(t+1)%p])-(2*sum(Bs[t])+1-2*e1))%(b-1)!=0: ok=False
        # closure criterion
        E=int(e,2); P=p
        print(f"b={b} p={p} g={g} e={e} law_ok={ok} gcd(2^P-1,b-1)={__import__('math').gcd(2**P-1,b-1)}  E mod (b-1)={E%(b-1)}  s0 mod(b-1)={sum(Bs[0])%(b-1)}")
