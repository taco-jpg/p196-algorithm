# Complement-mirror dual of a rooted wire exterior: number = [B][wire^n][Theta(B)][(9,9)^k][mirror]
from pipeline import *
B=10
def setup(g):
    r=rooted(B,g)
    out=[]
    for c,walk in cycles_of(r):
        H=r['order'][walk[0]]
        if all(s==9 for s in psums(H)):
            left=find_path(r['el'],list(range(r['nroots'])),walk[0])[:-1]
            out.append(([r['order'][i] for i in left],H))
    return out
def build(leftH,wireH,n,k,t0=0):
    Bc=[(H[0][t0],H[1][t0]) for H in leftH]
    w=(wireH[0][t0],wireH[1][t0])
    Th=[(9-b,9-a) for (a,b) in reversed(Bc)]
    cols=Bc+[w]*n+Th+[(9,9)]*k
    low=[c[0] for c in cols]; high=[c[1] for c in cols][::-1]
    return low+high, len(Bc)
if __name__=='__main__':
    g=(0,0,0,0,1,1,1,0,0,0,1)
    for leftH,wireH in setup(g):
        K=len(leftH); T=len(g)
        for t0 in range(1):
            for (n,k) in ((3,20),(3,40),(10,40),(3,80)):
                digs,K=build(leftH,wireH,n,k,t0)
                N0=len(digs); t=0; dev=None; pal=None
                while t<3000:
                    if is_pal(digs): pal=t; break
                    L=len(digs)
                    ok=all(digs[i]==leftH[i][0][(t0+t)%T] and digs[L-1-i]==leftH[i][1][(t0+t)%T] for i in range(K))
                    if not ok: dev=t; break
                    digs=ra_step(digs,B); t+=1
                print('p11 exterior K=%d  wire n=%d  nines k=%d (digits %d): exterior follows its 11-periodic history until t=%s ; palindrome seen: %s'%(K,n,k,N0,dev,pal))
        digs,K=build(leftH,wireH,2,6,0)
        print('example n=2,k=6:',digits_to_str(digs))
