"""Independent full-array mask propagation versus symbolic A^K pumping at EVERY layer."""
from symbolic_all_lengths import ALL,norm,add,step
from centre_scan_data import B,W,U
def full_step(p):
    ds=[];carry=1
    for x in p:
        d,carry=norm(x,carry);ds.append(d)
    assert carry in (1,2)
    if carry==2:ds.append(1<<1)
    return [add(ds[i],ds[-1-i]) for i in range(len(ds))]
for ui in range(3):
    for a,b in ((0,0),(2,11),(18,18),(9,9)):
        X=[1<<v for v in B+W*14+[5]+U[ui]*100+[a,b]]
        K=3;p=X+[ALL]*K+X[::-1]
        for t in range(120):
            X,K,gamma=step(X,K);p=full_step(p)
            assert X+[ALL]*K+X[::-1]==p,(ui,a,b,t,K)
            assert gamma==int(t%4==0)
        print('FULL_MASK_PASS',ui,a,b)
print('1,440 independent full-array abstract transitions PASS')