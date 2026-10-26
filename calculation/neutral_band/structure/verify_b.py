import sys, re
from bsys import bstep
def parse(line):
    b=int(re.search(r"b=(\d+)",line)[1]); Bs=[[int(x) for x in m.split(',') if x] for m in re.findall(r"\[([^\]]*)\]",line)]
    g=re.search(r"g=(\d+)",line)[1]; e=re.search(r" e=(\d+)",line)[1]
    return b,Bs,g,e
for line in open(sys.argv[1]):
    if not line.startswith("ACCEPT"): continue
    b,Bs,g,e=parse(line); p=len(Bs)
    cur=Bs[0]; ok=True; es=''; gs=''; us=[]
    for t in range(p):
        if cur!=Bs[t]: print("state mismatch at",t,cur,Bs[t]); ok=False
        nb,u,e1,gam=bstep(b,cur); es+=str(e1); gs+=str(gam); us.append(u); cur=nb
    print("b",b,"p",p,"returns to B0:",cur==Bs[0],"e-stream",es,"g-stream",gs,"u",us,"lens",[len(x) for x in Bs],"match",es==e and gs==g)
