#!/usr/bin/env python3
"""Independent Python BIGINT oracle for decimal N27 seeds (first T steps)."""
import sys
sys.set_int_max_str_digits(0)
def make_seed(m=3000,gap=12000,repair=0):
    B=[2,14,14] if repair else [12,9]
    C=[6]+[9]*m+[6]
    P=B+[9]*gap+C+[9]*gap+B[::-1]
    d=[0]*len(P)
    for i in range(len(d)//2):
        j=len(d)-1-i
        d[i]=min(P[i],9);d[j]=P[i]-d[i]
        if i==0 and d[j]==0:d[i]-=1;d[j]+=1
    if len(d)%2:d[len(d)//2]=P[len(d)//2]//2
    assert d[-1]!=0 and [d[i]+d[-1-i] for i in range(len(d))]==P
    return int(''.join(map(str,d[::-1])))
def main():
    T=int(sys.argv[1]) if len(sys.argv)>1 else 100
    m=int(sys.argv[2]) if len(sys.argv)>2 else 3000
    gap=int(sys.argv[3]) if len(sys.argv)>3 else 12000
    repair=int(sys.argv[4]) if len(sys.argv)>4 else 0
    N=make_seed(m,gap,repair)
    for t in range(T+1):
        s=str(N)
        assert s!=s[::-1],f'palindrome at {t}'
        if t in (0,1,10,40,100,200,T):
            print('BIGINT',t,len(s),s[:20],s[-20:])
        if t<T:N+=int(s[::-1])
    print('BIGINT PASS',T)
if __name__=='__main__':main()
