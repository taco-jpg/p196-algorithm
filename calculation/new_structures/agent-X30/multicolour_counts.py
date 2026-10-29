"""Independent enumeration of all two-step 4-digit mirror pairs; Q=2 controls."""
def rev4(n):return int(f'{n:04d}'[::-1])
def step(s):
 n=len(s);c=0;out=['0']*n
 for i in range(n-1,-1,-1):
  z=ord(s[i])+ord(s[n-i-1])-96+c
  out[i]=str(z%10);c=z//10
 return ('1' if c else '')+''.join(out)
ref='53465346';ref1=step(ref);ref2=step(ref1)
for k,count in [(0,4096),(1,1536)]:
 pairs=[]
 for U in range(1000,10000):
  r=11781+90*k-U
  if 0<=r<=9999:
   V=rev4(r)
   if rev4(V)==r and V+rev4(U)==11781+900*k and U//1000!=V%10:
    pairs.append((U,V))
 assert len(pairs)==count,(k,len(pairs))
 for U,V in pairs:
  s=f'{U:04d}{V:04d}'
  assert s[0]!=s[-1] and step(s)[1]!=step(s)[-2]
  assert (step(s)==ref1)==(k==0)
  assert step(step(s))==ref2
 print('k=',k,'count=',len(pairs),'Q=2 exact two-step controls PASSED')
