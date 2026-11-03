import sys
T=int(sys.argv[1]); out=[]
for w in ["01000101","10111010","1000100001110111"]:
    if T % len(w): continue
    full=w*(T//len(w))
    for o in range(4): out.append("stream:"+full[o:]+full[:o])
print(" ".join(out))
