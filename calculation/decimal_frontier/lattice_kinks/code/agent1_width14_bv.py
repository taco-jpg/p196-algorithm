#!/usr/bin/env python3
"""Experimental independent QF_BV encoding of K1 rec0/m20 exact finite-window map.

Uses 5-bit digits (0..18) and Boolean carry. Local experimental solver only;
not a published certificate. Reproduces the canonical 19-symbol one-hot model.
"""
import sys,os,time,ctypes,resource,tempfile,json
from pathlib import Path
from agent1_width14_z3 import W,cups,gam,nB,m,p

def b5(x):
    assert 0<=x<32
    return '#b'+format(x,'05b')
def bvadd(a,b):return f'(bvadd {a} {b})'
def val(s):return s if isinstance(s,str) else b5(s)
def carry_bv(c):return f'(ite {c} {b5(1)} {b5(0)})' if isinstance(c,str) else b5(c)
def digit_sum(a,c):return bvadd(val(a),carry_bv(c))
def carry_out(a,c):return f'(bvuge {digit_sum(a,c)} {b5(10)})'
def remainder(a,c,carry):return f'(bvsub {digit_sum(a,c)} (ite {carry} {b5(10)} {b5(0)}))'
def plus(a,b):return bvadd(val(a),val(b))

def build(w,o,H,M=6):
    K=w+M;n0=400+o; lines=['(set-logic QF_BV)']
    ns=[n0]
    for t in range(H):ns.append(ns[-1]+gam[t%p])
    def cell(t,pos):return W[t%p][(pos-nB)%m]
    def cupat(t,pos):return cups[t%p][(pos-nB)%m]
    def latlayer(t):
        h=(ns[t]+1)//2
        return [cell(t,h-K+i) for i in range(K)]
    fz=K-w
    layer=latlayer(0)[:fz]
    for i in range(fz,K):
        v=f'P_0_{i}'
        lines.append(f'(declare-const {v} (_ BitVec 5))')
        lines.append(f'(assert (bvule {v} {b5(18)}))')
        layer.append(v)
    def parity(t,layer):
        if ns[t]%2:
            lines.append(f'(assert (= (bvand {val(layer[-1])} {b5(1)}) {b5(0)}))')
    parity(0,layer)
    for t in range(H):
        n=ns[t];h=(n+1)//2;g=gam[t%p];odd=n&1
        n2=ns[t+1];h2=(n2+1)//2;dh=h2-h
        cu=[None]*(K+1);Oup=[None]*K
        cu[0]=cupat(t,h-K)
        for i in range(K):
            c=f'U_{t}_{i+1}';u=f'UP_{t}_{i}'
            lines.append(f'(define-fun {c} () Bool {carry_out(layer[i],cu[i])})')
            lines.append(f'(define-fun {u} () (_ BitVec 5) {remainder(layer[i],cu[i],c)})')
            cu[i+1]=c;Oup[i]=u
        D=[None]*K;Odn=[None]*K
        if odd:
            D[K-1]=cu[K-1];Odn[K-1]=Oup[K-1];D[K-2]=cu[K];top=K-2
        else:
            D[K-1]=cu[K];top=K-1
        for i in range(top,-1,-1):
            if i<top:
                c=f'D_{t}_{i}'
                lines.append(f'(define-fun {c} () Bool {carry_out(layer[i+1],D[i+1])})')
                D[i]=c
            u=f'DN_{t}_{i}'
            lines.append(f'(define-fun {u} () (_ BitVec 5) {remainder(layer[i],D[i],carry_out(layer[i],D[i]))})')
            Odn[i]=u
        nxt=[]
        for i2 in range(K):
            if i2<2:
                nxt.append(cell(t+1,h2-K+i2));continue
            i=i2+dh
            if g==0:
                up=Oup[i];part=Oup[i] if odd and i==K-1 else Odn[i]
            else:
                up=Oup[i] if i<=K-1 else Odn[K-1];part=Odn[i-1]
            target=cell(t+1,h2-K+i2) if i2<fz else None
            expr=plus(up,part)
            if target is not None:
                lines.append(f'(assert (= {expr} {b5(target)}))')
                nxt.append(target)
            else:
                v=f'P_{t+1}_{i2}'
                lines.append(f'(declare-const {v} (_ BitVec 5))')
                lines.append(f'(assert (= {v} {expr}))')
                lines.append(f'(assert (bvule {v} {b5(18)}))')
                nxt.append(v)
        layer=nxt
        parity(t+1,layer)
    return '\n'.join(lines)+'\n',K

def solve(w,o,H,workdir):
    st=time.time();script,K=build(w,o,H)
    fn=Path(workdir)/f'agent1_bv_w{w}_o{o}_h{H}.smt2'
    fn.write_text(script)
    print('BV script',len(script),'bytes', 'K',K,'build',round(time.time()-st,2),flush=True)
    z=ctypes.CDLL('libz3.so.4');ptr=ctypes.c_void_p;s=ctypes.c_char_p;i=ctypes.c_int
    def api(name,rest,args):
        f=getattr(z,name);f.restype=rest;f.argtypes=args;return f
    cfg=api('Z3_mk_config',ptr,[])()
    ctx=api('Z3_mk_context',ptr,[ptr])(cfg)
    sol=api('Z3_mk_solver',ptr,[ptr])(ctx)
    api('Z3_solver_inc_ref',None,[ptr,ptr])(ctx,sol)
    api('Z3_solver_from_file',None,[ptr,ptr,s])(ctx,sol,str(fn).encode())
    print('BV parsed',round(time.time()-st,2),flush=True)
    status=api('Z3_solver_check',i,[ptr,ptr])(ctx,sol)
    print('result',status,'wall',round(time.time()-st,2),'peakMB',resource.getrusage(resource.RUSAGE_SELF).ru_maxrss//1024,flush=True)
    if status==1:
        model=api('Z3_solver_get_model',ptr,[ptr,ptr])(ctx,sol)
        api('Z3_model_inc_ref',None,[ptr,ptr])(ctx,model)
        bvs=api('Z3_mk_bv_sort',ptr,[ptr,i])(ctx,5)
        mk_symbol=api('Z3_mk_string_symbol',ptr,[ptr,s]);mkconst=api('Z3_mk_const',ptr,[ptr,ptr,ptr]);eval=api('Z3_model_eval',ctypes.c_bool,[ptr,ptr,ptr,ctypes.c_bool,ctypes.POINTER(ptr)])
        tostr=api('Z3_ast_to_string',s,[ptr,ptr])
        fz=6;h=(400+o+1)//2
        row=[W[0][(h-K+i-nB)%m] for i in range(fz)]
        for j in range(fz,K):
            ast=mkconst(ctx,mk_symbol(ctx,f'P_0_{j}'.encode()),bvs)
            out=ptr();assert eval(ctx,model,ast,True,ctypes.byref(out))
            lit=tostr(ctx,out).decode();assert lit.startswith('#b')
            row.append(int(lit[2:],2))
        out=Path(str(fn)+'.witness.json');out.write_text(json.dumps({'initial_layer':row,'K':K},indent=2))
        print('witness',row,flush=True)
    return status

if __name__=='__main__':
    w,o,H=map(int,sys.argv[1:4]);workdir=os.environ.get('K1_WORK_DIR',tempfile.gettempdir());solve(w,o,H,workdir)
