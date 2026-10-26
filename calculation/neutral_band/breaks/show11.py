import sys
from btransfer import decide, patterns, from_path
from decouple import phiB
b=10; p=int(sys.argv[1])
for O in patterns(p):
    r,ns,path=decide(b,p,O,3_000_000,want_path=True)
    if r=='EXISTS':
        B=from_path(b,p,path); print("pattern O=",O,"sum gam=",sum(O),"states",ns,"|B|=",len(B))
        cur=list(B)
        for t in range(p):
            nb,u,E1,g=phiB(b,cur); print("  t=%2d e1=%d gam=%d u=%d  B="%(t,E1,g,u),cur); cur=nb
        print("returns:",cur==B)
