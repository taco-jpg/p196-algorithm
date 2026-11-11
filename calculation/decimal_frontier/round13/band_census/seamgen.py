#!/usr/bin/env python3
"""r13a: seam search between a known exterior band E (left) and a band V (right), for a common clock.
Window columns [A_s, H_s) (cone trimmed): left background exact E rows, right background exact V rows; J = Lj free letters between
them at time 0; condition: every column of the window returns after N steps (N = lcm(TE, TV), rows of both bands return).
usage: seamgen.py --b 10 --clock 1000 --E 5,18,4,8,1,15,4,0,5 --ET 12 --V 18,9,0 --VT 120 --tauV 0 --rotV 0 --Lj 4 [--Nmul 1] [--solver kissat404] [--maxJ -1]
E row at clock phase 0, phase convention: letter at column cJ-1 = E[-1], i.e. column c < cJ carries E[(c-cJ) mod sE].
V row at clock phase 0: V_tauV (tauV a multiple of p), rotated by rotV, phase 0 at cJ + Lj (first band column).
Prints RESULT SAT J=... or UNSAT.  The first SAT J is printed; the band phase/rotation/time origin of V are loop parameters of the caller."""
import sys, time, argparse, math
import bandsat as BS
from bandsat import CT, CF

def parse_word(s): return [int(x) for x in s.split(',')]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--b',type=int,default=10); ap.add_argument('--clock',required=True); ap.add_argument('--E',required=True); ap.add_argument('--ET',type=int,required=True)
    ap.add_argument('--rotE',type=int,default=0)
    ap.add_argument('--V',required=True); ap.add_argument('--VT',type=int,required=True); ap.add_argument('--tauV',type=int,default=0); ap.add_argument('--rotV',type=int,default=0)
    ap.add_argument('--Lj',type=int,default=0); ap.add_argument('--Nmul',type=int,default=1); ap.add_argument('--solver',default='kissat404')
    ap.add_argument('--noreturn',action='store_true',help='no return condition on the junction (band restored only)')
    a=ap.parse_args()
    b=a.b; cl=[int(c) for c in a.clock]; p=len(cl)
    E0=parse_word(a.E); V0=parse_word(a.V)
    sE=len(E0); sV=len(V0)
    # E rows at clock phase 0: E0 given.  Rotate: letter at c<cJ is E0rot[(c-cJ)%sE]  with E0rot = E0 rotated by rotE
    Erot=E0[a.rotE:]+E0[:a.rotE]
    # V_tau at time tauV under the clock
    x=list(V0)
    for t in range(a.tauV):
        x,_,_,_,_=BS.rowstep(x,cl[t%p],b)
    Vrot=x[a.rotV:]+x[:a.rotV]
    N0=a.ET*a.VT//math.gcd(a.ET,a.VT)
    # also lcm with p (ET, VT are multiples of p already)
    N=N0*a.Nmul
    clock=[cl[t%p] for t in range(N)]
    Erows,EAs,EBs,ELs,EHs=BS.background(Erot,clock,b)
    Vrows,VAs,VBs,VLs,VHs=BS.background(Vrot,clock,b)
    assert Erows[N]==Erot and Vrows[N]==Vrot, ('not periodic', Erows[N]==Erot, Vrows[N]==Vrot)
    rfE=BS.right_fronts(Erows,b,clock)
    lfV=BS.left_fronts(Vrows,b,clock)
    Delta=max(sE,sV)+3
    Lj=a.Lj
    cJ=rfE[N]+Delta+2*sE+3
    Nw=cJ+Lj+lfV[N]+Delta+2*sV+3
    def inE(c): return c<cJ
    def inV(c): return c>=cJ+Lj
    def bgl(s,c):
        if inE(c): return Erows[s][(c-cJ)%sE]
        if inV(c): return Vrows[s][(c-cJ-Lj)%sV]
        return 0
    def bga(s,c):
        if inE(c): return EAs[s][(c-cJ)%sE]
        if inV(c): return VAs[s][(c-cJ-Lj)%sV]
        return 0
    def bgb(s,c):
        if inE(c): return EBs[s][(c-cJ)%sE]
        if c>=cJ+Lj: return VBs[s][(c-cJ-Lj)%sV]
        return 0
    A=[max(0,cJ-rfE[s]-Delta) for s in range(N+1)]
    H=[min(Nw,cJ+Lj+lfV[s]+Delta) for s in range(N+1)]
    t0=time.time()
    E=BS.Enc(a.solver)
    X,AL,BE,HL=BS.encode_strip(E,b,clock,Nw,A,H,bgl,bga,bgb,left_free=False,right_free=False)
    # initial: band letters on both sides inside the variable region at t=0
    NL=2*b-1
    for c in range(A[0],H[0]):
        if inE(c) or inV(c):
            E.add([X[0][c][bgl(0,c)]])
    # return condition: X[N][c] == X[0][c]
    for c in range(A[N],H[N]):
        if c<A[0] or c>=H[0]:
            # constant at time 0
            E.add([X[N][c][bgl(0,c)]])
        else:
            if a.noreturn and not (inE(c) or inV(c)):
                continue
            x0=X[0][c]; xN=X[N][c]
            for v in range(NL):
                E.add([-x0[v],xN[v]]); E.add([x0[v],-xN[v]])
    r=E.S.solve()
    ans='SAT' if r else 'UNSAT'
    extra=''
    if r:
        m=set(l for l in E.S.get_model() if l>0)
        J=[BS.letter_of(m,X[0][c])[0] for c in range(cJ,cJ+Lj)]
        extra=f' J={J}'
    print(f'RESULT seam b={b} clock={a.clock} E={a.E} ET={a.ET} rotE={a.rotE} V={a.V} VT={a.VT} tauV={a.tauV} rotV={a.rotV} Lj={Lj} N={N} word_V={Vrot}: {ans}{extra} vars={E.nv} clauses={E.nc} total={time.time()-t0:.1f}s rss={BS.rss_gb():.2f}GB',flush=True)

if __name__=='__main__':
    main()
