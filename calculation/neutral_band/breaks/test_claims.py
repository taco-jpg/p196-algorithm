from lib import *
rng=random.Random(1)
# (1) carry = polarity of top non-neutral
bad=0; tot=0
for b in (2,3,4,10,11,17,26,32):
    for _ in range(3000):
        B,C=rand_state(b,rng)
        E1=e1(b,B); 
        assert E1==pol_top(b,B,0)
        assert e2(b,B,C)==pol_top(b,C,E1)
        assert gam(b,B,C)==pol_top(b,B[::-1],e2(b,B,C))
        tot+=1
print("claim1 carry=polarity of top non-neutral: OK on",tot)
# (2) overflow step flips (e1,e2) unless tie ; and (4) Delta identity on non-overflow steps w/o ties
stat=collections.Counter()
for b in (10,11,17,26,16):
    n=b-1
    for _ in range(20000):
        B,C=rand_state(b,rng,(2,8),(1,8))
        if not hyp(b,B,C): continue
        E1,E2,G=e1(b,B),e2(b,B,C),gam(b,B,C)
        B2=nextB(b,B,C); C2=nextC(b,B,C)
        # next-step carries (before trimming; trimming does not change e1,e2)
        F1,F2=e1(b,B2),e2(b,B2,C2)
        flipped = (F1==1-E1 and F2==1-E2)
        same = (F1==E1 and F2==E2)
        brk = (F1==F2)
        tie = (tie_depth(b,B2)>0 and False)
        # tie-free = top entries of B2 and C2 non-neutral
        notie = B2[-1]!=n and C2[-1]!=n
        stat[(b,'ovf' if G else 'non', 'brk' if brk else ('flip' if flipped else 'same'), 'notie' if notie else 'tie')]+=1
        if notie and not brk and not G:
            w,g_ = B[-1],C[0]
            # Delta identity: Delta' = 2 Delta + kB + kC - 1 with Delta = w+gamma-2n, needs bits complementary at time t (E1!=E2)
            kB = pol_top(b,B[:-1],0)
            # carry into top column of C: 
            # compute carries inside C with carry-in E1
            kk=E1; 
            for v in C[:-1]: kk=1 if v+kk>=b else 0
            Cm=C[-1]
            Dl = B[-1]+Cm-2*n
            Dl2= B2[-1]+C2[-1]-2*n
            if B[-1]!=n and Cm!=n:
                assert Dl2==2*Dl+kB+kk-1,(b,B,C,Dl,Dl2,kB,kk)
for k in sorted(stat): print(k,stat[k])
