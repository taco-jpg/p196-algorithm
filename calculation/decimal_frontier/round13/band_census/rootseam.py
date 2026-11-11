#!/usr/bin/env python3
"""r13a: rooted exterior search: find an exterior word X (columns 0..w-1, root at column 0) followed by the band V^inf (rows V_tau rotated, phase 0 at column w)
such that the whole configuration is time-periodic with period N under the forced clock g (overflow bit = carry out of column 0 at every step).
Root conditions: alpha_0 = 0; at overflow steps the new leading digit contributes 1: P'_0 = lo_0 + 1; beta_0(t) = g_t (the actual overflow equals the clock); letter at column 0 >= 1 (leading digit).
Return condition: all columns of the window return after N steps.
usage: rootseam.py --clock 1000 --V 5,11,8 [--N 24] --w 30 [--solver cadical195]"""
import sys, argparse, time
import bandsat as BS
ap=argparse.ArgumentParser(); ap.add_argument('--b',type=int,default=10); ap.add_argument('--clock',default='1000'); ap.add_argument('--V',required=True); ap.add_argument('--N',type=int,required=True); ap.add_argument('--w',type=int,required=True); ap.add_argument('--solver',default='cadical195')
a=ap.parse_args()
b=a.b; NL=2*b-1
cl=[int(c) for c in a.clock]; p=len(cl)
V=[int(x) for x in a.V.split(',')]; s=len(V)
N=a.N; w=a.w
clock=[cl[t%p] for t in range(N)]
rows,As,Bs,Ls,Hs=BS.background(V,clock,b)
assert rows[N]==list(V),'V not N-periodic'
lf=BS.left_fronts(rows,b,clock)
Delta=s+3
Nw=w+lf[N]+Delta+2*s+3
def bgl(t,c): return rows[t][(c-w)%s] if c>=w else 0
def bga(t,c): return As[t][(c-w)%s] if c>=w else 0
def bgb(t,c): return Bs[t][(c-w)%s] if c>=w else 0
A=[0]*(N+1); H=[min(Nw,w+lf[t]+Delta) for t in range(N+1)]
t0=time.time()
E=BS.Enc(a.solver)
X,AL,BE,HL=BS.encode_strip(E,b,clock,Nw,A,H,bgl,bga,bgb,left_free=True,right_free=False)
# root conditions
for t in range(N):
    E.add([-AL[t][0]])
    if clock[t]:
        E.add([HL[t][1]])
        E.add([BE[t][0]])
    else:
        E.add([-BE[t][0]])
    E.add([-X[t][0][0]])  # leading digit >= 1 at column 0 (letter >= 1)
E.add([-X[N][0][0]])
# initial band letters
for c in range(w,H[0]): E.add([X[0][c][V[(c-w)%s]]])
# return condition
for c in range(0,H[N]):
    if c<H[0]:
        for v in range(NL):
            E.add([-X[0][c][v],X[N][c][v]]); E.add([X[0][c][v],-X[N][c][v]])
    else:
        E.add([X[N][c][bgl(0,c)]])
r=E.S.solve()
ans='SAT' if r else 'UNSAT'
extra=''
if r:
    m=set(l for l in E.S.get_model() if l>0)
    Xw=[BS.letter_of(m,X[0][c])[0] for c in range(w)]
    extra=f' X={Xw}'
print(f'RESULT rootseam clock={a.clock} V={a.V} N={N} w={w}: {ans}{extra} vars={E.nv} clauses={E.nc} total={time.time()-t0:.1f}s',flush=True)
