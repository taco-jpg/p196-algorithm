"""AC45: exact binary decision diagram for a decimal column carry gate.
This is a building block, NOT a 120-layer T* decision.
Run: python3 calculation/new_structures/AC45/engine.py
"""
from functools import lru_cache
class BDD:
    def __init__(self):
        self.nodes=[None,None]; self.unique={};self.memo={}
    def node(self,v,l,h):
        if l==h:return l
        k=(v,l,h)
        if k not in self.unique:
            self.unique[k]=len(self.nodes);self.nodes.append(k)
        return self.unique[k]
    def var(self,v):return self.node(v,0,1)
    def apply(self,op,a,b):
        k=(op,a,b)
        if k in self.memo:return self.memo[k]
        if a<2 and b<2:
            return {'and':a&b,'or':a|b,'xor':a^b}[op]
        va=self.nodes[a][0] if a>1 else 9999
        vb=self.nodes[b][0] if b>1 else 9999
        v=min(va,vb)
        al,ah=self.nodes[a][1:] if va==v else (a,a)
        bl,bh=self.nodes[b][1:] if vb==v else (b,b)
        z=self.node(v,self.apply(op,al,bl),self.apply(op,ah,bh))
        self.memo[k]=z;return z
    def equal(self,bits,value):
        z=1
        for i,b in enumerate(bits):
            z=self.apply('and',z,b if value>>i&1 else self.apply('xor',b,1))
        return z
    def count(self,u,n):
        @lru_cache(None)
        def rec(u,j):
            if u<2:return u*(1<<(n-j))
            v,l,h=self.nodes[u]
            return (rec(l,v+1)+rec(h,v+1))<<(v-j)
        return rec(u,0)
    def eval(self,u,a):
        while u>1:
            v,l,h=self.nodes[u];u=h if a>>v&1 else l
        return u
    def reach(self,u):
        seen=set();stack=[u]
        while stack:
            i=stack.pop()
            if i<2 or i in seen:continue
            seen.add(i);stack.extend(self.nodes[i][1:])
        return len(seen)
def reverse(n):return int(str(n)[::-1])
def pw(n):
    d=list(map(int,str(n)[::-1]))
    return [x+y for x,y in zip(d,d[::-1])]
def realize(p):
    assert p==p[::-1] and p
    d=[0]*len(p)
    for i in range(len(p)//2):
        hi=min(9,p[i]);lo=p[i]-hi
        assert 0<=lo<=9
        d[i]=lo;d[-1-i]=hi
    if len(p)%2:
        assert p[len(p)//2]%2==0
        d[len(p)//2]=p[len(p)//2]//2
    assert d[-1]!=0
    return int(''.join(map(str,d[::-1])))
def test():
    import random
    rng=random.Random(45)
    for _ in range(500):
        ds=[rng.randrange(10) for _ in range(rng.randrange(2,60))]
        ds[-1]=rng.randrange(1,10)
        n=int(''.join(map(str,ds[::-1])))
        m=realize(pw(n))
        assert pw(n)==pw(m)
        assert pw(n+reverse(n))==pw(m+reverse(m))
    b=BDD();v=[b.var(i) for i in range(9)];carry=0;valid=0
    for x in range(10):
        for y in range(10):
            term=b.apply('and',b.equal(v[:4],x),b.equal(v[4:8],y))
            valid=b.apply('or',valid,term)
            for c in range(2):
                if x+y+c>=10:
                    t=b.apply('and',term,b.equal(v[8:],c))
                    carry=b.apply('or',carry,t)
    for a in range(512):
        x=a&15;y=a>>4&15;c=a>>8&1
        assert b.eval(valid,a)==int(x<10 and y<10)
        assert b.eval(carry,a)==int(x<10 and y<10 and x+y+c>=10)
    assert b.count(valid,9)==200 and b.count(carry,9)==100
    print(dict(inputs=9,valid=b.count(valid,9),carry_one=b.count(carry,9),
               allocated_nodes=len(b.nodes)-2,carry_reachable=b.reach(carry),
               valid_reachable=b.reach(valid),physical_controls=500))
if __name__=='__main__':test()
