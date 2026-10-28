import sys
sys.path.insert(0,'/home/claude/research/w3_formats/code')
from gt import *
from scc_to_tmpl import *
recs=parse(sys.argv[1]); ri=int(sys.argv[2]); periods=int(sys.argv[3])
rec=recs[ri]; p=rec['p']
cur=templates(rec,core=())[0]; tot=0; hist=[]
for t in range(p*periods):
    cur,gm,info=step(cur)
    tot+=gm[0][2]
    if (t+1)%p==0: hist.append(tot)
print('cumulative gap change after each period:',hist)
