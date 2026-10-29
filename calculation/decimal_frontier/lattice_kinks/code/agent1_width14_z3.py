#!/usr/bin/env python3
"""Independent exact one-hot CNF/Z3 implementation of rec0 K1 window SAT.

  K1_WORK_DIR=/tmp python3 agent1_width14_z3.py 14 0 80
  K1_WORK_DIR=/tmp python3 agent1_width14_z3.py 14 0 64 --seq --witness

Uses libz3.so.4 via ctypes (Linux). Optional --seq uses linear-size
sequential exactly-one encoding; default is the original pairwise encoding. The lattice was transcribed from
calculation/decimal_frontier/lattice_formats/p8_scc.txt; controls in
agent1_width14_controls.sh compare the canonical SAT implementation.
No state cap, but UNSAT is a computational solver result, not Lean-verified.
"""
import ctypes, itertools, sys, time, json, resource, os, tempfile
from pathlib import Path
Wcols=[
[17,12,6,10,2,3,7,8],
[3,11,3,9,0,2,4,11],
[1,4,9,13,7,7,15,10],
[13,5,11,1,3,10,0,6],
[17,12,5,7,14,8,17,8],
[11,10,1,6,12,8,16,15],
[14,7,15,7,15,9,18,16],
[3,8,17,14,9,5,11,11],
[18,12,5,13,7,17,15,8],
[1,10,1,6,13,11,4,10],
[2,3,7,8,17,12,6,10],
[0,2,4,11,3,11,3,9],
[7,7,15,10,1,4,9,13],
[3,10,0,6,13,5,11,1],
[14,8,17,8,17,12,5,7],
[12,8,16,15,11,10,1,6],
[15,9,18,16,14,7,15,7],
[9,5,11,11,3,8,17,14],
[7,17,15,8,18,12,5,13],
[13,11,4,10,1,10,1,6]
]
p,m,nB=8,20,39
gam=[int(c) for c in '10101010']
W=[[r[t] for r in Wcols] for t in range(p)]
cups=[]
for t in range(p):
    row=W[t];c=0
    for _ in range(100):
        out=[]
        for x in row:
            out.append(c);c=int(x+c>=10)
    cups.append(out)
for t in range(8):
    cc=cups[t][-1]
    assert [*cups[t]]==[int(x) for x in cups[t]]
class Enc:
 def __init__(self,seq=False):self.nv=0;self.cl=[];self.seq=seq
 def new(self):self.nv+=1;return self.nv
 def group(self,D):
  g=[self.new() for _ in range(D)]
  self.cl.append(g)
  if self.seq and D>1:
   t=[self.new() for _ in range(D-1)]
   self.cl.append([-g[0],t[0]])
   for j in range(1,D-1):
    self.cl.extend(([-g[j],t[j]],[-t[j-1],t[j]],[-g[j],-t[j-1]]))
   self.cl.append([-g[-1],-t[-1]])
  else:
   for i in range(D):
    for j in range(i+1,D):self.cl.append([-g[i],-g[j]])
  return g
 def gate(self,f,Dout,*ins):
  if all(isinstance(x,int) for x in ins):return f(*ins)
  o=self.group(Dout)
  ids=[i for i,s in enumerate(ins) if not isinstance(s,int)]
  for vals in itertools.product(*(range(len(ins[i])) for i in ids)):
   args=list(ins)
   for i,v in zip(ids,vals):args[i]=v
   r=f(*args)
   self.cl.append([-ins[i][v] for i,v in zip(ids,vals)]+[o[r]])
  return o
 def forbid_sum(self,u,d,target):
  if isinstance(u,int) and isinstance(d,int):
   if u+d!=target:self.cl.append([])
   return
  if isinstance(u,int):
   for dv in range(len(d)):
    if u+dv!=target:self.cl.append([-d[dv]])
   return
  if isinstance(d,int):
   for uv in range(len(u)):
    if uv+d!=target:self.cl.append([-u[uv]])
   return
  for uv in range(len(u)):
   for dv in range(len(d)):
    if uv+dv!=target:self.cl.append([-u[uv],-d[dv]])

def build(w,o,H,M=6,seq=False):
 K=w+M;n0=400+o;E=Enc(seq=seq);
 def cell(t,pos):return W[t%p][(pos-nB)%m]
 def cupat(t,pos):return cups[t%p][(pos-nB)%m]
 ns=[n0]
 for t in range(H):ns.append(ns[-1]+gam[t%p])
 def latlayer(t):
  h=(ns[t]+1)//2
  return [cell(t,h-K+i) for i in range(K)]
 layers=[latlayer(0)[:K-w]+[E.group(19) for _ in range(w)]]
 def parity(t):
  if ns[t]%2:
   top=layers[t][K-1]
   if not isinstance(top,int):
    for v in range(1,19,2):E.cl.append([-top[v]])
 parity(0);fz=K-w
 for t in range(H):
  n=ns[t];h=(n+1)//2;g=gam[t%p];odd=n&1
  P=layers[t];n2=n+g;h2=(n2+1)//2;dh=h2-h
  cu=[None]*(K+1);Oup=[None]*K
  cu[0]=cupat(t,h-K)
  for i in range(K):
   cu[i+1]=E.gate(lambda pv,a: int(pv+a>=10),2,P[i],cu[i])
   Oup[i]=E.gate(lambda pv,a:(pv+a)%10,10,P[i],cu[i])
  D=[None]*K;Odn=[None]*K
  if odd:
   D[K-1]=cu[K-1];Odn[K-1]=Oup[K-1];D[K-2]=cu[K];top=K-2
  else:
   D[K-1]=cu[K];top=K-1
   Odn[K-1]=E.gate(lambda pv,d:(pv+d)%10,10,P[K-1],D[K-1])
  for i in range(top,-1,-1):
   if i<top:D[i]=E.gate(lambda pv,d:int(pv+d>=10),2,P[i+1],D[i+1])
   Odn[i]=E.gate(lambda pv,d:(pv+d)%10,10,P[i],D[i])
  nxt=[]
  for i2 in range(K):
   if i2<2:
    nxt.append(cell(t+1,h2-K+i2));continue
   i=i2+dh
   if g==0:
    up=Oup[i];part=Oup[i] if odd and i==K-1 else Odn[i]
   else:
    up=Oup[i] if i<=K-1 else Odn[K-1];part=Odn[i-1]
   if i2<fz:
    E.forbid_sum(up,part,cell(t+1,h2-K+i2));nxt.append(cell(t+1,h2-K+i2))
   else:nxt.append(E.gate(lambda u,d:u+d,19,up,part))
  layers.append(nxt);parity(t+1)
 return E,layers,ns

