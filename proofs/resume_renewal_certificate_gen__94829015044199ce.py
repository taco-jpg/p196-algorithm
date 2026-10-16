from resume_renewal_normalization import *
def graph(first,hs):
 init=((0,1),tuple((0,h,1 if h else -1)for h in hs),False)
 seen=set();todo=deque()
 for q,ns in norm_edges(init[0]):
  if q!=first:continue
  for tail,r in feed(init[1],q,hs):seen.add((ns,tail,r>9));todo.append((ns,tail,r>9))
 while todo:
  ns,states,bad=todo.popleft()
  for q,nns in norm_edges(ns):
   for tail,r in feed(states,q,hs):
    nxt=(nns,tail,bad or r>9)
    if nxt not in seen:seen.add(nxt);todo.append(nxt)
 def fmt(s):
  (a,b),ss,bad=s
  codes=[x+2*y+4*max(t,0)for x,y,t in ss]
  return '⟨%s, %s, %s⟩'%(a+2*b,str(codes),str(bad).lower())
 return '[\n  '+',\n  '.join(fmt(s)for s in sorted(seen))+'\n]'
if __name__ == '__main__':
 current=open('resume_renewal_certificate.lean').read()
 prefix=current[:current.index('def cert10 :')]
 suffix=current[current.index('theorem cert10_initial'):]
 open('resume_renewal_certificate.lean','w').write(prefix+'def cert10 : List State := '+graph(10,(1,0))+'\n\ndef cert9 : List State := '+graph(9,(1,1,0))+'\n'+suffix)
