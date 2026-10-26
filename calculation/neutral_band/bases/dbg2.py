import os
import sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from decouple import *
from nb_mirror import _lean_certs
for b, es in _lean_certs():
    if b!=26: continue
    for i,(B,C,B2,C2,u,v) in enumerate(es[:3]):
        print(i,'B',B,'\n  expected',B2,u,'\n  G_ext',G_ext(b,B))
        print('  mirror step', step(b,B,C)[2:])
