import os
import sys, random, collections
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import p196cp as P, sched
random.seed(5)
def build(b,S,drop):
    M=P.encode(b,S,maximal=('max' not in drop),extra_nonzero_B0=('b0' not in drop))
    if 'flip' in drop:   # remove e1+e2=1 : it is the constraint with exactly two coefficient-1 vars and rhs 1 and name cb/cc ... identify by structure
        keep=[]
        for d,lo,hi in M.cons:
            names=[M.vars[i][0] for i in d]
            if len(d)==2 and lo==hi==1 and all(abs(a)==1 for a in d.values()) and names[0][:2] in('cb','cc') and names[1][:2] in('cb','cc'): continue
            keep.append((d,lo,hi))
        M.cons=keep
    if 'trim' in drop:   # remove equalities "== b-1" on trimmed entries (constraints whose rhs equals b-1 and  >=1 var... ) 
        keep=[]
        for d,lo,hi in M.cons:
            if lo==hi==b-1 and len(d)>=1 and all(abs(a)<=b for a in d.values()) and not any(M.vars[i][0].startswith(('cb','cc','cr')) and False for i in d): 
                # heuristic: trim eqs involve digit expressions: many vars
                if len(d)>=3: continue
            keep.append((d,lo,hi))
        M.cons=keep
    return M
for b in (10,11):
    ss=[]
    for (p,NM,MM) in [(4,9,12),(6,9,12),(8,9,12)]:
        L=list(sched.schedules(p,2,NM,MM,4,7,base=b)) if p<=6 else list(sched.schedules(p,2,9,12,5,8,base=b))[:20000]
        ss+=random.sample(L,40)
    for drop in [(),('trim',),('flip',),('b0',),('max',),('trim','flip')]:
        c=collections.Counter()
        for S in ss:
            M=build(b,S,drop); st,_=P.solve_cpsat(M,5); c[st]+=1
        print(f"base {b} drop={drop}: {dict(c)}",flush=True)
