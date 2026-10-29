#!/usr/bin/env python3
"""Independent integer reverse/add: all pairword-boundary rows for first 800 steps."""
import csv,sys
sys.set_int_max_str_digits(1000000)
PATH=(17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13)
CYC=(17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13)

def start(H,left=0,width=0):
    ds=[0]*(2*H)
    for j in range(H):
        p=PATH[j] if j<39 else CYC[(j-39)%20]
        if width and left<=j<left+width:p=(7*j+11)%19
        ds[j]=min(p,9)
        ds[2*H-1-j]=p-ds[j]
    return int(''.join(str(x) for x in reversed(ds)))

def diff(a,b):
    aa,bb=a.encode(),b.encode();L=min(len(aa),len(bb))//2
    first=-1;last=-1;count=0
    for j in range(L):
        if aa[j]+aa[-1-j] != bb[j]+bb[-1-j]:
            if first<0:first=j
            last=j;count+=1
    return first,last,count

def main():
    data=list(csv.DictReader(open(sys.argv[1]),delimiter='\t'))
    a,b,c=start(5200),start(5200,2000,100),start(12000)
    for t in range(801):
        sa,sb,sc=str(a),str(b),str(c)
        low,high,num=diff(sa,sb)
        central=diff(sa,sc)[0]
        r=data[t]
        got=(t,low,high,num,central,len(sa))
        expect=tuple(int(r[k]) for k in ('time','min','max','count','center_front','length'))
        assert got==expect,(t,got,expect)
        if t<800:
            a+=int(sa[::-1]);b+=int(sb[::-1]);c+=int(sc[::-1])
    print('INDEPENDENT_BIGINT_PULSE_PASS steps=0..800 all_801_rows 3_native_integer_orbits')

if __name__=='__main__':main()
