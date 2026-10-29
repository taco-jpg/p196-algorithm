B=[5,2,3,12,16,2,15,10,9,7,18,8,15,9,1,14,0,3,10,0,17,17,9,3,3,15,8,7,9,4,3,3,9,2]
W=[4,0,17,11,9,12,2,9,2]
U=[r for a in range(0,19,2) for w in [(9,a,18-a)] for r in (w,w[1:]+w[:1],w[2:]+w[:2])]
C1=[4,14,4]
C2=[4,4]
def template(j,u,c,q=14,k=100):
    h=B+W*q+list(j)+list(u)*k
    return h+list(c)+h[::-1]
def succ(p):
    d=[];carry=0
    for x in p:
        x+=carry;d.append(x%10);carry=x//10
    if carry:d.append(carry)
    return [x+y for x,y in zip(d,d[::-1])],int(bool(carry))
