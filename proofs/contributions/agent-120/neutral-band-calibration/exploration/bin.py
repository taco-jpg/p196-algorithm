def rev(n,b):
    r=0
    while n: r=r*b+n%b; n//=b
    return r
def digs(n,b):
    s=[]
    while n: s.append(n%b); n//=b
    return s[::-1]
n=22
for t in range(40):
    d=''.join(map(str,digs(n,2)))
    print(t, d)
    n=n+rev(n,2)
