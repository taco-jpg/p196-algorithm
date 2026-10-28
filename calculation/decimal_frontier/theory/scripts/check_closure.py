"""Check the mod-(b-1) closure condition  gcd(2^P-1,b-1) | E  on every ACCEPT line (exterior cycle found by bauto/bauto2/bauto4) in the given files."""
import sys, re, math
n=0; bad=0; nontriv=0; byb={}
for f in sys.argv[1:]:
    for line in open(f, errors='ignore'):
        m=re.search(r"ACCEPT b=(\d+) p=(\d+) g=([01]+) e=([01]+)",line)
        if not m: continue
        b,p,g,e=int(m[1]),int(m[2]),m[3],m[4]
        E=int(e,2); gg=math.gcd(2**p-1,b-1)
        n+=1
        if gg>1: nontriv+=1
        if E%gg: bad+=1; print("VIOLATION",f,b,p,g,e)
print("lines",n,"with gcd>1:",nontriv,"violations",bad)
