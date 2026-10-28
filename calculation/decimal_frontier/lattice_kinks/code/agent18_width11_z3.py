#!/usr/bin/env python3
"""Independent one-hot CNF encoding for the exact period-48 rec2 finite-window map.
Usage: python3 agent18_width11_z3.py W O H
Requires CPython 3 and a system libz3.so. Single-core SAT, at most 8 GiB.
"""
import sys,time,ctypes,resource,ctypes.util,tempfile
from pathlib import Path
HERE=Path(__file__).parent

def load_lat():
 a=list(map(int,(HERE.parent/'data'/'lat2.txt').read_text().split()));p,nB,m,b=a[:4];i=4
 gam=a[i:i+p];i+=p
 W=[a[i+t*m:i+(t+1)*m] for t in range(p)];i+=p*m
 cup=[a[i+t*m:i+(t+1)*m] for t in range(p)]
 assert b==10
 return dict(p=p,nB=nB,m=m,gam=gam,W=W,cup=cup)

class Enc:
 def __init__(self): self.nv=0;self.cl=[]
 def new(self):self.nv+=1;return self.nv
 def group(self,D):
  g=[self.new() for _ in range(D)];self.cl.append(g[:])
  for i in range(D):
   for j in range(i+1,D):self.cl.append([-g[i],-g[j]])
  return g
 def gate(self,f,Dout,*ins):
  if all(isinstance(x,int) for x in ins):return f(*ins)
  out=self.group(Dout);varidx=[k for k,x in enumerate(ins) if not isinstance(x,int)]
  def rec(k,vals):
   if k==len(varidx):
    args=[x if isinstance(x,int) else None for x in ins]
    for j,v in zip(varidx,vals):args[j]=v
    r=f(*args);self.cl.append([-ins[j][v] for j,v in zip(varidx,vals)]+[out[r]]);return
   for v in range(len(ins[varidx[k]])):rec(k+1,vals+[v])
  rec(0,[]);return out
 def forbid_sum(self,u,d,target):
  if isinstance(u,int) and isinstance(d,int):
   if u+d!=target:self.cl.append([])
  elif isinstance(u,int):
   for v in range(len(d)):
    if u+v!=target:self.cl.append([-d[v]])
  elif isinstance(d,int):
   for v in range(len(u)):
    if v+d!=target:self.cl.append([-u[v]])
  else:
   for v in range(len(u)):
    for z in range(len(d)):
     if v+z!=target:self.cl.append([-u[v],-d[z]])

def build(lat,w,o,H,M=6):
 p,nB,m,gam,W,cup=lat['p'],lat['nB'],lat['m'],lat['gam'],lat['W'],lat['cup'];K=w+M;n0=400+o;E=Enc()
 def cell(t,pos):return W[t%p][(pos-nB)%m]
 def cupat(t,pos):return cup[t%p][(pos-nB)%m]
 ns=[n0]
 for t in range(H):ns.append(ns[-1]+gam[t%p])
 def lattice(t):
  h=(ns[t]+1)//2;return [cell(t,h-K+i) for i in range(K)]
 layers=[lattice(0)[:M]+[E.group(19) for _ in range(w)]]
 def parity(t):
  if ns[t]%2:
   top=layers[t][K-1]
   if not isinstance(top,int):
    for v in range(1,19,2):E.cl.append([-top[v]])
 parity(0)
 for t in range(H):
  n=ns[t];h=(n+1)//2;g=gam[t%p];odd=n%2==1;n2=n+g;h2=(n2+1)//2;dh=h2-h;P=layers[t]
  cu=[None]*(K+1);Oup=[None]*K;cu[0]=cupat(t,h-K)
  for i in range(K):
   cu[i+1]=E.gate(lambda pv,a:int(pv+a>=10),2,P[i],cu[i]);Oup[i]=E.gate(lambda pv,a:(pv+a)%10,10,P[i],cu[i])
  D=[None]*K;Odn=[None]*K
  if odd:
   D[K-1]=cu[K-1];Odn[K-1]=Oup[K-1];D[K-2]=cu[K];top=K-2
  else:
   D[K-1]=cu[K];top=K-1;Odn[K-1]=E.gate(lambda pv,d:(pv+d)%10,10,P[K-1],D[K-1])
  for i in range(top,-1,-1):
   if i<top:D[i]=E.gate(lambda pv,d:int(pv+d>=10),2,P[i+1],D[i+1])
   Odn[i]=E.gate(lambda pv,d:(pv+d)%10,10,P[i],D[i])
  nxt=[]
  for i2 in range(K):
   if i2<2:
    nxt.append(cell(t+1,h2-K+i2));continue
   i=i2+dh
   if g==0:
    up=Oup[i];part=Oup[i] if (odd and i==K-1) else Odn[i]
   else:
    up=Oup[i] if i<=K-1 else Odn[K-1];part=Odn[i-1]
   if i2<M:
    E.forbid_sum(up,part,cell(t+1,h2-K+i2));nxt.append(cell(t+1,h2-K+i2))
   else:nxt.append(E.gate(lambda u,d:u+d,19,up,part))
  layers.append(nxt);parity(t+1)
 E.layers=layers;E.ns=ns
 return E

