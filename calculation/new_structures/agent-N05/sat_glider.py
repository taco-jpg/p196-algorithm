#!/usr/bin/env python3
"""Exact QF_LIA moving-defect space-time strip search via libz3 C API.
Run: python3 calculation/new_structures/agent-N05/sat_glider.py --H 5 --phase 2 --free --one-shot --drift 1 --wide 3 --margin 6 --M 48 --origin 990 --first 18 --timeout 4500
Requires Python 3 and libz3.so.4. SMT-LIB may also be written using --output.
"""
import argparse, ctypes, re, time
from phase_packet import bulk as val, incarry as cup, local_step as nextpatch
z=ctypes.CDLL('libz3.so.4')
PTR=ctypes.c_void_p
def api(name,restype,args):
    f=getattr(z,name);f.restype=restype;f.argtypes=args;return f
mkconf=api('Z3_mk_config',PTR,[])
mkctx=api('Z3_mk_context',PTR,[PTR])
mk=api('Z3_mk_solver',PTR,[PTR])
ref=api('Z3_solver_inc_ref',None,[PTR,PTR])
fromstr=api('Z3_solver_from_string',None,[PTR,PTR,ctypes.c_char_p])
check=api('Z3_solver_check',ctypes.c_int,[PTR,PTR])
getmodel=api('Z3_solver_get_model',PTR,[PTR,PTR])
modelstr=api('Z3_model_to_string',ctypes.c_char_p,[PTR,PTR])
reason=api('Z3_solver_get_reason_unknown',ctypes.c_char_p,[PTR,PTR])
setparam=api('Z3_global_param_set',None,[ctypes.c_char_p,ctypes.c_char_p])
def solve(smt,timeout_ms=30000,model=False):
    setparam(b'timeout',str(timeout_ms).encode())
    ctx=mkctx(mkconf());sol=mk(ctx);ref(ctx,sol)
    fromstr(ctx,sol,smt.encode())
    result=check(ctx,sol)
    output=modelstr(ctx,getmodel(ctx,sol)).decode() if result==1 and model else ''
    return result,output,reason(ctx,sol).decode() if result==0 else ''

def high_boundary(t,abs_end):
    c=0
    for j in range(abs_end+30,abs_end,-1):c=(val(t,j)+c)//10
    return c
def expr(t,x):return f'p_{t}_{x}'
def carr(t,x,side):return f'{side}_{t}_{x}'

def smt(H,phase,origin,M,first,wide,drift,margin,seed,stationary,oneshot):
    lines=['(set-logic QF_LIA)']
    def add(s):lines.append('(assert '+s+')')
    for t in range(H+1):
        for x in range(M):
            e=expr(t,x);lines.append(f'(declare-const {e} Int)')
            shift=drift*t//max(1,H)
            inside=first-margin+shift<=x<first+wide+margin+shift
            if t==0 or (t==H and (stationary or oneshot)):
                shift=drift if t==H else 0
                inside=first+shift<=x<first+wide+shift
            if not inside:add(f'(= {e} {val(phase+t,origin+x)})')
            else:add(f'(and (<= 0 {e}) (<= {e} 18))')
    for t in range(H):
        gm=(1,0,0,0,1,0,0,0,1,0,0,0)[(phase+t)%12]
        for x in range(M+1):
            lines.append(f'(declare-const {carr(t,x,"l")} Int)')
        for x in range(M):
            lines.append(f'(declare-const {carr(t,x,"h")} Int)')
        add(f'(= {carr(t,0,"l")} {cup(phase+t,origin)})')
        add(f'(= {carr(t,M-1,"h")} {high_boundary(phase+t,origin+M-1)})')
        for x in range(M):
            add(f'(= {carr(t,x+1,"l")} (ite (>= (+ {expr(t,x)} {carr(t,x,"l")}) 10) 1 0))')
        for x in range(1,M):
            add(f'(= {carr(t,x-1,"h")} (ite (>= (+ {expr(t,x)} {carr(t,x,"h")}) 10) 1 0))')
        for x in range(2,M-2):
            y=x-gm
            u=f'(- (+ {expr(t,x)} {carr(t,x,"l")}) (* 10 {carr(t,x+1,"l")}))'
            v=f'(- (+ {expr(t,y)} {carr(t,y,"h")}) (* 10 {carr(t,y-1,"h")}))'
            add(f'(= {expr(t+1,x)} (+ {u} {v}))')
    if seed:
        for x in range(first,first+wide):
            add(f'(= {expr(0,x)} {seed[x-first]})')
    else:
        add('(or '+' '.join(f'(not (= {expr(0,x)} {val(phase,origin+x)}))' for x in range(first,first+wide))+')')
    if oneshot:
        add(f'(not (= {expr(0,first)} {val(phase,origin+first)}))')
        add(f'(not (= {expr(H,first+drift)} {val(phase+H,origin+first+drift)}))')
    if stationary:
        for x in range(2,M-2):
            if 0<=x-drift<M:
                add(f'(= {expr(H,x)} {expr(0,x-drift)})')
        add('(or '+' '.join(f'(not (= {expr(H,x)} {val(phase+H,origin+x)}))' for x in range(first+drift,first+wide+drift))+')')
    return '\n'.join(lines)+'\n'

def model_p(text,t,M):
    d={int(x):int(y) for x,y in re.findall(rf'p_{t}_(\d+) -> (\d+)',text)}
    assert len(d)==M,(len(d),M)
    return d

if __name__=='__main__':
    a=argparse.ArgumentParser()
    a.add_argument('--H',type=int,default=16)
    a.add_argument('--phase',type=int,default=2)
    a.add_argument('--origin',type=int,default=978)
    a.add_argument('--M',type=int,default=72)
    a.add_argument('--first',type=int,default=30)
    a.add_argument('--wide',type=int,default=4)
    a.add_argument('--margin',type=int,default=15)
    a.add_argument('--drift',type=int,default=0)
    a.add_argument('--free',action='store_true')
    a.add_argument('--return-glider',action='store_true')
    a.add_argument('--one-shot',action='store_true')
    a.add_argument('--timeout',type=int,default=30000)
    a.add_argument('--output',type=str,default='')
    args=a.parse_args()
    seed=None if args.free else [8,8,4,16]
    formula=smt(args.H,args.phase,args.origin,args.M,args.first,args.wide,args.drift,args.margin,
                seed,args.return_glider,args.one_shot)
    if args.output:open(args.output,'w').write(formula)
    t0=time.time();state,model,why=solve(formula,args.timeout,True)
    print('SAT' if state==1 else 'UNSAT' if state==-1 else 'UNKNOWN',f'seconds={time.time()-t0:.2f}',why)
    if state==1:
        last=model_p(model,args.H,args.M)
        first=model_p(model,0,args.M)
        print('SAT initial patch',[first[i] for i in range(args.first,args.first+args.wide)])
        diffs={(x,last[x]) for x in range(args.M) if last[x]!=val(args.phase+args.H,args.origin+x)}
        print('final changed coefficients local coords',sorted(diffs))
        changes={args.origin+args.first+i:first[args.first+i] for i in range(args.wide)
                 if first[args.first+i]!=val(args.phase,args.origin+args.first+i)}
        for step in range(args.H):changes=nextpatch(args.phase+step,changes)
        expected={(k-args.origin,v) for k,v in changes.items()}
        assert diffs==expected,(diffs,expected)
        print('INDEPENDENT_LOCAL_REPLAY_PASS')
