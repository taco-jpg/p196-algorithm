# Adjacent-column segments next to a uniform absorbing band.  The band column u_t (a loop of k->2*((k+[k>=b])%b)),
# carry c_t=[u_t>=b].  A column x adjacent to it must satisfy floor((x_t+L_t)/b)=c_t, hn_t=c_t, and (non-gam)
# x_{t+1}=(x_t+L_t)%b+(x_t+c_t)%b ; at a gam time x_t=u_t is forced (digit match) with L_t free and x_{t+1} free in a range.
import sys
def seg_solutions(b, loop, ph, ell):
    """gam at time 0 (x_0=u_0, L free), then ell non-gam steps 1..ell, next gam at time ell+1 needs x_{ell+1}=u_{ell+1}.
       returns list of (x_1..x_ell, Lbits) with x_1 free (any in 0..2b-2)."""
    n=len(loop)
    u=lambda t: loop[(t+ph)%n]
    c=lambda t: 1 if u(t)>=b else 0
    sols=[]
    def rec(t,x,xs,Ls):
        # at time t (1<=t<=ell+1) holding x_t = x ; if t==ell+1 check gam condition
        if t==ell+1:
            if x==u(t): sols.append((tuple(xs),tuple(Ls)))
            return
        for L in (0,1):
            if (x+L)//b!=c(t): continue
            nx=(x+L)%b+(x+c(t))%b
            rec(t+1,nx,xs+[nx],Ls+[L])
    if ell==0:
        # gam, gam: x_1 must equal u_1 directly (x_1 free but is a gam time next)
        return [((),())]
    for x1 in range(0,2*b-1):
        rec(1,x1,[x1],[])
    return sols
def cyc_loops(b):
    nxt={k:2*((k+(1 if k>=b else 0))%b) for k in range(2*b-1) if k!=b-1}
    seen=set(); out=[]
    for k in nxt:
        if k in seen: continue
        path=[];x=k
        while x in nxt and x not in seen and x not in path: path.append(x); x=nxt[x]
        if x in path:
            i=path.index(x); out.append(path[i:])
        seen.update(path)
    return out
if __name__=="__main__":
    for b in map(int,sys.argv[1:]):
        for lp in cyc_loops(b):
            if len(lp)==1: continue
            for ph in range(len(lp)):
                row=[]
                for ell in range(0,6):
                    s=seg_solutions(b,lp,ph,ell)
                    row.append(len(s))
                print("b=%d loop=%s ph=%d  #segment solutions for ell=0..5 non-gam steps between gam times: %s"%(b,lp,ph,row))