def solve_z3(e,fn,layers=None):
 print('encoding',e.nv,'vars',len(e.cl),'clauses',flush=True)
 t=time.time()
 with open(fn,'w',buffering=2**20) as f:
  f.write(''.join(f'(declare-const v{i} Bool)\n' for i in range(1,e.nv+1)))
  for clause in e.cl:
   if not clause:f.write('(assert false)\n');continue
   if len(clause)==1:
    x=clause[0];v=f'v{abs(x)}'; expr=v if x>0 else f'(not {v})'
   else:expr='(or '+' '.join(f'v{x}' if x>0 else f'(not v{-x})' for x in clause)+')'
   f.write('(assert '+expr+')\n')
 print('smt2 bytes',os.path.getsize(fn),'time',round(time.time()-t,1),flush=True)
 z=ctypes.CDLL('libz3.so.4');ptr=ctypes.c_void_p;s=ctypes.c_char_p;i=ctypes.c_int
 def api(name,rest,args):
  a=getattr(z,name);a.restype=rest;a.argtypes=args;return a
 cfg=api('Z3_mk_config',ptr,[])()
 ctx=api('Z3_mk_context',ptr,[ptr])(cfg)
 sol=api('Z3_mk_solver',ptr,[ptr])(ctx)
 api('Z3_solver_inc_ref',None,[ptr,ptr])(ctx,sol)
 api('Z3_solver_from_file',None,[ptr,ptr,s])(ctx,sol,str(fn).encode())
 print('Z3 parsed',round(time.time()-t,1),flush=True)
 st=api('Z3_solver_check',i,[ptr,ptr])(ctx,sol)
 print('result',st,'wall',round(time.time()-t,1),'peakMB',resource.getrusage(resource.RUSAGE_SELF).ru_maxrss//1024,flush=True)
 if st==1 and layers is not None:
  model=api('Z3_solver_get_model',ptr,[ptr,ptr])(ctx,sol)
  api('Z3_model_inc_ref',None,[ptr,ptr])(ctx,model)
  boolsort=api('Z3_mk_bool_sort',ptr,[ptr])(ctx)
  mk_symbol=api('Z3_mk_string_symbol',ptr,[ptr,s])
  mkconst=api('Z3_mk_const',ptr,[ptr,ptr,ptr])
  modeleval=api('Z3_model_eval',ctypes.c_bool,[ptr,ptr,ptr,ctypes.c_bool,ctypes.POINTER(ptr)])
  getval=api('Z3_get_bool_value',i,[ptr,ptr])
  vals=[]
  for sig in layers[0]:
   if isinstance(sig,int):vals.append(sig);continue
   v=None
   for j,id in enumerate(sig):
    ast=mkconst(ctx,mk_symbol(ctx,f'v{id}'.encode()),boolsort)
    out=ptr()
    assert modeleval(ctx,model,ast,True,ctypes.byref(out))
    if getval(ctx,out)==1:
     assert v is None
     v=j
   assert v is not None
   vals.append(v)
  Path(str(fn)+'.witness.json').write_text(json.dumps({'initial_layer':vals,'K':len(vals)},indent=2))
  print('witness initial layer',vals,flush=True)
 return st

if __name__=='__main__':
 w,o,h=[int(a) for a in sys.argv[1:4]]
 E,layers,_=build(w,o,h,seq="--seq" in sys.argv)
 fixed=[x for x in sys.argv[4:] if x.startswith('--top=')]
 assert len(fixed)<=1
 top=int(fixed[0].split('=',1)[1]) if fixed else None
 if top is not None:
  assert 0<=top<=18
  E.cl.append([layers[0][-1][top]])
 workdir=Path(os.environ.get('K1_WORK_DIR', tempfile.gettempdir()))
 workdir.mkdir(parents=True,exist_ok=True)
 suffix=f'_top{top}' if top is not None else ''
 fn=workdir/f'agent1_w{w}_o{o}_h{h}{suffix}.smt2'
 print('w,o,H=',w,o,h, 'cup0=',cups[0], flush=True)
 solve_z3(E,fn,layers if "--witness" in sys.argv else None)
