import itertools, subprocess, re
from ctest import brute
bad=0; n=0; nf=0
for b in (2,3,4):
    for P in (1,2,3,4,5):
        for e in itertools.product((0,1),repeat=P):
            es=''.join(map(str,e)); gs='0'*P
            out=subprocess.run(['./cauto',str(b),es,gs,'1','7','-v','0'*P],capture_output=True,text=True).stdout
            got={int(m.group(1)) for m in re.finditer(r"m0=(\d+)",out) if 'FEASIBLE' in out}
            got={int(m.group(1)) for m in re.finditer(r"FEASIBLE .* m0=(\d+)",out)}
            exp={m0 for m0 in range(1,8) if brute(b,list(e),[0]*P,m0,[0]*P)>0}
            n+=1; nf+=len(exp)
            if got!=exp: bad+=1; print("MISMATCH",b,es,got,exp)
print("cases",n,"feasible",nf,"bad",bad)
