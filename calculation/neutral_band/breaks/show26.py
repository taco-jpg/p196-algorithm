import os
import sys
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
import neutral_band_search as N
from neutral_band_search import *
for b, es in N._lean_certs():
    if b in (26,):
        for E in es:
            B,C,B2,C2,u,v = E
            print("B",B,"C",C)
            print("  DB",DB(b,B),"DC",DC(b,B,C),"DR",DR(b,B,C),"e1,e2,gam",e1(b,B),e2(b,B,C),gam(b,B,C),"-> u,v",u,v)
