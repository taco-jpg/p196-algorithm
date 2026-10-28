from runsat import stream
b=10; N=9
cyc=stream('p11'); p=11
gam=[cyc[t][1] for t in range(p)]; e1=[cyc[t][2] for t in range(p)]
T=11
def traj(v0, dins):
    v=v0; out=[v]
    for t in range(T):
        a=e1[t]; din=dins[t]
        da=(v+a)%b; dd=(v+din)%b
        vn=da+(N*e1[t] if gam[t] else dd)
        out.append(vn)
        v=vn
    return out
import itertools
# cell 0: for v0 in range, din choices satisfying [v+din>=10]==1-e1
sols=[]
for v0 in range(19):
    def rec(t,v,dins,tr):
        if t==T:
            if v==v0: sols.append((v0,tuple(dins),tuple(tr)))
            return
        for din in (0,1):
            if ((v+din)>=b)!=bool(1-e1[t]): continue
            a=e1[t]; da=(v+a)%b; dd=(v+din)%b
            vn=da+(N*e1[t] if gam[t] else dd)
            if vn>18: continue
            rec(t+1,vn,dins+[din],tr+[vn])
    rec(0,v0,[],[v0])
print('t   ',list(range(T)))
print('gam ',gam); print('e1  ',e1)
for s in sols: print(s[0],'din0',s[1],'v0(t)',s[2])
