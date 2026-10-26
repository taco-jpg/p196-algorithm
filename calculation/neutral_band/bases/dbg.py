import os
import sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from decouple import *
from nb_mirror import _lean_certs
for b, es in _lean_certs():
    if b not in (11,26,17): continue
    for i,(B,C,B2,C2,u,v) in enumerate(es):
        r=G_ext(b,B); 
        okB = r is not None and (r[0],r[1])==(B2,u)
        E,g=r[2],r[3]
        h=H_int(b,C,E,g)
        okC = h is not None and (h[0],h[1])==(C2,v)
        print(b,i,'B',okB,'C',okC,'E',E,'Eint',E_of_C(b,C),'gam',g,'u',u,'v',v, 'e1,e2 mirror', E1(b,B), norm(b,C,E1(b,B))[1])
