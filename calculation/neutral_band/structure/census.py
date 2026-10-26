import sys, collections
from bsys import *
nmax=int(sys.argv[1]); lo=int(sys.argv[2]); hi=int(sys.argv[3])
for b in range(lo,hi+1):
    cyc=bgraph(b,nmax)
    streams=collections.Counter()
    for c,s in cyc.items():
        k=min(range(len(s)),key=lambda j:s[j:]+s[:j]); streams[s[k:]+s[:k]]+=1
    desc=[]
    for s,cnt in sorted(streams.items(),key=lambda kv:(len(kv[0]),kv[0])):
        desc.append(f"{cnt}x p{len(s)} e={''.join(str(e) for e,g,u in s)} g={''.join(str(g) for e,g,u in s)}")
    print(b,len(cyc),"; ".join(desc))
