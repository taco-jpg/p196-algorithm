import os
import sys
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
import neutral_band_search as N
for b,es in N._lean_certs():
    print("base",b,"p=",len(es))
    for E in es:
        B,C,B2,C2,u,v=E
        print("  n=%d m=%d gam=%d u=%d v=%d e1=%d e2=%d"%(len(B),len(C),N.gam(b,B,C),u,v,N.e1(b,B),N.e2(b,B,C)), "B=",B,"C=",C)