def solvez3(E,path):
 with open(path,'w') as f:
  f.write('(set-logic QF_UF)\n')
  for i in range(1,E.nv+1):f.write(f'(declare-fun v{i} () Bool)\n')
  for cl in E.cl:
   if not cl:f.write('(assert false)\n');continue
   lit=lambda k:(f'v{k}' if k>0 else f'(not v{-k})')
   f.write('(assert (or '+' '.join(map(lit,cl))+'))\n')
 t=time.time();lib=ctypes.CDLL(ctypes.util.find_library('z3') or 'libz3.so.4');ptr=ctypes.c_void_p
 def fn(n,rest,args):
  f=getattr(lib,n);f.restype=rest;f.argtypes=args;return f
 mkcfg=fn('Z3_mk_config',ptr,[]);mkctx=fn('Z3_mk_context',ptr,[ptr]);mktactic=fn('Z3_mk_tactic',ptr,[ptr,ctypes.c_char_p]);mksolver=fn('Z3_mk_solver_from_tactic',ptr,[ptr,ptr]);inc=fn('Z3_solver_inc_ref',None,[ptr,ptr]);fromfile=fn('Z3_solver_from_file',None,[ptr,ptr,ctypes.c_char_p]);check=fn('Z3_solver_check',ctypes.c_int,[ptr,ptr]);reason=fn('Z3_solver_get_reason_unknown',ctypes.c_char_p,[ptr,ptr]);cfg=mkcfg();ctx=mkctx(cfg);tactic=mktactic(ctx,b'sat');solver=mksolver(ctx,tactic);inc(ctx,solver)
 fromfile(ctx,solver,str(path).encode());load=time.time()-t;t=time.time();result=check(ctx,solver);return result,load,time.time()-t,reason(ctx,solver).decode() if result==0 else ''

if __name__=='__main__':
 w,o,H=map(int,sys.argv[1:4]);t=time.time();E=build(load_lat(),w,o,H);print('built',E.nv,'vars',len(E.cl),'clauses',round(time.time()-t,2),'s',flush=True)
 resource.setrlimit(resource.RLIMIT_AS,(8*1024**3,8*1024**3))
 with tempfile.TemporaryDirectory(prefix='agent18_') as td:
  result,load,elapsed,reason=solvez3(E,Path(td)/'instance.smt2')
 print('RESULT',w,o,H,{1:'SAT',-1:'UNSAT',0:'UNKNOWN'}[result],'load',round(load,2),'solve',round(elapsed,2),'reason',reason,flush=True)
 sys.exit(0 if result in (1,-1) else 2)
