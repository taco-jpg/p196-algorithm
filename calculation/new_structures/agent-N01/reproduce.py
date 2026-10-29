"""N01 locked two-band diagonal pumping, base 10. Run: python3 reproduce.py.
A finite carry-transducer *exactly* certifies one step for every k >= 2.
This is not an infinite reverse-and-add cycle or a Lychrel proof.
"""
from itertools import product
from random import Random
B=(17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,7,9,5,13)
W=(17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13)
V=(4,4,14,1,5,11,7,1,15,12,7,9,9,12,14,4,0,6,5,17,13,9,7,3,13,10,4,13,5,1,9,4,11,6,16,3,7,7,12,4,2,13,2,15,10,10,9,3)
ST=tuple(product((0,1),(0,1),range(10),(0,1)))
IDX={s:i for i,s in enumerate(ST)}
ID=tuple(1<<i for i in range(len(ST)))

def multiply(A,B):
    out=[]
    for bits in A:
        v=0
        while bits:
            j=bits&-bits;v|=B[j.bit_length()-1];bits-=j
        out.append(v)
    return tuple(out)

def symbol(x,y,g):
    table=[]
    for a,h,prev,diff in ST:
        bits=0
        for r in (0,1):
            dl=(x+a)%10;dh=(x+r)%10
            if (x+r)//10==h and y==dl+(prev if g else dh):
                bits|=1<<IDX[((x+a)//10,r,dh,int(bool(diff or dl!=(prev if g else dh))))]
        table.append(bits)
    return tuple(table)

def word(xs,ys,g):
    assert len(xs)==len(ys)
    M=ID
    for x,y in zip(xs,ys):M=multiply(M,symbol(x,y,g))
    return M

def accepted(M,g,src_center,dst_middle,nonpal=True):
    bits=M[IDX[(0,g,g,0)]]
    while bits:
        z=bits&-bits;bits-=z
        a,h,prev,diff=ST[z.bit_length()-1]
        if src_center is None:
            if a!=h or dst_middle!=(2*prev if g else None):continue
        else:
            d=(src_center+a)%10
            if (src_center+a)//10!=h:continue
            if dst_middle!=(d+prev if g else 2*d):continue
            if g:diff=int(bool(diff or d!=prev))
        if diff or not nonpal:return True
    return False

def direct(p):
    # INDEPENDENT reference with ordinary Python integers and divmod.
    n=sum(x*10**j for j,x in enumerate(p)); d=[]
    while n:d.append(n%10);n//=10
    return tuple(d[i]+d[-1-i] for i in range(len(d))), len(d)-len(p), d!=d[::-1]

def normalize(p):
    c=0;d=[]
    for x in p:
        x+=c;d.append(x%10);c=x//10
    if c:d.append(c)
    return tuple(d),c

def nextbulk(w,g):
    def cyc(w):
        for initial in (0,1):
            c=initial;d=[]
            for x in w:
                x+=c;d.append(x%10);c=x//10
            if c==initial:return tuple(d)
        raise AssertionError('no stationary carry')
    lo=cyc(w);hi=cyc(w[::-1])[::-1]
    return tuple(lo[j]+hi[(j-g)%len(w)] for j in range(len(w)))

def source(k):
    h=B+W*k+(9,)+V*k
    return h+(9,)+h[::-1]

def build():
    dst,g,neq=direct(source(2));assert g==1 and neq
    h=dst[:len(dst)//2];a=nextbulk(W,g);v=nextbulk(V,g)
    b=h[:len(B)];start=len(B)+2*len(W)
    assert h[len(B):start]==a*2
    j=h[start:start+1+len(V)];start+=len(j)
    assert h[start:start+len(V)]==v
    c=h[start+len(V):]; assert c==(12,)
    return b,a,j,v,c

def certify():
    b,a,j,v,c=build()
    # Input half: [B W^2] W^t [9 V^2] V^t ; centre = 9.
    # Output half: [b a^2] a^t [j v] v^t [12] ; no centre.
    head=word(B+W*2,b+a*2,1)
    X=word(W,a,1)
    seam=word((9,)+V*2,j+v,1)
    Y=word(V,v,1)
    px=py=ID;seen={};t=0
    while (px,py) not in seen:
        assert t<30,'power semigroup search unexpectedly long'
        seen[px,py]=t
        path=multiply(multiply(multiply(head,px),seam),py)
        assert accepted(path,1,9,12,True),('bad diagonal edge',t)
        px=multiply(px,X);py=multiply(py,Y);t+=1
    mu,period=seen[px,py],t-seen[px,py]
    assert (mu,period)==(1,1)
    print('EXACT all k>=2: two band powers jointly repeat after t=1, period=1; checked t=0,1.')
    print('sizes: B=39, W=20, J=1, V=48; B1=39, W1=20, J1=49, V1=48, C1=1')
    print('B1=',b,'W1=',a,'J1=',j,'V1=',v,'C1=',c)
    for k in (2,3,4,8,15,40):
        q,g,neq=direct(source(k));target=b+a*k+j+v*(k-1)+c
        assert q==target+target[::-1] and g==1 and neq
        print('independent bigint k=',k,'digits=',len(source(k))+1,'PASS')
    rng=Random(20261028)
    for i in range(200):
        n=rng.randrange(1,21);left=[rng.randrange(19) for _ in range(n)];left[0]=rng.randrange(1,19)
        cent= rng.choice((None,rng.randrange(19)))
        p=tuple(left+( [cent] if cent is not None else [])+left[::-1]);q,g,neq=direct(p)
        mat=word(p[:n],q[:n],g)
        assert accepted(mat,g,cent,q[n] if (g or cent is not None) else None,False)
        assert accepted(mat,g,cent,q[n] if (g or cent is not None) else None,True)==neq
    print('independent ordinary-integer two-ended controls: 200 PASS')

if __name__=='__main__':certify()
