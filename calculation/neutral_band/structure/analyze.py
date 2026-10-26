import os
import sys
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
import neutral_band_search as N
certs = N._lean_certs()
def carries(b, w, c=0):
    out=[]
    for v in w:
        out.append(c); c=(v+c)//b
    out.append(c); return out
for b, es in certs:
    print("=== base", b, "edges", len(es))
    for E in es:
        B,C,B2,C2,u,v=E
        e1=N.e1(b,B); e2=N.e2(b,B,C); g=N.gam(b,B,C)
        print(f" |B|={len(B)} |C|={len(C)} e1={e1} e2={e2} gam={g} xd={N.xd(b,B)} yd={N.yd(b,B,C)} u={u} v={v} |B2|={len(B2)} |C2|={len(C2)}")
        if b<=32 and len(B)<=3: print("   B",B,"C",C)
        if b in (11,17,26):
            cb=carries(b,B,0); cc=carries(b,C,e1); cr=carries(b,B[::-1],e2)
            print("   carriesB",''.join(map(str,cb)),"carriesC",''.join(map(str,cc)),"carriesRB",''.join(map(str,cr)))
