R=[17,5,0,2,1,9,15,18,14,9,3,4,4,14,1,5,11,7,1,15,12,7,9,9,12,14,4,0,6,5,17,8,11,4,18,5,2,12,6,0,0,8,1,12,9]
A=[9,12,10,1,15,12,12,12,16,16,15,0,9,16,1,2,4,5,13,10,16,15,3,10,2,11,6,5,16,5,16,3,7,13,13,5,15,11,15,1,5,7,15,13,16,9,13,13,9,6,0,10,5,15,10,4,17,4,11,9,3,8,0,6,18,2,0,10,12,18,12,10,14,4,0,6,5,17,8,11,4,18,5,2,12,6,0,0,8,1,12,9]
base=R+A
ls=[i//2 for i in base]+[i-i//2 for i in base[::-1]]
n=int(''.join(map(str,ls[::-1])))
seen={}
for t in range(17):
    s=str(n)
    pair=[int(s[j])+int(s[-j-1]) for j in range((len(s)+1)//2)]
    if t in (0,8,16):
       k=len(base)
       wanted=base+A[:4]
       bad=next((j for j,(u,v) in enumerate(zip(pair,wanted)) if u!=v),min(len(pair),len(wanted)))
       print('TIME',t,'digits',len(s),'half',len(pair),'first_bad',bad,'residue',n%9)
       seen[t]=n%9
    assert s!=s[::-1]
    if t<16:n+=int(s[::-1])
assert len(base)==137
assert seen[8]==(4*seen[0])%9
assert seen[16]==(4*seen[8])%9
assert (A[0]+A[1])%9==3 and (A[2]+A[3])%9==2
print('BIGINT-PASS')
