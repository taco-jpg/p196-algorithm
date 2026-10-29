B=[1,5,10,10,5,8,17,1,4,11,9,9,15,16,7,12,4,3,3,2,3,2,4,7,6,8,6,4,8,12,12,12,9,7]
W=[10,4,5,10,14,13,12,9,7]
U=[9,0,18]
J=[0,1,2]

def pair(J,U,q=14,k=100):
    return B+W*q+J+U*k

def collar_step(a):
    L=len(a)
    # low normalized digits of coefficients
    carry=0; low=[]
    for x in a:
        z=x+carry;low.append(z%10);carry=z//10
    # high end uncertain input carry; certificate for highmost suffix
    high=[];overflow=[]
    for incoming in (0,1):
        d=[];c=incoming
        for x in reversed(a):
            z=x+c; d.append(z%10);c=z//10
        high.append(d[::-1]); overflow.append(c)
    if overflow[0]!=overflow[1]:
        return None,('overflow',L)
    gamma=overflow[0]
    top0,top1=high
    overlap=0
    for i in range(L):
        if top0[i]!=top1[i]:break
        overlap+=1
    # top are reversed d values; first difference at index overlap from high end
    # Pnew prefix[j] needs top coefficient j if gamma0, j-1 if gamma1
    R=min(L,overlap+gamma)
    if gamma:
        b=[low[0]+gamma] + [low[i]+top0[i-1] for i in range(1,R)]
    else:
        b=[low[i]+top0[i] for i in range(R)]
    return b,(gamma,L,R)

def collar_replay(J,U,q=14,k=100,nsteps=120,R0=None):
    a=pair(J,U,q,k)
    H=len(a)
    if R0 is not None:a=a[:R0]
    if len(a)>H:raise Exception()
    record=[]
    for t in range(nsteps):
        b,info=collar_step(a)
        if b is None:return None,(t,info,record)
        a=b;record.append(info)
    target=pair(J,U,q,k+5)
    mismatch=next(((i,x,y) for i,(x,y) in enumerate(zip(a,target)) if x!=y),None)
    return mismatch, (len(a),min(z[2]-z[1] for z in record),sum(z[0] for z in record),record)

def bigint(J,U,C,q=14,k=100,nsteps=120):
    h=pair(J,U,q,k)
    p=h+C+h[::-1]
    assert p==p[::-1]
    d=[0]*len(p)
    for i in range(len(p)//2):
        v=p[i]; d[i]=max(0,v-9);d[-1-i]=min(9,v)
    if len(p)%2:d[len(p)//2]=p[len(p)//2]//2
    n=int(''.join(map(str,d[::-1])))
    assert len(str(n))==len(d)
    for t in range(nsteps):n+=int(str(n)[::-1])
    digs=list(map(int,str(n)[::-1]));pp=[digs[i]+digs[-1-i] for i in range(len(digs))]
    target=pair(J,U,q,k+5); target=target+C+target[::-1]
    mismatch=next(((i,x,y) for i,(x,y) in enumerate(zip(pp,target)) if x!=y),None)
    return mismatch,len(pp),len(target)

if __name__=='__main__':
    for J in ([0,0,0],[18,18,18],[0,1,2],[0,1,2,3],[18,18,18,18]):
        for U in ([9,0,18],[18,0,9],[9,8,10],[9,18,0]):
            res,info=collar_replay(J,U)
            physical=bigint(J,U,[4,4]);print('J',J,'U',U,'collar',res,'info',info[:3],'bigint',physical)