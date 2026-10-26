import os
import sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import p196cp as P
b=int(sys.argv[1]); nonmax = len(sys.argv)>2
for bb,es in P.mirror._lean_certs():
    if bb!=b: continue
    S=tuple((len(e[0]),len(e[1])) for e in es)
    M=P.encode(b,S,maximal=not nonmax)
    # fixed values
    fixed={}
    for k,e in enumerate(es):
        for i,x in enumerate(e[0]): fixed[f"B{k}_{i}"]=x
        for j in range((len(e[1])+1)//2): fixed[f"C{k}_{j}"]=e[1][j]
    # check domain/forbidden
    for i,(nm,lo,hi,fb) in enumerate(M.vars):
        if nm in fixed and not (lo<=fixed[nm]<=hi and fixed[nm] not in fb): print("domain violation",nm,fixed[nm],lo,hi,fb)
    # propagate: solve with the fixed vars
    M2=P.encode(b,S,maximal=not nonmax)
    for nm,x in fixed.items():
        i=M2.index[nm]; _,lo,hi,fb=M2.vars[i]; M2.vars[i]=(nm,x,x,())
    print(P.solve_cpsat(M2,10)[0])
