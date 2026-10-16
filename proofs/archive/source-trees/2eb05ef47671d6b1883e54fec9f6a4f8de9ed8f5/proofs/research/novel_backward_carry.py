from itertools import product

def carries(q):
 c=0;r=[]
 for x in q:
  c=(x+c)//10;r.append(c)
 return r

def image(q):
 c=0;ds=[]
 for x in q:
  z=x+c;ds.append(z%10);c=z//10
 if c:ds.append(c)
 return [x+y for x,y in zip(ds,ds[::-1])]

def canonical(c):
 q=[]
 for i,(a,b) in enumerate(zip(c,c[::-1])):
  if a!=b:x=9
  elif a==0:x=2 if i in (0,len(c)-1) and not c[-1] else 0
  else:x=10
  q.append(x)
 return q

if __name__=='__main__':
 seen={}
 for L in range(1,8):
  for p in product(range(19),repeat=L//2):
   if p and p[0]==0:continue
   for m in (range(2,19,2) if L==1 else range(0,19,2)) if L%2 else [None]:
    q=list(p)+([m] if m is not None else [])+list(p[::-1])
    c=tuple(carries(q));seen[c]=q
 bad=[]
 for c,q in seen.items():
  qc=canonical(c)
  assert carries(qc)==list(c),(q,c,qc,carries(qc))
  if not c[-1]:assert max(image(qc))<=9,(q,c,qc,image(qc))
  else:
   cur=qc
   for k in range(100):
    if max(cur)<=9 or cur[0]==11 and all(x in (0,11) for x in cur):break
    cur=image(cur)
   else:bad.append((c,qc))
 print('Valid carry words:',len(seen))
 print('Overflow normalized states not terminating within 100:',len(bad))
 print(bad[:10])
