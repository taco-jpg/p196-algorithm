"""Bounded alternating-hole search. Unknown means no exclusion."""
from pathlib import Path
import json,time
from collections import Counter
from renewal_search_alt_smt import solve

def run():
    started=time.monotonic();minima=[];trials=[];counts=Counter()
    for C in range(2,17,2):
        found=None
        for L in range(C,4*C+9):
            for h in [0,1]:
                for phase in [0,1]:
                    z=solve(L,C,h,phase,200)
                    trials.append([L,C,h,phase,z if isinstance(z,str) else 'sat'])
                    if isinstance(z,str):counts[z]+=1
                    else:counts['sat']+=1;found=z;break
                if found:break
            if found or time.monotonic()-started>40:break
        minima.append(dict(C=C,first=found))
        if time.monotonic()-started>40:break
    out=dict(counts=dict(counts),minima=minima,trials=trials,seconds=time.monotonic()-started)
    Path(__file__).with_name('renewal_search_alt_minima.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(counts=counts,found=[(x['C'],x['first']['L']) for x in minima if x['first']],seconds=out['seconds']),indent=2))
if __name__=='__main__':run()
