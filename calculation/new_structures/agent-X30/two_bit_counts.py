"""Exact alphabet of all carry-free two-switch mirror-pair changes, with Q=2 controls."""
def rev4(n):return int(f'{n:04d}'[::-1])
def step(s):
 n=len(s);c=0;out=['0']*n
 for i in range(n-1,-1,-1):
  z=ord(s[i])+ord(s[n-i-1])-96+c
  out[i]=str(z%10);c=z//10
 return ('1' if c else '')+''.join(out)
X='53465346';X1=step(X);X2=step(X1)
found=[]
for x in (0,1):
 for y in (0,1):
  A=90*x+900*y;B=900*x+90*y;options=[]
  for U in range(1000,10000):
   vr=11781+A-U
   if not(0<=vr<=9999):continue
   V=rev4(vr)
   if V+rev4(U)!=11781+B or U//1000==V%10:continue
   s=f'{U:04d}{V:04d}';s1=step(s)
   assert s[0]!=s[-1] and s1[1]!=s1[-2]
   assert step(s1)==X2
   assert (s1==X1)==(x==0 and y==0)
   options.append((U,V,x,y))
  expected=(64 if x==0 else 24)*(64 if y==0 else 24)
  assert len(options)==expected,(x,y,len(options),expected)
  print('x,y',x,y,'count',len(options),'first',options[0])
  found+=options
assert len(found)==7744
print('PASS 7744 distinct symbols, all Q2 exact delayed/one-step merger')
