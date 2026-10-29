#!/usr/bin/env python3
"""8-bit defect-mask charge truth table at the 107-step neutral gate."""
import sys,csv
sys.set_int_max_str_digits(0)
M='88283583'
def init(n,mask):
    s=''.join(M[min(i,n-1-i)%8] for i in range(n))
    x=int(s)
    for k in range(1,9):
        if mask>>(k-1)&1:x+=10**(n//2-k)
    return x
def st(a):
    s=str(a)
    return a+int(s[::-1])
def cout(a,j):
    s=str(a); L=len(s); c=0
    for i in range(j):
        c=(int(s[L-1-i])+int(s[i])+c)//10
    return c
def high(a,b):
    s,t=str(a),str(b)
    if len(s)!=len(t):return -1
    return next((i for i,(x,y) in enumerate(zip(s,t)) if x!=y),len(s))
def table(n,steps=107):
    p=init(n,0)
    baseline=p
    for _ in range(steps):baseline=st(baseline)
    j=len(str(baseline))-61
    cb=cout(baseline,j)
    rows=[]
    for mask in range(256):
        b=init(n,mask)
        for _ in range(steps):b=st(b)
        carry=cout(b,j)
        h=high(st(baseline),st(b))
        rows.append((mask,format(mask,'08b'),carry^cb,h))
    return j,rows
if __name__=='__main__':
    n=int(sys.argv[1]) if len(sys.argv)>1 else 2001
    j,rows=table(n)
    safe=[r for r in rows if not r[2]]
    gated=[r for r in rows if r[2]]
    print(n,'j',j,'safe',len(safe),'gated',len(gated),'safe high minimum',min(r[3] for r in safe),'gated high maximum',max(r[3] for r in gated))
    with open(sys.argv[2] if len(sys.argv)>2 else 'charge_logic.csv','w',newline='') as f:
        w=csv.writer(f);w.writerow(['mask','bits','differential_carry','matched_high_t108']);w.writerows(rows)
    vals=[r[2] for r in rows]
    anf=vals[:]
    for k in range(8):
        for mask in range(256):
            if mask&(1<<k):anf[mask]^=anf[mask^(1<<k)]
    terms=[i for i,a in enumerate(anf) if a]
    print('ANF terms',len(terms),'degree',max(i.bit_count() for i in terms),'first',terms[:50]); print('single-bit',[(i+1,vals[1<<i]) for i in range(8)]); print('adjacent',[(i+1,i+2,vals[(1<<i)|(1<<(i+1))]) for i in range(7)])
