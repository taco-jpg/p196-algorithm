import sys
sys.path.insert(0,'/home/claude/research/w3_formats/code')
from gt import *
from scc_to_tmpl import *
recs=parse(sys.argv[1]); ri=int(sys.argv[2]); core=tuple(int(x) for x in sys.argv[3].split(',')) if len(sys.argv)>3 and sys.argv[3] else ()
rec=recs[ri]
T=templates(rec,core=core)[0]
cur=T; tot=0
for t in range(rec['p']*3):
    T2,gm,info=step(cur)
    off=gm[0][2] if gm else None
    print(t,'gam',info['gam'],'differs',info['differs'],'|B|',[len(it[1]) for it in T2.Hs if it[0]=='L'],'band',[len(it[1]) for it in T2.Hs if it[0]=='B'],'core',T2.core,'gap off',off)
    cur=T2
    if (t+1)%rec['p']==0:
        same_B = cur.Hs[0]==T.Hs[0]
        print('   after full period: B equal to start:',same_B,'| band equal:',cur.Hs[1]==T.Hs[1] if len(cur.Hs)>1 else None, '| core',cur.core)
